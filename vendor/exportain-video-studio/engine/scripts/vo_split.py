#!/usr/bin/env python3
"""Split ONE long voiceover (all segments read in one ElevenLabs prompt) into <project>/vo/<id>.mp3.
  python3 vo_split.py --project P --voice full.mp3 [--anchor-from 1 --anchor-to -1] [--tempo 0.94]
ElevenLabs v4 often IGNORES <break> tags, so gaps between segments can be only ~0.5 s and are not the longest
pauses. Two-pass alignment:
 1. Dynamic programming over every pause (>=0.3 s at -35 dB): pick N-1 boundaries so each segment's length
    matches its character share (global speaking rate), with a small bonus for longer pauses.
 2. Anchor refinement: segments that start with the same spoken word ("Step …", "ধাপ …") sound alike for the
    first 0.42 s. A log-mel template is averaged from confident boundaries, and each boundary between
    --anchor-from and --anchor-to (segment indices that start with the anchor word) moves to the pause within
    ±4 s whose following audio best matches the template.
Prints duration vs expected and the similarity per boundary; review lines marked CHECK.
--tempo <1 slows speech without pitch change (0.94 = 6 % slower, good for tutorials)."""
import argparse, json, os, re, subprocess, sys
import numpy as np, scipy.io.wavfile as wf
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); from plan import silences
ap = argparse.ArgumentParser(); ap.add_argument('--project', required=True); ap.add_argument('--voice', required=True)
ap.add_argument('--anchor-from', type=int, default=1); ap.add_argument('--anchor-to', type=int, default=-1)
ap.add_argument('--tempo', type=float, default=1.0); ap.add_argument('--no-refine', action='store_true'); a = ap.parse_args()
D = a.project; nar = json.load(open(f'{D}/narration.json', encoding='utf-8')); N = len(nar)
chars = [len(re.sub(r'\[[^\]]+\]', '', x['text'])) for x in nar]
dur = lambda p: float(subprocess.run(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',p],capture_output=True,text=True).stdout)
T = dur(a.voice); r = T / sum(chars)
sil = [(s, e) for s, e in silences(a.voice, -35, 0.3) if s > 1 and e < T - 1]
pos = [0.0] + [(s+e)/2 for s, e in sil] + [T]; plen = [0] + [e-s for s, e in sil] + [0]; M = len(pos)
INF = 1e18; dp = [[INF]*M for _ in range(N+1)]; bk = [[-1]*M for _ in range(N+1)]; dp[0][0] = 0
for j in range(1, N+1):
    for b in (range(1, M-1) if j < N else [M-1]):
        for p in range(b):
            if dp[j-1][p] >= INF: continue
            e = (pos[b]-pos[p]) / (chars[j-1]*r); v = dp[j-1][p] + 40*(e-1)**2 - (6*plen[b] if j < N else 0)
            if v < dp[j][b]: dp[j][b], bk[j][b] = v, p
b = M-1; idx = []
for j in range(N, 0, -1): b = bk[j][b]; idx.append(b)
idx = idx[::-1][1:]; bnd = [pos[i] for i in idx]                       # N-1 boundary times (pause middles)
ends = {round((s+e)/2, 3): e for s, e in sil}
# ---- anchor refinement (log-mel similarity of the first 0.42 s after each boundary)
tmp = '/tmp/_vo16.wav'; subprocess.run(['ffmpeg','-y','-loglevel','error','-i',a.voice,'-ac','1','-ar','16000',tmp],check=True)
sr, x = wf.read(tmp); x = x.astype(np.float32)/32768; nf, hop = 400, 160
fr = np.lib.stride_tricks.sliding_window_view(x, nf)[::hop]*np.hanning(nf); S = np.abs(np.fft.rfft(fr, axis=1))**2
mel = lambda f: 2595*np.log10(1+f/700); im = lambda m: 700*(10**(m/2595)-1)
bins = np.floor((nf+1)*im(np.linspace(mel(80), mel(7600), 42))/sr).astype(int); fb = np.zeros((40, S.shape[1]))
for i in range(40):
    p0, p1, p2 = bins[i], bins[i+1], bins[i+2]; fb[i, p0:p1] = np.linspace(0,1,p1-p0,endpoint=False); fb[i, p1:p2] = np.linspace(1,0,p2-p1,endpoint=False)
LM = np.log(S@fb.T + 1e-8)
def feat(t):
    i = int(t*100); v = LM[i:i+42].copy(); v -= v.mean(0); return (v/(np.linalg.norm(v)+1e-9)).ravel()
onset = lambda m: min((e for s, e in sil), key=lambda e: abs(e-m))
ato = a.anchor_to if a.anchor_to > 0 else N + a.anchor_to          # last segment index that starts with the anchor
anch = [k for k in range(N-1) if a.anchor_from <= k+1 <= ato]        # boundary k starts segment k+1
if anch and not a.no_refine:
    errs = sorted(anch, key=lambda k: abs((bnd[k]-(bnd[k-1] if k else 0))/(chars[k]*r)-1))[:max(3, len(anch)//3)]
    tm = np.mean([feat(onset(bnd[k])) for k in errs], axis=0)
    for k in anch:
        lo = bnd[k-1] if k else 0; hi = bnd[k+1] if k+1 < len(bnd) else T
        cands = [m for m in pos[1:-1] if abs(m-bnd[k]) <= 4 and lo < m < hi]
        best = max(cands, key=lambda m: feat(onset(m))@tm)
        if feat(onset(best))@tm > feat(onset(bnd[k]))@tm + 0.15: bnd[k] = best
cuts = [0.0] + bnd + [T]; os.makedirs(f'{D}/vo', exist_ok=True)
for i, s in enumerate(nar):
    out = f'{D}/vo/{s["id"]}.mp3'; af = ['-af', f'atempo={a.tempo}'] if a.tempo != 1 else []
    subprocess.run(['ffmpeg','-y','-loglevel','error','-ss',f'{cuts[i]:.3f}','-to',f'{cuts[i+1]:.3f}','-i',a.voice,*af,'-ar','48000','-c:a','libmp3lame','-q:a','2',out],check=True)
    d = cuts[i+1]-cuts[i]; e = d/(chars[i]*r); sim = feat(onset(cuts[i]))@tm if (i and anch and not a.no_refine) else float('nan')
    print(f'{s["id"]:22} start {cuts[i]:7.2f}  {d:6.2f}s  ratio {e:.2f}  sim {sim:.2f} {"<-- CHECK" if abs(e-1) > .2 else ""}')
print('wrote', N, 'files; now run guide_plan.py')
