#!/usr/bin/env python3
"""Premium Shorts thumbnail / cover (1080x1920 JPEG <= 2 MB), designed — never a raw frame.

  python3 thumb.py <video.mp4> <spec.json> <out.jpg> [--n 7]

Used for: YouTube custom thumbnail (thumbnails.set), the cover frame prepended to the video (cover.py), which is also
the TikTok cover. Rendered from HTML in headless Chromium, so Bangla shaping and the brand fonts are exact.

spec.json ("|" = line break, *word* = highlighted word/phrase; everything optional except headline):
{
 "lang": "en" | "bn",
 "layout": "card" | "bleed" | "split" | "number",     # rotate: never the same layout two Shorts in a row
 "pal": 0-9,                                          # palette; default rotates with --n (plan number)
 "kicker": "BANGLADESH EXPORT GUIDE",                 # small pill above the headline (2-4 words)
 "headline": "How to *export*|garments",              # 2-6 words, max 3 lines — the click reason
 "sub": "3 simple steps",                             # optional one short line under the headline
 "number": "$38.7B",                                  # layout "number": the giant figure
 "burst": "3 STEPS",                                  # starburst sticker (short: 1-2 words / a number)
 "t": 3.5, "crop": [x, y, w, h],                      # hero = frame at second t (crop in 1080x1920 px; optional)
 "sticker": {"t": 15.2, "crop": [x, y, w, h], "round": true},   # optional 2nd frame as a round/square sticker
 "arrow": true                                        # big curved arrow pointing at the hero
}
Design rules baked in: vivid saturated gradient + light rays, white headline with a thick dark outline and glow,
highlight word in a tilted yellow (or palette) box, hero image in a thick white frame with a hard shadow, logo
(green icon + white wordmark, never on a white pill), everything important inside y 260-1600 (TikTok/YouTube grid
crop and UI). Text auto-shrinks to fit 960 px. After rendering: LOOK at the result at phone size.
"""
import base64, html, json, os, re, subprocess, sys, tempfile

KIT = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(KIT))
ICON = os.path.join(ROOT, "assets", "logo_icon.png")
WORD = os.path.join(ROOT, "assets", "logo_word_white.png")
FONTS = None
for c in (os.path.join(os.environ.get("SK", ""), "assets", "fonts"), "/tmp/evs_sh/engine/assets/fonts",
          os.path.join(ROOT, "vendor", "exportain-video-studio", "engine", "assets", "fonts")):
    if c and os.path.isdir(c):
        FONTS = c; break

# (background, ray colour, highlight bg, highlight text, kicker bg, kicker text, burst bg, burst text, outline)
PAL = [
    ("linear-gradient(160deg,#ff0f7b 0%,#ff6a00 55%,#ffd000 100%)", "255,255,255", "#ffe600", "#1a0033", "#1a0033", "#ffe600", "#00e5ff", "#00213a", "#3a0018"),
    ("linear-gradient(165deg,#3a00ff 0%,#a100ff 45%,#ff2ea6 100%)", "255,214,0", "#ffe600", "#2b0060", "#ffe600", "#2b0060", "#ff2e2e", "#ffffff", "#170033"),
    ("linear-gradient(160deg,#00c853 0%,#00b8a9 50%,#0052ff 100%)", "255,255,255", "#ffe600", "#002b1a", "#ff2ea6", "#ffffff", "#ffe600", "#c2002f", "#00213a"),
    ("linear-gradient(160deg,#ff1744 0%,#ff6d00 60%,#ffc400 100%)", "255,255,160", "#ffffff", "#c40026", "#0d1b6b", "#ffffff", "#00e676", "#002b14", "#3b0006"),
    ("linear-gradient(165deg,#0a1aa8 0%,#0091ff 50%,#00e5c4 100%)", "255,255,255", "#ffe600", "#0a1aa8", "#ffe600", "#0a1aa8", "#ff3d00", "#ffffff", "#000c3a"),
    ("linear-gradient(160deg,#7b00ff 0%,#ff0080 55%,#ff8c00 100%)", "255,230,0", "#00f5d4", "#1a0040", "#111111", "#00f5d4", "#ffe600", "#b00040", "#20002e"),
    ("linear-gradient(165deg,#005a1e 0%,#2e8b2e 45%,#b6f000 100%)", "255,255,200", "#ffe600", "#003c10", "#ffe600", "#003c10", "#ff2e63", "#ffffff", "#001a07"),
    ("linear-gradient(160deg,#ff4e00 0%,#ec2f4b 50%,#7b1fa2 100%)", "255,220,120", "#ffe600", "#4a0030", "#00e5ff", "#00213a", "#ffffff", "#ec2f4b", "#2a0010"),
    ("linear-gradient(165deg,#00b4db 0%,#0083b0 45%,#1a237e 100%)", "255,255,255", "#ff2ea6", "#ffffff", "#ffe600", "#1a237e", "#ffe600", "#1a237e", "#00102e"),
    ("linear-gradient(160deg,#f9d423 0%,#ff4e50 60%,#c2185b 100%)", "255,255,255", "#1a0033", "#ffe600", "#1a0033", "#ffffff", "#00e5ff", "#1a0033", "#40000f"),
]


