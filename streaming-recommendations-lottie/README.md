# Streaming recommendations Lotties

Two 1920×1080, 30 fps Lotties of a streaming app's end-of-video flow.

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
- `lottie_kit.py`: shared helpers. Text is converted to outlines, so no fonts are needed at playback.
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
