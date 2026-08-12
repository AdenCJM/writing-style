#!/usr/bin/env python3
"""Validate the writing-style skill repository without third-party packages."""

from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path
from urllib.parse import unquote


ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "SKILL.md"
OPENAI_YAML = ROOT / "agents" / "openai.yaml"
EVAL_PROMPTS = ROOT / "eval" / "PROMPTS.md"


def fail(errors: list[str], message: str) -> None:
    errors.append(message)


def quoted_yaml_value(text: str, key: str) -> str | None:
    match = re.search(rf'^\s*{re.escape(key)}:\s*"([^"]*)"\s*$', text, re.MULTILINE)
    return match.group(1) if match else None


def strip_fenced_code(text: str) -> str:
    """Remove Markdown fenced blocks while preserving prose between them."""

    return split_fenced_code(text)[0]


def split_fenced_code(text: str) -> tuple[str, bool]:
    """Strip fenced blocks; also report whether a fence was left open at EOF."""

    prose: list[str] = []
    fence_character: str | None = None
    fence_length = 0

    for line in text.splitlines(keepends=True):
        content = line.rstrip("\r\n")
        line_break = line[len(content) :]

        if fence_character is None:
            opening = re.match(r"^ {0,3}(`{3,}|~{3,})(.*)$", content)
            if opening:
                marker = opening.group(1)
                info = opening.group(2)
                if marker[0] == "`" and "`" in info:
                    prose.append(line)
                    continue
                fence_character = marker[0]
                fence_length = len(marker)
                prose.append(line_break)
                continue

            prose.append(line)
            continue

        closing = re.match(
            rf"^ {{0,3}}{re.escape(fence_character)}{{{fence_length},}}[ \t]*$",
            content,
        )
        if closing:
            fence_character = None
            fence_length = 0
        prose.append(line_break)

    return "".join(prose), fence_character is not None


def validate_fence_stripping(errors: list[str]) -> None:
    probe = (
        "```text\n[hidden](missing-hidden.md)\n````\n"
        "[ordinary](missing-prose.md)\n"
        "```text\n[also hidden](missing-hidden-two.md)\n```\n"
    )
    prose = strip_fenced_code(probe)
    if "[ordinary](missing-prose.md)" not in prose:
        fail(errors, "Markdown fence parser removed prose between fenced blocks")
    if "missing-hidden" in prose:
        fail(errors, "Markdown fence parser retained a link inside fenced code")

    nested_probe = (
        "````markdown\n"
        "```sh\n[nested](missing-nested.md)\n```\n"
        "[inside outer](missing-inside.md)\n"
        "````\n"
        "[after](missing-after.md)\n"
    )
    nested_prose, nested_open = split_fenced_code(nested_probe)
    if "missing-nested" in nested_prose or "missing-inside" in nested_prose:
        fail(errors, "Markdown fence parser retained a link inside a longer outer fence")
    if "[after](missing-after.md)" not in nested_prose:
        fail(errors, "Markdown fence parser removed prose after a nested fenced block")
    if nested_open:
        fail(errors, "Markdown fence parser reported a closed nested fence as open")

    _, unclosed_open = split_fenced_code("```text\n[hidden](missing-open.md)\n")
    if not unclosed_open:
        fail(errors, "Markdown fence parser missed an unclosed fence at end of file")

    inline_probe = "```a`b\n[visible](missing-visible.md)\n"
    inline_prose, _ = split_fenced_code(inline_probe)
    if "[visible](missing-visible.md)" not in inline_prose:
        fail(errors, "Markdown fence parser treated a backtick info string as a fence")


