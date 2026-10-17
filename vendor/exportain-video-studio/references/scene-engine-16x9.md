# Turn 2 craft — how the animated 16:9 scenes are built

## How the machine works (so you can reason about problems)
1. `full.mp3` (one ElevenLabs take) → `split_check.py` cuts it into `vo/<id>.mp3`, one file per narration item, at the
   2 s breaks (boundary RMS ≈1 = cut in silence). Per-scene API files (`tts_scenes.py`) skip this step.
2. `build.sh` = `cat js/*.js > scenes.js` → engine `topic_build.py` → `plan.json` + `vo.mp3` + `scenes.html`:
   - scenes are laid end to end with a small gap; each scene gets `start/end` and **beats** = the time of every
     board key: the key's character position inside the scene text × scene duration, snapped to a nearby pause
     (±0.6 s), at least 0.3 s apart. So a key fires roughly when the word is spoken.
   - `scenes.html` = engine template `illustrated.html` + your scenes. build.sh then patches it for Exportain:
     fonts (Noto Sans Bengali `B`, Inter, Poppins `Pop`), logo badge 7 % height top-left, **viewBox 1920×1080**,
     a stronger camera drift (prevents frozen frames), light brand gradients `e_*`, end card with "Exportain.com".
3. `make_video.py` opens scenes.html in headless Chromium, calls `render(t)` for every frame (30 fps), records,
   mixes voice + music bed (ducked under speech) + one SFX per beat (`board.sfx`), writes `final_16x9.mp4` + captions.
4. `finish.sh` → limiter, loudness (target ≈ −13.5…−14 LUFS, true peak ≤ −1.05 dBFS), `review.py` (frozen-frame
   detector: any > 2.5 s with no visual change fails), compressed share copy `<Name>.mp4` + `<Name>.srt`.

## A scene
```js
K.pd_rules=()=>({svg:`${BG} … <g data-k="r_bk">…</g> …`,          // drawn once
 upd(q,lt,t,bt){ … }});                                              // every frame
```
- `kind` in board.json = the K name. Prefix = 2 letters per project (`pd_`, `dl_`, `bs_`) so ambient code
  (`99_amb.js`, bubbles drifting on every scene) and old projects never collide.
- `data-k="id"` marks anything you animate; `q('id')` returns it. **ids must be unique inside the scene.**
- `lt` = seconds since scene start, `t` = global time, `bt(i)` = local time of key i (board order).
- `T(el,{x,y,s,r,o})` sets a transform **relative to where the element was drawn** (+opacity). To move an element to
  absolute positions, draw it at 0,0 (e.g. `cash(0,0)`) and pass x/y.
- Interpolation: `L(a,b,p)`, `cl(v)`, easing `eo` (out), `eb` (back/overshoot), `eio`; progress `pe(lt,b,d)`.

### Reveal vocabulary (use these, they keep the house style)
| call | effect |
|---|---|
| `popG(el,lt,b,t,i,dy=60,bob=4,d=.85)` | **ghost-then-pop**: before b the element shows at 16 % opacity (viewer sees the layout coming), at b it pops up with overshoot, then bobs gently. Default for cards. |
| `popIn(el,pe(lt,b,.35),t,i,dy,bob)` | plain pop (hidden before b) — for checks, chips, small items |
| `kw(id,x,y,'text',size,col,hl)` + `kwU(q,id,lt,b,t)` | kinetic word/phrase on a coloured highlight bar (hl) — the "muted viewer" text |
| `ttl2(P,'৩','পচনশীল কি?',C.o)` + `ttlU(q,P,lt,t)` | title card top-left (80–860 × 170–280) on the FIRST scene of each point |
| `rd(P)` + `rdU(q,P,lt,t,cur)` | 5-step road-map top centre (x 700–1700, y 30–140); done steps green, current step coloured & pulsing. Labels in `3_0helpers.js` `RLS.A` (two-part videos: copy `examples/dalal/js/3_0helpers.js` — `rd(P,'B')` uses `RLS.B` and adds a "ভাগ ক/খ" pill). |
| `fillTo(rectEl,lt,b,w,d)` | bar/meter grows to width w (`meter(x,y,w,h,col,id)` draws track + bar) |
| `slideG`, `pulse`, `fadeMul(el,v)` | slide in; spin-pulse; dim something that is "over" |
| idle motion | after an element has appeared in a long scene: `if(lt>X)T(q(id),{y:Math.sin(lt*2)*10,o:1})` — **required** wherever nothing new happens for > 2 s |
| shake | `T(el,{x:Math.sin(t*22)*cl(b+.8-lt)*8,o:1})` for "problem" moments |
| counter/strokes | set attributes per frame: `setAttribute('stroke-dashoffset',…)` draws lines; `'stroke-dasharray'` for gauges |

