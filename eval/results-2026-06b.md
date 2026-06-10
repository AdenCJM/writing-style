# Eval results: June 2026, second run (pacing and counterpoint rules)

- **Date:** 10 June 2026
- **Model:** Claude (Fable 5) via Claude Code, fresh subagent context per run
- **Skill version:** pacing-and-counterpoint-rules branch (adds the paragraph-pacing rule, the token-counterpoint ban and the matching self-check and checklist rows)
- **Method:** two runs of the six tasks in [PROMPTS.md](PROMPTS.md), one with SKILL.md loaded and one unguided baseline, both marked row by row against the updated checklist.

## With skill: verdicts

| Task | Verdict | Notes |
|---|---|---|
| 1. Slack message | Pass | No greeting or sign-off, zero exclamation marks, paragraph sizes vary (1, 2 and 2 sentences) |
| 2. Email | Pass | Plain subject, "Hi Sarah," greeting, "Thanks" sign-off, "Tuesday 23 June" date format |
| 3. LinkedIn post | Pass | Requested three-lesson structure, no in-sentence triads, closer is an action not engagement bait |
| 4. One-pager intro | Pass | Sentence-case title, only the supplied numbers, one allowed triad ("design, cost and rollout") |
| 5. Rewrite | Pass | All slop removed, no templates, no token counterpoint |
| 6. Report section | Pass | Formal register held, paragraph sizes vary (1, 3, 2 and 2 sentences), caveat in the close changes what the reader should do so it stays |

Every piece passed every applicable checklist row, including the two new rows. One judgement call: the report opens with "rose from 1,800 to 2,400, an increase of 33%". The 33% is arithmetic on the supplied figures, not an invented statistic, so it passes the no-invented-numbers row.

## Baseline (no skill, same six tasks, fresh run)

Three of six failed. The unguided model writes far cleaner than the mid-2025-era baseline (no emoji, no hashtags, no em dashes, no "I hope this finds you well"), so the gap has narrowed, but the failures that remain are exactly the ones the skill targets:

- **LinkedIn post: fail.** Two in-sentence triads ("summarising tickets, enriching leads, triaging alerts" and "started with drafts a human approved, measured the error rate, then removed checkpoints") plus an engagement-bait closer ("Curious what others have found, especially on the trust side.").
- **One-pager intro: fail.** Invented numbers with no basis in the task ("estimated at two to three weeks", "around 300 hours a year") and two in-sentence triads.
- **Report section: fail.** An invented capacity threshold ("a sustained rise beyond 3,000 tickets per quarter") presented as a planning figure.
- Slack message, email and rewrite passed.

On the two new rows specifically: the baseline didn't happen to produce uniform paragraph blocks or token counterpoints in this run, so they didn't separate the arms this time. They're guardrails for a known failure mode rather than the main source of baseline failures, which are now concentrated in invented numbers and triad stacking.

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
