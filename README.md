# writing-style

An opinionated Claude Code and Codex skill for clear, direct Australian English. It drafts, rewrites, tightens and audits prose without changing the underlying meaning.

## What makes it different

- **Fidelity first:** facts, uncertainty, commitments and required terminology survive the edit.
- **Four operations:** draft, rewrite, tighten and audit.
- **Three strengths:** light, standard and strong.
- **Reader-focused:** audience, channel, purpose and action come before surface style.
- **Australian English:** spelling, dates and punctuation with explicit overrides respected.
- **Generated-writing control:** removes filler, stock structures and assistant framing without flattening deliberate creative choices.
- **Do-no-harm behaviour:** good human prose can stay largely unchanged.

## Install

Claude Code:

```bash
git clone https://github.com/AdenCJM/writing-style.git ~/.claude/skills/writing-style
```

Codex:

```bash
git clone https://github.com/AdenCJM/writing-style.git ~/.codex/skills/writing-style
```

Update an existing installation with `git -C ~/.codex/skills/writing-style pull` or the equivalent Claude Code path.

## Use

The skill runs only when requested:

```text
$writing-style draft this announcement
$writing-style rewrite this in standard mode
$writing-style tighten this, light touch
$writing-style audit this without rewriting it
```

Claude Code users can invoke `/writing-style`. Natural requests such as “use the writing-style skill” also work.

Standard editing is the default. Light editing preserves structure and cadence; strong editing permits substantial restructuring while retaining the source's meaning.

## Example

**Overwritten:**

> In today's rapidly evolving digital landscape, businesses must leverage cutting-edge technologies to stay ahead of the curve. It is important to note that our new invoice platform reduced median processing time from four days to two in the June trial.

**Standard rewrite:**

> Businesses need current technology to keep up with change. In the June trial, our new invoice platform cut median processing time from four days to two.

## Product structure

`SKILL.md` contains the interaction model, priority order, fidelity contract and core voice. Detailed Australian English, anti-pattern and assistant-frame guidance lives under `references/` and is loaded only when relevant.

The public edition is deliberately useful out of the box. Personal editions can retain the core and add a private voice profile, real writing samples and private regression cases.

## Customise

- Change the default locale or punctuation conventions.
- Adjust what light, standard and strong mean.
- Add a personal voice profile under `references/`.
- Replace public examples with redacted examples from your own writing.
- Add real failures to the eval set without committing private correspondence.

## Evals and validation

[eval/PROMPTS.md](eval/PROMPTS.md) covers task success, fidelity, explicit overrides, editing strength, audit behaviour, restraint and creative work. Historical scored runs remain under [eval/](eval/) and are labelled with their source commit.

Run repository checks with:

```bash
python3 scripts/validate_repo.py
```

GitHub Actions runs the same dependency-free validator on pushes and pull requests. Tagged releases provide stable points for downstream personal editions.

## Licence

MIT
