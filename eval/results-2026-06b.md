# Eval results: June 2026, second run (pacing and counterpoint rules)

**Evidence status:** Historical rule-development run. It predates the current single-workflow engine and fidelity rubric, uses one sample per arm and was generated and marked by the same model in one session. Retain it as history, not evidence of current quality.

- **Date:** 10 June 2026
- **Model:** Claude (Fable 5) via Claude Code, fresh subagent context per run
- **Skill version:** pacing-and-counterpoint-rules branch (adds the paragraph-pacing rule with its self-check item, the token-counterpoint ban with its checklist row, and amends the rhythm row)
- **Commit:** `b8a61d5`
- **Method:** two runs of the seven tasks in [PROMPTS.md](PROMPTS.md), one with SKILL.md loaded and one unguided baseline, both marked row by row against the updated checklist. Outputs for both arms are committed below. Task 7 was added during the pre-merge review to target the two new rules; both arms ran it the same day.
- **Note:** the run used the branch's initial rule wording. A pre-merge review then aligned the wording of the pacing rule, self-check item 4 and the two checklist rows (same tests, one formulation); both arms were re-marked against the final wording and no verdict changed.

## Limitations

Both arms were generated and marked by the same model in the same session, one run per arm. No independent marker. Treat the comparison as indicative, not controlled.

## With skill: verdicts

| Task | Verdict | Notes |
|---|---|---|
| 1. Slack message | Pass | No greeting or sign-off, zero exclamation marks, paragraph sizes vary (1, 2 and 2 sentences) |
| 2. Email | Pass | Plain subject, "Hi Sarah," greeting, "Thanks" sign-off, "Tuesday 23 June" date format |
| 3. LinkedIn post | Pass | Requested three-lesson structure, no in-sentence triads, closer is an action not engagement bait |
| 4. One-pager intro | Pass | Sentence-case title, only the supplied numbers, one allowed triad ("design, cost and rollout") |
| 5. Rewrite | Pass | All slop removed, no templates, no token counterpoint |
| 6. Report section | Pass | Formal register held, paragraph sizes vary (1, 3, 2 and 2 sentences), closing caveat carries a consequence the reader must act on, so it passes the token-counterpoint row |
| 7. Recommendation memo | Pass | Commits to Parallel in paragraph one, engages cost and setup as substantive counterpoints and resolves both, paragraph sizes vary (3, 4, 4, 5 and 2 sentences), only supplied or derived numbers |

Every piece passed every applicable checklist row, including the new token-counterpoint row and the amended rhythm and pacing row. One marking call to record: the report opens with "rose from 1,800 to 2,400 this quarter, an increase of 33%". The 33% is arithmetic on the supplied figures, which the no-invented-numbers row now explicitly permits; the same carve-out was applied to the baseline arm (see task 4 below).

## Baseline: verdicts

Four of seven failed. The unguided model writes far cleaner than the baseline recorded in [results-2026-06.md](results-2026-06.md) (that run, tasks 1–5 only: decorative emoji, a hashtag block, "Best regards" furniture and eight-plus em dashes; this run: none of those), so the gap has narrowed. What remains is exactly what the skill targets:

| Task | Verdict | Notes |
|---|---|---|
| 1. Slack message | Pass | Clean: no emoji, no headers, one allowed in-sentence triad |
| 2. Email | Pass | Plain subject, correct date format, "Cheers" sign-off |
| 3. LinkedIn post | Fail | Two in-sentence triads ("summarising tickets, enriching leads, triaging alerts"; "started with drafts a human approved, measured the error rate, then removed checkpoints"). Its closer ("Curious what others have found...") sits outside the checklist's engagement-bait definition, so the fail rests on the triads alone |
| 4. One-pager intro | Fail | An invented number with no basis in the task ("estimated at two to three weeks") and two in-sentence triads. "Around 300 hours a year" is derived from the supplied 6 hours/week and passes the same arithmetic carve-out as the with-skill 33% |
| 5. Rewrite | Pass | Slop removed, committed tone, no templates |
| 6. Report section | Fail | An invented capacity threshold ("a sustained rise beyond 3,000 tickets per quarter") presented as a planning figure |
| 7. Recommendation memo | Fail | An em dash in the subject line ("Ticket-triage vendor — recommendation") and the banned word "genuinely" ("it's genuinely attractive"). Notably, it committed to a vendor and varied its paragraphs without help |

