#!/usr/bin/env python3
"""Shorts publish job (GitHub Actions): shorts-media:s/<id>.{mp4,jpg,json}  ->  YouTube (direct API) + TikTok (Buffer)
+ Facebook Page Reels (direct Graph API, video_reels).

MODE=check    read-only: YouTube login, Buffer TikTok channel and every waiting file; posts nothing
MODE=private  YouTube private upload only (test); TikTok skipped
MODE=live     YouTube scheduled (publishAt) + TikTok scheduled in Buffer + Facebook Reel scheduled, all at the slot
MODE=retry    repairs failed platforms: slot >= 15 min away -> scheduled again; slot passed < 6 h ago -> post now
MODE=now      publish immediately on both
MODE=thumbs   re-set YouTube thumbnails: shorts-media:t/<id>.jpg -> thumbnails.set on that Short's video, then removed

The TikTok copy is served to Buffer as a GitHub Release asset of this public repo (release tag "shorts-media-files"),
so the reel system's GitHub Pages / media branch are never touched. Results: shorts-state:posts.json + annotations.
"""
import glob, hashlib, hmac, json, os, sys, time, uuid, urllib.parse
from datetime import datetime, timedelta, timezone

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import branch_dir, http, jhttp, mask, note, push_branch, redact, secret, summary
from shorts_common import BR, SCFG, STZ, validate_files, validate_meta

YT = SCFG["youtube"]
TT = SCFG.get("tiktok", {"enabled": False})
FB = SCFG.get("facebook", {"enabled": False})
PLATFORMS = ["youtube"] + (["tiktok"] if TT.get("enabled") else []) + (["facebook"] if FB.get("enabled") else [])
REPO = os.environ.get("GITHUB_REPOSITORY", "exportain24-beep/posting")
RELEASE_TAG = "shorts-media-files"


def utc(t):
    return t.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.000Z")


# ------------------------------------------------------------------ YouTube
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
        try:
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
    where = f"https://youtube.com/shorts/{vid}"
    return vid, f"{where} — " + (f"scheduled {slot.astimezone(STZ):%d %b %H:%M}" if mode == "live" else mode) + \
        ("; " + ", ".join(extras) if extras else "")


# ------------------------------------------------------------------ public file for Buffer: GitHub Release asset
def gh_api(method, url, data=None, ctype=None, timeout=300):
    tok = secret("GITHUB_TOKEN")
    if not tok:
        raise RuntimeError("GITHUB_TOKEN missing")
    h = {"Authorization": f"Bearer {tok}", "Accept": "application/vnd.github+json", "X-GitHub-Api-Version": "2022-11-28"}
    if ctype:
        h["Content-Type"] = ctype
    body = http(method, url, h, data, timeout=timeout)
    return json.loads(body) if body and body[:1] in (b"{", b"[") else {}


def release():
    try:
        return gh_api("GET", f"https://api.github.com/repos/{REPO}/releases/tags/{RELEASE_TAG}")
    except RuntimeError as e:
        if "HTTP 404" not in str(e):
            raise
        return gh_api("POST", f"https://api.github.com/repos/{REPO}/releases",
                      {"tag_name": RELEASE_TAG, "target_commitish": "main", "name": "Shorts media files (temporary)",
                       "body": "Temporary public copies of Exportain Shorts for TikTok (Buffer) uploads. Cleaned automatically.",
                       "prerelease": True})


def public_url(mp4, name):
    rel = release()
    for a in rel.get("assets", []):
        if a["name"] == name:
            if a["size"] == os.path.getsize(mp4):
                return a["browser_download_url"]
            gh_api("DELETE", f"https://api.github.com/repos/{REPO}/releases/assets/{a['id']}")
    up = rel["upload_url"].split("{")[0] + "?" + urllib.parse.urlencode({"name": name})
    a = gh_api("POST", up, open(mp4, "rb").read(), ctype="video/mp4", timeout=900)
    url = a["browser_download_url"]
    for _ in range(12):                      # make sure the file is publicly downloadable before Buffer fetches it
        try:
            _, h = http("HEAD", url, want_headers=True, timeout=60)
            if int(h.get("Content-Length") or h.get("content-length") or 0) == os.path.getsize(mp4):
                return url
        except Exception:
            pass
        time.sleep(10)
    return url


def cleanup_release(keep_days=4):
    try:
        rel = release()
    except Exception:
        return 0
    n, cut = 0, datetime.now(timezone.utc) - timedelta(days=keep_days)
    for a in rel.get("assets", []):
        if datetime.fromisoformat(a["created_at"].replace("Z", "+00:00")) < cut:
            try:
                gh_api("DELETE", f"https://api.github.com/repos/{REPO}/releases/assets/{a['id']}"); n += 1
            except Exception:
                pass
    return n


