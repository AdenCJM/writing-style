# Eval results: June 2026

**Evidence status:** Historical rule-development run. It predates the current single-workflow engine and fidelity rubric, uses one Claude-only sample per task and does not include auditable raw baseline outputs. Retain it as history, not evidence of current quality.

- **Date:** 10 June 2026
- **Model:** Claude (Fable 5) via Claude Code, fresh subagent context per run
- **Skill version:** style-overhaul branch (post-review fixes)
- **Commit:** `6264aea`
- **Method:** one run with SKILL.md loaded across all six tasks in [PROMPTS.md](PROMPTS.md), marked row by row against the checklist. Baseline comparison from an earlier no-skill run of tasks 1–5.

## With skill: verdicts

| Task | Verdict | Notes |
|---|---|---|
| 1. Slack message | Pass | No greeting or sign-off, zero exclamation marks, paragraphs not headers |
| 2. Email | Pass | "Hi Sarah," greeting, "Thanks" sign-off, plain subject, "Tuesday 23 June" date format |
| 3. LinkedIn post | Pass | Requested three-lesson structure plus one allowed in-sentence triad, no hashtags or engagement bait |
| 4. One-pager intro | Pass | Sentence-case title, only the supplied numbers (6 hours/week, 2,000 leads/quarter), one allowed triad |
| 5. Rewrite | Pass | All slop removed, no "not X, but Y" contrast, one allowed triad |
| 6. Report section | Pass | Formal register held: no colloquialisms, no exclamation marks, supplied figures only |

Every piece passed every applicable checklist row. No banned words, no em dashes, no Oxford commas, no invented numbers.

## Baseline (no skill, tasks 1–5, earlier run)

The unguided baseline failed multiple rows per piece: decorative emoji and bold lead-in bullets in the Slack post, "I hope you're doing well!" and "Best regards" in the email, a hashtag block and an engagement-bait closer on the LinkedIn post, and eight-plus em dashes across the set.

## Outputs (with skill)

### Task 1: Slack message

Scout is live for everyone as of today. It's the internal tool that auto-summarises customer support tickets, so you get the shape of a thread in seconds instead of reading the full history.

We're running a 30-minute training session on Thursday for anyone who wants a walkthrough. Worth joining if you deal with support tickets at all.

Questions, drop them in this thread.

### Task 2: Email

Subject: Rescheduling our QBR

Hi Sarah,

Two of our team are travelling next Tuesday, so we need to move the quarterly business review. Could we do Tuesday 23 June instead, same time?

Sorry to shuffle things this close to the date. Everything on our side is ready to go, so the agenda doesn't change, just the day.

If Tuesday doesn't suit, send through a couple of times that week and we'll fit in around you.

Thanks,
Aden

### Task 3: LinkedIn post

We've spent the past year putting AI agents into production workflows at a blockchain gaming company. Some worked, some quietly got turned off. Three lessons that stuck:

1. **Boring workflows first.** The agents earning their keep are doing ticket triage and data entry. Nothing you'd put on a conference slide. Start where the work repeats and mistakes are cheap.

2. **Trust is the bottleneck.** The models could handle most of our use cases a year ago. What took the time was the human side: review steps, escalation paths and a way to override the output when it's wrong.

3. **Maintenance is the real cost.** Prompts drift and edge cases pile up. An agent needs an owner the same way a service does, and that cost belongs in the plan from day one.

If you're starting now, pick one dull process and get an agent running it end to end. You'll learn more from that than from any pilot deck.

### Task 4: One-pager intro

**Automating lead enrichment**

The growth team enriches inbound leads by hand: about 2,000 leads a quarter, each looked up across multiple tools and copied into the CRM. The work takes roughly 6 hours a week, and every new lead waits on it before sales can follow up. It is repetitive work that scales only by adding people.

This proposal recommends an automated enrichment pipeline. New leads would be enriched on arrival using the data sources the team already pays for, with a person reviewing only the records that fail validation. The change removes the manual step for the bulk of inbound volume and gives sales complete records the moment a lead lands. The sections below cover the design, the cost and the rollout plan.

### Task 5: Rewrite

Most teams don't need convincing to use AI. The hard part is fitting it into how they already work. That's what our platform does: it plugs into your existing tools, picks up the repetitive work and frees your team for the things that need a person. No new processes to learn and nothing to migrate.

### Task 6: Report section

**Current state**

Support demand grew this quarter, with ticket volume rising from 1,800 to 2,400. Response performance improved over the same period: median first-response time fell from 9 hours to 4.

The improvement came from changes to triage and routing made early in the quarter. Tickets now reach the right queue on arrival rather than after a manual review, which removed the longest delays from the process. The gains held through the busiest weeks of the quarter. Median figures are used instead of averages so that a small number of complex tickets does not distort the picture.

Capacity is the open question. The team absorbed the higher volume without additional staff, and the current setup has room for some further growth, but a similar rise next quarter would put first-response times under pressure. Recommendations for handling that growth are set out in the next section.
