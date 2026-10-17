# Exportain — brand, facts and the client's standing rules (non-negotiable)

## Who
Exportain (exportain.com) is the client's own brand: a Bangladeshi **B2B export marketplace** connecting Bangladeshi
manufacturers/exporters with international buyers, plus export service providers. Feature truth: https://docs.exportain.com
(WebFetch the relevant page before any feature claim). Sellers: seller.exportain.com · Providers: provider.exportain.com.

## Brand colours (from the logo)
| token | hex | JS | use |
|---|---|---|---|
| brand-green | #005A1E | `C.gd` | brand cards, CTA, dark headers |
| brand-forest | #003C10 | `C.f` | deep backgrounds |
| brand-lime | #5CBF14 | `C.g2`/`C.l` | highlights |
| brand-leaf | #2E8B2E | `C.g` | checks, positive, buttons |
| accent-gold | #F2B705 | `C.y` | B2B tag, small accents |
| accent-teal | #0E8C88 | `C.t` | secondary |
| accent-navy | #0B3B5C | `C.bd` (blue `C.b` #0B5F8A) | Latin headings, browser bars |
| signal-red | #D93636 | `C.r` | **only** risks, mistakes, prohibited |
Scene backgrounds: light brand gradients `e_mint e_lime e_sea e_gold e_sky`; dark `e_forest` only for a bridge/hook.

## Logo
`starter16/assets/logo.png` = transparent 752×217 PNG, used unaltered: top-left badge on every scene (build.sh),
large floating logo in the Exportain scene and CTA (`<image href="__LOGO__">`), silent end card with "Exportain.com".
The client keeps the logo in claude.ai "Exportain" Design System artifacts and usually sends one link with the voice:
https://claude.ai/artifact/KsdQD7N8mWtKrnSJnB1ByJ or https://claude.ai/artifact/ExDz8iJRmMHZxq7RhiDMok (same kit:
original 790×316, transparent 752×217, colours). The bundled PNG is identical — no need to download.

## Exportain features you may state (docs, Oct 2026)
- Buyers post RFQs and compare quotations from verified sellers; can find/request trade services.
- Sellers: company page, product listings, answer RFQs with quotations; certificates on the company page show
  "Verified until …" after approval; payouts in BDT to a verified Bangladeshi bank account (target ≈ 7 days).
- Providers (10 categories: freight forwarders, shipping agents, customs brokers/C&F, inspection & audits,
  certification bodies, bonded warehousing, export packaging, sourcing & buying houses, cargo insurance, trade finance):
  listing with photo, price, service areas (up to 20), licence verification → Verified Provider badge, leads →
  price offers → service orders, freight rates. Plans in docs: Free (docs say first 90 days; 3 listings, 15 lead replies/
  month, 5 % commission), Gold 599 BDT/month (2 %), Platinum 1,199 BDT/month (0 %).
  **Client instruction for ads: say "লাইফটাইম ফ্রি" for provider accounts (not "৯০ দিন")** — remind them once that docs
  still say 90 days and captions should add "কমিশন প্রযোজ্য".
- Never invent prices, user counts, rankings, guarantees or features.

## Standing rules (all videos)
1. Research first; only current verified facts with year + source; "today" = the date the user gives.
2. **Format: 16:9, 1920×1080 for all topic videos** (rule since Oct 2026). 9:16 only when asked (reels/ads).
3. **Illustrated motion graphics only** — every idea drawn and animated (people, objects, documents, flows). Text-led
   caption-slide frames are never acceptable. Vary the visual style from video to video ("not always same style").
4. Every video: one dedicated Exportain scene in the body, tied to the topic, with
   "এক্সপোর্টেইন হলো বাংলাদেশি প্রস্তুতকারক আর রপ্তানিকারকদের বিটুবি মার্কেটপ্লেস…", **plus** the CTA
   "আপনি যদি বাংলাদেশের প্রস্তুতকারক বা রপ্তানিকারক হন, বিশ্বের ক্রেতাদের কাছে পৌঁছাতে আজই ভিজিট করুন এক্সপোর্টেইন ডট কম।"
5. **No spoken outro after the CTA**; 2.5 s silent logo end card.
6. Voice text: Bangla script only, no slash, no Latin; acronyms in Bangla; Latin forms on screen.
7. Fictional characters named and labelled (voice: "একজন কাল্পনিক উদ্যোক্তা"; screen: pill "কাল্পনিক চরিত্র").
8. No naming of weak banks, accused firms or people in the voice.
9. Legal/regulatory/fee topics end with the advice line (authority / AD bank / professional).
10. Never mention previous or next episodes. Automation reels: 3–5 minutes.
11. Voice: the user records on elevenlabs.io — voice **Debashish** (id 3XjJ1C8taYP9CHnHKmK5), model **eleven_v4**,
    speed 1.00, stability 50, similarity 75 (files "ElevenLabs_<date>_Debashish_-_Warm_Proud_gen_sp100_s50_sb75_v4.mp3").
    The automation pipeline uses the API with the same voice (model eleven_v4_turbo, Bangla only) — locked.
12. Look: professional, colourful, brand colours, light gradients, calm reveals (nothing flashes by), camera drift,
    ambient bubbles, varied SFX, low ducked music, ≈ −13.5…−14 LUFS, 0 frozen stretches.