# ------------------------------------------------------------------ Facebook Page Reels (direct Graph API)
def multipart(fields, files):
    b = uuid.uuid4().hex
    out = bytearray()
    for k, v in fields.items():
        out += f"--{b}\r\nContent-Disposition: form-data; name=\"{k}\"\r\n\r\n{v}\r\n".encode()
    for k, (fname, data, ctype) in files.items():
        out += (f"--{b}\r\nContent-Disposition: form-data; name=\"{k}\"; filename=\"{fname}\"\r\n"
                f"Content-Type: {ctype}\r\n\r\n").encode() + data + b"\r\n"
    out += f"--{b}--\r\n".encode()
    return bytes(out), f"multipart/form-data; boundary={b}"


def _proof(app_secret, tok):
    return {"appsecret_proof": hmac.new(app_secret.encode(), tok.encode(), hashlib.sha256).hexdigest()} if app_secret else {}


_fb = None


def fb_auth():
    """FB_PAGE_TOKEN (system user or Page token) -> fresh Page token. Same secrets as the reel system, read-only use."""
    global _fb
    if _fb:
        return _fb
    page, tok, app_secret = secret("FB_PAGE_ID"), secret("FB_PAGE_TOKEN"), secret("FB_APP_SECRET")
    if not (page and tok):
        raise RuntimeError("Facebook secrets missing (FB_PAGE_ID / FB_PAGE_TOKEN)")
    g = f"https://graph.facebook.com/{FB.get('graph_version', 'v23.0')}"
    q = urllib.parse.urlencode({"fields": "access_token", **_proof(app_secret, tok)})
    page_tok = jhttp("GET", f"{g}/{page}?{q}", {"Authorization": f"OAuth {tok}"}).get("access_token")
    if not page_tok:
        raise RuntimeError("could not get the Page token — does the system user have full control of the Page?")
    mask(page_tok)
    _fb = (page, page_tok, _proof(app_secret, page_tok), g)
    return _fb


def fb_check():
    page, tok, proof, g = fb_auth()
    p = jhttp("GET", f"{g}/{page}?" + urllib.parse.urlencode({"fields": "id,name", **proof}), {"Authorization": f"OAuth {tok}"})
    return f"page OK: {p.get('name')}"


def fb_publish(meta, mp4, jpg, slot, mode):
    """9:16 Short -> Facebook Page Reel: start -> rupload bytes -> finish (SCHEDULED at the slot / PUBLISHED / DRAFT)."""
    page, tok, proof, g = fb_auth()
    auth = {"Authorization": f"OAuth {tok}"}
    form = {"Content-Type": "application/x-www-form-urlencoded"}
    f = meta.get("facebook") or {}
    st = jhttp("POST", f"{g}/{page}/video_reels", {**auth, **form},
               urllib.parse.urlencode({"upload_phase": "start", **proof}).encode())
    vid = st.get("video_id")
    if not vid:
        raise RuntimeError(f"reel start failed: {st}")
    size = os.path.getsize(mp4)
    up = jhttp("POST", st.get("upload_url") or f"https://rupload.facebook.com/video-upload/{FB.get('graph_version', 'v23.0')}/{vid}",
               {**auth, "offset": "0", "file_size": str(size), "Content-Type": "application/octet-stream"},
               open(mp4, "rb").read(), timeout=900)
    if not up.get("success"):
        raise RuntimeError(f"reel upload failed: {up}")
    text = f.get("description", "")
    fields = {"upload_phase": "finish", "video_id": vid, "description": text, **proof}
    if f.get("title"):
        fields["title"] = f["title"]
    lead = (slot - datetime.now(timezone.utc)).total_seconds()
    if mode == "live" and 11 * 60 < lead < 29 * 86400:
        fields.update({"video_state": "SCHEDULED", "scheduled_publish_time": str(int(slot.timestamp()))})
        state = f"scheduled {slot.astimezone(STZ):%d %b %H:%M}"
    elif mode in ("live", "now"):
        fields["video_state"] = "PUBLISHED"; state = "published now"
    else:
        fields["video_state"] = "DRAFT"; state = "draft"
    fin = None
    for i in range(6):                       # Facebook may still be processing the upload
        try:
            fin = jhttp("POST", f"{g}/{page}/video_reels", {**auth, **form}, urllib.parse.urlencode(fields).encode())
            break
        except RuntimeError as e:
            if i == 5 or "HTTP 5" not in str(e) and "processing" not in str(e).lower():
                raise
            time.sleep(20)
    if not (fin or {}).get("success", True):
        raise RuntimeError(f"reel finish failed: {fin}")
    extras = [state]
    if jpg and os.path.isfile(jpg):
        try:
            b, c = multipart({"is_preferred": "true", **proof}, {"source": ("thumb.jpg", open(jpg, "rb").read(), "image/jpeg")})
            jhttp("POST", f"{g}/{vid}/thumbnails", {**auth, "Content-Type": c}, b)
            extras.append("cover set")
        except Exception as e:
            extras.append(f"cover not set ({redact(e)[:120]})")
    return vid, f"https://www.facebook.com/reel/{vid} — " + ", ".join(extras)


