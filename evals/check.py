#!/usr/bin/env python3
"""Deterministic checker for the writing-style skill.

The checker parses the rules straight out of ``SKILL.md`` so it always tests the
current version of the skill rather than a hard-coded copy. It reports two kinds
of findings:

* **hard violations** - unambiguous AI tells (banned words with no context
  qualifier, em dashes, American spelling). Any of these fails an output.
* **soft warnings** - context-dependent issues the checker can't judge reliably
  (e.g. "leverage" is only banned outside finance, uncontracted "it is" is only
  banned in casual writing). These are reported but never fail an output.

Usage:
    python check.py file1.md file2.md ...   # check files, print findings
    python check.py --json file.md          # machine-readable output
    python check.py --selftest              # validate the checker against fixtures
"""

from __future__ import annotations

import json
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SKILL_PATH = REPO_ROOT / "SKILL.md"
FIXTURES = Path(__file__).resolve().parent / "fixtures"

# A bullet is treated as context-dependent (soft) if its parenthetical note
# narrows where the word is banned. Otherwise the word is an unconditional tell.
RESTRICTION_KEYWORDS = (
    "outside",
    "when ",
    "metaphor",
    "as a ",
    "standalone",
    "as filler",
)

# Connectors are only banned as sentence openers, so they get position-aware
# detection instead of a plain word match.
SENTENCE_OPENERS = {"moreover", "furthermore", "additionally"}

# High-confidence American spellings mapped to their Australian form. Kept
# conservative on purpose: anything ambiguous (program, license, meter) is left
# out to avoid false positives.
US_SPELLING_MAP = {
    "color": "colour", "colors": "colours", "colored": "coloured",
    "coloring": "colouring", "flavor": "flavour", "flavors": "flavours",
    "flavored": "flavoured", "honor": "honour", "honors": "honours",
    "honored": "honoured", "honorable": "honourable", "favor": "favour",
    "favors": "favours", "favored": "favoured", "favorite": "favourite",
    "favorites": "favourites", "favorable": "favourable", "behavior": "behaviour",
    "behaviors": "behaviours", "neighbor": "neighbour", "neighbors": "neighbours",
    "rumor": "rumour", "rumors": "rumours", "humor": "humour",
    "humored": "humoured", "harbor": "harbour", "harbors": "harbours",
    "vapor": "vapour", "savor": "savour", "savory": "savoury", "valor": "valour",
    "vigor": "vigour", "odor": "odour", "odors": "odours", "armor": "armour",
    "endeavor": "endeavour", "endeavors": "endeavours", "splendor": "splendour",
    "candor": "candour", "clamor": "clamour", "parlor": "parlour",
    "tumor": "tumour", "tumors": "tumours", "demeanor": "demeanour",
    "defense": "defence", "defenses": "defences", "offense": "offence",
    "offenses": "offences", "pretense": "pretence",
    "center": "centre", "centers": "centres", "centered": "centred",
    "theater": "theatre", "theaters": "theatres", "fiber": "fibre",
    "fibers": "fibres", "liter": "litre", "liters": "litres",
    "caliber": "calibre", "specter": "spectre", "gray": "grey",
    "mold": "mould", "molds": "moulds", "smolder": "smoulder",
    "catalog": "catalogue", "catalogs": "catalogues", "dialog": "dialogue",
    "dialogs": "dialogues", "analog": "analogue", "traveled": "travelled",
    "traveling": "travelling", "traveler": "traveller", "travelers": "travellers",
    "canceled": "cancelled", "canceling": "cancelling", "modeled": "modelled",
    "modeling": "modelling", "labeled": "labelled", "labeling": "labelling",
    "fueled": "fuelled", "fueling": "fuelling", "signaled": "signalled",
    "signaling": "signalling", "totaled": "totalled", "jewelry": "jewellery",
    "plow": "plough", "aluminum": "aluminium", "maneuver": "manoeuvre",
    "maneuvers": "manoeuvres", "mustache": "moustache", "esthetic": "aesthetic",
    "pajamas": "pyjamas", "enrollment": "enrolment", "fulfill": "fulfil",
    "fulfillment": "fulfilment", "installment": "instalment", "skillful": "skilful",
}

