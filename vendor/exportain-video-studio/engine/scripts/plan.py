#!/usr/bin/env python3
"""Bangla script + voiceover -> timed scene plan (plan.json). No ASR needed:
sentence boundaries are snapped to real pauses found by ffmpeg silencedetect.
Optional --words words.json ([{word,start,end}]) gives exact karaoke timing."""
import argparse, json, re, subprocess, sys

TAG_RE = re.compile(r"\[([^\]]+)\]")
SENT_END = re.compile(r"(?<=[।?!])\s+|(?<=\.)\s+(?=[^\x00-\x7F])")
ICON_RULES = [
    ("customs", ["কাস্টমস", "ক্লিয়ারিং", "customs"]),
    ("ship", ["শিপিং", "জাহাজ", "shipping"]),
    ("freight", ["ফ্রেইট", "ফরওয়ার্ড", "লজিস্টিক", "freight"]),
    ("globe", ["আন্তর্জাতিক", "বিদেশি", "বিশ্ব", "global"]),
    ("search", ["খুঁজে", "সঠিক", "find"]),
    ("store", ["মার্কেটপ্লেস", "বিটুবি", "b2b", "marketplace"]),
    ("profile", ["পরিচিতি", "বিবরণ", "যোগাযোগের তথ্য", "profile"]),
    ("handshake", ["যোগাযোগ", "সংযুক্ত", "সংযোগ", "connect"]),
    ("chart", ["বাণিজ্য", "ব্যবসা", "বেশি", "grow"]),
    ("cursor", ["ভিজিট", "visit", ".com"]),
    ("question", ["?"]),
]
FALLBACK = ["spark", "handshake", "chart", "store", "network"]
ACCENT_BY_TAG = {"excited": "#ff9f1c", "happy": "#26d07c", "thoughtful": "#38bdf8",
                 "inquisitive": "#a78bfa", "encouraging": "#26d07c"}
EMPH = ["শিপিং", "ফ্রেইট", "কাস্টমস", "আন্তর্জাতিক", "বিদেশি", "বিটুবি", "মার্কেটপ্লেস", "ক্রেতা", "সাপ্লায়ার", "ট্রেড"]


def duration(p):
    return float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                                 "-of", "csv=p=0", p], capture_output=True, text=True, check=True).stdout)


def silences(p, noise_db=-32, min_len=0.22):
    err = subprocess.run(["ffmpeg", "-hide_banner", "-i", p, "-af",
                          f"silencedetect=noise={noise_db}dB:d={min_len}", "-f", "null", "-"],
                         capture_output=True, text=True).stderr
    s = [float(x) for x in re.findall(r"silence_start: ([\d.]+)", err)]
    e = [float(x) for x in re.findall(r"silence_end: ([\d.]+)", err)]
    return list(zip(s, e))


def parse(raw):
    out, chunks, tag, last = [], [], None, 0
    for m in TAG_RE.finditer(raw):
        chunks.append((tag, raw[last:m.start()])); tag, last = m.group(1).strip().lower(), m.end()
    chunks.append((tag, raw[last:]))
    for tag, text in chunks:
        for s in SENT_END.split(" ".join(text.split())):
            if s.strip(): out.append({"text": s.strip(), "tag": tag})
    return out


def align(sents, total, pauses, lead, tail):
    a0, a1 = lead, total - tail
    w = [max(1, len(re.sub(r"\s", "", s["text"]))) for s in sents]
    cum, acc = [], 0
    for x in w[:-1]:
        acc += x; cum.append(a0 + (a1 - a0) * acc / sum(w))
    mids = sorted(((a + b) / 2, b - a) for a, b in pauses if a0 < a and b < a1)
    bounds, used = [], set()
    for exp in cum:
        best, bd = None, 1e9
        for i, (m, ln) in enumerate(mids):
            d = abs(m - exp) - 0.3 * ln
            if i not in used and d < bd and abs(m - exp) < 2.5: best, bd = i, d
        if best is None: bounds.append(exp)
        else: used.add(best); bounds.append(mids[best][0])
    for i in range(1, len(bounds)): bounds[i] = max(bounds[i], bounds[i - 1] + 0.6)
    edges = [0.0] + bounds + [total]
    return [(edges[i], edges[i + 1]) for i in range(len(sents))]


def pick_icon(text, prev, i):
    t, best = text.lower(), []
    for icon, keys in ICON_RULES:
        pos = [t.find(k.lower()) for k in keys if k.lower() in t]
        if pos and icon != prev: best.append((-len(pos), min(pos), icon))
    if best: return sorted(best)[0][2]
    return next(f for f in FALLBACK[i % len(FALLBACK):] + FALLBACK if f != prev)


def emphasis(text, brand):
    keys = ([brand.lower()] if brand else []) + EMPH
    return [w for w in text.split() if any(k and k in w.lower() for k in keys)]


def main():
    ap = argparse.ArgumentParser()
    for f in ["--script", "--voice", "--out"]: ap.add_argument(f, required=True)
    for f in ["--words", "--brand", "--url", "--logo", "--tagline"]: ap.add_argument(f, default="")
    ap.add_argument("--endcard", type=float, default=3.0)
    ap.add_argument("--noise-db", type=float, default=-32)
    a = ap.parse_args()
    sents = parse(open(a.script, encoding="utf-8").read())
    if not sents: sys.exit("No text found in script.")
    total = duration(a.voice); pauses = silences(a.voice, a.noise_db)
    lead = pauses[0][1] if pauses and pauses[0][0] < 0.05 else 0.0
    tail = total - pauses[-1][0] if pauses and pauses[-1][1] > total - 0.05 else 0.0
    times = align(sents, total, pauses, lead, tail)
    words = json.load(open(a.words, encoding="utf-8")) if a.words else None
    scenes, prev = [], None
    for i, (s, (st, en)) in enumerate(zip(sents, times)):
        prev = pick_icon(s["text"], prev, i)
        sc = {"start": round(st, 3), "end": round(en, 3), "text": s["text"], "tag": s["tag"], "icon": prev,
              "accent": ACCENT_BY_TAG.get(s["tag"] or "", "#26d07c"), "emphasis": emphasis(s["text"], a.brand)}
        if words: sc["words"] = [w for w in words if st - 0.05 <= w["start"] < en]
        scenes.append(sc)
    plan = {"voice_duration": round(total, 3), "endcard": a.endcard, "total": round(total + a.endcard, 3),
            "brand": a.brand, "url": a.url, "logo": a.logo, "pauses_found": len(pauses),
            "tagline": a.tagline or (sents[-1]["text"] if a.brand and a.brand in sents[-1]["text"] else ""),
            "scenes": scenes}
    json.dump(plan, open(a.out, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    print(f"{len(scenes)} scenes, VO {total:.2f}s, {len(pauses)} pauses -> {a.out}")
    for i, sc in enumerate(scenes):
        print(f"  {i:02d} {sc['start']:6.2f}-{sc['end']:6.2f} [{sc['icon']:9}] {sc['text'][:50]}")


if __name__ == "__main__":
    main()
