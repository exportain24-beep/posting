---
name: bangla-motion-video
description: Make professional motion-graphics videos in Bangla or English — from just a topic (research, layered script, ElevenLabs voice, custom animated scenes, original music, self-review), from a voiceover (captions or text-free illustrated promos, 9:16/16:9), or full 16:9 website/portal tutorials with recreated UI screens, hook openers, word-synced cursor callouts, SFX and ducked music. Use for any Bangla/English video, reel, explainer, tutorial or walkthrough, including when the user only gives a topic.
---

# Motion Video Studio (bangla-motion-video v5 — v4 + topic mode)

Frame-exact HTML motion graphics rendered in headless Chromium → ffmpeg, with a broadcast-style audio mix (cleaned voice, sidechain-ducked music, synthesized SFX, −14 LUFS). Every frame is a pure function of time `t`.

**Before any work read `references/lessons.md`** (client preferences + every environment gotcha already paid for). Tutorials also need `references/guide-components.md`; topic videos need `references/topic-mode.md`. Copy the skill folder to a writable place first (e.g. `cp -r <skill> /tmp/mv && SK=/tmp/mv`) — installed skill folders can be read-only.

## Requirements (any account)
- Linux shell with ffmpeg, Python 3, Playwright + Chromium (preinstalled browsers are fine), numpy/scipy/Pillow. `bash $SK/scripts/setup.sh` checks and fills gaps. Fonts are bundled (Noto Sans Bengali, Inter, Poppins).
- Voice: the **ElevenLabs connector** (MCP `creative_*` tools) — or the user generates audio on elevenlabs.io and uploads it. Default voice in examples: Debashish `3XjJ1C8taYP9CHnHKmK5` (eleven_v4, works for Bangla and English).
- Docs reading: WebFetch. Files over ~30 MB can't be sent → tutorials are split into parts automatically.

## Pick the mode
| Mode | When | Template | Driver |
|---|---|---|---|
| **A. Captions** | VO + script, kinetic Bangla text OK | `timeline.html` | `make_video.py` |
| **B. Illustrated, text-free** | Promo with *no text on screen* | `illustrated.html` | `plan.py` → `storyboard.py` → `make_video.py --plan` |
| **C. Tutorial** (Bangla or English) | Walkthrough of a portal from docs | `guide.html` | `guide_plan.py` → `render.py` → `guide_finish.py` |
| **D. Topic → video** | User gives only a topic: research, write, voice, draw, score | `illustrated.html` + project `scenes.js` (or `timeline.html`) | `topic_build.py` → `music_bed.py` → `make_video.py --plan` → `review.py` |

## Quality bar (always)
Colourful gradients, never flat black · eased motion only, staggered, idle breathing · varied SFX on every visual event · music very low and ducked (−28 dB tutorials, −22…−24 dB promos) · supplied logo unaltered (transparent PNG on a white card) · **speech and motion in sync — every change lands on the word that names it** · QA stills before rendering; after rendering, `review.py` (timestamped sheets, frozen-stretch check, loudness) and read every sheet · no music file → `music_bed.py` writes an original bed for any mode (pass it as `--music`).

---
## Mode A — captions
```bash
python3 $SK/scripts/make_video.py --voice vo.mp3 --script script.txt --music bg.mp3 --logo logo.png \
  --brand "Exportain" --url "Exportain.com" --formats 9:16,16:9 --music-db -22 --outdir out
```
Check plan.py's table (scenes = sentences, pauses_found ≥ scenes−1); fix `out/plan.json` and rerun with `--plan`. Options `--endcard`, `--no-sfx`, `--sfx-db`, `--words`.

## Mode B — illustrated (text-free)
1. `plan.py --voice vo.mp3 --script script.txt --out plan.json`
2. `board.json` per scene: `{"kind","bg","keys":[spoken words in order],"sfx":[one per key]}` (example `examples/illustrated-9x16/`). Kinds: port_roles gap_globe world_arcs supply_chain logo_reveal marketplace showcase profile_build circle_break network_grow phone_visit bridge_connect journey products4 conveyor door categories20 sellers_upload rfq grow visit_trio; backgrounds c_peach c_mint c_sky c_lilac c_lemon c_coral c_aqua c_deep c_ocean.
3. `storyboard.py --plan plan.json --board board.json --voice vo.mp3 --out plan_sb.json`
4. `make_video.py --voice vo.mp3 --plan plan_sb.json --music bg.mp3 --logo logo.png --music-db -24 --outdir out`

## Mode C — tutorial from docs (full job)
Project dir P: `narration.json`, `screenplay.py`, `durations.json`, `vo/`, `out/`. Worked examples: `examples/seller-guide/` (Bangla, 23 seg), `examples/provider-guide/` (Bangla, `who` opener, CONFIG), `examples/buyer-guide-en/` (English, `hook` opener, tables/product cards/timelines, one-prompt VO).