Timing rules: one visual event per board key; ≥ 0.3–0.7 s between reveals; **something visible within 0.3–1 s of
scene start** (bring the first card in with `Math.min(bt(1)-.3, .9)`); last reveal ≥ 1.5 s before scene end;
long scenes (> 12 s) need idle motion or more keys.

## Canvas & layout grid (1920×1080)
- Reserved: logo badge top-left (≈ 0–260 × 0–100); road-map top centre (700–1700 × 0–150).
- Side margins 100 px. Content band y ≈ 190/330 → 980. Title card scenes start content at y 330.
- Proven columns: 2 cols `100–900 | 980–1820`; 3 cols width 540 at x = 100+i*590; 4 cols width 410 at x = 100+i*440;
  left character card `100–660` + right panel `740–1820`.
- Text: Bangla `tx(x,y,txt,size,col,weight,anchor)` (font B), Latin `lat(...)` (Poppins). Min 26 px; headings 44–56;
  big numbers 110–200. Card label length > ~12 Bangla chars → drop size to 32–34. `kw` highlight width is estimated
  from text length — keep its centre ≥ (len×size×0.3) from the edges.
- Colours `C`: g #2E8B2E (positive), gd #005A1E (brand cards), f #003C10, g2/l #5CBF14, y #F2B705, t #0E8C88,
  b #0B5F8A, bd #0B3B5C, o orange, p purple, pk pink, r #D93636 (**risk only**), ink, mute.
- Backgrounds (board `bg`): e_mint e_lime e_sea e_gold e_sky (light, rotate them) · e_forest/e_deep dark (bridges only;
  draw `<rect width="1920" height="1080" fill="url(#e_forest)"/>` after `${BG}` and use white text).

## Drawing library (see helpers-api.md for every signature)
- Containers: `card`, `docPage(x,y,w,h,title,col,lines)`, `cert`, `ercCard`, `browser(x,y,w,h,url,col)`,
  `phone(x,y,w,h)`, `laptop`, `field(x,y,w,label,col,id)` (fillable), `bub(x,y,w,text,bg,fg,size,tail)`, `pill`, `chipT`,
  `meter`, `cal(x,y,w,day,month,col)`, `badge`, `stampT`, `check`, `cross`, `slash`, `octo` (STOP sign), `qr`.
- People: `person(x,y,s,'s'|'g'|'n',id)` (head at y), `woman2(x,y,s)` (head at y), `brk` (broker with cap & shades),
  `womanMini`.
- Things: `icon(name,x,y,size,col,stroke)` with names ship truck doc shirt shoe bag box phone mail mappin globe check
  cart lock cal bld star chat hand arrow linkb; `mag(x,y,s,col)` (**col required**), `coin`, `cash`, `bank`, `factB`,
  `bldg`, `shipA`, `plane`, `carton`, `pallet`, `folder`, `scanner`, `cloudS`, `pdfF`, `mat` (শীতলপাটি), `jutebag`,
  `basket`, `mango`, `rice`, `seeds`, `leaf2`, `fish2`, `shrimp2`, `kantha`, `honey`, flags `bdflag deflag euflag ukflag`
  (no detailed foreign flags — use code circles like "AE", "US").
- Add new art per topic in `js/2e_extra.js` (copy into the project) — every video should get at least 2–3 new drawings.

