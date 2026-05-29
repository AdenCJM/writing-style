#!/usr/bin/env python3
"""Live evaluation of the writing-style skill.

For every prompt in ``cases.json`` this generates two completions:

* **with skill** - SKILL.md is passed as the system prompt
* **baseline**   - no system prompt

Both are scored with the deterministic checker in ``check.py``. The script
reports pass rates, average violations, and token overhead, and writes a
markdown + JSON report. Cases that still fail *with* the skill are listed
separately; those are the inputs ``improve.py`` works from.

Requires ANTHROPIC_API_KEY. If it isn't set (or the anthropic SDK isn't
installed) the script prints a notice and exits 0 so CI stays green.

Env vars:
    ANTHROPIC_API_KEY   required for a live run
    GEN_MODEL           generation model (default: claude-sonnet-4-6)
    TEMPERATURE         sampling temperature (default: 0.0)
    JUDGE               set to 1/true to add an LLM naturalness score
    JUDGE_MODEL         judge model (default: claude-opus-4-8)

Usage:
    python run_eval.py [--out evals/reports/latest] [--max-tokens 1024]
"""

from __future__ import annotations

import argparse
import json
import os
import statistics
import sys
from datetime import datetime, timezone
from pathlib import Path

from check import Report, load_rules

HERE = Path(__file__).resolve().parent
SKILL_PATH = HERE.parent / "SKILL.md"
CASES_PATH = HERE / "cases.json"

GEN_MODEL = os.environ.get("GEN_MODEL", "claude-sonnet-4-6")
JUDGE_MODEL = os.environ.get("JUDGE_MODEL", "claude-opus-4-8")
TEMPERATURE = float(os.environ.get("TEMPERATURE", "0.0"))
USE_JUDGE = os.environ.get("JUDGE", "").lower() in ("1", "true", "yes")

JUDGE_PROMPT = """You are scoring a piece of writing for how human and natural it sounds.

Rate it 1-5 where:
5 = sounds like a sharp, direct human wrote it; varied sentence length; no filler
3 = readable but a bit generic or stiff
1 = obviously AI-generated: padded, over-structured, full of corporate filler

Reply with ONLY a JSON object: {"score": <1-5>, "reason": "<one short sentence>"}

The writing:
---
%s
---"""


def _skip(msg: str) -> int:
    print(f"[run_eval] SKIPPED: {msg}")
    print("[run_eval] Set ANTHROPIC_API_KEY to run a live evaluation.")
    return 0


def generate(client, system: str | None, prompt: str, max_tokens: int) -> tuple[str, int, int]:
    kwargs = dict(model=GEN_MODEL, max_tokens=max_tokens, temperature=TEMPERATURE,
                  messages=[{"role": "user", "content": prompt}])
    if system:
        kwargs["system"] = system
    resp = client.messages.create(**kwargs)
    text = "".join(b.text for b in resp.content if b.type == "text")
    return text, resp.usage.input_tokens, resp.usage.output_tokens


def judge(client, text: str) -> dict:
    resp = client.messages.create(
        model=JUDGE_MODEL, max_tokens=200, temperature=0.0,
        messages=[{"role": "user", "content": JUDGE_PROMPT % text}],
    )
    raw = "".join(b.text for b in resp.content if b.type == "text").strip()
    try:
        start, end = raw.index("{"), raw.rindex("}") + 1
        return json.loads(raw[start:end])
    except (ValueError, json.JSONDecodeError):
        return {"score": None, "reason": "could not parse judge output"}


def summarise(results: list[dict], variant: str) -> dict:
    reports = [r[variant]["report"] for r in results]
    n = len(reports)
    passed = sum(1 for rep in reports if rep["passed"])
    hard = [len(rep["hard"]) for rep in reports]
    out_toks = [r[variant]["output_tokens"] for r in results]
    in_toks = [r[variant]["input_tokens"] for r in results]
    summary = {
        "pass_rate": round(100 * passed / n, 1) if n else 0.0,
        "passed": passed,
        "total": n,
        "avg_hard_violations": round(statistics.mean(hard), 2) if hard else 0.0,
        "avg_input_tokens": round(statistics.mean(in_toks), 1) if in_toks else 0.0,
        "avg_output_tokens": round(statistics.mean(out_toks), 1) if out_toks else 0.0,
    }
    if USE_JUDGE:
        scores = [r[variant].get("judge", {}).get("score") for r in results]
        scores = [s for s in scores if isinstance(s, (int, float))]
        summary["avg_judge_score"] = round(statistics.mean(scores), 2) if scores else None
    return summary


