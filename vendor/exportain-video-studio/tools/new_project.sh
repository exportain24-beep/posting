#!/usr/bin/env bash
# Create a new video project.
# Usage: bash new_project.sh <project_dir> <prefix> "L1|L2|L3|L4|L5" [--916]
#   prefix : 2 lowercase letters, scenes become K.<prefix>_hook ... K.<prefix>_cta
#   labels : 5 short road-map labels (<= ~10 Bangla chars each), one per point, in order
#   --916  : use the vertical 9:16 reel starter instead of the default 16:9 starter
set -e
S="$(cd "$(dirname "$0")/.." && pwd)"; P="$1"; X="$2"; LBL="$3"; FMT="${4:-}"
[ -z "$P" ] || [ -z "$X" ] && { echo "usage: new_project.sh dir prefix 'l1|l2|l3|l4|l5' [--916]"; exit 1; }
ENG="$S/engine"; touch "$ENG/.w" 2>/dev/null && rm -f "$ENG/.w" || { mkdir -p /tmp/ev_engine; cp -r "$ENG/." /tmp/ev_engine/; ENG=/tmp/ev_engine; }
mkdir -p "$P"
if [ "$FMT" = "--916" ]; then
  cp -r "$S/starter916/." "$P/"; sed -i "s#__ENGINE__#$ENG#" "$P/build.sh"
  sed -i "s/PFX_/${X}_/g" "$P/js/99_amb.js" "$P/js/9_end.js" "$P/build.sh"
  [ -n "$LBL" ] && python3 - "$P/js/2_helpers.js" "$LBL" <<'PY'
import re,sys
p,l=sys.argv[1],sys.argv[2].split('|');assert len(l)==5,'need 5 labels'
s=open(p,encoding='utf-8').read()
s=re.sub(r"const R5L=\[.*?\]","const R5L=["+",".join("'%s'"%x.strip() for x in l)+"]",s,count=1)
open(p,'w',encoding='utf-8').write(s)
PY
else
  cp -r "$S/starter16/." "$P/"; sed -i "s#__ENGINE__#$ENG#" "$P/build.sh"
  sed -i "s/PFX_/${X}_/g" "$P/js/99_amb.js" "$P/js/3_9end.js" "$P/build.sh"
  [ -n "$LBL" ] && python3 - "$P/js/3_0helpers.js" "$LBL" <<'PY'
import re,sys
p,l=sys.argv[1],sys.argv[2].split('|');assert len(l)==5,'need 5 labels'
s=open(p,encoding='utf-8').read()
s=re.sub(r"A:\[.*?\]","A:["+",".join("'%s'"%x.strip() for x in l)+"]",s,count=1)
open(p,'w',encoding='utf-8').write(s)
PY
fi
echo "project ready: $P   engine: $ENG   prefix: ${X}_   format: ${FMT:-16:9}"
echo "next: narration.json (+ split_check), board.json, js/3_a.js, js/4_b.js, bash build.sh"
