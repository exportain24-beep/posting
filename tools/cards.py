#!/usr/bin/env python3
"""Facebook photo carousel: 3–5 colourful 4:5 key-takeaway cards for each reel (owner, 31 Oct 2026: photo posts reach
more people on Facebook — every video also gets a photo post, scheduled after the video's slot).

  cards.py <EP> <DIR> [--video DIR/out/<Name_9x16>.mp4] [--spec DIR/cards.json]

cards.json:
{"pal": 5,                                   # optional palette index (tools/thumbs.py PAL); default rotates per episode
 "cards": [
  {"kind": "cover", "headline": "বিদেশে প্রথম|*ক্রেতা* কোথায়?", "chip": "৫টি ধাপে প্রবাসী বাজার", "t": 21},
  {"kicker": "ধাপ ১", "title": "প্রবাসী বাজার কী", "points": ["বিদেশে থাকা বাংলাদেশি আর তাঁদের দোকান", "…"]},
  {"kicker": "ধাপ ২", "title": "…", "points": ["…", "…"], "note": "উদাহরণ"},
  {"kind": "end", "headline": "চেনা বাজারে শুরু,|*মান* বাড়িয়ে বড় বাজার", "chip": "পুরো ভিডিও আমাদের পেজে"}]}
"|" = line break, *word* = highlighted. "t" (cover) = second of the video for the picture (needs --video).
Points: 2–4 short lines (≤ 42 Bangla characters each). Facts only from the video's verified script.
Writes DIR/card_1.jpg … card_N.jpg (1080×1350). Read every card before delivering.
"""
import argparse, html, json, os, re, sys, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from thumbs import ICON, WORD, PAL, css, frame_at, head, uri   # noqa: E402

W, H = 1080, 1350


def build(ep, d, video, spec):
    n = int(re.sub(r"\D", "", ep)[:3] or 0)
    p = PAL[int(spec["pal"]) % len(PAL)] if "pal" in spec else PAL[(n * 3 + 2) % len(PAL)]
    ic, wd = uri(ICON, "image/png"), uri(WORD, "image/png")
    logo = f'<div class=logo style="left:60px;top:52px;font-size:96px"><img class=ic src="{ic}"><img class=wd src="{wd}"></div>'
    cards = spec["cards"]
    tmp = tempfile.mkdtemp()
    out = []
    for i, c in enumerate(cards, 1):
        pager = f'<div style="position:absolute;right:60px;top:70px;color:#fff;font:800 40px P,B;opacity:.9">{i}/{len(cards)}</div>'
        foot = ('<div style="position:absolute;left:0;right:0;bottom:46px;text-align:center"><span style="background:#fff;'
                'color:#005a1e;font:800 40px P;padding:10px 36px;border-radius:999px;box-shadow:0 10px 30px rgba(0,0,0,.25)">'
                'exportain.com</span></div>')
        kind = c.get("kind", "point")
        if kind in ("cover", "end"):
            pic = ""
            if kind == "cover" and video and "t" in c:
                pic = (f'<div class=frame style="left:150px;right:150px;top:690px;height:440px;border-radius:40px;'
                       f'transform:rotate(-2deg)"><img src="{frame_at(video, c["t"], os.path.join(tmp, f"c{i}.jpg"))}"></div>')
            top = 250 if pic else 360
            body = f"""<div class=blob style="width:900px;height:900px;right:-360px;top:-300px"></div>
<div class=blob style="width:600px;height:600px;left:-260px;bottom:-260px"></div>{logo}{pager}
<div class=h style="left:70px;right:70px;top:{top}px;text-align:center;font:800 {c.get('size', 104)}px/1.18 B,P">{head(c.get('headline', ''))}</div>{pic}
{f'<div style="position:absolute;left:0;right:0;top:{1170 if pic else 1000}px;text-align:center"><span class=chip style="position:static;font:800 48px B,P;padding:12px 40px">{html.escape(c["chip"])}</span></div>' if c.get('chip') else ''}
{'' if pic else foot}"""
        else:
            pts = "".join(
                f'<div style="display:flex;gap:26px;align-items:flex-start;margin:0 0 34px">'
                f'<div style="flex:none;width:64px;height:64px;border-radius:50%;background:#2e8b2e;color:#fff;'
                f'font:800 38px/64px P;text-align:center">✓</div>'
                f'<div style="font:700 46px/1.32 B,P;color:#0f1f14">{html.escape(t)}</div></div>' for t in c.get("points", []))
            body = f"""<div class=blob style="width:800px;height:800px;left:-320px;top:-280px"></div>{logo}{pager}
{f'<div class=chip style="left:70px;top:205px;font:800 42px B,P;padding:8px 30px">{html.escape(c["kicker"])}</div>' if c.get('kicker') else ''}
<div class=h style="left:70px;right:70px;top:290px;font:800 {c.get('size', 84)}px/1.16 B,P">{head(c.get('title', ''))}</div>
<div style="position:absolute;left:60px;right:60px;top:{c.get('panel_top', 560)}px;bottom:150px;background:#fff;border-radius:44px;
 padding:56px 56px;box-shadow:0 18px 50px rgba(0,0,0,.28);display:flex;flex-direction:column;justify-content:center">{pts}
{f'<div style="position:absolute;right:40px;bottom:30px;background:#e8890c;color:#fff;font:800 30px B;padding:6px 22px;border-radius:999px">{html.escape(c["note"])}</div>' if c.get('note') else ''}</div>
{foot}"""
        out.append((f"card_{i}.jpg", body))
    from playwright.sync_api import sync_playwright
    with sync_playwright() as pw:
        b = pw.chromium.launch()
        for name, body in out:
            f = os.path.join(tmp, name + ".html")
            open(f, "w", encoding="utf-8").write(
                f"<!doctype html><meta charset=utf-8><style>{css(p)} body{{width:{W}px;height:{H}px}} "
                f"#c{{width:{W}px;height:{H}px}}</style><div id=c>{body}</div>")
            pg = b.new_page(viewport={"width": W, "height": H}); pg.goto("file://" + f)
            pg.evaluate("document.fonts.ready"); pg.wait_for_timeout(300)
            o = os.path.join(d, name); pg.screenshot(path=o, type="jpeg", quality=88); pg.close()
            print(f"{name}: {W}x{H} {os.path.getsize(o)//1024} KB")
        b.close()
    for f in os.listdir(d):    # drop stale cards from an earlier, longer spec
        m = re.fullmatch(r"card_(\d+)\.jpg", f)
        if m and int(m.group(1)) > len(out):
            os.remove(os.path.join(d, f))


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("ep"); ap.add_argument("dir"); ap.add_argument("--video"); ap.add_argument("--spec")
    a = ap.parse_args()
    spec = json.load(open(a.spec or os.path.join(a.dir, "cards.json"), encoding="utf-8"))
    if not 3 <= len(spec.get("cards", [])) <= 6:
        raise SystemExit("cards.json: 3-6 cards")
    build(a.ep, a.dir, a.video, spec)
