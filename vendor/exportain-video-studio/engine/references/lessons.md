# Field notes from real jobs (Exportain, Oct 2026)

Five delivered videos: trade-service promo (9:16, captions → reworked to text-free), seller-acquisition promo (9:16 illustrated, text-free), Seller Center tutorial (16:9, 23 segments, 12:25), Service Provider tutorial (16:9, 22 segments, 14:15), Buyer tutorial in ENGLISH for international buyers (16:9, 19 segments, 11:14, hook opener).

## What the client cared about (in their words, paraphrased)
- "Make the SKILL, not the video" — when asked for a skill, do not start rendering test videos.
- "Call the video editing skill and use it properly" — always load this skill before any video work.
- Colourful, professional, never a plain black background; real motion-graphic sound effects, varied, not one sound repeated.
- Promo videos: **no text on screen** — every spoken idea shown as a graphic; realistic, not "AI-looking". Use the real logo.
- Music very low ("so the voiceover is never interrupted"): −28 dB bed for tutorials, −22…−24 dB for promos, always sidechain-ducked.
- Tutorials: explain clearly, make the screenshots understandable, and above all **speech and motion must not drift apart**.
- Tutorials must open by explaining who the portal is for (e.g. Provider = trade services only; anyone with physical products → Seller).

## Environment realities
- Shell network is allow-listed: pip/npm/git usually work; curl to arbitrary sites returns 403. docs sites, storage.googleapis.com (ElevenLabs file URLs) and elevenlabs.io cannot be downloaded from the shell.
- WebFetch can read docs pages but only returns a model summary — ask it explicitly for "every UI label, field, button, status and a description of each screenshot's numbered callouts". Screenshots themselves cannot be downloaded → recreate them as HTML mock screens.
- Fonts: Noto Sans Bengali via `git clone --sparse` of googlefonts/noto-fonts (bundled in assets/fonts now).
- SendUserFile limit ≈ 30 MB → share copies at crf 26 and split long tutorials into Part 1 / Part 2 at a step boundary.
- Shell commands die after 10 min: start renders with `setsid nohup … > log 2>&1 < /dev/null &`, poll with `sleep 590`. A plain `nohup … &` died silently once. Don't run the audio mix in the foreground while a render is using the CPUs — it timed out; background it too.
- Render speed (2 workers, 1080p): ~25k frames ≈ 42 min.

## ElevenLabs (MCP connector)
- One flow per video: `creative_create_flow`, then `creative_generate_speech(model_id='eleven_v4', voice_id=<given>, generations_count=1, flow_id)` once per segment, **sequentially in narration order** (node numbering follows generation order). Never re-call to retry — it charges again.
- Cost ≈ 1 credit per character (≈ 300–700 credits per 30–50 s segment; 22 segments ≈ 10k credits).
- `creative_get_flow_run_status` with all session_ids returns `duration_secs` per generation — write them to `durations.json` and build/QA the whole timeline before the files arrive. Calls with 22 ids can error; query in batches of ~11.
- The user downloads the MP3s and uploads them. Names: `New_tts_node.mp3, New_tts_node1.mp3 …` — numbering base varies between downloads, and old files with the same names linger in the upload folder. Use `guide_voice_intake.py` with only the files from this message; it matches each to nar[N-1]/nar[N] by duration. Real files run ~0.03–0.05 s longer than duration_secs.
- `[warmly]`, `[proud]` style tags at the start of a line work with eleven_v4; they are stripped from on-screen/beat text.
- Write numbers the way they should be spoken when it matters ("প্লাস আট আট শূন্য" for +880). English UI labels stay in English inside the Bangla sentence — the voice reads them naturally and the callout keys can match them exactly.

## Sync technique (what made "speech = motion" work)
- One TTS file per scene → exact scene boundaries (LEAD 0.5 s before the first, GAP 0.8 s between).
- Inside a scene, each callout key's character position → time (`a0 + 3% + 92% × charShare`), then snapped to the nearest pause end (silencedetect −32 dB, 0.12 s) within 0.6 s → the click lands as the word starts.
- Write the narration so every UI element is **named in the same order it appears on screen**; then the callout list is just those names.

