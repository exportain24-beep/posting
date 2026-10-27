#!/usr/bin/env python3
"""Claude's side of the YouTube Shorts lane (runs in Claude's workspace, never sees a secret).
Separate from tools/studio.py and the 3-5 min reel system: own branches, own workflows, own state.

  shorts.py status                      free Short slots (06:00, 15:00, 20:00 BD), next plan items, pending, errors
  shorts.py next [K]                    the next K unused plan items in full (default 3)
  shorts.py item N                      one plan item (N = plan number, e.g. 12)
  shorts.py recent [K]                  the last K produced Shorts (title, subtopic, hook, visual) — avoid repeats
  shorts.py voice EP DIR [--test-tone]  push DIR/narration.json, run shorts-voice.yml, fetch DIR/vo + durations.json
  shorts.py deliver EP DIR [--mode M]   push DIR/final.mp4 + thumb.jpg + post.json to shorts-media, run shorts-publish.yml
  shorts.py publish MODE                run shorts-publish.yml only (check | private | live | now | retry)
  shorts.py log EP DIR                  record what was produced (script, title, visual concept) on shorts-content
  shorts.py plan-push FILE              (setup) put plan.json on shorts-content

EP = sh-<NNNN>-<bn|en>-<short-english-slug>, NNNN = plan number.
"""
import glob, json, os, shutil, subprocess, sys, time
from datetime import datetime, timedelta, timezone

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(HERE), "scripts"))
from common import branch_dir, push_branch                     # generic git helpers only
from shorts_common import BR, SCFG, SHORT_ID, STZ, short_lang, validate_files, validate_meta, validate_narration

REPO = "exportain24-beep/posting"


def gh(*args, check=True):
    r = subprocess.run(["gh", "api", *args], capture_output=True, text=True)
    if check and r.returncode:
        raise SystemExit(f"gh api {args[0]} failed: {(r.stderr or r.stdout).strip()[:400]}")
    return json.loads(r.stdout) if r.stdout.strip().startswith(("{", "[")) else r.stdout


def run_workflow(wf, inputs, timeout_min=30):
    t0 = datetime.now(timezone.utc) - timedelta(seconds=15)
    args = ["-X", "POST", f"repos/{REPO}/actions/workflows/{wf}/dispatches", "-f", "ref=main"]
    for k, v in inputs.items():
        args += ["-f", f"inputs[{k}]={v}"]
    gh(*args)
    run = None
    for _ in range(40):
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
        time.sleep(12)
    notes = []
    for j in gh(f"repos/{REPO}/actions/runs/{run['id']}/jobs")["jobs"]:
        for a in gh(f"repos/{REPO}/check-runs/{j['id']}/annotations"):
            if not a["message"].startswith("Process completed with exit code"):
                notes.append(f"{a['annotation_level']}: {a['message']}")
    print(f"{wf}: {run['status']} / {run.get('conclusion')}")
    print("\n".join(notes) or "(no notes)")
    return run.get("conclusion") == "success", notes


def load(branch, rel, default):
    p = os.path.join(branch_dir(branch), rel)
    return json.load(open(p, encoding="utf-8")) if os.path.isfile(p) else default


def plan_items():
    return load(BR["content"], "plan.json", {"shorts": []})["shorts"]


def pending_media():
    md = branch_dir(BR["media"])
    out = {}
    for f in glob.glob(os.path.join(md, "s", "*.json")):
        try:
            m = json.load(open(f, encoding="utf-8")); out[m["id"]] = m
        except Exception:
            pass
    return out


def produced():
    cd = branch_dir(BR["content"])
    out = []
    for f in sorted(glob.glob(os.path.join(cd, "produced", "*.json"))):
        try:
            out.append(json.load(open(f, encoding="utf-8")))
        except Exception:
            pass
    return out


def used_numbers(state, media):
    return {str(r.get("n")) for r in state["posts"].values()} | {str(m.get("n")) for m in media.values()}


