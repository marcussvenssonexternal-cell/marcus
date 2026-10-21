# Streaming recommendations Lotties

Two 1920×1080, 30 fps Lotties of a streaming app's end-of-video flow.

## Curio landing page (`curio-*`)

One Lottie per image slot on the Curio landing page. In each one, the thing the section is
about lights up in turn:

| File | Page slot | Length | What it shows |
| --- | --- | --- | --- |
| `curio-hero` | Hero visual | 8.4 s, 1920×1080 | Interstellar's credits shrink into a mini-player. Then the three cards light up in turn, **Because You Watched → Recommendations → Similar Titles**, in the same order and 2.8 s rhythm as the rotating headline. Each highlight switches the hero to that pick. Markers: `because-you-watched`, `recommendations`, `similar-titles` |
| `curio-because-you-watched` | Three experiences: Because You Watched | 8 s, 1280×720 | What viewers who loved Interstellar watched next, shown as a slideshow. Oppenheimer, The Martian, Top Gun: Maverick and Across the Spider-Verse light up in turn; the row slides one card left before the fourth |
| `curio-personalized-recommendations` | Three experiences: Personalized Recommendations | 6 s, 1280×720 | A new viewer on day one, with 2 titles watched, gets mood rows (Thought-Provoking Sci-Fi, High-Stakes Thrills). Two picks light up and show their mood tags |
| `curio-similar-titles` | Three experiences: Similar Titles | 6 s, 1280×720 | Interstellar's title page. As Arrival, then The Martian, lights up, so do the mood tags each one shares with Interstellar |

- **Section stills:** to keep the page calm, Personalized Recommendations and Similar Titles use still images in `stills/`. The hero and the Because You Watched slideshow are the only animations. Stills for all three sections rendered at 2560×1440 (WebP + JPEG) from each section Lottie at its highlighted moment, via `./render_stills.sh`. The section Lotties stay in the repo in case one of them should move again.
- **Blurred variants:** the `-blurred` files blur the movie artwork, like the screenshots currently on the page.
- **Readability:** the section Lotties use large type, so they stay readable at about 640px wide.
- **Previews:** in `previews/`.
- **Build:** `python3 build_curio.py`, and `CURIO_BLUR=1 python3 build_curio.py` for the blurred set.
- **Hero sync:** if the hero Lottie and the headline start together, they stay in step (8.4 s = 3 × 2.8 s).

## Agentic Layer landing page (`agentic-*`)

Same approach as Curio, for the Agentic Layer page. One "Space Night" campaign runs through
every visual:

| File | Page slot | Length | What it shows |
| --- | --- | --- | --- |
| `agentic-hero` | Hero visual | 8.4 s, 1920×1080 | A request is typed into the agent and sent. Then its three results light up in turn, **Curated Lists → Clips in Every Ratio → Branded Thumbnails**, with the agent's replies building up in the conversation. It ends on "Approve & publish". Same 252-frame timing as `curio-hero` (beats at 61 / 99 / 183, hold frame 90), so the page's rotating headline drives it without script changes. Markers: `curated-lists`, `clips-in-every-ratio`, `branded-thumbnails` |
| `agentic-curated-lists` | What the agent does: Curated Lists | 8 s, 1280×720 | Asked "Give me 5 space movies for a Friday night line-up", the Curation Agent ranks five titles by relevance; the highlight walks down the list |
| `agentic-clips` | What the agent does: Clips in Every Ratio | still, 1280×720 | Asked for a 30-second clip of the low-level canyon flight in Top Gun: Maverick, the Creative Agent cuts the same scene in 16:9 for TV, 1:1 for feeds and 9:16 for TikTok |
| `agentic-branded-thumbnails` | What the agent does: Branded Thumbnails | still, 1280×720 | Thumbnails for Arrival, Sunshine and The Martian, each from the same scene as the hero's first clip, with the title's lettering placed and checked off in 16:9, 1:1 and 9:16, then "Approve & publish" |

- **Hero v3 (on the page):** `agentic-hero-v3` (18.5 s, 1920×1080, loops on its own, transparent background so it sits on the page). It's about vertical clips:
  - **Opening:** no frame, just the question, the input and three suggestions (scenes by mood, vertical 9:16 clips, ready for TikTok). Each suggestion lights up as its word is typed.
  - **Send:** the request "Turn the most intense scenes in 3 sci-fi films into vertical TikTok clips" is typed one letter at a time. On send, the input grows into the chat, still alone in the middle as one box. Then the chat docks right and the workspace opens out from behind it to the left, the Creative Agent's own layout.
  - **Results:** each film (Arrival, Sunshine, The Martian) gets a row: poster, title, "Open in Creative Lab", and four clips. Each clip arrives as the 16:9 shot and reframes to 9:16 around its subject, then plays. The agent ticks the top clips "Added to list", and the view scrolls to the next film.
  - **Files:** preview on the page's navy: `previews/agentic-hero-v3.mp4`; transparent poster: `posters/agentic-hero-v3.webp`.
  - It goes with a static headline, not the rotating one. `render_preview.cjs` takes `--bg <colour>` and `--transparent` for Lotties like this one.