## Bugs already fixed in the templates (don't reintroduce)
- CSS transform on an SVG element overrides its `transform` attribute → wrap in `<g>` or use transform-box.
- Measuring text while `display:none` returns 0 → temporarily display the scene to measure (auto-shrink loop).
- Duplicate callouts on one field re-cleared the typed value → `seen` set; first callout owns typing.
- Sidebar logo `<img>` had no height at measure time → all sidebar markers sat one row too high. Fixed with a fixed 61 px height. Any image above measured targets needs explicit dimensions.
- Class-name collisions inside custom scenes (a `.tg` grid picked up the toggle row border) → prefix custom classes.
- Text overflowing chips in portrait → auto-shrink.

## QA habits
- Render stills near the end of every scene (all markers visible) with `qa_stills.py` in one browser session, look at them, fix, then do the full render.
- After the render: contact sheet from the master + `ebur128` integrated loudness (target ≈ −14, result ≈ −13 LUFS).

## English / international videos (Buyer guide)
- Client wanted: English, "international level, no mistakes", Premiere-Pro-grade motion, and an **anchor/hook at the start** that makes viewers stay (promise of what they will learn + strongest benefits). Built as the `hook` scene: question-led line ("What if you could source directly from…"), 4 benefit cards, 3-step roadmap, logo.
- Fact-check every claim in the hook against the docs or reliable knowledge (e.g. "one of the world's largest garment exporters", not a disputed rank; "no membership fees" only because the docs say buyers pay none). Don't embellish UI behaviour.
- English look: `CONFIG lang='en'` → Inter body + Poppins headings (bundled), "STEP 01" counters, light sweep across the window. Example data should feel international (Hamburg buyer, USD, real-looking ports/certifications).
- The same Bangla voice (Debashish) was used for English at the client's request — it works with eleven_v4.

## ElevenLabs account problems
- The connector can suddenly return "Unusual activity… Free Tier access has been disabled… do not retry". Stop immediately, tell the user in one sentence that a paid plan is needed, and offer the fallback: give them the script to generate themselves. Nothing is charged by the refused call.
- To check access later without a full job: `creative_list_voices`, then `estimate_only=true`, then one tiny real line (~20 credits) — estimate_only succeeds even while generation is blocked.
- Fallback that worked: the user generated the WHOLE narration in one prompt on elevenlabs.io and uploaded one MP3. Give them a single text file (`examples/buyer-guide-en/vo_one_prompt_example.txt` format): all segments in order separated by `<break time="2.0s" /> ...`, plus a split point in case of character limits.
- eleven_v4 IGNORED the break tags: gaps between segments were only ~0.5 s and were NOT the longest pauses. `scripts/vo_split.py` solves it (DP on pauses vs character share + "Step…" onset similarity refinement). Without refinement 3 of 18 boundaries were 2–3 s off; with it all matched. The outro (no "Step") and the hook are excluded from the anchor set (`--anchor-to -2`).
- User asked for a slightly slower voice → `--tempo 0.94` (pitch preserved). Re-run guide_plan.py after splitting.
- English TTS pace ≈ 14.5–15 chars/s (Bangla ≈ 10–11); use this to estimate durations.json before audio exists.

## More template fixes
- Fonts other than the Bengali one must be preloaded before `__init` (render.py now loads Inter/Poppins) — otherwise markers/highlights are measured with fallback metrics and land in the wrong place.
- A modal screen shows the previous screen under it; a modal after another modal stacks two dims — use `layout='center'` for the later one.
- Logo from the client: strip near-white to transparent with PIL and crop to bbox; it always sits on a white card in the templates.

## Topic mode (Mode D, Oct 2026)
- The client wants to give only a topic: research it, write the voice script and the video script, build the motion graphics, voice it with ElevenLabs.
- Studied repos: claude-code-video-toolkit, awesome-claude-video-skills (+ motionmaxxing, motion-video-kit, agent-video-editor), claude-video, dramatron, audiocraft. Their methods are adapted in topic-mode.md. None is installed.
- audiocraft/MusicGen can't run here: no GPU, and huggingface.co is blocked by the shell allowlist (as is pip on some days). `music_bed.py` writes an original melody-free bed with an arc instead. Pads must overlap across bar lines, or the bed pumps on every bar.
- One TTS take per scene keeps speech = motion exact. `topic_build.py` joins the takes with 0.7 s gaps into `vo.mp3` and cuts scenes in the middle of each gap.
- A custom template path works: `plan["template"]` may be absolute (render.py joins it onto templates/), so each topic gets its own `scenes.html` without touching the skill.
