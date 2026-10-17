#!/usr/bin/env python3
"""Publish job (GitHub Actions): media:v/<id>.{mp4,jpg,json}  ->  YouTube + Facebook (direct API), TikTok (Buffer).

MODE=check    read-only: verifies every platform login and the media files, posts nothing
MODE=private  YouTube private, Facebook draft, TikTok skipped (safe first test)
MODE=live     schedules each video at its slot on all three platforms

Results go to state:posts.json and to GitHub annotations (Claude reads both).
"""
import hashlib, hmac, json, os, sys, time, glob, uuid, urllib.parse
from datetime import datetime, timedelta, timezone

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import (CFG, TZ, branch_dir, http, jhttp, log, mask, note, parse_slot, push_branch, redact, secret,
                    summary, validate_files, validate_meta)

PL = CFG["platforms"]


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


def utc(t):
    return t.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.000Z")


# ------------------------------------------------------------------ YouTube (direct API)
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
    scopes = info.get("scope", "")
    extra = [s for s in scopes.split() if not s.endswith("youtube.upload")]
    return f"login OK, scopes: {scopes.replace('https://www.googleapis.com/auth/', '')}" + \
           (" (more than upload — consider upload-only)" if extra else "")


def yt_publish(meta, mp4, jpg, slot, mode):
    tok = yt_token()
    auth = {"Authorization": f"Bearer {tok}"}
    y = meta["youtube"]
    title = y["title"] if "#shorts" in y["title"].lower() else (y["title"] + " #Shorts")[:100]
    status = {"privacyStatus": "private", "selfDeclaredMadeForKids": False,
              "containsSyntheticMedia": PL["youtube"]["contains_synthetic_media"]}
    if mode == "live":
        status["publishAt"] = utc(slot)
    body = {"snippet": {"title": title, "description": y["description"], "tags": y.get("tags", []),
                        "categoryId": PL["youtube"]["category_id"], "defaultLanguage": "bn", "defaultAudioLanguage": "bn"},
            "status": status}
    size = os.path.getsize(mp4)
    _, hdr = http("POST", "https://www.googleapis.com/upload/youtube/v3/videos?uploadType=resumable&part=snippet,status",
                  {**auth, "X-Upload-Content-Type": "video/mp4", "X-Upload-Content-Length": str(size)}, body,
                  want_headers=True)
    loc = hdr.get("Location") or hdr.get("location")
    vid = json.loads(http("PUT", loc, {**auth, "Content-Type": "video/mp4", "Content-Length": str(size)},
                          open(mp4, "rb").read(), timeout=1200))["id"]
    thumb = "set"
    try:
        http("POST", f"https://www.googleapis.com/upload/youtube/v3/thumbnails/set?videoId={vid}",
             {**auth, "Content-Type": "image/jpeg"}, open(jpg, "rb").read())
    except Exception as e:
        thumb = f"not set ({redact(e)[:160]})"
    return vid, f"thumbnail {thumb}"


# ------------------------------------------------------------------ Facebook (direct API)
def _proof(app_secret, tok):
    return {"appsecret_proof": hmac.new(app_secret.encode(), tok.encode(), hashlib.sha256).hexdigest()} if app_secret else {}


def fb_auth():
    """FB_PAGE_TOKEN may be the System User token (recommended) or a Page token.
    Either way the Page token is fetched fresh from it, so the user never handles a Page token."""
    page, tok, app_secret = secret("FB_PAGE_ID"), secret("FB_PAGE_TOKEN"), secret("FB_APP_SECRET")
    if not (page and tok):
        raise RuntimeError("Facebook secrets missing")
    g = f"https://graph.facebook.com/{PL['facebook']['graph_version']}"
    q = urllib.parse.urlencode({"fields": "access_token", **_proof(app_secret, tok)})
    page_tok = jhttp("GET", f"{g}/{page}?{q}", {"Authorization": f"OAuth {tok}"}).get("access_token")
    if not page_tok:
        raise RuntimeError("could not get the Page token — does the system user have full control of the Page?")
    mask(page_tok)
    return page, {"Authorization": f"OAuth {page_tok}"}, _proof(app_secret, page_tok), g


def fb_check():
    page, auth, proof, g = fb_auth()
    q = urllib.parse.urlencode({"fields": "id,name", **proof})
    p = jhttp("GET", f"{g}/{page}?{q}", auth)
    return f"page OK: {p.get('name')}" + ("" if proof else " (FB_APP_SECRET not set — add it)")