def free_slots(taken, now):
    res, day = [], now.astimezone(STZ).date()
    for d in range(0, SCFG["plan_ahead_hours"] // 24 + 2):
        for hm in SCFG["slots_local"]:
            h, m = map(int, hm.split(":"))
            s = datetime(day.year, day.month, day.day, h, m, tzinfo=STZ) + timedelta(days=d)
            if now + timedelta(minutes=SCFG["min_lead_minutes"]) <= s <= now + timedelta(hours=SCFG["plan_ahead_hours"]) \
                    and s.isoformat() not in taken:
                res.append(s.isoformat())
    return res


def cmd_status():
    now = datetime.now(timezone.utc)
    state = load(BR["state"], "posts.json", {"posts": {}})
    media = pending_media()
    plan = plan_items()
    used = used_numbers(state, media)
    taken = {datetime.fromisoformat(r["slot"]).astimezone(STZ).isoformat() for r in state["posts"].values()} | \
            {datetime.fromisoformat(m["slot"]).astimezone(STZ).isoformat() for m in media.values()}
    unused = [p for p in plan if f"{p['n']:04d}" not in used]
    info = {"now_local": now.astimezone(STZ).isoformat(timespec="minutes"),
            "plan_total": len(plan), "shorts_left": len(unused),
            "free_slots": free_slots(taken, now),
            "next_items": [{"n": f"{p['n']:04d}", "lang": p["lang"], "keyword": p["keyword"], "subtopic": p["subtopic"]}
                           for p in unused[:4]],
            "pending": {k: {"slot": v["slot"], "youtube": state["posts"].get(k, {}).get("done", {}).get("youtube")}
                        for k, v in media.items()},
            "recent_errors": {k: v["errors"] for k, v in state["posts"].items() if v.get("errors")}}
    print(json.dumps(info, ensure_ascii=False, indent=1))


def cmd_next(k):
    state = load(BR["state"], "posts.json", {"posts": {}})
    used = used_numbers(state, pending_media())
    items = [p for p in plan_items() if f"{p['n']:04d}" not in used][:k]
    print(json.dumps(items, ensure_ascii=False, indent=1))


def cmd_item(n):
    it = next((p for p in plan_items() if p["n"] == n), None)
    print(json.dumps(it, ensure_ascii=False, indent=1) if it else f"no plan item {n}")


def cmd_recent(k):
    rows = produced()[-k:]
    for r in rows:
        print(f"{r.get('id')}: {r.get('title')} | subtopic: {r.get('subtopic')} | hook: {r.get('hook')} | "
              f"visual: {r.get('visual')} | lessons: {r.get('lessons', '')}")
    if not rows:
        print("(nothing produced yet)")


def cmd_voice(ep, d, test):
    lang = short_lang(ep)
    if not lang:
        raise SystemExit("EP must look like sh-0001-bn-slug or sh-0001-en-slug")
    nar = json.load(open(os.path.join(d, "narration.json"), encoding="utf-8"))
    errs = validate_narration(nar, lang)
    if errs:
        raise SystemExit("narration problems:\n" + "\n".join(errs))
    cd = branch_dir(BR["content"])
    vd = os.path.join(cd, "voice", ep)
    os.makedirs(vd, exist_ok=True)
    json.dump(nar, open(os.path.join(vd, "narration.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    push_branch(cd, BR["content"], f"shorts voice request {ep}")
    ok, _ = run_workflow("shorts-voice.yml", {"episode": ep, "test_tone": "true" if test else "false"}, timeout_min=15)
    if not ok:
        raise SystemExit("shorts voice workflow failed (see notes above)")
    src = os.path.join(branch_dir(BR["audio"]), ep)
    os.makedirs(os.path.join(d, "vo"), exist_ok=True)
    for f in glob.glob(os.path.join(src, "vo", "*.mp3")):
        shutil.copy(f, os.path.join(d, "vo", os.path.basename(f)))
    shutil.copy(os.path.join(src, "durations.json"), os.path.join(d, "durations.json"))
    durs = json.load(open(os.path.join(d, "durations.json")))
    print(f"audio ready in {d}/vo ({len(nar)} takes, {sum(durs.values()):.1f}s of speech)")


def cmd_deliver(ep, d, mode):
    """DIR must hold final.mp4 (9:16, <= 30 s), thumb.jpg (1080x1920 or 1280x720, <= 2 MB) and post.json."""
    meta = json.load(open(os.path.join(d, "post.json"), encoding="utf-8"))
    meta["id"] = ep
    mp4, thumb = os.path.join(d, "final.mp4"), os.path.join(d, "thumb.jpg")
    errs = validate_meta(meta, f"{ep}.json") + validate_files(mp4, thumb if os.path.isfile(thumb) else None)
    if mode == "now":
        meta["slot"] = (datetime.now(timezone.utc) + timedelta(minutes=30)).astimezone(STZ).isoformat(timespec="minutes")
    elif datetime.fromisoformat(meta["slot"]) < datetime.now(timezone.utc) + timedelta(minutes=SCFG["min_lead_minutes"]):
        errs.append(f"slot is less than {SCFG['min_lead_minutes']} minutes away — use the next free slot")
    if errs:
        raise SystemExit("cannot deliver:\n" + "\n".join(errs))
    md = branch_dir(BR["media"])
    os.makedirs(os.path.join(md, "s"), exist_ok=True)
    v = os.path.join(md, "s", ep)
    shutil.copy(mp4, v + ".mp4")
    if os.path.isfile(thumb):
        shutil.copy(thumb, v + ".jpg")
    json.dump(meta, open(v + ".json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    push_branch(md, BR["media"], f"short {ep}", squash=True)
    print("media pushed")
    ok, _ = run_workflow("shorts-publish.yml", {"mode": mode})
    st = load(BR["state"], "posts.json", {"posts": {}})["posts"].get(ep)
    print(json.dumps(st, ensure_ascii=False, indent=1) if st else "(no state record)")
    return 0 if ok and st and "youtube" in st.get("done", {}) else 1


def cmd_log(ep, d):
    """d/log.json: {"title","subtopic","hook","visual","script":[...],"sources":[...],"lessons"} -> shorts-content:produced/"""
    rec = json.load(open(os.path.join(d, "log.json"), encoding="utf-8"))
    rec["id"] = ep
    rec["logged"] = datetime.now(STZ).isoformat(timespec="minutes")
    cd = branch_dir(BR["content"])
    os.makedirs(os.path.join(cd, "produced"), exist_ok=True)
    json.dump(rec, open(os.path.join(cd, "produced", f"{ep}.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    push_branch(cd, BR["content"], f"produced {ep}")
    print("logged", ep)


def cmd_plan_push(f):
    cd = branch_dir(BR["content"])
    shutil.copy(f, os.path.join(cd, "plan.json"))
    for extra in sys.argv[3:]:
        shutil.copy(extra, os.path.join(cd, os.path.basename(extra)))
    push_branch(cd, BR["content"], "shorts plan")
    print("plan pushed")


def main():
    a = sys.argv[1:]
    if not a:
        print(__doc__); return 2
    c = a[0]
    if c == "status":
        cmd_status()
    elif c == "next":
        cmd_next(int(a[1]) if len(a) > 1 else 3)
    elif c == "item":
        cmd_item(int(a[1]))
    elif c == "recent":
        cmd_recent(int(a[1]) if len(a) > 1 else 12)
    elif c == "voice":
        cmd_voice(a[1], a[2], "--test-tone" in a)
    elif c == "deliver":
        mode = a[a.index("--mode") + 1] if "--mode" in a else "live"
        return cmd_deliver(a[1], a[2], mode)
    elif c == "publish":
        ok, _ = run_workflow("shorts-publish.yml", {"mode": a[1]})
        return 0 if ok else 1
    elif c == "log":
        cmd_log(a[1], a[2])
    elif c == "plan-push":
        cmd_plan_push(a[1])
    else:
        print(__doc__); return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
