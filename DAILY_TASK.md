# Daily run — what Claude does every day (unattended)

Goal: keep every 08:00 and 18:00 (Bangladesh) slot in the next ~2.5 days filled with a finished
3–5 minute 16:9 Exportain video built from the owner's numbered script prompts (starting at 057). YouTube + Facebook are posted by the
`publish.yml` workflow with the platforms' own APIs; TikTok, LinkedIn and X (Twitter) through Buffer. Claude never sees a key.

**LOCKED by the owner (never change, never ask):** voice = Debashish `3XjJ1C8taYP9CHnHKmK5`,
model = `eleven_v4_turbo`, language = Bangla (`bn`) only. These are hard-coded in `scripts/voice.py`; the
workflow refuses any other voice, model or non-Bangla text. Never use the ElevenLabs connector or any other
TTS — audio comes only from `studio.py voice`.

Nobody is watching: never stop to ask. If something blocks, finish what can be finished and
report the problem in the final message (that message is what the user gets notified about).

## 0. Setup (every run, it is a fresh machine)
```bash
git clone --depth 1 https://github.com/exportain24-beep/posting /home/claude/posting
cp -r <bangla-motion-video skill folder> /tmp/mv && export SK=/tmp/mv && bash $SK/scripts/setup.sh
cd /home/claude/posting && python3 tools/studio.py status
```
Load the `bangla-motion-video` skill and read its `references/lessons.md` and `references/topic-mode.md`.

`status` prints `next_script`, `scripts_unused`, `free_slots`, `pending_videos`, `recent_errors`.
- No free slots → nothing to build; go to step 6.
- Make **one video per free slot, earliest slot first, at most 3 this run**, each with the next unused script number.
- No unused scripts → build nothing; report "scripts finished".

## 1. Script → narration (per video, project dir `P=/tmp/ep/<EP>`, `EP=<NNN>-<short-english-slug>`)
**Source:** the user's 500-prompt file (`Exportain_Reels_500_Script_Prompts.md`, block `### NNN.`). Work through the
numbers in order **starting at 057**; `studio.py status` → `next_script` is the next unused number.
Follow that block's points, order, references and structure, **with these owner overrides (they win over the prompt):**
- **Never** mention a previous or next episode/video ("গত পর্বে", "আগামী পর্বে", "পরের পর্বে", the next title). Each video stands alone.
  The prompt's CTA line "…এবং পরের পর্বের নাম" is dropped. CTA = "আরও গাইড আর আন্তর্জাতিক বায়ারের সাথে যুক্ত হতে ভিজিট করুন
  এক্সপোর্টেইন ডট কম।" then the last line "এক্সপোর্টেইন, বাংলাদেশের পণ্য, বিশ্বের বাজারের পথে।"
- Voice text is **Bangla script only** (locked): LC → "এল সি", HS Code → "এইচ এস কোড", FOB → "এফ ও বি", B2B → "বি টু বি".
  On-screen text may show the proper English form.
- Length **3–5 minutes**: 2,000–3,300 narration characters (tags excluded), 22–40 takes, one sentence per take.
- Research and verify every fact against the prompt's references (and official sources). No invented numbers; examples are
  clearly called examples. Mention Exportain once in the body where it fits (seller profile / buyers), plus the CTA.
- Write `P/narration.json` (skill format `[{"id":"00_hook","text":"[tag] …"}]`), `P/script.md`, and keep `P/sources.md`.

## 2. Voice (GitHub runs ElevenLabs — locked: Debashish, `eleven_v4_turbo`, Bangla)
```bash
python3 tools/studio.py voice <EP> $P
```
Pushes the narration, runs `voice.yml`, copies `vo/<id>.mp3` + `durations.json` into `$P`. Never re-run for unchanged text.

