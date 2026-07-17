---
name: writing-style
description: >-
  Write, rewrite, tighten or audit English prose in a clear, direct Australian
  voice while preserving meaning and explicit requirements. Supports light,
  standard and strong editing across messages, emails, posts, reports and
  documents. ONLY use when the user explicitly requests this skill, names
  /writing-style or $writing-style, or asks to apply their writing rules. Do not
  invoke automatically for general writing or code generation.
---

# Writing style

Produce clear, direct prose that sounds considered rather than generated. Preserve the writer's intent before applying stylistic preferences.

## Priority order

Resolve conflicts in this order:

1. Fulfil the user's goal and explicit requirements.
2. Preserve facts, meaning, uncertainty, commitments and required wording.
3. Fit the audience, channel and stakes.
4. Preserve the writer's voice and structure when editing.
5. Apply the direct Australian voice.
6. Remove generated-writing patterns where the higher priorities permit it.

## Choose the operation

Infer the operation from the request. Follow an operation the user names.

- **Draft:** Create prose from supplied facts. Write around missing details or use clear placeholders; never fill gaps with guesses.
- **Rewrite:** Change voice and structure while preserving every substantive claim.
- **Tighten:** Make the smallest useful edits. Retain the writer's cadence, layout and deliberate choices.
- **Audit:** Identify issues without rewriting. Quote only the minimum text needed and group findings by impact.

For draft, rewrite and tighten, return the finished prose without commentary unless the user asks for rationale or a change summary. For audit, return findings rather than a replacement draft.

## Choose the editing strength

Use **standard** unless the user asks for another strength.

- **Light:** Correct required spelling and punctuation, remove obvious filler and leave structure and cadence alone.
- **Standard:** Apply the full voice and anti-pattern guidance while preserving natural variation.
- **Strong:** Restructure freely and remove every avoidable generated-writing pattern. Fidelity and explicit requirements still win.

## Understand the reader

Before writing, identify the audience, channel, purpose and action. Match formality and explanation depth to the reader's knowledge and the consequences of misunderstanding.

Make the purpose clear early. Give the reader enough context to understand the decision or request. Make actions, owners and deadlines easy to find when they exist in the source. Do not invent them.

## Preserve substance

- Use only facts supplied by the user or source, plus arithmetic clearly derived from supplied figures.
- Keep qualifications such as "may", "suggests", "preliminary" and "subject to approval" unless the user asks to change the claim.
- Preserve legal, medical, academic and technical terms. Plain language can surround a precise term; it cannot replace it with something less accurate.
- Keep the writer's position. Do not turn promotion into scepticism, a neutral account into opinion or a proposal into an approved plan.
- Preserve exact titles, defined terms, citations, link destinations, direct quotes and wording the user asks to keep.
- Never invent names, examples, anecdotes, capabilities, dates, figures, causes, results, promises or sender identities.
- When the user requests analysis, distinguish conclusions from supplied facts.

Leave code, variable names and inline code unchanged. Apply the style to prose in comments, documentation and interface copy only when that prose is part of the requested work.

## Use the supporting references

- Read [Australian English](references/australian-english.md) when Australian English applies. Skip it when the user or required house style requests another variety.
- Read [Anti-pattern catalogue](references/anti-patterns.md) for standard or strong editing, or when auditing for generated-writing patterns. For light edits, use only the core rules below.
- Read [Assistant frame](references/assistant-frame.md) for analyses, reports, recommendations and other substantial deliverables.

## Core voice

- Default to short. If one sentence does the job, send one sentence.
- Prefer plain verbs and concrete nouns. Replace vague intensity with supplied specifics; never invent evidence.
- Use short paragraphs and varied sentence lengths. Change repeated openings or rhythms.
- Use contractions in casual and semi-formal prose.
- Ask questions directly. Put an important question on its own line when useful.
- Use warmth through relevant specifics rather than gush or reader-flattery.
- Keep the writer's asides and quirks unless they obstruct the task or the user asks to remove them.
- Get to the point without a ceremonial opener. End on the decision, action or fact that matters.

## Core punctuation

- Avoid em dashes in new operational prose. Preserve them when required by the source, user or creative form.
- Omit the Oxford comma unless it prevents ambiguity or the user requests it.
- Use sentence-case headings unless preserving an exact title or following another house style.
- Use at most one exclamation mark in a short casual piece and none in formal prose unless requested.
- Use punctuation to improve reading, not to create a repeated rhetorical pattern.

## Creative work

In fiction, speeches, personal essays and other creative work, preserve deliberate rhythm, fragments, repetition, rhetorical questions and punctuation. Apply locale and fidelity rules, then edit only what the user asks to change. Do not flatten a creative voice to satisfy operational-prose defaults.

## Examples

**Overwritten:**
> In today's rapidly evolving digital landscape, businesses must leverage cutting-edge technologies to stay ahead of the curve. It is important to note that our new invoice platform reduced median processing time from four days to two in the June trial.

**Standard rewrite:**
> Businesses need current technology to keep up with change. In the June trial, our new invoice platform cut median processing time from four days to two.

**Light tighten:**
> Thanks for sending this through. I've read it and agree with the recommendation. Let's discuss timing tomorrow.

Keep that natural draft largely intact. Do not rewrite it merely to demonstrate the skill.

## Final check

Before delivering, ask:

1. Does this achieve the user's purpose for the intended reader?
2. Did every fact, name, number and commitment come from the source?
3. Did meaning, uncertainty and required wording survive?
4. Did I follow the requested operation and editing strength?
5. Did I preserve good human writing rather than changing it for activity's sake?
6. Are actions and decisions clear without invented detail?
7. Did I remove avoidable filler, stock structures and assistant framing?

Fix violations silently unless the user requested an audit or explanation.
