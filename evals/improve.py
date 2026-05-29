#!/usr/bin/env python3
"""Propose evidence-driven improvements to the writing-style skill.

Reads an evaluation report (from ``run_eval.py``), gathers the cases that still
failed with the skill applied plus the AI tells the baseline reached for, and
asks a model to propose *minimal* edits to SKILL.md - new banned words, tighter
rules, clearer scope. The proposed skill is then run through
``check.validate_skill`` and is only written to disk if it still parses and stays
self-consistent. A change that breaks the harness is rejected.

The script never opens a PR itself; the workflow does that from the diff it
leaves in the working tree.

Requires ANTHROPIC_API_KEY. Without it (or without the anthropic SDK) the
script prints a notice and exits 0.

Env vars:
    ANTHROPIC_API_KEY   required
    IMPROVE_MODEL       model to use (default: claude-opus-4-8)

Usage:
    python improve.py [--report evals/reports/latest.json] [--notes evals/reports/improvement-notes.md]
"""

from __future__ import annotations

import argparse
import collections
import difflib
import json
import os
import re
import sys
from pathlib import Path

from check import load_rules, validate_skill

HERE = Path(__file__).resolve().parent
SKILL_PATH = HERE.parent / "SKILL.md"
IMPROVE_MODEL = os.environ.get("IMPROVE_MODEL", "claude-opus-4-8")

SYSTEM = """You maintain a Claude Code "writing-style" skill: a single SKILL.md that enforces
Australian English, bans AI-tell words and phrases, kills em dashes, and pushes a direct,
human tone. You are given the current SKILL.md and evidence from an automated evaluation.

Propose the SMALLEST useful change that would raise the skill's pass rate or close a real gap.
Allowed changes:
- add genuinely AI-tell words or phrases (seen in the evidence) to the banned list
- tighten or clarify an existing rule that is being missed
- improve the self-check list so the model catches the failure itself

Rules:
- Do NOT remove existing rules or banned words.
- Do NOT change the frontmatter `name`.
- Keep Australian English and the existing structure and headings.
- Keep every example consistent with the rules (Good examples must obey them; Bad must break them).
- Be conservative: if the evidence doesn't justify a change, say so.

Output format:
- First, 2-4 sentences of rationale describing exactly what you changed and why.
- Then, if and only if you are changing the file, output the COMPLETE updated SKILL.md inside a
  single fenced code block tagged `skill`, like:
  ```skill
  ...entire file...
  ```
- If no change is warranted, write the line `NO CHANGE` and a one-sentence reason, with no code block."""

USER_TEMPLATE = """## Current SKILL.md

```markdown
{skill}
```

## Evaluation evidence

Model: {model}
Pass rate with skill: {with_rate}%   Baseline: {base_rate}%

### Cases that STILL FAILED with the skill applied
{remaining}

### AI tells the BASELINE reached for (frequency across baseline outputs)
These hint at words/phrases worth banning if they aren't already covered:
{baseline_tells}

Propose the smallest change that helps."""


def _skip(msg: str) -> int:
    print(f"[improve] SKIPPED: {msg}")
    return 0


def _format_remaining(remaining: list[dict]) -> str:
    if not remaining:
        return "None - every case passed with the skill applied. A change may not be needed."
    lines = []
    for rf in remaining[:20]:
        tells = ", ".join(f"{f['kind']}:{f['match']}" for f in rf["hard"])
        snippet = rf.get("text", "").strip().replace("\n", " ")[:200]
        lines.append(f"- [{rf['id']}] tells: {tells}\n    output: \"{snippet}...\"")
    return "\n".join(lines)


def _baseline_tells(report: dict) -> str:
    counter: collections.Counter = collections.Counter()
    for case in report.get("cases", []):
        base = case.get("baseline", {}).get("report", {})
        for f in base.get("hard", []) + base.get("soft", []):
            counter[f["match"].lower()] += 1
    if not counter:
        return "None recorded."
    return "\n".join(f"- {word} (x{n})" for word, n in counter.most_common(25))


