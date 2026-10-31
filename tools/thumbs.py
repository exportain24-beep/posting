#!/usr/bin/env python3
"""Colourful per-platform thumbnails + the 9:16 frame for the vertical video.

  thumbs.py <EP> <DIR> --video <16:9 video without cover> [--spec DIR/thumbs.json]

Writes into DIR:
  thumb.jpg     1280x720   YouTube (Bangla)
  thumb_li.jpg  1280x720   LinkedIn (English, first frame of the LinkedIn copy)
  thumb_fb.jpg  1080x1920  Facebook + Instagram cover (Bangla)
  thumb_tt.jpg  1080x1920  TikTok cover (Bangla, first frame of the TikTok copy)
  vframe.jpg    1080x1920  background of the vertical video (16:9 video sits in the middle)
When --video is 9:16 (the reel format since 31 Oct 2026) it also writes:
  thumb_yt9.jpg 1080x1920  YouTube Shorts cover = first frames of final.mp4 (cover.py --prepend), yt headline
  thumb_li9.jpg 1080x1920  LinkedIn cover (English, li headline) = first frames of the LinkedIn copy
and picture frames / stickers are taken from the vertical video (sticker "crop" in 1080x1920 coordinates).

thumbs.json (all keys optional except headlines; "|" = line break, *word* = highlighted, kept on one line):
{"yt": {"headline": "টুপির আয়|সাইকেলের *৩ গুণ!*", "chip": "বিস্ময়কর রপ্তানি পণ্য", "badge": "$447M", "t": 66.5},
 "li": {"headline": "Caps out-earned|bicycles *3×*", "sub": "Bangladesh's surprising export products", "chip": "Export insight", "t": 10.8},
 "fb": {"headline": "টুপির আয়|সাইকেলের|*৩ গুণ!*", "chip": "বিস্ময়কর রপ্তানি পণ্য", "t": 66.5},
 "tt": {"headline": "টুপি vs সাইকেল|*কে জিতল?*", "chip": "আয় প্রায় ৩ গুণ!", "t": 76},
 "v":  {"title": "টুপি রপ্তানি সাইকেলের ৩ গুণ!", "sub": "বিস্ময়কর রপ্তানি পণ্য তালিকা"}}
Optional per platform (yt/li/fb/tt): "size" (headline px; defaults yt 100, li 74, fb/tt 140), "pal" (palette index),
"stickers": [{"t": 31, "crop": [620,330,330,330], "x": 900, "y": 60, "w": 260, "r": -6, "round": 200}]  (a crop of a
video frame in 1920x1080 coords, e.g. the story character's face — round 200 = circle), "bursts": [{"text": "৩×",
"x": 980, "y": 420, "d": 230, "bg": "#ffe600", "fg": "#d00", "size": 90, "r": -10}] (starburst), "art": "<raw HTML/SVG>"
(own drawing for the topic, absolutely positioned).
Each platform gets a different vivid palette; the palette set rotates with the episode number,
so consecutive videos never share colours. Read every output (Read tool) before delivering.
"""
import argparse, base64, html, json, os, re, subprocess, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
ICON = os.path.join(os.path.dirname(HERE), "assets", "logo_icon.png")
WORD = os.path.join(os.path.dirname(HERE), "assets", "logo_word_white.png")
FONTS = os.path.join(os.environ.get("SK", "/tmp/evs/engine"), "assets", "fonts")
if not os.path.isdir(FONTS):
    FONTS = os.path.join(os.path.dirname(HERE), "vendor", "exportain-video-studio", "engine", "assets", "fonts")

