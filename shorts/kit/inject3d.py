#!/usr/bin/env python3
"""Runs at the end of build.sh: copies board.json "gl" options into plan.json scenes and, if any scene uses gl,
adds the three.js layer (r3d.js) to scenes.html. Scenes with gl draw their SVG with a transparent background."""
import json, os, sys
P, KIT = sys.argv[1], sys.argv[2]
board = json.load(open(os.path.join(P, "board.json"), encoding="utf-8"))
plan = json.load(open(os.path.join(P, "plan.json"), encoding="utf-8"))
used = False
for sc, b in zip(plan["scenes"], board):
    if b.get("gl"):
        sc["gl"] = b["gl"]; used = True
    else:
        sc.pop("gl", None)
    if b.get("badge") == "white":
        sc["badge"] = "white"; used = True
json.dump(plan, open(os.path.join(P, "plan.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
h = os.path.join(P, "scenes.html"); s = open(h, encoding="utf-8").read()
if used and "data-r3" not in s:
    inj = (f'<script>window.R3_WANT=true;</script><script type="module" data-r3>import * as R from "file://{KIT}/r3d.js";'
           'window.R3=R;window.R3_READY=true;</script>\n'
           '<script>(function(){const i=window.__init,r=window.__render;window.__init=function(p){window.__plan=p;return i.apply(this,arguments)};'
           'window.__render=function(t){const o=r.apply(this,arguments);if(window.R3){if(!window.__r3p&&window.__plan){R3.setPlan(window.__plan);window.__r3p=1}R3.frame(t)}return o}})();</script>')
    s = s.replace("</body>", inj + "</body>") if "</body>" in s else s + inj
    open(h, "w", encoding="utf-8").write(s)
print("3D layer:", "on (" + ", ".join(f"{x['id']}={x['gl']['world']}" for x in plan["scenes"] if x.get("gl")) + ")" if used else "off")
