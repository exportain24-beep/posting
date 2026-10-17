#!/usr/bin/env python3
"""Instagram job (GitHub Actions, own workflow ig.yml): posts each video as a Reel at its slot time.

Instagram's API cannot schedule, so this job waits on the runner and publishes at the exact slot:
  ~20 min before the slot: create the Reel container, upload the video (resumable upload, no public video
  URL needed), wait until Instagram has processed it; at the slot: media_publish.

MODE=check    find the Instagram account linked to the Page, post nothing
MODE=slots    handle every video whose slot is between 3 h ago and ~5 h 45 min ahead (sorted by slot)
MODE=now      publish EPISODE immediately (owner-requested test)

Auth = the same FB_PAGE_TOKEN (system user) -> Page token + appsecret_proof as Facebook. Results: state:ig.json.
"""
import json, os, subprocess, sys, time, urllib.parse
from datetime import datetime, timedelta, timezone

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import CFG, TZ, branch_dir, http, jhttp, note, parse_slot, push_branch, redact, summary
from publish import fb_auth

PL = CFG["platforms"]
AHEAD = timedelta(hours=5, minutes=45)    # job limit is 6 h
PREP = timedelta(minutes=20)              # upload/processing lead before the slot
LATE = timedelta(hours=3)                 # still post if the slot was missed by less than this


def ig_account():
    page, auth, proof, g = fb_auth()
    q = urllib.parse.urlencode({"fields": "instagram_business_account{id,username}", **proof})
    acc = jhttp("GET", f"{g}/{page}?{q}", auth).get("instagram_business_account")
    if not acc:
        raise RuntimeError("no Instagram professional account is linked to the Page (or the token lacks instagram_basic)")
    return acc, auth, proof, g


def ig_video(mp4):
    """Instagram limits: AAC <= 128 kbps, <= 48 kHz; H.264 kept as is."""
    out = mp4[:-4] + "_ig.mp4"
    subprocess.check_call(["ffmpeg", "-y", "-loglevel", "error", "-i", mp4, "-c:v", "copy", "-c:a", "aac", "-b:a", "128k",
                           "-ar", "48000", "-ac", "2", "-movflags", "+faststart", out])
    return out


def caption(meta):
    ig = meta.get("instagram") or {}
    return (ig.get("caption") or meta["facebook"]["description"])[:2200]


def prepare(meta, mp4):
    acc, auth, proof, g = ig_account()
    vid = ig_video(mp4)
    size = os.path.getsize(vid)
    data = {"media_type": "REELS", "upload_type": "resumable", "caption": caption(meta), "share_to_feed": "true", **proof}
    cover = f"{CFG['pages_base_url']}/v/{meta['id']}_ig.jpg"
    try:
        h = http("HEAD", cover, timeout=30, want_headers=True)[1]
        if "image" in (h.get("Content-Type") or h.get("content-type", "")):
            data["cover_url"] = cover
    except Exception:
        pass
    c = jhttp("POST", f"{g}/{acc['id']}/media", {**auth, "Content-Type": "application/x-www-form-urlencoded"},
              urllib.parse.urlencode(data).encode())
    cid = c.get("id")
    if not cid:
        raise RuntimeError(f"container not created: {c}")
    gv = PL["facebook"]["graph_version"]
    http("POST", f"https://rupload.facebook.com/ig-api-upload/{gv}/{cid}",
         {**auth, "offset": "0", "file_size": str(size), "Content-Type": "application/octet-stream"},
         open(vid, "rb").read(), timeout=1800)
    end = time.time() + 20 * 60
    st = {}
    while time.time() < end:
        q = urllib.parse.urlencode({"fields": "status_code,status", **proof})
        st = jhttp("GET", f"{g}/{cid}?{q}", auth)
        if st.get("status_code") == "FINISHED":
            return acc, cid, auth, proof, g, "cover set" if "cover_url" in data else "default cover"
        if st.get("status_code") in ("ERROR", "EXPIRED"):
            raise RuntimeError(f"Instagram processing failed: {st}")
        time.sleep(15)
    raise RuntimeError(f"Instagram processing timed out: {st}")


def publish_now(acc, cid, auth, proof, g):
    r = jhttp("POST", f"{g}/{acc['id']}/media_publish", {**auth, "Content-Type": "application/x-www-form-urlencoded"},
              urllib.parse.urlencode({"creation_id": cid, **proof}).encode())
    if not r.get("id"):
        raise RuntimeError(f"media_publish failed: {r}")
    q = urllib.parse.urlencode({"fields": "permalink", **proof})
    try:
        link = jhttp("GET", f"{g}/{r['id']}?{q}", auth).get("permalink", "")
    except Exception:
        link = ""
    return r["id"], link


def sleep_until(t):
    while True:
        left = (t - datetime.now(timezone.utc)).total_seconds()
        if left <= 0:
            return
        time.sleep(min(left, 60))


def main():
    mode = os.environ.get("MODE", "check")
    if mode == "check":
        try:
            acc = ig_account()[0]
            note("notice", f"check instagram: account OK @{acc.get('username')}")
            return 0
        except Exception as e:
            note("error", f"check instagram: {redact(e)}"); return 1
    if not PL.get("instagram", {}).get("enabled"):
        note("notice", "instagram disabled in config"); return 0
    media = branch_dir("media")
    metas = []
    for f in sorted(os.listdir(os.path.join(media, "v"))):
        if f.endswith(".json"):
            try:
                metas.append(json.load(open(os.path.join(media, "v", f), encoding="utf-8")))
            except Exception:
                pass
    sd = branch_dir("state")
    sp = os.path.join(sd, "ig.json")
    state = json.load(open(sp, encoding="utf-8")) if os.path.isfile(sp) else {}
    now = datetime.now(timezone.utc)
    if mode == "now":
        ep = os.environ.get("EPISODE", "")
        todo = [m for m in metas if m["id"] == ep]
        if not todo:
            note("error", f"instagram: episode {ep} not found on the media branch"); return 1
    else:
        todo = sorted((m for m in metas if not state.get(m["id"], {}).get("media_id")
                       and now - LATE <= parse_slot(m["slot"]) <= now + AHEAD), key=lambda m: m["slot"])
    if not todo:
        note("notice", "instagram: nothing due in the next 5 h 45 min"); return 0
    bad = 0
    for m in todo:
        ep, slot = m["id"], parse_slot(m["slot"])
        rec = state.setdefault(ep, {"slot": m["slot"]})
        if rec.get("media_id") and mode != "now":
            continue
        try:
            if mode != "now":
                note("notice", f"{ep} instagram: waiting for {slot.astimezone(TZ):%d %b %H:%M}")
                sleep_until(slot - PREP)
            acc, cid, auth, proof, g, info = prepare(m, os.path.join(media, "v", ep + ".mp4"))
            if mode != "now":
                sleep_until(slot)
            mid, link = publish_now(acc, cid, auth, proof, g)
            rec.update({"media_id": mid, "permalink": link, "posted": datetime.now(timezone.utc).isoformat()})
            rec.pop("error", None)
            note("notice", f"{ep} instagram: OK Reel published, {info} {link}")
        except Exception as e:
            bad += 1
            rec["error"] = redact(e)[:400]
            note("error", f"{ep} instagram: {redact(e)}")
        json.dump(state, open(sp, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        push_branch(sd, "state", f"instagram {ep}")
    summary(f"### Instagram ({mode})\nvideos: {len(todo)}, problems: {bad}")
    return 1 if bad else 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as e:
        note("error", f"instagram failed: {redact(e)}")
        sys.exit(1)
