#!/usr/bin/env python3
"""Prepend the designed thumbnail as the first frames of the Short (YouTube Shorts first frame + TikTok cover).
  python3 cover.py <final.mp4> <thumb.jpg> <out.mp4> [--hold 0.4]
Keeps the total <= 30.0 s: the hold shrinks to fit (min 0.25 s); if even that does not fit, the video is copied
unchanged and the script prints "cover: skipped" (then set tiktok.cover_ms to a hook frame instead).
Prints the TikTok cover_ms to use (middle of the cover hold)."""
import shutil, subprocess, sys

src, img, out = sys.argv[1], sys.argv[2], sys.argv[3]
hold = float(sys.argv[sys.argv.index("--hold") + 1]) if "--hold" in sys.argv else 0.4
dur = float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of",
                                     "default=nw=1:nk=1", src]).decode())
hold = min(hold, round(29.95 - dur, 2))
if hold < 0.25:
    shutil.copy(src, out); print(f"cover: skipped (video {dur:.2f}s leaves no room)"); sys.exit(0)
ms = int(hold * 1000)
subprocess.check_call([
    "ffmpeg", "-y", "-loglevel", "error", "-loop", "1", "-t", f"{hold}", "-framerate", "30", "-i", img, "-i", src,
    "-filter_complex",
    "[0:v]scale=1080:1920,setsar=1,format=yuv420p[c];[1:v]scale=1080:1920,setsar=1,format=yuv420p,fps=30[v];"
    f"[c][v]concat=n=2:v=1:a=0[vo];[1:a]adelay={ms}|{ms}[ao]",
    "-map", "[vo]", "-map", "[ao]", "-c:v", "libx264", "-crf", "19", "-preset", "medium", "-r", "30",
    "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-movflags", "+faststart", out])
d2 = float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of",
                                    "default=nw=1:nk=1", out]).decode())
print(f"cover: {hold:.2f}s prepended, video {d2:.2f}s, tiktok cover_ms {int(hold * 500)}")
