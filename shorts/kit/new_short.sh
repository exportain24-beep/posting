#!/usr/bin/env bash
# New 9:16 Short project from the skill's 9:16 starter + the Shorts kit (short CTA scenes, 3D layer, Shorts build).
# Usage: bash new_short.sh <project_dir> <2-letter prefix> <bn|en>
set -e
P="$1"; X="$2"; LG="$3"; KIT="$(cd "$(dirname "$0")" && pwd)"
[ -n "$SS" ] || { echo "run: source <(bash $KIT/setup.sh) first"; exit 1; }
[ -n "$P" ] && [ -n "$X" ] && [ -n "$LG" ] || { echo "usage: new_short.sh dir prefix bn|en"; exit 1; }
mkdir -p "$P"
cp -rn "$SS/starter916/." "$P/"                    # keeps narration.json / vo / durations.json if already there
sed -i "s#__ENGINE__#$SK#" "$P/build.sh"
rm -f "$P/js/9_end.js"
sed "s/PFX_/${X}_/g; s#__KIT__#$KIT#g" "$KIT/js/9_short_end.js" > "$P/js/9_end.js"
sed -i "s/PFX_/${X}_/g" "$P/js/99_amb.js"
sed -i "s/--endcard 2.5/--endcard 1.2/" "$P/build.sh"
grep -q inject3d "$P/build.sh" || cat >> "$P/build.sh" <<EOS
# ---- Shorts kit: realistic 3D layer + gl options from board.json into plan.json
python3 "$KIT/inject3d.py" "\$(pwd)" "$KIT"
EOS
echo "$LG" > "$P/.lang"
echo "short ready: $P  prefix ${X}_  lang $LG   (CTA scene: ${X}_cta_$LG)"
