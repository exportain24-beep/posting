# Daily run — what Claude does every day (unattended)

Goal: keep every **12:30 and 18:00** (Bangladesh) slot filled with a finished **3–5 minute 16:9**
Exportain video built from the owner's numbered script prompts, strictly in number order (060, 061, 062 … — the next unused number from `status`), posted to YouTube + Facebook
(their own APIs, run by `publish.yml`) and TikTok, LinkedIn, X (Buffer). Claude never sees a key.

**LOCKED by the owner (never change, never ask):** voice = Debashish `3XjJ1C8taYP9CHnHKmK5`, model = `eleven_v4_turbo`,
language = Bangla only. Hard-coded in `scripts/voice.py`; the workflow refuses anything else. Audio comes only from
`studio.py voice` — never the ElevenLabs connector or any other TTS.

**The video skill is `exportain-video-studio`** (the owner's skill). Load it fresh every run and follow its SKILL.md and
references exactly — it is the source of truth for research, narration, scenes, build, QA and render. If the owner has
updated it, the new version applies automatically. Only the differences listed in this file override it.

Nobody is watching: never stop to ask. If something blocks, finish what can be finished and report it in the final
message (that message is what the owner is notified about).

## 0. Setup (every run — fresh machine)
```bash
git clone --depth 1 https://github.com/exportain24-beep/posting /home/claude/posting
S=$(ls -d /mnt/skills/*/exportain-video-studio 2>/dev/null | head -1)   # installed skill = newest; else the repo copy
[ -n "$S" ] || S=/home/claude/posting/vendor/exportain-video-studio
cp -r "$S" /tmp/evs; S=/tmp/evs; export SK=$S/engine
bash $SK/scripts/setup.sh
cd /home/claude/posting && python3 tools/studio.py status
```
Read the skill's `SKILL.md`, `references/exportain-brand.md`, `references/writing-rules.md`,
`references/scene-engine-16x9.md` (and `helpers-api.md` for lookups); study `examples/prod/js` (closest reference).

Then, every run, first: `python3 tools/studio.py ig slots` (starts the Instagram job that posts any already-delivered
video due in the next ~5 h at its exact slot; returns immediately).

## Self-repair (owner's standing order: fix problems yourself, never wait for the owner)
At the start of every run, after `ig slots`: run `python3 tools/studio.py status`. If `recent_errors` lists any
platform, run `python3 tools/studio.py publish retry` (future slot → scheduled again; slot missed by < 12 h → posted
now). Read its notes. During the run, when any step fails:
- Read the error, find the cause, fix it, and try again (up to 3 attempts per step). Examples: JS/board errors → fix
  the scene code; frozen frames → add motion and re-render; length outside 180–300 s → adjust narration (only changed
  scenes are re-voiced); a GitHub workflow hiccup → run it again; a platform 5xx/timeout → `publish retry` later in
  the run.
- A bug in the repo's tools may be fixed and pushed to `main` (clear commit message, mention it in the report). Never
  touch the locks (voice/model/language in scripts/voice.py), secrets handling, workflow permissions or the
  environment; never weaken security to make something pass.
- Things only the owner can fix (expired/revoked token, ElevenLabs balance, Buffer channel disconnected, a platform
  policy block): finish everything else, keep the video delivered for the platforms that work, and put the exact fix
  steps at the top of the report.

`status` prints `next_script`, `scripts_left`, `free_slots`, `pending_videos`, `recent_errors`.
- No free slots → nothing to build; go to step 6.
- **Exactly one video per run, for the earliest free slot** (`free_slots[0]`), with `next_script`. Two runs a day
  (≈ 09:00 for the 12:30 slot, ≈ 14:15 for the 18:00 slot) give the ~3 h needed for research, voice, scenes, render
  and upload. The video is uploaded as soon as it is ready and **scheduled** for its slot (`--mode live`), so it
  goes public exactly at 12:30 / 18:00 on every platform. If a run fails, the next run takes the earliest free slot.
- Work fast: research ≤ 15 min, keep QA fixes to the scenes that need them, start the render as early as possible.
- If less than 50 min is left before the slot when the video is ready, deliver to the next free slot instead
  (edit `slot` in post.json); never post late or out of order.
- No unused scripts → build nothing; report "scripts finished".

## 1. Research + narration (skill TURN 1, automated) — `P=/home/claude/ep/<EP>`, `EP=<NNN>-<short-english-slug>`
Source: block `### NNN.` of `content:prompts/Exportain_Reels_500_Script_Prompts.md` (`git fetch origin content` then
`git show origin/content:prompts/Exportain_Reels_500_Script_Prompts.md`). Use its title, idea, audience, points (all, in
order) and references as the topic brief the skill expects.
- Follow `writing-rules.md`: research first (sources with dates), narration structure (hook → fictional character story
  → points in order → story outcome → optional tip → **Exportain scene** with the required sentence → advice line →
  the **exact CTA**, nothing after it), voice-text rules (Bangla script only, no slash, acronyms in Bangla).
- **Overrides of the prompt file:** ignore its ending instructions ("পরের পর্বের নাম", "Exportain — বাংলাদেশের পণ্য…" line):
  never mention a previous/next episode; the skill's CTA + silent end card are the ending.
- **Length: final video must be 3:00–5:00 (180–300 s), target ≈ 3:45–4:15** → 2,500–3,000 narration characters (tags
  excluded), 18–24 scenes. `publish` refuses anything outside 180–300 s.
- Write `narration.json` + `meta.json`, run `python3 $S/tools/make_scripts.py $P` (asserts no slash/Latin, prints length).
  Keep `<prefix>_script.md` (verified facts + sources) in `$P`.

## 2. Voice (GitHub runs ElevenLabs — locked voice/model/language)
```bash
python3 tools/studio.py voice <EP> $P        # → $P/vo/<id>.mp3 + durations.json (per scene, no splitting needed)
```
Never re-run for unchanged text (charges again). If it fails, read the notes; fix the text only if the notes say so.
Check the real total: sum(durations) + gaps + 2.5 s end card + 0.5 s cover frame must land in 180–300 s; if not,
trim/extend the narration (changed scenes only are re-voiced).

## 2b. Design brief — make every video different and better (owner's standing order)
Before drawing anything: `python3 tools/studio.py styles` (what the last videos looked like + lessons). Then decide a
**fresh visual concept that comes from THIS script's subject** and write it down (3–5 lines) before the scenes:
- **Metaphor / world** taken from the topic (e.g. packaging → a factory line with boxes moving; payment → money
  travelling bank to bank on a map; documents → a desk with papers flying into folders; pricing → a scale/calculator;
  buyers → a world map with routes and chat bubbles). Never reuse the previous video's main metaphor.
- **Layout recipe mix**: vary card grids, full-width diagrams, maps, timelines, split-screen before/after, flow
  charts, phone/browser mockups, stacked counters, character close-ups — at least 6 different recipes per video and
  never the same opening layout two videos in a row.
- **Rotate** the background order, the accent colour emphasis (within brand colours), the character (person kinds
  `s g n a`, woman2, new ones in `2e_extra.js`), and the motion style (slide, orbit, draw-on lines, counters, zooms).
- **New art every video**: at least 3 new drawings in `js/2e_extra.js` that belong to this topic.
- Keep all fixed brand rules (logo badge, road-map, title cards, Exportain scene, CTA, end card, colours, QA gates).
After delivering, log it: `python3 tools/studio.py log-style <EP> "concept: …; recipes: …; new art: …; what looked
best / what to improve next time: …"` — honest lessons, so the next run improves on it.

## 3. Video (skill TURN 2) — 16:9, illustrated, the owner's house style
```bash
bash $S/tools/new_project.sh $P <pfx> "লেবেল১|লেবেল২|লেবেল৩|লেবেল৪|লেবেল৫"    # in the same $P (keeps narration/vo)
```
Then exactly the skill's steps: `board.json` → new illustrated scenes in `js/3_a.js`, `js/4_b.js` (+ new art in
`js/2e_extra.js`) → `bash $P/build.sh && bash $S/tools/check_js.sh $P && python3 $S/tools/board_check.py $P` (JS OK,
board OK, 0 key warnings) → `bash $S/tools/qa.sh $P` → **read every sheet** and fix → render in the background:
`setsid nohup bash $S/tools/render.sh $P <Name_16x9> > $P/render_all.log 2>&1 < /dev/null &` and poll.
Gates from the skill: 0 frozen > 2.5 s, ≈ −13.5…−14 LUFS, peak ≤ −1.05 dBFS. Transparent logo badge (no white pill),
road-map, title cards, "কাল্পনিক চরিত্র" pill, "উদাহরণ" on invented data, brand colours only, varied style per video.
Never caption/text slides. Output: `$P/out/<Name_16x9>.mp4` + `.srt`.

