# Agents on the Vionlabs LinkedIn ads

Two Claude Code sessions work on these ads together, and Marcus decides. This file is how they find each
other and what each one owns.

| Agent | Session | Owns | Branch |
| --- | --- | --- | --- |
| **Creative** | `session_015zQo2DxndqXYRPj5MCGL5s` | Images, videos, copy, the review page and share links (`creatives/`) | `claude/exciting-cerf-d0xnu7` |
| **Optimization** | `session_01V9gwdqJSbDxs4Z7JKFuXKZ` | Performance data, tests, recommendations (`optimization/`) | `claude/linkedin-ads-optimization` |

Optimization session: `session_01V9gwdqJSbDxs4Z7JKFuXKZ` ("Vionlabs LinkedIn ads optimization")

## Talking to each other

Send a message with the `send_message` tool (claude-code-remote) to the other agent's session ID. Keep each message
self-contained, with:
- the **ad or asset ID** (see below);
- **what you found or what you need**, with the numbers and date range behind it;
- **what you're asking for**: a new variant, a copy change, a new format, a pause.

The creative agent replies with what it made, the new asset IDs and their share links. Anything that changes
spend, budgets, targeting or what is live goes to Marcus first, never straight to LinkedIn.

## IDs: how a result maps back to a creative

Everything is keyed by the IDs in `creatives/brief/copy.json`:
- **Ad IDs:** `ad0`–`ad3` (brand and audience ads), `m1`–`m3`, `c1`–`c3`, `o1` (feature follow-ups), `v1`–`v4` (video series).
- **Asset IDs:** one file each, e.g. `a2-c3` (Ad 2, carousel card 3), `m1-L` (1200×627), `v2-S` / `v2-V` (video, 1:1 / 9:16).
  A whole carousel, as one LinkedIn ad, is its card prefix plus `-carousel`, e.g. `a2-carousel`; a revised card set
  gets its own ID, e.g. `a0b-carousel`. Carousels have no ad-level headline: their `h1` stands for their card
  headlines, which are in `carousel-cards.csv` with one tracked URL per card (`utm_content` ends `-c<card>`).
  Variants get a letter, e.g. `v1b-S` (Video 1, variant B). Rights-safe revisions get an `r`: `a3r-L`, `v1br-S`, card
  `o1-c2r`, carousel `o1r-carousel` (see `creatives/brief/rights-check.md`); none has been in a LinkedIn draft yet.
  Images are in `creatives/brief/png/<asset>.png`, videos in `creatives/brief/video/<asset>.mp4`.
- **Copy variants:** headline `h1`–`h3` and intro text `i1`–`i3`, in the order they appear in `copy.json`.
  Ad 0 also has `i4`, written for pay-TV and telco operators, and `i5`, the first intro rewritten for the new hero
  frame from Papillon (`a0r-L`, `a0r-S`, `ad0r-*`). Ad 3 and M2 have an `i4` with no unverified claims.

Use these in LinkedIn so results can be traced:
- **Ad name:** `<ad>/<asset>/<headline>-<intro>`, e.g. `v1/v1-S/h2-i1`.
- **Campaign name:** `AIBFE | <ad> | <audience>`, e.g. `AIBFE | v2 | ad ops`.
- **UTM on every link:** `utm_source=linkedin&utm_medium=paid_social&utm_campaign=ai-built-for-entertainment&utm_content=<ad>-<asset>-<headline>-<intro>`.

## Where things are

- `creatives/brief/launch.csv`: every LinkedIn ad to build (asset × headline × intro), with its ad name, headline
  and full tracked URL; `first_wave = yes` marks the first test wave in `optimization/plan.md`. A `status` saying
  "retired" means don't build it: the row stays for traceability and names the asset to use instead, once approved;
  "awaiting Marcus's approval" means don't build it yet
- `creatives/brief/carousel-cards.csv`: each carousel card's headline (≤ 45 characters) and tracked URL, with the same `status`
- `creatives/brief/rights-check.md`: the board's rule for film and TV imagery, what was retired and what replaced it
- `creatives/approve.html`, published at https://claude.ai/artifact/LK5tRig3ZafiXWbs5te7dv: Marcus approves each
  rights swap there. His decisions are in that artifact's `decisions` collection (ArtifactData), one document per
  change, status `approved` or `changes` with a note. Only an approved change may be swapped in LinkedIn
- `creatives/brief/copy.json`: every ad's assets, headlines, intro texts, targeting, destination page and claim checks
- `creatives/share/links.json`: each ad's own share link; full review page: https://claude.ai/artifact/RedxbdkboDwKTX5Cm22UtR
- `references/twelvelabs-videos.md`: what we took from TwelveLabs' video ads
- `README.md`: how to re-render images and videos and rebuild the review page

## Rules for new creative

From Viktor's ad brief:
- CTA "Book a demo".
- At most 8 words on the image.
- Headlines ≤ 70 characters; intro texts ≤ 600, with the hook in the first 150.
- Every intro ends "Vionlabs. AI built for entertainment."
- Only use the brief's numbers. Claims marked "Check before launch" in `copy.json` need a source before they run.

From the board (Oct 2026):
- Famous film and TV titles only as small posters among many, never as one big frame or close-up. A big frame
  (player, phone, hero image) shows a lesser-known title (the list is in `creatives/brief/rights-check.md`).
  `node rights-audit.cjs` must pass: no famous title over 7.5% of a square the width of the ad.
- Marcus approves every new or changed creative before it goes to LinkedIn. New assets carry `"approval": "pending"`
  in `copy.json`, and their `launch.csv` rows say "awaiting Marcus's approval" until then.

Once an asset or URL is in a campaign draft (from commit `2954e0d` on), it never changes: a revised image, video or
copy line gets a new ID (e.g. `a3-L` becomes `a3c-L`, a new intro becomes `i5`) and new rows in `launch.csv`, so
every result stays traceable to exactly what ran.

## Data

LinkedIn Ads is connected through Supermetrics (source `LIA`). LinkedIn Pages is not connected yet.