def uri(p, mime):
    return f"data:{mime};base64," + base64.b64encode(open(p, "rb").read()).decode()


def head(txt):
    out = []
    for line in str(txt).split("|"):
        s = html.escape(line.strip())
        s = re.sub(r"\*(.+?)\*", r"<span class='hl'><span>\1</span></span>", s)
        out.append(f"<div class='ln'>{s}</div>")
    return "".join(out)


def frame(video, t, crop, out):
    vf = "scale=1080:1920"
    if crop:
        x, y, w, h = crop
        vf += f",crop={w}:{h}:{x}:{y}"
    subprocess.check_call(["ffmpeg", "-y", "-loglevel", "error", "-ss", str(t), "-i", video, "-frames:v", "1",
                           "-vf", vf, "-q:v", "2", out])
    return out


def hero3d(gl, out):
    """Clean 3D hero straight from r3d.js (no text, no bubbles): gl = board-style world options + "at" (seconds)."""
    from playwright.sync_api import sync_playwright
    d = os.path.dirname(out)
    page = os.path.join(d, "h3d.html")
    open(page, "w").write(f"""<!doctype html><html><body style='margin:0;background:#000'><div id='st' style='position:relative;width:1080px;height:1920px'></div>
<script type='module'>import * as R from 'file://{KIT}/r3d.js';
R.setPlan({{scenes:[{{id:'h',start:0,end:{gl.get('dur', 8)},gl:{json.dumps(gl)}}}],voice_duration:999}});
R.frame({gl.get('at', 2.5)});window.done=true;</script></body></html>""")
    png = out[:-4] + ".png"
    with sync_playwright() as p:
        b = p.chromium.launch(args=["--use-gl=angle", "--use-angle=swiftshader", "--enable-unsafe-swiftshader",
                                    "--ignore-gpu-blocklist", "--allow-file-access-from-files"])
        pg = b.new_page(viewport={"width": 1080, "height": 1920})
        pg.set_default_timeout(180000)
        pg.goto("file://" + page)
        pg.wait_for_function("window.done===true", timeout=180000)
        pg.wait_for_timeout(200)
        pg.screenshot(path=png)
        b.close()
    vf = "eq=saturation=1.25:contrast=1.08"
    if gl.get("crop"):
        x, y, w, h = gl["crop"]
        vf = f"crop={w}:{h}:{x}:{y}," + vf
    subprocess.check_call(["ffmpeg", "-y", "-loglevel", "error", "-i", png, "-vf", vf, "-q:v", "2", out])
    return out


