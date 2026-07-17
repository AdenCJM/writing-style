# Eval set

Writing tasks covering the formats the skill is used for, fidelity under rewriting and explicit overrides, plus a marking checklist.

## Method

1. Record the date, exact model identifier, harness, repository commit SHA and whether SKILL.md was loaded.
2. Run each task in a fresh context, once with SKILL.md loaded and once without it. Use at least three samples per arm when making comparative claims.
3. Save raw outputs unchanged before marking. Never silently repair a scored output. Put any corrected illustration after the raw sample and label it unscored.
4. Have a separate context or model mark every applicable checklist row. The generator must not mark its own output in the same session.
5. Report row-level verdicts, not only an overall pass. Record ambiguous marking calls and all failures.
6. Run both Claude Code and Codex before making cross-platform claims. Treat results from one harness as evidence for that harness only.

Register key: tasks 1, 2, 3, 5, 7, 8, 10, 13 and 14 are casual or semi-formal. Tasks 4, 6, 9, 11 and 16 are formal. Task 12 supplies its own house style. Task 15 is creative.

## Tasks

1. **Slack message** (casual). Announce to #general that an internal AI tool called "Scout" (auto-summarises customer support tickets) is now live for everyone. Mention a 30-min training session Thursday. Under 120 words.

2. **Email** (semi-formal). Ask an external partner (Sarah at a games studio) to reschedule the quarterly business review from next Tuesday to the following week because two team members will be travelling. Propose Tuesday 23 June at the same time. Professional but warm. Under 150 words.

3. **LinkedIn post** (semi-formal). Share three lessons learned from deploying AI agents into production workflows at a blockchain gaming company over the past year. Use only these supplied lessons: narrow ticket-triage agents stayed in use while general-purpose agents were retired; customer-facing messages still require human review; each live agent has a named owner who reviews errors weekly. 150–200 words.

4. **One-pager intro** (formal). A one-line document title plus the opening two paragraphs of an internal proposal recommending an automated lead-enrichment pipeline. Audience is the exec team. The team currently spends about 6 hours a week manually enriching roughly 2,000 inbound leads a quarter. The proposed pipeline would pull company size and location from the team's existing data provider, write those fields to the CRM and flag incomplete records for review. Cost and implementation time are unknown. 100–150 words.

5. **Rewrite** (semi-formal). Make this paragraph sound natural and human without adding, removing or strengthening any claim:
   > "In today's rapidly evolving technological landscape, businesses must leverage cutting-edge AI solutions to stay ahead of the curve. Our comprehensive platform empowers teams to seamlessly streamline their workflows, fostering a culture of innovation and unlocking unprecedented levels of productivity. It's not just a tool — it's a paradigm shift in how organisations navigate the complexities of digital transformation."

6. **Report section** (formal). The "Current state" section (about 150 words) of an external quarterly partner report on support operations. Ticket volume rose from 1,800 to 2,400 this quarter; median first-response time fell from 9 hours to 4. The cause of the change and the team's remaining capacity are unknown. Do not speculate about either.

7. **Recommendation memo** (semi-formal). An internal memo to the exec team recommending one of two shortlisted ticket-triage vendors after a trial: Parallel ($2,300 a month, 94% routing accuracy in the trial, two-week integration) or Slate ($900 a month, 81% accuracy, one-day setup on the existing helpdesk). Pick one and commit to it. At least five paragraphs, 200–250 words.

8. **Analysis writeup** (semi-formal). A founder asked you to pull apart whether their toy-rental startup should go narrow (one city, premium service) or wide (national, self-serve marketplace) before raising. The narrow option: about 400 paying families in one city, 70% gross margin, break-even in month 8. The wide option: needs about 5,000 users to cover logistics, burns the raise faster, no clear moat. Write up the analysis and the call you'd make, for the founder to read. End on what they should do next. 180–220 words.

9. **Uncertainty-preserving rewrite** (formal). Rewrite the following for a board paper in 60–90 words. Preserve every qualification and don't add a recommendation:
   > "Early testing suggests the device may reduce median processing time. The evidence is preliminary, and the trial did not measure safety outcomes. The device uses a fail-safe interlock classified under IEC 61508. Further testing is subject to ethics approval."

10. **Constrained product blurb** (semi-formal). Rewrite this as a natural 60–90 word website blurb without adding capabilities, integrations, customers or results:
    > "Northstar groups customer messages by topic and exports a weekly CSV. It does not reply to customers and does not connect to a CRM. Setup is completed by the customer using a documented import process."

11. **Defined terms and exact wording** (formal). Rewrite the surrounding prose in plain English while preserving the defined terms `Supplier`, `Customer Data` and `Security Incident`, and reproduce the quoted clause verbatim. Don't add legal interpretation:
    > "The Supplier has an obligation to give notice in relation to a Security Incident affecting Customer Data. The operative requirement is: 'The Supplier must notify the Customer within 48 hours of becoming aware of a Security Incident.' This provision does not state when remediation must be completed."

12. **Explicit house-style override**. Write exactly three bullet points under the exact heading `AI Safety, Security, and Governance`. Use American English and an Oxford comma. The points must cover model testing, access controls and incident response. Do not add a greeting or closing.

13. **Light tighten and do no harm** (semi-formal). Tighten the following in light mode. Make no change that is not clearly necessary:
    > "Thanks for sending this through. I've read it and agree with the recommendation. Let's discuss timing tomorrow."

14. **Audit mode** (semi-formal). Audit the paragraph from task 5 using the writing-style skill. Group the most important issues by effect on the reader. Do not provide a rewritten paragraph.