def validate_skill(errors: list[str]) -> None:
    text = SKILL.read_text(encoding="utf-8")
    match = re.match(r"\A---\n(.*?)\n---\n", text, re.DOTALL)
    if not match:
        fail(errors, "SKILL.md must start with valid YAML frontmatter delimiters")
        return

    frontmatter = match.group(1)
    keys = re.findall(r"^([a-zA-Z][a-zA-Z0-9_-]*):", frontmatter, re.MULTILINE)
    if set(keys) != {"name", "description"}:
        fail(errors, "SKILL.md frontmatter must contain only name and description")

    name_match = re.search(r"^name:\s*([^\n]+)$", frontmatter, re.MULTILINE)
    name = name_match.group(1).strip() if name_match else ""
    if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", name):
        fail(errors, "skill name must use lowercase hyphen-case")
    if len(name) > 64:
        fail(errors, "skill name must be at most 64 characters")
    if name != "writing-style":
        fail(errors, "public skill name must be writing-style")

    description_match = re.search(
        r"^description:\s*>-\n(?P<body>(?:[ \t]+.*\n?)*)", frontmatter, re.MULTILINE
    )
    if not description_match:
        fail(errors, "description must use a folded YAML block")
    else:
        lines = [line.strip() for line in description_match.group("body").splitlines()]
        description = " ".join(line for line in lines if line)
        if not description:
            fail(errors, "description must not be empty")
        if len(description) > 1024:
            fail(errors, "description must be at most 1,024 characters")
        if "<" in description or ">" in description:
            fail(errors, "description must not contain angle brackets")

    body = text[match.end() :]
    if len(body.splitlines()) >= 500:
        fail(errors, "SKILL.md body must stay under 500 lines")
    if len(re.findall(r"\b\w+\b", body)) >= 5000:
        fail(errors, "SKILL.md body must stay under 5,000 words")


def parse_restricted_yaml(text: str) -> tuple[dict[str, dict[str, str]], list[str]]:
    """Parse the two-level mapping agents/openai.yaml uses, rejecting duplicates."""
    problems: list[str] = []
    root: dict[str, dict[str, str]] = {}
    current: str | None = None
    for line_number, raw_line in enumerate(text.splitlines(), start=1):
        line = raw_line.rstrip()
        if not line or line.lstrip().startswith("#"):
            continue
        match = re.fullmatch(r"( *)([A-Za-z_][A-Za-z0-9_-]*):(?: (.*))?", line)
        if not match:
            problems.append(f"line {line_number} is not a simple key or key-value entry")
            continue
        indent, key, value = match.group(1), match.group(2), match.group(3)
        if indent == "":
            if value:
                problems.append(f"top-level key {key} must be a mapping, not a value")
                continue
            if key in root:
                problems.append(f"duplicate top-level key: {key}")
            else:
                root[key] = {}
            current = key
        else:
            if current is None:
                problems.append(f"line {line_number} is indented under no mapping")
                continue
            if value is None:
                problems.append(f"nested key {key} must carry a value")
                continue
            if key in root[current]:
                problems.append(f"duplicate key {key} under {current}")
            else:
                root[current][key] = value
    return root, problems


def unquote_yaml_scalar(value: str | None) -> str | None:
    if value is None:
        return None
    match = re.fullmatch(r'"([^"]*)"', value)
    return match.group(1) if match else None


def validate_openai_yaml(errors: list[str]) -> None:
    text = OPENAI_YAML.read_text(encoding="utf-8")
    if "\t" in text:
        fail(errors, "agents/openai.yaml must not contain tabs")

    parsed, problems = parse_restricted_yaml(text)
    for problem in problems:
        fail(errors, f"agents/openai.yaml: {problem}")

    allowed = {
        "interface": {"display_name", "short_description", "default_prompt"},
        "policy": {"allow_implicit_invocation"},
    }
    for top_key, nested in parsed.items():
        if top_key not in allowed:
            fail(errors, f"agents/openai.yaml has an unexpected mapping: {top_key}")
            continue
        for nested_key in nested:
            if nested_key not in allowed[top_key]:
                fail(errors, f"agents/openai.yaml has an unexpected key: {top_key}.{nested_key}")
    for required_top in allowed:
        if required_top not in parsed:
            fail(errors, f"agents/openai.yaml is missing the {required_top} mapping")

    interface = parsed.get("interface", {})
    display_name = unquote_yaml_scalar(interface.get("display_name"))
    if not display_name:
        fail(errors, "agents/openai.yaml needs a quoted, non-empty display_name")

    short_description = unquote_yaml_scalar(interface.get("short_description"))
    if short_description is None:
        fail(errors, "agents/openai.yaml needs a quoted short_description")
    elif not 25 <= len(short_description) <= 64:
        fail(errors, "short_description must contain 25–64 characters")

    default_prompt = unquote_yaml_scalar(interface.get("default_prompt"))
    if default_prompt is None:
        fail(errors, "agents/openai.yaml needs a quoted default_prompt")
    elif "$writing-style" not in default_prompt:
        fail(errors, "default_prompt must mention $writing-style")

    if parsed.get("policy", {}).get("allow_implicit_invocation") != "false":
        fail(errors, "policy.allow_implicit_invocation must resolve to exactly false")