# Legitimate -ize / -yze words that should NOT be flagged by the long-tail regex.
IZE_ALLOWLIST = {
    "size", "sizes", "sized", "sizing", "resize", "resizes", "resized",
    "resizing", "downsize", "downsized", "upsize", "midsize", "oversize",
    "prize", "prizes", "prized", "seize", "seizes", "seized", "seizing",
    "capsize", "capsized", "maize",
}


@dataclass
class Finding:
    kind: str          # "banned-word", "em-dash", "us-spelling", "construction", "uncontracted"
    match: str         # the offending text
    suggestion: str = ""
    context: str = ""  # short snippet around the match


@dataclass
class Report:
    path: str = ""
    hard: list[Finding] = field(default_factory=list)
    soft: list[Finding] = field(default_factory=list)

    @property
    def passed(self) -> bool:
        return not self.hard

    def to_dict(self) -> dict:
        return {
            "path": self.path,
            "passed": self.passed,
            "hard": [f.__dict__ for f in self.hard],
            "soft": [f.__dict__ for f in self.soft],
        }


@dataclass
class Rules:
    hard_words: list[str]      # single words / hyphenated, unconditional
    hard_phrases: list[str]    # multi-word phrases, unconditional
    soft_words: list[str]      # context-dependent words
    soft_phrases: list[str]

    # Compiled lazily in __post_init__
    def __post_init__(self) -> None:
        self._hard_word_re = _word_regex(self.hard_words)
        self._hard_phrase_re = _phrase_regex(self.hard_phrases)
        self._soft_word_re = _word_regex(self.soft_words)
        self._soft_phrase_re = _phrase_regex(self.soft_phrases)
        self._opener_re = re.compile(
            r"(?:(?<=[.!?])\s+|^|\n\s*)(" + "|".join(SENTENCE_OPENERS) + r")\b",
            re.IGNORECASE,
        )
        us_terms = sorted(US_SPELLING_MAP, key=len, reverse=True)
        self._us_re = re.compile(r"\b(" + "|".join(map(re.escape, us_terms)) + r")\b", re.IGNORECASE)
        self._ize_re = re.compile(r"\b([a-z]+(?:iz|yz)(?:e|es|ed|ing|ation|ations|er|ers))\b", re.IGNORECASE)
        self._uncontracted_re = re.compile(r"\b(it|there|that|here)\s+is\b", re.IGNORECASE)
        # "not X, it's/it is Y" template (and isn't/aren't variants).
        self._template_re = re.compile(
            r"\b(?:is|are|isn't|aren't|it's|they're)\b[^.!?\n]{0,8}\bnot\b[^.!?\n]{1,60},\s+(?:it's|it is|they're|they are|but rather|rather)\b",
            re.IGNORECASE,
        )

    def check(self, text: str) -> Report:
        text = _normalise(text)
        report = Report()

        for m in self._hard_word_re.finditer(text) if self._hard_word_re else []:
            report.hard.append(Finding("banned-word", m.group(0), context=_ctx(text, m)))
        for m in self._hard_phrase_re.finditer(text) if self._hard_phrase_re else []:
            report.hard.append(Finding("banned-phrase", m.group(0), context=_ctx(text, m)))
        for m in self._opener_re.finditer(text):
            report.hard.append(Finding("banned-opener", m.group(1), context=_ctx(text, m)))

        # Em dash U+2014, plus the classic typed "word--word" substitute. En
        # dash U+2013 is allowed for ranges. The lookarounds keep this off
        # markdown table rules (|---|), frontmatter (---), and CLI flags.
        for m in re.finditer(r"—|(?<=\w)--(?=\w)", text):
            report.hard.append(Finding("em-dash", m.group(0), suggestion="comma, full stop, or rewrite", context=_ctx(text, m)))

        # American spelling: explicit map first, then long-tail -ize/-yze regex.
        seen_spans: set[tuple[int, int]] = set()
        for m in self._us_re.finditer(text):
            seen_spans.add(m.span())
            au = US_SPELLING_MAP[m.group(0).lower()]
            report.hard.append(Finding("us-spelling", m.group(0), suggestion=au, context=_ctx(text, m)))
        for m in self._ize_re.finditer(text):
            if m.span() in seen_spans or m.group(0).lower() in IZE_ALLOWLIST:
                continue
            report.hard.append(Finding("us-spelling", m.group(0), suggestion="use -ise/-yse spelling", context=_ctx(text, m)))

        # Soft warnings - context-dependent, never fail an output.
        for m in self._soft_word_re.finditer(text) if self._soft_word_re else []:
            report.soft.append(Finding("context-word", m.group(0), context=_ctx(text, m)))
        for m in self._soft_phrase_re.finditer(text) if self._soft_phrase_re else []:
            report.soft.append(Finding("context-phrase", m.group(0), context=_ctx(text, m)))
        for m in self._uncontracted_re.finditer(text):
            report.soft.append(Finding("uncontracted", m.group(0), suggestion="use a contraction", context=_ctx(text, m)))
        for m in self._template_re.finditer(text):
            report.soft.append(Finding("construction", m.group(0)[:60], suggestion='avoid "not X, it\'s Y"', context=_ctx(text, m)))

        return report


