#!/usr/bin/env bash
# Contact sheets of every scene's last frame (scene end - 0.25 s), 9 per sheet -> qa_a.jpg, qa_b.jpg ...
# Usage: bash qa.sh <project_dir> [scene_index ...]   (indices = only those scenes, e.g. after a fix)
set -e; P="$1"; shift || true; SK=${SK:-$(cd "$(dirname "$0")/../engine" && pwd)}
cd "$P"
SIZE=$(grep -q "1920 1080" build.sh && echo 1920x1080 || echo 1080x1920)
COLS=$([ "$SIZE" = 1920x1080 ] && echo 3 || echo 4)
T=$(python3 - "$@" <<'PY'
import json,sys
s=json.load(open('plan.json'))['scenes']; idx=[int(a) for a in sys.argv[1:]] or range(len(s))
print(' '.join('%.2f'%(s[i]['end']-.25) for i in idx))
PY
)
set -- $T; n=0; for L in a b c d e f; do [ $# -eq 0 ] && break; chunk=""; for k in 1 2 3 4 5 6 7 8 9; do [ $# -eq 0 ] && break; chunk="$chunk $1"; shift; done
  python3 $SK/scripts/qa_stills.py --plan plan.json --size $SIZE --cols $COLS --out qa_$L.jpg $chunk >/dev/null 2>&1; echo "qa_$L.jpg:$chunk"; done