def validate_single_workflow(errors: list[str]) -> None:
    skill_text = SKILL.read_text(encoding="utf-8")
    frontmatter_match = re.match(r"\A---\n(.*?)\n---\n", skill_text, re.DOTALL)
    frontmatter = frontmatter_match.group(1) if frontmatter_match else ""
    if "$writing-style" not in frontmatter:
        fail(errors, "SKILL.md description must require the $writing-style trigger")
    if "## Follow one workflow" not in skill_text:
        fail(errors, "SKILL.md must define the single workflow")
    for heading in ("## Choose the operation", "## Choose the editing strength"):
        if heading in skill_text:
            fail(errors, f"SKILL.md must not retain mode heading: {heading}")

    for markdown_file in (SKILL, ROOT / "README.md"):
        if re.search(r"(?<![\w/.~])/writing-style", markdown_file.read_text(encoding="utf-8")):
            relative_file = markdown_file.relative_to(ROOT)
            fail(errors, f"{relative_file} must not document a slash-command trigger")


def exact_case_path(path: Path) -> bool:
    """Check every path component's letter case against the file system entry.

    macOS file systems are usually case-insensitive, so Path.exists() passes a
    wrong-case link that breaks on the case-sensitive CI runner and on GitHub.
    """

    try:
        relative = path.relative_to(ROOT)
    except ValueError:
        return True
    current = ROOT
    for part in relative.parts:
        try:
            entries = {entry.name for entry in current.iterdir()}
        except OSError:
            # Best-effort: the link already resolved via exists(), so an
            # unreadable or non-directory component must not break validation.
            return True
        if part not in entries:
            return False
        current = current / part
    return True


def validate_link_check_probes(errors: list[str]) -> None:
    if not exact_case_path(ROOT / "README.md"):
        fail(errors, "exact-case probe wrongly rejected a correct-case path")
    if exact_case_path(ROOT / "readme.MD"):
        fail(errors, "exact-case probe accepted a wrong-case path")
    if (ROOT.parent / "outside-probe").resolve().is_relative_to(ROOT):
        fail(errors, "containment probe wrongly placed an outside path inside the repository")
    if ROW_LIMITS_PATTERN.search("task 19 needs 450 words"):
        fail(errors, "row-limit pattern matched a reworded row it should reject")


def validate_markdown_links(errors: list[str]) -> None:
    markdown_files = [
        ROOT / "README.md",
        SKILL,
        *sorted((ROOT / "references").glob("*.md")),
        *sorted((ROOT / "eval").glob("*.md")),
    ]
    link_pattern = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
    for markdown_file in markdown_files:
        relative_file = markdown_file.relative_to(ROOT)
        text = markdown_file.read_text(encoding="utf-8")
        prose, fence_left_open = split_fenced_code(text)
        if fence_left_open:
            fail(errors, f"unclosed Markdown code fence in {relative_file}")
        for target in link_pattern.findall(prose):
            if re.match(r"(?:https?://|mailto:|#)", target):
                continue
            path_text = unquote(target.split("#", 1)[0])
            target_path = (markdown_file.parent / path_text).resolve()
            if not target_path.exists():
                fail(errors, f"broken local link in {relative_file}: {target}")
                continue
            if not target_path.is_relative_to(ROOT):
                fail(errors, f"local link escapes the repository in {relative_file}: {target}")
                continue
            if not exact_case_path(target_path):
                fail(errors, f"local link case mismatch in {relative_file}: {target}")


def validate_synced_examples(errors: list[str]) -> None:
    skill_text = SKILL.read_text(encoding="utf-8")
    readme_text = (ROOT / "README.md").read_text(encoding="utf-8")
    skill_match = re.search(
        r"\*\*LLM draft:\*\*\n> (?P<before>.*?)\n\n"
        r"\*\*Finished prose:\*\*\n> (?P<after>.*?)\n",
        skill_text,
        re.DOTALL,
    )
    readme_match = re.search(
        r"\*\*LLM draft:\*\*\n\n> (?P<before>.*?)\n\n"
        r"\*\*Finished prose:\*\*\n\n> (?P<after>.*?)\n",
        readme_text,
        re.DOTALL,
    )
    if not skill_match or not readme_match:
        fail(errors, "could not locate the synced README and SKILL.md examples")
        return
    if skill_match.groupdict() != readme_match.groupdict():
        fail(errors, "README and SKILL.md before/after examples must match")