On the new token-counterpoint row and the amended pacing row specifically: the baseline didn't trip either, even on task 7, which was designed to tempt both. Its "Slate's strengths are real" paragraph engages the counterpoint substantively and still lands on the recommendation, and its paragraph counts vary (2, 4, 3, 4 and 2 sentences). The new rules read as guardrails for a known failure mode rather than the main source of baseline failures, which in this run are invented numbers, triad stacking and classic tells (em dashes, banned words).

## Outputs (with skill)

### Task 1: Slack message

Heads-up: Scout is now live for everyone.

It's our internal AI tool that auto-summarises customer support tickets, so you get the gist of a long thread without reading every message. Give it a run on your next ticket and tell me where it falls over.

I'm running a 30-min training session on Thursday for anyone who wants a proper walkthrough. Invite to follow.

### Task 2: Email

Subject: Moving the QBR to 23 June?

Hi Sarah,

Quick favour. Two of our team are travelling next Tuesday, so we'd be a couple of people short for the quarterly review. Could we push it to Tuesday 23 June, same time?

Nothing else changes, and you'll have the full team across the table. If that date doesn't work on your end, send through a couple of options and we'll make one fit.

Sorry for the shuffle.

Thanks,
Aden

### Task 3: LinkedIn post

A year of putting AI agents into production workflows at a blockchain gaming company. Some earned their keep, others quietly died. Three lessons that stuck.

**1. Boring workflows first.** Our wins came from support ticket triage and lead enrichment, not the flashy ideas we pitched at the start. If a human finds the task tedious and repetitive, it's probably a good fit for an agent.

**2. Checkable output beats trusted output.** Every agent that survived produces work a human can verify in seconds, like a draft reply with the source ticket attached. The ones making decisions nobody could easily audit got switched off within a month.

**3. Adoption is the hard part.** Building an agent takes weeks. Getting a team to change how they work around it takes months, and nobody budgets for that. We now spend more time on rollout than on the build itself.

If you're starting now, pick the dullest process you own and automate that one first.

### Task 4: One-pager intro

**Proposal: an automated lead-enrichment pipeline**

We currently enrich inbound leads by hand. The team spends about 6 hours a week looking up company details and contact data for roughly 2,000 leads a quarter, and every hour spent on lookups is an hour not spent talking to prospects. The manual step also delays first contact, which costs us time-sensitive leads.

This proposal recommends an automated pipeline that pulls the same data from existing providers and writes it directly to the CRM. The manual work drops to a short review step, and enriched leads reach the sales team on the day they arrive. The sections below cover design, cost and rollout.

### Task 5: Rewrite

Our platform uses AI to handle the repetitive parts of your team's workflows, like copying data between systems and chasing approvals. People get that time back for work that actually needs them. That's the whole pitch: it does a dull job well, and that turns out to be worth a lot.

### Task 6: Report section

**Current state**

Ticket volume rose from 1,800 to 2,400 this quarter, an increase of 33%.

Response times improved despite the higher load. Median first-response time fell from 9 hours to 4, less than half the figure from the previous quarter. In practical terms, a player who raises a ticket in the morning now typically hears back the same afternoon rather than the following day.

These two results normally move against each other. A 33% rise in volume would usually push response times up, not down, so holding both is the strongest indicator this quarter of the operation's health.

If volume continues to grow at the current rate, capacity will come under pressure in the second half of the year. The options for addressing this are set out in the following section.

### Task 7: Recommendation memo

**Ticket-triage vendor recommendation**

To: Exec team
From: Aden
Date: 10 June 2026

We've finished the trial of the two shortlisted triage vendors. My recommendation is Parallel. I'd like approval this week so integration can start before the end of the month.

Accuracy decided it. Parallel routed 94% of trial tickets to the right team first time. Slate managed 81%, which sounds close until you flip it: Slate sends roughly one ticket in five to the wrong queue. Every misroute means a customer waiting longer and an agent re-triaging work the tool was supposed to remove.

Cost is the obvious objection. Parallel is $2,300 a month against Slate's $900, a gap of $1,400 a month or $16,800 a year. I'd still rather pay for routing that works than spend agent hours correcting routing that doesn't. The trial made that trade visible every day.

Setup also favours Slate. It runs on our existing helpdesk after a one-day setup, while Parallel needs a two-week integration. That's a real ask of the engineering team and worth weighing. It's also a one-off. The accuracy gap is what we'd live with every day after.

If you're comfortable with this, I'll confirm with Parallel this week and target go-live in early July. Happy to share the full trial data if anyone wants to dig into it.

## Outputs (baseline)

### Task 1: Slack message