def build(spec, hero, sticker, n):
    p = PAL[int(spec.get("pal", n * 3 % len(PAL))) % len(PAL)]
    bg, ray, hlb, hlt, kb, kt, bb, bt, ol = p
    lang = spec.get("lang", "en")
    hfont = "Pop" if lang == "en" else "B"
    layout = spec.get("layout", ["card", "bleed", "split", "number"][n % 4])
    if layout == "number" and not spec.get("number"):
        layout = "card"
    ff = "".join(f"@font-face{{font-family:{f};src:url('file://{FONTS}/{fn}');font-weight:{w}}}" for f, fn, w in [
        ("B", "NotoSansBengali-Bold.ttf", 700), ("B", "NotoSansBengali-ExtraBold.ttf", 800),
        ("Pop", "Poppins-Bold.ttf", 700), ("Pop", "Poppins-ExtraBold.ttf", 800), ("Pop", "Poppins-SemiBold.ttf", 600)])
    kicker = html.escape(spec.get("kicker", ""))
    sub = html.escape(spec.get("sub", ""))
    burst = html.escape(spec.get("burst", ""))
    number = html.escape(spec.get("number", ""))
    up = "text-transform:uppercase;" if lang == "en" else ""
    hero_uri = uri(hero, "image/jpeg")
    stk = ""
    if sticker:
        r = "50%" if spec.get("sticker", {}).get("round", True) else "36px"
        stk = (f"<div class='stk' style='border-radius:{r}'><img src='{uri(sticker, 'image/jpeg')}' "
               f"style='border-radius:{r}'></div>")
    arrow = ("<svg class='arrow' viewBox='0 0 220 220'><path d='M30 40 Q 120 30 150 120 L 182 104 L 170 200 L 92 150 "
             "L 122 136 Q 104 84 40 86 Z' fill='#ffe600' stroke='#111' stroke-width='12' stroke-linejoin='round'/></svg>") if spec.get("arrow") else ""
    pts = []
    import math
    for i in range(24):
        r = 1 if i % 2 == 0 else .74
        a = i / 24 * 2 * math.pi
        pts.append(f"{50 + 50 * r * math.cos(a):.1f}% {50 + 50 * r * math.sin(a):.1f}%")
    burst_html = f"<div class='burst'><div class='bin'>{burst}</div></div>" if burst else ""

    # layout-specific blocks
    if layout == "bleed":
        body = f"""<img class='full' src='{hero_uri}'><div class='shade'></div>
        <div class='band'><div class='kick'>{kicker}</div><div class='h'>{head(spec['headline'])}</div>{f"<div class='sub'>{sub}</div>" if sub else ''}</div>
        {burst_html}{stk}{arrow}"""
    elif layout == "split":
        body = f"""<div class='rays'></div><div class='top'><div class='kick'>{kicker}</div><div class='h'>{head(spec['headline'])}</div>{f"<div class='sub'>{sub}</div>" if sub else ''}</div>
        <div class='torn'><img src='{hero_uri}'></div>{burst_html}{stk}{arrow}"""
    elif layout == "number":
        body = f"""<div class='rays'></div><div class='top'><div class='kick'>{kicker}</div><div class='h small'>{head(spec['headline'])}</div></div>
        <div class='num'><span class='nv'>{number}</span></div><div class='hero round'><img src='{hero_uri}'></div>{f"<div class='sub low'>{sub}</div>" if sub else ''}{burst_html}{stk}{arrow}"""
    else:  # card
        body = f"""<div class='rays'></div><div class='top'><div class='kick'>{kicker}</div><div class='h'>{head(spec['headline'])}</div>{f"<div class='sub'>{sub}</div>" if sub else ''}</div>
        <div class='hero'><img src='{hero_uri}'></div>{burst_html}{stk}{arrow}"""

    css = f"""{ff}
*{{margin:0;padding:0;box-sizing:border-box}}
html,body{{width:1080px;height:1920px;overflow:hidden}}
#c{{position:relative;width:1080px;height:1920px;overflow:hidden;background:{bg}}}
.rays{{position:absolute;left:-540px;top:-300px;width:2160px;height:2160px;opacity:.22;
 background:repeating-conic-gradient(from 0deg at 50% 50%,rgba({ray},.9) 0deg 7deg,transparent 7deg 18deg);
 -webkit-mask:radial-gradient(circle at 50% 50%,#000 10%,transparent 62%)}}
.glow{{position:absolute;inset:0;background:radial-gradient(60% 38% at 50% 30%,rgba(255,255,255,.35),transparent 70%)}}
.grain{{position:absolute;inset:0;opacity:.07;z-index:30;pointer-events:none;background-image:url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='200' height='200'><filter id='n'><feTurbulence type='fractalNoise' baseFrequency='.85' numOctaves='2'/></filter><rect width='100%25' height='100%25' filter='url(%23n)'/></svg>")}}
.vig{{position:absolute;inset:0;z-index:29;background:radial-gradient(90% 70% at 50% 45%,transparent 60%,rgba(0,0,0,.35))}}
.brand{{position:absolute;left:56px;top:70px;z-index:40;display:flex;align-items:center;gap:14px;filter:drop-shadow(0 6px 14px rgba(0,0,0,.45))}}
.brand img.i{{height:96px}} .brand img.w{{height:46px}}
.url{{position:absolute;left:50%;bottom:150px;transform:translateX(-50%);z-index:40;font:800 40px Pop;color:#fff;letter-spacing:1px;
 background:rgba(0,0,0,.55);padding:16px 40px;border-radius:60px;border:4px solid rgba(255,255,255,.85);white-space:nowrap}}
.top{{position:absolute;left:60px;right:60px;top:250px;z-index:20;text-align:center}}
.kick{{display:inline-block;font:800 40px {hfont};{up}letter-spacing:{'3px' if lang == 'en' else '0'};color:{kt};background:{kb};
 padding:12px 34px 14px;border-radius:14px;transform:rotate(-2deg);box-shadow:0 10px 0 rgba(0,0,0,.28);margin-bottom:26px}}
.kick:empty{{display:none}}
.h{{font-family:{hfont};font-weight:800;{up}color:#fff;font-size:150px;line-height:{'1.02' if lang == 'en' else '1.22'};letter-spacing:{'-2px' if lang == 'en' else '0'};
 -webkit-text-stroke:14px {ol};paint-order:stroke fill;text-shadow:0 14px 0 rgba(0,0,0,.30),0 0 50px rgba(0,0,0,.25)}}
.h.small{{font-size:96px}}
.ln{{white-space:nowrap}}
.hl{{display:inline-block;position:relative;padding:0 18px;margin:6px 0;z-index:1;color:{hlt};-webkit-text-stroke:0}}
.hl::before{{content:'';position:absolute;inset:{'6px' if lang == 'en' else '10px'} 0 {'2px' if lang == 'en' else '-2px'} 0;background:{hlb};border-radius:18px;transform:rotate(-2.5deg);z-index:-1;
 box-shadow:0 12px 0 rgba(0,0,0,.30)}}
.hl span{{text-shadow:none}}
.sub{{display:inline-block;margin-top:24px;font:800 54px {hfont};color:#fff;background:rgba(0,0,0,.42);padding:10px 32px 14px;border-radius:50px}}
.sub.low{{position:absolute;left:50%;top:1500px;transform:translateX(-50%);white-space:nowrap;z-index:22}}
.hero{{position:absolute;left:75px;top:1010px;width:930px;height:620px;z-index:10;border:16px solid #fff;border-radius:40px;overflow:hidden;
 transform:rotate(-3deg);box-shadow:24px 28px 0 rgba(0,0,0,.30),0 30px 70px rgba(0,0,0,.4)}}
.hero img{{width:100%;height:100%;object-fit:cover;object-position:{spec.get('pos', '50% 50%')}}}
.hero.round{{left:290px;top:1080px;width:500px;height:500px;border-radius:50%;transform:none}}
.nv{{display:inline-block}}
.num{{position:absolute;left:0;right:0;top:600px;text-align:center;z-index:21;font:800 300px Pop;color:{hlb};letter-spacing:-8px;
 -webkit-text-stroke:18px {ol};paint-order:stroke fill;text-shadow:0 18px 0 rgba(0,0,0,.3);white-space:nowrap}}
.full{{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;filter:saturate(1.35) contrast(1.12)}}
.shade{{position:absolute;inset:0;background:linear-gradient(180deg,rgba(0,0,0,.55) 0%,rgba(0,0,0,0) 30%,rgba(0,0,0,0) 62%,rgba(0,0,0,.6) 100%)}}
.band{{position:absolute;left:-60px;right:-60px;top:560px;padding:50px 120px 60px;z-index:20;text-align:center;background:{bg};
 transform:rotate(-5deg);box-shadow:0 26px 0 rgba(0,0,0,.25),0 30px 80px rgba(0,0,0,.45);border-top:12px solid #fff;border-bottom:12px solid #fff}}
.band .h{{font-size:140px}}
.torn{{position:absolute;left:0;right:0;top:1000px;height:920px;z-index:10;overflow:hidden;
 clip-path:polygon(0 8%,10% 3%,22% 9%,35% 2%,48% 8%,60% 1%,73% 7%,86% 2%,100% 8%,100% 100%,0 100%)}}
.torn img{{width:100%;height:100%;object-fit:cover;filter:saturate(1.3) contrast(1.1)}}
.burst{{position:absolute;right:46px;top:880px;width:300px;height:300px;z-index:25;background:{bb};transform:rotate(12deg);
 clip-path:polygon({','.join(pts)});filter:drop-shadow(0 10px 0 rgba(0,0,0,.3));display:flex;align-items:center;justify-content:center}}
.bin{{font:800 54px {'Pop' if re.fullmatch(r'[ -~৳$%×+.,#]+', spec.get('burst', '') or 'x') else 'B'};color:{bt};text-align:center;line-height:1.05;padding:0 40px;{up}}}
.stk{{position:absolute;left:46px;top:1440px;width:260px;height:260px;z-index:26;border:12px solid #fff;overflow:hidden;
 box-shadow:0 14px 0 rgba(0,0,0,.3);transform:rotate(-6deg)}}
.stk img{{width:100%;height:100%;object-fit:cover}}
.arrow{{position:absolute;left:70px;top:820px;width:210px;height:210px;z-index:24;filter:drop-shadow(0 10px 0 rgba(0,0,0,.35))}}
"""
    if layout == "number":
        css += ".burst{top:1180px;right:40px;width:260px;height:260px}.arrow{display:none}"
    if layout == "bleed":
        css += ".burst{top:1180px}.arrow{top:1120px;left:90px}"
    if layout == "split":
        css += ".burst{top:900px}"
    brand = (f"<div class='brand'><img class='i' src='{uri(ICON, 'image/png')}'><img class='w' src='{uri(WORD, 'image/png')}'></div>"
             "<div class='url'>EXPORTAIN.COM</div>")
    fit = """<script>
document.fonts.ready.then(()=>{for(const h of document.querySelectorAll('.h,.num')){let s=parseFloat(getComputedStyle(h).fontSize);
 const max=h.classList.contains('num')?920:960;
 const lines=[...h.querySelectorAll('.ln,.nv')];const w=()=>h.classList.contains('num')?Math.max(...lines.map(l=>l.getBoundingClientRect().width)):Math.max(h.scrollWidth,...lines.map(l=>l.scrollWidth));
 while(w()>max&&s>50){s-=4;h.style.fontSize=s+'px'}
 const top=h.closest('.top');if(top&&!h.classList.contains('small')){while(top.getBoundingClientRect().bottom>990&&s>60){s-=4;h.style.fontSize=s+'px'}}}
 window.done=true});</script>"""
    return f"<!doctype html><html><head><meta charset='utf-8'><style>{css}</style></head><body><div id='c'><div class='glow'></div>{body}{brand}<div class='vig'></div><div class='grain'></div></div>{fit}</body></html>"


