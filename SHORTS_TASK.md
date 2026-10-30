# Shorts run (YouTube + TikTok + Facebook Reels) — what Claude does (unattended)

Goal: every day **06:00, 15:00 and 20:00 (Bangladesh)** one finished **≤ 30-second 9:16 YouTube Short** goes public,
in plan order (1 → 1000), on **YouTube (Shorts), TikTok and the Facebook Page (Reels)** — nowhere else
(Facebook added by the owner on 30 Oct 2026, from Short 0008 on). Nobody is watching: never stop to ask; decide, finish, report.

**Hands off the reel system.** The 3–5 min reel pipeline (DAILY_TASK.md, tools/studio.py, scripts/voice.py,
scripts/publish.py, config.json, their workflows and the content/audio/media/state branches, the two existing
scheduled tasks) is the owner's running system. A Shorts run never edits, runs or "fixes" any of it. Shorts use only:
`tools/shorts.py`, `scripts/shorts_*.py`, `shorts/`, `.github/workflows/shorts-*.yml` and the branches
`shorts-content`, `shorts-audio`, `shorts-media`, `shorts-state`.

**Locked:** voice Debashish `3XjJ1C8taYP9CHnHKmK5`, model `eleven_v4_turbo`, only through `tools/shorts.py voice`
(never the ElevenLabs connector, never another TTS). Language = the plan item's language: **Bangla item → Bangla
Short, English item → English Short, Banglish keyword → Bangla Short.** Never print, read or ask for a key.

## 0. Setup (fresh machine every run)
```bash
cd /home/claude/posting && eval "$(bash shorts/kit/setup.sh | tail -1)"     # exports SS (skill copy) SK (engine) KIT
python3 tools/shorts.py status        # free_slots, next_items, pending, recent_errors
python3 tools/shorts.py recent 15     # what the last Shorts looked like — do NOT repeat hook, world, camera or layout
```
If `recent_errors` is not empty: `python3 tools/shorts.py publish retry` first (future slot → scheduled again; slot
missed by < 6 h → public now). Read the skill once: `$SS/SKILL.md`, `$SS/references/exportain-brand.md`,
`$SS/references/scene-engine-16x9.md` (the drawing library and reveal vocabulary apply to 9:16 too),
`$SS/examples/assoc_9x16/js` (9:16 layout reference), and this kit: `shorts/kit/r3d.js` (3D worlds + options).

## 1. Which Shorts this run makes
Up to **3 Shorts**, one per entry of `free_slots` (earliest first), using `next_items` in order: first free slot ←
first next item. EP = `sh-<NNNN>-<bn|en>-<short-english-slug>` (NNNN = plan number). `python3 tools/shorts.py item N`
prints the full plan entry (keyword, seo_keyword, subtopic, hook_format, visual_world, draft_title, tags, hashtags).
Budget per Short ≈ 30 min (research 5 · script 3 · voice 2 · scenes 10 · render 8 · deliver 2). Never post late: if
a Short cannot be delivered ≥ 20 min before its slot, give it the next free slot instead (edit `slot` in post.json).

## 2. Research + script (the plan entry is a brief, not a script)
- The Short must **answer the searched keyword** (`seo_keyword`). `subtopic` is the angle; if it does not fit the
  keyword well, choose the closest angle that does (and say so in the log). `hook_format` = the hook style to use.
- 2–4 WebSearch queries (+ WebFetch the best page) for every fact; Bangladesh sources first (EPB, NBR, CCI&E, BSW,
  Bangladesh Bank, BGMEA/BKMEA, Daily Star, Financial Express, TBS). Today's date counts — use the newest figure and
  show its year on screen. Unsure fee/rule → don't state an amount ("check the latest on the portal").
