# Mode D — Topic → video (full workflow)

The user gives only a **topic**. You research it, write a layered script (voice + scene-by-scene video script), voice it with ElevenLabs, draw new animated scenes for it, generate an original music bed, render, review and deliver.

Methods adapted (studied Oct 2026):
- Dramatron: layered script writing.
- claude-code-video-toolkit: per-scene TTS, pacing guard.
- agent-video-editor: hook, retention, audio targets.
- motionmaxxing: anti-slop checks.
- motion-video-kit: independent critic loop.
- claude-video "watch": review your own render.
- audiocraft/MusicGen: prompt-shaped music. MusicGen itself needs a GPU and Hugging Face, so `music_bed.py` synthesises instead.

## Defaults (unless the user says otherwise)
| Setting | Default |
|---|---|
| Format | 9:16 1080×1920 reel. 16:9 → `--mode captions` (the illustrated template is portrait-only), or Mode C if the topic is a website walkthrough |
| Length | 60–90 s, 8–12 scenes of 5–9 s |
| Look | **Illustrated, text-free**: every spoken idea drawn and animated. Captions only if on-screen text is asked for |
| Language | Bangla. English works the same; budget ≈ 15 chars/s instead of 11 |
| Voice | the user's → else Debashish `3XjJ1C8taYP9CHnHKmK5` → else `creative_list_voices(languages=['bn'])`, pick a clear narrator, say which |
| TTS | ElevenLabs `eleven_v4`, `generations_count=1` |
| Music | user's file → else `music_bed.py` at −24 dB, ducked |
| Logo/brand | only if given (badge + short end card); none → neither |

Project dir `P`: `research.md`, `script.md`, `narration.json`, `board.json`, `scenes.js`, `durations.json`, `vo/`, `music.wav`, `out/`, `review/`. Worked example: `examples/topic-water-cycle/`. Run it with `topic_build.py --project <copy>` and it renders from durations.json.

## Step 1 — research → `$P/research.md`
- 3–5 WebSearch queries in parallel (Bangla + English, Bangladesh angle where it matters), then WebFetch 2–4 authoritative pages (government, WHO/UN, universities, established media, official docs).
- Record facts and numbers with year + URL, common misconceptions, and one surprising hook fact. **Never invent a number.** Time-sensitive facts get "as of <date>".
- Decide **the one true thing** the video says. Choose 3–5 supporting points and drop the rest on purpose.

## Step 2 — layered script (Dramatron method: top-down, each layer conditioned on the one above)
Write these layers into `script.md` in order. Never jump straight to narration.
1. **Logline**: one sentence: who/what, the tension, the payoff.
2. **Title** (internal, not shown).
3. **Cast & world**: 1–3 recurring visual anchors that carry the story through every scene (a named person "রিনা", a water drop, a rickshaw, a seed). Recurring anchors give continuity, and they are what the viewer follows. Give each a fixed look (colours, proportions).
4. **Beat sheet**: one line per scene. *Place* (visual world), *Plot element* (Hook · Setup · Turn · Point 1…n · Payoff · CTA), *Beat* (what **happens**: an event, not a state).
5. **Place descriptions**: for each scene, what is drawn, where, and what moves on which word.
6. **Narration**: written scene by scene, each with the previous beat in view, so it flows as one voice.
7. **Read-aloud pass**: speak it in your head at ≈ 11 chars/s. Cut anything that doesn't serve the one true thing.

### Narration rules → `$P/narration.json` `[{"id":"00_hook","text":"..."}]`, one entry = one scene = one take
- **Hook in the first 3 s**: open on the payoff or a sharp question. No greeting, no "এই ভিডিওতে আমরা দেখব…", no logo intro.
- Open a loop early ("তৃতীয় কারণটাই সবচেয়ে অবাক করা") and pay it off.
- Spoken standard Bangla (চলিত), short sentences, 1–2 per scene, 55–110 Bangla characters. Total ≈ 11 chars/s (90 s ≈ 1000 chars).
- Write numbers as spoken ("দুই হাজার চব্বিশ সালে", "সত্তর শতাংশ"). Keep the English words Bangladeshis actually say. No abbreviations.
- Optional mood tag only at the start of a take: `[excited]` `[warmly]` `[thoughtful]`.
- **Name each visual in the order it appears.** Those words become the animation keys.
- End in one sentence (takeaway or CTA). No recap, no long sign-off.

