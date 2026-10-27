"""Shared helpers for the Exportain YouTube Shorts lane.

This lane is fully separate from the 3-5 min reel system:
  * its own config (shorts/config.json), workflows (shorts-voice.yml, shorts-publish.yml) and data branches
    (shorts-content / shorts-audio / shorts-media / shorts-state);
  * it only *imports* generic helpers from common.py (HTTP, git, logging, secret masking) and never writes to the
    reel system's branches or files.
"""
import json, os, re, subprocess
from datetime import datetime, timedelta, timezone

from common import ROOT, TAG, note, redact   # generic helpers only

SCFG = json.load(open(os.path.join(ROOT, "shorts", "config.json"), encoding="utf-8"))
STZ = timezone(timedelta(hours=SCFG["timezone_offset_hours"]))
BR = SCFG["branches"]
SHORT_ID = re.compile(r"sh-[0-9]{4}-(bn|en)(-[a-z0-9-]{2,40})?")
TAKE_ID = re.compile(r"[0-9]{2}_[a-z0-9_]{1,30}")


def short_lang(ep):
    m = SHORT_ID.fullmatch(ep or "")
    return m.group(1) if m else None


def is_bangla(text):
    spoken = TAG.sub("", str(text))
    if re.search(r"[A-Za-z]", spoken):
        return False
    letters = [c for c in spoken if c.isalpha()]
    return bool(letters) and sum("ঀ" <= c <= "৿" for c in letters) / len(letters) >= 0.9


def is_english(text):
    spoken = TAG.sub("", str(text))
    if re.search(r"[ঀ-৿]", spoken):
        return False
    letters = [c for c in spoken if c.isalpha()]
    return bool(letters) and sum(c.isascii() for c in letters) / len(letters) >= 0.97


def validate_narration(nar, lang):
    """narration.json = [{"id": "00_hook", "text": "..."}]; Bangla Shorts: Bangla script only; English Shorts: English only."""
    errs = []
    if lang not in SCFG["languages"]:
        return [f"language {lang} not allowed"]
    if not isinstance(nar, list) or not 2 <= len(nar) <= 12:
        return ["narration must be a list of 2-12 takes"]
    seen, total = set(), 0
    for i, t in enumerate(nar):
        if not isinstance(t, dict):
            errs.append(f"take {i} is not an object"); continue
        tid, text = str(t.get("id", "")), str(t.get("text", ""))
        if not TAKE_ID.fullmatch(tid) or tid in seen:
            errs.append(f"take {i}: id '{tid}' must look like 00_hook and be unique")
        seen.add(tid)
        spoken = TAG.sub("", text)
        if not 3 <= len(spoken) <= 260:
            errs.append(f"{tid}: text length {len(spoken)} (want 3-260)")
        if "/" in spoken:
            errs.append(f"{tid}: contains '/' — write it out")
        if lang == "bn" and not is_bangla(text):
            errs.append(f"{tid}: Bangla Short must be Bangla script only (English terms written in Bangla)")
        if lang == "en" and not is_english(text):
            errs.append(f"{tid}: English Short must be English only")
        total += len(spoken)
    cap = SCFG["max_voice_chars_bn" if lang == "bn" else "max_voice_chars_en"]
    if total > cap:
        errs.append(f"total {total} characters > limit {cap} for a 30-second Short")
    return errs


def _txt(d, key, lo, hi, errs, where, no_angle=False):
    v = d.get(key, "")
    if not isinstance(v, str) or not lo <= len(v) <= hi:
        errs.append(f"{where}.{key}: {lo}-{hi} characters")
    elif no_angle and re.search(r"[<>]", v):
        errs.append(f"{where}.{key}: no < or >")


def validate_meta(meta, name):
    """shorts-media:s/<id>.json written by Claude for each finished Short (YouTube only)."""
    errs = []
    if not isinstance(meta, dict):
        return [f"{name}: not an object"]
    if not SHORT_ID.fullmatch(str(meta.get("id", ""))) or f"{meta.get('id')}.json" != name:
        errs.append(f"{name}: id must look like sh-0001-bn-<slug> and equal the file name")
    if not re.fullmatch(r"[0-9]{4}", str(meta.get("n", ""))):
        errs.append(f"{name}: n must be the 4-digit plan number, e.g. 0001")
    try:
        t = datetime.fromisoformat(str(meta.get("slot")))
        if t.tzinfo is None:
            raise ValueError
    except Exception:
        errs.append(f"{name}: slot must be an ISO time with timezone")
    yt = meta.get("youtube") or {}
    _txt(yt, "title", 5, 100, errs, "youtube", True)
    _txt(yt, "description", 20, 4800, errs, "youtube", True)
    tags = yt.get("tags", [])
    if not isinstance(tags, list) or len(",".join(map(str, tags))) > 480 or not all(isinstance(x, str) for x in tags):
        errs.append("youtube.tags: list of strings, 480 characters in total")
    if yt.get("language") not in ("bn", "en"):
        errs.append("youtube.language must be bn or en")
    return errs


def probe(path):
    out = subprocess.check_output(["ffprobe", "-v", "error", "-show_entries",
                                   "format=duration:stream=codec_type,codec_name,width,height",
                                   "-of", "json", path]).decode()
    return json.loads(out)


def validate_files(mp4, jpg):
    errs, lim = [], SCFG["video_limits"]
    if not os.path.isfile(mp4):
        return [f"video missing: {os.path.basename(mp4)}"]
    if os.path.getsize(mp4) > lim["max_mb"] * 1e6:
        errs.append("video too large")
    try:
        p = probe(mp4)
        v = next(s for s in p["streams"] if s["codec_type"] == "video")
        dur = float(p["format"]["duration"])
        if v["codec_name"] not in ("h264", "hevc"):
            errs.append(f"video codec {v['codec_name']} (need h264)")
        if abs(v["width"] / v["height"] - 9 / 16) > 0.01 or v["width"] < 720:
            errs.append(f"video is {v['width']}x{v['height']} (need 9:16, 1080x1920)")
        if not lim["min_seconds"] <= dur <= lim["max_seconds"] + 0.05:
            errs.append(f"video is {dur:.2f}s (Shorts must be {lim['min_seconds']}-{lim['max_seconds']}s)")
        if not any(s["codec_type"] == "audio" for s in p["streams"]):
            errs.append("video has no audio")
    except Exception as e:
        errs.append(f"cannot read video: {redact(e)}")
    if jpg and os.path.isfile(jpg) and os.path.getsize(jpg) > lim["thumb_max_mb"] * 1e6:
        errs.append("thumbnail larger than 2 MB")
    return errs