- **Script = 4–6 takes, 280–370 spoken characters in total** (cap 390; the voice is slow), in `narration.json`
  (`[{"id":"00_hook","text":"…"}]`):
  1. `00_hook` (≤ 2.5 s spoken): the keyword (or its core words) in the first sentence + a pattern interrupt: a
     surprising number, a mistake, a myth, a direct question. No greeting, no logo intro, no "in this video".
  2. 2–4 value takes: one idea each, concrete (what / where / how), numbered when it is a list ("One:", "প্রথম,").
  3. last take: payoff + CTA in one line naming Exportain, e.g. EN "Then list your factory on Exportain, and let
     buyers find you." / BN "তারপর এক্সপোর্টেইনে পণ্য তুলুন, বিশ্বের ক্রেতারাই আপনাকে খুঁজে নেবে।" Vary the wording.
     Never promise orders, profit or approval. Optional loop line: the last words lead back into the hook.
- Bangla Shorts: Bangla script only, no Latin letters, no slash; acronyms in Bangla (ইআরসি, এলসি, এইচএস কোড, সিএন্ডএফ);
  screen shows the Latin form. English Shorts: plain English, no Bangla script in the voice text.
- Legal/fee/bank topics: one short hedge inside a take ("rules change — confirm with your AD bank").
- Never mention other episodes; never name companies or people negatively.

## 3. Voice + pacing
```bash
P=/home/claude/sh/<EP>; mkdir -p $P   # narration.json goes here
python3 tools/shorts.py voice <EP> $P          # GitHub runs ElevenLabs (locked voice/model, language from EP)
python3 shorts/kit/tighten.py $P --tempo 1.08  # trims breaths/pauses, light speed-up; originals kept in vo_raw/
```
Target: sum(durations) ≤ 26.5 s (the build adds ≈ 1.2 s gaps + 1.2 s end card; the final video must be ≤ 30.0 s,
ideally 24–29 s). Too long → shorten the text of the longest take and re-voice (only changed takes are charged).
Never use `--tempo` above 1.10.

## 4. Video — 9:16, every Short different, realistic 3D + motion graphics
```bash
bash shorts/kit/new_short.sh $P <2-letter prefix> <bn|en>
```
- **Design brief first (write it in log.json "visual")**: pick a 3D world + time of day + camera move + palette
  that fit THIS topic and differ from the last 3 (`recent`). Worlds in r3d.js: `ship`, `port`, `globe`
  (routes from Bangladesh), `warehouse`, `docs` (3D papers landing on a desk, custom titles), `fabric` (garment
  floor), `farm` (agro crates; `produce` colour). Options: `time` day|golden|dusk|studio, `cam`
  orbit|dolly|crane|push|flyby, `palette`, `label`, `seed`, `stack`, `routes`, `papers`, `r`, `h`, `fov`.
  A new world or prop for the topic may be added to r3d.js (keep the API; commit it).
- **At least one realistic 3D scene per Short** (normally the hook, often one more): in board.json add
  `"gl": {"world": "…", …}` to that scene and draw its SVG **without a background rect** — only overlay text/cards,
  with a dark gradient band behind text (see `shade()` in examples). Other scenes: illustrated motion graphics on
  the brand gradients (e_sky e_mint e_gold e_sea e_lime) — never caption slides.
- Board: one entry per take, `kind` `<pfx>_<name>`, 3–6 `keys` (exact substrings of the take), `sfx` one per key.
  Last entry = the kit CTA scene `<pfx>_cta_en` or `<pfx>_cta_bn` with `"badge": "white"`, `bg` `e_forest`.
- Muted-viewer rule: every scene has big readable text (keyword in the first frame of the hook, ≥ 56 px headline,
  numbers 120–200 px), something new appears every 1–1.5 s, nothing frozen > 1.5 s. Keep text inside x 70–1010,
  y 230–1720 (YouTube UI covers the bottom ≈ 200 px and the right edge buttons). Brand colours only; red = risk only;
  invented examples tagged "Example"/"উদাহরণ"; real figures carry the year + source.
- Build & check: `cd $P && bash build.sh && bash $SS/tools/check_js.sh $P && python3 $SS/tools/board_check.py $P`
  (JS OK, board OK, 0 key warnings, "3D layer: on (…)"), then look at stills of every scene (render.py --still or a
  small contact sheet) and fix overlaps/clipping/empty areas before rendering.