### Video script → `$P/board.json`, one entry per narration entry
`{"kind":"tp_seed","bg":"c_mint","keys":["বীজ","বৃষ্টি","চারা"],"sfx":["pop","bubble","rise"]}`
- `keys`: 2–6 exact substrings of that scene's text, in spoken order (2–3 words if a word repeats). Each fires the next visual event as it is spoken. Something new every 1.5–3 s, and never a hold over 3 s.
- `sfx`: one per key, varied (whoosh pop pop2 bubble click tick ding sparkle shutter swoosh rise boom riser chime). Bigger sounds only on the Turn and Payoff.
- `bg`: vary. Light: c_peach c_mint c_sky c_lilac c_lemon c_coral c_aqua. Dark (c_deep c_ocean) for the Turn or a dramatic moment.
- `kind`: almost always a new kind drawn for this topic (Step 5). The built-ins (port_roles gap_globe world_arcs supply_chain logo_reveal marketplace showcase profile_build circle_break network_grow phone_visit bridge_connect journey products4 conveyor door categories20 sellers_upload rfq grow visit_trio) are trade/export art. Reuse one only if it truly fits.

### Storyboard check (before spending credits). Fix every "no":
- Is there one true thing, and does every scene serve it?
- Does every beat describe an **event** (something moves, causes, transforms), not a picture that just sits?
- Is every claim in research.md with a source?
- Did you look past the topic's first cliché (rain → umbrella, money → coin stack, internet → globe)? Write the cliché down, then pick something specific to Bangladesh or to this story.
- Is any scene "a small icon on empty ground", a stat slide, a progress bar, a HUD or a label? Redesign it.
- Does the sound have an arc: quieter Setup, a hit or a breath of silence on the Turn, lift on the Payoff?
- Does the hook work in 3 s with the sound off?

Add to `script.md` the table `# | narration | visual event | beat words | sfx`, a **music brief** (MusicGen-style: mood, tempo, instruments, where the drop lands), and the sources.

**Checkpoint:** send the script table with SendUserMessage and ask "voice it?". Voice costs credits (≈ 1 per character), and everything downstream depends on the wording. Skip it if the user said to go straight through, or the run is unattended.

