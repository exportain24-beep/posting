#!/usr/bin/env python3
"""Generate one ElevenLabs voice sample, the same call as the ElevenLabs quickstart
(text_to_speech.convert -> POST /v1/text-to-speech/{voice_id}).

  python scripts/voice_test.py [OUT.mp3] [--model eleven_v4_turbo] [--text "..."]

Reads ELEVENLABS_API_KEY from the environment only. Never prints it.
"""
import os, sys, time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pipeline as P

DEFAULT_TEXT = ("আসসালামু আলাইকুম। এক্সপোর্টেইনে আপনাকে স্বাগতম। "
                "বাংলাদেশের পণ্য এখন পৌঁছে যাক বিশ্ববাজারে। এটি একটি ভয়েস পরীক্ষা।")


def arg(name, default):
    if name in sys.argv:
        i = sys.argv.index(name)
        return sys.argv[i + 1]
    return default


def main():
    out = next((a for a in sys.argv[1:] if a.endswith(".mp3")), "voice-test/sample.mp3")
    text = arg("--text", "") or DEFAULT_TEXT
    model = arg("--model", "") or P.CFG["tts_model_id"]
    if not P.secret("ELEVENLABS_API_KEY"):
        print("ELEVENLABS_API_KEY is not set (add it to the 'production' environment)."); return 1
    if "/" in text:
        print("Text contains '/'. Write it out in Bangla (B/L -> বি এল)."); return 1
    os.makedirs(os.path.dirname(out) or ".", exist_ok=True)
    P.CFG["tts_model_id"] = model
    t = time.time()
    try:
        P.tts(text, out)
    except Exception as e:
        P.log("Voice test FAILED:", e)
        P.summary(f"### Voice test failed\n`{P.redact(e)}`\n\nCheck the key, its Text to Speech permission, "
                  f"your credits, and that voice `{P.CFG['voice_id']}` is in your ElevenLabs library.")
        return 1
    secs = P.duration(out)
    P.log(f"OK: {out}  {secs:.1f}s audio  model={model}  voice={P.CFG['voice_id']}  ({time.time() - t:.1f}s)")
    P.summary(f"### Voice test passed ✅\nModel `{model}`, voice `{P.CFG['voice_id']}`, "
              f"{len(text)} characters → **{secs:.1f} s** of audio.\n\nDownload `voice-sample` below to listen.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
