#!/usr/bin/env python3
"""Claude's side of the pipeline (runs in Claude's workspace, never on GitHub, never sees a secret).

  studio.py status                         scripts left, next script number, free slots, pending videos
  studio.py add-scripts FILE...            put the user's numbered scripts into content/scripts/
  studio.py voice EP DIR [--test-tone]     push DIR/narration.json, run the Voice workflow, fetch DIR/vo + durations.json
  studio.py deliver EP DIR [--mode M] [--meta post.json]  push DIR/final.mp4 + thumb.jpg + meta.json (+captions.srt) to media, run Publish
  studio.py publish MODE                   run Publish only (check | private | live)
  studio.py pages                          make sure GitHub Pages serves the media branch
  studio.py ig MODE [EP]                   Instagram job: check | slots (fire and forget) | now EP (waits)
  studio.py styles                         last 12 entries of the visual style log (read before designing)
  studio.py log-style EP "TEXT"            append what this video looked like + lessons learned

Results of every GitHub run are read back from the run's annotations.
"""
import glob, json, os, shutil, subprocess, sys, time
from datetime import datetime, timedelta, timezone

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(HERE), "scripts"))
from common import (CFG, ROOT, SLUG, TZ, branch_dir, prompt_numbers, parse_slot, push_branch, validate_files, validate_meta,
                    validate_narration)

REPO = "exportain24-beep/posting"


def gh(*args, check=True):
    r = subprocess.run(["gh", "api", *args], capture_output=True, text=True)
    if check and r.returncode:
        raise SystemExit(f"gh api {args[0]} failed: {(r.stderr or r.stdout).strip()[:400]}")
    return json.loads(r.stdout) if r.stdout.strip().startswith(("{", "[")) else r.stdout


def dispatch(wf, inputs):
    """Start a workflow and return at once (Instagram waits on the runner until the slot)."""
    args = ["-X", "POST", f"repos/{REPO}/actions/workflows/{wf}/dispatches", "-f", "ref=main"]
    for k, v in inputs.items():
        args += ["-f", f"inputs[{k}]={v}"]
    gh(*args)
    print(f"{wf}: started {inputs}")


def ig_cover(thumb, out):
    """9:16 cover for Instagram: the 16:9 thumbnail centred on a blurred copy of itself."""
    subprocess.check_call(["ffmpeg", "-y", "-loglevel", "error", "-i", thumb, "-filter_complex",
                           "[0]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,boxblur=30:3,"
                           "eq=brightness=0.06[bg];[0]scale=1080:-2[fg];[bg][fg]overlay=0:(H-h)/2",
                           "-frames:v", "1", "-q:v", "3", out])


def ig_mp4(src, out):
    """Instagram-ready copy (AAC 128 kbps / 48 kHz, video untouched), served by GitHub Pages as video_url."""
    subprocess.check_call(["ffmpeg", "-y", "-loglevel", "error", "-i", src, "-c:v", "copy", "-c:a", "aac", "-b:a", "128k",
                           "-ar", "48000", "-ac", "2", "-movflags", "+faststart", out])


COVER_HOLD = 0.5   # seconds of cover at the start of final.mp4 (cover.py --prepend --hold 0.5)


def vertical(src, cover, vframe, out, hold=COVER_HOLD):
    """9:16 copy for Facebook / Instagram / TikTok / X: the 16:9 video (its own cover cut off) in the middle of the
    colourful vframe.jpg, with the platform's 9:16 cover as the first frames (TikTok/Buffer takes the first frame)."""
    subprocess.check_call([
        "ffmpeg", "-y", "-loglevel", "error", "-loop", "1", "-t", str(hold), "-framerate", "30", "-i", cover,
        "-loop", "1", "-framerate", "30", "-i", vframe, "-ss", str(hold), "-i", src, "-filter_complex",
        "[2:v]scale=1080:608,setsar=1[v];[1:v]scale=1080:1920,setsar=1[bg];[bg][v]overlay=0:656:shortest=1,"
        "format=yuv420p[m];[0:v]scale=1080:1920,setsar=1,format=yuv420p[c];[c][m]concat=n=2:v=1:a=0[vo];"
        f"[2:a]adelay={int(hold*1000)}|{int(hold*1000)}[ao]",
        "-map", "[vo]", "-map", "[ao]", "-c:v", "libx264", "-crf", "21", "-preset", "veryfast", "-r", "30",
        "-c:a", "aac", "-b:a", "128k", "-ar", "48000", "-ac", "2", "-movflags", "+faststart", out])


