# Streaming recommendations Lottie

A 12 s, 1920×1080, 30 fps Lottie of a streaming app's end-of-video flow:

| Time | What happens |
| --- | --- |
| 0.0–2.8 s | Fullscreen playback: the last shot of *Sky Pilots*, jets fly into the sunset, end title fades in, the progress bar runs out |
| 2.8–4.0 s | The finished video shrinks into a mini-player (top left) and the home screen appears behind it |
| 3.7–5.0 s | Hero for the next title (*Wild Road*) plus three rails: **Recommended**, **Similar titles**, **Since you watched Sky Pilots** |
| 5.0–8.0 s | "Playing preview in 3 · 2 · 1" countdown |
| 8.0–11.5 s | The hero preview plays (parallax road trip), credits keep rolling in the mini-player |
| 11.5–12 s | Fade to black so the loop restarts cleanly |

## Files

- `streaming-recommendations.json`: the Lottie (Bodymovin 5.12 format)
- `streaming-recommendations.lottie`: the same animation as a dotLottie
- `preview.mp4`: a render of the Lottie made with lottie-web
- `build.py` / `lottie_kit.py`: generator scripts. All artwork is vector, and text is converted to outlines, so no fonts are needed at playback.
- `render_preview.cjs`: renders frames with lottie-web in headless Chromium

All titles, names and artwork are placeholders.

## Editing

Text, colours and timing are set in `build.py`. The timeline constants (`T_SHRINK`, `T_COUNT`,
`T_PREVIEW`, …) are at the top, and the rail labels are in `build_main()`. To rebuild:

```sh
pip install fonttools uharfbuzz          # uses the Inter font (OFL)
python3 build.py                         # writes the .json and .lottie
npm install && node render_preview.cjs streaming-recommendations.json frames
ffmpeg -framerate 30 -i frames/frame_%04d.png -pix_fmt yuv420p preview.mp4
```

Icons are from Material Design Icons (Apache 2.0).
