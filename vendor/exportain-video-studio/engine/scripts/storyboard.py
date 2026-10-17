#!/usr/bin/env python3
"""Attach an illustrated storyboard to plan.json (text-free mode).
board.json = [{"kind", "keys":[spoken words], "sfx":[sound per beat], "bg": gradient id}, ...] one per scene.
Each key is located in the sentence (searching forward) -> char-share time, then snapped to the
nearest pause end in the voiceover (= the moment that word starts) when one is within 0.6 s."""
import argparse, json, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from plan import silences


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--plan", required=True); ap.add_argument("--board", required=True)
    ap.add_argument("--voice"); ap.add_argument("--out", required=True)
    ap.add_argument("--keep-intro", action="store_true", help="keep the 1 s logo sting before scene 1")
    a = ap.parse_args()
    plan = json.load(open(a.plan, encoding="utf-8")); board = json.load(open(a.board, encoding="utf-8"))
    assert len(board) == len(plan["scenes"]), f"board {len(board)} vs plan {len(plan['scenes'])} scenes"
    plan["template"] = "illustrated.html"
    if not a.keep_intro: plan["intro"] = False
    ends = [e for _, e in silences(a.voice, -32, 0.12)] if a.voice else []
    intro = plan.get("intro", True)
    for i, (sc, bd) in enumerate(zip(plan["scenes"], board)):
        text = sc["text"]; st = max(sc["start"], 1.0) if (i == 0 and intro) else sc["start"]; span = sc["end"] - st
        n = len(text.replace(" ", "")) or 1
        beats, pos = [], 0
        for j, k in enumerate(bd.get("keys", [])):
            f = text.find(k, pos)
            frac = (j + 1) / (len(bd["keys"]) + 1) if f < 0 else len(text[:f].replace(" ", "")) / n
            if f >= 0: pos = f + len(k)
            t = st + 0.04 * span + 0.9 * span * frac
            near = [e for e in ends if st <= e < sc["end"] and abs(e - t) < 0.6]
            if near: t = min(near, key=lambda e: abs(e - t))
            if beats: t = max(t, beats[-1] + 0.25)
            beats.append(round(t, 3))
        sc["kind"], sc["beats"] = bd["kind"], beats
        for key in ("sfx", "bg"):
            if key in bd: sc[key] = bd[key]
        print(f"{i:02d} {bd['kind']:15} " + " ".join(f"{b:.2f}" for b in beats))
    json.dump(plan, open(a.out, "w", encoding="utf-8"), ensure_ascii=False, indent=2)


if __name__ == "__main__":
    main()
