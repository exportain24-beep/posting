#!/usr/bin/env python3
"""Exportain reel pipeline: episode JSON -> ElevenLabs voice -> rendered 9:16 reel -> YouTube / Facebook / TikTok (Buffer).

Commands
  pipeline.py run                 full automatic run (used by GitHub Actions)
  pipeline.py preview EP.json OUT render one episode locally (no publishing; --fake-voice skips ElevenLabs)
  pipeline.py validate [FILES]    check episode files

Security rules this file follows
  * Secrets are read from environment variables only, never from files or CLI args, and never printed.
  * Any derived token (e.g. a YouTube access token) is masked in the GitHub log immediately.
  * Every error message passes through redact() before it is logged.
  * Episode files are untrusted DATA: they are validated and only ever inserted as escaped text.
"""
import json, os, re, sys, time, glob, shutil, subprocess, tempfile, hashlib, urllib.request, urllib.parse, urllib.error
from datetime import datetime, timedelta, timezone
from multiprocessing import Pool

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CFG = json.load(open(os.path.join(ROOT, "config.json"), encoding="utf-8"))
FONTDIR = os.path.join(ROOT, "assets", "fonts")
LOGO = os.path.join(ROOT, "assets", "logo.png")
TZ = timezone(timedelta(hours=CFG["timezone_offset_hours"]))

SECRET_NAMES = ["ELEVENLABS_API_KEY", "YT_CLIENT_ID", "YT_CLIENT_SECRET", "YT_REFRESH_TOKEN",
                "FB_PAGE_ID", "FB_PAGE_TOKEN", "FB_APP_SECRET", "BUFFER_API_KEY"]
_extra_secrets = []


def secret(name):
    return (os.environ.get(name) or "").strip()


def mask(value):
    """Hide a runtime value in GitHub Actions logs."""
    if value:
        _extra_secrets.append(value)
        if os.environ.get("GITHUB_ACTIONS"):
            print(f"::add-mask::{value}", flush=True)


def redact(text):
    text = str(text)
    for v in [secret(n) for n in SECRET_NAMES] + _extra_secrets:
        if v and len(v) >= 6:
            text = text.replace(v, "***")
    text = re.sub(r"(access_token|key|token|secret)=([^&\s\"']+)", r"\1=***", text, flags=re.I)
    return text


def log(*a):
    print(redact(" ".join(str(x) for x in a)), flush=True)


def summary(md):
    p = os.environ.get("GITHUB_STEP_SUMMARY")
    if p:
        open(p, "a", encoding="utf-8").write(redact(md) + "\n")


# ---------------------------------------------------------------- HTTP helpers
def http(method, url, headers=None, data=None, timeout=300, want_headers=False):
    if isinstance(data, (dict, list)):
        data = json.dumps(data).encode()
        headers = {**(headers or {}), "Content-Type": "application/json"}
    req = urllib.request.Request(url, data=data, method=method, headers=headers or {})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            body = r.read()
            return (body, dict(r.headers)) if want_headers else body
    except urllib.error.HTTPError as e:
        detail = e.read()[:800].decode("utf-8", "replace")
        raise RuntimeError(redact(f"HTTP {e.code} {method} {url.split('?')[0]}: {detail}")) from None


def jhttp(method, url, headers=None, data=None, timeout=300):
    return json.loads(http(method, url, headers, data, timeout) or b"{}")


# ---------------------------------------------------------------- episodes
TEXT_LIMITS = {"title": 140, "kicker": 40, "body": 220, "narration": 600, "caption": 600}