- Render (background, ≈ 8–15 min):
  `setsid nohup bash $SS/tools/render.sh $P Exportain_Short_<NNNN> upbeat 0.4 -22 > $P/render_all.log 2>&1 < /dev/null &`
  Gates: 0 frozen > 2.5 s, ≈ −14 LUFS, peak ≤ −1.05 dBFS, **duration ≤ 30.0 s** (ffprobe `$P/out/final_9x16.mp4`).

## 4b. Premium thumbnail + cover (owner's standing order, 28 Oct 2026: heavy colour, high contrast, must make people click)
Never use a raw video frame as the thumbnail. Design it with `shorts/kit/thumb.py` (read its header) — it is the
YouTube thumbnail AND the first frame of the Short (TikTok cover):
```bash
# $P/thumb.json — e.g.
# {"lang":"en","layout":"card","kicker":"Bangladesh export guide","headline":"Export *garments*|in 3 steps",
#  "sub":"from licence to first order","burst":"$38.7B","arrow":true,
#  "hero":{"world":"ship","time":"golden","cam":"orbit","a0":0.9,"r":105,"h":26,"stack":5,"at":3,"crop":[0,520,1080,760]}}
python3 shorts/kit/thumb.py $P/out/final_9x16.mp4 $P/thumb.json $P/thumb.jpg --n <plan number>
python3 shorts/kit/cover.py $P/out/final_9x16.mp4 $P/thumb.jpg $P/final.mp4      # prints tiktok cover_ms
```
- **Headline** = the click reason in 2–6 words (max 3 lines), in the Short's language, keyword or its core word
  included; one `*highlighted*` word/number. Curiosity, a striking number, a mistake, "how to … in 3 steps" —
  never a full sentence, never the video title copied. Bangla Short → Bangla thumbnail; English → English.
- **Hero** = a clean 3D shot (`"hero": {world options…, "at": seconds, "crop": […]}`) of a world that fits the topic,
  bright and close (not the far, foggy view). Optional `sticker` (round crop of a second moment) and `burst`
  (number / "৩ ধাপ" / "NEW 2026"), `arrow` pointing at the hero.
- **Rotate** layout (card → bleed → split → number), palette (`--n` rotates it; or `pal` 0–9) and hero world so no two
  consecutive Shorts look alike; check `recent` and log the thumbnail in log.json ("thumb": layout/pal/headline).
- **Check at phone size (Read the jpg)**: headline readable in 1 second, nothing clipped, important content within
  y 260–1600, colours vivid (no grey/pastel), logo = green icon + white wordmark. Fix thumb.json and re-run if not.
- `post.json` → `"tiktok": {"cover_ms": <value cover.py printed>}`. If cover.py prints "skipped" (video too long),
  shorten the voice instead of shipping without the cover.
- To replace the thumbnail of an already-uploaded Short: `python3 tools/shorts.py rethumb <EP> <jpg> [<EP> <jpg> …]`.

## 5. SEO for Shorts — `$P/post.json`
```json
{"id": "<EP>", "n": "<NNNN>", "slot": "<free slot ISO, +06:00>", "cluster": "<plan cluster>",
 "youtube": {"title": "…", "description": "…", "tags": ["…"], "language": "bn|en"},
 "tiktok":  {"caption": "…", "cover_ms": 1800},
 "facebook": {"title": "…", "description": "…"}}
```
- **Title** (≤ 70 chars, best 40–60): primary keyword first (plan `seo_keyword`, natural form), then the hook/benefit,
  then ` #Shorts`. Bangla Short → Bangla title (one key English term allowed); English Short → English title.
  Start from plan `draft_title`, improve it; no clickbait the video does not deliver; no ALL CAPS sentences.
