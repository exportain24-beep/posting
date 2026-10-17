#!/usr/bin/env python3
"""Turn the skill's illustrated (text-free, drawn) scenes page into a 16:9 1920x1080 page.

The bangla-motion-video skill's illustrated engine draws on a 1080x1920 canvas. Run this after
`topic_build.py --project P` (illustrated mode, scenes.js drawn at 1920x1080), then render at --size 1920x1080:

  python3 tools/illustrated16.py P/scenes.html

Custom scenes in scenes.js must use the 1920x1080 canvas: start with
  <rect width="1920" height="1080" fill="url(#studio)"/>
and keep key art between x≈120..1800, y≈120..980. Built-in portrait kinds are not used in 16:9 videos.
"""
import sys

p = sys.argv[1]
s = open(p, encoding="utf-8").read()
rep = [
    ('viewBox="0 0 1080 1920" preserveAspectRatio="xMidYMid slice"', 'viewBox="0 0 1920 1080" preserveAspectRatio="xMidYMid slice"'),
    ("o.q('cam').style.transformOrigin='540px 960px'", "o.q('cam').style.transformOrigin='960px 540px'"),
    ("#badge{position:absolute;left:5.5%;top:3.6%;height:4.2%;padding:.6% 2.2%;",
     "#badge{position:absolute;left:3%;top:4.5%;height:7.2%;padding:1% 1.6%;"),
    ("#intro img,#end img{width:74%}", "#intro img,#end img{width:46%}"),
    (".lw{position:relative;width:74%;display:flex}", ".lw{position:relative;width:46%;display:flex}"),
]
for a, b in rep:
    if a not in s:
        sys.exit(f"illustrated16: pattern not found (skill template changed?): {a[:60]}")
    s = s.replace(a, b)
open(p, "w", encoding="utf-8").write(s)
print("16:9 scenes page ->", p)