# (background gradient, highlight bg, highlight text, chip bg, chip text, text shadow)
PAL = [
    ("linear-gradient(125deg,#ff3d77 0%,#ff7a18 55%,#ffd200 100%)", "#1d2bff", "#ffe600", "#111", "#ffe600", "rgba(120,0,40,.35)"),
    ("linear-gradient(170deg,#00c853 0%,#00a6a6 45%,#1565ff 100%)", "#ffe600", "#0b3b5c", "#ff3d77", "#fff", "rgba(0,40,80,.3)"),
    ("linear-gradient(165deg,#7b2ff7 0%,#f107a3 60%,#ff6a00 100%)", "#ffe600", "#7b0050", "#111", "#ffe600", "rgba(80,0,60,.35)"),
    ("linear-gradient(135deg,#0a2a66 0%,#0b6fb8 55%,#16c2c2 100%)", "#5cbf14", "#05220c", "#f2b705", "#1b1400", "rgba(0,10,40,.35)"),
    ("linear-gradient(150deg,#ff0844 0%,#ff5e3a 50%,#ffb199 100%)", "#ffffff", "#c2002f", "#1d2bff", "#fff", "rgba(110,0,20,.35)"),
    ("linear-gradient(160deg,#00b09b 0%,#5cbf14 55%,#d4fc79 100%)", "#ff3d77", "#fff", "#0b3b5c", "#fff", "rgba(0,60,30,.35)"),
    ("linear-gradient(140deg,#c62828 0%,#ef6c00 55%,#ffb300 100%)", "#d93636", "#fff", "#005a1e", "#fff", "rgba(120,60,0,.3)"),
    ("linear-gradient(150deg,#0039cb 0%,#0091c2 50%,#00a86b 100%)", "#7b2ff7", "#fff", "#ff3d77", "#fff", "rgba(0,50,90,.3)"),
]


def uri(p, mime):
    return f"data:{mime};base64," + base64.b64encode(open(p, "rb").read()).decode()


def head(txt):
    out = []
    for line in txt.split("|"):
        s = html.escape(line.strip())
        s = re.sub(r"\*(.+?)\*", r"<span class='hl'>\1</span>", s)
        out.append(s)
    return "<br>".join(out)


def frame_at(video, t, out):
    subprocess.check_call(["ffmpeg", "-y", "-loglevel", "error", "-ss", str(t), "-i", video, "-frames:v", "1", "-q:v", "2", out])
    return uri(out, "image/jpeg")


def css(p):
    bg, hb, hf, cb, cf, sh = p
    return f"""@font-face{{font-family:B;src:url(file://{FONTS}/NotoSansBengali-ExtraBold.ttf)}}
@font-face{{font-family:P;src:url(file://{FONTS}/Poppins-ExtraBold.ttf)}}
*{{margin:0;padding:0;box-sizing:border-box}} body{{overflow:hidden;font-family:B,P}}
#c{{position:relative;overflow:hidden;background:{bg}}}
.logo{{position:absolute;display:flex;align-items:center;gap:.12em}}
.logo .ic{{height:1em;filter:drop-shadow(2px 0 0 #fff) drop-shadow(-2px 0 0 #fff) drop-shadow(0 2px 0 #fff) drop-shadow(0 -2px 0 #fff) drop-shadow(0 8px 16px rgba(0,0,0,.35))}}
.logo .wd{{height:.38em;filter:drop-shadow(0 4px 10px rgba(0,0,0,.35))}}
.frame{{position:absolute;overflow:hidden;border:10px solid #fff;box-shadow:0 18px 50px rgba(0,0,0,.35)}}
.frame img{{width:100%;height:100%;object-fit:cover;object-position:50% 38%;display:block}}
.h{{position:absolute;color:#fff;letter-spacing:-.5px;text-shadow:3px 3px 0 rgba(0,0,0,.62),-3px 3px 0 rgba(0,0,0,.62),3px -3px 0 rgba(0,0,0,.62),-3px -3px 0 rgba(0,0,0,.62),0 9px 0 {sh},0 0 34px rgba(0,0,0,.5)}}   /* high contrast (owner, 26 Oct 2026) */
#c::before{{content:'';position:absolute;inset:0;pointer-events:none;background:radial-gradient(ellipse at 62% 48%,rgba(0,0,0,0) 38%,rgba(0,0,0,.34) 100%)}}
.hl{{background:{hb};color:{hf};padding:0 14px;border-radius:14px;white-space:nowrap;text-shadow:none;display:inline-block;border:5px solid rgba(0,0,0,.8);box-shadow:0 8px 0 rgba(0,0,0,.4)}}
.chip{{position:absolute;background:{cb};color:{cf};border-radius:999px;white-space:nowrap}}
.blob{{position:absolute;border-radius:50%;background:rgba(255,255,255,.17)}}
.burst{{position:absolute;display:flex;align-items:center;justify-content:center;text-align:center;background:#fff;color:#111;
  clip-path:polygon(50% 0,61% 13%,77% 6%,80% 22%,96% 24%,89% 39%,100% 50%,89% 61%,96% 76%,80% 78%,77% 94%,61% 87%,50% 100%,39% 87%,23% 94%,20% 78%,4% 76%,11% 61%,0 50%,11% 39%,4% 24%,20% 22%,23% 6%,39% 13%)}}
.stk{{position:absolute;overflow:hidden;border:9px solid #fff;box-shadow:0 14px 40px rgba(0,0,0,.4)}}
.stk img{{position:absolute;display:block}}
.spark{{position:absolute;color:#fff;font:800 60px P;text-shadow:0 0 18px rgba(255,255,255,.8)}}"""


