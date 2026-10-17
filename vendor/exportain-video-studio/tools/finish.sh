#!/usr/bin/env bash
# Usage: bash finish.sh <project_dir> <out_dir> <ShareName>
# limiter -> loudness/true-peak check -> review (frozen stretches) -> share MP4 + SRT
set -e; P="$1"; O="$2"; N="$3"; SK=${SK:-$(cd "$(dirname "$0")/../engine" && pwd)}
cd "$O"
lim(){ ffmpeg -v error -y -i final_9x16.mp4 -map 0:a -af "volume=-0.5dB,alimiter=limit=$1:level=false" -c:a aac -b:a 192k a2.m4a
       ffmpeg -v error -y -i final_9x16.mp4 -i a2.m4a -map 0:v -map 1:a -c copy fin.mp4 && mv fin.mp4 final_9x16.mp4; }
lim 0.82
PK=$(ffmpeg -i final_9x16.mp4 -af ebur128=peak=true -f null - 2>&1 | grep -A20 Summary | grep "Peak:" | awk '{print $2}')
python3 -c "import sys;sys.exit(0 if float('$PK')<=-1.05 else 1)" || { echo "peak $PK -> second pass"; lim 0.79; }
ffmpeg -i final_9x16.mp4 -af ebur128=peak=true -f null - 2>&1 | grep -A20 Summary | grep -E "I:|Peak:"
python3 $SK/scripts/review.py --video final_9x16.mp4 --plan "$P/plan.json" --every 2.5 --out review | grep -A3 frozen
ffmpeg -v error -y -i final_9x16.mp4 -c:v libx264 -crf 28 -tune animation -preset slow -pix_fmt yuv420p -c:a copy -movflags +faststart "$N.mp4"
cp captions.srt "$N.srt"; ls -la "$N".*
