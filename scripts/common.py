"""Shared helpers for the Exportain reel workflows.

Security rules every script follows:
  * Secrets come from environment variables only, are never printed, never put in URLs.
  * Runtime tokens (e.g. a YouTube access token) are masked in the GitHub log at once.
  * Every message that can reach a log or an annotation goes through redact().
  * Files from the data branches (content / audio / media / state) are untrusted DATA:
    they are validated and never executed.
"""
import hashlib, json, os, re, shutil, subprocess, urllib.error, urllib.parse, urllib.request
from datetime import datetime, timedelta, timezone

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CFG = json.load(open(os.path.join(ROOT, "config.json"), encoding="utf-8"))
TZ = timezone(timedelta(hours=CFG["timezone_offset_hours"]))

SECRET_NAMES = ["ELEVENLABS_API_KEY", "YT_CLIENT_ID", "YT_CLIENT_SECRET", "YT_REFRESH_TOKEN",
                "FB_PAGE_ID", "FB_PAGE_TOKEN", "FB_APP_SECRET", "BUFFER_API_KEY"]
_runtime = []
IN_ACTIONS = bool(os.environ.get("GITHUB_ACTIONS"))


# ------------------------------------------------------------------ secrets & logging
def secret(name):
    return (os.environ.get(name) or "").strip()


def mask(value):
    if value:
        _runtime.append(value)
        if IN_ACTIONS:
            print(f"::add-mask::{value}", flush=True)


def redact(text):
    text = str(text)
    for v in [secret(n) for n in SECRET_NAMES] + _runtime:
        if v and len(v) >= 6:
            text = text.replace(v, "***")
    return re.sub(r"(access_token|api_key|key|token|secret|proof)=([^&\s\"']+)", r"\1=***", text, flags=re.I)


def log(*a):
    print(redact(" ".join(str(x) for x in a)), flush=True)


def note(level, msg):
    """GitHub annotation (notice / warning / error). Claude reads these through the API."""
    msg = redact(msg)
    if IN_ACTIONS:
        enc = msg.replace("%", "%25").replace("\r", "").replace("\n", "%0A")
        print(f"::{level}::{enc}", flush=True)
    else:
        print(f"[{level}] {msg}", flush=True)


def summary(md):
    p = os.environ.get("GITHUB_STEP_SUMMARY")
    if p:
        open(p, "a", encoding="utf-8").write(redact(md) + "\n")


# ------------------------------------------------------------------ HTTP
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
        detail = e.read()[:600].decode("utf-8", "replace")
        raise RuntimeError(redact(f"HTTP {e.code} {method} {url.split('?')[0]}: {detail}")) from None
    except urllib.error.URLError as e:
        raise RuntimeError(redact(f"network error {method} {url.split('?')[0]}: {e.reason}")) from None


def jhttp(method, url, headers=None, data=None, timeout=300):
    return json.loads(http(method, url, headers, data, timeout) or b"{}")


# ------------------------------------------------------------------ git data branches
def git(*args, cwd=ROOT, check=True):
    r = subprocess.run(["git", *args], cwd=cwd, capture_output=True, text=True)
    if check and r.returncode:
        raise RuntimeError(redact(f"git {' '.join(args[:2])} failed: {r.stderr.strip()[:300]}"))
    return r.stdout.strip()


def branch_dir(branch):
    """Check a data branch out into .work/<branch> (an empty orphan if it doesn't exist yet)."""
    d = os.path.join(ROOT, ".work", branch)
    if os.path.isdir(d):
        git("worktree", "remove", "--force", d, check=False)
    shutil.rmtree(d, ignore_errors=True)
    os.makedirs(os.path.dirname(d), exist_ok=True)
    git("worktree", "prune", check=False)
    exists = subprocess.run(["git", "ls-remote", "--exit-code", "--heads", "origin", branch], cwd=ROOT,
                            capture_output=True).returncode == 0
    if exists:
        git("fetch", "--depth", "1", "origin", f"+refs/heads/{branch}:refs/remotes/origin/{branch}")
        git("worktree", "add", "--force", "-B", f"local-{branch}", d, f"origin/{branch}")
    else:
        git("worktree", "add", "--force", "--orphan", "-b", f"local-{branch}", d)
    return d


