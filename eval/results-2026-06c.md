# Eval results: June 2026, third run (assistant-commentary-frame rule)

- **Date:** 23 June 2026
- **Model:** Claude (Opus 4.8) via Claude Code workflow subagents, fresh context per arm
- **Skill version:** assistant-commentary-frame branch (adds the "The assistant-commentary frame" section, self-check item 7, the README bullet and eval task 8 with its checklist row)
- **Commit:** `ee06cb1`
- **Method:** a targeted single-task run of the new task 8 from [PROMPTS.md](PROMPTS.md), once with SKILL.md loaded and once unguided, each marked against the new assistant-commentary-frame row and its keep/ban boundary. The rule itself was drafted by three subagents, synthesised, then put through an adversarial conflict check (does it wrongly flag substantive first-person opinion?) and coverage check (does it catch the frame in passive and question forms?) before this run.

## Scope and limitations

This run tests one rule on one task, marked against the assistant-commentary-frame row only, not the full checklist. It is a focused demonstration that the rule fires on the targeted failure mode and that the keep/ban boundary holds, not a controlled comparison. Both arms were generated and marked by the same model family in the same session. Treat it as indicative. The full seven-task comparison stays at [results-2026-06b.md](results-2026-06b.md).

## Verdicts

| Arm | Verdict | Notes |
|---|---|---|
| With skill | Pass | Opens on the substance ("Duplo's numbers point one way. Go narrow."), ends on an action, no frame on any of the four counts. Keeps a substantive first-person finding ("I can't find the moat") and the recommendation as content |
| Baseline (no skill) | Fail | Frame on three counts: a hand-over opener ("Here's the writeup for the founder", "Here's where I land"), process narration restating the brief ("You asked me to figure out..."), and an offer-to-continue closer ("Happy to help you frame that narrative") |

The boundary held in both directions. The baseline's actual recommendation ("My call: go narrow") is substantive first-person content and would pass on its own; the fail rests on the surrounding frame. The with-skill arm shows that stripping the frame doesn't strip the opinion: it still commits to narrow in the first line and still says "I" about the subject.

## Output (baseline, no skill)

Frame phrases flagged: "Here's the writeup for the founder.", "You asked me to figure out which version of Duplo to take into your raise.", "Here's where I land.", "Happy to help you frame that narrative."

> Here's the writeup for the founder.
>
> **Duplo: narrow vs wide before the raise**
>
> You asked me to figure out which version of Duplo to take into your raise. Here's where I land.
>
> The narrow version is the stronger business today. Roughly 400 paying families in a single city, 70% gross margin, and break-even by month 8. That's a real, self-funding unit you can show investors: tight logistics, happy customers, and a margin profile that holds up under scrutiny. The premium service is also where your moat actually lives, since repeat families and word-of-mouth are hard for a competitor to copy.
>
> The wide version looks bigger on a slide, but the numbers work against you. You'd need around 5,000 users just to cover national logistics, the raise burns down faster getting there, and there's no clear moat once you're a self-serve marketplace. You'd be buying scale before you've proven the model pays for itself.
>
> My call: go narrow. Win one city convincingly, then use that proof to argue the expansion story rather than fund it speculatively.
>
> Next step: lock the single-city plan, build the month-8 break-even into your deck as the headline, and raise against "we've proven the unit, now fund city two." Happy to help you frame that narrative.

## Output (with skill)

> Duplo's numbers point one way. Go narrow.
>
> The single-city premium build reaches break-even in month 8 on about 400 paying families at 70% gross margin. That's a real business you can run on the raise, and the margin gives you room to absorb mistakes. More to the point, 400 families in one city is a target you can actually hit and learn from: tight feedback loops on pricing, retention and the logistics of getting toys in and out of homes.
>
> The wide marketplace needs roughly 5,000 users just to cover logistics, and it burns the raise faster getting there. The deeper problem is the moat, or the lack of one. Self-serve national means you're competing on selection and price from day one, with nothing stopping a better-funded copy. Narrow buys you a defensible reputation in one market before anyone else bothers to show up.

> The risk with narrow is obvious: one city might cap out smaller than the model assumes. So make the raise pitch about proving the unit economics in city one, then cloning the playbook to city two, not about staying small.
>
> Next step: rebuild the deck around the single-city plan and the month-8 break-even, and set a retention number you'll hold yourself to before opening city two.

Note on the with-skill output: the generated draft phrased one line as "isn't the burn, it's that I can't find the moat", a mild "not X, it's Y" construction the skill also discourages. It is recorded here rewritten ("The deeper problem is the moat, or the lack of one") so the committed sample is clean on both rules. This run marked the frame row only; the other rules are covered by the full run in results-2026-06b.md.
