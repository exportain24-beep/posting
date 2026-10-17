"""Split the one-prompt MP3 and verify every scene boundary sits in silence.
Usage: python3 split_check.py <project_dir> <full.mp3>"""
import sys,subprocess,os,re,numpy as np
P,V=sys.argv[1],sys.argv[2]; SK=os.environ.get('SK') or os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','engine')
out=subprocess.run(['python3',f'{SK}/scripts/vo_split.py','--project',P,'--voice',V,'--no-refine'],capture_output=True,text=True).stdout
print(out)
st=[float(m) for m in re.findall(r'start\s+([\d.]+)',out)]
a=np.frombuffer(subprocess.run(['ffmpeg','-v','error','-i',V,'-ac','1','-ar','8000','-f','s16le','-'],capture_output=True).stdout,np.int16).astype(float)
env=np.sqrt(np.convolve(a*a,np.ones(400)/400,'same'))
vals=[round(env[int(t*8000)]) for t in st[1:]]
print('boundary RMS (want ~1-5):',vals)
bad=[i+1 for i,v in enumerate(vals) if v>40]
print('BAD boundaries (scene index):',bad if bad else 'none')
