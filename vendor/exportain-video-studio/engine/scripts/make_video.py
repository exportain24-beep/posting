#!/usr/bin/env python3
"""One command: plan -> mix -> parallel render per format -> mux -> SRT -> QA sheet."""
import argparse, json, os, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
SIZES = {"9:16": "1080x1920", "16:9": "1920x1080", "1:1": "1080x1080", "4:5": "1080x1350"}


def run(*c): subprocess.run([str(x) for x in c], check=True)


def srt(plan, path):
    f = lambda s: "%02d:%02d:%02d,%03d" % (s // 3600, s % 3600 // 60, s % 60, round(s % 1 * 1000) % 1000)
    with open(path, "w", encoding="utf-8") as o:
        for i, sc in enumerate(plan["scenes"], 1):
            o.write(f"{i}\n{f(sc['start'])} --> {f(sc['end'])}\n{sc['text']}\n\n")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--voice", required=True)
    for f in ["--script", "--plan", "--music", "--words"]: ap.add_argument(f)
    for f in ["--logo", "--brand", "--url", "--tagline"]: ap.add_argument(f, default="")
    ap.add_argument("--formats", default="9:16"); ap.add_argument("--fps", type=int, default=30)
    ap.add_argument("--endcard", type=float, default=3.0); ap.add_argument("--music-db", type=float, default=-18)
    ap.add_argument("--outdir", default="out")
    ap.add_argument("--no-sfx", action="store_true"); ap.add_argument("--sfx-db", type=float, default=-4)
    a = ap.parse_args(); os.makedirs(a.outdir, exist_ok=True); py = sys.executable
    plan_path = a.plan or os.path.join(a.outdir, "plan.json")
    if not a.plan:
        if not a.script: sys.exit("--script (or --plan) is required")
        c = [py, f"{HERE}/plan.py", "--script", a.script, "--voice", a.voice, "--out", plan_path, "--brand", a.brand,
             "--url", a.url, "--logo", a.logo, "--endcard", a.endcard, "--tagline", a.tagline]
        if a.words: c += ["--words", a.words]
        run(*c)
    plan = json.load(open(plan_path, encoding="utf-8"))
    mix = os.path.join(a.outdir, "mix.m4a")
    c = [py, f"{HERE}/mix_audio.py", "--voice", a.voice, "--total", plan["total"], "--out", mix, "--music-db", a.music_db]
    if a.music: c += ["--music", a.music]
    if not a.no_sfx:
        fx = os.path.join(a.outdir, "sfx.wav"); run(py, f"{HERE}/sfx.py", "--plan", plan_path, "--out", fx)
        c += ["--sfx", fx, "--sfx-db", a.sfx_db]
    run(*c); srt(plan, os.path.join(a.outdir, "captions.srt"))
    for fmt in [x.strip() for x in a.formats.split(",")]:
        tag = fmt.replace(":", "x")
        silent, final = os.path.join(a.outdir, f"_silent_{tag}.mp4"), os.path.join(a.outdir, f"final_{tag}.mp4")
        run(py, f"{HERE}/render.py", "--plan", plan_path, "--out", silent, "--size", SIZES[fmt], "--fps", a.fps)
        run("ffmpeg", "-y", "-loglevel", "error", "-i", silent, "-i", mix, "-map", "0:v", "-map", "1:a",
            "-c", "copy", "-shortest", "-movflags", "+faststart", final)
        os.remove(silent)
        run("ffmpeg", "-y", "-loglevel", "error", "-i", final, "-c:v", "libx264", "-preset", "slow", "-crf", "23",
            "-pix_fmt", "yuv420p", "-c:a", "copy", "-movflags", "+faststart", os.path.join(a.outdir, f"share_{tag}.mp4"))
        times = [(s["start"] + s["end"]) / 2 for s in plan["scenes"]] + [plan["total"] - 0.5]
        sel = "+".join(f"eq(n\\,{round(t * a.fps)})" for t in times)
        cols = 6 if fmt == "9:16" else 4
        run("ffmpeg", "-y", "-loglevel", "error", "-i", final, "-vf",
            f"select='{sel}',scale=360:-1,tile={cols}x{-(-len(times) // cols)}:padding=6",
            "-frames:v", "1", "-vsync", "vfr", os.path.join(a.outdir, f"qa_{tag}.jpg"))
        print("done:", final)


if __name__ == "__main__":
    main()
