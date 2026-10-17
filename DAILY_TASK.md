# Daily run — what Claude does every day (unattended)

Goal: keep every 08:00 and 18:00 (Bangladesh) slot in the next ~2.5 days filled with a finished
Exportain reel built from the user's numbered scripts. YouTube + Facebook are posted by the
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
Read `content` branch `scripts/<NNN>.txt` (`git show origin/content:scripts/<NNN>.txt` after `git fetch origin content`).
The user's script is the source: keep its message, order and facts. Polish it for voice and video:
- Research every factual claim (WebSearch/WebFetch). Remove or correct anything not verifiable today. Never invent numbers.
- Hook in the first 3 s. Mention Exportain once in the body where it fits, and end with the CTA (exportain.com).
- Service-provider accounts are **lifetime free** (never "90 days free").
- `P/narration.json` in the skill's format, one take per scene: `[{"id":"00_hook","text":"..."}]`, 6–12 takes, 55–110 characters each,
  **total ≤ 900 characters** (Facebook Reels max 90 s).
- Voice rules (checked by the workflow, it refuses otherwise): Bangla script only, no Latin letters, no `/`.
  B/L → "বি এল", HS code → "এইচ এস কোড", LC → "এল সি", B2B → "বি টু বি", exportain.com → "এক্সপোর্টেইন ডট কম".
- Write `P/script.md` (layers as in topic-mode.md) and `P/board.json`.

## 2. Voice (GitHub runs ElevenLabs `eleven_v4_turbo`, voice Debashish)
```bash
python3 tools/studio.py voice <EP> $P
```
This pushes the narration, starts `voice.yml`, waits, and copies `vo/<id>.mp3` + `durations.json` into `$P`.
Never call it twice for the same text unless the text changed (unchanged takes are reused, changed ones cost credits).
If it fails, read the notes it prints; fix the narration if the notes say so, otherwise report and stop this video.

## 3. Video (bangla-motion-video skill, Mode D, 9:16)
Follow topic-mode.md steps 4–8 exactly: new `scenes.js` art for the topic, `topic_build.py --project $P --logo assets/logo.png
--brand Exportain --url exportain.com` (0 key warnings), QA stills, `music_bed.py`, `make_video.py --formats 9:16`,
`review.py`, then the fresh-agent critic pass, at most 2 fix rounds. Brand colours: #005A1E #003C10 #5CBF14 #2E8B2E,
accents #F2B705 #0E8C88 #0B3B5C. Vary the look between videos. Skip the "voice it?" checkpoint (unattended).

## 4. Cover, final file, texts
```bash
ffmpeg -y -ss <a strong moment> -i $P/out/final_9x16.mp4 -frames:v 1 $P/still.jpg
python3 tools/cover.py --headline "<short hook, one *highlight*>" --chip "<2-3 words>" --bg $P/still.jpg --out $P/cover.jpg
python3 tools/cover.py --prepend $P/cover.jpg --video $P/out/final_9x16.mp4 --out $P/final.mp4
```
Read `cover.jpg` and check the headline fits (≤ 4 short lines). `final.mp4` must be ≤ 90 s.

`$P/meta.json`:
```json
{"id": "<EP>", "script": "<NNN>", "slot": "<free slot, e.g. 2026-10-18T08:00:00+06:00>",
 "youtube":  {"title": "≤ 90 chars, Bangla, keyword first", "description": "2-4 lines + https://exportain.com + 3-5 hashtags", "tags": ["8-15 Bangla + English keywords"]},
 "facebook": {"title": "≤ 90 chars", "description": "hook line + value + https://exportain.com + 3-5 hashtags"},
 "tiktok":   {"caption": "hook + exportain.com + 3-6 hashtags"},
 "linkedin": {"text": "≤ 2900 chars, professional tone, value first, https://exportain.com, 3-5 hashtags"},
 "twitter":  {"text": "≤ 270 chars INCLUDING link and 1-2 hashtags"}}
```
SEO: research what Bangladeshi exporters / service providers search for the topic (Bangla and English terms).

## 5. Deliver
```bash
python3 tools/studio.py deliver <EP> $P --mode live
```
It checks the files, puts them on the `media` branch (GitHub Pages serves them to Buffer), starts `publish.yml`, and prints
what was scheduled on each platform. A platform error is recorded and retried automatically by the next deliver/publish
run as long as the slot is still ≥ 15 min away; run `python3 tools/studio.py publish live` once more at the end of the run
if any platform failed.

## 6. Report (final message)
One short Bangla summary: which videos were scheduled for which slots and platforms, scripts left, any failures with the
reason and what the user must do (e.g. reconnect TikTok in Buffer, renew a key, add scripts). If scripts left < 4, say so first.
