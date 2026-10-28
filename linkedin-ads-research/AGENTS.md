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
  Images are in `creatives/brief/png/<asset>.png`, videos in `creatives/brief/video/<asset>.mp4`.
- **Copy variants:** headline `h1`–`h3` and intro text `i1`–`i3`, in the order they appear in `copy.json`.

Use these in LinkedIn so results can be traced:
- **Ad name:** `<ad>/<asset>/<headline>-<intro>`, e.g. `v1/v1-S/h2-i1`.
- **Campaign name:** `AIBFE | <ad> | <audience>`, e.g. `AIBFE | v2 | ad ops`.
- **UTM on every link:** `utm_source=linkedin&utm_medium=paid_social&utm_campaign=ai-built-for-entertainment&utm_content=<ad>-<asset>-<headline>-<intro>`.

## Where things are

- `creatives/brief/copy.json`: every ad's assets, three headlines, three intro texts, targeting and claim checks
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

## Data

LinkedIn Ads is connected through Supermetrics (source `LIA`). LinkedIn Pages is not connected yet.