def vsize(src):
    w, h = subprocess.check_output(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=width,height",
                                    "-of", "csv=p=0:s=x", src]).decode().strip().split("x")[:2]
    return int(w), int(h)


def duration(src):
    return float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                                          "-of", "default=nw=1:nk=1", src]).decode())


def recover(src, cover, out, hold=COVER_HOLD):
    """Same video (16:9 or 9:16) with a different cover in the first frames (platform copies)."""
    w, h = vsize(src)
    subprocess.check_call([
        "ffmpeg", "-y", "-loglevel", "error", "-loop", "1", "-t", str(hold), "-framerate", "30", "-i", cover,
        "-ss", str(hold), "-i", src, "-filter_complex",
        f"[0:v]scale={w}:{h},setsar=1,format=yuv420p[c];[1:v]scale={w}:{h},setsar=1,format=yuv420p[v];"
        f"[c][v]concat=n=2:v=1:a=0[vo];[1:a]adelay={int(hold*1000)}|{int(hold*1000)}[ao]",
        "-map", "[vo]", "-map", "[ao]", "-c:v", "libx264", "-crf", "21", "-preset", "veryfast", "-r", "30",
        "-c:a", "aac", "-b:a", "160k", "-ar", "48000", "-movflags", "+faststart", out])


def run_workflow(wf, inputs, timeout_min=40):
    t0 = datetime.now(timezone.utc) - timedelta(seconds=15)
    args = ["-X", "POST", f"repos/{REPO}/actions/workflows/{wf}/dispatches", "-f", "ref=main"]
    for k, v in inputs.items():
        args += ["-f", f"inputs[{k}]={v}"]
    gh(*args)
    run = None
    for _ in range(30):
        time.sleep(6)
        runs = gh(f"repos/{REPO}/actions/workflows/{wf}/runs?event=workflow_dispatch&per_page=5")["workflow_runs"]
        runs = [r for r in runs if datetime.fromisoformat(r["created_at"].replace("Z", "+00:00")) >= t0]
        if runs:
            run = runs[-1]; break
    if not run:
        raise SystemExit(f"{wf}: run did not start")
    print(f"{wf}: run {run['id']} started", flush=True)
    end = time.time() + timeout_min * 60
    while time.time() < end:
        run = gh(f"repos/{REPO}/actions/runs/{run['id']}")
        if run["status"] == "completed":
            break
        time.sleep(15)
    notes = []
    for j in gh(f"repos/{REPO}/actions/runs/{run['id']}/jobs")["jobs"]:
        for a in gh(f"repos/{REPO}/check-runs/{j['id']}/annotations"):
            if not a["message"].startswith("Process completed with exit code"):
                notes.append(f"{a['annotation_level']}: {a['message']}")
    print(f"{wf}: {run['status']} / {run.get('conclusion')}")
    print("\n".join(notes) or "(no notes)")
    return run.get("conclusion") == "success", notes


def load_state():
    sd = branch_dir("state")
    p = os.path.join(sd, "posts.json")
    return json.load(open(p, encoding="utf-8")) if os.path.isfile(p) else {"posts": {}}


def pending_media(md):
    out = {}
    for f in glob.glob(os.path.join(md, "v", "*.json")):
        try:
            m = json.load(open(f, encoding="utf-8")); out[m["id"]] = m
        except Exception:
            pass
    return out


