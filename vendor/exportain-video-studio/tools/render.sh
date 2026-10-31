#!/usr/bin/env bash
# Music + render + finish in one go. RUN IN THE BACKGROUND (takes ~15-30 min for 3-5 min of video).
# Usage: bash render.sh <project_dir> <ShareName> [mood=warm] [drop=2.2] [music_db=-24]
#   ads: mood=upbeat, drop=<reveal time>, music_db=-21
set -e; P="$(cd "$1" && pwd)"; N="$2"; MOOD="${3:-warm}"; DROP="${4:-2.2}"; MDB="${5:--24}"
T="$(cd "$(dirname "$0")" && pwd)"; SK=${SK:-$(cd "$T/../engine" && pwd)}; export SK
cd "$P"; FMT=$(grep -q "1920 1080" build.sh && echo 16:9 || echo 9:16); TAG=${FMT/:/x}
D=$(python3 -c "import json;p=json.load(open('plan.json'));print(round(p['scenes'][-1]['end']+2.8,1))")
[ -f music.wav ] || python3 $SK/scripts/music_bed.py --duration $D --mood $MOOD --drop $DROP --out music.wav >/dev/null 2>&1
rm -rf out; python3 $SK/scripts/make_video.py --voice vo.mp3 --plan plan.json --music music.wav --music-db $MDB --sfx-db -7 --formats $FMT --outdir out > render.log 2>&1
cd out; [ -f final_$TAG.mp4 ] && [ "$TAG" != 9x16 ] && mv final_$TAG.mp4 final_9x16.mp4
bash "$T/finish.sh" "$P" "$P/out" "$N" > "$P/finish.log" 2>&1
grep -E "I:|Peak:|frozen" "$P/finish.log"; python3 "$T/frozen_map.py" "$P"; ls -la "$P/out/$N".*
