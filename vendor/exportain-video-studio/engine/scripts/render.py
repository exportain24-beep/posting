#!/usr/bin/env python3
"""plan.json -> silent MP4. One timeline page, JPEG frames piped to ffmpeg,
frame range split over parallel Chromium workers, lossless concat.
  render.py --plan plan.json --out v.mp4 [--size 1080x1920] [--fps 30]
  render.py --plan plan.json --still 12.5 --out f.png"""
import argparse, json, os, subprocess, sys, tempfile
from playwright.sync_api import sync_playwright

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def page_html(work, template="timeline.html"):
    html = open(os.path.join(ROOT, "templates", template), encoding="utf-8").read()
    html = html.replace("__FONTDIR__", "file://" + os.path.join(ROOT, "assets", "fonts"))
    p = os.path.join(work, "timeline.html"); open(p, "w", encoding="utf-8").write(html); return p


def load_plan(path):
    plan = json.load(open(path, encoding="utf-8"))
    if plan.get("logo") and not plan["logo"].startswith(("file://", "data:", "http")):
        plan["logo"] = "file://" + os.path.abspath(plan["logo"])
    return plan


def open_page(p, html, plan, w, h):
    b = p.chromium.launch(args=["--force-color-profile=srgb", "--disable-gpu"])
    pg = b.new_page(viewport={"width": w, "height": h})
    pg.goto("file://" + html)
    pg.evaluate("Promise.all(['400','600','700','800'].map(w=>document.fonts.load(w+' 80px B','বাংলা')))")
    pg.evaluate("Promise.all([...['400','500','600','700','800'].map(w=>document.fonts.load(w+' 40px Inter','Aa')),...['500','600','700','800'].map(w=>document.fonts.load(w+' 40px Pop','Aa'))])")
    pg.evaluate("(p) => window.__init(p)", plan); pg.evaluate("document.fonts.ready")
    return b, pg


def worker(a):
    plan = load_plan(a.plan); w, h = map(int, a.size.split("x"))
    ff = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "image2pipe", "-framerate", str(a.fps),
                           "-c:v", "mjpeg", "-i", "-", "-c:v", "libx264", "-preset", "medium", "-crf", "18",
                           "-pix_fmt", "yuv420p", "-r", str(a.fps), a.out], stdin=subprocess.PIPE)
    with sync_playwright() as p:
        b, pg = open_page(p, a.html, plan, w, h)
        for f in range(a.f0, a.f1):
            pg.evaluate("(t) => window.__render(t)", f / a.fps)
            ff.stdin.write(pg.screenshot(type="jpeg", quality=93))
        b.close()
    ff.stdin.close(); sys.exit(ff.wait())


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--plan", required=True); ap.add_argument("--out", required=True)
    ap.add_argument("--size", default="1080x1920"); ap.add_argument("--fps", type=int, default=30)
    ap.add_argument("--workers", type=int, default=max(1, os.cpu_count() or 1))
    ap.add_argument("--still", type=float)
    ap.add_argument("--_worker", action="store_true"); ap.add_argument("--html")
    ap.add_argument("--f0", type=int); ap.add_argument("--f1", type=int)
    a = ap.parse_args()
    if a._worker: return worker(a)
    plan = load_plan(a.plan)
    work = tempfile.mkdtemp(prefix="render_"); html = page_html(work, plan.get("template", "timeline.html")); w, h = map(int, a.size.split("x"))
    if a.still is not None:
        with sync_playwright() as p:
            b, pg = open_page(p, html, plan, w, h)
            pg.evaluate("(t) => window.__render(t)", a.still); pg.screenshot(path=a.out); b.close()
        print("still ->", a.out); return
    n = round(plan["total"] * a.fps); k = max(1, min(a.workers, n // 30 or 1))
    cuts = [round(i * n / k) for i in range(k + 1)]; segs, procs = [], []
    for i in range(k):
        seg = os.path.join(work, f"seg{i:02d}.mp4"); segs.append(seg)
        procs.append(subprocess.Popen([sys.executable, __file__, "--_worker", "--plan", a.plan, "--out", seg,
                                       "--size", a.size, "--fps", str(a.fps), "--html", html,
                                       "--f0", str(cuts[i]), "--f1", str(cuts[i + 1])]))
    if any(pr.wait() for pr in procs): sys.exit("a render worker failed")
    lst = os.path.join(work, "list.txt"); open(lst, "w").write("".join(f"file '{s}'\n" for s in segs))
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", lst,
                    "-c", "copy", a.out], check=True)
    print(f"{n} frames @ {a.fps}fps, {k} workers -> {a.out}")


if __name__ == "__main__":
    main()
