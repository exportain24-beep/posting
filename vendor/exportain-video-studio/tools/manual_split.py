"""Cut full.mp3 at times YOU choose (when split_check shows BAD boundaries, e.g. ads where ElevenLabs ignored
<break> tags). First list candidate pauses, listen/compare with the text, then cut.
  python3 manual_split.py <project_dir> full.mp3 --pauses            # list pauses (>=0.18 s) with times
  python3 manual_split.py <project_dir> full.mp3 0 3.42 7.9 ...      # N cut times (first must be 0.0) -> vo/<id>.mp3
Tip: never start a cut later than the first word (the seller-ad hook once lost "এক্সপোর্ট কোর্স শেষ" that way);
put each cut in the middle of a pause, ~0.1 s before the next phrase."""
import sys,os,json,subprocess,numpy as np
P,V=sys.argv[1],sys.argv[2]
a=np.frombuffer(subprocess.run(['ffmpeg','-v','error','-i',V,'-ac','1','-ar','8000','-f','s16le','-'],capture_output=True).stdout,np.int16).astype(float)
dur=len(a)/8000
if sys.argv[3:]==['--pauses']:
    env=np.sqrt(np.convolve(a*a,np.ones(160)/160,'same')); thr=max(60,np.percentile(env,20)*1.5)
    q=env<thr; i=0; out=[]
    while i<len(q):
        if q[i]:
            j=i
            while j<len(q) and q[j]: j+=1
            if (j-i)/8000>=.18: out.append((i/8000,j/8000))
            i=j
        else: i+=1
    print(f'duration {dur:.2f}s; pauses (start-end, mid):')
    for s,e in out: print(f'  {s:7.2f}-{e:7.2f}  mid {(s+e)/2:7.2f}  ({e-s:.2f}s)')
    sys.exit()
cuts=[float(x) for x in sys.argv[3:]]+[dur]
n=json.load(open(os.path.join(P,'narration.json'),encoding='utf-8'))
assert len(cuts)-1==len(n), f'need {len(n)} cut times (got {len(cuts)-1})'
os.makedirs(os.path.join(P,'vo'),exist_ok=True)
for i,x in enumerate(n):
    o=os.path.join(P,'vo',x['id']+'.mp3')
    subprocess.run(['ffmpeg','-y','-loglevel','error','-ss',f'{cuts[i]:.3f}','-to',f'{cuts[i+1]:.3f}','-i',V,'-ar','48000','-c:a','libmp3lame','-q:a','2',o],check=True)
    print(f"{x['id']:<16} {cuts[i]:7.2f} {cuts[i+1]-cuts[i]:6.2f}s  {x['text'][:40]}")
