#!/usr/bin/env python3
"""Watch your own render before shipping: timestamped contact sheets, frozen-stretch detection, loudness.
  python3 review.py --video out/final_9x16.mp4 [--plan plan.json] [--every 1.0] [--out review/]
Writes review/sheet_NN.jpg (12 frames each, time printed on every frame) and review/report.txt:
- frozen stretches (no visible change for > 2.5 s = a dead hold; shorts need something new every 5-7 s)
- integrated loudness / true peak (target -14 LUFS, <= -1 dBTP)
- per scene: seconds of near-still picture (from --plan)
Read every sheet. Hand them to an independent critic when the job is high-stakes."""
import argparse, json, os, re, subprocess
import numpy as np
from PIL import Image, ImageDraw


def probe(v):
    o = subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration:stream=width,height', '-of', 'json', v],
                       capture_output=True, text=True).stdout
    j = json.loads(o); s = [x for x in j['streams'] if 'width' in x][0]
    return float(j['format']['duration']), s['width'], s['height']


def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--video', required=True); ap.add_argument('--plan')
    ap.add_argument('--every', type=float, default=1.0); ap.add_argument('--out', default='review')
    a = ap.parse_args(); os.makedirs(a.out, exist_ok=True)
    dur, w, h = probe(a.video)
    # low-res grey frames at 5 fps for motion analysis
    sw, sh = 64, int(64 * h / w)
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', a.video, '-vf', f'fps=5,scale={sw}:{sh},format=gray', '-f', 'rawvideo', '-'],
                         capture_output=True).stdout
    fr = np.frombuffer(raw, np.uint8).reshape(-1, sh, sw).astype(np.float32)
    diff = np.r_[0, np.abs(np.diff(fr, axis=0)).mean(axis=(1, 2))]
    still = diff < 0.35; frozen, i = [], 0
    while i < len(still):
        if still[i]:
            j = i
            while j < len(still) and still[j]: j += 1
            if (j - i) / 5 > 2.5: frozen.append((i / 5, j / 5))
            i = j
        else: i += 1
    # contact sheets with timestamps
    times = list(np.arange(0.5, dur, a.every)); tw = 270; th = int(tw * h / w); sheets = []
    for k in range(0, len(times), 12):
        chunk = times[k:k + 12]; cols = 6 if h > w else 4; rows = -(-len(chunk) // cols)
        sheet = Image.new('RGB', (cols * tw, rows * (th + 22)), 'white'); d = ImageDraw.Draw(sheet)
        for n, t in enumerate(chunk):
            png = subprocess.run(['ffmpeg', '-v', 'error', '-ss', f'{t:.2f}', '-i', a.video, '-frames:v', '1', '-vf', f'scale={tw}:{th}',
                                  '-f', 'image2pipe', '-vcodec', 'png', '-'], capture_output=True).stdout
            p = os.path.join(a.out, '_f.png'); open(p, 'wb').write(png)
            x, y = (n % cols) * tw, (n // cols) * (th + 22); sheet.paste(Image.open(p), (x, y + 22)); d.text((x + 6, y + 5), f'{t:.1f}s', fill='black')
        f = os.path.join(a.out, f'sheet_{k // 12:02d}.jpg'); sheet.save(f, quality=82); sheets.append(f)
    lo = subprocess.run(['ffmpeg', '-i', a.video, '-af', 'ebur128=peak=true', '-f', 'null', '-'], capture_output=True, text=True).stderr
    I = re.findall(r'I:\s+(-?[\d.]+) LUFS', lo); P = re.findall(r'Peak:\s+(-?[\d.]+) dBFS', lo)
    lines = [f'video {a.video}: {dur:.2f}s {w}x{h}',
             f'loudness I={I[-1] if I else "?"} LUFS (target -14), true peak={P[-1] if P else "?"} dBTP (<= -1)',
             f'frozen stretches > 2.5 s: {len(frozen)}'] + [f'  {s:6.1f}-{e:6.1f}s ({e - s:.1f}s)' for s, e in frozen]
    if a.plan:
        plan = json.load(open(a.plan, encoding='utf-8')); lines.append('per scene (still seconds / length):')
        for n, sc in enumerate(plan['scenes']):
            m = (np.arange(len(still)) / 5 >= sc['start']) & (np.arange(len(still)) / 5 < sc['end'])
            lines.append(f'  {n:02d} {sc["start"]:6.1f}-{sc["end"]:6.1f}  still {still[m].sum() / 5:4.1f}s / {sc["end"] - sc["start"]:.1f}s  {sc.get("kind", "")}')
    lines.append('sheets: ' + ' '.join(sheets)); os.remove(os.path.join(a.out, '_f.png')) if sheets else None
    open(os.path.join(a.out, 'report.txt'), 'w').write('\n'.join(lines)); print('\n'.join(lines))


if __name__ == '__main__':
    main()