def validate_episode(ep, name="episode"):
    errs = []
    req = lambda c, m: errs.append(m) if not c else None
    req(isinstance(ep, dict), "not an object")
    if errs:
        return errs
    req(re.fullmatch(r"[a-z0-9][a-z0-9-]{3,80}", str(ep.get("id", ""))), "id must be lowercase-slug")
    req(ep.get("audience") in ("seller", "provider", "buyer", "general"), "audience invalid")
    req(ep.get("theme", "light") in ("light", "dark", "navy"), "theme invalid")
    sc = ep.get("scenes") or []
    req(3 <= len(sc) <= 9, "need 3-9 scenes")
    for i, s in enumerate(sc):
        req(s.get("kind") in ("hook", "point", "stat", "steps", "cta"), f"scene {i} kind invalid")
        n = str(s.get("narration", ""))
        req(n.strip(), f"scene {i} narration missing")
        req("/" not in n, f"scene {i} narration contains '/' (write it out in Bangla)")
        req(not re.search(r"[A-Za-z]{2,}", n), f"scene {i} narration has Latin letters (write English terms in Bangla script)")
        for k, lim in TEXT_LIMITS.items():
            req(len(str(s.get(k, ""))) <= lim, f"scene {i} {k} too long (>{lim})")
        req(len(s.get("bullets") or []) <= 4, f"scene {i} max 4 bullets")
    req(sc and sc[-1].get("kind") == "cta", "last scene must be kind=cta")
    total_chars = sum(len(s.get("narration", "")) for s in sc)
    req(200 <= total_chars <= 1300, f"narration total {total_chars} chars (want 200-1300, about 25-85 s)")
    yt = ep.get("youtube") or {}
    req(0 < len(yt.get("title", "")) <= 95 and not re.search(r"[<>]", yt.get("title", "")), "youtube.title 1-95 chars, no < >")
    req(len(yt.get("description", "")) <= 4500 and not re.search(r"[<>]", yt.get("description", "")), "youtube.description too long or has < >")
    req(len(",".join(yt.get("tags") or [])) <= 450, "youtube.tags too long")
    req(0 < len((ep.get("facebook") or {}).get("description", "")) <= 2000, "facebook.description 1-2000 chars")
    req(0 < len((ep.get("tiktok") or {}).get("caption", "")) <= 2000, "tiktok.caption 1-2000 chars")
    th = ep.get("thumbnail") or {}
    req(0 < len(th.get("headline", "")) <= 70, "thumbnail.headline 1-70 chars")
    return [f"{name}: {e}" for e in errs]


# ---------------------------------------------------------------- voice
def tts(text, out_mp3):
    key = secret("ELEVENLABS_API_KEY")
    if not key:
        raise RuntimeError("ELEVENLABS_API_KEY is not set")
    url = (f"https://api.elevenlabs.io/v1/text-to-speech/{CFG['voice_id']}"
           f"?output_format={urllib.parse.quote(CFG['tts_output_format'])}")
    body = {"text": text, "model_id": CFG["tts_model_id"]}
    if CFG.get("tts_language_code"):
        body["language_code"] = CFG["tts_language_code"]
    audio = http("POST", url, {"xi-api-key": key, "Accept": "audio/mpeg"}, body, timeout=180)
    open(out_mp3, "wb").write(audio)


def duration(path):
    out = subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                                   "-of", "default=nw=1:nk=1", path]).decode().strip()
    return float(out)


def fake_voice(text, out_wav):
    secs = max(2.0, len(text) / 14.0)
    subprocess.check_call(["ffmpeg", "-y", "-loglevel", "error", "-f", "lavfi", "-i",
                           f"sine=frequency=220:duration={secs:.2f}", "-af", "volume=0.05", out_wav])


def chunk_caption(text, dur):
    words = text.split()
    chunks, cur = [], []
    for w in words:
        cur.append(w)
        if len(" ".join(cur)) >= 34 or w.endswith(("।", "?", "!")):
            chunks.append(" ".join(cur)); cur = []
    if cur:
        chunks.append(" ".join(cur))
    total = sum(len(c) for c in chunks) or 1
    t, res = 0.0, []
    for c in chunks:
        d = dur * len(c) / total
        res.append({"t0": round(t, 3), "t1": round(t + d, 3), "text": c}); t += d
    return res


# ---------------------------------------------------------------- render
def _page_html(template, work):
    html = open(os.path.join(ROOT, "templates", template), encoding="utf-8").read()
    html = html.replace("__FONTDIR__", "file://" + FONTDIR)
    p = os.path.join(work, template)
    open(p, "w", encoding="utf-8").write(html)
    return p


def _open(p, html, data, w, h):
    b = p.chromium.launch(args=["--force-color-profile=srgb", "--disable-gpu"])
    pg = b.new_page(viewport={"width": w, "height": h})
    pg.goto("file://" + html)
    pg.evaluate("(d) => window.__init(d)", data)
    pg.evaluate("document.fonts.ready")
    pg.wait_for_timeout(300)
    return b, pg


