# writing-style

An opinionated Claude Code and Codex skill for clear, direct Australian English. It turns supplied LLM drafts into finished prose, or writes a requested piece from supplied facts, without changing the underlying meaning.

## What makes it different

- **Fidelity first:** facts, uncertainty, commitments and required terminology survive the edit, and explicit user instructions outrank every default.
- **One workflow:** supply a draft and it becomes the finished piece; supply facts, notes or a brief and it writes from them. No modes or editing strengths to choose.
- **Reader-focused:** audience, channel, purpose and action come before surface style.
- **Australian English:** spelling, dates and punctuation, with explicit overrides respected.
- **Generated-writing control:** a broad anti-pattern taxonomy removes filler, stock structures, grammar-level tells and assistant framing, with paired guardrail lists that stop it sanding away a real human voice.
- **Structured documents:** briefs, guides and repository documentation are grounded in supplied or inspected evidence, never convention.
- **Do-no-harm behaviour:** good human prose can stay largely unchanged, and a supplied voice sample outranks the skill's own style rules.

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

Invoke the skill only with `$writing-style`, then include either the LLM-generated prose to transform or the facts and constraints for a new piece:

```text
$writing-style Turn the text below into final copy for an external partner.
$writing-style Write a short customer update from these facts.
$writing-style Write a README for this repository from the facts below.
```

When a recipient-facing draft is supplied, the skill transforms it into the finished piece. When the input is a brief or source material, it writes from supplied and verified facts without guessing missing commands, policies or claims.

## Example

**LLM draft:**

> In light of the significant uncertainty surrounding customer adoption, my recommendation is to proceed with the four-week, $18,000 portal pilot. This pragmatic approach will provide valuable insights and create a strong evidence base for a future decision on the 12-week, $42,000 rebuild.

**Finished prose:**

> I'd run the four-week, $18,000 pilot. The main thing we don't know is whether customers will use the portal, and the pilot gives us evidence before we decide whether the $42,000 rebuild is worth it.

## Product structure

`SKILL.md` contains the interaction model, priority order, fidelity contract, output contracts and core voice. Detailed Australian English, anti-pattern, assistant-frame and structured-document guidance lives under `references/` and is loaded only when relevant.

The public edition is deliberately useful out of the box. Personal editions can retain the core and add a private voice profile, real writing samples and private regression cases.

## Customise

- Change the default locale or punctuation conventions.
- Add a personal voice profile under `references/`.
- Replace public examples with redacted examples from your own writing.
- Add real failures to the eval set without committing private correspondence.

## Evals and validation

[eval/PROMPTS.md](eval/PROMPTS.md) holds 29 regression tasks covering fidelity, explicit overrides, structured documents, grammar-level tells, guardrail preservation and voice-sample precedence, with a row-level marking checklist. Historical scored runs remain under [eval/](eval/) and are labelled with their source commit and evidence status.

Run repository checks with:

```bash
python3 scripts/validate_repo.py
```

GitHub Actions runs the same dependency-free validator on pushes and pull requests. Tagged releases provide stable points for downstream personal editions.

## Design history

Rule changes and the reasoning behind them are logged in [CHANGELOG.md](CHANGELOG.md). Parts of the anti-pattern taxonomy were informed by [blader/humanizer](https://github.com/blader/humanizer) and Wikipedia's "Signs of AI writing" guide; this skill applies them inside a fidelity-first transformation workflow rather than as a detector-evasion pass.

## Licence

MIT
