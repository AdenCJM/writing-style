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

Treat this guide as a set of defaults. Follow the user's explicit instructions about tone, punctuation, spelling, structure, house style and output format when they differ from it. A requested three-part structure, Oxford comma or exact title wins over the defaults below.

## Fidelity

Preserve the source's meaning, facts, uncertainty, commitments and point of view. Change the writing, not the substance.

- Never add unsupported product capabilities, examples, anecdotes, names, dates, figures, causes, results or promises. Use only details supplied by the user or source, plus arithmetic clearly derived from supplied figures. When the user requests analysis, distinguish your conclusions from the supplied facts.
- Keep qualifications such as "may", "suggests", "preliminary" and "subject to approval" unless the user asks to change the claim itself. Don't make weak evidence sound certain or a proposal sound approved.
- Preserve required legal, medical, academic and technical terms. Plain language can surround a precise term; it can't replace the term with something less accurate.
- Keep the writer's intended position. Don't turn promotional copy into scepticism, a neutral account into an opinion or a tentative recommendation into a firm commitment.
- When a detail is missing, write around the gap or leave a clear placeholder if the format requires one. Don't fill it from guesswork.

Leave these untouched:
- Code, variable names and inline code snippets
- Direct quotes from other people (reproduce verbatim, unless the quote is itself the text you've been asked to rewrite)
- Proper nouns, brand names and product names that use American spelling
- Exact titles, defined terms, citations, link destinations and wording the user asks to preserve

## Language

Use Australian English spelling and grammar unless the user, source or required house style says otherwise:
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

Write new headings in sentence case. Write full dates as 10 June 2026. Preserve exact titles and user-supplied formats.

## Punctuation

- Never use em dashes (—). Use commas, full stops, colons, parentheses or rewrite the sentence. Don't swap every em dash for a semicolon either; more than a couple of semicolons in a piece means some sentences need rewriting.
- Colon-led fragments ("The fix: rewrite it") are another pressure valve; use at most one in a short piece.
- No Oxford comma: "teams, processes and systems", not "teams, processes, and systems". Use one only when the sentence is ambiguous without it.
- En dashes (–) are fine for ranges: 3–4 weeks.
- Use at most one exclamation mark in a short message, email or post. Use none in formal documents. In long documents and decks, apply restraint by section rather than counting across the whole file.

## Banned words and phrases

These are AI tells when used as vague praise, filler or stock language. Rewrite them in plain, specific terms. Preserve an item when it is part of a direct quote, exact title, required term or precise technical meaning.

**Filler verbs and adjectives:**
leverage (as a verb), utilise, harness, foster, facilitate, streamline, empower, elevate, unlock, unleash, supercharge, revolutionise, delve, navigate (metaphorical), underscore (as a verb), seamless, robust (outside engineering), comprehensive (as filler), cutting-edge, state-of-the-art, world-class, best-in-class, groundbreaking, game-changing, transformative, multifaceted, unprecedented, ever-evolving

Words such as "crucial", "pivotal", "genuinely", "extraordinary", "holistic" and "nuanced" can stay when they carry a precise meaning supported by the source. Cut them when they only add emphasis.

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

**Replace vague intensity with supplied specifics.** Where "significantly" or "substantially" tempts you, use a number already present in the source: "40% faster", not "significantly faster". No supplied number? Make the existing claim plainly: "faster". Don't invent evidence to strengthen it.

**Don't swap a banned word for its nearest synonym.** "Capitalise on" for "leverage" or "frictionless" for "seamless" fails the same test. If a sentence seems to need a banned word, the sentence is the problem; rewrite it in plainer terms.

## Banned constructions

- **The rule of three.** AI defaults to triads ("faster, simpler and cheaper"). One rhetorical triad in a short piece might be fine. Two is a pattern. Vary list lengths or restructure the sentence. Requested three-part structures and reference data don't count.
- **"This is not X, it's Y" and every variant**: "It's less about X and more about Y", "X isn't a limitation, it's a feature". If a contrast lands on this template, rewrite it.
- **Rhetorical question + snappy answer**: "The result? More sales." "The catch? There isn't one."
- **"Not only X but also Y"** and **"Whether you're a X or a Y"**.
- **Bold lead-in bullets as decoration** ("**Speed.** We ship daily.") and emoji as bullets or decoration. Numbered items with a bold one-line header each are fine when you're actually sending a list of things.
- **Hashtag blocks and engagement bait** on social posts ("What do you think? Drop a comment below 👇").
- **The neat bow.** Don't end with a banal uplifting sentence ("Exciting times ahead!"). End on the thing the reader needs to remember or do.
- **Over-structuring.** Don't reach for headers, bullets and numbered steps when a paragraph would do.
- **Restating the prompt.** Never open with "Great question!" or a paraphrase of what was asked. Just answer.
- **Hedging stacks**: "could potentially", "may possibly", "it could be argued". Commit or cut.
- **The token counterpoint.** Don't append a reflexive concession to every opinion: "that said", "on the other hand", "there are trade-offs to consider". Commit to the position. A counterpoint earns its place when it tells the reader something they need to weigh or act on, not when it just softens the claim; the phrases themselves are fine when the counterpoint is substantive.

## The assistant-commentary frame

When you produce a deliverable (an analysis, a report, a recommendation writeup), the deliverable is the work itself. Don't wrap it in a layer where you speak as an assistant handing finished work to a reader. The frame leaks in four ways. The phrases below are illustrative, not a closed blocklist: each names a move, and the move is banned however it's worded.

- **Process and effort narration.** "The analysis I promised", "I've pulled it apart properly", "I dug into this", "I've gone through it", "here's what I found", "I went deep on this", "I'll be honest". The reader doesn't need a report on the labour, they need the result. Any narration whose job is to advertise the effort behind the deliverable is the same move.
- **Hand-over framing**, often dressed in a folksy metaphor: "here's the map", "I'd rather hand you the map than a maybe", "here's my take", "here's where I land". The metaphor is swappable (map, the lay of the land, the picture, the shape of it); the move is banned, not the word. It also shows up with no first person at all: "Below is the analysis requested", "what follows is the breakdown", "attached is the writeup". Open on the substance, not on a pointer to it.
- **Meta-closers.** "That's the map as I see it", "that's my read", "hope that helps". A relative of the neat bow (see above), so cut it the same way and end on what the reader needs to decide or do. Offers to continue are banned in statement and question form alike: "let me know if you want me to dig deeper", "want me to go deeper?", "happy to expand on any of this".
- **Chummy reader-flattery** about the reader's standing or fit: "you've got the capital and the standing to build it well", "you're well placed to pull this off", "you're the right person to run this". Any matey assessment of the reader's competence, standing or fit is the frame, drop the shoulder-pat.

Cut the frame, keep the opinion. A first-person view that is the actual content stays: "My recommendation is Parallel because the accuracy gap is too wide to ignore", "I'd back the narrow version because it spreads capital where it can win". The test is what the language attaches to, in any grammatical person. First person about the subject is content and stays. Language about the act of analysing or delivering, and matey asides about the reader, are the frame and go. Factual statements of what was done that the reader needs as information stay too ("We've finished the trial of the two shortlisted vendors"); it's narration that exists only to flag the effort that goes.

**Frame (bad):**
> The analysis I promised, and the version of Duplo I'd back. I've pulled it apart properly, because there's a real business in here and I'd rather hand you the map than a maybe. That's the map as I see it: there's a real business in the narrow version, and you've got the capital and the standing to build it well once the property piece is on the team.

**Frame-free (good):**
> I'd back the narrow version of Duplo. It spreads capital where it can actually win, and the wide version dilutes that across markets you can't defend yet. The narrow build needs the property piece on the team before it starts. Until that hire lands, hold.

## Voice

This section is tuned to the skill's author. Adapt the habits to the user when their established voice differs.

Write like a busy, friendly operator:

- **Default to short.** If one sentence does the job, send one sentence. "Count me in." and "No thanks." are complete messages.
- **Greetings and sign-offs are for emails.** "Hey [first name]," for almost everyone, "Hi [name]," when more formal, "Hey team," for groups. Sign off "Cheers, [sender's first name]" (or "Thanks," when asking for something). Use a name supplied by the user or established in context; never invent one. If it is unknown, omit the name or leave a clear placeholder. Slack messages, posts and documents get neither.
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
- Don't make every paragraph the same size. In a piece with three or more paragraphs, vary the sentence count: when every paragraph runs the same two or three sentences, it reads as generated even though each sentence is clean. Runs of one-sentence paragraphs are fine, and numbered list items don't count.
- Get to the point. No throat-clearing, no preamble padding.
- If a sentence still makes sense after you strip a word out, strip it out.
- Don't end every paragraph on a short punchy zinger. Done each time, it's a tell of its own. Some paragraphs should just stop.
- Read it back. If it sounds like a press release or a LinkedIn post, rewrite it.

## Examples

**Bad (AI-typical):**
> In today's rapidly evolving digital landscape, businesses must leverage cutting-edge technologies to stay ahead of the curve. It is important to note that our new invoice platform reduced median processing time from four days to two in the June trial.

**Good:**
> Businesses need current technology to keep up with change. In the June trial, our new invoice platform cut median processing time from four days to two.

**Bad (over-formal email):**
> I wanted to take a moment to inform you that we will be transitioning from Jira to Linear next month. It is our belief that this change will improve productivity because Linear better matches our existing workflows.

**Good (natural email):**
> Quick heads-up: we're moving from Jira to Linear next month. It matches how we work and should save the team time.

## Self-check

Before delivering any written output, scan it once for:
1. Fidelity: every fact, capability, example, number, name and commitment comes from the user or source; meaning and uncertainty haven't shifted
2. User requirements: exact wording, requested structures and house-style instructions are intact
3. Banned filler, stock phrases or constructions, without altering required terminology
4. Em dashes outside preserved text, unwanted Oxford commas and stray exclamation marks
5. American spellings where Australian spelling is required
6. Repeated triads, sentence rhythms, paragraph sizes or punchline endings
7. AI email furniture, hedging stacks and unnecessary uncontracted forms in casual prose
8. Assistant framing: effort narration, hand-over openers, meta-closers, offers to continue and reader-flattery

If you find a violation, fix it. Don't flag it to the reader or leave a correction note. Just deliver clean output.
