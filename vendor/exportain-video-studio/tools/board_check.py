"""Validate board.json against narration.json and the scene JS before building.
Usage: python3 board_check.py <project_dir>
Checks: same count/order, every key is an exact substring in increasing order, one sfx per key,
known bg + sfx names, every kind defined as K.<kind> somewhere in js/*.js."""
import json,sys,os,re,glob
P=sys.argv[1] if len(sys.argv)>1 else '.'
n=json.load(open(os.path.join(P,'narration.json'),encoding='utf-8'))
b=json.load(open(os.path.join(P,'board.json'),encoding='utf-8'))
BG={'e_mint','e_lime','e_sea','e_gold','e_sky','e_forest','e_deep'}
SFX={'boom','bubble','chime','click','ding','pop','pop2','rise','riser','shutter','sparkle','swoosh','tick','whoosh'}
js=''.join(open(f,encoding='utf-8').read() for f in glob.glob(os.path.join(P,'js','*.js')))
err=[]
if len(n)!=len(b): err.append(f'count: narration {len(n)} vs board {len(b)}')
for i,(x,e) in enumerate(zip(n,b)):
    t=x['text'];pos=0
    for k in e['keys']:
        j=t.find(k,pos)
        if j<0: err.append(f"[{i} {e['kind']}] key not found in order: {k!r}")
        else: pos=j+len(k)
    if len(e.get('sfx',[]))!=len(e['keys']): err.append(f"[{i} {e['kind']}] sfx count {len(e.get('sfx',[]))} != keys {len(e['keys'])}")
    for s in e.get('sfx',[]):
        if s not in SFX: err.append(f"[{i}] unknown sfx {s}")
    if e.get('bg') not in BG and not str(e.get('bg','')).startswith('c_'): err.append(f"[{i}] unknown bg {e.get('bg')}")
    if not re.search(r'K\.'+re.escape(e['kind'])+r'\s*=',js): err.append(f"[{i}] K.{e['kind']} not defined in js/")
print('\n'.join(err) if err else f'board OK ({len(b)} scenes)')
sys.exit(1 if err else 0)
