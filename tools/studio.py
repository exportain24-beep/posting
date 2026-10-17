#!/usr/bin/env python3
"""Claude's side of the pipeline (runs in Claude's workspace, never on GitHub, never sees a secret).

  studio.py status                         scripts left, next script number, free slots, pending videos
  studio.py add-scripts FILE...            put the user's numbered scripts into content/scripts/
  studio.py voice EP DIR [--test-tone]     push DIR/narration.json, run the Voice workflow, fetch DIR/vo + durations.json
  studio.py deliver EP DIR [--mode M] [--meta post.json]  push DIR/final.mp4 + thumb.jpg + meta.json (+captions.srt) to media, run Publish
  studio.py publish MODE                   run Publish only (check | private | live)
  studio.py pages                          make sure GitHub Pages serves the media branch
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
    """DIR must hold final.mp4 (16:9, 3-5 min), thumb.jpg (1280x720), meta.json, optional captions.srt."""
    meta = json.load(open(os.path.join(d, meta_name), encoding="utf-8"))
    meta["id"] = ep
    mp4, thumb = os.path.join(d, "final.mp4"), os.path.join(d, "thumb.jpg")
    errs = validate_meta(meta, f"{ep}.json") + validate_files(mp4, thumb)
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
    srt = os.path.join(d, "captions.srt")
    if os.path.isfile(srt):
        shutil.copy(srt, v + ".srt")
    if CFG["platforms"]["buffer"].get("twitter", {}).get("enabled"):
        make_teaser(mp4, v + "_x.mp4", CFG["video_limits"]["x_teaser_seconds"])
    json.dump(meta, open(v + ".json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    push_branch(md, "media", f"video {ep}", squash=True)
    print("media pushed")
    ok, _ = run_workflow("publish.yml", {"mode": mode})
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
    elif c == "styles":
        cmd_styles()
    elif c == "log-style":
        cmd_log_style(a[1], a[2])
    else:
        print(__doc__); return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
