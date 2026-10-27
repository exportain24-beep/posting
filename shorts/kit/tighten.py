#!/usr/bin/env python3
"""Shorts pacing: trims each voice take's lead/tail silence and shortens long internal pauses (jump-cut style),
then rewrites durations.json. Keeps the original takes in vo_raw/ (never re-voice to fix pacing).
  python3 tighten.py <project_dir> [--pause 0.16] [--thresh -32] [--tempo 1.08]
--tempo speeds speech up without changing pitch (ffmpeg atempo); keep it 1.0-1.12 so the voice stays natural.
"""
import json, os, re, shutil, subprocess, sys

P = sys.argv[1]
PAUSE = float(sys.argv[sys.argv.index("--pause") + 1]) if "--pause" in sys.argv else 0.16
TH = sys.argv[sys.argv.index("--thresh") + 1] if "--thresh" in sys.argv else "-32"
TEMPO = min(1.12, max(1.0, float(sys.argv[sys.argv.index("--tempo") + 1]) if "--tempo" in sys.argv else 1.0))
vo, raw = os.path.join(P, "vo"), os.path.join(P, "vo_raw")
if not os.path.isdir(raw):
    shutil.copytree(vo, raw)


def dur(f):
    return float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                                          "-of", "default=nw=1:nk=1", f]).decode())


def silences(f):
    out = subprocess.run(["ffmpeg", "-i", f, "-af", f"silencedetect=noise={TH}dB:d=0.12", "-f", "null", "-"],
                         capture_output=True, text=True).stderr
    st = [float(x) for x in re.findall(r"silence_start: ([0-9.]+)", out)]
    en = [float(x) for x in re.findall(r"silence_end: ([0-9.]+)", out)]
    return list(zip(st, en + [None] * (len(st) - len(en))))


durs, before = {}, 0.0
for name in sorted(os.listdir(raw)):
    if not name.endswith(".mp3"):
        continue
    src, d = os.path.join(raw, name), None
    d = dur(src); before += d
    keep, cur = [], 0.0
    sil = silences(src)
    lead = sil[0][1] if sil and sil[0][0] <= 0.02 and sil[0][1] else 0.0
    cur = max(0.0, lead - 0.04)
    for s, e in sil:
        if s <= 0.02:
            continue
        if e is None:                     # trailing silence
            keep.append((cur, min(d, s + 0.06))); cur = None; break
        keep.append((cur, s + PAUSE / 2)); cur = max(s + PAUSE / 2, e - PAUSE / 2)
    if cur is not None:
        keep.append((cur, d))
    parts = "".join(f"[0:a]atrim={a:.3f}:{b:.3f},asetpts=PTS-STARTPTS[p{i}];" for i, (a, b) in enumerate(keep))
    fc = parts + "".join(f"[p{i}]" for i in range(len(keep))) + f"concat=n={len(keep)}:v=0:a=1,atempo={TEMPO:.3f}[o]"
    out = os.path.join(vo, name)
    subprocess.check_call(["ffmpeg", "-y", "-loglevel", "error", "-i", src, "-filter_complex", fc, "-map", "[o]",
                           "-c:a", "libmp3lame", "-b:a", "192k", out])
    durs[name[:-4]] = round(dur(out), 3)
json.dump(durs, open(os.path.join(P, "durations.json"), "w"), indent=1)
print(f"tightened: {before:.1f}s -> {sum(durs.values()):.1f}s of speech", json.dumps(durs))
