#!/usr/bin/env bash
# One-time per run: make a Shorts copy of the video engine (the owner's skill stays untouched) with
#  * WebGL (SwiftShader) enabled + file:// module access for the realistic 3D layer (r3d.js)
#  * Shorts pacing: lead 0.15 s, gap 0.25 s between takes, tail 0.3 s
# Usage: source <(bash shorts/kit/setup.sh)   -> exports SS (skill copy) and SK (engine)
set -e
KIT="$(cd "$(dirname "$0")" && pwd)"
SRC=$(ls -d /mnt/skills/*/exportain-video-studio 2>/dev/null | head -1)
[ -n "$SRC" ] || SRC="$KIT/../../vendor/exportain-video-studio"
rm -rf /tmp/evs_sh; cp -r "$SRC" /tmp/evs_sh; SS=/tmp/evs_sh; SK=$SS/engine
python3 - "$SK" <<'PY'
import re,sys
sk=sys.argv[1]
p=f"{sk}/scripts/render.py"; s=open(p).read()
s=s.replace('args=["--force-color-profile=srgb", "--disable-gpu"]',
 'args=["--force-color-profile=srgb", "--use-gl=angle", "--use-angle=swiftshader", "--enable-unsafe-swiftshader", "--ignore-gpu-blocklist", "--allow-file-access-from-files"]')
s=s.replace('pg.goto("file://" + html)','pg.goto("file://" + html)\n    pg.wait_for_function("!window.R3_WANT || window.R3_READY===true", timeout=90000)')
assert "swiftshader" in s and "R3_WANT" in s; open(p,"w").write(s)
p=f"{sk}/scripts/topic_build.py"; s=open(p).read()
s=s.replace("LEAD, GAP, TAIL = 0.6, 0.7, 0.6","LEAD, GAP, TAIL = 0.15, 0.25, 0.3"); assert "0.15, 0.25" in s; open(p,"w").write(s)
PY
bash $SK/scripts/setup.sh >/dev/null 2>&1 || true
echo "export SS=$SS SK=$SK KIT=$KIT"
