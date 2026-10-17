#!/usr/bin/env python3
"""Tutorial mode final assembly (run after the silent render exists):
  python3 guide_finish.py --project <dir> --name Exportain_Provider_Guide [--music bg.mp3] [--music-db -28]
         [--sfx-db -9] [--split-scene 11] [--max-mb 30]
Builds vo_full.wav (every segment at its planned start), sfx.wav, the ducked mix, muxes with out/silent_16x9.mp4
(-c copy) and writes share copies. If the crf26 share file is over --max-mb it is split at the start of
--split-scene (a step number n; default = the step nearest the middle) into Part1/Part2.
Long steps here can exceed a 10-min shell limit: run with setsid nohup ... & and poll."""
import argparse, json, os, subprocess, sys
S = os.path.dirname(os.path.abspath(__file__))
ap = argparse.ArgumentParser(); ap.add_argument('--project', required=True); ap.add_argument('--name', required=True)
ap.add_argument('--music'); ap.add_argument('--music-db', default='-28'); ap.add_argument('--sfx-db', default='-9')
ap.add_argument('--split-scene', type=int); ap.add_argument('--max-mb', type=float, default=30); a = ap.parse_args()
D = os.path.abspath(a.project); O = f'{D}/out'; os.makedirs(O, exist_ok=True)
plan = json.load(open(f'{D}/plan.json', encoding='utf-8')); T = plan['total']; segs = json.load(open(f'{D}/segments.json'))
run = lambda c: subprocess.run(c, check=True)
cmd = ['ffmpeg','-y','-loglevel','error']
for p, a0, d in segs: cmd += ['-i', p]
fc = ''.join(f'[{i}:a]aresample=48000,aformat=channel_layouts=stereo,adelay={int(a0*1000)}|{int(a0*1000)}[v{i}];' for i,(p,a0,d) in enumerate(segs))
fc += ''.join(f'[v{i}]' for i in range(len(segs))) + f'amix=inputs={len(segs)}:normalize=0:duration=longest,apad=whole_dur={T},atrim=0:{T}[o]'
run(cmd + ['-filter_complex', fc, '-map', '[o]', f'{O}/vo_full.wav'])
run([sys.executable, f'{S}/sfx.py', '--plan', f'{D}/plan.json', '--out', f'{O}/sfx.wav'])
mus = ['--music', a.music] if a.music else []
run([sys.executable, f'{S}/mix_audio.py', '--voice', f'{O}/vo_full.wav', *mus, '--total', str(T), '--music-db', a.music_db,
     '--sfx', f'{O}/sfx.wav', '--sfx-db', a.sfx_db, '--out', f'{O}/mix.m4a'])
run(['ffmpeg','-y','-loglevel','error','-i',f'{O}/silent_16x9.mp4','-i',f'{O}/mix.m4a','-map','0:v','-map','1:a','-c','copy','-shortest','-movflags','+faststart',f'{O}/master.mp4'])
enc = lambda extra, out: run(['ffmpeg','-y','-loglevel','error',*extra,'-c:v','libx264','-preset','medium','-crf','26','-pix_fmt','yuv420p','-c:a','aac','-b:a','128k','-movflags','+faststart',out])
full = f'{O}/{a.name}.mp4'; enc(['-i', f'{O}/master.mp4'], full)
if os.path.getsize(full) / 1e6 > a.max_mb:
    sc = plan['scenes']; steps = [s for s in sc if s.get('n')]
    cut = next((s['start'] for s in sc if s.get('n') == a.split_scene), None) if a.split_scene else min((abs(s['start'] - T/2), s['start']) for s in steps)[1]
    enc(['-i', f'{O}/master.mp4', '-t', str(cut)], f'{O}/{a.name}_Part1.mp4'); enc(['-ss', str(cut), '-i', f'{O}/master.mp4'], f'{O}/{a.name}_Part2.mp4')
    print(f'split at {cut:.2f}s'); os.remove(full)
for f in sorted(os.listdir(O)):
    if f.startswith(a.name): print(f, round(os.path.getsize(f'{O}/{f}')/1e6, 1), 'MB')
