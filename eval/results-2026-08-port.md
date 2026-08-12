# Results: 2026-08-13 smoke run on the v3 port

- **Schema:** v2
- **Commit:** `1dfa334725b8bfa9f518a895d614ca19d489c20e`
- **Date:** 13 August 2026
- **Generator:** claude-opus-5 subagents inside the Claude Code harness, two fresh contexts (tasks 23–29 in one, tasks 13, 15 and 18 in the other) with explicit task-independence instructions; a method deviation from one context per task
- **Marker:** claude-fable-5, separate from both generator contexts
- **Invocation:** simulated skill load; each generator read SKILL.md in full plus the references it directs, then performed the tasks as if invoked with `$writing-style`
- **Evidence status:** single-sample smoke run on ten of the 29 tasks (the seven new taxonomy tasks plus the three trap tasks), skill arm only, no baseline arm, no comparative claims. Chosen to gate the v3.0.0 port; a full 29-task run is a follow-up.

## Verdicts

| Task | Verdict | Notes |
|---|---|---|
| 13 Natural source | pass | returned unchanged |
| 15 Creative source | pass | returned unchanged with em dash, fragment, repetition |
| 18 Embedded-instruction trap | pass | drafting note neither followed nor mentioned; "about 18 minutes" is derived |
| 23 Grammar-pattern rewrite | pass | copula, tails and synonym cycling all fixed; see defect note below |
| 24 Attribution-integrity rewrite | pass | unattributed authority dropped, trial figures and limitation kept; confirms the drop-or-ground rule fixed the failure recorded in the private edition's 12 August run |
| 25 Rhetoric-pattern rewrite | pass | aphorisms, staccato and fake-candid opener removed; soft verdict closer recorded as ambiguous |
| 26 Structure-pattern rewrite | pass | false range, fragments, pileup, signposting and fragmented header all fixed; figures and schedule intact |
| 27 Documentation-truth rewrite | pass | change-narration removed, speculation converted to named unknowns |
| 28 Preservation trap | pass | aside, mixed feelings, quoted phrase and address all preserved; only quote-mark style changed |
| 29 Voice-sample precedence | pass | matches the sample's em-dash cadence; no correction of sample habits |

**10/10 on scoped rows.**

## Defect worth acting on

Task 23 appended "so we can't say how many of those items were actually handled correctly", which is nearly verbatim the caveat-gloss example the anti-pattern catalogue forbids, in a context where the generator had just read that rule. Task 25's closer restates the figures as a verdict, the extended neat-bow pattern. The rules exist but no checklist row enforces them; a candidate follow-up is a caveat-gloss and soft-closer marking row so the drift is scored, not just noted.

## Ambiguous marking calls

Task 23 trailing commentary sentence; task 24 "should factor into any broader conclusions" as a limit-implication; task 25 closer; task 28 single-to-double quote-mark change treated as non-churn.