ROW_LIMITS_PATTERN = re.compile(
    r"task 19 has (\d+) or more whitespace-delimited words; "
    r"task 20 has (\d+) or more; task 21 has (\d+) or more"
)


def validate_evals(errors: list[str]) -> None:
    text = EVAL_PROMPTS.read_text(encoding="utf-8")
    checklist_start = text.find("## Marking checklist")
    if checklist_start == -1:
        fail(errors, "eval prompts must contain a marking checklist section")
        checklist_start = len(text)
    tasks_text = text[:checklist_start]
    checklist_text = text[checklist_start:]

    task_numbers = [
        int(number) for number in re.findall(r"^(\d+)\. \*\*", tasks_text, re.MULTILINE)
    ]
    if task_numbers != list(range(1, 30)):
        fail(errors, "eval tasks must be numbered consecutively from 1 to 29")

    required_taxonomy_task_text = (
        "23. **Grammar-pattern rewrite**",
        "serves as a centralised hub",
        "24. **Attribution-integrity rewrite**",
        "Attribute claims only to supplied sources",
        "25. **Rhetoric-pattern rewrite**",
        "the currency of modern support",
        "26. **Structure-pattern rewrite**",
        "from onboarding to analytics to culture",
        "27. **Documentation-truth rewrite**",
        "This section was added to replace",
        "28. **Preservation trap**",
        "44 Batman Street",
        "29. **Voice-sample precedence**",
        "color-coded dashboard",
    )
    for requirement in required_taxonomy_task_text:
        if requirement not in tasks_text:
            fail(errors, f"taxonomy eval coverage is missing: {requirement}")

    required_taxonomy_rows = (
        "No participle-tail assertions, copula avoidance or synonym cycling (task 23)",
        "no invented authority (task 24)",
        "No staccato runs, aphorism formulas or fake-candid openers (task 25)",
        "No false ranges, subjectless fragments, compound pileups, signposting or fragmented headers (task 26)",
        "documentation describes current state rather than its own history (task 27)",
        "Human-hand signals survive transformation (task 28)",
        "A supplied voice sample outranks style defaults (task 29)",
    )
    for requirement in required_taxonomy_rows:
        if requirement not in checklist_text:
            fail(errors, f"taxonomy marking row is missing: {requirement}")

    required_structured_task_text = (
        "19. **Implementation brief**",
        "implementation brief under 450 words",
        "20. **Contributor guide**",
        "practical guide under 500 words",
        "21. **GitHub README**",
        "README under 400 words",
        "22. **Starved minimum**",
        "at least 250 words",
    )
    for requirement in required_structured_task_text:
        if requirement not in tasks_text:
            fail(errors, f"structured-document eval coverage is missing: {requirement}")

    row_limits = ROW_LIMITS_PATTERN.search(checklist_text)
    prompt_limits = tuple(
        match.group(1) if match else None
        for match in (
            re.search(r"implementation brief under (\d+) words", tasks_text),
            re.search(r"practical guide under (\d+) words", tasks_text),
            re.search(r"README under (\d+) words", tasks_text),
        )
    )
    if not row_limits:
        fail(errors, "length marking row must state the task 19-21 word limits")
    elif None not in prompt_limits and row_limits.groups() != prompt_limits:
        fail(errors, "length marking row word limits must match the task prompts")

    task22_prompt = re.search(r"22\. \*\*Starved minimum\*\*.*?at least (\d+) words", tasks_text)
    task22_row = re.search(r"task 22 reaches (\d+) words", checklist_text)
    if not task22_prompt or not task22_row:
        fail(errors, "task 22 word minimum must appear in both the prompt and its marking row")
    elif task22_prompt.group(1) != task22_row.group(1):
        fail(errors, "task 22 marking-row word minimum must match the task prompt")

    required_checks = (
        "Meaning and point of view are preserved",
        "No unsupported facts",
        "Uncertainty and evidentiary limits are preserved",
        "Explicit user instructions override skill defaults",
        "The single workflow is followed",
        "Supplied source is transformed without cosmetic churn",
        "Creative choices survive operational defaults",
        "Transitions and paragraph shape show real logic",
        "No leaked assistant or source artefact",
        "No deliberate errors added merely to look human",
        "The sender sounds involved rather than like an anonymous adviser",
        "Conversational channels do not inherit memo furniture",
        "No thoroughness theatre",
        "Profile alignment is scored independently of rule compliance",
        "Explicit length and document-format constraints are met",
        "Structured documents contain no prompt-aware narration",
        "Brief required content is complete",
        "Brief decision integrity is preserved without repetition",
        "Guide prerequisites and platform limits are complete",
        "Guide setup and verification are complete",
        "Guide milestones expose observable success",
        "Guide checkpoints read as prose, not form fields",
        "Guide troubleshooting and editing boundaries are complete",
        "Guides do not invent project-specific detail or unsafe remedies",
        "README purpose, setup and usage are complete",
        "README status, behaviour and limits are complete",
        "README repository navigation and reporting are complete",
        "GitHub documentation does not invent repository claims",
        "Starved minimums are not met by padding or invention",
        "Starved-minimum handling stays out of the deliverable",
    )
    for check in required_checks:
        if check not in checklist_text:
            fail(errors, f"eval checklist is missing: {check}")

    required_method_text = (
        "pin the previous skill commit as a separate baseline arm",
        "Hide the arm and randomise output order",
        "Rule compliance alone does not establish voice similarity",
        "only the voice owner's judgement against held-out, authentic samples",
    )
    for requirement in required_method_text:
        if requirement not in tasks_text:
            fail(errors, f"eval method is missing: {requirement}")

    for result_file in sorted((ROOT / "eval").glob("results-*.md")):
        result_text = result_file.read_text(encoding="utf-8")
        commit_match = re.search(
            r"^- \*\*Commit:\*\* `([0-9a-f]{7,40})`$", result_text, re.MULTILINE
        )
        if not commit_match:
            fail(errors, f"{result_file.name} must record an immutable commit SHA")
        else:
            commit = commit_match.group(1)
            resolved = subprocess.run(
                ["git", "cat-file", "-e", f"{commit}^{{commit}}"],
                cwd=ROOT,
                capture_output=True,
                text=True,
            )
            if resolved.returncode != 0:
                fail(errors, f"{result_file.name} references an unresolved commit: {commit}")

        if "**Evidence status:**" not in result_text:
            fail(errors, f"{result_file.name} must state its evidence status")
        if "recorded here rewritten" in result_text and "not raw evidence" not in result_text:
            fail(errors, f"{result_file.name} must disclose that edited output is not raw evidence")

        if "**Schema:** v2" in result_text:
            if not (commit_match and re.fullmatch(r"[0-9a-f]{40}", commit_match.group(1))):
                fail(
                    errors,
                    f"{result_file.name} (schema v2) must record a full 40-character commit SHA",
                )
            for field in ("- **Date:**", "- **Generator:**", "- **Marker:**", "- **Invocation:**"):
                if field not in result_text:
                    fail(errors, f"{result_file.name} (schema v2) is missing field: {field}")


