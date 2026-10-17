# Ads (Facebook / Instagram / YouTube) — playbook

Examples: `examples/ad_adseller` (seller invite 9:16, 47 s, with `ad_seller_plan.md`), `ad_ad169` (same 16:9),
`ad_adprov` (provider invite 9:16, 37 s, `ad_provider_plan.md`), `ad_prov169` (16:9).

## Turn A — plan first (the client asked: "plan first, then tell me which voice to record")
Deliver `<name>_plan.md` (goal, format, one-sentence message, verified facts with docs URLs, scene table with time,
voice, motion, music/SFX plan, 2–3 alternative hooks) + `<name>_voiceover.txt`.
- Audience examples: people taking export courses / interested in exporting → free seller account; export service
  providers (freight, C&F, packaging…) → provider account, "লাইফটাইম ফ্রি" (client's instruction).
- **< 60 s** (450–650 chars). Hook in the first 2–3 s, voice + giant on-screen text together, no logo intro, no greeting.
  The client rejected a weak hook once — make it a sharp question/pain: "এক্সপোর্ট কোর্স শেষ? এবার বায়ার পাবেন কোথায়?",
  "রপ্তানির সেবা দেন? এবার ক্লায়েন্টরাই আপনাকে খুঁজে নেবে।"
- Works muted: every scene has big kinetic Bangla text; a cut every 4–8 s; something moves every 1–1.5 s.
- Logo reveal at ~8–10 s with music drop; CTA twice (mid + end); end button "Exportain.com — ফ্রি সেলার অ্যাকাউন্ট খুলুন".
- Only documented features.

## Turn B — build
- Voice often comes without usable breaks → `manual_split.py --pauses`, map pauses to phrases, cut; check the first
  word of the hook is not lost (listen to vo/00_*.mp3 duration vs text).
- Same engine; 9:16 uses `new_project.sh … --916` (1080×1920, starter916), 16:9 the default starter.
- Music: `render.sh <dir> <Name> upbeat <reveal_time> -21`.
- Deliver MP4 + SRT; then captions on request.

## Captions the client asked for (write in Bangla, polished, "high class")
- Facebook/Instagram: hook line, 3–5 short benefit lines with tasteful emoji, clear CTA with link
  (seller.exportain.com / provider.exportain.com / exportain.com), 5–10 hashtags (#Exportain #রপ্তানি #ExportBangladesh
  #B2B #MadeInBangladesh …), compliance notes where needed ("কমিশন প্রযোজ্য").
- YouTube: SEO title (≤ 70 chars, Bangla + key English term), description (summary, timestamps for long videos,
  links, hashtags), 15–25 tags, Shorts title variant. For keyword data use the keyword-research skill if installed.
