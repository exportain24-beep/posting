#!/usr/bin/env python3
"""Map downloaded ElevenLabs MP3s to narration segments -> <project>/vo/<id>.mp3
  python3 guide_voice_intake.py --project <dir> <files or dirs...>
ElevenLabs Flow downloads are named New_tts_node.mp3, New_tts_node1.mp3 ... in GENERATION order, but the
numbering base varies (sometimes 'New_tts_node' = 1st, node1 = 2nd; sometimes node1 = 1st). For every file the
candidates nar[N-1] / nar[N] (no number -> nar[0]) are compared with durations.json and the closer one wins.
Upload folders often contain older files with the same names: pass only this job's files."""
import argparse, glob, json, os, re, shutil, subprocess
ap = argparse.ArgumentParser(); ap.add_argument('--project', required=True); ap.add_argument('files', nargs='+'); a = ap.parse_args()
D = a.project; nar = json.load(open(f'{D}/narration.json', encoding='utf-8')); est = json.load(open(f'{D}/durations.json'))
dur = lambda p: float(subprocess.run(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',p],capture_output=True,text=True).stdout)
files = []
for x in a.files: files += sorted(glob.glob(os.path.join(x, '*.mp3'))) if os.path.isdir(x) else [x]
os.makedirs(f'{D}/vo', exist_ok=True); bad = 0
for f in files:
    d = dur(f); m = re.search(r'node[_ ]?(\d+)', os.path.basename(f), re.I)
    cands = [0] if not m else [i for i in (int(m.group(1)) - 1, int(m.group(1))) if 0 <= i < len(nar)]
    if not cands: cands = range(len(nar))
    i = min(cands, key=lambda i: abs(est[nar[i]['id']] - d)); err = abs(est[nar[i]['id']] - d)
    flag = '' if err < 0.3 else '   <-- CHECK (duration mismatch)'; bad += bool(flag)
    shutil.copy(f, f'{D}/vo/{nar[i]["id"]}.mp3'); print(f'{nar[i]["id"]:24} <- {os.path.basename(f)}  {d:.2f}s vs {est[nar[i]["id"]]}{flag}')
miss = [n['id'] for n in nar if not os.path.exists(f'{D}/vo/{n["id"]}.mp3')]
print('missing:', miss or 'none', '| mismatches:', bad)
