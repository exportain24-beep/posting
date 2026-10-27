#!/usr/bin/env python3
"""Shorts publish job (GitHub Actions): shorts-media:s/<id>.{mp4,jpg,json}  ->  YouTube only (as a Short).

MODE=check    read-only: YouTube login + every waiting file, posts nothing
MODE=private  upload as private (test)
MODE=live     upload now, scheduled to go public at its slot (publishAt)
MODE=retry    re-try failed uploads: slot >= 15 min away -> scheduled; slot passed < 6 h ago -> public now
MODE=now      upload and publish immediately

Results go to shorts-state:posts.json and to GitHub annotations. Reads only the three YouTube secrets.
"""
import glob, json, os, sys, time, urllib.parse
from datetime import datetime, timedelta, timezone

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import branch_dir, http, jhttp, mask, note, push_branch, redact, secret, summary
from shorts_common import BR, SCFG, STZ, validate_files, validate_meta

YT = SCFG["youtube"]


def utc(t):
    return t.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.000Z")


def yt_token():
    cid, cs, rt = secret("YT_CLIENT_ID"), secret("YT_CLIENT_SECRET"), secret("YT_REFRESH_TOKEN")
    if not (cid and cs and rt):
        raise RuntimeError("YouTube secrets missing")
    tok = jhttp("POST", "https://oauth2.googleapis.com/token", {"Content-Type": "application/x-www-form-urlencoded"},
                urllib.parse.urlencode({"client_id": cid, "client_secret": cs, "refresh_token": rt,
                                        "grant_type": "refresh_token"}).encode())["access_token"]
    mask(tok)
    return tok


def yt_check():
    tok = yt_token()
    info = jhttp("POST", "https://oauth2.googleapis.com/tokeninfo",
                 {"Content-Type": "application/x-www-form-urlencoded"}, urllib.parse.urlencode({"access_token": tok}).encode())
    return "login OK, scopes: " + info.get("scope", "").replace("https://www.googleapis.com/auth/", "")


def yt_publish(meta, mp4, jpg, slot, mode):
    tok = yt_token()
    auth = {"Authorization": f"Bearer {tok}"}
    y = meta["youtube"]
    status = {"privacyStatus": "private", "selfDeclaredMadeForKids": False,
              "containsSyntheticMedia": YT.get("contains_synthetic_media", False)}
    if mode == "live":
        status["publishAt"] = utc(slot)
    elif mode == "now":
        status["privacyStatus"] = "public"
    lang = y.get("language", "bn")
    body = {"snippet": {"title": y["title"][:100], "description": y["description"], "tags": y.get("tags", []),
                        "categoryId": YT.get("category_id", "27"), "defaultLanguage": lang, "defaultAudioLanguage": lang},
            "status": status}
    size = os.path.getsize(mp4)
    _, hdr = http("POST", "https://www.googleapis.com/upload/youtube/v3/videos?uploadType=resumable&part=snippet,status",
                  {**auth, "X-Upload-Content-Type": "video/mp4", "X-Upload-Content-Length": str(size)}, body,
                  want_headers=True)
    loc = hdr.get("Location") or hdr.get("location")
    vid = json.loads(http("PUT", loc, {**auth, "Content-Type": "video/mp4", "Content-Length": str(size)},
                          open(mp4, "rb").read(), timeout=900))["id"]
    extras = []
    if YT.get("set_thumbnail") and jpg and os.path.isfile(jpg):
        try:   # used in search/channel pages; the Shorts feed shows the video's own first frames
            http("POST", f"https://www.googleapis.com/upload/youtube/v3/thumbnails/set?videoId={vid}",
                 {**auth, "Content-Type": "image/jpeg"}, open(jpg, "rb").read())
            extras.append("thumbnail set")
        except Exception as e:
            extras.append(f"thumbnail not set ({redact(e)[:120]})")
    pl = (YT.get("playlist_ids") or {}).get(meta.get("cluster", ""), "")
    if pl:
        try:
            jhttp("POST", "https://www.googleapis.com/youtube/v3/playlistItems?part=snippet", auth,
                  {"snippet": {"playlistId": pl, "resourceId": {"kind": "youtube#video", "videoId": vid}}})
            extras.append("added to playlist")
        except Exception as e:
            extras.append(f"playlist not added ({redact(e)[:120]})")
    return vid, ", ".join(extras) or "uploaded"


TRANSIENT = ("HTTP 500", "HTTP 502", "HTTP 503", "HTTP 504", "HTTP 429", "network error", "timed out", "temporarily")