def push_branch(d, branch, message, squash=False):
    """Commit everything in the worktree and push. squash=True keeps a single commit (no history growth)."""
    git("add", "-A", cwd=d)
    if not git("status", "--porcelain", cwd=d) and not squash:
        return False
    ident = ["-c", "user.name=exportain-bot", "-c", "user.email=exportain-bot@users.noreply.github.com"]
    if squash:
        tree = git("write-tree", cwd=d)
        commit = git(*ident, "commit-tree", tree, "-m", message, cwd=d)
        git("push", "--force", "origin", f"{commit}:refs/heads/{branch}", cwd=d)
    else:
        git(*ident, "commit", "-q", "-m", message, cwd=d)
        for i in range(5):           # another job may have pushed meanwhile (different files): rebase and retry
            if subprocess.run(["git", "push", "origin", f"HEAD:refs/heads/{branch}"], cwd=d,
                              capture_output=True).returncode == 0:
                break
            git("fetch", "-q", "origin", branch, cwd=d)
            git(*ident, "rebase", "-q", f"origin/{branch}", cwd=d)
        else:
            raise RuntimeError(f"push to {branch} failed after retries")
    return True


# ------------------------------------------------------------------ validation
SLUG = re.compile(r"[a-z0-9][a-z0-9-]{2,60}")
TAKE_ID = re.compile(r"[0-9]{2}_[a-z0-9_]{1,30}")
TAG = re.compile(r"^\s*\[[a-z ]{2,20}\]\s*")


def is_bangla(text):
    """True when the spoken text (tags removed) is Bangla script: no Latin letters, >= 90% of letters Bengali."""
    spoken = TAG.sub("", str(text))
    if re.search(r"[A-Za-z]", spoken):
        return False
    letters = [c for c in spoken if c.isalpha()]
    return bool(letters) and sum("\u0980" <= c <= "\u09FF" for c in letters) / len(letters) >= 0.9


BN_DIGITS = str.maketrans("০১২৩৪৫৬৭৮৯", "0123456789")


def prompt_numbers(content_dir):
    """Script numbers available in the owner's prompt file ('### ০৫৭. title'), from start_script on, as '057'."""
    p = os.path.join(content_dir, CFG["prompts_file"])
    if not os.path.isfile(p):
        return []
    nums = []
    for line in open(p, encoding="utf-8"):
        m = re.match(r"###\s*([০-৯0-9]{3})\.", line)
        if m:
            n = int(m.group(1).translate(BN_DIGITS))
            if n >= CFG.get("start_script", 1):
                nums.append(f"{n:03d}")
    return nums


def text_hash(s):
    return hashlib.sha256(s.encode("utf-8")).hexdigest()[:16]


def validate_narration(nar):
    """narration.json = [{"id": "00_hook", "text": "..."}] in the skill's format."""
    errs = []
    if not isinstance(nar, list) or not 2 <= len(nar) <= 45:
        return ["narration must be a list of 2-45 takes"]
    seen, total = set(), 0
    for i, t in enumerate(nar):
        if not isinstance(t, dict):
            errs.append(f"take {i} is not an object"); continue
        tid, text = str(t.get("id", "")), str(t.get("text", ""))
        if not TAKE_ID.fullmatch(tid) or tid in seen:
            errs.append(f"take {i}: id '{tid}' must look like 00_hook and be unique")
        seen.add(tid)
        spoken = TAG.sub("", text)
        if not 5 <= len(spoken) <= 400:
            errs.append(f"{tid}: text length {len(spoken)} (want 5-400)")
        if "/" in spoken:
            errs.append(f"{tid}: contains '/' — write it out in Bangla (B/L -> বি এল)")
        if not is_bangla(text):
            errs.append(f"{tid}: must be Bangla only (Bangla script, English terms written in Bangla, no Latin letters)")
        total += len(spoken)
    if total > CFG["max_voice_chars_per_episode"]:
        errs.append(f"total {total} characters > limit {CFG['max_voice_chars_per_episode']}")
    return errs


def _txt(d, key, lo, hi, errs, where, no_angle=False):
    v = d.get(key, "")
    if not isinstance(v, str) or not lo <= len(v) <= hi:
        errs.append(f"{where}.{key}: {lo}-{hi} characters")
    elif no_angle and re.search(r"[<>]", v):
        errs.append(f"{where}.{key}: no < or >")


