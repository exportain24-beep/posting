#!/usr/bin/env bash
# Rebuild one of the bundled examples (to study it or reuse its scenes).
# Usage: bash from_example.sh <example_name> <project_dir>     e.g. from_example.sh prod /tmp/prod
# You still need a voice MP3 for that narration to render (split_check.py <dir> <mp3>).
set -e
S="$(cd "$(dirname "$0")/.." && pwd)"; E="$S/examples/$1"; P="$2"
[ -d "$E" ] || { echo "no example $1; have: $(ls $S/examples)"; exit 1; }
ENG="$S/engine"; touch "$ENG/.w" 2>/dev/null && rm -f "$ENG/.w" || { mkdir -p /tmp/ev_engine; cp -r "$ENG/." /tmp/ev_engine/; ENG=/tmp/ev_engine; }
if grep -q "1920 1080" "$E/build.sh" 2>/dev/null; then ST=starter16; else ST=starter916; fi
mkdir -p "$P"; cp -r "$S/$ST/." "$P/"
[ -f "$E/js/1_lib.js" ] && rm -rf "$P/js"   # example ships its own full library
cp -r "$E/." "$P/"; sed -i "s#__ENGINE__#$ENG#" "$P/build.sh"
PF=$(python3 -c "import json;print(json.load(open('$P/board.json'))[0]['kind'].split('_')[0])")
sed -i "s/startsWith('[A-Za-z]*_')/startsWith('${PF}_')/" "$P/js/99_amb.js"
for f in "$P/js/3_9end.js" "$P/js/9_end.js" "$P/build.sh"; do [ -f "$f" ] && sed -i "s/PFX_/${PF}_/g" "$f"; done
echo "example $1 copied to $P (starter $ST, prefix ${PF}_). Add full.mp3, run split_check.py, then bash build.sh"
