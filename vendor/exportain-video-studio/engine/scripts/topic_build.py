#!/usr/bin/env python3
"""Topic project -> plan.json (+ vo.mp3 once the voice files are in) for make_video.py (Mode D).
  python3 topic_build.py --project P [--mode illustrated|captions] [--logo logo.png] [--brand X] [--url X] [--endcard 3]
P/narration.json [{id,text}]  one ElevenLabs take per scene, in order
P/board.json     [{kind,bg,keys,sfx}] same order (illustrated mode only)
P/durations.json {id: secs}   from ElevenLabs duration_secs -> plan + QA before the MP3s arrive
P/vo/<id>.mp3                 real takes (guide_voice_intake.py) -> exact timing + vo.mp3
P/scenes.js                   custom K.<kind> scenes for this topic, injected into the template
Scene i is exactly take i; beats = the moment each key word is spoken (char share, snapped to pause ends)."""
import argparse, json, os, re, subprocess, sys
BMV = os.environ.get('BMV', os.path.dirname(os.path.dirname(os.path.abspath(__file__))))  # this skill's root
sys.path.insert(0, os.path.join(BMV, 'scripts'))
from plan import silences, pick_icon, emphasis, ACCENT_BY_TAG
LEAD, GAP, TAIL = 0.6, 0.7, 0.6
dur = lambda p: float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', p],
                                     capture_output=True, text=True, check=True).stdout)


def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--project', required=True)
    ap.add_argument('--mode', default='illustrated', choices=['illustrated', 'captions'])
    for f in ['--logo', '--brand', '--url']: ap.add_argument(f, default='')
    ap.add_argument('--endcard', type=float, default=3.0)
    a = ap.parse_args(); D = os.path.abspath(a.project)
    nar = json.load(open(f'{D}/narration.json', encoding='utf-8'))
    est = json.load(open(f'{D}/durations.json')) if os.path.exists(f'{D}/durations.json') else {}
    ill = a.mode == 'illustrated'
    board = json.load(open(f'{D}/board.json', encoding='utf-8')) if ill else [{}] * len(nar)
    assert len(board) == len(nar), f'board {len(board)} vs narration {len(nar)}'
    vo = [f'{D}/vo/{n["id"]}.mp3' for n in nar]; real = all(map(os.path.exists, vo))
    if not real and any(n['id'] not in est for n in nar): sys.exit('need vo/<id>.mp3 for every segment or durations.json')
    t, rows, warn, prev = LEAD, [], 0, None
    for i, (n, b) in enumerate(zip(nar, board)):
        d = dur(vo[i]) if real else float(est[n['id']]); a0 = t
        m = re.match(r'\s*\[([^\]]+)\]', n['text']); tag = m.group(1).strip().lower() if m else None
        text = re.sub(r'\[[^\]]+\]', '', n['text']).strip(); N = len(text.replace(' ', '')) or 1
        ends = [a0 + e for _, e in silences(vo[i], -32, 0.12)] if real else []
        beats, pos, keys = [], 0, b.get('keys', [])
        for j, k in enumerate(keys):
            f = text.find(k, pos)
            if f < 0: warn += 1; print(f'  ! scene {i} ({n["id"]}): key "{k}" not found after char {pos}')
            frac = (j + 1) / (len(keys) + 1) if f < 0 else len(text[:f].replace(' ', '')) / N
            if f >= 0: pos = f + len(k)
            bt = a0 + 0.03 * d + 0.92 * d * frac
            near = [e for e in ends if a0 <= e < a0 + d and abs(e - bt) < 0.6]
            if near: bt = min(near, key=lambda e: abs(e - bt))
            if beats: bt = max(bt, beats[-1] + 0.3)
            beats.append(round(bt, 3))
        prev = pick_icon(text, prev, i)
        sc = {'id': n['id'], 'a0': round(a0, 3), 'dur': round(d, 3), 'text': text, 'tag': tag, 'icon': prev,
              'accent': ACCENT_BY_TAG.get(tag or '', '#26d07c'), 'emphasis': emphasis(text, a.brand)}
        if ill: sc.update(kind=b['kind'], beats=beats, **{k: b[k] for k in ('bg', 'sfx') if k in b})
        rows.append(sc); t = a0 + d + GAP
    V = round(t - GAP + TAIL, 3)
    for i, sc in enumerate(rows):  # contiguous scenes: cut in the middle of each gap
        sc['start'] = 0.0 if i == 0 else round(sc['a0'] - GAP / 2, 3)
        sc['end'] = V if i == len(rows) - 1 else round(rows[i + 1]['a0'] - GAP / 2, 3)
    end = a.endcard if a.logo else 0.0
    plan = dict(voice_duration=V, endcard=end, total=round(V + end, 3), brand=a.brand, url=a.url, logo=a.logo,
                tagline='', intro=False if ill else bool(a.logo), pauses_found=0, scenes=rows)
    tpl = open(os.path.join(BMV, 'templates', 'illustrated.html' if ill else 'timeline.html'), encoding='utf-8').read()
    if ill and os.path.exists(f'{D}/scenes.js'):
        tpl = tpl.replace('// ---------- engine ----------', open(f'{D}/scenes.js', encoding='utf-8').read() + '\n// ---------- engine ----------')
    if not a.logo: tpl = tpl.replace('</style>', '#badge{display:none!important}</style>', 1)
    open(f'{D}/scenes.html', 'w', encoding='utf-8').write(tpl); plan['template'] = f'{D}/scenes.html'
    if real:
        ins = sum((['-i', p] for p in vo), [])
        fc = ''.join(f'[{i}:a]aresample=48000,aformat=channel_layouts=mono,adelay={int(r["a0"]*1000)}[s{i}];' for i, r in enumerate(rows))
        fc += ''.join(f'[s{i}]' for i in range(len(rows))) + f'amix=inputs={len(rows)}:normalize=0,apad=whole_dur={V},atrim=0:{V}[o]'
        subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', *ins, '-filter_complex', fc, '-map', '[o]', '-c:a', 'libmp3lame', '-q:a', '2', f'{D}/vo.mp3'], check=True)
    json.dump(plan, open(f'{D}/plan.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print(f'{len(rows)} scenes, {V:.1f}s voice ({"real takes -> vo.mp3" if real else "estimated durations"}), key warnings: {warn}')
    for i, r in enumerate(rows):
        print(f'  {i:02d} {r["start"]:6.2f}-{r["end"]:6.2f} {r.get("kind", r["icon"]):14} ' + ' '.join(f'{b:.2f}' for b in r.get('beats', [])) + f'  | {r["text"][:40]}')
        cps = len(r['text'].replace(' ', '')) / r['dur']; fast = '  <-- FAST: slow it (atempo 0.94) or trim words' if cps > 15 else ''
        print(f'      still: {round(r["end"] - 0.25, 2)}   pace {cps:.1f} chars/s{fast}')


if __name__ == '__main__':
    main()