def main():
    video, spec_p, out = sys.argv[1], sys.argv[2], sys.argv[3]
    n = int(sys.argv[sys.argv.index("--n") + 1]) if "--n" in sys.argv else 0
    spec = json.load(open(spec_p, encoding="utf-8"))
    tmp = tempfile.mkdtemp()
    if spec.get("hero"):          # preferred: clean 3D shot of the Short's world
        hero = hero3d(spec["hero"], os.path.join(tmp, "hero.jpg"))
    else:                         # fallback: a frame of the video
        hero = frame(video, spec.get("t", 3.0), spec.get("crop"), os.path.join(tmp, "hero.jpg"))
    st = spec.get("sticker")
    sticker = frame(video, st["t"], st.get("crop"), os.path.join(tmp, "stk.jpg")) if st else None
    page = os.path.join(tmp, "t.html")
    open(page, "w", encoding="utf-8").write(build(spec, hero, sticker, n))
    from playwright.sync_api import sync_playwright
    png = os.path.join(tmp, "t.png")
    with sync_playwright() as p:
        b = p.chromium.launch(args=["--allow-file-access-from-files"])
        pg = b.new_page(viewport={"width": 1080, "height": 1920})
        pg.goto("file://" + page)
        pg.wait_for_function("window.done===true", timeout=60000)
        pg.wait_for_timeout(150)
        pg.screenshot(path=png)
        b.close()
    for q in (2, 3, 5, 8):
        subprocess.check_call(["ffmpeg", "-y", "-loglevel", "error", "-i", png, "-q:v", str(q), out])
        if os.path.getsize(out) <= 1_900_000:
            break
    print(out, os.path.getsize(out), "bytes")


if __name__ == "__main__":
    main()