def render_markdown(report: dict) -> str:
    w, b = report["with_skill"], report["baseline"]
    lines = [
        "# Writing-style skill - evaluation report",
        "",
        f"- **Generated:** {report['generated']}",
        f"- **Model:** `{report['model']}` (temperature {report['temperature']})",
        f"- **Cases:** {w['total']}",
        f"- **Judge:** {'on (' + report['judge_model'] + ')' if report['judge'] else 'off'}",
        "",
        "## Results",
        "",
        "| Metric | With skill | Baseline |",
        "|---|---|---|",
        f"| Pass rate | {w['pass_rate']}% | {b['pass_rate']}% |",
        f"| Avg hard violations / output | {w['avg_hard_violations']} | {b['avg_hard_violations']} |",
        f"| Avg output tokens | {w['avg_output_tokens']} | {b['avg_output_tokens']} |",
        f"| Avg input tokens | {w['avg_input_tokens']} | {b['avg_input_tokens']} |",
    ]
    if report["judge"]:
        lines.append(f"| Avg naturalness (1-5) | {w.get('avg_judge_score')} | {b.get('avg_judge_score')} |")

    overhead = report["token_overhead_pct"]
    lines += [
        "",
        f"**Total token overhead of the skill:** {overhead:+.1f}%",
        "",
        "## Per-case breakdown",
        "",
        "| Case | Type | With skill | Baseline |",
        "|---|---|---|---|",
    ]
    for r in report["cases"]:
        wv = "PASS" if r["with_skill"]["report"]["passed"] else f"FAIL ({len(r['with_skill']['report']['hard'])})"
        bv = "PASS" if r["baseline"]["report"]["passed"] else f"FAIL ({len(r['baseline']['report']['hard'])})"
        lines.append(f"| {r['id']} | {r['type']} | {wv} | {bv} |")

    remaining = report["remaining_failures"]
    lines += ["", "## Remaining failures (with skill applied)", ""]
    if not remaining:
        lines.append("None. Every case passed with the skill applied.")
    else:
        for rf in remaining:
            tells = ", ".join(f"{f['kind']}:{f['match']}" for f in rf["hard"])
            lines.append(f"- **{rf['id']}**: {tells}")
    lines.append("")
    return "\n".join(lines)


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", default=str(HERE / "reports" / "latest"))
    parser.add_argument("--max-tokens", type=int, default=1024)
    args = parser.parse_args(argv)

    if not os.environ.get("ANTHROPIC_API_KEY"):
        return _skip("ANTHROPIC_API_KEY not set")
    try:
        import anthropic
    except ImportError:
        return _skip("anthropic SDK not installed (pip install -r evals/requirements.txt)")

    rules = load_rules(SKILL_PATH)
    skill = SKILL_PATH.read_text(encoding="utf-8")
    cases = json.loads(CASES_PATH.read_text(encoding="utf-8"))["cases"]
    client = anthropic.Anthropic()

    print(f"[run_eval] model={GEN_MODEL} cases={len(cases)} judge={USE_JUDGE}")
    results = []
    for case in cases:
        print(f"[run_eval] {case['id']} ...", flush=True)
        row = {"id": case["id"], "type": case["type"], "prompt": case["prompt"]}
        for variant, system in (("with_skill", skill), ("baseline", None)):
            text, in_tok, out_tok = generate(client, system, case["prompt"], args.max_tokens)
            rep: Report = rules.check(text)
            entry = {
                "text": text,
                "input_tokens": in_tok,
                "output_tokens": out_tok,
                "report": rep.to_dict(),
            }
            if USE_JUDGE:
                entry["judge"] = judge(client, text)
            row[variant] = entry
        results.append(row)

    with_sum = summarise(results, "with_skill")
    base_sum = summarise(results, "baseline")

    w_total = with_sum["avg_input_tokens"] + with_sum["avg_output_tokens"]
    b_total = base_sum["avg_input_tokens"] + base_sum["avg_output_tokens"]
    overhead = 100 * (w_total - b_total) / b_total if b_total else 0.0

    remaining = [
        {"id": r["id"], "type": r["type"], "prompt": r["prompt"],
         "text": r["with_skill"]["text"], "hard": r["with_skill"]["report"]["hard"]}
        for r in results if not r["with_skill"]["report"]["passed"]
    ]

    report = {
        "generated": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "model": GEN_MODEL,
        "temperature": TEMPERATURE,
        "judge": USE_JUDGE,
        "judge_model": JUDGE_MODEL if USE_JUDGE else None,
        "with_skill": with_sum,
        "baseline": base_sum,
        "token_overhead_pct": round(overhead, 1),
        "remaining_failures": remaining,
        "cases": results,
    }

    out_base = Path(args.out)
    out_base.parent.mkdir(parents=True, exist_ok=True)
    (out_base.with_suffix(".json")).write_text(json.dumps(report, indent=2), encoding="utf-8")
    md = render_markdown(report)
    (out_base.with_suffix(".md")).write_text(md, encoding="utf-8")

    print("\n" + md)
    print(f"\n[run_eval] wrote {out_base.with_suffix('.json')} and {out_base.with_suffix('.md')}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