## 4. Thumbnail, final file, captions/SEO
```bash
ffmpeg -y -ss <strong moment> -i $P/out/<Name_16x9>.mp4 -frames:v 1 $P/still.jpg
python3 tools/cover.py --size 1280x720 --headline "<4-6 words, one *highlight*>" --chip "<series>" --badge "<short hook>" \
  --bg $P/still.jpg --out $P/thumb.jpg                                   # read it: readable at phone size
python3 tools/cover.py --prepend $P/thumb.jpg --video $P/out/<Name_16x9>.mp4 --out $P/final.mp4 --hold 0.5
```
**SEO first:** `keyword-research` skill for the topic (Bangla + Banglish + English, Bangladesh). Then write every
platform's text by **`CAPTION_GUIDE.md`** (owner's caption rules win). `$P/meta.json` (publishing meta — keep the skill's
own meta.json separate, e.g. save this one as `$P/post.json` and pass it as below):
```json
{"id": "<EP>", "script": "<NNN>", "slot": "<free slot>",
 "youtube":  {"title": "≤ 100 chars, primary keyword first", "description": "summary, what you'll learn, CHAPTERS from the real
              plan.json (0:00 first, ≥ 3 chapters ≥ 10 s apart, +0.5 s for the cover frame), qualifications, exportain.com with
              ?utm_source=youtube&utm_medium=video&utm_campaign=reels&utm_content=<NNN>, CTA, 3-5 hashtags",
              "tags": ["≤ 500 chars total, Bangla + Banglish + English"]},
 "facebook": {"title": "≤ 100 chars", "description": "hook, value, bullets, CTA, exactly 5 hashtags, no URL"},
 "tiktok":   {"caption": "hook + value + CTA, 15-20 relevant hashtags incl. #FYP #ForYou, no URL"},
 "linkedin": {"text": "ENGLISH, ≤ 2,900 chars, professional, 3-5 hashtags, no URL"},
 "twitter":  {"text": "ENGLISH, ≤ 275 weighted chars, 0-2 hashtags, no URL (X gets a 2:15 teaser)"},
 "instagram": {"caption": "Bangla, hook first line, value bullets, CTA, exactly 5 hashtags, no URL, ≤ 2,200 chars (Reel)"}}
```
Never reuse identical text across platforms.

