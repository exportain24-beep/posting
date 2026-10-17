#!/usr/bin/env python3
"""Generate one ElevenLabs voice sample, the same call as the ElevenLabs quickstart
(text_to_speech.convert -> POST /v1/text-to-speech/{voice_id}).

  python scripts/voice_test.py [OUT.mp3] [--text "..."]   (model, voice and language are locked)

Reads ELEVENLABS_API_KEY from the environment only. Never prints it.
"""
import os, sys, time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import common as P
import voice as V

DEFAULT_TEXT = ("আসসালামু আলাইকুম। এক্সপোর্টেইনে আপনাকে স্বাগতম। "
                "বাংলাদেশের পণ্য এখন পৌঁছে যাক বিশ্ববাজারে। এটি একটি ভয়েস পরীক্ষা।")


def arg(name, default):
    if name in sys.argv:
        i = sys.argv.index(name)
        return sys.argv[i + 1]
    return default


def check_only():
    """Validate the key without generating audio (costs nothing): read the locked voice's info."""
    import urllib.error, urllib.request
    req = urllib.request.Request(f"https://api.elevenlabs.io/v1/voices/{V.LOCKED_VOICE_ID}",
                                 headers={"xi-api-key": P.secret("ELEVENLABS_API_KEY")})
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            name = __import__("json").loads(r.read()).get("name", "?")
        P.note("notice", f"key check OK: key is valid, voice {V.LOCKED_VOICE_ID} = {name}. No audio made, no credits used.")
        return 0
    except urllib.error.HTTPError as e:
        body = e.read()[:300].decode("utf-8", "replace")
        if e.code == 401 and "missing_permissions" not in body and "permission" not in body.lower():
            P.note("error", f"key check FAILED: ElevenLabs rejected the key (401). Is it copied correctly? {P.redact(body)}")
            return 1
        if e.code in (401, 403):
            P.note("notice", "key check OK: key is valid and correctly restricted (it may not read voice info, "
                             "Text to Speech is what matters). No audio made, no credits used.")
            return 0
        P.note("error", f"key check: unexpected HTTP {e.code}: {P.redact(body)}")
        return 1


def main():
    out = next((a for a in sys.argv[1:] if a.endswith(".mp3")), "voice-test/sample.mp3")
    text = arg("--text", "") or DEFAULT_TEXT
    model = V.LOCKED_MODEL_ID
    if not P.secret("ELEVENLABS_API_KEY"):
        P.note("error", "voice test: ELEVENLABS_API_KEY is not set in the production environment"); return 1
    if "--check-only" in sys.argv:
        return check_only()
    if "/" in text:
        print("Text contains '/'. Write it out in Bangla (B/L -> বি এল)."); return 1
    os.makedirs(os.path.dirname(out) or ".", exist_ok=True)
    t = time.time()
    try:
        V.tts(text, out)
    except Exception as e:
        P.note("error", f"voice test FAILED: {P.redact(e)}")
        P.summary(f"### Voice test failed\n`{P.redact(e)}`\n\nCheck the key, its Text to Speech permission, "
                  f"your credits, and that voice `{V.LOCKED_VOICE_ID}` is in your ElevenLabs library.")
        return 1
    secs = V.duration(out)
    P.note("notice", f"voice test OK: {out}  {secs:.1f}s audio  model={model}  voice={V.LOCKED_VOICE_ID}  ({time.time() - t:.1f}s)")
    P.summary(f"### Voice test passed ✅\nModel `{model}`, voice `{V.LOCKED_VOICE_ID}`, "
              f"{len(text)} characters → **{secs:.1f} s** of audio.\n\nDownload `voice-sample` below to listen.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
