#!/usr/bin/env bash
# Renders the static section images for the Curio page from the section Lotties,
# at 2x (2560x1440), as WebP and JPEG. Needs node + playwright + lottie-web and Pillow.
#   ./render_stills.sh
set -euo pipefail
cd "$(dirname "$0")"
mkdir -p stills
tmp=$(mktemp -d)
# frame where everything is in and the section's highlight is fully on
for spec in curio-because-you-watched:60 curio-personalized-recommendations:112 curio-similar-titles:104; do
  name=${spec%%:*}; frame=${spec##*:}
  for variant in "" "-blurred"; do
    node render_preview.cjs "$name$variant.json" "$tmp/$name$variant" --width 2560 --frames "$frame" >/dev/null
    python3 - "$tmp/$name$variant/frame_$(printf %04d "$frame").png" "stills/$name$variant" <<'PY'
import sys
from PIL import Image
src, out = sys.argv[1], sys.argv[2]
im = Image.open(src).convert("RGB")
im.save(out + ".webp", quality=88, method=6)
im.save(out + ".jpg", quality=88, optimize=True, progressive=True)
PY
    echo "stills/$name$variant.{webp,jpg}"
  done
done
# Agentic Layer page: the v1 hero poster
node render_preview.cjs agentic-hero.json "$tmp/agentic-hero" --width 1920 --frames 90 >/dev/null
python3 - "$tmp/agentic-hero/frame_0090.png" posters/agentic-hero <<'PY'
import sys
from PIL import Image
src, out = sys.argv[1], sys.argv[2]
im = Image.open(src).convert("RGB")
im.save(out + ".webp", quality=88, method=6)
im.save(out + ".jpg", quality=88, optimize=True, progressive=True)
PY
echo "posters/agentic-hero.{webp,jpg}"
# The hero v3 and the section visuals have no background of their own, so they keep transparency
# (WebP), plus a JPEG on the page's navy. Section stills, and posters shown before (or instead of)
# each animation.
for spec in agentic-hero-v3:424:1920:posters agentic-curated-lists:60:1920:posters \
            agentic-clips:60:1920:stills agentic-branded-thumbnails:60:1920:stills; do
  IFS=: read -r name frame width dir <<<"$spec"
  mkdir -p "$dir"
  node render_preview.cjs "$name.json" "$tmp/$name" --width "$width" --frames "$frame" --transparent >/dev/null
  python3 - "$tmp/$name/frame_$(printf %04d "$frame").png" "$dir/$name" <<'PY'
import sys
from PIL import Image
src, out = sys.argv[1], sys.argv[2]
im = Image.open(src).convert("RGBA")
im.save(out + ".webp", quality=86, method=6)
bg = Image.new("RGBA", im.size, "#0a1322")
Image.alpha_composite(bg, im).convert("RGB").save(out + ".jpg", quality=86, optimize=True, progressive=True)
PY
  echo "$dir/$name.{webp,jpg}"
done