# ------------------------------------------------------------------ TikTok via Buffer
def gql_literal(v, enums=(), key=None):
    import re
    if isinstance(v, dict):
        return "{" + " ".join(f"{k}: {gql_literal(x, enums, k)}" for k, x in v.items()) + "}"
    if isinstance(v, list):
        return "[" + " ".join(gql_literal(x, enums) for x in v) + "]"
    if isinstance(v, bool):
        return "true" if v else "false"
    if isinstance(v, (int, float)):
        return str(v)
    if key in enums:
        if not re.fullmatch(r"[A-Za-z_]+", str(v)):
            raise ValueError("bad enum value")
        return str(v)
    return json.dumps(str(v), ensure_ascii=False)


def buffer(query):
    key = secret("BUFFER_API_KEY")
    if not key:
        raise RuntimeError("BUFFER_API_KEY missing")
    r = jhttp("POST", "https://api.buffer.com", {"Authorization": f"Bearer {key}"}, {"query": query})
    if r.get("errors"):
        raise RuntimeError(f"Buffer: {r['errors']}")
    return r["data"]


_tt = None


def tiktok_channel():
    global _tt
    if _tt is None:
        for o in buffer("query { account { organizations { id name } } }")["account"]["organizations"]:
            for c in buffer("query { channels(input: {organizationId: %s}) { id name service } }" % json.dumps(o["id"]))["channels"]:
                if str(c.get("service", "")).lower() == "tiktok":
                    _tt = (c["id"], c.get("name")); break
            if _tt:
                break
    if not _tt:
        raise RuntimeError("no TikTok channel connected in Buffer")
    return _tt