15. **Creative restraint**. Lightly edit this line from a personal essay while preserving its deliberate em dash, fragment and repetition: `I waited—and waited. No answer. Still no answer.` Correct only an objective error; if none exists, return it unchanged.

16. **Reader outcome** (formal). Draft a short internal incident update from these facts only: checkout failed for 18 minutes from 14:07; service recovered at 14:25; the cause is still under investigation; Priya owns the investigation; the next update is due at 16:00. Audience: customer support leads who need to brief their teams. 80–110 words.

Marker's note, not part of any task prompt: task 7 targets token counterpoints and metronome paragraphs. Task 8 targets the assistant-commentary frame. Tasks 9–11 target fidelity, unsupported detail and required terminology. Task 12 tests explicit overrides. Tasks 13–15 test operation, strength and restraint. Task 16 tests whether the reader can understand and act. Don't paste this note when running the tasks.

## Marking checklist

Score each piece pass/fail per row (rows scoped to specific tasks only apply there). A piece passes overall only if every applicable row passes.

| Check | Fail examples |
|---|---|
| The requested operation is followed | audit mode returns a rewrite; tighten mode rebuilds the piece |
| Editing strength is respected | task 13 receives a structural rewrite; strong mode makes only cosmetic changes to poor prose |
| Good source prose is not changed for activity's sake | task 13 replaces natural wording without a clear reader benefit |
| Creative choices survive operational defaults | task 15 removes the deliberate em dash, fragment or repetition |
| The reader can identify the purpose and any supplied action, owner or deadline | task 16 buries Priya's ownership or the 16:00 update time |
| Meaning and point of view are preserved in rewrites | promotional source becomes sceptical; a proposal becomes an approved plan |
| No unsupported facts, capabilities, examples, anecdotes, causes, results, names or commitments | task 10 claims Northstar connects to Salesforce or saves five hours a week |
| Uncertainty and evidentiary limits are preserved | task 9 changes "suggests" to "shows", drops "preliminary" or implies safety was tested |
| Required technical, legal and defined terms remain accurate | task 11 changes `Security Incident`, paraphrases the quoted clause or adds legal advice |
| Explicit user instructions override skill defaults | task 12 changes the exact heading, removes the Oxford comma or uses Australian spelling |
| No banned words or phrases, including nearest-synonym swaps, unless the source requires a precise term | leverage, "capitalise on", seamless, "frictionless", delve as filler |
| No vague intensifiers; use the numbers supplied by the task | "significantly faster" in task 4 or 6 where real numbers were given |
| No invented numbers (arithmetic derived from supplied figures passes) | "estimated at two to three weeks" with no basis in the task; a 33% rise derived from supplied 1,800→2,400 figures is fine |
| No em dashes outside quoted input text | — anywhere in fresh prose |
| No Oxford comma unless needed for ambiguity or explicitly requested | "a, b, and c" with no ambiguity outside task 12 |
| Australian spelling unless another variety is supplied or requested | -ize, -yze, -ense, -or for -our, -er for -re outside task 12 |
| Sentence-case headings (task 4 title) | "Automated Lead Enrichment: A Proposal" in Title Case |
| Dates as day month year (task 2) | "June 23rd" or "06/23" |
| At most one in-sentence triad per piece; structures the task requests (task 3's three lessons) don't count | two "x, y and z" lists in one piece |
| No "not X, but Y" template or variants | "it's not just a tool, it's a shift" |
| No rhetorical question + snappy answer | "The result? More sales." |
| No AI email furniture | "I hope this finds you well", "feel free to reach out" |
| No engagement bait or hashtag blocks | "What do you think? 👇 #AI" |
| No decorative emoji or bold lead-in decoration (numbered bold headers for a real list of things are fine) | 🚀 anywhere, "**Speed.** We ship daily." |
| Exclamation marks: max one in casual or semi-formal pieces; zero in formal pieces unless requested | "!" twice in the Slack post, any "!" in a formal report |
| No neat-bow ending | "Exciting times ahead." as the closer |
| No over-structuring (tasks 1 and 2 should be paragraphs, not header stacks) | a Slack post with three headers and a bullet list |
| No hedging stacks | "could potentially", "may possibly" |
| No token counterpoint: opinions aren't balanced with a reflexive concession; a caveat the reader needs to weigh or act on passes | "This is the right call. That said, there are trade-offs to consider." (a capacity warning with a consequence attached is not a fail) |
| No assistant-commentary frame (esp. task 8): no effort or process narration, no hand-over opener in any grammatical person, no meta-closer or offer to continue, no chummy reader-flattery; substantive first-person opinions and plain statements of what was done pass | "Here's the analysis I promised", "here's where I land", "below is the writeup", "that's my read", "want me to go deeper?", "you're well placed to pull this off" (a plain "My recommendation is X because..." or "We've finished the trial" is not a fail) |
| Contractions in casual and semi-formal pieces | "it is" where "it's" reads naturally |
| Email voice (task 2): plain subject line, "Hey Sarah," or "Hi Sarah," greeting, "Cheers" or "Thanks" sign-off | subject "Touching Base Regarding Our QBR", "Dear Sarah", "Best regards" |
| No invented sender identity | a sign-off name that wasn't supplied by the prompt or established in context |
| No colloquialisms in formal pieces | "keen", "heads-up" or "mate" in the report |
| Varied sentence rhythm; in pieces of three or more paragraphs, paragraph sizes vary too (one-sentence paragraphs and numbered list items exempt); paragraphs don't all end on a punchy fragment | three consecutive same-shape sentences, every paragraph exactly two sentences, every paragraph closing "That's it." style |
