#!/usr/bin/env python3
"""Shorts voice job (GitHub Actions):
   shorts-content:voice/<EP>/narration.json  ->  shorts-audio:<EP>/vo/<id>.mp3 + durations.json

LOCKED (owner): voice Debashish 3XjJ1C8taYP9CHnHKmK5, model eleven_v4_turbo. Language comes from the episode name
(sh-0001-bn-… = Bangla, sh-0002-en-… = English) and the text is checked against it, so nothing else can be voiced.
Unchanged takes are never generated twice (no double charge).

  EPISODE=sh-0001-bn-slug [TEST_TONE=1] python scripts/shorts_voice.py
"""
import json, os, shutil, subprocess, sys, time, urllib.parse
from datetime import datetime, timedelta, timezone

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import TAG, branch_dir, http, note, push_branch, redact, secret, summary, text_hash
from shorts_common import BR, SCFG, SHORT_ID, is_bangla, is_english, short_lang, validate_narration

LOCKED_VOICE_ID = "3XjJ1C8taYP9CHnHKmK5"   # Debashish
LOCKED_MODEL_ID = "eleven_v4_turbo"


def check_lock():
    if SCFG.get("voice_id") != LOCKED_VOICE_ID or SCFG.get("tts_model_id") != LOCKED_MODEL_ID:
        raise RuntimeError("LOCKED: shorts/config.json voice/model changed — refusing to generate")


def tts(text, lang, out, previous_text=None):
    check_lock()
    if (lang == "bn" and not is_bangla(text)) or (lang == "en" and not is_english(text)):
        raise RuntimeError(f"LOCKED: text does not match the Short's language ({lang}) — refusing to generate")
    key = secret("ELEVENLABS_API_KEY")
    if not key:
        raise RuntimeError("ELEVENLABS_API_KEY is not set in the 'production' environment")
    url = (f"https://api.elevenlabs.io/v1/text-to-speech/{LOCKED_VOICE_ID}"
           f"?output_format={urllib.parse.quote(SCFG['tts_output_format'])}")
    body = {"text": text, "model_id": LOCKED_MODEL_ID, "language_code": lang,
            "voice_settings": SCFG.get("voice_settings", {"stability": 0.5, "similarity_boost": 0.75, "speed": 1.0})}
    if previous_text:
        body["previous_text"] = previous_text[-300:]
    audio = http("POST", url, {"xi-api-key": key, "Accept": "audio/mpeg"}, body, timeout=180)
    if len(audio) < 2000:
        raise RuntimeError("ElevenLabs returned an empty audio file")
    open(out, "wb").write(audio)


def tone(text, out):
    secs = max(1.0, len(TAG.sub("", text)) / 14.0)
    subprocess.check_call(["ffmpeg", "-y", "-loglevel", "error", "-f", "lavfi", "-i",
                           f"sine=frequency=330:duration={secs:.2f}", "-af", "volume=0.05",
                           "-c:a", "libmp3lame", "-b:a", "128k", out])


def duration(path):
    return float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                                          "-of", "default=nw=1:nk=1", path]).decode())


def save(audio, d, man, durs, nar, ep):
    man["updated"] = datetime.now(timezone.utc).isoformat()
    json.dump(man, open(os.path.join(d, "manifest.json"), "w"), indent=1)
    json.dump(durs, open(os.path.join(d, "durations.json"), "w"), indent=1)
    json.dump(nar, open(os.path.join(d, "narration.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    push_branch(audio, BR["audio"], f"shorts voice {ep}", squash=True)


def main():
    ep = os.environ.get("EPISODE", "").strip()
    test = os.environ.get("TEST_TONE") == "1"
    lang = short_lang(ep)
    if not SHORT_ID.fullmatch(ep) or not lang:
        note("error", f"shorts voice: bad episode name '{ep}' (want sh-0001-bn-slug or sh-0001-en-slug)"); return 1
    content = branch_dir(BR["content"])
    src = os.path.join(content, "voice", ep, "narration.json")
    if not os.path.isfile(src):
        note("error", f"shorts voice {ep}: {BR['content']}:voice/{ep}/narration.json not found"); return 1
    try:
        nar = json.load(open(src, encoding="utf-8"))
    except Exception as e:
        note("error", f"shorts voice {ep}: narration.json is not valid JSON ({e})"); return 1
    errs = validate_narration(nar, lang)
    if errs:
        note("error", f"shorts voice {ep}: " + "; ".join(errs)); return 1

    audio = branch_dir(BR["audio"])
    cutoff = datetime.now(timezone.utc) - timedelta(days=SCFG["keep_audio_days"])
    for m in os.listdir(audio):
        mf = os.path.join(audio, m, "manifest.json")
        if os.path.isfile(mf):
            try:
                if datetime.fromisoformat(json.load(open(mf))["updated"]) < cutoff and m != ep:
                    shutil.rmtree(os.path.join(audio, m))
            except Exception:
                shutil.rmtree(os.path.join(audio, m), ignore_errors=True)

    d = os.path.join(audio, ep)
    os.makedirs(os.path.join(d, "vo"), exist_ok=True)
    mpath = os.path.join(d, "manifest.json")
    man = json.load(open(mpath)) if os.path.isfile(mpath) else {"takes": {}}
    kind = "tone" if test else f"{LOCKED_MODEL_ID}:{LOCKED_VOICE_ID}:{lang}:{json.dumps(SCFG.get('voice_settings'), sort_keys=True)}"
    made = reused = chars = 0
    durs = {}
    for i, t in enumerate(nar):
        tid, text = t["id"], t["text"]
        out = os.path.join(d, "vo", f"{tid}.mp3")
        h = text_hash(text + "|" + kind)
        if os.path.isfile(out) and man["takes"].get(tid) == h:
            reused += 1
        else:
            try:
                if test:
                    tone(text, out)
                else:
                    tts(text, lang, out, nar[i - 1]["text"] if i else None)
            except Exception as e:
                note("error", f"shorts voice {ep} take {tid}: {redact(e)}")
                save(audio, d, man, durs, nar, ep)
                return 1
            man["takes"][tid] = h
            made += 1
            chars += len(TAG.sub("", text))
            time.sleep(0.4)
        durs[tid] = round(duration(out), 3)
    keep = {t["id"] for t in nar}
    for f in os.listdir(os.path.join(d, "vo")):
        if f[:-4] not in keep:
            os.remove(os.path.join(d, "vo", f))
    man["takes"] = {k: v for k, v in man["takes"].items() if k in keep}
    save(audio, d, man, durs, nar, ep)
    total = sum(durs.values())
    note("notice", f"shorts voice {ep}: OK {'TEST TONE ' if test else ''}{made} new take(s), {reused} reused, "
                   f"{chars} characters charged, {len(durs)} takes, {total:.1f}s of speech")
    summary(f"### Shorts voice `{ep}`\n{made} new, {reused} reused, {chars} characters, {total:.1f} s of speech.")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as e:
        note("error", f"shorts voice failed: {redact(e)}")
        sys.exit(1)