def attempt(fn, *args):
    for i in range(3):
        try:
            return fn(*args)
        except Exception as e:
            if i == 2 or not any(t in str(e) for t in TRANSIENT):
                raise
            note("warning", f"{fn.__name__}: transient error, retrying in {60 * (i + 1)} s: {redact(e)[:160]}")
            time.sleep(60 * (i + 1))


def main():
    mode = os.environ.get("MODE", "check")
    if mode not in ("check", "private", "live", "now", "retry"):
        note("error", f"shorts publish: unknown mode {mode}"); return 1
    now = datetime.now(timezone.utc)
    media, state_d = branch_dir(BR["media"]), branch_dir(BR["state"])
    sp = os.path.join(state_d, "posts.json")
    state = json.load(open(sp, encoding="utf-8")) if os.path.isfile(sp) else {"posts": {}}
    bad = 0
    if mode == "check":
        try:
            note("notice", f"check youtube: {yt_check()}")
        except Exception as e:
            bad += 1; note("error", f"check youtube: {redact(e)}")

    metas = sorted(glob.glob(os.path.join(media, "s", "*.json")))
    for mf in metas:
        name = os.path.basename(mf)
        try:
            meta = json.load(open(mf, encoding="utf-8"))
        except Exception as e:
            bad += 1; note("error", f"{name}: invalid JSON ({e})"); continue
        mp4, jpg = mf[:-5] + ".mp4", mf[:-5] + ".jpg"
        errs = validate_meta(meta, name) + validate_files(mp4, jpg)
        if errs:
            bad += 1; note("error", f"{name}: " + "; ".join(errs)); continue
        ep, slot = meta["id"], datetime.fromisoformat(meta["slot"])
        rec = state["posts"].setdefault(ep, {"n": meta["n"], "slot": meta["slot"], "done": {}, "errors": {}})
        if mode == "check":
            note("notice", f"{ep}: files OK, slot {slot.astimezone(STZ):%d %b %H:%M}, youtube: {rec['done'].get('youtube', 'not yet')}")
            continue
        if "youtube" in rec["done"]:
            continue
        m = mode
        if mode == "retry":
            if not rec.get("errors"):
                continue
            if slot >= now + timedelta(minutes=15):
                m = "live"
            elif slot >= now - timedelta(hours=6):
                m = "now"
            else:
                continue
        elif rec.get("mode") and rec["mode"] != mode and not rec.get("errors"):
            note("warning", f"{ep}: already handled in {rec['mode']} mode, skipped"); continue
        if m == "live" and slot < now + timedelta(minutes=15):
            bad += 1; rec["errors"]["youtube"] = "slot too close or past"
            note("error", f"{ep}: slot {meta['slot']} is too close or past; not uploaded"); continue
        rec["mode"] = m if mode != "retry" else rec.get("mode", m)
        try:
            vid, info = attempt(yt_publish, meta, mp4, jpg, slot, m)
            rec["done"]["youtube"] = vid
            rec["errors"].pop("youtube", None)
            note("notice", f"{ep} youtube: OK https://youtube.com/shorts/{vid} — "
                           f"{'scheduled ' + slot.astimezone(STZ).strftime('%d %b %H:%M') if m == 'live' else m}; {info}")
        except Exception as e:
            bad += 1
            rec["errors"]["youtube"] = redact(e)[:400]
            note("error", f"{ep} youtube: {redact(e)}")
        rec["updated"] = now.isoformat()

    if mode != "check":
        cutoff = now - timedelta(days=90)
        state["posts"] = {k: v for k, v in state["posts"].items()
                          if datetime.fromisoformat(v["slot"]) > cutoff}
        json.dump(state, open(sp, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        push_branch(state_d, BR["state"], f"shorts publish ({mode})")
        # uploaded files are no longer needed on the media branch: keep it small
        removed = 0
        for mf in metas:
            ep = os.path.basename(mf)[:-5]
            rec = state["posts"].get(ep, {})
            if "youtube" in rec.get("done", {}):
                for ext in (".mp4", ".jpg", ".json"):
                    p = mf[:-5] + ext
                    if os.path.isfile(p):
                        os.remove(p); removed += 1
        if removed:
            push_branch(media, BR["media"], f"shorts media cleanup ({mode})", squash=True)
    summary(f"### Shorts publish ({mode})\nfiles: {len(metas)}, problems: {bad}")
    return 1 if bad else 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as e:
        note("error", f"shorts publish failed: {redact(e)}")
        sys.exit(1)
