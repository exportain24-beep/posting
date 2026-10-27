#!/usr/bin/env python3
"""Shorts thumbnail (search/channel pages): a 1080x1920 frame of the hook at second T, saved as JPEG <= 2 MB.
  python3 thumb.py <final.mp4> <seconds> <out.jpg>
The hook frame already carries the big headline; pick a moment where the headline and the 3D world are both on screen."""
import os, subprocess, sys
src, t, out = sys.argv[1], sys.argv[2], sys.argv[3]
for q in (2, 4, 6, 9):
    subprocess.check_call(["ffmpeg", "-y", "-loglevel", "error", "-ss", t, "-i", src, "-frames:v", "1",
                           "-vf", "scale=1080:1920", "-q:v", str(q), out])
    if os.path.getsize(out) <= 1_900_000:
        break
print(out, os.path.getsize(out), "bytes")
