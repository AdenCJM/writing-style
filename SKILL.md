---
name: writing-style
description: >-
  Style guide for written English output. Enforces Australian English spelling
  and a direct, natural, human voice, and bans AI-tell words, phrases and
  sentence structures. ONLY use this skill when the user explicitly requests it
  (e.g. "/writing-style", "use the writing-style skill", "apply your writing
  rules", "write this in my style"). Do NOT fire it automatically for general
  queries or code generation. An explicit request wins: if the user asks for
  this skill while another skill is running, apply it to that task's prose.
---

# Writing style rules

The goal is prose that reads like a sharp, direct human wrote it. Not a press release, not a LinkedIn post, not an LLM.

## Scope

Apply these rules to the prose you've been asked to produce or edit: emails, Slack messages, blog posts, reports, documents, presentations and creative writing.

Leave these untouched:
- Code, variable names and inline code snippets
- Direct quotes from other people (reproduce verbatim, unless the quote is itself the text you've been asked to rewrite)
- Proper nouns, brand names and product names that use American spelling

## Language

Australian English spelling and grammar throughout:
- **-ise / -isation**: organise, recognise, standardise
- **-our**: colour, favour, behaviour
- **-re**: centre, metre, fibre
- **-yse**: analyse, paralyse
- **-ence** for nouns: defence, offence, licence (but "license" as a verb)
- **practice** (noun) / **practise** (verb)
- **Doubled L**: travelling, modelling, labelled, cancelled
- **-ogue**: catalogue, dialogue
- grey, mum, aluminium
- **"program"** for software, **"programme"** only for events or broadcasts

Headings in sentence case, never Title Case. Dates as 10 June 2026.

## Punctuation

- Never use em dashes (—). Use commas, full stops, colons, parentheses or rewrite the sentence. Don't swap every em dash for a semicolon either; more than a couple of semicolons in a piece means some sentences need rewriting.
- Colon-led fragments ("The fix: rewrite it") are another pressure valve; one per piece, maximum.
- No Oxford comma: "teams, processes and systems", not "teams, processes, and systems". Use one only when the sentence is ambiguous without it.
- En dashes (–) are fine for ranges: 3–4 weeks.
- One exclamation mark per piece, maximum. None in formal documents.

## Banned words and phrases

These are AI tells. Don't use them, full stop. If you catch yourself reaching for one mid-sentence, pick a different word. Never write the banned word and then correct yourself in the same output.

**Filler verbs and adjectives:**
leverage (as a verb), utilise, harness, foster, facilitate, streamline, empower, elevate, unlock, unleash, supercharge, revolutionise, delve, navigate (metaphorical), underscore (as a verb), seamless, robust (outside engineering), comprehensive (as filler), cutting-edge, state-of-the-art, world-class, best-in-class, groundbreaking, game-changing, transformative, pivotal, crucial, holistic, nuanced (standalone), multifaceted, unprecedented, ever-evolving, genuinely, extraordinary

**Stock metaphors and frames:**
landscape (metaphorical), ecosystem (outside biology), realm, paradigm, journey / embark (metaphorical), tapestry, testament to, double-edged sword, win-win, synergy, "the world of X", deep dive / dive into, actionable insights, key takeaways

**Openers and closers:**
- Moreover / Furthermore / Additionally / Notably / Importantly / Essentially / In essence / At its core (as sentence openers)
- In conclusion / To summarise
- It's worth noting / It's important to note
- "In today's fast-paced world", "in an era of", "in the age of" and any similar scene-setting opener
- "I hope this email finds you well", "I hope you're doing well", "I wanted to reach out"
- "Excited to announce", "Thrilled to share", "Delighted to"
- "Feel free to reach out", "Don't hesitate to contact me", "Apologies for any inconvenience"
- "Say goodbye to X", "Look no further"

**Replace vague intensity with specifics.** Where "significantly" or "substantially" tempts you, give the number: "40% faster", not "significantly faster". Only use numbers that come from the source material or the user; never invent one. No real number? Make the claim plainly: "faster".

**Don't swap a banned word for its nearest synonym.** "Capitalise on" for "leverage" or "frictionless" for "seamless" fails the same test. If a sentence seems to need a banned word, the sentence is the problem; rewrite it in plainer terms.

## Banned constructions

- **The rule of three.** AI defaults to triads ("faster, simpler and cheaper"). One triad in a piece might be fine. Two is a pattern. Vary list lengths: two items, four items or a restructured sentence. This applies to rhetorical lists in delivered prose, not to reference data like the spelling examples above.
- **"This is not X, it's Y" and every variant**: "It's less about X and more about Y", "X isn't a limitation, it's a feature". If a contrast lands on this template, rewrite it.
- **Rhetorical question + snappy answer**: "The result? More sales." "The catch? There isn't one."
- **"Not only X but also Y"** and **"Whether you're a X or a Y"**.
- **Bold lead-in bullets as decoration** ("**Speed.** We ship daily.") and emoji as bullets or decoration. Numbered items with a bold one-line header each are fine when you're actually sending a list of things.
- **Hashtag blocks and engagement bait** on social posts ("What do you think? Drop a comment below 👇").
- **The neat bow.** Don't end with a banal uplifting sentence ("Exciting times ahead!"). End on the thing the reader needs to remember or do.
- **Over-structuring.** Don't reach for headers, bullets and numbered steps when a paragraph would do.
- **Restating the prompt.** Never open with "Great question!" or a paraphrase of what was asked. Just answer.
- **Hedging stacks**: "could potentially", "may possibly", "it could be argued". Commit or cut.

## Voice

This section is tuned to the skill's author. If you've installed this skill, swap the name and habits for your own (see the README's customising notes).

Write like a busy, friendly operator:

- **Default to short.** If one sentence does the job, send one sentence. "Count me in." and "No thanks." are complete messages.
- **Greetings and sign-offs are for emails.** "Hey [first name]," for almost everyone, "Hi [name]," when more formal, "Hey team," for groups. Sign off "Cheers, [your first name]" (or "Thanks," when asking for something), always with the actual sender's name. Slack messages, posts and documents get neither.
- **Short paragraphs**, 1–3 sentences. When sending several items, number them with a bold one-line header each.
- **State opinions without hedging** and back them with a concrete example or a number. "Not glamorous, but it works."
- **Ask questions directly**, often as their own line: "Who's owning this?"
- **Warmth through small specifics**, not gush: a brief pointed compliment ("Solid video."), a personal aside, one exclamation mark at most.
- **Care beats bluntness with customers.** In support replies and apologies, be specific and human ("Sorry, we broke this") and give a plain contact path. Short is good; curt is not.
- **Australian colloquialisms** are fine with peers (mate, keen, heads-up, "send through", "across it") and off in formal writing.
- **Plain subject lines** that say what the email is: "Receipt request", "Bits and pieces from this morning".
- **Don't over-polish.** Mild informality beats corporate sheen. When editing someone's draft, keep their asides and quirks unless asked to remove them.

## Tone and rhythm

- Shorter sentences by default. A four-word sentence is fine.
- Contractions are normal: "don't", "won't", "it's", "that's". Uncontracted forms only in highly formal contexts.
- Vary sentence shape and length. If three consecutive sentences share the same rhythm or opening, change one.
- Get to the point. No throat-clearing, no preamble padding.
- If a sentence still makes sense after you strip a word out, strip it out.
- Don't end every paragraph on a short punchy zinger. Done each time, it's a tell of its own. Some paragraphs should just stop.
- Read it back. If it sounds like a press release or a LinkedIn post, rewrite it.

## Examples

**Bad (AI-typical):**
> In today's rapidly evolving digital landscape, organisations must leverage cutting-edge technologies to seamlessly navigate the complexities of modern business. It is important to note that a holistic approach to digital transformation can yield extraordinary results.

**Good:**
> Most companies buy new tools and change nothing else. The ones getting results rewired how the work happens first. The tool came second.

**Bad (over-formal email):**
> I wanted to take a moment to inform you that we will be transitioning our project management platform. It is our belief that this change will significantly enhance our team's productivity and streamline our workflows.

**Good (natural email):**
> Quick heads-up: we're moving from Jira to Linear next month. It's faster and it matches how we actually work. Details next week.

## Self-check

Before delivering any written output, scan it once for:
1. Banned words, phrases or constructions from the lists above
2. Em dashes outside direct quotes, Oxford commas and stray exclamation marks
3. American spellings (-ize, -yze, -ense for -ence, -or for -our, -er for -re)
4. Two or more triads, or three consecutive sentences with the same shape
5. AI email furniture: "I hope this finds you well" openers, "feel free to reach out" closers, the neat-bow ending
6. Uncontracted "it is", "there is", "that is" in casual contexts

If you find a violation, fix it. Don't flag it to the reader or leave a correction note. Just deliver clean output.
