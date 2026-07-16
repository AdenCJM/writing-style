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


def validate_openai_yaml(errors: list[str]) -> None:
    text = OPENAI_YAML.read_text(encoding="utf-8")
    short_description = quoted_yaml_value(text, "short_description")
    if short_description is None:
        fail(errors, "agents/openai.yaml needs a quoted short_description")
    elif not 25 <= len(short_description) <= 64:
        fail(errors, "short_description must contain 25–64 characters")

    default_prompt = quoted_yaml_value(text, "default_prompt")
    if default_prompt is None:
        fail(errors, "agents/openai.yaml needs a quoted default_prompt")
    elif "$writing-style" not in default_prompt:
        fail(errors, "default_prompt must mention $writing-style")

    if not re.search(r"^policy:\n\s+allow_implicit_invocation:\s+false\s*$", text, re.MULTILINE):
        fail(errors, "Codex policy must set allow_implicit_invocation to false")
    if "\t" in text:
        fail(errors, "agents/openai.yaml must not contain tabs")


def validate_markdown_links(errors: list[str]) -> None:
    markdown_files = [ROOT / "README.md", *sorted((ROOT / "eval").glob("*.md"))]
    link_pattern = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
    for markdown_file in markdown_files:
        text = markdown_file.read_text(encoding="utf-8")
        for target in link_pattern.findall(text):
            if re.match(r"(?:https?://|mailto:|#)", target):
                continue
            path_text = unquote(target.split("#", 1)[0])
            target_path = (markdown_file.parent / path_text).resolve()
            if not target_path.exists():
                relative_file = markdown_file.relative_to(ROOT)
                fail(errors, f"broken local link in {relative_file}: {target}")


def validate_synced_examples(errors: list[str]) -> None:
    skill_text = SKILL.read_text(encoding="utf-8")
    readme_text = (ROOT / "README.md").read_text(encoding="utf-8")
    skill_match = re.search(
        r"\*\*Bad \(AI-typical\):\*\*\n> (?P<before>.*?)\n\n"
        r"\*\*Good:\*\*\n> (?P<after>.*?)\n",
        skill_text,
        re.DOTALL,
    )
    readme_match = re.search(
        r"\*\*Before \(AI-typical\):\*\*\n\n> (?P<before>.*?)\n\n"
        r"\*\*After:\*\*\n\n> (?P<after>.*?)\n",
        readme_text,
        re.DOTALL,
    )
    if not skill_match or not readme_match:
        fail(errors, "could not locate the synced README and SKILL.md examples")
        return
    if skill_match.groupdict() != readme_match.groupdict():
        fail(errors, "README and SKILL.md before/after examples must match")


def validate_evals(errors: list[str]) -> None:
    text = EVAL_PROMPTS.read_text(encoding="utf-8")
    task_numbers = [int(number) for number in re.findall(r"^(\d+)\. \*\*", text, re.MULTILINE)]
    if task_numbers != list(range(1, 13)):
        fail(errors, "eval tasks must be numbered consecutively from 1 to 12")

    required_checks = (
        "Meaning and point of view are preserved",
        "No unsupported facts",
        "Uncertainty and evidentiary limits are preserved",
        "Explicit user instructions override skill defaults",
    )
    for check in required_checks:
        if check not in text:
            fail(errors, f"eval checklist is missing: {check}")

    for result_file in sorted((ROOT / "eval").glob("results-*.md")):
        result_text = result_file.read_text(encoding="utf-8")
        if not re.search(r"^- \*\*Commit:\*\* `[0-9a-f]{7,40}`$", result_text, re.MULTILINE):
            fail(errors, f"{result_file.name} must record an immutable commit SHA")


def validate_tracked_files(errors: list[str]) -> None:
    result = subprocess.run(
        ["git", "ls-files"], cwd=ROOT, check=True, capture_output=True, text=True
    )
    tracked = set(result.stdout.splitlines())
    if ".DS_Store" in tracked:
        fail(errors, ".DS_Store must not be tracked")


def main() -> int:
    errors: list[str] = []
    validate_skill(errors)
    validate_openai_yaml(errors)
    validate_markdown_links(errors)
    validate_synced_examples(errors)
    validate_evals(errors)
    validate_tracked_files(errors)

    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1

    print("Repository validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