def x_weighted_len(text):
    """X (Twitter) weighted length: most scripts incl. Bangla count 1, others (emoji, CJK) 2, URLs 23."""
    text = re.sub(r"https?://\S+", "x" * 23, text)
    n = 0
    for ch in text:
        o = ord(ch)
        n += 1 if (o <= 4351 or 8192 <= o <= 8205 or 8208 <= o <= 8223 or 8242 <= o <= 8247) else 2
    return n


def parse_slot(s):
    t = datetime.fromisoformat(str(s))
    if t.tzinfo is None:
        raise ValueError("slot needs a timezone")
    return t


def validate_meta(meta, name):
    """media/v/<id>.json written by Claude for each finished video."""
    errs = []
    if not isinstance(meta, dict):
        return [f"{name}: not an object"]
    if not SLUG.fullmatch(str(meta.get("id", ""))) or f"{meta.get('id')}.json" != name:
        errs.append(f"{name}: id must be a slug equal to the file name")
    if not re.fullmatch(r"[0-9]{3,4}", str(meta.get("script", ""))):
        errs.append(f"{name}: script must be the script number, e.g. 007")
    try:
        parse_slot(meta.get("slot"))
    except Exception:
        errs.append(f"{name}: slot must be an ISO time with timezone")
    yt, fb, tt = meta.get("youtube") or {}, meta.get("facebook") or {}, meta.get("tiktok") or {}
    _txt(yt, "title", 1, 95, errs, "youtube", True)
    _txt(yt, "description", 1, 4500, errs, "youtube", True)
    tags = yt.get("tags", [])
    if not isinstance(tags, list) or len(",".join(map(str, tags))) > 450 or not all(isinstance(x, str) for x in tags):
        errs.append("youtube.tags: list of strings, 450 characters in total")
    _txt(fb, "title", 1, 100, errs, "facebook")
    _txt(fb, "description", 1, 2000, errs, "facebook")
    _txt(tt, "caption", 1, 2000, errs, "tiktok")
    buf = CFG["platforms"].get("buffer", {})
    if buf.get("linkedin", {}).get("enabled"):
        _txt(meta.get("linkedin") or {}, "text", 1, 2900, errs, "linkedin")
    if buf.get("twitter", {}).get("enabled"):
        t = (meta.get("twitter") or {}).get("text", "")
        if not isinstance(t, str) or not 1 <= x_weighted_len(t) <= 275:
            errs.append("twitter.text: 1-275 weighted characters (X counts emoji and some scripts double)")
    return errs


def probe(path):
    out = subprocess.check_output(["ffprobe", "-v", "error", "-show_entries",
                                   "format=duration:stream=codec_type,codec_name,width,height",
                                   "-of", "json", path]).decode()
    return json.loads(out)


def validate_files(mp4, jpg):
    errs, lim = [], CFG["video_limits"]
    if not os.path.isfile(mp4):
        return [f"video missing: {os.path.basename(mp4)}"]
    if os.path.getsize(mp4) > lim["max_mb"] * 1e6:
        errs.append("video too large")
    want = 16 / 9 if lim.get("aspect", "16:9") == "16:9" else 9 / 16
    try:
        p = probe(mp4)
        v = next(s for s in p["streams"] if s["codec_type"] == "video")
        dur = float(p["format"]["duration"])
        if v["codec_name"] not in ("h264", "hevc"):
            errs.append(f"video codec {v['codec_name']} (need h264)")
        if abs(v["width"] / v["height"] - want) > 0.01 or min(v["width"], v["height"]) < 720:
            errs.append(f"video is {v['width']}x{v['height']} (need {lim.get('aspect')}, e.g. 1920x1080)")
        if not lim["min_seconds"] <= dur <= lim["max_seconds"]:
            errs.append(f"video is {dur:.0f}s (need {lim['min_seconds']}-{lim['max_seconds']}s, i.e. 3-5 minutes)")
        if not any(s["codec_type"] == "audio" for s in p["streams"]):
            errs.append("video has no audio")
    except Exception as e:
        errs.append(f"cannot read video: {e}")
    if not os.path.isfile(jpg):
        errs.append(f"thumbnail missing: {os.path.basename(jpg)}")
    elif os.path.getsize(jpg) > lim["thumb_max_mb"] * 1e6:
        errs.append("thumbnail larger than 2 MB")
    return errs