- **Section look:** the three section visuals share the hero's style: an "Agentic Layer" window, the request in a blue bubble, the agent's answer in a card, and the result below. There's nothing to import by hand; people only approve.
- **Stills and posters:** `stills/agentic-*` (2560×1440) and `posters/agentic-*` (the frame shown before an animation loads, or instead of it with reduced motion) are rendered by `./render_stills.sh`.
- **Share image:** `posters/agentic-og.jpg` (1200×630) is the page's social preview: the headline next to the clip cards and chat from the v3 hero.
- **Previews:** `previews/agentic-hero.mp4`, `previews/agentic-curated-lists.mp4`.
- **Build:** `python3 build_agentic.py`. It reuses the Curio UI pieces (`curio_ui.py`, `build_curio.py`) and artwork.
- The relevance scores, timecodes and title lettering are illustrative, like the rest of the demo UI.

## Vionlabs version (`vionlabs-recommendations.*`)

16 s, styled after the Vionlabs demo UI, using the movies from the demo recording:

| Time | What happens |
| --- | --- |
| 0.0–3.3 s | Fullscreen: Interstellar has ended and the end credits roll |
| 3.3–4.5 s | The credits shrink into a mini-player (top left), with a "Did you enjoy it?" prompt underneath |
| 3.9–5.3 s | Top Gun: Maverick fills the screen behind it: title, genre and mood tags, "Play now" / "Playing preview in", and three cards: **Recommended for you**, **Similar titles**, **Since you watched Interstellar** |
| 5.3–8.3 s | "Playing preview in 3 · 2 · 1" countdown |
| 8.3–11.0 s | The preview plays full screen |
| 11.0–12.7 s | The page scrolls down to two rails: **Recommended for you** (Top Gun: Maverick, No Hard Feelings, Spider-Man: Across the Spider-Verse, Oppenheimer) and **Similar titles**, labelled "Because you watched Interstellar" (The Martian, Arrival, 2001: A Space Odyssey, Sunshine) |
| 13.1–15.4 s | Focus lands on The Martian: the card enlarges, plays a preview and shows genres and mood tags |
| 15.4–16 s | Fade to black for a clean loop |

The movie images in `images/` were cropped from the demo recording. The full-screen hero
(`topgun_hero.jpg`) is upscaled from a thumbnail, so swap in a high-res still for a sharper result.
Everything else (UI, credits, icons, logo) is vector. Built by `build_vionlabs.py`, previewed in
`vionlabs-preview.mp4`.

## Generic version (`streaming-recommendations.*`)

12 s, with placeholder titles and illustrated artwork:

| Time | What happens |
| --- | --- |
| 0.0–2.8 s | Fullscreen playback: the last shot of *Sky Pilots*, jets fly into the sunset, end title fades in, the progress bar runs out |
| 2.8–4.0 s | The finished video shrinks into a mini-player (top left) and the home screen appears behind it |
| 3.7–5.0 s | Hero for the next title (*Wild Road*) plus three rails: **Recommended**, **Similar titles**, **Since you watched Sky Pilots** |
| 5.0–8.0 s | "Playing preview in 3 · 2 · 1" countdown |
| 8.0–11.5 s | The hero preview plays (parallax road trip), credits keep rolling in the mini-player |
| 11.5–12 s | Fade to black so the loop restarts cleanly |

All titles, names and artwork in this version are placeholders. Built by `build.py`, previewed in `preview.mp4`.

## Files

- `*.json`: the Lotties (Bodymovin 5.12 format). `*.lottie` is the same animation as a dotLottie, which is much smaller.
- `lottie_kit.py` / `curio_ui.py`: shared helpers and UI pieces. Text is converted to outlines, so no fonts are needed at playback.
- `render_preview.cjs`: renders frames with lottie-web in headless Chromium

## Editing

Text, colours and timing are set in the build scripts. The timeline constants (`T_SHRINK`,
`T_SCROLL`, `T_HOVER`, …) are at the top. In the Vionlabs version, titles, tags and rails are in
`HERO`, `HERO_CARDS` and `ROWS`. To rebuild:

```sh
pip install fonttools uharfbuzz pillow   # uses the Inter font (OFL)
python3 build_vionlabs.py                # or build.py; writes the .json and .lottie
npm install && node render_preview.cjs streaming-recommendations.json frames
ffmpeg -framerate 30 -i frames/frame_%04d.png -pix_fmt yuv420p preview.mp4
```

Icons are from Material Design Icons (Apache 2.0).
