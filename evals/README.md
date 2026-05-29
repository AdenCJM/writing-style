# Evaluating and improving the skill

This directory holds the harness that measures whether the `writing-style` skill
actually works, and a step that proposes improvements to it. The two GitHub
Actions workflows in `.github/workflows/` run all of this.

## How it fits together

```
SKILL.md ──parsed by──> check.py ──scores──> run_eval.py ──evidence──> improve.py ──PR──> SKILL.md
```

- **`check.py`** parses the banned-word rules straight out of `SKILL.md`, so it
  always tests the *current* skill. It flags em dashes, American spelling, and
  banned words (hard = always a fail; soft = context-dependent, reported only).
- **`run_eval.py`** generates each prompt in `cases.json` twice (with the skill
  as a system prompt, and a no-skill baseline), scores both, and reports pass
  rates and token overhead.
- **`improve.py`** takes the eval evidence and proposes the smallest useful edit
  to `SKILL.md`, but only keeps it if it still passes validation.

## Running locally

The deterministic checker needs nothing but Python 3.11+:

```bash
# Validate the checker, fixtures, and the skill's own examples
python evals/check.py --selftest

# Check any file against the skill's rules
python evals/check.py path/to/draft.md
python evals/check.py --json path/to/draft.md
```

The live eval and improve steps call the Anthropic API:

```bash
pip install -r evals/requirements.txt
export ANTHROPIC_API_KEY=sk-...

# Generate with/without the skill and score the results
python evals/run_eval.py --out evals/reports/latest
# Optional: add an LLM naturalness score (1-5)
JUDGE=1 python evals/run_eval.py

# Propose an improvement from the latest report (writes SKILL.md + notes)
python evals/improve.py
```

Without `ANTHROPIC_API_KEY` the live scripts print a notice and exit 0, so CI
stays green.

## Workflows

- **`eval.yml`** - runs `check.py --selftest` on every push and PR (no secrets).
  On manual dispatch or a weekly schedule it runs the live eval and uploads a
  report artifact.
- **`improve.yml`** - manual dispatch. Runs the eval, proposes an improvement,
  and opens a PR if `SKILL.md` changed. It never commits to the default branch.

Set the `ANTHROPIC_API_KEY` repository secret to enable the live steps. Override
models with the `GEN_MODEL` / `IMPROVE_MODEL` env vars (or the `GEN_MODEL`
repository variable).

## Files

| File | Purpose |
|---|---|
| `check.py` | Deterministic rule checker + self-test (`validate_skill`) |
| `run_eval.py` | Live with/without-skill eval and scoring |
| `improve.py` | Evidence-driven, validated skill improvement |
| `cases.json` | Prompts spanning the writing types the skill targets |
| `fixtures/` | `good_*` must pass, `bad_*` must be caught (self-test) |
| `requirements.txt` | `anthropic` SDK (live steps only) |