def _normalise(text: str) -> str:
    return text.replace("’", "'").replace("‘", "'")


def _ctx(text: str, m: re.Match, width: int = 30) -> str:
    start = max(0, m.start() - width)
    end = min(len(text), m.end() + width)
    snippet = text[start:end].replace("\n", " ").strip()
    return ("..." if start > 0 else "") + snippet + ("..." if end < len(text) else "")


def _word_regex(words: list[str]) -> re.Pattern | None:
    if not words:
        return None
    return re.compile(r"\b(" + "|".join(re.escape(w) for w in words) + r")\b", re.IGNORECASE)


def _phrase_regex(phrases: list[str]) -> re.Pattern | None:
    if not phrases:
        return None
    parts = []
    for p in phrases:
        tokens = _normalise(p).split()
        parts.append(r"\b" + r"\s+".join(re.escape(t) for t in tokens) + r"\b")
    return re.compile("(" + "|".join(parts) + ")", re.IGNORECASE)


def load_rules(skill_path: Path = SKILL_PATH) -> Rules:
    """Parse the banned-words section out of a SKILL.md file."""
    return parse_rules(skill_path.read_text(encoding="utf-8"))


def parse_rules(text: str) -> Rules:
    """Parse the banned-words section out of skill text."""
    section = _extract_section(text, "### Banned words and phrases")

    hard_words: list[str] = []
    hard_phrases: list[str] = []
    soft_words: list[str] = []
    soft_phrases: list[str] = []

    for line in section.splitlines():
        line = line.strip()
        if not line.startswith("- "):
            continue
        body = line[2:].strip()

        paren = re.search(r"\(([^)]*)\)", body)
        note = paren.group(1).lower() if paren else ""
        is_soft = any(k in note for k in RESTRICTION_KEYWORDS)

        term_str = re.sub(r"\([^)]*\)", "", body).strip()
        for variant in term_str.split("/"):
            variant = variant.strip()
            if not variant:
                continue
            lowered = variant.lower()
            if lowered in SENTENCE_OPENERS:
                continue  # handled by the opener regex
            is_phrase = " " in variant
            if is_soft:
                (soft_phrases if is_phrase else soft_words).append(variant)
            else:
                (hard_phrases if is_phrase else hard_words).append(variant)

    return Rules(hard_words, hard_phrases, soft_words, soft_phrases)


def _extract_section(text: str, heading: str) -> str:
    lines = text.splitlines()
    out: list[str] = []
    capturing = False
    for line in lines:
        if line.strip() == heading:
            capturing = True
            continue
        if capturing and line.startswith("#"):
            break
        if capturing:
            out.append(line)
    return "\n".join(out)


def format_report(report: Report) -> str:
    lines = []
    status = "PASS" if report.passed else "FAIL"
    header = f"[{status}] {report.path}" if report.path else f"[{status}]"
    lines.append(header)
    for f in report.hard:
        lines.append(f"  HARD {f.kind}: '{f.match}'" + (f" -> {f.suggestion}" if f.suggestion else ""))
        if f.context:
            lines.append(f"       in: {f.context}")
    for f in report.soft:
        lines.append(f"  soft {f.kind}: '{f.match}'" + (f" -> {f.suggestion}" if f.suggestion else ""))
    return "\n".join(lines)


