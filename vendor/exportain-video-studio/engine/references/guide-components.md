# Tutorial mode — screenplay.py reference (templates/guide.html)

A tutorial is `INTRO + STEPS + OUTRO`, one narration segment (one TTS file) per scene, in that order.

## Optional CONFIG (portal look)
```python
CONFIG = dict(
  menu=[['Home',['Overview']],['Your services',['My Services','Freight rates']], ...],  # sidebar groups
  steps=20,                     # progress dots on the left panel
  url='provider.exportain.com', # default address bar text
  add_label='+ Add service',    # header button text
  badges={'Leads': 5},          # red counters on menu items
  lang='en',                    # 'en' = English look: Inter + Poppins, 'STEP 01' counters (default Bangla: ধাপ ১)
  search='Search products & suppliers…',  # header search placeholder
)
```
Without CONFIG the template falls back to the Seller Center menu (Selling / Inbox / Buy trade services / Company), 21 dots, seller.exportain.com.

## Scene kinds
| kind | use | fields |
|---|---|---|
| step (default) | a recreated portal page | `n, title (Bangla), icon, url, active (menu item), side (False = no sidebar, e.g. login/register), screens, callouts, sfx` |
| `big` | intro / outro title card with logo and orbiting icons | `title, sub` |
| `hook` | English/international attention opener (≈25–35 s): kinetic headline (word-by-word masked rise), a fact pill, 4 benefit cards (optional red strike-through), then a "what you'll learn" 01-02-03 roadmap with a drawing progress rail, then logo reveal with light sweep + tagline. Fields in `hook=dict(l1, l2, pill, cards=[[label, icon, colour, strike?]×4], stay, road=[[label, icon, colour]×3], tag)`. Callout ids in order: `h1, h2, pill, c0..c3, stay, r0..r2, logo` (phase 1 exits at `stay`, phase 2 exits at `logo`) | `hook`, `callouts`, `sfx` |
| `who` | "who should open which account" comparison (Provider vs Seller). Fixed layout: logo + question, green panel with 10 service tiles L0..L9 + chip Lok, VS, orange panel with 4 product tiles R0..R3 + chip Rok, CTA `go`. Callout ids: `q, L, L0..L9, Lok, R, R0..R3, Rok, Lg (glow left), Rg (glow right), go` | `callouts` only |

Icons (`icon` and inside templates): rocket grid store box shield bank cart doc ship wallet truck star help key phone chat bell team scale lock mail plane anchor stamp search medal warehouse shirt shoe sack leaf.

## Screens
`screens=[dict(comps=[...]), dict(layout='center', comps=[...]), dict(layout='modal', comps=[...])]`
- default: full content area under the header. `center`: white card centred (forms, login). `modal`: dims the previous screen and pops a dialog over it.
- A screen becomes visible 0.35 s before the first callout that targets it (`s=index`). Screens only move forward — to "come back" to a list page, add it again as a new screen.

## Components (`t=`) and the ids callouts can target
Helpers in the examples: `F(label,value,ph)` field, `SEL` select, `TA` textarea, `BTN(text,kind)`, `H(text,sub)`, `ROW(*comps)`, `N(text,tone)` note, `C(k,id,s)` callout.

| t | fields | target ids |
|---|---|---|
| h | text, sub | id |
| field / select / textarea | label, value (typed in on its callout), ph | id |
| btn | text, kind primary/ghost/blue/danger | id (press animation) |
| btns | items [[text,kind],...] | id.i |
| row | items [comps] (each child keeps its own id) | child ids |
| tabs | items, active | id.i |
| cards | items [[label,value]], n columns | id.i |
| list | items [title, sub, pillText, pillClass(''/y/b/r/g), buttonText] | id.i, id.i.b (row button) |
| ring | center, text, sub — callout `ring=pct` animates the arc | id |
| badges | items [[name, verified bool]] | id.i |
| choice | items [[title, sub]], active, n columns — becomes selected on its callout | id.i |
| code | value '482915' — digits drop in one by one | id |
| upload | label, sub | id |
| plans | items [name, price, [lines], buttonText], active | id.i, id.i.b |
| chat | items [['me'/'them', text]] | id.i |
| toggles | items [[label, on]] — callout `flip=True` switches it on the beat | id.i |
| note | text, tone ''/w/g/r | id |
| stepper | items, active | id |
| check | label — ticks on its callout | id |
| grid | count, n (thumbnail tiles) | id |
| swatch, cover | colour swatches / cover banner with logo | id, id.logo |
| table | cols, rows, w (CSS grid columns), low=[row,col] adds a green "Lowest" tag | id, id.r (row), id.r.c (cell) |
| pcards | product/service cards: items [dict(icon,c1,c2,cat,title,sup,ver,moq,price)], n, btns=[primary, secondary] | id.i, id.i.b0, id.i.b1 |
| pdp | product page: icon,c1,c2,sup,title,price,sub,qty,total,specs[] | id.im, id.price, id.qty, id.cart, id.rfq, id.contact, id.save |
| timeline | shipment / status stages: items [[label, icon]], done (pre-completed count) — each callout turns its stage green and draws the rail | id.i |
| sitebar | public-site header (logo + search typing + Search button) | id (typing), id.go |
| sidebar | — | `menu:<Item>` (click also moves the green active state) |
| header | — | `hdr:search`, `hdr:bell`, `hdr:add` |

## Callouts
`dict(k='<exact spoken substring>', id='<target>', s=<screen index>, ring=, flip=)`
- `k` is searched in the segment text **after the previous key's position** — keys must be in spoken order and unique enough (use 2–3 words). A missing key is reported by guide_plan.py; never ship with warnings.
- Each callout = cursor glide + click ripple + numbered red marker (top-left of target) + green highlight + camera push-in (1.07×) + field typing / selection / toggle.
- Several callouts on the same element: only the first controls typing; extra markers are hidden and the visible marker shows the latest number.
- Minimum spacing between beats is 0.45 s; beats snap to real pause ends (word onsets) within 0.6 s once the real MP3s are in `vo/`.
