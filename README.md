# yeaminmahid.github.io — portfolio

Static portfolio site. No framework, no build step, no external requests at runtime —
every icon is inline SVG and all styling lives in one stylesheet.

```
index.html        the page
css/style.css     palette, layout, animations, light/dark theme variables
js/main.js        typing loop, neural-network canvas, scroll reveals, count-ups, tilt, theme toggle
build.py          generator that re-emits index.html (optional)
icons.json        Simple Icons path data used by build.py
tests/dom.test.js boots the real page in a DOM and asserts it initialises
```

## Sections

Hero → About → **Research** (featured publication, competitive-programming stats,
competition write-ups) → Skills → Projects → Journey → Contact. The tech stack is listed
once, in Skills — there's no separate scrolling logo strip duplicating it.

## Light / dark theme

There's a toggle button in the nav (sun/moon icon). It:

- Defaults to dark, unless the visitor's OS is set to light mode (`prefers-color-scheme`).
- Remembers the choice in `localStorage`, so it persists across visits.
- Applies before first paint via a small inline script in `<head>`, so there's no flash of
  the wrong theme on load.
- Reuses the same CSS variables as the rest of the site (`css/style.css`, under
  `[data-theme="light"]`) — no component styles are duplicated.

## Run it locally

```bash
python3 -m http.server 8000
# http://localhost:8000
```

## Deploy to GitHub Pages

**Option A — Actions (recommended, already configured)**

1. Create the repo `mahidrahman375.github.io` (or any name) and push these files.
2. Repo **Settings → Pages → Build and deployment → Source: GitHub Actions**.
3. Push to `main`. `.github/workflows/deploy.yml` stages `index.html`, `css/` and `js/`
   and publishes them. It skips `node_modules`, `build.py` and the tests.
4. Your site lands at `https://mahidrahman375.github.io/`.

Using a project repo instead of `<username>.github.io`? Then it publishes at
`https://mahidrahman375.github.io/<repo>/` — no path changes needed, every asset here is
relative.

**Option B — branch deployment**

Settings → Pages → Source: *Deploy from a branch* → `main` / `/ (root)`.

## Edit content

Text, projects, skills and the timeline are all in `build.py` — edit the blocks at the top
and run `python3 build.py`. Or edit `index.html` directly; nothing is generated at runtime.

## Verify

```bash
npm i --no-save jsdom
node tests/dom.test.js            # full animation path
node tests/dom.test.js --reduced  # prefers-reduced-motion path
```

The test loads the actual `index.html` and `js/main.js` into a DOM and asserts: 8 cards
(6 project repos + 2 competitions), 4 skill cards, 8 timeline entries, 40 scroll reveals
fired, 16 skill bars filled, counters landing on `13 | 6 | 100+ | 3`, the featured paper
and its 4 metrics, 3 competitive-programming facts, every in-page anchor resolving, no
runtime console errors, the theme toggle switching `data-theme` and persisting the choice
to `localStorage` on click, and — in reduced-motion mode — the canvas never initialising
and the typing loop replaced by a static line.

## Accessibility & motion

All animation is disabled under `prefers-reduced-motion: reduce`: no aurora drift, no caret
blink, no count-up, no canvas. Decorative SVGs are `aria-hidden`, the menu button is
labelled, and there is exactly one `h1`.
