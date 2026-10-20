---
name: human-prose
description: Write or rewrite content (blog posts, LinkedIn articles and posts, carousel captions, newsletters, press copy) so it reads like careful human prose rather than typical LLM output. Use for all content and blog writing, and as the final pass on every draft before it's published or handed to the team.
---

# Human prose

Use this for every piece of content writing: when drafting from scratch, and as a separate final
pass over any draft (yours, the content bot's, the radar's, or a teammate's) before it's published.

## The rewrite

Rewrite the text below so it reads like careful human prose rather than typical LLM output. Keep the meaning, facts, and level of detail intact; change only how it's expressed.

Avoid these patterns:
- Negative parallelism: "No X, no Y – just Z", "It's not X, it's Y", "Not only X, but Y". State what is true directly instead of first dismissing what isn't.
- Easy/hard foils: "Anyone can X. Y is the hard part." Make the point without setting up a straw contrast.
- Reflexive triads: lists of exactly three items or clauses used for rhythm rather than because there are three things to say.
- Punchy kicker sentences at the end of paragraphs that restate the point as a lesson or aphorism.
- Em-dashes (—) used for dramatic pivots or asides; use commas, parentheses, colons, or separate sentences instead.

Vary sentence length naturally, connect ideas with plain logical links (because, so, although) where they help, and let paragraphs end when the content ends. Don't add a summary or moral that wasn't in the original.

## How to apply it

1. Read the whole piece once for meaning. Note every number, name, quote, link and `[check]` or
   `[Arash: …]` / `[Team: …]` placeholder: these survive the rewrite unchanged.
2. Run the checker for a list of likely problem spots (it's a hint list, not a verdict):
   `python3 content-engine/bot/prose_check.py <file.md|file.txt|topic.json>`
3. Go paragraph by paragraph:
   - A sentence that dismisses something before saying what's true ("isn't X, it's Y", "X, not Y",
     "more A, not fewer"): say the true thing directly.
   - A paragraph whose last sentence restates the paragraph as a lesson: cut it, or fold the
     content into the sentence before.
   - A list of three: keep it only if there really are three things. Otherwise use the real number.
   - An em-dash: replace with a comma, parentheses, a colon or a full stop.
   - A run of short sentences, or of fragments, used for rhythm: join the ones that belong together
     with because, so, although, which.
4. Keep the house voice from `content-engine/config/brand.md` (warm, specific, first line is the
   opinion, a specific closing question). When this skill and the voice rules pull in different
   directions, keep the facts and the opening opinion, and follow this skill for sentence shape.
5. Read it aloud in your head. If a sentence sounds like a slogan, rewrite it as something a person
   would say across a table.

Don't add new claims, summaries or morals, and don't shorten the piece by dropping detail.