## Scene recipes that worked (vary them — the client wants variety, never caption slides)
| content | recipe |
|---|---|
| hook | big "?" with products orbiting; money flying into a broker; customs counter + red stamp "গ্রহণযোগ্য নয়"; problem item shakes; end on a big `kw` promise ("৫টি প্রশ্নে সঠিক পণ্য") |
| fictional character | left card: person + "নাম · জেলা" + purple pill "কাল্পনিক চরিত্র" + their product; right: options/old-vs-new panels |
| point opener | `ttl2` + road-map + one strong metaphor (wallet with cost blocks stacking, policy book + prohibited tiles with red slash) |
| list of N items | N cards popping on their keys; icon in tinted circle; Latin name big + Bangla meaning small |
| process / steps | numbered cards with arrows; browser mockup with real URL (`olm.ccie.gov.bd`, `bswnbr.gov.bd`, `trademap.org`), fields filling (`fillTo`), button press scale .93, tap ripple `tap(id)` |
| numbers | big stat cards (২২০+ / ≈৫,৩০০ / ফ্রি), bar meters with % labels, counters, confetti (`k_f` pattern in bsw example) |
| comparison | table ✕ vs ✓ (dalal vs professional), scorecard grid products × questions, before/after cards |
| time / perishability | colour-changing timeline, clock hand rotating `T(hand,{x,y,r:t*120})` |
| rules / risk | STOP octagon slamming in (scale 2.2→1), red cross, shake, lock icon |
| documents system | scanner → PDFs fly into a folder; file names morph from messy to the naming rule; spreadsheet with "উদাহরণ" tag; cloud upload arrow (dash offset animation) |
| success | ship/plane, "Payment Successful" phone, "Thanks!" reply, staircase with the character climbing |
| Exportain | logo image `__LOGO__` floating (s & y sine), company page "Company page · <Character's company>" with 3 items "Verified", dark-green tag "বাংলাদেশি প্রস্তুতকারক ও রপ্তানিকারকদের B2B মার্কেটপ্লেস", buyer card with bubble or search bar (`starter16/js/3_9end.js` → `K.PFX_brand`) |
| advice | three cards (authority / AD Bank / professional) + `kw` banner, each floating |
| CTA | BD flag card "প্রস্তুতকারক বা রপ্তানিকারক?", globe with orbiting product icons, logo, green "Exportain.com" button pulsing, tap ripple, orange `kw` "আজই ভিজিট করুন" (`K.PFX_cta`) |
Invented data on screen (dates, country bars, HS search results) → small tag **"উদাহরণ" / "চিত্র উদাহরণ"**.

## Pitfalls (all happened — check_js.sh catches most)
1. `${0}+` / `${0}||` placeholders left in code → `sed -i 's/\${0}+//g; s/\${0}||//g' js/3_a.js js/4_b.js`.
2. Writing `tx(820,${928-i*130},…)` inside a `${…}` expression is a syntax error — write `tx(820,928-i*130,…)`.
   Fix: `sed -i -E 's/,\$\{([0-9]+[-+]i\*[0-9]+)\},/,\1,/g' js/*.js`.
3. Re-declaring a lib name (`CATS`, `R5L`, `card`…) → "Identifier already declared": rename yours (PCAT).
4. `mag()` without colour draws nothing; `icon('svg')` / unknown icon names render blank.
5. Element ids reused across scenes are fine, inside one scene they are not.
6. White plane/text on white card; red used for non-risk things; Latin words in Bangla font (use `lat`).
7. Frozen stretches: always at scene starts (only a title showing) or after the last reveal of a long scene →
   earlier first reveal + idle motion (see `frozen_map.py`).
8. A dark-bg scene needs light text; `kw` on dark → `kw(id,x,y,txt,size,C.gd,'#fff')`.
9. Ads: ElevenLabs often ignores `<break>` → `split_check` shows BAD → `manual_split.py --pauses` and cut by ear/text.
   Never cut after the first word of the hook (the client noticed a missing "এক্সপোর্ট কোর্স শেষ").

## QA checklist for every contact sheet
Overlap/clipping (labels touching card edges, pills colliding, text past 1820 px), empty halves, illegible small
text, duplicate titles, wrong road-map step, Latin vs Bangla font, invented numbers without "উদাহরণ", red used only for
risks, fictional label visible, Exportain scene + CTA present, last frame of each scene "complete".