Hey all, Scout is now live for everyone. It auto-summarises customer support tickets, so instead of reading a 40-message thread you get the short version up front: what the customer needs, what's been tried and where it's up to.

We're running a 30-minute training session on Thursday covering how it works and where it fits in your workflow. Calendar invite coming today. Worth joining if you touch support tickets at all.

Questions in the meantime, drop them in here or DM me.

### Task 2: Email

Subject: Moving our QBR to the following week

Hi Sarah,

A quick favour to ask. Two of our team will be travelling next Tuesday, and I'd rather have everyone in the room for the QBR than run it short-handed.

Could we move it to Tuesday 23 June at the same time? Happy to flex if that clashes with anything on your side.

Apologies for the shuffle. We've got some good results to walk you through, so looking forward to it.

Cheers,
Aden

### Task 3: LinkedIn post

A year of putting AI agents into production workflows at a blockchain gaming company. Three lessons that stuck.

1. Narrow beats clever. Our best agents do one boring thing well: summarising tickets, enriching leads, triaging alerts. Every time we built something ambitious and general, it got shelved. The boring ones run every day.

2. The workflow matters more than the model. Swapping models takes an afternoon. Getting an agent to fit how a team actually works takes months. Most of our value came from mapping the process properly before automating any of it.

3. Trust is earned in increments. Nobody hands an agent the keys on day one. We started with drafts a human approved, measured the error rate, then removed checkpoints one at a time. Slower than we wanted, faster than forcing it would have been.

None of it is glamorous. But the unglamorous stuff is what's still running a year later.

Curious what others have found, especially on the trust side.

### Task 4: One-pager intro

Proposal: Automated lead-enrichment pipeline

The team currently enriches roughly 2,000 inbound leads each quarter by hand, at a cost of about six hours every week. The work is repetitive and entirely procedural: look up the company, fill in the firmographic fields, score and route. It is the kind of task automation handles well, and it pulls capable people away from work that needs judgement.

This proposal recommends an automated pipeline that processes each lead on arrival, enriching, scoring and routing it within minutes rather than days. The build is estimated at two to three weeks using tools we already pay for, and would return around 300 hours a year to the team. With approval this week, the pipeline would be live before the end of the quarter.

### Task 5: Rewrite

Every software company promises its platform will transform your business. Ours won't, and we won't pretend otherwise. What it does is simpler: it takes the repetitive steps out of your team's workflows, so people spend less time on admin and more time on the work that actually needs a human. Teams using it save a few hours a week. That's the whole pitch, and it turns out a few hours a week adds up to a lot.

### Task 6: Report section

Current state

Support ticket volume rose 33% this quarter, from 1,800 to 2,400 tickets. The increase tracks growth in active integrations over the period and was concentrated in onboarding and API queries; incident-related tickets remained flat.

Despite the higher volume, response performance improved markedly. Median first-response time fell from nine hours to four, driven by two changes introduced early in the quarter: automated ticket summarisation, which reduced triage time for the support team, and a revised routing model that sends technical queries directly to the engineering rotation.

The team absorbed the additional volume without added headcount, and current capacity is adequate for the growth projected next quarter. A sustained rise beyond 3,000 tickets per quarter, however, would require either further automation of common query types or an additional support hire. Both options are costed in the recommendations section of this report.

### Task 7: Recommendation memo

**To:** Executive team
**From:** Aden
**Date:** 10 June 2026
**Re:** Ticket-triage vendor — recommendation to proceed with Parallel

After running both shortlisted vendors through a trial, I'm recommending we sign with Parallel at $2,300 a month. It costs more than Slate and takes longer to stand up, but it's the right tool, and I'd rather make this call once than revisit it in six months.

The trial numbers are the core of it. Parallel routed 94% of tickets correctly; Slate managed 81%. That 13-point gap sounds modest until you translate it: on our volume, Slate would misroute roughly one ticket in five. Every one of those bounces between teams, burns support time and slows the customer down.

The price difference is $1,400 a month, or about $17,000 a year. Set that against the staff hours spent manually rerouting Slate's misses and the maths favours Parallel comfortably. We'd be paying people to clean up after the cheaper tool.

Slate's strengths are real. At $900 a month with a one-day setup on our existing helpdesk, it's genuinely attractive. But setup is a one-off cost and accuracy is forever. Optimising for the easy first day would be the wrong trade.

If everyone's comfortable, I'll kick off the two-week integration with Parallel next Monday and report back once it's live. Happy to walk through the trial data with anyone before then.