1. **Research** — WebFetch the docs index and every sub-page (+ shared pages like account/login). Ask for every UI label, field, button, status, limit, price, and each screenshot's numbered callouts. Try `/en/...` and plain paths; screenshots can't be downloaded → recreate them.
2. **Opening** — audience portal → `who` scene (who should / shouldn't use it). International/English → `hook` scene (question-led promise, 4 benefits, 3-step roadmap, logo). Fact-check every claim.
3. **Narration** (`[{id,title,text}]`) — one segment per step, 30–45 s (Bangla 350–480 chars; English 430–530). Start "ধাপ এক— …" / "Step one: …". UI labels verbatim, named in on-screen order. Numbers written as spoken.
4. **Voice** — preferred: ElevenLabs connector, `creative_create_flow` then `creative_generate_speech` per segment **in order** (eleven_v4, voice_id, `generations_count=1`), durations from `creative_get_flow_run_status` (≤11 ids/call) → `durations.json`; user downloads + uploads MP3s → `guide_voice_intake.py --project P <files>`.
   Fallback (connector blocked/unavailable): write one text file with all segments separated by `<break time="2.0s" /> ...` (see `examples/buyer-guide-en/vo_one_prompt_example.txt`); user uploads one MP3 → `python3 $SK/scripts/vo_split.py --project P --voice full.mp3 --anchor-from 1 --anchor-to -2 [--tempo 0.94]` (anchors = segments that start with "Step"/"ধাপ"). Check the ratios/similarities it prints.
   Never retry a refused generation; tell the user once.
5. **Screenplay** — `CONFIG` (menu, steps, url, add_label, badges, `lang='en'`, search), `INTRO`, `STEPS`, `OUTRO`. Callout `k` = exact spoken substring, in order. API: `references/guide-components.md`.
6. **Plan + QA before audio** — `python3 $SK/scripts/guide_plan.py --project P --logo logo.png` (0 key warnings) → `python3 $SK/scripts/qa_stills.py --plan P/plan.json --out qa.jpg <t near end of each scene>` → Read → fix.
7. **After audio** — rerun guide_plan.py (beats snap to real pauses), spot-check stills.
8. **Render** — `cd P && setsid nohup python3 $SK/scripts/render.py --plan plan.json --out out/silent_16x9.mp4 --size 1920x1080 --fps 30 --workers 2 > out/render.log 2>&1 < /dev/null &`; poll every ~590 s (≈ 20k frames ≈ 50 min).
9. **Finish** — `setsid nohup python3 $SK/scripts/guide_finish.py --project P --name Exportain_Buyer_Guide [--music bg.mp3] --music-db -28 --sfx-db -9 > out/finish.log 2>&1 &` → master, share copy, auto Part1/Part2 under 30 MB (no music file → soft synth pad).
10. **Final QA + deliver** — frame sheet from `out/master.mp4`, `ebur128` ≈ −13/−14 LUFS; SendUserFile the parts with a few lines on what each covers.

Re-mix only (music level/SFX) needs no re-render: rerun `guide_finish.py` / `mix_audio.py`.

## Mode D — topic → video (full workflow in `references/topic-mode.md`)
1. **Research** (WebSearch + WebFetch, sources kept) → `research.md`; choose the one true thing + 3–5 points.
2. **Layered script** (Dramatron): logline → recurring visual anchors → beat sheet (Hook · Setup · Turn · Points · Payoff · CTA; every beat an *event*) → place descriptions → narration. Hook in 3 s, no greeting or logo intro. Write `narration.json` (one take per scene, 55–110 chars) and `board.json` (kind, bg, spoken keys, sfx). Run the storyboard check, then send the script table and ask "voice it?" before spending credits.
3. **Voice**: ElevenLabs connector, one `creative_generate_speech` per scene, in order, `generations_count=1` → `durations.json` → the user uploads the MP3s → `guide_voice_intake.py`. Connector blocked → one-prompt file + `vo_split.py --no-refine`.
4. **Scenes**: new `K.<kind>` art per topic in `P/scenes.js` (flat SVG, real proportions, events not states, no text), injected automatically.
5. `python3 $SK/scripts/topic_build.py --project P [--logo … --brand … --url …] [--mode captions]` → 0 key warnings, pace ≤ 15 chars/s → `qa_stills.py --size 1080x1920` at every printed "still:" time → fix. Rerun after the voice arrives (writes `vo.mp3`, snaps beats to word onsets).
6. `python3 $SK/scripts/music_bed.py --duration <plan total> --mood <calm|hopeful|upbeat|warm|curious|tense|epic> --drop <turn scene start> --out P/music.wav`
7. Render in the background: `make_video.py --voice P/vo.mp3 --plan P/plan.json --music P/music.wav --music-db -24 --formats 9:16 --outdir P/out`
8. `python3 $SK/scripts/review.py --video P/out/final_9x16.mp4 --plan P/plan.json --out P/review`. Gates: 0 frozen stretches > 2.5 s, ≈ −14 LUFS, true peak ≤ −1. Then a fresh-agent critic pass (prompt in topic-mode.md), at most 2 fix rounds.
9. Deliver `share_9x16.mp4` + `script.md` + `captions.srt`, then Sources.

## Files
- scripts: `plan.py` `render.py` (`--still t`) `mix_audio.py` `sfx.py` `storyboard.py` `make_video.py` `guide_plan.py` `guide_voice_intake.py` `vo_split.py` `guide_finish.py` `qa_stills.py` `setup.sh` · Mode D: `topic_build.py` `music_bed.py` (original music bed, any mode) `review.py` (post-render review, any mode)
- templates: `timeline.html` (A) · `illustrated.html` (B) · `guide.html` (C: step / big / who / hook scenes, configurable menu, Bangla + English)
- assets/fonts (OFL) · examples/ (4 real projects + `topic-water-cycle` Mode D demo) · references/ (lessons, component API, topic-mode)