def _extract(reply: str) -> tuple[str, str | None]:
    """Return (rationale, new_skill_or_None)."""
    m = re.search(r"```(?:skill|markdown)?\s*\n(.*?)```", reply, re.DOTALL)
    if not m:
        return reply.strip(), None
    rationale = reply[: m.start()].strip()
    return rationale, m.group(1).strip() + "\n"


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--report", default=str(HERE / "reports" / "latest.json"))
    parser.add_argument("--notes", default=str(HERE / "reports" / "improvement-notes.md"))
    args = parser.parse_args(argv)

    if not os.environ.get("ANTHROPIC_API_KEY"):
        return _skip("ANTHROPIC_API_KEY not set")
    try:
        import anthropic
    except ImportError:
        return _skip("anthropic SDK not installed (pip install -r evals/requirements.txt)")

    report_path = Path(args.report)
    if not report_path.exists():
        return _skip(f"report not found at {report_path} (run run_eval.py first)")

    report = json.loads(report_path.read_text(encoding="utf-8"))
    current = SKILL_PATH.read_text(encoding="utf-8")

    user = USER_TEMPLATE.format(
        skill=current,
        model=report.get("model", "?"),
        with_rate=report.get("with_skill", {}).get("pass_rate", "?"),
        base_rate=report.get("baseline", {}).get("pass_rate", "?"),
        remaining=_format_remaining(report.get("remaining_failures", [])),
        baseline_tells=_baseline_tells(report),
    )

    client = anthropic.Anthropic()
    print(f"[improve] model={IMPROVE_MODEL}")
    resp = client.messages.create(
        model=IMPROVE_MODEL, max_tokens=4096, temperature=0.0,
        system=SYSTEM, messages=[{"role": "user", "content": user}],
    )
    reply = "".join(b.text for b in resp.content if b.type == "text")
    rationale, new_skill = _extract(reply)

    notes_path = Path(args.notes)
    notes_path.parent.mkdir(parents=True, exist_ok=True)

    if new_skill is None:
        notes_path.write_text(f"# No change proposed\n\n{rationale}\n", encoding="utf-8")
        print(f"[improve] no change proposed.\n\n{rationale}")
        return 0

    problems = validate_skill(new_skill)
    if problems:
        body = "# Proposed change REJECTED (failed validation)\n\n## Rationale\n" + rationale
        body += "\n\n## Validation problems\n" + "\n".join(f"- {p}" for p in problems) + "\n"
        notes_path.write_text(body, encoding="utf-8")
        print("[improve] proposed change rejected - it broke validation:")
        for p in problems:
            print(f"  - {p}")
        return 0

    if new_skill.strip() == current.strip():
        notes_path.write_text(f"# No effective change\n\n{rationale}\n", encoding="utf-8")
        print("[improve] proposal was identical to the current skill.")
        return 0

    diff = "".join(difflib.unified_diff(
        current.splitlines(keepends=True), new_skill.splitlines(keepends=True),
        fromfile="SKILL.md (before)", tofile="SKILL.md (after)",
    ))

    old_rules, new_rules = load_rules(), None
    SKILL_PATH.write_text(new_skill, encoding="utf-8")
    new_rules = load_rules()
    added = sorted(set(new_rules.hard_words + new_rules.hard_phrases)
                   - set(old_rules.hard_words + old_rules.hard_phrases))

    body = [
        "# Proposed writing-style improvement", "",
        "## Rationale", rationale, "",
        f"## New hard-banned terms ({len(added)})",
        ("\n".join(f"- {t}" for t in added) if added else "_none_"), "",
        "## Diff", "```diff", diff.rstrip(), "```", "",
    ]
    notes_path.write_text("\n".join(body), encoding="utf-8")
    print(f"[improve] wrote updated SKILL.md and notes to {notes_path}")
    print(f"[improve] new hard-banned terms: {added or 'none'}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
