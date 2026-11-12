# Daily run — what Claude does every day (unattended)

Goal: keep every **12:30 and 19:30** (Bangladesh) slot filled with a finished **9:16 vertical Short of at most 50 s
(40–50 s, target 44–48 s; owner's order 6–7 Nov 2026: Shorts only, story style, no long videos)** built from the owner's numbered script prompts, strictly in number order (the next
unused number from `status`), posted to YouTube (as a Short) + Facebook (native Page video, shown as a Reel)
(their own APIs, run by `publish.yml`), Instagram (Reel, `ig.yml`) and TikTok, LinkedIn, X (Buffer).
Claude never sees a key.

**LOCKED by the owner (never change, never ask):** voice = Debashish `3XjJ1C8taYP9CHnHKmK5`, model = `eleven_v4_turbo`,
language = Bangla only. Hard-coded in `scripts/voice.py`; the workflow refuses anything else. Audio comes only from
`studio.py voice` — never the ElevenLabs connector or any other TTS.

**The video skill is `exportain-video-studio`** (the owner's skill). Load it fresh every run and follow its SKILL.md and
references for research, writing rules, drawing library, reveal vocabulary, build, QA and render. **Only the
differences listed in this file override it** — above all: the video is now a 9:16 Short of at most 50 s (40–50 s), with burned-in subtitles.

Nobody is watching: never stop to ask. If something blocks, finish what can be finished and report it in the final
message (that message is what the owner is notified about).

## Owner's order — 13 Nov 2026 (newest; wins over everything below)
1. **No Facebook photo cards any more.** Do not write `cards.json`, do not run `tools/cards.py`, no
   `facebook_photos` block in post.json. `config.json` → `facebook_photos.enabled` is false; publish.py cancels any photo
   post that is still scheduled. Never turn it back on unless the owner asks.
2. **Fluent, error-free Bangla.** The narration must sound like a real person talking — smooth, natural spoken
   (প্রমিত কথ্য) Bangla, never broken telegram style ("দেশের এক নম্বর, প্রমাণ নেই" ✗ → "লিখেছিলেন দেশের সেরা, অথচ কোনো
   প্রমাণ নেই" ✓). Full short sentences with a verb, natural joins (তারপর / কিন্তু / তাই / এবার), no list of bare nouns.
   Before voicing, re-read every line aloud in your head and fix: spelling (বানান), grammar, wrong word, missing verb,
   awkward order, unclear meaning, Banglish mix. The subtitles show the same text, so a typo is a visible error.
   If the 50 s limit forces a cut, cut a whole idea, never the grammar.
3. **Useful first.** Every Short must leave the viewer with something they can do today: a concrete step, check,
   document name, number with its year, or a do/don't. Say the fix, not only the problem (for a "mistakes" topic: each
   mistake + its fix in one natural sentence). No filler, no vague motivation lines.
4. **Built for reach (how Shorts/Reels/TikTok rank: viewers who stay, rewatch, share and save).**
   - Hook in the first 1–2 s: a specific relatable problem, surprise or number, spoken AND shown big by 0.3 s. Never a slow
     intro.
   - Open a loop early ("পাঁচটা ভুল…", "শেষেরটাই সবচেয়ে বড়…") and close it at the end, so people watch to the end.
   - A turn every 5–7 s (new point, twist, re-hook at ≈ 50 %); something new on screen every 1–1.5 s.
   - End on a clear, save-worthy takeaway; a last line that echoes the hook so the loop replays smoothly.
   - Keep 44–48 s; shorter and tighter beats longer and slow.
   - Captions: keyword in the first line, one easy specific question at the end, no engagement bait.

## Owner's order — Shorts only, max 50 s (6–7 Nov 2026; THIS SECTION IS THE AUTHORITY)
From script 087 on, the job makes **two Shorts a day, at 12:30 and 19:30 Bangladesh time** (the old 18:00 slot is
gone), from the same numbered script prompts in strict number order. **No long videos any more**, and everything that
belonged only to the long videos is dropped: the 90–150 s length, the long 150 s structure, the road-map header, the
Exportain/brand scene, the advice scene, the spoken CTA, the company page. Kept: research, the locked voice,
illustrated 9:16 scenes, burned-in subtitles, covers, captions, all six platforms, deliver (photo cards dropped 13 Nov 2026).
- **No Exportain talk in the video:** nothing about Exportain is said or shown in the scenes (no "এক্সপোর্টেইন হলো…",
  no "ভিজিট করুন / যোগ দিন"). The only Exportain element is a **1-second silent logo end card** at the very end (plus the
  small corner logo badge the build adds). After `new_project.sh` run `sed -i 's/--endcard 2.5/--endcard 1/' $P/build.sh`.
- **Length: never over 50 s.** Finished file (incl. 0.5 s cover + 1 s end card) **40–50 s**, target 44–48 s;
  `publish` refuses anything else. Narration **380–460 characters** (tags excluded, hard cap 600) in **5–7 scenes**
  (real rate ≈ 11.3 chars/s; finished ≈ speech + 0.7 s per scene + 1.5 s). Check `durations.json` right after voicing:
  over 48.5 s → shorten the longest scenes (only changed scenes are re-voiced); under 41 s → add one concrete fact.
- **Tell it as a story (owner: "গল্পের মতো, যাতে বেশি ভিউ হয়").** One fictional Bangladeshi entrepreneur (named,
  district + product, "একজন কাল্পনিক উদ্যোক্তা" said once, pill "কাল্পনিক চরিত্র" on screen) lives the topic:
  - `00_hook` (0–3 s): the character's moment of trouble or surprise with the topic keyword in the first sentence and a
    number/risk ("নাদিয়ার প্রথম আমেরিকান অর্ডার, কিন্তু শুল্কেই চলে যাচ্ছে পঁচিশ শতাংশ!"). Moving hook text by 0.3 s.
  - `01…` (3–36 s): what the character finds out, **every point of the prompt in order**, one short spoken sentence
    each, each point a turn in the story ("তারপর জানলেন…", "কিন্তু আসল চমক…" as the mid re-hook at ≈ 50 %).
  - last scene (36–45 s): how the story ends + one save-worthy takeaway (a number with its year, a document name or a
    step order). Legal/fee/bank/regulatory topics end with "কাজের আগে এডি ব্যাংক বা বিশেষজ্ঞের সাথে মিলিয়ে নিন।"
  - Then only the 1 s logo end card. A last line that echoes the hook helps replays.
- **Pace:** one visual event per key, something new every 1–1.5 s, the character visible in most scenes, a small
  "১/৫"-style point counter chip instead of the road-map, big short on-screen words; facts stay verified and dated,
  invented numbers labelled "উদাহরণ".
- **Captions:** same platforms and rules (a short natural exportain.com mention is allowed in captions only);
  YouTube description and LinkedIn text short (LinkedIn ≤ 1,500 chars). (No Facebook photo cards since 13 Nov 2026.)
- The older sections below are kept only for the process steps (setup, research sources, voice, build, QA, render,
  subtitles, covers, deliver, self-repair). Wherever they mention 90–150 s, 18:00, the road-map, brand/advice/CTA
  scenes or the long structure, this section wins.

## Owner's standing order — Professional Video Growth System v2.0 (31 Oct 2026, from script 083 on)
Exportain is a professional B2B export-education and international-trade media brand, not entertainment. Every
video must teach a Bangladeshi exporter something they can use, build trust in Exportain, and only then invite them
to Exportain. These rules replace the 26 Oct "quality upgrade" where they differ.
1. **Format:** 9:16, 1080×1920, 30 fps, H.264 MP4, **90–150 s** (`publish` refuses anything else). Target 115–140 s;
   a simple topic may be 95–110 s, a complex one up to 150 s. Never stretch, never rush a regulatory point to fit.
2. **The prompt is the authority.** Use the script prompt's title, idea, audience, points (all, in order) and
   references. Never invent a new subject, never change its meaning, decisions or technical instructions. Shorten by
   removing repetition, not essential requirements. If a fact in the prompt is outdated or wrong, verify and correct
   it and say so in the report ("key corrections").
3. **Structure (≈ 150 s template, scale to the real length):**
   - 0–5 s **hook**: the viewer's real problem, risk or opportunity, with the topic's keyword in the first sentence.
     Never "আসসালামু আলাইকুম", "আজকের ভিডিওতে…", a logo intro or a brand introduction.
   - 5–20 s **context**: the problem / question / opportunity (one fictional entrepreneur may appear here,
     labelled "একজন কাল্পনিক উদ্যোক্তা").
   - 20–65 s **main explanation**: the prompt's points in order, what each one is in plain Bangla, why it matters.
   - 65–110 s **practical application**: how a Bangladeshi exporter does it — steps, where to look, what to check,
     a small clearly-labelled example (the fictional entrepreneur's case with "উদাহরণ" numbers).
   - 110–135 s **actionable takeaways**: what to do, what to avoid, what to verify (2–3 short sentences).
   - 135–150 s **close**: the Exportain scene (shortened, still with the required sentence) → advice line when the
     topic is legal / fee / bank / regulatory → the exact CTA. Nothing after the CTA.
4. **Language:** natural, professional, conversational Bangla; short spoken sentences; every important technical term
   gets a one-line plain-Bangla meaning at first use. Voice text stays Bangla script only (acronyms spelled in Bangla:
   এইচএস কোড, এলসি, ইআরসি…); the **screen** shows the standard English term (HS Code, Commercial Invoice, Bill of Lading,
   Certificate of Origin, LC, Incoterms, FOB/CIF, ERC, Proforma Invoice…).
5. **Visuals explain, never decorate.** Keep the house illustrated motion-graphics style but make it more
   professional and documentary: more documents (labelled "উদাহরণ" — never shown as genuine government papers),
   process flows, maps with routes, charts with real dated figures, port/shipping/manufacturing scenes; fewer
   cartoon gags; no flashy transitions; correct flags, currency and units. One visual event per key, something new
   every 1.5–2.5 s, continuous gentle motion.
6. **Subtitles are mandatory** — burned in by `tools/subs.py` (short 1–2-line Bangla cues, white on dark outline,
   centred at y ≈ 1490). Keep important scene content **out of the band y 1400–1600**; the bottom 300 px
   (y 1620–1920) is covered by platform buttons/captions on TikTok/Reels/Shorts — background and ambient motion only.
   On-screen key terms (HS CODE, LETTER OF CREDIT (LC), FOB vs CIF…) are big and short; no paragraphs on screen.
7. **Copyright:** original narration (locked voice), the engine's own generated music bed, original drawings only.
   No stock clips, no copyrighted music, no real logos except Exportain's.
8. **No promises:** never promise buyers, orders, rankings, views or approval.

## Reach rules (owner, 31 Oct 2026: "use what makes posts reach more people" — only methods the platforms reward)
Checked against Meta / YouTube / TikTok guidance, Oct 2026. Every run applies all of them:
1. **Frame 1 must move and say the hook.** The hook scene shows its big kinetic hook text (the keyword + the problem
   or number) by 0.3 s and has motion from the first frame — no empty title card, no slow fade, no logo intro.
   Facebook/Instagram copies start straight on this moving hook (deliver strips the still cover; their covers are
   set through the API); YouTube (first frames = Shorts cover) and TikTok (Buffer takes frame 1) keep a 0.5 s cover.
2. **Retention over length.** Something new on screen every 1.5–2.5 s, a mid-video "re-hook" line around 45–60 s
   ("কিন্তু আসল ভুলটা হয় এখানে…" style, only when true), no slow stretches. Watch time, completion and replays are
   the strongest signals on all three platforms.
3. **One clear topic per video, same niche every day** (export education for Bangladeshi exporters). Viewer-interest
   surveys and topic consistency decide who sees it; never chase unrelated trends.
4. **100 % original** (Meta favours content produced by the page itself; reposts and lightly edited clips are
   demoted): our own drawings, narration and generated music; never another platform's watermark; never re-upload
   an old video unchanged.
5. **Search words where they are read and heard:** the primary keyword is spoken in the first sentence, shown on
   screen in the hook, in the subtitles, and in the first line of every caption/title.
6. **Comments that are real conversation:** end each caption with ONE specific, easy question about the topic
   (e.g. "আপনার পণ্যের প্রথম প্রবাসী বাজার কোন দেশ?"). **Never engagement bait** (Meta demotes it): no "লাইক দিন",
   "শেয়ার করুন", "বন্ধুকে ট্যাগ করুন", "কমেন্টে হ্যাঁ লিখুন", vote-by-reaction or "শেয়ার না করলে…".
7. **Shareable value:** at least one concrete, save-worthy item per video (a checklist, a document name, a number with
   its year, a step order) — that is what people forward to other exporters.
8. **Consistency:** both daily slots filled, every day, at the fixed times; never late, never two at once.
Facebook Reels API only accepts 3–90 s videos, so the 90–150 s reel is uploaded as a native Page video (Facebook shows
it as a Reel) with `content_category` BUSINESS. YouTube Shorts custom thumbnails are desktop/YPP-only (no API), so
the Shorts cover is the 0.5 s first frame.

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
`references/scene-engine-16x9.md` (drawing library + reveal vocabulary; they work the same at 1080×1920) and
`helpers-api.md` for lookups; **study `examples/assoc_9x16/js` + `starter916/js` (9:16 layouts, `road5`, the 9:16 CTA)**.

Then, every run, first: `python3 tools/studio.py ig slots` (starts the Instagram job that posts any already-delivered
video due in the next ~5 h at its exact slot; returns immediately).

## Self-repair (owner's standing order: fix problems yourself, never wait for the owner)
At the start of every run, after `ig slots`: run `python3 tools/studio.py status`. If `recent_errors` lists any
platform, run `python3 tools/studio.py publish retry` (future slot → scheduled again; slot missed by < 12 h → posted
now). Read its notes. During the run, when any step fails:
- Read the error, find the cause, fix it, and try again (up to 3 attempts per step). Examples: JS/board errors → fix
  the scene code; frozen frames → add motion and re-render; length outside 90–150 s → adjust narration (only changed
  scenes are re-voiced); a GitHub workflow hiccup → run it again; a platform 5xx/timeout → `publish retry` later in
  the run.
- A bug in the repo's tools may be fixed and pushed to `main` (clear commit message, mention it in the report). Never
  touch the locks (voice/model/language in scripts/voice.py), secrets handling, workflow permissions or the
  environment; never weaken security to make something pass.
- Things only the owner can fix (expired/revoked token, ElevenLabs balance, Buffer channel disconnected, a platform
  policy block): finish everything else, keep the video delivered for the platforms that work, and put the exact fix
  steps at the top of the report.
- Long commands (`deliver` waits for publish.yml, renders) can outlast a 10-minute tool call: run them in the
  background (`setsid nohup … > log 2>&1 &`) and poll the log / `status`.

`status` prints `next_script`, `scripts_left`, `free_slots`, `pending_videos`, `recent_errors`.
- No free slots → nothing to build; go to step 6.
- **Exactly one video per run, for the earliest free slot** (`free_slots[0]`), with `next_script`. The video is
  uploaded as soon as it is ready and **scheduled** for its slot (`--mode live`), so it goes public exactly at
  12:30 / 18:00 on every platform. If a run fails, the next run takes the earliest free slot.
- If less than 50 min is left before the slot when the video is ready, deliver to the next free slot instead
  (edit `slot` in post.json); never post late or out of order.
- No unused scripts → build nothing; report "scripts finished".

## 1. Research + narration — `P=/home/claude/ep/<EP>`, `EP=<NNN>-<short-english-slug>`
Source: block `### NNN.` of `content:prompts/Exportain_Reels_500_Script_Prompts.md` (`git fetch origin content` then
`git show origin/content:prompts/Exportain_Reels_500_Script_Prompts.md`; block headings use Bangla digits, e.g.
`### ০৮৩.`). Use it as the topic brief (point 2 of the standing order).
- Research first (writing-rules.md): Bangladesh official sources (EPB, Bangladesh Bank, NBR, Customs, CCI&E, MoC,
  BIDA, BSTI, DAE, BFSA) and international ones (WTO, ITC, WCO, ICC, UNCTAD, World Bank, destination customs), then
  The Daily Star / Financial Express / TBS / Prothom Alo. For every important claim note issuing authority,
  publication + effective date, whether it is still in force, product scope, URL and research date. Never present a
  proposed rule as implemented. Unconfirmed fee or amount → do not speak a number.
- Narration follows the standing-order structure; ids `00_hook`, `01_context`, …, then `NN_brand`, (`NN_advice`),
  `NN_cta`. Ignore the prompt file's ending instructions ("পরের পর্বের নাম", "Exportain — বাংলাদেশের পণ্য…" line):
  never mention a previous/next episode.
- **Length:** the real voice rate is ≈ 11.5 spoken characters per second (082: 2,998 chars → 257 s). Final length =
  sum(durations) + ≈ 0.7 s per scene + 3.5 s (end card + cover). **1,150–1,500 narration characters** (tags
  excluded; hard cap 700 in config.json since the Shorts order) in **11–15 scenes** lands at ≈ 110–145 s. `make_scripts.py` estimates at
  the old speed — trust `durations.json`. If over 150 s, trim sentences in the longest scenes (only changed scenes
  are re-voiced); under 90 s, add explanation, never filler.
- The Exportain scene keeps the sentence "এক্সপোর্টেইন হলো বাংলাদেশি প্রস্তুতকারক আর রপ্তানিকারকদের বিটুবি মার্কেটপ্লেস, …"
  (short continuation tied to the topic). The CTA stays exactly: "আপনি যদি বাংলাদেশের প্রস্তুতকারক বা রপ্তানিকারক
  হন, বিশ্বের ক্রেতাদের কাছে পৌঁছাতে আজই ভিজিট করুন এক্সপোর্টেইন ডট কম।"
- Write `narration.json` + `meta.json`, run `python3 $S/tools/make_scripts.py $P` (asserts no slash/Latin).
  Keep `<prefix>_script.md` (verified facts + sources) in `$P`.

## 2. Voice (GitHub runs ElevenLabs — locked voice/model/language)
```bash
python3 tools/studio.py voice <EP> $P        # → $P/vo/<id>.mp3 + durations.json (per scene)
```
Never re-run for unchanged text (charges again). If it fails, read the notes; fix the text only if the notes say so.
Check the real total against 90–150 s (formula above) before drawing.

## 2b. Design brief — every video different and better
Before drawing: `python3 tools/studio.py styles` (recent videos + lessons). Write a 3–5 line concept that comes from
THIS topic (a professional metaphor/world: port and vessel, document desk, customs counter, factory line, trade map,
bank transaction flow…), never the previous video's main metaphor; ≥ 6 recipes (process flow, document close-up,
map route, comparison table, chart with dated figures, checklist, before/after…); rotate backgrounds, accent
emphasis and motion style; ≥ 2 new drawings for the topic in `js/2e_extra.js` (or a topic art file).
After delivering: `python3 tools/studio.py log-style <EP> "concept: …; recipes: …; new art: …; subtitles: …; what
looked best / improve next time: …"`.

## 3. Video — 9:16 1080×1920, illustrated-professional, subtitles
```bash
bash $S/tools/new_project.sh $P <pfx> "লেবেল১|লেবেল২|লেবেল৩|লেবেল৪|লেবেল৫" --916    # same $P (keeps narration/vo)
```
- `board.json` (one entry per narration item, 3–6 keys each), scenes in `js/3_a.js` + `js/4_b.js`, topic art.
  `starter916/js/9_end.js` defines only `<pfx>_cta`; write `<pfx>_brand` and `<pfx>_advice` yourself for 9:16
  (logo `__LOGO__`, company page of the story company with "Verified"/"Listed" rows, the B2B tag; advice = EPB /
  AD Bank / expert cards).
- **Layout (1080×1920):** logo badge top-left; `road5` road-map at y ≈ 230–300 on point scenes; content band
  x 70–1010 × y 320–1380; **subtitle band y 1400–1600 kept clear**; y 1620–1920 background/ambient only.
  Text ≥ 34 px, headings 56–72 px, big numbers 120–200 px. Check the 9:16 CTA too (move its button above y 1380).
- Build + checks: `bash $P/build.sh && bash $S/tools/check_js.sh $P && python3 $S/tools/board_check.py $P` →
  `bash $S/tools/qa.sh $P` → **read every sheet** and fix overlaps/clipping/empty areas/anything in the subtitle band.
- Render in the background: `setsid nohup bash $S/tools/render.sh $P <Name_9x16> > $P/render_all.log 2>&1 < /dev/null &`
  and poll. Gates: 0 frozen > 2.5 s, ≈ −13.5…−14 LUFS, peak ≤ −1.05 dBFS. Output `$P/out/<Name_9x16>.mp4`.
- **Subtitles:**
  ```bash
  python3 tools/subs.py $P --video $P/out/<Name_9x16>.mp4 --out $P/out/<Name_9x16>_sub.mp4
  ```
  → `$P/subs.srt` (also uploaded as captions) + the burned video. Extract 3–4 frames (`ffmpeg -ss T -i … -frames:v 1`)
  and **read them**: Bangla shaped correctly, ≤ 2 lines, nothing important hidden. `--y` / `--size` / `--chars` tune
  position, size and line length.

## 4. Thumbnails/covers, final file, captions/SEO
Covers must be HEAVILY colourful and eye-catching, every platform a different palette, different from the last
video, logo always the green "e" icon + white EXPORTAIN wordmark (never on a white box). Headlines BIG (3–6 words,
one highlighted word, readable at phone size in 1 second). Write `$P/thumbs.json` (format in the header of
`tools/thumbs.py`; sticker `crop` in 1080×1920 coordinates of the 9:16 video), then:
```bash
python3 tools/thumbs.py <EP> $P --video $P/out/<Name_9x16>.mp4
#   thumb.jpg (16:9, YouTube API thumbnail), thumb_yt9.jpg (Shorts cover), thumb_fb.jpg (FB/IG), thumb_tt.jpg,
#   thumb_li.jpg + thumb_li9.jpg (LinkedIn, English). Read every one; fix thumbs.json and re-run.
python3 tools/cover.py --prepend $P/thumb_yt9.jpg --video $P/out/<Name_9x16>_sub.mp4 --out $P/final.mp4 --hold 0.5
```
**Facebook photo carousel: DROPPED by the owner on 13 Nov 2026** — no cards.json, no cards.py, no `facebook_photos` in post.json.

**SEO first:** `keyword-research` skill for the topic (Bangla + Banglish + English, Bangladesh; TikTok Creator Search
Insights cannot be reached from here — use web research). Then write every platform's text by `CAPTION_GUIDE.md`
with these overrides, as `$P/post.json`:
```json
{"id": "<EP>", "script": "<NNN>", "slot": "<free slot>",
 "youtube":  {"title": "≤ 95 chars, Bangla, primary keyword in the first 40 characters, accurate (a Short)",
              "description": "2 opening lines with primary + secondary keyword (Bangla + English); 'এই ভিডিওতে যা শিখবেন' bullets;
                qualification (date of the information, verify with the authority / AD bank); sources with links; exportain.com
                with ?utm_source=youtube&utm_medium=shorts&utm_campaign=reels&utm_content=<NNN>; short FAQ (2–3 searched
                questions); CTA; 3–5 hashtags",
              "tags": ["≈ 400–450 characters in total (validator caps 450), Bangla + Banglish + English"]},
 "facebook": {"title": "≤ 100 chars", "description": "Bangla: practical question or keyword first line, value bullets, natural
              sharing line (no engagement bait), 3–5 hashtags, no URL"},
 "instagram": {"caption": "Bangla, hook first line, value bullets, CTA, 3–5 hashtags, no URL, ≤ 2,200 chars"},
 "tiktok":   {"caption": "Bangla, keyword-rich first line, value, CTA, 11–15 relevant hashtags incl. #FYP #ForYou, no URL"},
 "linkedin": {"text": "ENGLISH, ≤ 2,900 chars, professional insight-led, 3–5 hashtags, no URL"},
 "twitter":  {"text": "ENGLISH, ≤ 275 weighted chars, 0–2 hashtags, no URL"},
 "playlist": "suggested YouTube playlist: Export Business Basics | Bangladesh Export Documentation | International Trade Regulations | Shipping and Logistics | Product Export Guides | International Certification | Bangladesh Export Opportunities"}
```
Never reuse identical text across platforms. CTA in captions: educate first, invite naturally, never promise orders.
Every caption follows the Reach rules: keyword in the first line, one specific question at the end, no engagement
bait ("লাইক/শেয়ার/ট্যাগ/কমেন্টে লিখুন" asks).

## 5. Deliver
```bash
setsid nohup python3 tools/studio.py deliver <EP> $P --mode live --meta post.json > $P/deliver.log 2>&1 < /dev/null &
```
(poll `$P/deliver.log` and `status`). Deliver checks the files (9:16, 90–150 s, thumbnail ≤ 2 MB, texts within
limits), makes the platform copies (Facebook/Instagram without the still cover so they start in motion; TikTok and
LinkedIn with their own covers; X gets the reel, or its first 135 s if longer), puts everything on the `media` branch (GitHub Pages serves it to Buffer), runs
`publish.yml` (YouTube files a 9:16 ≤ 3 min video as a Short) and starts the Instagram job. Never claim a platform as
scheduled unless `status` shows it in `posted`. A platform error is retried by the next deliver/publish while the
slot is ≥ 15 min away; run `python3 tools/studio.py publish retry` once more at the end if anything failed.

## 5b. On time, every time
Budget: research + narration ≤ 25 min, voice ≤ 10 min, scenes + QA ≤ 40 min, render ≈ 15 min, subtitles + covers
≈ 10 min, deliver ≈ 10 min. Never skip QA gates or length rules to save time — if it truly cannot make the slot,
schedule it for the next free slot (the series stays in order and nothing is posted late).

## 6. Report (final message, short Bangla)
If scripts left < 4, say so first. Then: script number + title, slot, YouTube title, length, research status +
key corrections (if any), QA result (frozen / loudness / subtitles checked), which platforms `status` shows as
scheduled, scripts left, failures with reason and exactly what the owner must do (reconnect TikTok in Buffer, renew a
key, top up ElevenLabs…).
Analytics (watch time, retention, shares, followers per platform at 1 h / 6 h / 24 h / 48 h / 7 d) are not collected
by this pipeline yet — the publishing tokens have no analytics scopes. Never invent numbers.
