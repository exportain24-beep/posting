#!/usr/bin/env bash
# One-time environment check. Fonts ship in assets/fonts; this only verifies tools.
set -e; D="$(cd "$(dirname "$0")/.." && pwd)"
command -v ffmpeg >/dev/null || { echo "ffmpeg missing (apt-get install -y ffmpeg)"; exit 1; }
python3 -c "import playwright, PIL" 2>/dev/null || pip install --break-system-packages playwright pillow
ls "$D"/assets/fonts/NotoSansBengali-Bold.ttf >/dev/null || {
  echo "fetching Noto Sans Bengali via git sparse clone"; cd /tmp && rm -rf nf && git clone --depth 1 --filter=blob:none --sparse https://github.com/googlefonts/noto-fonts.git nf \
  && cd nf && git sparse-checkout set hinted/ttf/NotoSansBengali && cp hinted/ttf/NotoSansBengali/NotoSansBengali-{Regular,SemiBold,Bold,ExtraBold}.ttf "$D/assets/fonts/"; }
python3 - <<'PY'
from playwright.sync_api import sync_playwright
with sync_playwright() as p: b=p.chromium.launch(); b.close(); print("chromium OK")
PY
echo "ready: $D"