def fb_publish(meta, mp4, jpg, slot, mode):
    page, auth, proof, g = fb_auth()
    form = lambda d: urllib.parse.urlencode({**d, **proof}).encode()
    hf = {**auth, "Content-Type": "application/x-www-form-urlencoded"}
    vid = jhttp("POST", f"{g}/{page}/video_reels", hf, form({"upload_phase": "start"}))["video_id"]
    size = os.path.getsize(mp4)
    http("POST", f"https://rupload.facebook.com/video-upload/{PL['facebook']['graph_version']}/{vid}",
         {**auth, "offset": "0", "file_size": str(size), "Content-Type": "application/octet-stream"},
         open(mp4, "rb").read(), timeout=1200)
    f = meta["facebook"]
    params = {"upload_phase": "finish", "video_id": vid, "title": f["title"], "description": f["description"]}
    lead = (slot - datetime.now(timezone.utc)).total_seconds()
    if mode == "private":
        params["video_state"] = "DRAFT"
    elif 11 * 60 < lead < 28 * 86400:
        params.update({"video_state": "SCHEDULED", "scheduled_publish_time": str(int(slot.timestamp()))})
    else:
        params["video_state"] = "PUBLISHED"
    res = jhttp("POST", f"{g}/{page}/video_reels", hf, form(params))
    if res.get("success") is False:
        raise RuntimeError(f"finish failed: {res}")
    thumb = "set"
    try:
        body, ctype = multipart({"is_preferred": "true", **proof}, {"source": ("cover.jpg", open(jpg, "rb").read(), "image/jpeg")})
        http("POST", f"{g}/{vid}/thumbnails", {**auth, "Content-Type": ctype}, body)
    except Exception as e:
        thumb = f"not set ({redact(e)[:160]})"
    return vid, f"{params['video_state'].lower()}, thumbnail {thumb}"


# ------------------------------------------------------------------ TikTok via Buffer
def gql_literal(v, enums=(), key=None):
    """Python value -> GraphQL literal; strings are JSON-escaped so text can't break out."""
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


BUFFER_TEXT = {"tiktok": ("tiktok", "caption"), "linkedin": ("linkedin", "text"), "twitter": ("twitter", "text")}
BUFFER_ALIASES = {"tiktok": {"tiktok"}, "linkedin": {"linkedin"}, "twitter": {"twitter", "x"}}
_chans = None


def buffer_channels():
    """{'tiktok': (id, name), 'linkedin': ..., 'twitter': ...} for every channel connected in Buffer."""
    global _chans
    if _chans is None:
        _chans = {}
        for o in buffer("query { account { organizations { id name } } }")["account"]["organizations"]:
            for c in buffer("query { channels(input: {organizationId: %s}) { id name service } }" % json.dumps(o["id"]))["channels"]:
                svc = str(c.get("service", "")).lower()
                for key, names in BUFFER_ALIASES.items():
                    if svc in names and key not in _chans:
                        _chans[key] = (c["id"], c.get("name"))
    return _chans


def buffer_check():
    ch = buffer_channels()
    out = []
    for key, conf in PL["buffer"].items():
        if conf.get("enabled"):
            out.append(f"{key}: {ch[key][1]}" if key in ch else f"{key}: NOT CONNECTED")
    if any("NOT CONNECTED" in x for x in out):
        raise RuntimeError("Buffer channels — " + "; ".join(out))
    return "Buffer channels OK — " + "; ".join(out)


def wait_public(url, size, minutes=8):
    """GitHub Pages must serve the exact file before Buffer fetches it."""
    end = time.time() + minutes * 60
    last = ""
    while time.time() < end:
        try:
            _, h = http("HEAD", url, want_headers=True, timeout=30)
            ct = h.get("Content-Type") or h.get("content-type", "")
            ln = int(h.get("Content-Length") or h.get("content-length") or 0)
            if "video/mp4" in ct and ln == size:
                return
            last = f"type {ct}, {ln} bytes"
        except Exception as e:
            last = str(e)
        time.sleep(20)
    raise RuntimeError(f"video not public yet at {url} ({last}) — is GitHub Pages on for the media branch?")


_public_ok = set()


