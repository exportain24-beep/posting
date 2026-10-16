# Content guide for Claude's episode-writing task

This file is the brief for the scheduled Claude task that keeps the episode queue full.
Claude writes **data only** (JSON episode files) to the `content` branch. It never edits
`main`, never touches workflows, and never sees any API key.

## Each run
1. Clone the repo, fetch the `content` and `state` branches.
2. Read `state:posts.json` → `used` lists episode ids already produced. Queue = `content:queue/*.json` whose id is not in `used`.
3. If the queue has **8 or more** unused episodes, stop: nothing to do.
4. Otherwise write new episodes until there are 10 unused ones.
5. Run `python3 scripts/pipeline.py validate <new files>` from `main`. Fix every error.
6. Commit only `queue/*.json` to the `content` branch and push. Delete files whose id is in `used` and older than 30 days.

## Rules for every episode
- Brand: **Exportain** (exportain.com), a Bangladeshi B2B export marketplace. Feature reference: docs.exportain.com.
- Audience alternates: about half `seller` (Bangladeshi exporters, manufacturers), half `provider`
  (shipping agents, C&F agents, packing factories, other export-service businesses). Provider accounts are **lifetime free** — never write "90 days free".
- Research first. Use only current, verified facts. If a number cannot be verified, leave it out.
- Mention Exportain once in the body where it fits naturally, plus the closing CTA scene.
- Length: 25–60 seconds of voice (200–900 narration characters in total). Hook in the first 2–3 seconds.
- Vary topics, layouts (`theme`: light / dark / navy), `mood` (calm hopeful upbeat warm curious) and scene kinds.
- Never repeat a topic that appears in the last 30 used episodes.

### Narration (what ElevenLabs reads)
- Bangla only. No Latin letters, no slash. English words in Bangla script:
  B/L → "বি এল", HS code → "এইচ এস কোড", LC → "এল সি", B2B → "বি টু বি", exportain.com → "এক্সপোর্টেইন ডট কম".
- Short spoken sentences. One idea per scene.

### On-screen text
- May use the proper form (B/L, HS Code, LC). Wrap one key word in `*stars*` to highlight it.
- `caption` (optional per scene) = subtitle text; if absent the narration is shown.

## File format (`queue/<YYYY-MM-DD>-<slug>.json`)
See `examples/sample-episode.json`. Fields:

| field | notes |
|---|---|
| `id` | lowercase slug, unique, e.g. `2026-10-20-hs-code-basics` |
| `audience` | `seller` / `provider` / `buyer` / `general` |
| `theme`, `mood` | visual theme and music mood |
| `scenes[]` | 3–9 scenes; `kind` = hook / point / stat / steps / cta; last one must be `cta` |
| scene fields | `narration` (required), `title`, `kicker`, `body`, `icon` (one emoji), `bullets` (≤4), `stat {value,label}`, `url`, `sub`, `caption` |
| `youtube` | `title` (≤95, no < >), `description`, `tags[]` — SEO in Bangla + English |
| `facebook` | `description` with link and 3–5 hashtags |
| `tiktok` | `caption` with 3–6 hashtags |
| `thumbnail` | `chip`, `headline` (≤70), `sub`, `icon` |