def _render_worker(args):
    html, plan, f0, f1, out = args
    from playwright.sync_api import sync_playwright
    v = CFG["video"]
    ff = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "image2pipe", "-framerate", str(v["fps"]),
                           "-c:v", "mjpeg", "-i", "-", "-c:v", "libx264", "-preset", "medium", "-crf", str(v["crf"]),
                           "-pix_fmt", "yuv420p", "-r", str(v["fps"]), out], stdin=subprocess.PIPE)
    with sync_playwright() as p:
        b, pg = _open(p, html, plan, v["width"], v["height"])
        for f in range(f0, f1):
            pg.evaluate("(t) => window.__render(t)", f / v["fps"])
            ff.stdin.write(pg.screenshot(type="jpeg", quality=92))
        b.close()
    ff.stdin.close()
    if ff.wait():
        raise RuntimeError("ffmpeg frame encode failed")
    return out


def render_video(plan, out, work):
    v = CFG["video"]
    html = _page_html("reel.html", work)
    frames = int(round(plan["total"] * v["fps"]))
    n = max(1, min(4, os.cpu_count() or 1))
    step = -(-frames // n)
    parts = [(html, plan, i * step, min(frames, (i + 1) * step), os.path.join(work, f"part{i}.mp4"))
             for i in range(n) if i * step < frames]
    with Pool(len(parts)) as pool:
        files = pool.map(_render_worker, parts)
    lst = os.path.join(work, "parts.txt")
    open(lst, "w").write("".join(f"file '{f}'\n" for f in files))
    subprocess.check_call(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", lst, "-c", "copy", out])


def render_still(template, data, out, w, h, quality=90):
    from playwright.sync_api import sync_playwright
    work = tempfile.mkdtemp(prefix="still_")
    html = _page_html(template, work)
    with sync_playwright() as p:
        b, pg = _open(p, html, data, w, h)
        if template == "reel.html":
            pg.evaluate("(t) => window.__render(t)", 0.0)
        pg.screenshot(path=out, type="jpeg", quality=quality)
        b.close()


def build_audio(voice_files, starts, total, mood, out, work):
    music = os.path.join(work, "music.wav")
    subprocess.check_call([sys.executable, os.path.join(ROOT, "scripts", "music_bed.py"), "--duration", f"{total:.2f}",
                           "--mood", mood, "--out", music, "--seed", str(int(time.time()) % 97)])
    cmd = ["ffmpeg", "-y", "-loglevel", "error"]
    for f in voice_files:
        cmd += ["-i", f]
    cmd += ["-i", music]
    parts, labels = [], []
    for i, s in enumerate(starts):
        ms = int(s * 1000)
        parts.append(f"[{i}:a]aresample=48000,aformat=channel_layouts=stereo,adelay={ms}|{ms}[v{i}]")
        labels.append(f"[v{i}]")
    m = len(voice_files)
    parts.append(f"{''.join(labels)}amix=inputs={m}:normalize=0,apad,atrim=0:{total:.3f}[voice]")
    parts.append("[voice]asplit=2[vk][vo]")
    parts.append(f"[{m}:a]aresample=48000,aformat=channel_layouts=stereo,volume={CFG['music_volume']},atrim=0:{total:.3f}[mus]")
    parts.append("[mus][vk]sidechaincompress=threshold=0.03:ratio=6:attack=20:release=350[duck]")
    parts.append("[vo][duck]amix=inputs=2:normalize=0,loudnorm=I=-14:TP=-1.5:LRA=11,aresample=48000[out]")
    cmd += ["-filter_complex", ";".join(parts), "-map", "[out]", "-c:a", "pcm_s16le", out]
    subprocess.check_call(cmd)


def produce(ep, outdir, fake=False):
    """Episode -> outdir/<id>.mp4 + outdir/<id>.jpg (YouTube thumbnail). Returns paths."""
    os.makedirs(outdir, exist_ok=True)
    work = tempfile.mkdtemp(prefix="ep_")
    pad, lead = CFG["scene_pad_seconds"], CFG["voice_start_seconds"]
    t, scenes, voice_files, starts = 0.0, [], [], []
    for i, s in enumerate(ep["scenes"]):
        f = os.path.join(work, f"v{i}." + ("wav" if fake else "mp3"))
        (fake_voice if fake else tts)(s["narration"], f)
        d = duration(f)
        dur = lead + d + pad + (0.9 if s["kind"] == "cta" else 0)
        cap_text = s.get("caption") or s["narration"]
        scenes.append({**{k: s.get(k) for k in ("kind", "icon", "kicker", "title", "body", "bullets", "stat", "url", "sub")},
                       "start": round(t, 3), "dur": round(dur, 3),
                       "captions": [{"t0": c["t0"] + lead, "t1": c["t1"] + lead, "text": c["text"]} for c in chunk_caption(cap_text, d)]})
        voice_files.append(f); starts.append(t + lead); t += dur
    total = round(t, 3)
    plan = {"theme": ep.get("theme", "light"), "logo": "file://" + LOGO, "scenes": scenes, "total": total}
    silent = os.path.join(work, "silent.mp4"); render_video(plan, silent, work)
    audio = os.path.join(work, "mix.wav"); build_audio(voice_files, starts, total, ep.get("mood", "hopeful"), audio, work)
    mp4 = os.path.join(outdir, f"{ep['id']}.mp4")
    subprocess.check_call(["ffmpeg", "-y", "-loglevel", "error", "-i", silent, "-i", audio, "-map", "0:v", "-map", "1:a",
                           "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-ac", "2",
                           "-movflags", "+faststart", "-shortest", mp4])
    th = ep.get("thumbnail") or {}
    jpg = os.path.join(outdir, f"{ep['id']}.jpg")
    render_still("thumb.html", {"logo": "file://" + LOGO, "headline": th.get("headline", ""), "chip": th.get("chip", ""),
                                "sub": th.get("sub", "exportain.com"), "icon": th.get("icon", "")}, jpg, 1280, 720)
    shutil.rmtree(work, ignore_errors=True)
    return mp4, jpg, total


# ---------------------------------------------------------------- publishers
def youtube_publish(ep, mp4, jpg, publish_at):
    cid, csec, rtok = secret("YT_CLIENT_ID"), secret("YT_CLIENT_SECRET"), secret("YT_REFRESH_TOKEN")
    if not (cid and csec and rtok):
        raise RuntimeError("YouTube secrets missing")
    tok = jhttp("POST", "https://oauth2.googleapis.com/token", {"Content-Type": "application/x-www-form-urlencoded"},
                urllib.parse.urlencode({"client_id": cid, "client_secret": csec, "refresh_token": rtok,
                                        "grant_type": "refresh_token"}).encode())["access_token"]
    mask(tok)
    auth = {"Authorization": f"Bearer {tok}"}
    yt = ep["youtube"]
    title = yt["title"] if "#shorts" in yt["title"].lower() else (yt["title"] + " #Shorts")[:100]
    meta = {"snippet": {"title": title, "description": yt.get("description", ""), "tags": yt.get("tags", []),
                        "categoryId": CFG["platforms"]["youtube"]["category_id"], "defaultLanguage": "bn",
                        "defaultAudioLanguage": "bn"},
            "status": {"privacyStatus": "private", "publishAt": publish_at.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.000Z"),
                       "selfDeclaredMadeForKids": False,
                       "containsSyntheticMedia": CFG["platforms"]["youtube"]["contains_synthetic_media"]}}
    size = os.path.getsize(mp4)
    _, hdr = http("POST", "https://www.googleapis.com/upload/youtube/v3/videos?uploadType=resumable&part=snippet,status",
                  {**auth, "X-Upload-Content-Type": "video/mp4", "X-Upload-Content-Length": str(size)}, meta,
                  want_headers=True)
    loc = hdr.get("Location") or hdr.get("location")
    vid = json.loads(http("PUT", loc, {**auth, "Content-Type": "video/mp4", "Content-Length": str(size)},
                          open(mp4, "rb").read(), timeout=900))["id"]
    try:
        http("POST", f"https://www.googleapis.com/upload/youtube/v3/thumbnails/set?videoId={vid}",
             {**auth, "Content-Type": "image/jpeg"}, open(jpg, "rb").read())
    except Exception as e:  # unverified channels cannot set custom thumbnails; the video itself is fine
        log("YouTube thumbnail not set:", e)
    return vid


def facebook_publish(ep, mp4, publish_at):
    page, token, app_secret = secret("FB_PAGE_ID"), secret("FB_PAGE_TOKEN"), secret("FB_APP_SECRET")
    if not (page and token):
        raise RuntimeError("Facebook secrets missing")
    gv = CFG["platforms"]["facebook"]["graph_version"]
    auth = {"Authorization": f"OAuth {token}"}  # token in a header, never in the URL
    proof = {}
    if app_secret:  # appsecret_proof: a leaked page token alone is useless when "Require app secret" is on
        import hmac
        proof = {"appsecret_proof": hmac.new(app_secret.encode(), token.encode(), hashlib.sha256).hexdigest()}
    form = lambda d: urllib.parse.urlencode({**d, **proof}).encode()
    hform = {**auth, "Content-Type": "application/x-www-form-urlencoded"}
    start = jhttp("POST", f"https://graph.facebook.com/{gv}/{page}/video_reels", hform, form({"upload_phase": "start"}))
    vid = start["video_id"]
    size = os.path.getsize(mp4)
    http("POST", f"https://rupload.facebook.com/video-upload/{gv}/{vid}",
         {**auth, "offset": "0", "file_size": str(size), "Content-Type": "application/octet-stream"},
         open(mp4, "rb").read(), timeout=900)
    lead = (publish_at - datetime.now(timezone.utc)).total_seconds()
    params = {"upload_phase": "finish", "video_id": vid, "description": ep["facebook"]["description"]}
    if 11 * 60 < lead < 28 * 86400:
        params.update({"video_state": "SCHEDULED", "scheduled_publish_time": str(int(publish_at.timestamp()))})
    else:
        params["video_state"] = "PUBLISHED"
    res = jhttp("POST", f"https://graph.facebook.com/{gv}/{page}/video_reels", hform, form(params))
    if not res.get("success", True):
        raise RuntimeError(f"Facebook finish failed: {res}")
    return vid


def gql_literal(v, enums=(), key=None):
    """Python value -> GraphQL input literal. Strings are JSON-escaped, so content cannot break out of them."""
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
            raise ValueError("bad enum")
        return str(v)
    return json.dumps(str(v), ensure_ascii=False)


def buffer_gql(query, variables=None):
    key = secret("BUFFER_API_KEY")
    if not key:
        raise RuntimeError("BUFFER_API_KEY missing")
    res = jhttp("POST", "https://api.buffer.com", {"Authorization": f"Bearer {key}"},
                {"query": query, "variables": variables or {}})
    if res.get("errors"):
        raise RuntimeError(f"Buffer error: {res['errors']}")
    return res["data"]


def buffer_tiktok_channel():
    orgs = buffer_gql("query { account { organizations { id name } } }")["account"]["organizations"]
    for o in orgs:
        chans = buffer_gql("query { channels(input: {organizationId: %s}) { id name service } }"
                           % json.dumps(o["id"]))["channels"]
        for c in chans:
            if str(c.get("service", "")).lower() == "tiktok":
                return c["id"]
    raise RuntimeError("No TikTok channel connected in Buffer")


def tiktok_publish(ep, video_url, publish_at, channel_id):
    q = ("mutation { createPost(input: %s) { ... on PostActionSuccess { post { id dueAt } } "
         "... on MutationError { message } } }")
    inp = {"text": ep["tiktok"]["caption"], "channelId": channel_id, "schedulingType": "automatic",
           "mode": "customScheduled", "dueAt": publish_at.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.000Z"),
           "assets": [{"video": {"url": video_url,
                                 "metadata": {"thumbnailOffset": CFG["platforms"]["tiktok_via_buffer"]["thumbnail_offset_ms"]}}}]}
    r = buffer_gql(q % gql_literal(inp, enums={"schedulingType", "mode"}))["createPost"]
    if "post" not in r:
        raise RuntimeError(f"Buffer createPost failed: {r.get('message')}")
    return r["post"]["id"]


# ---------------------------------------------------------------- scheduling & state
def upcoming_slots(now):
    res = []
    day = now.astimezone(TZ).date()
    end = now + timedelta(hours=CFG["horizon_hours"])
    lead = timedelta(minutes=CFG["min_lead_minutes"])
    for d in range(0, CFG["horizon_hours"] // 24 + 2):
        for hm in CFG["slots_local"]:
            h, m = map(int, hm.split(":"))
            s = datetime(day.year, day.month, day.day, h, m, tzinfo=TZ) + timedelta(days=d)
            if now + lead <= s <= end:
                res.append(s)
    return sorted(res)


def git(*args, cwd=ROOT, check=True):
    return subprocess.run(["git", *args], cwd=cwd, check=check, capture_output=True, text=True).stdout.strip()


def branch_dir(branch):
    """Check out a data branch into its own folder (created empty if the branch does not exist yet)."""
    d = os.path.join(ROOT, ".work", branch)
    shutil.rmtree(d, ignore_errors=True); os.makedirs(os.path.dirname(d), exist_ok=True)
    exists = subprocess.run(["git", "ls-remote", "--exit-code", "--heads", "origin", branch], cwd=ROOT,
                            capture_output=True).returncode == 0
    if exists:
        git("fetch", "--depth", "1", "origin", f"+refs/heads/{branch}:refs/remotes/origin/{branch}")
        git("worktree", "add", "--force", "-B", f"local-{branch}", d, f"origin/{branch}")
    else:
        git("worktree", "add", "--force", "--orphan", "-b", f"local-{branch}", d)
    return d


def push_branch(d, branch, message, force=False):
    git("add", "-A", cwd=d)
    if not git("status", "--porcelain", cwd=d):
        return
    git("-c", "user.name=exportain-bot", "-c", "user.email=actions@users.noreply.github.com",
        "commit", "-m", message, cwd=d)
    git("push", *(["--force"] if force else []), "origin", f"local-{branch}:{branch}", cwd=d)


def cmd_run():
    dry = os.environ.get("DRY_RUN") == "1"
    now = datetime.now(timezone.utc)
    repo = os.environ.get("GITHUB_REPOSITORY", "")
    content, state_dir = branch_dir("content"), branch_dir("state")
    state_file = os.path.join(state_dir, "posts.json")
    state = json.load(open(state_file, encoding="utf-8")) if os.path.exists(state_file) else {"posts": [], "used": []}
    used = set(state["used"])
    taken = {p["slot"] for p in state["posts"]}
    plat = CFG["platforms"]
    enabled = {"youtube": plat["youtube"]["enabled"] and bool(secret("YT_REFRESH_TOKEN")),
               "facebook": plat["facebook"]["enabled"] and bool(secret("FB_PAGE_TOKEN")),
               "tiktok": plat["tiktok_via_buffer"]["enabled"] and bool(secret("BUFFER_API_KEY"))}
    log("Platforms active:", ", ".join(k for k, v in enabled.items() if v) or "none")
    if not dry and not any(enabled.values()):
        log("No platform secrets are available, so nothing would be posted. Stopping.")
        summary("### Stopped\nNo platform secrets found in the `production` environment.")
        return 1

    # queue = episode files on the content branch that were not used yet, oldest first
    queue, bad = [], []
    for f in sorted(glob.glob(os.path.join(content, "queue", "*.json"))):
        try:
            ep = json.load(open(f, encoding="utf-8"))
        except Exception as e:
            bad.append(f"{os.path.basename(f)}: invalid JSON ({e})"); continue
        errs = validate_episode(ep, os.path.basename(f))
        if errs:
            bad += errs; continue
        if ep["id"] not in used:
            queue.append(ep)
    for b in bad:
        log("SKIPPED", b)

    free = [s for s in upcoming_slots(now) if s.isoformat() not in taken][:CFG["max_new_per_run"]]
    log(f"Free slots: {len(free)}  queued episodes: {len(queue)}")
    media = branch_dir("media")
    os.makedirs(os.path.join(media, "v"), exist_ok=True)
    # keep only videos whose post is still upcoming (Buffer needs the link until it publishes)
    keep = {p["episode"] for p in state["posts"] if datetime.fromisoformat(p["slot"]) > now - timedelta(hours=12)}
    for f in glob.glob(os.path.join(media, "v", "*")):
        if os.path.splitext(os.path.basename(f))[0] not in keep:
            os.remove(f)

    made = []
    for slot in free:
        if not queue:
            break
        ep = queue.pop(0)
        log(f"Producing {ep['id']} for {slot.isoformat()}")
        try:
            mp4, jpg, total = produce(ep, os.path.join(media, "v"), fake=os.environ.get("FAKE_VOICE") == "1")
        except Exception as e:
            log("RENDER FAILED", ep["id"], e); bad.append(f"{ep['id']}: render failed: {redact(e)}"); continue
        made.append((slot, ep, mp4, jpg, total))
        used.add(ep["id"])

    if dry:
        out = os.path.join(ROOT, "preview"); os.makedirs(out, exist_ok=True)
        for _, ep, mp4, jpg, _ in made:
            shutil.copy(mp4, out); shutil.copy(jpg, out)
        summary(f"### Dry run\nRendered {len(made)} video(s). Nothing was published.")
        return 0 if not bad else 1

    if made:
        push_branch(media, "media", "media for upcoming posts", force=True)  # history is not kept: repo stays small
    ttch = None
    for slot, ep, mp4, jpg, total in made:
        rec = {"slot": slot.isoformat(), "episode": ep["id"], "seconds": total, "done": {}, "errors": {}}
        if enabled["youtube"]:
            try: rec["done"]["youtube"] = youtube_publish(ep, mp4, jpg, slot)
            except Exception as e: rec["errors"]["youtube"] = redact(e)
        if enabled["facebook"]:
            try: rec["done"]["facebook"] = facebook_publish(ep, mp4, slot)
            except Exception as e: rec["errors"]["facebook"] = redact(e)
        if enabled["tiktok"]:
            try:
                ttch = ttch or buffer_tiktok_channel()
                url = f"https://raw.githubusercontent.com/{repo}/media/v/{ep['id']}.mp4"
                rec["done"]["tiktok"] = tiktok_publish(ep, url, slot, ttch)
            except Exception as e: rec["errors"]["tiktok"] = redact(e)
        for k, v in rec["errors"].items():
            log(f"{ep['id']} {k} FAILED: {v}")
        if rec["done"]:
            state["posts"].append(rec)
        else:  # nothing was posted: free the slot and keep the episode for the next run
            used.discard(ep["id"])
            bad.append(f"{ep['id']}: every platform failed, will retry next run")
    state["used"] = sorted(used)
    state["posts"] = [p for p in state["posts"] if datetime.fromisoformat(p["slot"]) > now - timedelta(days=45)]
    json.dump(state, open(state_file, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    push_branch(state_dir, "state", f"posted {len(made)} episode(s)")

    lines = ["### Exportain reels", f"Scheduled this run: **{len(made)}**, episodes left in queue: **{len(queue)}**", ""]
    for slot, ep, *_ in made:
        rec = next((p for p in state["posts"] if p["episode"] == ep["id"]), {"done": {}, "errors": {"all": 1}})
        lines.append(f"- {slot.astimezone(TZ):%a %d %b %H:%M} — `{ep['id']}` — ok: {', '.join(rec['done']) or 'none'}"
                     + (f" — failed: {', '.join(rec['errors'])}" if rec["errors"] else ""))
    lines += [f"- skipped: {b}" for b in bad]
    if len(queue) < CFG["min_queue_warning"]:
        lines.append(f"\n**Queue is low ({len(queue)}).** Claude's content task should refill it.")
    summary("\n".join(lines))
    failed = bad or any(p["errors"] for p in state["posts"] if p["episode"] in {e["id"] for _, e, *_ in made})
    no_content = free and not made
    return 1 if (failed or no_content) else 0  # a failed run makes GitHub email the repo owner


def main():
    a = sys.argv[1:]
    if not a:
        print(__doc__); return 2
    if a[0] == "validate":
        files = a[1:] or sorted(glob.glob(os.path.join(ROOT, "content", "queue", "*.json")))
        errs = []
        for f in files:
            try:
                errs += validate_episode(json.load(open(f, encoding="utf-8")), os.path.basename(f))
            except Exception as e:
                errs.append(f"{f}: {e}")
        print("\n".join(errs) or f"OK: {len(files)} file(s) valid")
        return 1 if errs else 0
    if a[0] == "preview":
        ep = json.load(open(a[1], encoding="utf-8"))
        errs = validate_episode(ep)
        if errs:
            print("\n".join(errs)); return 1
        mp4, jpg, total = produce(ep, a[2], fake="--fake-voice" in a)
        print(f"{mp4} ({total:.1f}s)\n{jpg}"); return 0
    if a[0] == "run":
        try:
            return cmd_run()
        except Exception as e:
            log("FATAL:", e); return 1
    print(__doc__); return 2


if __name__ == "__main__":
    sys.exit(main())
