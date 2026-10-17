#!/usr/bin/env python3
"""Make the 9:16 cover (used as YouTube + Facebook thumbnail) and put it at the start of the video
(so TikTok, which only takes a frame, shows the same cover).

  cover.py --headline "বিদেশি *বায়ার* কোথায়?" [--chip "রপ্তানি টিপস"] [--sub exportain.com]
           [--bg STILL.jpg] --out cover.jpg
  cover.py --prepend cover.jpg --video final_9x16.mp4 --out final.mp4 [--hold 0.5]

*word* = highlighted in gold. --bg = a frame from the video (blurred and darkened behind the text).
Fonts: the video skill's bundled fonts (SK env var, default /tmp/mv).
"""
import argparse, base64, html, os, re, subprocess, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
LOGO = os.path.join(os.path.dirname(HERE), "assets", "logo.png")
FONTS = os.path.join(os.environ.get("SK", "/tmp/mv"), "assets", "fonts")


def data_uri(p, mime):
    return f"data:{mime};base64," + base64.b64encode(open(p, "rb").read()).decode()


def make_cover(a):
    from playwright.sync_api import sync_playwright
    h = html.escape(a.headline)
    h = re.sub(r"\*(.+?)\*", r"<em>\1</em>", h)
    bg = (f"<img class='bgimg' src='{data_uri(a.bg, 'image/jpeg')}'>" if a.bg else "")
    page = f"""<!doctype html><html><head><meta charset=utf-8><style>
@font-face{{font-family:B;src:url(file://{FONTS}/NotoSansBengali-ExtraBold.ttf);font-weight:800}}
@font-face{{font-family:B;src:url(file://{FONTS}/NotoSansBengali-Bold.ttf);font-weight:700}}
@font-face{{font-family:P;src:url(file://{FONTS}/Poppins-ExtraBold.ttf);font-weight:800}}
*{{margin:0;padding:0;box-sizing:border-box}}
body{{width:1080px;height:1920px;overflow:hidden;font-family:B,P}}
#c{{position:relative;width:1080px;height:1920px;overflow:hidden;background:linear-gradient(160deg,#003C10,#005A1E 50%,#2E8B2E)}}
.bgimg{{position:absolute;inset:-40px;width:1160px;height:2000px;object-fit:cover;filter:blur(14px) brightness(.55) saturate(1.2)}}
.shade{{position:absolute;inset:0;background:linear-gradient(180deg,rgba(0,40,10,.55),rgba(0,40,10,.15) 40%,rgba(0,40,10,.75))}}
.ring{{position:absolute;border-radius:50%;border:46px solid rgba(92,191,20,.28)}}
#logo{{position:absolute;left:50%;top:190px;transform:translateX(-50%);background:#fff;border-radius:999px;padding:22px 54px;box-shadow:0 16px 50px rgba(0,0,0,.3)}}
#logo img{{height:100px;display:block}}
#chip{{position:absolute;left:90px;top:640px;background:#F2B705;color:#1b1400;font:800 56px B,P;padding:14px 40px;border-radius:999px}}
#h{{position:absolute;left:90px;right:90px;top:780px;color:#fff;font:800 132px/1.2 B,P;text-shadow:0 8px 30px rgba(0,0,0,.45)}}
#h em{{font-style:normal;color:#F2B705}}
#sub{{position:absolute;left:0;right:0;bottom:300px;text-align:center;color:#E8F7DD;font:800 64px P,B}}
</style></head><body><div id=c>{bg}<div class=shade></div>
<div class=ring style="width:700px;height:700px;right:-260px;top:-200px"></div>
<div class=ring style="width:520px;height:520px;left:-220px;bottom:-160px"></div>
<div id=logo><img src="{data_uri(LOGO, 'image/png')}"></div>
{f"<div id=chip>{html.escape(a.chip)}</div>" if a.chip else ""}
<div id=h>{h}</div><div id=sub>{html.escape(a.sub)}</div></div></body></html>"""
    tmp = tempfile.mkdtemp()
    p = os.path.join(tmp, "c.html"); open(p, "w", encoding="utf-8").write(page)
    with sync_playwright() as pw:
        b = pw.chromium.launch(); pg = b.new_page(viewport={"width": 1080, "height": 1920})
        pg.goto("file://" + p); pg.evaluate("document.fonts.ready"); pg.wait_for_timeout(300)
        pg.screenshot(path=a.out, type="jpeg", quality=88); b.close()
    # if the headline overflows, the text runs off the canvas; warn the caller
    print(f"cover -> {a.out} ({os.path.getsize(a.out)//1024} KB)")


def prepend(a):
    """cover still for --hold seconds, then the video. Audio is delayed by the same amount."""
    hold = a.hold
    total = hold + float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                                                   "-of", "default=nw=1:nk=1", a.video]).decode())
    subprocess.check_call([
        "ffmpeg", "-y", "-loglevel", "error", "-loop", "1", "-t", str(hold), "-framerate", "30", "-i", a.prepend,
        "-i", a.video, "-filter_complex",
        f"[0:v]scale=1080:1920,setsar=1,format=yuv420p[c];[1:v]scale=1080:1920,setsar=1,format=yuv420p[v];"
        f"[c][v]concat=n=2:v=1:a=0[vo];[1:a]adelay={int(hold*1000)}|{int(hold*1000)},apad=whole_dur={total:.3f}[ao]",
        "-map", "[vo]", "-map", "[ao]", "-t", f"{total:.3f}", "-c:v", "libx264", "-crf", "20", "-preset", "medium",
        "-r", "30", "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-movflags", "+faststart", a.out])
    print(f"video with cover first -> {a.out}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--headline"); ap.add_argument("--chip", default=""); ap.add_argument("--sub", default="exportain.com")
    ap.add_argument("--bg"); ap.add_argument("--out", required=True)
    ap.add_argument("--prepend"); ap.add_argument("--video"); ap.add_argument("--hold", type=float, default=0.5)
    a = ap.parse_args()
    prepend(a) if a.prepend else make_cover(a)