def tt_publish(meta, mp4, slot, mode):
    if mode not in ("live", "now"):
        return None, "skipped in private mode"
    url = public_url(mp4, os.path.basename(mp4))
    ch = tiktok_channel()
    t = meta.get("tiktok") or {}
    video = {"url": url, "metadata": {"thumbnailOffset": int(t.get("cover_ms", 0))}}
    inp = {"text": t["caption"], "channelId": ch[0], "schedulingType": "automatic", "mode": "customScheduled",
           "dueAt": utc(slot), "assets": [{"video": video}]}
    if mode == "now":
        inp["mode"] = "shareNow"; inp.pop("dueAt")
    q = ("mutation { createPost(input: %s) { ... on PostActionSuccess { post { id dueAt } } "
         "... on MutationError { message } } }") % gql_literal(inp, enums={"schedulingType", "mode"})
    r = buffer(q)["createPost"]
    if "post" not in r:
        raise RuntimeError(f"createPost: {r.get('message')}")
    return r["post"]["id"], ("sent now" if mode == "now" else f"scheduled in Buffer {slot.astimezone(STZ):%d %b %H:%M}")


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
    if mode not in ("check", "private", "live", "now", "retry", "thumbs"):
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
        if "tiktok" in PLATFORMS:
            try:
                note("notice", f"check tiktok: Buffer channel OK — {tiktok_channel()[1]}")
                note("notice", f"check release storage: {release().get('html_url', 'ok')}")
            except Exception as e:
                bad += 1; note("error", f"check tiktok: {redact(e)}")
        if "facebook" in PLATFORMS:
            try:
                note("notice", f"check facebook: {fb_check()}")
            except Exception as e:
                bad += 1; note("error", f"check facebook: {redact(e)}")

    if mode == "thumbs":
        tok, done = None, 0
        for jpg in sorted(glob.glob(os.path.join(media, "t", "*.jpg"))):
            ep = os.path.basename(jpg)[:-4]
            vid = state["posts"].get(ep, {}).get("done", {}).get("youtube")
            if not vid:
                bad += 1; note("error", f"{ep}: no YouTube video recorded for this Short"); continue
            if os.path.getsize(jpg) > 2_000_000:
                bad += 1; note("error", f"{ep}: thumbnail larger than 2 MB"); continue
            try:
                tok = tok or yt_token()
                attempt(lambda: http("POST", f"https://www.googleapis.com/upload/youtube/v3/thumbnails/set?videoId={vid}",
                                     {"Authorization": f"Bearer {tok}", "Content-Type": "image/jpeg"}, open(jpg, "rb").read()))
                os.remove(jpg); done += 1
                note("notice", f"{ep} youtube: new thumbnail set on https://youtube.com/shorts/{vid}")
            except Exception as e:
                bad += 1; note("error", f"{ep} youtube thumbnail: {redact(e)}")
        if done:
            push_branch(media, BR["media"], "shorts thumbnails set", squash=True)
        summary(f"### Shorts thumbnails\nset: {done}, problems: {bad}")
        return 1 if bad else 0

    metas = sorted(glob.glob(os.path.join(media, "s", "*.json")))
    for mf in metas:
        name = os.path.basename(mf)
        try:
            meta = json.load(open(mf, encoding="utf-8"))
        except Exception as e:
            bad += 1; note("error", f"{name}: invalid JSON ({e})"); continue
        mp4, jpg = mf[:-5] + ".mp4", mf[:-5] + ".jpg"
        errs = validate_meta(meta, name) + validate_files(mp4, jpg)
        if "tiktok" in PLATFORMS:
            cap = (meta.get("tiktok") or {}).get("caption", "")
            if not isinstance(cap, str) or not 10 <= len(cap) <= 2200:
                errs.append("tiktok.caption: 10-2200 characters")
        if "facebook" in PLATFORMS:
            fd = (meta.get("facebook") or {}).get("description", "")
            if not isinstance(fd, str) or not 10 <= len(fd) <= 5000:
                errs.append("facebook.description: 10-5000 characters")
        if errs:
            bad += 1; note("error", f"{name}: " + "; ".join(errs)); continue
        ep, slot = meta["id"], datetime.fromisoformat(meta["slot"])
        rec = state["posts"].setdefault(ep, {"n": meta["n"], "slot": meta["slot"], "done": {}, "errors": {}})
        if mode == "check":
            note("notice", f"{ep}: files OK, slot {slot.astimezone(STZ):%d %b %H:%M}, posted on: {', '.join(rec['done']) or 'none'}")
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
        todo = [p for p in PLATFORMS if p not in rec["done"]]
        if not todo:
            continue
        if m == "live" and slot < now + timedelta(minutes=15):
            bad += 1
            for p in todo:
                rec["errors"][p] = "slot too close or past"
            note("error", f"{ep}: slot {meta['slot']} is too close or past; not posted on {', '.join(todo)}"); continue
        if mode != "retry":
            rec["mode"] = m
        for p in todo:
            try:
                if p == "youtube":
                    pid, info = attempt(yt_publish, meta, mp4, jpg, slot, m)
                elif p == "facebook":
                    pid, info = attempt(fb_publish, meta, mp4, jpg, slot, m)
                else:
                    tmp4 = mf[:-5] + "_tt.mp4"
                    pid, info = attempt(tt_publish, meta, tmp4 if os.path.isfile(tmp4) else mp4, slot, m)
                    if pid is None:
                        note("notice", f"{ep} {p}: {info}"); continue
                rec["done"][p] = pid
                rec["errors"].pop(p, None)
                note("notice", f"{ep} {p}: OK {info}")
            except Exception as e:
                bad += 1
                rec["errors"][p] = redact(e)[:400]
                note("error", f"{ep} {p}: {redact(e)}")
        rec["updated"] = now.isoformat()

    if mode != "check":
        cutoff = now - timedelta(days=90)
        state["posts"] = {k: v for k, v in state["posts"].items() if datetime.fromisoformat(v["slot"]) > cutoff}
        json.dump(state, open(sp, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        push_branch(state_d, BR["state"], f"shorts publish ({mode})")
        removed = 0
        for mf in metas:          # posted everywhere (or private test) -> files no longer needed on the media branch
            ep = os.path.basename(mf)[:-5]
            rec = state["posts"].get(ep, {})
            if all(p in rec.get("done", {}) for p in PLATFORMS) or rec.get("mode") == "private":
                for f in glob.glob(mf[:-5] + "*"):
                    os.remove(f); removed += 1
        if removed:
            push_branch(media, BR["media"], f"shorts media cleanup ({mode})", squash=True)
        if "tiktok" in PLATFORMS:
            cleanup_release()
    summary(f"### Shorts publish ({mode})\nfiles: {len(metas)}, platforms: {', '.join(PLATFORMS)}, problems: {bad}")
    return 1 if bad else 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as e:
        note("error", f"shorts publish failed: {redact(e)}")
        sys.exit(1)
