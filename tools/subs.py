#!/usr/bin/env python3
"""Burned-in Bangla subtitles for the 9:16 reel (owner's standing order, 31 Oct 2026: subtitles are mandatory).

  subs.py <PROJECT_DIR> --video <in.mp4> --out <out.mp4> [--y 1490] [--size 54] [--chars 26]

Reads PROJECT_DIR/plan.json (scene start + voice length per scene) and narration.json, splits every scene's
narration into short cues (max 2 lines of ~26 Bangla characters, broken at punctuation / spaces), times each cue by
its share of the scene's spoken characters, writes PROJECT_DIR/subs.srt (also the captions file for the platforms)
and PROJECT_DIR/subs.ass, and burns the ASS into the video with libass (HarfBuzz shaping, Noto Sans Bengali).
Subtitles sit in the band y ≈ 1400–1600 of the 1080×1920 frame (above the TikTok / Reels / Shorts bottom UI):
keep important scene content out of that band.
Times are relative to the rendered video (no cover frame) — run this BEFORE cover.py --prepend.
"""
import argparse, json, os, re, subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
FONTS = os.path.join(os.environ.get("SK", "/tmp/evs/engine"), "assets", "fonts")
if not os.path.isdir(FONTS):
    FONTS = os.path.join(os.path.dirname(HERE), "vendor", "exportain-video-studio", "engine", "assets", "fonts")
TAG = re.compile(r"\[[^\]]*\]")


def ts_srt(t):
    ms = int(round(t * 1000)); h, ms = divmod(ms, 3600000); m, ms = divmod(ms, 60000); s, ms = divmod(ms, 1000)
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


def ts_ass(t):
    cs = int(round(t * 100)); h, cs = divmod(cs, 360000); m, cs = divmod(cs, 6000); s, cs = divmod(cs, 100)
    return f"{h}:{m:02d}:{s:02d}.{cs:02d}"


def two_lines(text, width):
    """one line when it fits, else two lines split at the space nearest the middle"""
    if len(text) <= width + 4 or " " not in text:
        return [text]
    mid, best = len(text) / 2, None
    for i, ch in enumerate(text):
        if ch == " " and (best is None or abs(i - mid) < abs(best - mid)):
            best = i
    return [text[:best], text[best + 1:]]


def split_long(text, cap):
    """a phrase longer than one cue -> n cues of similar size, broken at spaces"""
    words, n = text.split(), -(-len(text) // cap)
    target, out, cur = len(text) / n, [], ""
    for w in words:
        if cur and len(cur) + 1 + len(w) > target + 6 and len(out) < n - 1:
            out.append(cur); cur = w
        else:
            cur = f"{cur} {w}".strip()
    return out + ([cur] if cur else [])


def chunks(text, width):
    """cues of at most 2 lines (~2*width chars); break after । ? ! , : ; when possible, never orphan a word"""
    text = TAG.sub("", text).strip()
    phrases = [p.strip() for p in re.split(r"(?<=[।?!,:;])\s+", text) if p.strip()]
    cap, cues, cur = 2 * width, [], ""
    for ph in phrases:
        if len(ph) > cap:
            if cur:
                cues.append(cur); cur = ""
            cues += split_long(ph, cap)
        elif cur and len(cur) + 1 + len(ph) > cap:
            if len(cur) < width * .6:              # a short lead-in phrase would flash by: join it to the next one
                cues += split_long(f"{cur} {ph}", cap); cur = ""
            else:
                cues.append(cur); cur = ph
        else:
            cur = f"{cur} {ph}".strip()
    if cur:
        cues.append(cur)
    return [two_lines(c, width) for c in cues]


def build(pdir, width):
    plan = json.load(open(os.path.join(pdir, "plan.json"), encoding="utf-8"))
    nar = {n["id"]: n["text"] for n in json.load(open(os.path.join(pdir, "narration.json"), encoding="utf-8"))}
    dur = {}
    p = os.path.join(pdir, "durations.json")
    if os.path.isfile(p):
        dur = json.load(open(p, encoding="utf-8"))
    out = []
    for sc in plan["scenes"]:
        sid = sc.get("id")
        if sid not in nar:
            continue
        start = sc["start"]; speak = dur.get(sid) or (sc["end"] - sc["start"])
        cs = chunks(nar[sid], width)
        tot = sum(len("".join(c)) for c in cs) or 1
        t = start
        for c in cs:
            d = speak * len("".join(c)) / tot
            out.append((t, min(t + d + .12, start + speak + .25), c))
            t += d
    # no overlaps
    for i in range(len(out) - 1):
        a, b, c = out[i]
        out[i] = (a, min(b, out[i + 1][0] - .02), c)
    return out


def write(pdir, cues, y, size):
    srt = "\n".join(f"{i}\n{ts_srt(a)} --> {ts_srt(b)}\n" + "\n".join(c) + "\n" for i, (a, b, c) in enumerate(cues, 1))
    open(os.path.join(pdir, "subs.srt"), "w", encoding="utf-8").write(srt)
    head = f"""[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920
WrapStyle: 2
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: S,Noto Sans Bengali,{size},&H00FFFFFF,&H00FFFFFF,&H00142A00,&H64000000,-1,0,0,0,100,100,0,0,1,6,3,5,60,60,0,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    ev = []
    for a, b, c in cues:
        txt = r"\N".join(x.replace("{", "(").replace("}", ")") for x in c)
        ev.append(f"Dialogue: 0,{ts_ass(a)},{ts_ass(b)},S,,0,0,0,,{{\\pos(540,{y})\\fad(80,60)}}{txt}")
    open(os.path.join(pdir, "subs.ass"), "w", encoding="utf-8").write(head + "\n".join(ev) + "\n")


def burn(pdir, src, dst):
    ass = os.path.join(pdir, "subs.ass").replace(":", r"\:")
    subprocess.check_call(["ffmpeg", "-y", "-loglevel", "error", "-i", src, "-vf",
                           f"ass='{ass}':fontsdir='{FONTS}':shaping=complex", "-c:v", "libx264", "-crf", "20", "-preset", "medium",
                           "-pix_fmt", "yuv420p", "-c:a", "copy", "-movflags", "+faststart", dst])


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("dir"); ap.add_argument("--video"); ap.add_argument("--out")
    ap.add_argument("--y", type=int, default=1490); ap.add_argument("--size", type=int, default=62)
    ap.add_argument("--chars", type=int, default=26)
    a = ap.parse_args()
    cues = build(a.dir, a.chars)
    write(a.dir, cues, a.y, a.size)
    print(f"{len(cues)} cues -> {a.dir}/subs.srt, subs.ass")
    if a.video and a.out:
        burn(a.dir, a.video, a.out)
        print(f"burned -> {a.out}")
