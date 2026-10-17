#!/usr/bin/env python3
"""Render several exact frames in ONE browser session and tile them into a contact sheet.
  python3 qa_stills.py --plan plan.json --size 1920x1080 --out qa.jpg 12.5 40 81.2 ...
Pick times near the END of each scene so every numbered marker / typed field is visible."""
import argparse, os, sys, tempfile
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from render import open_page, page_html, load_plan
from playwright.sync_api import sync_playwright
from PIL import Image
ap = argparse.ArgumentParser(); ap.add_argument('--plan', required=True); ap.add_argument('--out', required=True)
ap.add_argument('--size', default='1920x1080'); ap.add_argument('--cols', type=int, default=2); ap.add_argument('times', nargs='+', type=float)
a = ap.parse_args(); w, h = map(int, a.size.split('x')); plan = load_plan(a.plan); work = tempfile.mkdtemp()
html = page_html(work, plan.get('template', 'timeline.html')); ims = []
with sync_playwright() as p:
    b, pg = open_page(p, html, plan, w, h)
    for i, t in enumerate(a.times):
        pg.evaluate('(t)=>window.__render(t)', t); f = os.path.join(work, f's{i}.jpg'); pg.screenshot(path=f, type='jpeg', quality=80)
        ims.append(Image.open(f).resize((w // 2, h // 2)))
    b.close()
c = a.cols; r = (len(ims) + c - 1) // c; sheet = Image.new('RGB', (c * w // 2, r * h // 2), 'white')
for i, im in enumerate(ims): sheet.paste(im, ((i % c) * w // 2, (i // c) * h // 2))
sheet.save(a.out, quality=80); print(a.out)