def validate_tracked_files(errors: list[str]) -> None:
    result = subprocess.run(
        ["git", "ls-files"], cwd=ROOT, check=True, capture_output=True, text=True
    )
    tracked = set(result.stdout.splitlines())
    if ".DS_Store" in tracked:
        fail(errors, ".DS_Store must not be tracked")
    for relative_path in ("references/structured-documents.md",):
        if relative_path not in tracked:
            fail(errors, f"required repository file must be tracked: {relative_path}")


def validate_references(errors: list[str]) -> None:
    required = {
        "references/australian-english.md",
        "references/anti-patterns.md",
        "references/assistant-frame.md",
        "references/structured-documents.md",
    }
    for relative_path in required:
        if not (ROOT / relative_path).is_file():
            fail(errors, f"missing required reference: {relative_path}")

    skill_text = SKILL.read_text(encoding="utf-8")
    if "[Structured documents](references/structured-documents.md)" not in skill_text:
        fail(errors, "SKILL.md must route structured-document tasks to their reference")

    structured_text = (ROOT / "references" / "structured-documents.md").read_text(
        encoding="utf-8"
    )
    for heading in (
        "## Plan privately",
        "## Treat length as a delivery gate",
        "## Ground project documentation",
        "## Briefs",
        "## Guides",
        "## GitHub project documentation",
        "## Final verification",
    ):
        if heading not in structured_text:
            fail(errors, f"structured-document reference is missing: {heading}")


def main() -> int:
    errors: list[str] = []
    validate_skill(errors)
    validate_openai_yaml(errors)
    validate_single_workflow(errors)
    validate_fence_stripping(errors)
    validate_link_check_probes(errors)
    validate_markdown_links(errors)
    validate_synced_examples(errors)
    validate_evals(errors)
    validate_tracked_files(errors)
    validate_references(errors)

    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1

    print("Repository validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
