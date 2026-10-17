---
name: exportain-video-studio
description: Exportain's complete Bangla commercial video studio — topic brief → verified research → one-prompt ElevenLabs voiceover + scene script → (voice MP3) → fully illustrated, animated 16:9 brand video with logo, roadmap, Exportain scene, CTA, music, SFX, QA → MP4 + SRT. Also 9:16 reels and <60 s ads with captions. Use whenever the user sends an Exportain video topic (শিরোনাম/মূল পয়েন্ট…), a recorded voice MP3, or asks for an Exportain ad/reel.
---

# Exportain Video Studio

Everything needed to reproduce the client's videos exactly: `engine/` (render engine: Chromium frame capture, music
bed, SFX, mixing, review, fonts, templates — background in `engine/ENGINE.md`), `starter16/` (16:9 project template:
scene library, Exportain build patches, logo, closing scenes), `starter916/` (vertical reels), `tools/` (one command
per step), `references/` (rules + craft), `examples/` (finished projects with narration, board, scenes, voiceover
prompt and script: **prod** = latest reference, dalal = two-topic 4:53, bsw, epbenrol, ercrules, ads, assoc_9x16).

**Read before working:** `references/exportain-brand.md` (client rules) → `references/writing-rules.md` (turn 1) →
`references/scene-engine-16x9.md` (turn 2). Lookups: `references/helpers-api.md`, `references/ads.md`.

## Setup (once per session)
```bash
S=<this skill folder>; [ -w "$S" ] || { cp -r "$S" /tmp/evs; S=/tmp/evs; }; export SK=$S/engine
bash $SK/scripts/setup.sh        # checks ffmpeg, python3 numpy/scipy/Pillow, playwright+chromium, fonts; fills gaps
which node || echo "node missing: check_js.sh needs it (apt/npm install nodejs)"
```
Long renders must run in the background (Bash `run_in_background`, or `setsid nohup … &`) — foreground calls time out.

The work is always **two turns**. Talk to the user in Bangla, briefly; no step-by-step narration.

---
## TURN 1 — topic → research → `<prefix>_voiceover.txt` + `<prefix>_script.md`
1. One sentence saying what you will do, then research immediately (writing-rules.md → Research). Combine several
   pasted topics into one video when asked (two-part structure).
2. `mkdir /home/claude/<topic>`; write `narration.json` (structure, length table and voice rules in writing-rules.md).
3. Write `meta.json` → `python3 $S/tools/make_scripts.py <dir>` (asserts no slash/Latin, prints chars + estimated
   length; adjust until it matches the wish — default ≈ 3.5–4 min).
4. SendUserFile both files (display attach) + Bangla reply: duration/scenes, story, point order, verified facts,
   hedged/omitted items, "ভয়েস পাঠালেই ১৬:৯ ভিডিও বানিয়ে দেব।", Sources list.

## TURN 2 — voice MP3 (+ usually a logo artifact link — the logo is already bundled) → video
Create a task list. Then:
```bash
P=/home/claude/<topic>          # same dir as turn 1 (narration.json, meta.json there)
bash $S/tools/new_project.sh $P <pfx> "লেবেল১|লেবেল২|লেবেল৩|লেবেল৪|লেবেল৫"     # 16:9 default; 2-letter prefix
cp "<uploaded mp3>" $P/full.mp3
python3 $S/tools/split_check.py $P $P/full.mp3   # all boundary RMS ≈1, "BAD: none"  (else manual_split.py)
```
1. **board.json** — one entry per narration item: `{"kind":"<pfx>_<name>","bg":"e_sky","keys":[…],"sfx":[…]}`.
   keys = 3–6 exact substrings of that scene's text, in order (each fires one visual event); sfx one per key from
   boom bubble chime click ding pop pop2 rise riser shutter sparkle swoosh tick whoosh (chime on point openers, boom on
   problems, sparkle on wins, tick on lists). Rotate light bgs. Last three kinds: `<pfx>_brand`, `<pfx>_advice`,
   `<pfx>_cta` — the starter already defines them in `js/3_9end.js` (CTA keys
   `["প্রস্তুতকারক","বিশ্বের ক্রেতাদের","এক্সপোর্টেইন ডট কম"]`; set `BRAND_CO`/`BRAND_ITEMS` for the story company,
   or override with your own `K.<pfx>_brand` in 4_b.js for a topic-specific page like product cards).
   `python3 $S/tools/board_check.py $P` after writing the scenes.
2. **Scenes** — `js/3_a.js` (first half) and `js/4_b.js` (second half), new illustrations for this topic
   (add art to `js/2e_extra.js`). Follow scene-engine-16x9.md: road-map `rd/rdU` with current point on every point
   scene, `ttl2` on the first scene of each point, story character card with "কাল্পনিক চরিত্র", one visual event per key,
   Latin names on screen, "উদাহরণ" on invented data, varied recipes. Study `examples/prod/js` first (closest match).
3. Build & check:
   ```bash
   sed -i 's/\${0}+//g; s/\${0}||//g' $P/js/3_a.js $P/js/4_b.js
   bash $P/build.sh && bash $S/tools/check_js.sh $P && python3 $S/tools/board_check.py $P   # JS OK, board OK, 0 key warnings
   bash $S/tools/qa.sh $P            # qa_a.jpg, qa_b.jpg … = last frame of every scene
   ```
   **Read every sheet** (Read tool) and fix overlaps/clipping/empty areas (checklist in scene-engine-16x9.md);
   rebuild; re-check only the fixed scenes: `bash $S/tools/qa.sh $P 4 9 15`.
4. Render (background, ~15–30 min):
   ```bash
   bash $S/tools/render.sh $P <Name_16x9>          # ads: bash render.sh $P <Name> upbeat <reveal_s> -21
   ```
   It makes music (warm, drop 2.2 s), renders, limits, checks loudness, runs the frozen-frame review and prints
   frozen stretches mapped to scenes (`frozen_map.py`). Gates: **0 frozen > 2.5 s**, ≈ −13.5…−14 LUFS,
   peak ≤ −1.05 dBFS. If frozen: add an early reveal + idle motion in the named scene, `bash build.sh`, re-run render.sh.
5. Deliver: SendUserFile `$P/out/<Name>.mp4` + `.srt` (caption "<title> — ১৬:৯, m:ss"), then a short Bangla reply:
   how each part is visualised (2–5 bullets), what is example/illustrative data, one offer if useful. No step recap.

## Other jobs
- **9:16 reel**: `new_project.sh $P <pfx> "…" --916`, scenes as in `examples/assoc_9x16` (road5/ttl helpers,
  `qa.sh` picks 1080×1920 automatically).
- **Ads / captions**: references/ads.md.
- **Re-render or study an old video**: `bash $S/tools/from_example.sh prod /tmp/prod` (+ its voice MP3).
- **Voice via API** (automation, key in env only): `python3 $S/tools/tts_scenes.py $P --model eleven_v4_turbo` writes
  vo/<id>.mp3 directly (no split).

## Quality bar (the client's words, condensed)
Professional and commercial; colourful but on-brand; every spoken idea drawn and animated (never caption slides);
calm readable pacing; style varies between videos; facts true and current; Exportain featured once in the body + CTA;
no outro; logo crisp; music low; SFX varied; nothing frozen.