def page(w, h, p, body):
    return (f"<!doctype html><meta charset=utf-8><style>{css(p)} body{{width:{w}px;height:{h}px}} "
            f"#c{{width:{w}px;height:{h}px}}</style><div id=c>{body}</div>")


def vsize(video):
    w, h = subprocess.check_output(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=width,height",
                                    "-of", "csv=p=0:s=x", video]).decode().strip().split("x")[:2]
    return int(w), int(h)


def build(ep, d, video, spec):
    FW, FH = vsize(video); vert = FH > FW
    n = int(re.sub(r"\D", "", ep)[:3] or 0)
    pal = [PAL[(n * 3 + k) % len(PAL)] for k in range(4)]          # yt, li, fb, tt — all different
    ic, wd = uri(ICON, "image/png"), uri(WORD, "image/png")
    logo = lambda style, size: f'<div class=logo style="{style};font-size:{size}px"><img class=ic src="{ic}"><img class=wd src="{wd}"></div>'
    tmp = tempfile.mkdtemp()
    img = lambda k, dflt: frame_at(video, spec.get(k, {}).get("t", dflt), os.path.join(tmp, f"{k}.jpg"))
    yt, li, fb, tt, v = (spec.get(k, {}) for k in ("yt", "li", "fb", "tt", "v"))
    for k, c in (("yt", yt), ("li", li), ("fb", fb), ("tt", tt)):
        if "pal" in c:
            pal[("yt", "li", "fb", "tt").index(k)] = PAL[int(c["pal"]) % len(PAL)]
    fz = lambda c, dflt: c.get("size", dflt)

    def extras(k):
        """stickers (crops of video frames, e.g. a character's face) + free HTML/SVG art drawn for this topic"""
        c, out = spec.get(k, {}), []
        for i, st in enumerate(c.get("stickers", [])):
            src = frame_at(video, st.get("t", 12), os.path.join(tmp, f"{k}_s{i}.jpg"))
            cx, cy, cw, chh = st.get("crop", [0, 0, FW, FH]); w = st.get("w", 300); sc = w / cw; h = chh * sc
            out.append(f'<div class=stk style="left:{st.get("x", 0)}px;top:{st.get("y", 0)}px;width:{w + 18}px;height:{h + 18:.0f}px;'
                       f'border-radius:{st.get("round", 40)}px;transform:rotate({st.get("r", 0)}deg)"><img src="{src}" '
                       f'style="left:{-cx * sc:.0f}px;top:{-cy * sc:.0f}px;width:{FW * sc:.0f}px"></div>')
        for b in c.get("bursts", []):
            out.append(f'<div class=burst style="left:{b["x"]}px;top:{b["y"]}px;width:{b.get("d", 220)}px;height:{b.get("d", 220)}px;'
                       f'background:{b.get("bg", "#fff")};color:{b.get("fg", "#111")};font:800 {b.get("size", 52)}px/1.05 P,B;'
                       f'transform:rotate({b.get("r", -8)}deg)">{head(b["text"])}</div>')
        out.append(c.get("art", ""))
        return "\n".join(out)
    cards = {}
    cards["thumb.jpg"] = (1280, 720, pal[0], f"""<div class=blob style="width:900px;height:900px;right:-330px;top:-260px"></div>
<div class=frame style="right:40px;top:120px;width:560px;height:480px;border-radius:36px;transform:rotate(3deg)"><img src="{img('yt', 12)}"></div>
{logo('left:46px;top:36px', 87)}
<div class=h style="left:50px;top:165px;width:700px;font:800 {fz(yt, 100)}px/1.15 B,P">{head(yt.get('headline', ''))}</div>{extras('yt')}
{f'<div class=chip style="left:50px;bottom:46px;font:800 40px B,P;padding:10px 28px">{html.escape(yt["chip"])}</div>' if yt.get('chip') else ''}
{f'<div style="position:absolute;right:70px;bottom:40px;background:#fff;color:#111;font:800 56px P,B;padding:4px 26px;border-radius:20px;transform:rotate(-4deg);box-shadow:0 10px 26px rgba(0,0,0,.3)">{html.escape(yt["badge"])}</div>' if yt.get('badge') else ''}""")
    cards["thumb_li.jpg"] = (1280, 720, pal[1], f"""<div class=blob style="left:-160px;bottom:-240px;width:640px;height:640px"></div>
<div class=frame style="right:46px;top:100px;width:600px;height:520px;border-radius:28px"><img src="{img('li', 12)}"></div>
{logo('left:46px;top:36px', 81)}
<div class=h style="left:52px;top:160px;width:590px;font:800 {fz(li, 74)}px/1.12 P">{head(li.get('headline', ''))}</div>{extras('li')}
{f'<div class=h style="left:52px;top:440px;width:560px;font:800 32px/1.35 P;text-shadow:none;opacity:.92">{html.escape(li["sub"])}</div>' if li.get('sub') else ''}
{f'<div class=chip style="left:52px;bottom:46px;font:800 32px P;padding:8px 24px;border-radius:12px">{html.escape(li["chip"])}</div>' if li.get('chip') else ''}""")
    cards["thumb_fb.jpg"] = (1080, 1920, pal[2], f"""<div class=blob style="width:1100px;height:1100px;left:-500px;top:-420px"></div>
{logo('left:50%;top:120px;transform:translateX(-50%)', 144)}
<div class=h style="left:70px;right:70px;top:320px;font:800 {fz(fb, 140)}px/1.15 B,P">{head(fb.get('headline', ''))}</div>
<div class=frame style="left:70px;right:70px;top:1020px;height:560px;border-radius:44px;transform:rotate(-2deg)"><img src="{img('fb', 12)}"></div>{extras('fb')}
{f'<div style="position:absolute;left:0;right:0;bottom:140px;text-align:center"><span class=chip style="position:static;font:800 58px B,P;padding:16px 46px">{html.escape(fb["chip"])}</span></div>' if fb.get('chip') else ''}""")
    cards["thumb_tt.jpg"] = (1080, 1920, pal[3], f"""<div class=blob style="width:900px;height:900px;right:-420px;bottom:-300px"></div>
{logo('left:70px;top:130px', 129)}
<div class=frame style="left:60px;right:60px;top:330px;height:620px;border-radius:44px;transform:rotate(2deg)"><img src="{img('tt', 12)}"></div>
<div class=h style="left:70px;right:70px;top:1020px;font:800 {fz(tt, 140)}px/1.12 B,P">{head(tt.get('headline', ''))}</div>{extras('tt')}
{f'<div class=chip style="left:70px;bottom:200px;font:800 58px B,P;padding:14px 40px">{html.escape(tt["chip"])}</div>' if tt.get('chip') else ''}""")
    # vertical video frame: video goes into the slot 0..1080 x 656..1264
    cards["vframe.jpg"] = (1080, 1920, pal[2], f"""<div class=blob style="width:1000px;height:1000px;left:-460px;top:-460px"></div>
<div class=blob style="width:700px;height:700px;right:-300px;bottom:-260px"></div>
{logo('left:50%;top:110px;transform:translateX(-50%)', 126)}
<div class=h style="left:60px;right:60px;top:285px;text-align:center;font:800 84px/1.22 B,P">{head(v.get('title', ''))}</div>
<div style="position:absolute;left:0;top:646px;width:1080px;height:628px;background:#0b1d12"></div>
{f'<div style="position:absolute;left:0;right:0;top:1330px;text-align:center"><span class=chip style="position:static;font:800 50px B,P;padding:14px 40px">{html.escape(v["sub"])}</span></div>' if v.get('sub') else ''}
<div style="position:absolute;left:0;right:0;top:1480px;text-align:center"><span style="background:#fff;color:#005a1e;font:800 58px P;padding:12px 44px;border-radius:999px;box-shadow:0 10px 30px rgba(0,0,0,.25)">Exportain.com</span></div>""")
    if vert:   # 9:16 video: portrait picture frames + 9:16 covers for YouTube Shorts and LinkedIn
        def vcard(k, c, p, font, size):
            return (1080, 1920, p, f"""<div class=blob style="width:1000px;height:1000px;right:-420px;top:-360px"></div>
{logo('left:50%;top:110px;transform:translateX(-50%)', 132)}
<div class=h style="left:70px;right:70px;top:300px;text-align:center;font:800 {fz(c, size)}px/1.14 {font}">{head(c.get('headline', ''))}</div>
<div class=frame style="left:250px;width:580px;top:900px;height:780px;border-radius:44px;transform:rotate(-2deg)"><img src="{img(k, 12)}"></div>{extras(k)}
{f'<div style="position:absolute;left:0;right:0;bottom:110px;text-align:center"><span class=chip style="position:static;font:800 54px {font};padding:14px 42px">{html.escape(c["chip"])}</span></div>' if c.get('chip') else ''}""")
        cards["thumb_yt9.jpg"] = vcard("yt", yt, pal[0], "B,P", 130)
        cards["thumb_li9.jpg"] = vcard("li", li, pal[1], "P", 110)
        for k in ("thumb_fb.jpg", "thumb_tt.jpg"):   # landscape boxes -> portrait boxes for a 9:16 picture
            w, h, p, body = cards[k]
            body = body.replace('left:70px;right:70px;top:1020px;height:560px', 'left:270px;right:270px;top:1000px;height:680px')
            body = body.replace('left:60px;right:60px;top:330px;height:620px', 'left:300px;right:300px;top:300px;height:640px')
            cards[k] = (w, h, p, body)
    from playwright.sync_api import sync_playwright
    with sync_playwright() as pw:
        b = pw.chromium.launch()
        for name, (w, h, p, body) in cards.items():
            f = os.path.join(tmp, name + ".html"); open(f, "w", encoding="utf-8").write(page(w, h, p, body))
            pg = b.new_page(viewport={"width": w, "height": h}); pg.goto("file://" + f)
            pg.evaluate("document.fonts.ready"); pg.wait_for_timeout(300)
            out = os.path.join(d, name); pg.screenshot(path=out, type="jpeg", quality=88); pg.close()
            print(f"{name}: {w}x{h} {os.path.getsize(out)//1024} KB")
        b.close()


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("ep"); ap.add_argument("dir"); ap.add_argument("--video", required=True); ap.add_argument("--spec")
    a = ap.parse_args()
    spec = json.load(open(a.spec or os.path.join(a.dir, "thumbs.json"), encoding="utf-8"))
    build(a.ep, a.dir, a.video, spec)