# --------------------------------------------------------------------------- #
# Self-test: proves the checker catches what it should and passes clean text.
# --------------------------------------------------------------------------- #

def validate_skill(skill_text: str) -> list[str]:
    """Check that candidate skill text is well-formed and self-consistent.

    Returns a list of problems; an empty list means the skill parses, keeps the
    expected structure, its own Good/Bad examples agree with its rules, and the
    fixtures still behave. Used by both the self-test and improve.py so a
    proposed change can never be accepted unless it still holds together.
    """
    problems: list[str] = []

    if not skill_text.lstrip().startswith("---"):
        problems.append("missing YAML frontmatter")
    if "### Banned words and phrases" not in skill_text:
        problems.append("missing '### Banned words and phrases' section")

    try:
        rules = parse_rules(skill_text)
    except Exception as exc:  # noqa: BLE001 - report any parse failure as a problem
        problems.append(f"failed to parse rules: {exc}")
        return problems

    if not rules.hard_words and not rules.hard_phrases:
        problems.append("parsed zero hard-banned terms")

    # The skill's own examples must agree with its rules.
    for label, block in _skill_examples(skill_text).items():
        rep = rules.check(block)
        if label == "good" and not rep.passed:
            problems.append(f"'Good' example violates the rules: {[f.match for f in rep.hard]}")
        if label == "bad" and rep.passed:
            problems.append("'Bad' example is not caught by the checker")

    # Fixtures must still behave under the candidate rules.
    for fp in sorted(FIXTURES.glob("*.md")) if FIXTURES.exists() else []:
        rep = rules.check(fp.read_text(encoding="utf-8"))
        if fp.name.startswith("good_") and not rep.passed:
            problems.append(f"{fp.name} should PASS but failed: {[f.match for f in rep.hard]}")
        if fp.name.startswith("bad_") and rep.passed:
            problems.append(f"{fp.name} should be CAUGHT but passed clean")

    return problems


def _selftest() -> int:
    fixture_files = sorted(FIXTURES.glob("*.md")) if FIXTURES.exists() else []
    failures = validate_skill(SKILL_PATH.read_text(encoding="utf-8"))
    if not fixture_files:
        failures.append("no fixtures found in evals/fixtures/")

    if failures:
        print("SELFTEST FAILED:")
        for f in failures:
            print(f"  - {f}")
        return 1
    rules = load_rules()
    print(f"SELFTEST PASSED ({len(fixture_files)} fixtures, {len(US_SPELLING_MAP)} mapped spellings)")
    print(f"  parsed {len(rules.hard_words)} hard words, {len(rules.hard_phrases)} hard phrases, "
          f"{len(rules.soft_words)} soft words")
    return 0


def _skill_examples(text: str | None = None) -> dict[str, str]:
    """Pull the **Bad** / **Good** blockquote examples out of skill text."""
    if text is None:
        text = SKILL_PATH.read_text(encoding="utf-8")
    examples: dict[str, list[str]] = {"good": [], "bad": []}
    current: str | None = None
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith("**Bad"):
            current = "bad"
        elif stripped.startswith("**Good"):
            current = "good"
        elif stripped.startswith("> ") and current:
            examples[current].append(stripped[2:])
        elif current and not stripped.startswith(">") and stripped:
            current = None
    return {k: "\n".join(v) for k, v in examples.items() if v}


def main(argv: list[str]) -> int:
    if "--selftest" in argv:
        return _selftest()

    as_json = "--json" in argv
    paths = [a for a in argv if not a.startswith("--")]
    if not paths:
        print(__doc__)
        return 0

    rules = load_rules()
    reports = []
    any_fail = False
    for p in paths:
        rep = rules.check(Path(p).read_text(encoding="utf-8"))
        rep.path = p
        reports.append(rep)
        any_fail = any_fail or not rep.passed

    if as_json:
        print(json.dumps([r.to_dict() for r in reports], indent=2))
    else:
        for r in reports:
            print(format_report(r))
    return 1 if any_fail else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