## 3. Video — always the **currently installed** bangla-motion-video skill (re-read its SKILL.md and references every run;
never a cached copy, so the owner's skill updates apply automatically)
**Look (owner's rule, non-negotiable):** the skill's **illustrated, text-free motion-graphics mode (Mode D)** — every spoken idea
drawn as its own animated scene (people, factories, farms, documents, ships, maps…), events not slides, exactly like the
hand-made Exportain videos. **Never** the text-led captions mode (`--mode captions` / timeline.html) and never text slides.
- 16:9, 1920×1080, 3–5 minutes, Exportain colours + logo (`assets/logo.png`).
- Draw new scenes for every topic in `$P/scenes.js` on a **1920×1080 canvas** (`<rect width="1920" height="1080" fill="url(#studio)"/>`,
  key art inside x 120–1800, y 120–980), one `K.e<NNN>_<name>` kind per idea, prefix every data-k/class; follow topic-mode.md
  step 4 (recurring anchors, real proportions, 2–6 beat keys per scene, something new every 1.5–3 s, varied backgrounds).
  Do not use the skill's built-in portrait kinds in 16:9.
- Then:
```bash
python3 $SK/scripts/topic_build.py --project $P --logo assets/logo.png --brand Exportain --url exportain.com   # 0 key warnings
python3 tools/illustrated16.py $P/scenes.html                                                                 # switch engine to 16:9
python3 $SK/scripts/qa_stills.py --plan $P/plan.json --size 1920x1080 --cols 3 --out $P/qa.jpg <every "still:" time>   # read + fix
python3 $SK/scripts/music_bed.py --duration <plan total> --mood <mood> --drop <turn start> --out $P/music.wav
setsid nohup python3 $SK/scripts/make_video.py --voice $P/vo.mp3 --plan $P/plan.json --music $P/music.wav --music-db -24 \
  --formats 16:9 --outdir $P/out > $P/out.log 2>&1 < /dev/null &      # ~35-45 min for 4 min; poll
python3 $SK/scripts/review.py --video $P/out/final_16x9.mp4 --plan $P/plan.json --out $P/review
```
  then the fresh-agent critic pass (topic-mode.md), max 2 fix rounds. Rerun `illustrated16.py` after every `topic_build.py`.
- Copy the skill output `$P/out/captions.srt` → `$P/captions.srt` (Bangla subtitles for YouTube and Facebook).

## 4. Thumbnail, final file, captions/SEO
```bash
python3 tools/cover.py --size 1280x720 --headline "<4-6 words, one *highlight*>" --chip "<series name>" --badge "<short hook>" \
  --bg <a strong 16:9 still from the video> --out $P/thumb.jpg
python3 tools/cover.py --prepend $P/thumb.jpg --video $P/out/final_16x9.mp4 --out $P/final.mp4   # thumbnail = first frame (TikTok)
```
Read `thumb.jpg`: headline must be readable at phone size.

**SEO first:** run the `keyword-research` skill for the topic (Bangla + Banglish + English, Bangladesh) → primary keyword,
secondary keywords, tags. Then write every platform's text by **`CAPTION_GUIDE.md`** (the owner's caption skill) — its rules,
limits and hashtag counts win. `$P/meta.json`:
```json
{"id": "<EP>", "script": "<NNN>", "slot": "<free slot>",
 "youtube":  {"title": "≤ 100 chars, primary keyword first", "description": "summary, what you'll learn, CHAPTERS from the real
              plan (0:00 first, ≥ 3 chapters, ≥ 10 s each, add 0.5 s for the cover frame), qualifications, exportain.com link with
              UTM ?utm_source=youtube&utm_medium=video&utm_campaign=reels&utm_content=<NNN>, CTA, 3-5 hashtags",
              "tags": ["≤ 500 chars total, Bangla + Banglish + English"]},
 "facebook": {"title": "≤ 100 chars", "description": "hook, value, bullets, CTA, exactly 5 hashtags, no URL"},
 "tiktok":   {"caption": "hook + value + CTA, 15-20 relevant hashtags incl. #FYP #ForYou, no URL"},
 "linkedin": {"text": "≤ 2,900 chars, professional, 3-5 hashtags, no URL"},
 "twitter":  {"text": "≤ 275 weighted chars, 0-2 hashtags, no URL (X gets a 2:15 teaser of the video)"}}
```
Never reuse identical text across platforms.

## 5. Deliver
```bash
python3 tools/studio.py deliver <EP> $P --mode live
```
It checks the files, makes the X teaser, puts them on the `media` branch (GitHub Pages serves them to Buffer), starts `publish.yml`, and prints
what was scheduled on each platform. A platform error is recorded and retried automatically by the next deliver/publish
run as long as the slot is still ≥ 15 min away; run `python3 tools/studio.py publish live` once more at the end of the run
if any platform failed.

## 6. Report (final message)
One short Bangla summary: which videos were scheduled for which slots and platforms, scripts left, any failures with the
reason and what the user must do (e.g. reconnect TikTok in Buffer, renew a key, add scripts). If scripts left < 4, say so first.
