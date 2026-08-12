# Changelog

A design diary, not just a release log. Each entry records what changed and why, so future edits don't quietly re-fight settled decisions. Log the reasoning behind any non-obvious rule change: the failure it fixes, the trade-off it accepts.

## v3.0.0, 2026-08-13: single workflow, expanded taxonomy, structured documents

Breaking release. The four operations (draft, rewrite, tighten, audit) and three editing strengths are gone; mode selection was friction without benefit. One workflow remains: transform a supplied recipient-facing draft, or write from supplied facts and constraints. The only trigger is `$writing-style`.

- **Single workflow and output contracts.** Four mutually exclusive delivery contracts (chat, file edited in place, embedded step, missing-material request) replace mode documentation. A draft is treated as working material: its supported substance survives, its generated surface does not.
- **Priority order with voice-sample precedence.** A user-supplied voice sample now sits inside the numbered hierarchy: it outranks every style default, including punctuation and locale, and never overrides goals or fidelity.
- **Anti-pattern taxonomy expanded**, informed by blader/humanizer and Wikipedia's "Signs of AI writing": grammar-level tells (participle tails, copula avoidance, synonym cycling, false ranges, subjectless fragments, compound pileups), vague attribution, speculative gap-filling, change-narration, aphorism formulas, signposting, fragmented headers, fake-candid openers and staccato runs. A clusters principle (judge tell density, not single tokens) and two guardrail lists ("Do not flag" false positives and "Signs of a human hand" to preserve) stop the taxonomy sanding a real voice into blandness.
- **Two-question self-audit** in the final check: one question chases residual generated surface, the opposing one chases fabrication, because a rewrite that only audits for slop lets invented-but-natural-sounding detail through. Live eval failures added two fidelity rules: vivid elaboration is invention, and an instruction to ground claims means drop-or-ground, never keep-with-a-disclaimer.
- **Structured documents** are a new reference owning briefs, guides and repository documentation: evidence-first project claims, length as a delivery gate, placeholder discipline and per-document-type patterns.
- **Evals rebuilt to 29 tasks** with a row-level checklist: structured documents, grammar tells, documentation truth, a guardrail preservation trap and voice-sample precedence. Task numbering matches the private edition for two-way syncs. Results before this release cover the old 16-task set; historical runs are labelled with evidence-status headers rather than deleted.
- **Validator hardened:** structural YAML parsing with duplicate-key rejection, enforcement of task prompts and marking rows, a v2 results schema, and link, example-sync and fence checks.

## v2.0.0, 2026-07-17: product model release

Fidelity contract, priority order, four-operations interaction model, Australian English reference set and the first validator.

## v1, 2026-03-18: initial release

First public version of the writing-style skill for Claude Code, with Codex compatibility added 2026-03-19.
