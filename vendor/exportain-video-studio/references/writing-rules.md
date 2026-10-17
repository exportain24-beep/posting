# Turn 1 — research, narration, voiceover prompt, script

## What the user sends
Usually Bangla, in this shape (sometimes 2–3 topics pasted together with "এই দুইটা/তিনটা মিলে একটা ভিডিও"):
```
শিরোনাম: …            ভিডিওর মূল ভাবনা: …       দর্শক: বাংলাদেশি রপ্তানিকারক, লেভেল বিগিনার (নতুন উদ্যোক্তা)
আজকের তারিখ ধরে নাও: অক্টোবর ২০২৬
মূল পয়েন্ট (সবগুলো কভার করতে হবে, এই ক্রমে): ১. … ২. … ৩. … ৪. … ৫. …
রেফারেন্স: <urls>        লেখার নিয়ম: … (optional)        length wish (optional, e.g. "সাড়ে চার মিনিট")
```
Start immediately with one sentence ("দুটো টপিক মিলিয়ে সাড়ে চার মিনিটের স্ক্রিপ্ট বানাচ্ছি…"), no questions
unless the request truly contradicts itself (e.g. a pasted file is truncated — then ask how to combine).

## Research (before writing a single line)
- 3–8 WebSearch queries in parallel (Bangla + English), then WebFetch the 3–6 best pages. Open the user's reference
  links when reachable (gov sites often time out → use news reports of the same circular/notice).
- Source priority: government (NBR, EPB, CCI&E/olm.ccie.gov.bd, Bangladesh Bank, BSW bswnbr.gov.bd, customs hub
  hub.bangladeshcustoms.gov.bd, bangladesh.eregulations.org — note eRegulations pages can be years old), ITC/intracen,
  then The Daily Star, The Financial Express, TBS, Prothom Alo, bdnews24, Dhaka Tribune, UNB, Ittefaq.
- Every number gets its year/date + URL. Search for the **newest** figure up to the user's "today" (fees and policies
  change; FY data: Bangladesh FY = July–June).
- Fees/amounts that you cannot confirm as current → do NOT speak an amount; say "সর্বশেষ ফি পোর্টালে দেখে নিন" and record
  the old figure in the script notes as "যাচাই দরকার".
- Exportain claims only from docs.exportain.com (see exportain-brand.md).

## Length → characters
Measured on the client's voice (Debashish, v4, one prompt with 2 s breaks): **≈ 0.0858 s of finished video per
character** (tags excluded, breaks and end card included) → 1 minute ≈ 700 chars.
| wish | chars | scenes |
|---|---|---|
| ~3.5 min (default single topic) | 2,300–2,500 | 18–20 |
| ~4 min | 2,700–2,800 | 19–21 |
| ~4.5–5 min (combined topics) | 3,100–3,400 | 24–26 |
| ad < 60 s | 450–650 | 6–9 |
Automation reels (the posting pipeline) must be 3–5 min. `make_scripts.py` prints the estimate — trim/extend until it fits.

## Narration structure (narration.json = [{id,text}], ids "00_hook", "01_story", …)
1. `00_hook` — tension or question in 1–3 short sentences, may start with `[curious]`. E.g. "রপ্তানি শুরু করবেন, কিন্তু কোন
   পণ্য দিয়ে? ভুল পণ্য বাছলে প্রথম চালানেই আটকে যেতে পারেন। আজ পাঁচটা প্রশ্নে সঠিক পণ্য বাছাই।"
2. `01_story` — a fictional entrepreneur from a district with a concrete product, **labelled in the voice**:
   "রংপুরের শাহেদ, একজন কাল্পনিক উদ্যোক্তা, …". Used so far: যশোরের রাকিব, খুলনার সুমন (চিংড়ি), সিলেটের রুমানা
   (শীতলপাটি), রংপুরের শাহেদ (পাট) — pick a new name/district/product each time.