- **Description**: line 1 = one sentence with the primary keyword + one secondary keyword (from plan `tags`); lines
  2–4 = the 3 takeaways as short lines; source line ("Source: EPB, FY2025-26"); Exportain line
  `https://exportain.com/?utm_source=youtube&utm_medium=shorts&utm_campaign=shorts&utm_content=<NNNN>` with
  "Bangladesh's B2B export marketplace" / "বাংলাদেশের বিটুবি এক্সপোর্ট মার্কেটপ্লেস"; last line 3–5 hashtags, `#Shorts`
  first, then plan hashtags (the first 3 show above the title).
- **Tags**: 300–450 characters total: keyword + its English/Bangla/Banglish variants + subtopic terms + brand.
- Spoken keyword in the first 2 s and on screen in the first frame (YouTube reads both). One clear topic per Short.
- **TikTok caption** (same language as the Short; never copy the YouTube description): line 1 = keyword-rich hook
  (TikTok search reads captions), 2–3 short value lines (emoji allowed, sparingly), CTA "আরও জানতে ফলো করুন ·
  Exportain.com" / "Follow for more · Exportain.com" (no clickable links), then 6–10 hashtags: 2–3 niche keyword
  tags, #fyp #foryou, 1–2 Bangladesh tags, #Exportain. ≤ 600 characters. `cover_ms` = the value `cover.py`
  printed (the designed cover frame at the start of final.mp4).

- **Facebook Reel** (same language as the Short; written fresh, not a copy of YouTube or TikTok): `title` ≤ 60 chars,
  keyword first, no `#Shorts`. `description` (≤ 900 chars, Facebook search + feed read it): line 1 = keyword-rich hook
  question/statement (first ~125 chars show before "See more"), 2–3 short value lines (✅/👉 sparingly), source line
  when a figure is shown, one engagement question ("আপনি কোন পণ্য রপ্তানি করতে চান? কমেন্টে লিখুন" / "Which product
  would you export? Tell us below"), the Exportain link
  `https://exportain.com/?utm_source=facebook&utm_medium=reels&utm_campaign=shorts&utm_content=<NNNN>`, then 5–8
  hashtags: #Reels first, 2–3 keyword tags, 1–2 Bangladesh tags, #Exportain. The thumbnail is set as the Reel cover.

## 6. Deliver, log, next
```bash
python3 tools/shorts.py deliver <EP> $P --mode live     # validates, YouTube upload (publishAt) + TikTok via Buffer at the slot
```
Prints `youtube: OK https://youtube.com/shorts/<id> — scheduled …`, `tiktok: OK scheduled in Buffer …` and
`facebook: OK https://www.facebook.com/reel/<id> — scheduled …` (Facebook Reels API, Page secrets FB_PAGE_ID/FB_PAGE_TOKEN/FB_APP_SECRET). TikTok's
file is served to Buffer as a temporary asset of the GitHub release `shorts-media-files` (cleaned after 4 days); the
reel system's Pages/media branch are not used. A Buffer "queue full" error is retried by the next run's `publish retry`. If it failed, read the notes, fix, run
`python3 tools/shorts.py publish retry`. Then write `$P/log.json`
`{"title","subtopic","hook","visual":"world/time/cam/palette/layout recipes","thumb":"layout/pal/headline/hero",
 "script":[take texts],"sources":[urls],
 "lessons":"what looked best / improve next time"}` and `python3 tools/shorts.py log <EP> $P`.
Then the next free slot (max 3 per run).

## Self-repair
Up to 3 attempts per failing step: read the error, fix, retry. JS/board errors → fix the scene code; too long →
shorten text; render frozen → add motion to the named scene; workflow hiccup → run it again; YouTube 5xx/429 →
`publish retry` later in the run. A bug in the Shorts lane files may be fixed and pushed to `main` (clear commit
message, mention it in the report). Never touch the reel system, secrets, workflow permissions or the voice lock.
Owner-only problems (revoked YouTube token, ElevenLabs balance, quota): finish what works, put exact fix steps first.

## Report (final message, short Bangla)
Per Short: number, slot, title, length, YouTube link/status, TikTok status, Facebook link/status. Shorts left. Failures + what the owner must do.
