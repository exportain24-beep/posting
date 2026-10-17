"""Map the frozen stretches reported by finish.sh/review to scenes, with key times, and suggest the fix.
Usage: python3 frozen_map.py <project_dir> [finish.log]"""
import json,sys,os,re
P=sys.argv[1]; L=sys.argv[2] if len(sys.argv)>2 else os.path.join(P,'finish.log')
pl=json.load(open(os.path.join(P,'plan.json'),encoding='utf-8'))['scenes']
txt=open(L,encoding='utf-8',errors='ignore').read()
fr=[(float(a),float(b)) for a,b in re.findall(r'^\s+([\d.]+)-\s*([\d.]+)s',txt,re.M)]
if not fr: print('no frozen stretches'); sys.exit()
for a,b in fr:
    for s in pl:
        if s['start']<=a<s['end']:
            ks=[round(k-s['start'],2) for k in s.get('beats',[])]
            print(f"{a:.1f}-{b:.1f}s  ->  {s['kind']}  (scene {s['start']:.1f}-{s['end']:.1f}; local {a-s['start']:.1f}-{b-s['start']:.1f}s; key times {ks})")
            print("   fix: reveal something inside that local window (e.g. popG(...,Math.min(bt(k)-.3, <early>)...)) and add idle motion\n"
                  "        after it appears: if(lt>X)T(q('id'),{y:Math.sin(lt*2)*10,o:1}); then build, re-render.")