3. The user's points **in the given order**, each opened with "প্রথম কথা / প্রথম প্রশ্ন / প্রথম, …", "দ্বিতীয়…",
   … 1–3 scenes per point. Concrete, verified facts; numbers spoken in words ("দুই হাজার পঁচিশের জুলাই", "সাত শতাংশের বেশি").
   Two-topic videos: "আজকের ভিডিও দুই ভাগে…", part ক (5 points) → one bridge sentence → part খ (5 points).
4. `NN_story2` — the character's outcome using the points (makes it memorable).
5. Optional tip/habit scene.
6. `NN_brand` — the Exportain scene, tied to the topic, containing the sentence
   "এক্সপোর্টেইন হলো বাংলাদেশি প্রস্তুতকারক আর রপ্তানিকারকদের বিটুবি মার্কেটপ্লেস, …".
7. `NN_advice` — rules change / check with the authority, AD bank or a professional ("…আপনার এডি ব্যাংকের সাথে মিলিয়ে নিন।")
   — mandatory for legal, regulatory, fee or banking topics.
8. `NN_cta` — exactly: "আপনি যদি বাংলাদেশের প্রস্তুতকারক বা রপ্তানিকারক হন, বিশ্বের ক্রেতাদের কাছে পৌঁছাতে আজই ভিজিট করুন এক্সপোর্টেইন ডট কম।"
   **Nothing after it** (no outro; a silent 2.5 s logo end card follows).

## Voice-text rules (make_scripts.py asserts the first two)
- Bangla script only — **no Latin letters, no slash** ("বি এল", not B/L).
- Acronyms/English terms written in Bangla as they are spoken: ইআরসি, আইআরসি, ই টিআইএন, বিএসডব্লিউ, ইপিবি, এইচএস কোড,
  এলসি, সিএন্ডএফ, এডি ব্যাংক, ওটিপি, বিআইএন, বিডা, বেপজা, বিজিএমইএ, ট্রেড ম্যাপ, পিডিএফ, গুগল ড্রাইভ. First use gets a
  short Bangla meaning: "ইআরসি, মানে রপ্তানি নিবন্ধন সনদ". The screen shows the Latin form (ERC, HS Code, BSW…).
- No hyphenated Latin; "ই টিআইএন" not "ই-টিআইএন".
- Never name banks, firms or people in a negative/accusing context; general wording ("কিছু ক্ষেত্রে অভিযোগ ওঠে").
- Hedge what is uncertain: "সাধারণত", "হতে পারে", "সর্বশেষ নোটিশটাই দেখুন".
- Never mention previous/next episodes ("আগের ভিডিওতে…") — videos are standalone.
- Friendly spoken Bangla (প্রমিত, কথ্য), short sentences, 55–230 chars per scene.
- Tags: only at scene start, sparingly: `[curious]` hook, `[warmly]` CTA optional.

## meta.json (drives the two output files)
`title, prefix, format ("১৬:৯"), length_bn, acronyms (Bangla list), idea, audience, story, order (which scenes cover
which point), vis{scene_id: what is drawn, naming the Latin on-screen text}, verified[markdown bullets: fact + source +
date; "যাচাই দরকার" items], sources[urls]`. Then `python3 $S/tools/make_scripts.py <dir>` writes
`<prefix>_voiceover.txt` (one ElevenLabs prompt, scenes joined by `<break time="2.0s" />`, START/END markers, how-to
header) and `<prefix>_script.md` (scene table + verification + sources). See examples/prod.

## Reply to the user (Bangla, short)
SendUserFile both files (display attach), then: what to paste into ElevenLabs (Debashish, eleven_v4), duration +
scene count, the story, how the points are ordered, **যাচাই করা তথ্য** bullets (numbers with years), what was
deliberately left out or hedged and why, "ভয়েস পাঠালেই ১৬:৯ ভিডিও বানিয়ে দেব।", then `Sources:` markdown links.