## 5. Deliver
```bash
python3 tools/studio.py deliver <EP> $P --mode live --meta post.json
```
Instagram: deliver also makes the 9:16 cover and starts the Instagram job, which posts the Reel at the slot.
It checks the files (16:9, 180–300 s, thumbnail ≤ 2 MB, texts within limits), makes the X teaser, puts everything on the
`media` branch (GitHub Pages serves it to Buffer), runs `publish.yml` and prints what was scheduled on each platform.
A platform error is retried by the next deliver/publish while the slot is ≥ 15 min away; run
`python3 tools/studio.py publish live` once more at the end if anything failed.

## 5b. On time, every time
The slot is fixed. Budget: research+narration ≤ 25 min, voice ≤ 10 min, scenes+QA ≤ 45 min, render ≈ 25 min,
deliver ≈ 10 min. Start the render the moment QA is clean; while it renders write post.json and the thumbnail
plan. Never skip QA gates or length rules to save time — if it truly cannot make the slot, schedule it for the next
free slot (the series stays in order and nothing is posted late).

## 6. Report (final message)
Short Bangla summary: videos scheduled (slot, title, length, platforms), scripts left, failures with reason and what the
owner must do (reconnect TikTok in Buffer, renew a key, top up ElevenLabs…). If scripts left < 4, say so first.
