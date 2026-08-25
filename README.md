# Order Process Walkthrough — deck

Client-facing 3D deck for the custom van signage engagement. 14 slides: the process as
it runs today, the ten changes, the flow it becomes, the plate-lookup addition, and the
order of work.

**PRIVATE, and it should stay that way.** The deck names the client, quotes his
per-design cost, and says he personally verifies every order. GitHub Pages on the free
plan requires a public repo, so Pages is deliberately **not** enabled — publishing this
would put a client's internal process and margins on an indexable URL.

---

## To show it

`order-process-deck.html` (and the identical `index.html`) is **one self-contained
file** — fonts and every tool logo are embedded as data URIs.

- Download it and **double-click**. No server, no build step, no internet needed.
- Press **`F`** for fullscreen before presenting.

> GitHub will not render it in the browser. It serves repo HTML as source, by design.
> Use the **Download raw file** button, or:
> ```bash
> gh api repos/consult-with-riz/deck-for-tom/contents/order-process-deck.html \
>   -H "Accept: application/vnd.github.raw" > deck.html
> ```
> Run that in Git Bash, not PowerShell — PowerShell's `>` writes UTF-16 and corrupts it.

| Key | Action |
|---|---|
| `→` / `Space` / click | Next slide |
| `←` | Previous slide |
| `F` | Fullscreen |
| `Home` / `End` | First / last slide |

Dots on the right jump to any slide. Swipe works on touch. Respects
`prefers-reduced-motion`.

---

## To change it

**Never hand-edit `order-process-deck.html` or `index.html`.** They are generated, and
the assets inside them are base64. Your edit would be overwritten by the next build.

Everything lives in `src/`:

| File | What it holds |
|---|---|
| `src/build_deck.py` | **All slide copy and structure.** Edit this for wording, slides, tools. |
| `src/deck_template.html` | The CSS, the 3D stage, and the keyboard/touch navigation. |
| `src/logos/*.svg` | Tool marks from simple-icons. |
| `src/fonts/*.woff2` | Poppins 600/700 and Instrument Sans, latin subsets. |

Then rebuild:

```bash
python src/build_deck.py
```

Needs Python 3, no packages. It rewrites `order-process-deck.html` and `index.html` at
the repo root. Pass a path to write somewhere else: `python src/build_deck.py out.html`.

### Where things are in `build_deck.py`

- **Tool chips** — the `T_*` constants near the top. `REAL` lists slugs with a real
  simple-icons mark; `CHIPS` covers tools with no mark and gets a typographic chip
  instead. Never fabricate a company's logo.
- **`WORDMARKS`** — for simple-icons entries that are wordmarks rather than glyphs
  (Typeform). The offsets are the path's real `getBBox()`, measured in a browser.
  Do not eyeball them; guessing clipped the ascenders last time.
- **Slides** — each `slide("<theme>", """...""")` call, in order. The theme string
  becomes the `<section>` class list.
- **Attribution** — the `.wordmark` on the cover and close slides, and the `<span>` in
  the `.sfoot` footer at the bottom of the assemble block.

### Two traps worth knowing

1. **Theme class names collide with CSS class names.** The slide's classes go straight
   onto the `<section>`. A rule like `.finding{...}` intended for an inner div will also
   match a slide themed `"black finding"`. Scope inner-element rules as
   `.inner > .thing`. This exact bug collapsed a slide into the left third of the screen.
2. **`.slide` needs a definite grid column.** It uses
   `grid-template-columns:minmax(0,1fr)`. Do not replace that with `place-items:center` —
   a centred grid item stops stretching, and `.inner`'s `width:min(1180px,100%)` then
   resolves its percentage against an auto column, which is cyclic and collapses to
   content width.

### Check your work

Serve it and look at it — `file:` is blocked in most automation:

```bash
python -m http.server 8000
```

Then confirm every slide is full width and nothing runs under the footer:

```js
[...document.querySelectorAll('.slide')].map((s,i) => ({
  n: i+1,
  width: s.querySelector('.inner').offsetWidth,        // want 1180
  room:  s.clientHeight - s.querySelector('.inner').scrollHeight  // want > 0
}))
```

---

## Palette

Coral `#ED5C45`, cream `#F4F3ED`, black `#0E0E0E`, white `#FFFFFF`. Poppins display,
Instrument Sans body. Approved pairings only, never white-on-cream. Coral is an accent —
never a large background. The 3D lives on the stage and the cards, never on type.

## Tool logos

Real marks, recoloured to coral: Shopify, Typeform, ClickUp, Claude, n8n, Google Drive,
Gmail.

Typographic chips, **not** logos — these have no simple-icons entry, and a fabricated
mark would be worse than none: Klaviyo, ShipStation, Vehicle Outlines
(vehicleoutlines.co.uk), and the vehicle-data provider.
