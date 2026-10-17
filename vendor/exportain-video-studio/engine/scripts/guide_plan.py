#!/usr/bin/env python3
"""Tutorial (guide) mode: narration.json + screenplay.py + segment durations -> plan.json + segments.json.
  python3 guide_plan.py --project <dir> [--logo logo.png]
<dir> holds narration.json [{id,title,text}], screenplay.py (INTRO, STEPS, OUTRO, optional CONFIG),
durations.json {id: secs} (from ElevenLabs duration_secs) and, once downloaded, vo/<id>.mp3.
Real vo files win over durations.json; beats then snap to real pause ends (word onsets)."""
import argparse, importlib.util, json, os, re, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from plan import silences
GAP, LEAD = 0.8, 0.5

def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--project', required=True); ap.add_argument('--logo', default='')
    a = ap.parse_args(); D = os.path.abspath(a.project)
    spec = importlib.util.spec_from_file_location('screenplay', os.path.join(D, 'screenplay.py')); sp = importlib.util.module_from_spec(spec); spec.loader.exec_module(sp)
    cfg = getattr(sp, 'CONFIG', {})
    nar = json.load(open(f'{D}/narration.json', encoding='utf-8'))
    est = json.load(open(f'{D}/durations.json')) if os.path.exists(f'{D}/durations.json') else {}
    specs = [sp.INTRO] + sp.STEPS + [sp.OUTRO]
    assert len(specs) == len(nar), f'{len(specs)} scenes vs {len(nar)} narration segments'
    def dur(i):
        p = f'{D}/vo/{nar[i]["id"]}.mp3'
        if os.path.exists(p):
            return float(subprocess.run(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',p],capture_output=True,text=True).stdout), p
        return est[nar[i]['id']], None
    scenes, segs, t, warn = [], [], 0.0, 0
    for i, s in enumerate(specs):
        d, path = dur(i); a0 = t + (LEAD if i == 0 else 0)
        text = re.sub(r'\[[^\]]+\]', '', nar[i]['text']).strip(); n = len(text.replace(' ', '')) or 1
        ends = [a0 + e for _, e in silences(path, -32, 0.12)] if path else []
        beats, pos = [], 0
        for j, c in enumerate(s.get('callouts', [])):
            f = text.find(c['k'], pos)
            if f < 0: print(f'  ! scene {i} ({nar[i]["id"]}): key not found after pos {pos}: {c["k"]}'); warn += 1
            else: pos = f + len(c['k'])
            frac = (j + 1) / (len(s['callouts']) + 1) if f < 0 else len(text[:f].replace(' ', '')) / n
            bt = a0 + 0.03 * d + 0.92 * d * frac
            near = [e for e in ends if a0 <= e < a0 + d and abs(e - bt) < 0.6]
            if near: bt = min(near, key=lambda e: abs(e - bt))
            if beats: bt = max(bt, beats[-1] + 0.45)
            beats.append(round(bt, 3))
        sc = dict(s); sc.setdefault('sfx', ['click'])
        sc.update(start=round(max(0, a0 - LEAD), 3), audio=round(a0, 3), dur=round(d, 3), beats=beats, text=text)
        scenes.append(sc); segs.append((path, a0, d)); t = a0 + d + GAP
    for i in range(len(scenes) - 1): scenes[i]['end'] = scenes[i + 1]['start']
    total = round(t + 0.5, 3); scenes[-1]['end'] = total
    logo = os.path.abspath(a.logo) if a.logo else cfg.get('logo', '')
    plan = dict(template='guide.html', logo=logo, intro=False, endcard=0, voice_duration=total, total=total, scenes=scenes)
    for k_cfg, k_plan in [('lang','lang'),('search','search'),('menu','menu'),('steps','steps'),('url','url'),('add_label','addLabel'),('badges','badges')]:
        if k_cfg in cfg: plan[k_plan] = cfg[k_cfg]
    plan.setdefault('steps', len(sp.STEPS))
    json.dump(plan, open(f'{D}/plan.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    json.dump(segs, open(f'{D}/segments.json', 'w'))
    print(f'{len(scenes)} scenes, {total/60:.1f} min, real audio {sum(1 for x in segs if x[0])}/{len(segs)}, key warnings {warn}')

if __name__ == '__main__': main()