## Step 3 — voice with ElevenLabs (MCP connector)
1. `creative_create_flow(name="<topic> VO")` once.
2. `creative_generate_speech(prompt=<text incl. tag>, model_id="eleven_v4", voice_id=…, generations_count=1, flow_id=…)` **once per scene, sequentially in narration order** (node numbering = generation order). Never re-call to retry: it charges again.
3. Poll `creative_get_flow_run_status` (≤ 11 session_ids per call, wait poll_after_seconds) until complete. Write `$P/durations.json` `{id: duration_secs}`.
4. Files: if the status gives URLs, try **one** `curl -sSfL -o` from the shell. If it is refused (usual), send the flow link and ask the user to download every take and upload them. Continue with Steps 4–5 meanwhile.
5. On arrival: `python3 $SK/scripts/guide_voice_intake.py --project $P <only this upload's files>` → `vo/<id>.mp3`. Fix any "CHECK" lines.
5b. **Connector blocked or unavailable** ("Unusual activity… Free Tier disabled"): stop and tell the user once. Give them one text file with every take in order, separated by `<break time="2.0s" /> ...`. They generate it on elevenlabs.io and upload one MP3. Then run `python3 $SK/scripts/vo_split.py --project $P --voice full.mp3 --no-refine` (topic scenes don't share a start word, so skip the anchor refinement) and check every ratio line.
6. Pacing guard: `topic_build.py` prints chars/s per take. A "FAST" take (> 15 chars/s) gets slowed in place (`ffmpeg -i x.mp3 -af atempo=0.94 y.mp3`) or rewritten and regenerated (one call, with the user's OK). Same for a mispronunciation.

## Step 4 — motion graphics → `$P/scenes.js`
Plain JS, injected into `illustrated.html` before the engine. One `K.<kind>` per new kind:
```js
K.tp_seed=()=>({svg:`<rect width="1080" height="1920" fill="url(#studio)"/>
  <g data-k="tp_soil">…flat SVG art…</g>
  <g data-k="tp_sprout">…</g>`,
 upd(q,lt,t,bt){                       // q(id)=element, lt=local secs, t=global secs, bt(i)=local time of beat i
   const p0=eb(cl((lt-bt(0))/.6));     // beat 0 = keys[0]
   T(q('tp_soil'),{y:L(160,0,eo(p0))+Math.sin(t*1.6)*6,s:L(.6,1,p0),o:cl(p0*2)});
   const p1=eb(cl((lt-bt(1))/.5)); T(q('tp_sprout'),{s:L(.2,1,p1),r:L(-12,0,eo(p1)),o:cl(p1*2)}) }});
```
- Canvas 1080×1920 viewBox. Keep the key art between y≈260 and y≈1650 (reel UI covers the edges). The svg starts with a full rect `fill="url(#studio)"` (or `#night`) so `bg` can recolour it.
- Helpers: `T(el,{x,y,s,r,o})`; easings `eo` `eb` `eio` `es`; `cl`, `L`. Art: `icon(name,x,y,size,col)` (ship truck doc shirt shoe bag box phone mail mappin globe check cart lock cal bld star chat hand arrow linkb), `chip`, `card`, `avatar`, `pin`, `factory()`, `truck()`, `ship()`, `doc()`, `mapper/mapDots/arc` + `CITY`; filters `url(#sh)` `url(#sh2)` (soft shadows), `url(#glow)`.
- **Events, not states**: every beat makes something happen (grow, fill, travel, break, connect, transform), and the result causes the next beat. Carry the recurring anchor across scenes (same look, new situation).
- Stage a picture that fills the frame: a ground plane, depth (near/far scale), light from one side. Never a small card floating in a void.
- Motion: 2–3 properties per entrance, eased (never linear), staggered. The slowest move in a scene ≈ 3× the fastest. Idle breathing on everything that has landed.
- Real things at real proportions, flat shapes, soft shadows. **No text** in illustrated mode. Show quantities as things: bars, a filling vessel, counted objects, a pie that fills.
- Prefix every data-k id and custom class with the kind's prefix (`tp_`). Animate `<g data-k>` wrappers, not shapes that already have a transform attribute.

## Step 5 — plan + QA stills (before the audio arrives)
```bash
python3 $SK/scripts/topic_build.py --project $P [--logo logo.png --brand X --url X]      # --mode captions for text mode
python3 $SK/scripts/qa_stills.py --plan $P/plan.json --size 1080x1920 --cols 4 --out $P/qa.jpg <every "still:" time printed>
```
The build must show **0 key warnings**. Read the sheet. Check: everything visible, nothing clipped or overlapping, varied colours, each scene readable without words, the anchor consistent. Check 2–3 mid-scene times for motion too. Fix and repeat. After voice intake, rerun both (real takes → exact lengths, beats snapped to word onsets, `vo.mp3`).

## Step 6 — music → `$P/music.wav`
User's track → use it. Otherwise generate an original bed matched to the music brief. Put the drop at the start of the Turn or Payoff scene (its `start` in plan.json):
```bash
python3 $SK/scripts/music_bed.py --duration <plan total> --mood calm|hopeful|upbeat|warm|curious|tense|epic --drop <turn start> --out $P/music.wav
```
It's melody-free (it sits under speech), structured on bars, with intro → build → breakdown + riser → drop → a real ending on a bar line. MusicGen (audiocraft) needs a GPU and Hugging Face weights, which this sandbox can't reach. If the user has MusicGen or another generator, give them the music brief as the prompt and use their upload.

## Step 7 — render (background)
Use Bash `run_in_background: true` (or `setsid nohup … > out/render.log 2>&1 < /dev/null &`):
```bash
python3 $SK/scripts/make_video.py --voice $P/vo.mp3 --plan $P/plan.json --music $P/music.wav --music-db -24 --formats 9:16 --outdir $P/out
```
≈ 1.7 frames/s per worker, 2 workers: 90 s ≈ 14 min. Wait for the completion notice. Run no other heavy jobs meanwhile.

## Step 8 — review: watch your own film, then a critic
```bash
python3 $SK/scripts/review.py --video $P/out/final_9x16.mp4 --plan $P/plan.json --out $P/review
```
Read **every** sheet and `report.txt`. Gates:
- 0 frozen stretches > 2.5 s.
- Loudness ≈ −14 LUFS (−13…−15), true peak ≤ −1 dBTP.
- No scene mostly still.
- First 3 s readable on mute.
- Ending ≤ 1.5 s after the last word (+ end card if a logo).

Then a critic pass: send the sheets, report and script.md to a **fresh agent** that did not build it (Agent tool) with this prompt:
> You are an independent, blunt critic; you did not build this. Judge rendered frames and measured audio only. Video: <path>, <duration>s 1080×1920, Bangla text-free motion-graphics explainer about <topic>; its one message: <one true thing>. Read the contact sheets <paths>, report <path>, script <path>. Report under 500 words: per scene, the problems ranked (slide-like frames, small object on empty ground, holds, clichés, unclear picture for the words, inconsistent anchor, colour monotony); then the top 5 fixes, concrete and implementable in SVG/JS; end with SHIP or ONE MORE PASS.

Apply the fixes, re-render, re-review: **two passes at most**. Never certify your own film without the numbers. Music or SFX changes alone: rerun `mix_audio.py` and mux with `-c copy`, no re-render.

## Step 9 — deliver
SendUserFile: `out/share_9x16.mp4` (≤ 30 MB; else re-encode crf 26), `script.md`, `out/captions.srt`. Reply in one line on what the video covers, then "Sources:" from research.md.

## Lessons carried over
- Speech = motion: one take per scene, one spoken key per beat.
- Colourful gradients, never flat black. Varied SFX. Music low and ducked. Real logo, untouched.
- Shell network is allow-listed: ElevenLabs/Hugging Face URLs are usually unreachable, so the user uploads takes. Commands die after ~10 min: background long jobs.
- QA stills before the render, review sheets after. Never ship blind.

