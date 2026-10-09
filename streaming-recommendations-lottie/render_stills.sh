#!/usr/bin/env bash
# Renders the static section images for the Curio page from the section Lotties,
# at 2x (2560x1440), as WebP and JPEG. Needs node + playwright + lottie-web and Pillow.
#   ./render_stills.sh
set -euo pipefail
cd "$(dirname "$0")"
mkdir -p stills
tmp=$(mktemp -d)
# frame where everything is in and the section's highlight is fully on
for spec in curio-because-you-watched:120 curio-personalized-recommendations:112 curio-similar-titles:104; do
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
