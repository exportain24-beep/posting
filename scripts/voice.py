#!/usr/bin/env python3
"""Voice job (GitHub Actions): content:voice/<EP>/narration.json  ->  audio:<EP>/vo/<id>.mp3 + durations.json

One ElevenLabs take per scene, in order, exactly the files the bangla-motion-video skill expects.
A take whose text is unchanged is never generated twice (no double charge).

  EPISODE=<slug> [TEST_TONE=1] python scripts/voice.py
"""
import json, os, re, shutil, subprocess, sys, time, urllib.parse
from datetime import datetime, timedelta, timezone

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import (CFG, SLUG, TAG, branch_dir, is_bangla, http, log, note, push_branch, redact, secret, summary,
                    text_hash, validate_narration)


# LOCKED by the owner: only this voice, only this model, only Bangla. Not read from config, not overridable.
LOCKED_VOICE_ID = "3XjJ1C8taYP9CHnHKmK5"   # Debashish
LOCKED_MODEL_ID = "eleven_v4_turbo"
LOCKED_LANGUAGE = "bn"


def check_lock():
    for k, want in (("voice_id", LOCKED_VOICE_ID), ("tts_model_id", LOCKED_MODEL_ID), ("tts_language_code", LOCKED_LANGUAGE)):
        if CFG.get(k) != want:
            raise RuntimeError(f"LOCKED: config {k} must be {want} — refusing to generate")


def tts(text, out):
    check_lock()
    if not is_bangla(text):
        raise RuntimeError("LOCKED: text is not Bangla — refusing to generate")
    key = secret("ELEVENLABS_API_KEY")
    if not key:
        raise RuntimeError("ELEVENLABS_API_KEY is not set in the 'production' environment")
    url = (f"https://api.elevenlabs.io/v1/text-to-speech/{LOCKED_VOICE_ID}"
           f"?output_format={urllib.parse.quote(CFG['tts_output_format'])}")
    body = {"text": text, "model_id": LOCKED_MODEL_ID, "language_code": LOCKED_LANGUAGE}
    audio = http("POST", url, {"xi-api-key": key, "Accept": "audio/mpeg"}, body, timeout=180)
    if len(audio) < 2000:
        raise RuntimeError("ElevenLabs returned an empty audio file")
    open(out, "wb").write(audio)


def tone(text, out):
    """Test mode: a quiet tone as long as the speech would be. Costs no credits."""
    secs = max(1.5, len(TAG.sub("", text)) / 11.0)
    subprocess.check_call(["ffmpeg", "-y", "-loglevel", "error", "-f", "lavfi", "-i",
                           f"sine=frequency=330:duration={secs:.2f}", "-af", "volume=0.05",
                           "-c:a", "libmp3lame", "-b:a", "128k", out])


def duration(path):
    return float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                                          "-of", "default=nw=1:nk=1", path]).decode())


def main():
    ep = os.environ.get("EPISODE", "").strip()
    test = os.environ.get("TEST_TONE") == "1"
    if not SLUG.fullmatch(ep):
        note("error", f"voice: bad episode name '{ep}'"); return 1
    content = branch_dir("content")
    src = os.path.join(content, "voice", ep, "narration.json")
    if not os.path.isfile(src):
        note("error", f"voice {ep}: content:voice/{ep}/narration.json not found"); return 1
    try:
        nar = json.load(open(src, encoding="utf-8"))
    except Exception as e:
        note("error", f"voice {ep}: narration.json is not valid JSON ({e})"); return 1
    errs = validate_narration(nar)
    if errs:
        note("error", f"voice {ep}: " + "; ".join(errs)); return 1

    audio = branch_dir("audio")
    # drop episodes older than keep_audio_days so the branch stays small
    cutoff = datetime.now(timezone.utc) - timedelta(days=CFG["keep_audio_days"])
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
    want_kind = "tone" if test else f"{LOCKED_MODEL_ID}:{LOCKED_VOICE_ID}"
    made = reused = chars = 0
    durs = {}
    for t in nar:
        tid, text = t["id"], t["text"]
        out = os.path.join(d, "vo", f"{tid}.mp3")
        h = text_hash(text + "|" + want_kind)
        if os.path.isfile(out) and man["takes"].get(tid) == h:
            reused += 1
        else:
            try:
                (tone if test else tts)(text, out)
            except Exception as e:
                note("error", f"voice {ep} take {tid}: {redact(e)}")
                push_partial(audio, d, man, durs, nar, ep)  # keep paid takes even if a later one fails
                return 1
            man["takes"][tid] = h
            made += 1
            chars += len(TAG.sub("", text))
            time.sleep(0.5)
        durs[tid] = round(duration(out), 3)
    # remove takes that are no longer in the narration
    keep = {t["id"] for t in nar}
    for f in os.listdir(os.path.join(d, "vo")):
        if f[:-4] not in keep:
            os.remove(os.path.join(d, "vo", f))
    man["takes"] = {k: v for k, v in man["takes"].items() if k in keep}
    push_partial(audio, d, man, durs, nar, ep)
    total = sum(durs.values())
    note("notice", f"voice {ep}: OK {'TEST TONE ' if test else ''}{made} new take(s), {reused} reused, "
                   f"{chars} characters charged, {len(durs)} takes, {total:.1f}s of speech")
    summary(f"### Voice `{ep}`\n{made} new, {reused} reused, {chars} characters, {total:.1f} s of speech.")
    return 0


def push_partial(audio, d, man, durs, nar, ep):
    man["updated"] = datetime.now(timezone.utc).isoformat()
    json.dump(man, open(os.path.join(d, "manifest.json"), "w"), indent=1)
    json.dump(durs, open(os.path.join(d, "durations.json"), "w"), indent=1)
    json.dump(nar, open(os.path.join(d, "narration.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    push_branch(audio, "audio", f"voice {ep}", squash=True)


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as e:
        note("error", f"voice failed: {redact(e)}")
        sys.exit(1)