def free_slots(taken, now):
    res, day = [], now.astimezone(TZ).date()
    for d in range(0, CFG["plan_ahead_hours"] // 24 + 2):
        for hm in CFG["slots_local"]:
            h, m = map(int, hm.split(":"))
            s = datetime(day.year, day.month, day.day, h, m, tzinfo=TZ) + timedelta(days=d)
            if now + timedelta(minutes=CFG["min_lead_minutes"]) <= s <= now + timedelta(hours=CFG["plan_ahead_hours"]) \
                    and s.isoformat() not in taken:
                res.append(s.isoformat())
    return res


def cmd_status():
    now = datetime.now(timezone.utc)
    state, md, cd = load_state(), branch_dir("media"), branch_dir("content")
    media = pending_media(md)
    scripts = prompt_numbers(cd)
    used = {r.get("script") for r in state["posts"].values()} | {m.get("script") for m in media.values()}
    taken = {parse_slot(r["slot"]).astimezone(TZ).isoformat() for r in state["posts"].values()} | \
            {parse_slot(m["slot"]).astimezone(TZ).isoformat() for m in media.values()}
    unused = [s for s in scripts if s not in used]
    info = {"now_local": now.astimezone(TZ).isoformat(timespec="minutes"),
            "scripts_total": len(scripts), "scripts_unused": unused[:10], "scripts_left": len(unused),
            "next_script": unused[0] if unused else None,
            "free_slots": free_slots(taken, now),
            "pending_videos": {k: {"slot": v["slot"], "posted": list(state["posts"].get(k, {}).get("done", {}))}
                               for k, v in media.items()},
            "recent_errors": {k: v["errors"] for k, v in state["posts"].items() if v.get("errors")}}
    print(json.dumps(info, ensure_ascii=False, indent=1))


def cmd_add_scripts(files):
    cd = branch_dir("content")
    os.makedirs(os.path.join(cd, "scripts"), exist_ok=True)
    for f in files:
        name = os.path.basename(f)
        if not (name.endswith(".txt") and name[:-4].isdigit() and len(name[:-4]) in (3, 4)):
            raise SystemExit(f"{name}: scripts must be named 001.txt, 002.txt ...")
        shutil.copy(f, os.path.join(cd, "scripts", name))
    push_branch(cd, "content", f"add scripts {', '.join(map(os.path.basename, files))}")
    print("pushed", len(files), "script(s)")


def cmd_voice(ep, d, test):
    if not SLUG.fullmatch(ep):
        raise SystemExit("episode name must be a lowercase slug")
    nar = json.load(open(os.path.join(d, "narration.json"), encoding="utf-8"))
    errs = validate_narration(nar)
    if errs:
        raise SystemExit("narration problems:\n" + "\n".join(errs))
    cd = branch_dir("content")
    vd = os.path.join(cd, "voice", ep)
    os.makedirs(vd, exist_ok=True)
    json.dump(nar, open(os.path.join(vd, "narration.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    push_branch(cd, "content", f"voice request {ep}")
    ok, _ = run_workflow("voice.yml", {"episode": ep, "test_tone": "true" if test else "false"})
    if not ok:
        raise SystemExit("voice workflow failed (see notes above)")
    ad = branch_dir("audio")
    src = os.path.join(ad, ep)
    os.makedirs(os.path.join(d, "vo"), exist_ok=True)
    for f in glob.glob(os.path.join(src, "vo", "*.mp3")):
        shutil.copy(f, os.path.join(d, "vo", os.path.basename(f)))
    shutil.copy(os.path.join(src, "durations.json"), os.path.join(d, "durations.json"))
    print(f"audio ready in {d}/vo ({len(nar)} takes)")


def make_teaser(src, out, seconds):
    """First N seconds for X (free accounts: max 140 s), with a short fade out."""
    fade = max(0.0, seconds - 1.5)
    subprocess.check_call(["ffmpeg", "-y", "-loglevel", "error", "-i", src, "-t", str(seconds),
                           "-vf", f"fade=t=out:st={fade}:d=1.5", "-af", f"afade=t=out:st={fade}:d=1.5",
                           "-c:v", "libx264", "-crf", "21", "-preset", "medium", "-c:a", "aac", "-b:a", "160k",
                           "-movflags", "+faststart", out])


def cmd_deliver(ep, d, mode, meta_name="meta.json"):
    """DIR must hold final.mp4 (9:16 1080x1920, 90-150 s, burned-in subtitles; limits in config.json), thumb.jpg
    (1280x720), the post meta (--meta), optional captions.srt (subs.srt is used when present)."""
    meta = json.load(open(os.path.join(d, meta_name), encoding="utf-8"))
    meta["id"] = ep
    mp4, thumb = os.path.join(d, "final.mp4"), os.path.join(d, "thumb.jpg")
    errs = validate_meta(meta, f"{ep}.json") + validate_files(mp4, thumb)
    for f in ("thumb_li.jpg", "thumb_fb.jpg", "thumb_tt.jpg"):
        p = os.path.join(d, f)
        if os.path.isfile(p) and os.path.getsize(p) > CFG["video_limits"]["thumb_max_mb"] * 1e6:
            errs.append(f"{f} larger than 2 MB")
    if mode == "now":
        meta["slot"] = (datetime.now(timezone.utc) + timedelta(hours=1)).astimezone(TZ).isoformat(timespec="minutes")
    if parse_slot(meta["slot"]) < datetime.now(timezone.utc) + timedelta(minutes=20):
        errs.append("slot is less than 20 minutes away")
    if errs:
        raise SystemExit("cannot deliver:\n" + "\n".join(errs))
    now = datetime.now(timezone.utc)
    state, md = load_state(), branch_dir("media")
    os.makedirs(os.path.join(md, "v"), exist_ok=True)
    open(os.path.join(md, ".nojekyll"), "w").close()
    want = 2 + sum(1 for v in CFG["platforms"]["buffer"].values() if v.get("enabled"))
    for m in pending_media(md).values():   # keep what is not fully posted yet (Buffer reads the URLs)
        rec = state["posts"].get(m["id"], {})
        posted_all = len(rec.get("done", {})) >= want or rec.get("mode") == "private"
        if posted_all and parse_slot(m["slot"]) < now - timedelta(hours=24):
            for f in glob.glob(os.path.join(md, "v", f"{m['id']}*")):
                os.remove(f)
    v = os.path.join(md, "v", ep)
    shutil.copy(mp4, v + ".mp4")
    shutil.copy(thumb, v + ".jpg")
    srt = os.path.join(d, "subs.srt")
    if not os.path.isfile(srt):
        srt = os.path.join(d, "captions.srt")
    if os.path.isfile(srt):
        shutil.copy(srt, v + ".srt")
    th = {k: os.path.join(d, f) for k, f in (("li", "thumb_li.jpg"), ("fb", "thumb_fb.jpg"), ("tt", "thumb_tt.jpg"),
                                             ("vf", "vframe.jpg"))}
    w, h = vsize(mp4)
    li9 = os.path.join(d, "thumb_li9.jpg")
    if h > w and all(os.path.isfile(th[k]) for k in ("fb", "tt")):   # native 9:16 reel: only the covers change
        print("making platform copies: Facebook/Instagram, TikTok, LinkedIn (9:16, own covers) …")
        recover(mp4, th["fb"], v + "_ig.mp4")
        recover(mp4, th["tt"], v + "_tt.mp4")
        if CFG["platforms"]["buffer"].get("linkedin", {}).get("enabled"):
            if not os.path.isfile(li9):
                ig_cover(th["li"], li9)          # 16:9 English cover centred on its own blur
            recover(mp4, li9, v + "_li.mp4")
        shutil.copy(th["fb"], v + "_fb.jpg"); shutil.copy(th["fb"], v + "_ig.jpg")
        x_src = v + "_ig.mp4"
    elif all(os.path.isfile(p) for p in th.values()):   # per-platform covers (tools/thumbs.py): 9:16 for FB/IG/TikTok/X
        print("making platform copies: 9:16 (Facebook/Instagram, TikTok, X) + 16:9 LinkedIn …")
        vertical(mp4, th["fb"], th["vf"], v + "_ig.mp4")          # Facebook + Instagram
        vertical(mp4, th["tt"], th["vf"], v + "_tt.mp4")          # TikTok
        recover(mp4, th["li"], v + "_li.mp4")                     # LinkedIn
        shutil.copy(th["fb"], v + "_fb.jpg"); shutil.copy(th["fb"], v + "_ig.jpg")
        x_src = v + "_ig.mp4"
    else:
        if CFG["platforms"].get("instagram", {}).get("enabled"):
            ig_cover(thumb, v + "_ig.jpg")
            ig_mp4(mp4, v + "_ig.mp4")
        x_src = mp4
    if CFG["platforms"]["buffer"].get("twitter", {}).get("enabled"):
        make_teaser(x_src, v + "_x.mp4", min(CFG["video_limits"]["x_teaser_seconds"], duration(x_src)))
    json.dump(meta, open(v + ".json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    push_branch(md, "media", f"video {ep}", squash=True)
    print("media pushed")
    ok, _ = run_workflow("publish.yml", {"mode": mode})
    if CFG["platforms"].get("instagram", {}).get("enabled"):
        if mode == "now":
            ok = run_workflow("ig.yml", {"mode": "now", "episode": ep}, timeout_min=45)[0] and ok
        elif mode == "live":
            dispatch("ig.yml", {"mode": "slots"})
    st = load_state()["posts"].get(ep)
    print(json.dumps(st, ensure_ascii=False, indent=1) if st else "(no state record)")
    return 0 if ok else 1


def cmd_pages():
    r = subprocess.run(["gh", "api", f"repos/{REPO}/pages"], capture_output=True, text=True)
    if r.returncode == 0:
        print("Pages:", json.loads(r.stdout).get("source")); return
    r = subprocess.run(["gh", "api", "-X", "POST", f"repos/{REPO}/pages", "-f", "source[branch]=media", "-f", "source[path]=/"],
                       capture_output=True, text=True)
    print("enable Pages:", (r.stdout or r.stderr).strip()[:300])


def cmd_styles():
    p = os.path.join(branch_dir("content"), "style_log.md")
    lines = open(p, encoding="utf-8").read().strip().split("\n## ") if os.path.isfile(p) else []
    print(("## " + "\n## ".join(lines[-12:])) if lines else "(no style log yet)")


def cmd_log_style(ep, text):
    cd = branch_dir("content")
    p = os.path.join(cd, "style_log.md")
    with open(p, "a", encoding="utf-8") as f:
        f.write(f"\n## {ep} ({datetime.now(TZ):%Y-%m-%d %H:%M})\n{text.strip()}\n")
    push_branch(cd, "content", f"style log {ep}")
    print("style logged")


def main():
    a = sys.argv[1:]
    if not a:
        print(__doc__); return 2
    c = a[0]
    if c == "status":
        cmd_status()
    elif c == "add-scripts":
        cmd_add_scripts(a[1:])
    elif c == "voice":
        cmd_voice(a[1], a[2], "--test-tone" in a)
    elif c == "deliver":
        mode = a[a.index("--mode") + 1] if "--mode" in a else "live"
        meta = a[a.index("--meta") + 1] if "--meta" in a else "meta.json"
        return cmd_deliver(a[1], a[2], mode, meta)
    elif c == "publish":
        ok, _ = run_workflow("publish.yml", {"mode": a[1]})
        return 0 if ok else 1
    elif c == "pages":
        cmd_pages()
    elif c == "ig":
        if a[1] == "slots":
            dispatch("ig.yml", {"mode": "slots"})
        else:
            ok, _ = run_workflow("ig.yml", {"mode": a[1], "episode": a[2] if len(a) > 2 else ""}, timeout_min=45)
            return 0 if ok else 1
    elif c == "styles":
        cmd_styles()
    elif c == "log-style":
        cmd_log_style(a[1], a[2])
    else:
        print(__doc__); return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
