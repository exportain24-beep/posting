"""OPTIONAL (automation / when you have an ElevenLabs API key): voice every narration scene separately with the
ElevenLabs API, straight into <project>/vo/<id>.mp3 — no splitting needed, boundaries are perfect.
  export ELEVENLABS_API_KEY=...            (never print it, never commit it)
  python3 tts_scenes.py <project_dir> [--model eleven_v4] [--voice 3XjJ1C8taYP9CHnHKmK5]
Defaults = the client's locked voice: Debashish (3XjJ1C8taYP9CHnHKmK5), Bangla. Manual recordings used model
eleven_v4 with speed 1.00, stability 0.50, similarity 0.75 (file names "…sp100_s50_sb75_v4.mp3"); the automation
repo uses eleven_v4_turbo — pass --model to match whatever the client has locked for that pipeline.
Audio tags like [curious] / [warmly] at the start of a scene are kept (v4 models read them as delivery hints).
Note: the sandbox network may block api.elevenlabs.io; then the user records the one-prompt file manually instead."""
import argparse, json, os, sys, time, urllib.request, urllib.error
ap = argparse.ArgumentParser(); ap.add_argument('project'); ap.add_argument('--model', default='eleven_v4')
ap.add_argument('--voice', default='3XjJ1C8taYP9CHnHKmK5'); ap.add_argument('--stability', type=float, default=.5)
ap.add_argument('--similarity', type=float, default=.75); ap.add_argument('--speed', type=float, default=1.0)
ap.add_argument('--only', nargs='*', help='scene ids to (re)generate'); a = ap.parse_args()
key = os.environ.get('ELEVENLABS_API_KEY') or sys.exit('set ELEVENLABS_API_KEY')
n = json.load(open(os.path.join(a.project, 'narration.json'), encoding='utf-8'))
os.makedirs(os.path.join(a.project, 'vo'), exist_ok=True)
prev = None
for x in n:
    if a.only and x['id'] not in a.only: prev = x['text']; continue
    body = {'text': x['text'], 'model_id': a.model, 'language_code': 'bn',
            'voice_settings': {'stability': a.stability, 'similarity_boost': a.similarity, 'speed': a.speed}}
    if prev: body['previous_text'] = prev[-300:]
    req = urllib.request.Request(f'https://api.elevenlabs.io/v1/text-to-speech/{a.voice}?output_format=mp3_44100_128',
                                 data=json.dumps(body).encode(), method='POST',
                                 headers={'xi-api-key': key, 'Content-Type': 'application/json', 'Accept': 'audio/mpeg'})
    for attempt in range(3):
        try:
            data = urllib.request.urlopen(req, timeout=120).read(); break
        except urllib.error.HTTPError as e:
            msg = e.read()[:300]
            if e.code == 400 and b'language_code' in msg: body.pop('language_code'); req.data = json.dumps(body).encode(); continue
            if attempt == 2: sys.exit(f"{x['id']}: HTTP {e.code} {msg}")
            time.sleep(3)
    open(os.path.join(a.project, 'vo', x['id'] + '.mp3'), 'wb').write(data)
    print(f"{x['id']:<16} {len(data)//1024} KB"); prev = x['text']
print('done -> vo/*.mp3 ; next: bash build.sh (topic_build makes vo.mp3 from the scene files)')