def buffer_publish(platform, meta, mp4, slot, mode):
    if mode != "live":
        return None, "skipped in private mode"
    url = f"{CFG['pages_base_url']}/v/{meta['id']}.mp4"
    if url not in _public_ok:
        wait_public(url, os.path.getsize(mp4)); _public_ok.add(url)
    ch = buffer_channels()
    if platform not in ch:
        raise RuntimeError(f"no {platform} channel connected in Buffer")
    sec, field = BUFFER_TEXT[platform]
    video = {"url": url}
    if platform == "tiktok":
        video["metadata"] = {"thumbnailOffset": PL["buffer"]["tiktok"].get("thumbnail_offset_ms", 0)}
    inp = {"text": meta[sec][field], "channelId": ch[platform][0], "schedulingType": "automatic",
           "mode": "customScheduled", "dueAt": utc(slot), "assets": [{"video": video}]}
    q = ("mutation { createPost(input: %s) { ... on PostActionSuccess { post { id dueAt } } "
         "... on MutationError { message } } }") % gql_literal(inp, enums={"schedulingType", "mode"})
    r = buffer(q)["createPost"]
    if "post" not in r:
        raise RuntimeError(f"createPost: {r.get('message')}")
    return r["post"]["id"], "scheduled in Buffer"


# ------------------------------------------------------------------ main
def main():
    mode = os.environ.get("MODE", "check")
    if mode not in ("check", "private", "live"):
        note("error", f"publish: unknown mode {mode}"); return 1
    now = datetime.now(timezone.utc)
    media, state_d, content = branch_dir("media"), branch_dir("state"), branch_dir("content")
    sp = os.path.join(state_d, "posts.json")
    state = json.load(open(sp, encoding="utf-8")) if os.path.isfile(sp) else {"posts": {}}
    active = {"youtube": PL["youtube"]["enabled"], "facebook": PL["facebook"]["enabled"],
              **{k: bool(v.get("enabled")) for k, v in PL["buffer"].items()}}
    bad = 0

    if mode == "check":
        for name, fn in (("youtube", yt_check), ("facebook", fb_check), ("buffer", buffer_check)):
            if name != "buffer" and not active[name]:
                continue
            try:
                note("notice", f"check {name}: {fn()}")
            except Exception as e:
                bad += 1; note("error", f"check {name}: {redact(e)}")

    metas = sorted(glob.glob(os.path.join(media, "v", "*.json")))
    for mf in metas:
        name = os.path.basename(mf)
        try:
            meta = json.load(open(mf, encoding="utf-8"))
        except Exception as e:
            bad += 1; note("error", f"{name}: invalid JSON ({e})"); continue
        errs = validate_meta(meta, name)
        mp4, jpg = mf[:-5] + ".mp4", mf[:-5] + ".jpg"
        errs += validate_files(mp4, jpg)
        if errs:
            bad += 1; note("error", f"{name}: " + "; ".join(errs)); continue
        ep, slot = meta["id"], parse_slot(meta["slot"])
        rec = state["posts"].setdefault(ep, {"script": meta["script"], "slot": meta["slot"], "done": {}, "errors": {}})
        if mode == "check":
            note("notice", f"{ep}: files OK, slot {slot.astimezone(TZ):%d %b %H:%M}, posted on: {', '.join(rec['done']) or 'none'}")
            continue
        if rec.get("mode") and rec["mode"] != mode:
            note("warning", f"{ep}: already handled in {rec['mode']} mode, skipped"); continue
        todo = [p for p in active if active[p] and p not in rec["done"]]
        if not todo:
            continue
        if mode == "live" and slot < now + timedelta(minutes=15):
            bad += 1; note("error", f"{ep}: slot {meta['slot']} is too close or past; not posted on {', '.join(todo)}"); continue
        rec["mode"] = mode
        for p in todo:
            try:
                if p == "youtube":
                    pid, info = yt_publish(meta, mp4, jpg, slot, mode)
                elif p == "facebook":
                    pid, info = fb_publish(meta, mp4, jpg, slot, mode)
                else:
                    pid, info = buffer_publish(p, meta, mp4, slot, mode)
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

    # scripts left
    scripts = {os.path.basename(f)[:-4] for f in glob.glob(os.path.join(content, "scripts", "*.txt"))}
    used = {r.get("script") for r in state["posts"].values()}
    for mf in metas:
        try:
            used.add(json.load(open(mf, encoding="utf-8")).get("script"))
        except Exception:
            pass
    left = len(scripts - used)
    if left < CFG["min_scripts_warning"]:
        note("warning", f"only {left} unused script(s) left in content/scripts — add more")

    if mode != "check":
        cutoff = now - timedelta(days=60)
        state["posts"] = {k: v for k, v in state["posts"].items() if parse_slot(v["slot"]) > cutoff}
        json.dump(state, open(sp, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        push_branch(state_d, "state", f"publish ({mode})")
    summary(f"### Publish ({mode})\nvideos: {len(metas)}, problems: {bad}, unused scripts: {left}")
    return 1 if bad else 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as e:
        note("error", f"publish failed: {redact(e)}")
        sys.exit(1)
