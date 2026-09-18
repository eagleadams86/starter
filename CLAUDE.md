# CLAUDE.md — working on the starter itself

README.md speaks to someone COPYING this repo into a new app. This file is for
editing the starter in place. The difference matters: a mistake here doesn't
break one app, it ships silently inside every app that hasn't been started yet.

## What this repo is, and is not

- It is the template every new family web app begins from (see
  `family-starter` in memory). The app it implements — named numbers with
  dates — is **deliberately dull**: it exists to give the family's patterns
  something to hang on. Don't grow it a feature the family doesn't have, and
  don't make the sample data cleverer than the patterns need.
- It is **downstream for the shared chrome**. Sprint Predictability is the
  design lead for buttons, dialogs and the header row; Golf Handicap is the
  transcription reference this repo copies from. A change to shared chrome
  starts THERE and arrives here by transcription — never the other way, and
  never here alone. When this repo disagrees with the leads, fix it toward
  them.
- `theme.css` is a byte-copy of the pack's. Never edit it here; when the pack
  moves, copy the fresh file in. The pack's `check_consumers.py` is what
  notices this repo is behind.

## Editing rules

- **Nothing below the header is painted until the first `render()` has run — `data-booting` (2026-09-12).** Every panel inside `<main>` is built by `render()`, so `<main>` measures 0 at first paint. **This is the template every new app starts from, so the gate ships with it** and every future app inherits it. The browser paints the parsed body before the main script executes, so first paint was the header and then the **footer immediately under it**: the privacy line — "…sign in with Google…" — flashing at the top of the page on every refresh, before the app appeared and shoved it back down. Charles saw it in Money Map; a sweep of all eight pages on 2026-09-12 found **five** doing it (Money Map, Sprint Velocity, League Night, PAPTrack and the `claude-starter` template) and three clean (Golf Handicap, Flow Metrics, the NY calculator — clean because their cards are REAL MARKUP inside `<main>`). The fix is the arrangement the head script already uses for the theme: a thing settled a frame late is a page that visibly jumps as it opens.
  - **Set in the HEAD script, before anything that can throw.** The theme read below it touches `localStorage`, which a private-mode browser throws on — and that is the browser most likely to be slow enough to show the flash.
  - **Released in the SAME TASK as the first render.** A frame later and the reveal is itself the flash.
  - **`visibility: hidden`, NEVER `display: none`.** `render()` runs while the gate is on and a chart sizes itself off its container; a zero-width container is a zero-width chart that never corrects itself, because nothing re-measures once it has built. The boxes stay; only the painting is held. The suite asserts the measured width is unchanged while gated, which is what pins this.
  - **A `DOMContentLoaded` backstop removes it too**, so a script that dies on the way to the release can never leave the page blank.
  - The header is deliberately outside the gate: static markup, already correct at first paint.
  - **Don't count markup to decide whether a page has this** — League Night and PAPTrack were first written off as clean on a line count of what sits inside `<main>`, and both were wrong: their panels are `hidden` until the first render, so `<main>` measures 0. Measure the rendered box.
- **Every comment is a teaching comment.** The copier reads this file's
  comments as documentation of family rules, so a stale one doesn't just
  mislead a reader — it mis-teaches every future app. When code changes, the
  comments beside it move in the same commit (2026-08-31 caught four that
  hadn't: the five-tile grid, the "?" help sheet, the ResizeObserver's
  position, the 1px test frame).
- **README.md is part of the product.** It is the first thing a copier reads
  and it makes checkable claims (ports, key names, feature lists, the
  what-to-change-first list). Keep it in lockstep with the code, same commit.
- **The header's controls and the tab bar are ONE SCROLLING LINE AT EVERY WIDTH (2026-09-14, family-wide).** Charles: *"should we just make them both always single line side scrollers?"* Money Map is the reference (`claude-financial-plan` b14f4ae); this is its shape in the starter's own classes. `.headrow` holds `.headctl`, the scroller, and a `.rownav` of two arrows. **The row stays beside the name and scrolls there** (Charles, the same evening: *"keep buttons beside the name"* — the first cut, content-sized with `flex: 0 1 auto`, wrapped the whole row under the name the moment it didn't fit): `flex: 1 1 0%` takes what the name leaves, `justify-content: flex-end` packs the controls right, and `min-width: min(15rem, 100%)` wraps it under the name only when less than 15rem would be left (a phone; the starter's 360–480px windows). The row never overflows — the scroller inside shrinks — so flex-end cannot strand a control. Money Map 2c19e01 is the reference; the CSS and the `focusin` listener below are its, verbatim. `.tabrow` holds the tablist (the scroller) and ITS `.rownav no-print`, outside the tablist, and takes the tablist's old bottom margin; the welcome card and print hide `.tabrow`. `wireScrollRow(row, nav)` is Money Map's verbatim: arrows shown only while the row overflows (ResizeObserver + MutationObserver + scroll + resize — nothing calls it after boot), each disabled at its end, a press steps 80% of the row. **Arrows are for a mouse or trackpad only** (`@media (hover: none), (pointer: coarse)` hides them), `tabindex="-1"` + `aria-hidden`. `.rownav` must never set `display`, or `hidden` stops working. Print wraps `.headctl`. No drag edge-scroll here — the starter's tabs don't drag. Measured against the previous commit: 1600px, 1100px and a sideways phone are pixel-identical; at 705px and 480px the header went 93px → 88.5 (two lines of controls → one); an upright 390px phone went 147px → 92.5 (three lines → one that scrolls, 140px of it). **The starter's two tabs never overflow — the rule is here for the apps built from it.**
- **A keyboard focus lands whole inside a scrolling row (2026-09-14).** The browser scrolls a focus target into view only when it is ENTIRELY hidden, so Tab (or an arrow key along a tab bar) onto a control half past the edge left it clipped. `wireScrollRow()` carries a `focusin` listener, guarded by `:focus-visible` (a mouse press needs no help, and scrolling under it would move a tab about to be dragged), that scrolls the target fully inside the row's PADDING edges, so the 4px ring room stays the ring's. The test makes the straddle (scrolls a control's middle onto the edge) rather than hoping one exists, on the header and on a hand-narrowed tab bar. Measured against 2868e8c with sample data: 1600px, 1100px, 480px, 360px and both phone orientations unchanged (the name leaves room at the wide ones, and under 15rem at the narrow ones); at 705px the controls moved from a line of their own to beside the name, header 88.5px → 51, the row scrolling 90px. Real Tab and Shift+Tab walks at 360px clip nothing; before, Share was focused 48.5px past the edge.
- **A keyboard focus never lands under the pinned header (2026-09-14).** Charles: *"fix the sticky header shift+tab issue too"*. The browser's own scroll to a focused control lines it up with the top of the WINDOW, which is where the sticky bar sits, and a control wholly inside the bar's band counts as visible and is not scrolled at all. `html { scroll-padding-top: calc(var(--head-h, 0px) + 8px) }` moves the window's top edge below the bar; `--head-h` is the header's measured height, written by a ResizeObserver beside `wireScrollRow()` (Golf Handicap 8935363, verbatim), because the bar changes depth with the window, the zoom and the name wrapping. **The ≤560px block sets it back to 0**, since `header { position: static }` there pins nothing. **This repo has no 📌 pin mode**, so the header is the only thing to clear; an app built from here that pins more chrome under the bar takes Money Map's shape instead — one `--pin-clear` (header + stuck bars + 8px, header always observed) — and never ALSO a per-control `scroll-margin-top`, since the two add together (the suite pins its absence). Measured against d761b69 with the sample data: every control put half above the window, or wholly behind the bar, was focused still behind it — 16 of 16 at 1280×800, 844×390 and 705×800 each — and 0 now. The real Shift+Tab/Tab walk found none either side, because this app's controls are short and the walk never stops on a straddle; an app with taller rows would. The test places the control rather than hoping a walk finds one, in runAsync()'s 705px frame, and is red on d761b69 in both halves separately.
- **Every test body is AWAITED (since 2026-09-14).** `run()` is `async` and awaits whatever `item.fn()` returns, raced against a 20s `TEST_TIMEOUT_MS` so a test that never settles fails by name instead of hanging CI on "Loading…". Before that, `run()` called `item.fn()` and moved on: an `async` test was marked ✓ at its first `await` and its later failures went nowhere — the gate test `a loaded page never holds the gate…` was the one test in the suite written that way, and could never fail. An async test may now be written plainly. `runAsync()` + `asyncResults` is still the right home for a measurement several tests read (the row frames), because it is done once rather than per test — not because a test body would go unawaited.
- The suite pins `EXPECTED` (142 as of 2026-09-14) — bump it when adding a
  test; removing one fails the build on purpose. Tests refuse to run off
  localhost.
- **This repo's own dev port is 8022** (`.claude/launch.json`). The 8024 in
  the README's quickstart is for a NEW app cloned from here — don't "fix"
  either number to match the other.

## Deliberate decisions — don't undo

- **tests.html has no CI scorecard** (decided 2026-08-31). Every sibling's
  tests page names `api.github.com` in its CSP for the scorecard line; the
  starter instead models the strictest baseline — no external endpoint
  anywhere. An app that wants the scorecard copies it from a sibling AND adds
  the endpoint to its CSP knowingly. Don't add it here.
- The CSP comment on `form-action 'self'` describes future code, not present
  code (the dialogs here use plain buttons). It stays as guidance for apps
  built from the template.
- **The bars sit at the SOLID tint strength, and the hover is full strength**
  (2026-09-03). Pack rule 3: a bar is a tint fill plus a full-strength edge, and
  a *solid, untextured* series keeps ~55% of its colour where a textured one may
  go to 32%, because the texture puts full strength back over part of the bar and
  an outline alone cannot. These bars carry no texture. They sat at 32% anyway
  until a family-wide survey caught it: that bought `.bar.on` a place to stand —
  the highlight was the 55% the resting fill now uses — and cost the resting bars
  the contrast the rule exists to protect, most visibly on the white Light card.
  **The two levels are a pair. Raising one without the other silently deletes the
  highlight**, so both are pinned by tests, and so is the legend swatch, which
  carries the bar's own numbers because a key that does not depict its mark is
  worse than no key. The hover went to the colour itself — Money Map's Spending
  chart's answer to the same squeeze, not a new idea. The swatch stays a tint
  rather than going solid: the pack's carve-out is about swatches that must be
  told apart from EACH OTHER, and there are two here under edges that are most of
  a 22×10 box, where Money Map's five-account key needed the full-strength fill.
- **The full-screen chart has no step arrows, and that is deliberate** (decided
  2026-09-03). Flow Metrics grew a `‹ ›` pair beside the ⤢ that walks the charts
  on the screen the card came from; it was ported the same day to the Lottery
  Portfolio, Sprint Predictability and Money Map. **This template draws one
  chart, so there is nothing to walk** — everywhere else the arrows hide
  themselves below two charts, and here they would be hidden always. The
  template's `openMaxi`/`closeMaxi` are written around a single `#chartCard` (a
  `maxiUp` boolean, not a card reference), so an app built from this that grows
  a second chart takes BOTH the card-based shape and the walk from Flow Metrics:
  `maxiGroup()` + `dressStepBtns()` + `maxiStep()`, with the arrows in the
  OVERLAY — a button inside the card is detached mid-step and takes the
  keyboard's focus to `<body>` with it.
- Security baseline is the global one and non-negotiable: CSP on every page,
  no third-party scripts ever, escape at every render, sanitize at every
  entry, `SCHEMA` halt at all four entry points, service-worker fetches with
  `cache: 'no-cache'`.

## Fixes From the 2026-09-03 Audit

The family's Find window (⌘K) was audited across every repo that carries it and
the same faults were found here. Each fix has its own test in the
`find — one search across everything` group.

- **Enter opens the first hit (fix 1 — the family fix, and it landed the same
  day in Sprint Predictability 8637323, Money Map and Flow Metrics).** The only
  listener on `#searchBox` was the `input` one, so Enter — the one key a search
  box teaches — did nothing at all and a reader had to Tab out of the box and
  down the list. A `keydown` listener now opens `searchHits[0]` through
  `goToSearchHit()`: deliberately the SAME call a click on that hit makes, so
  the two paths cannot drift. A plain Enter only (a modifier means the reader is
  asking the browser for something else), and with nothing matching there is
  nothing to go to, so the window stays open. Nothing else about the box
  changed. **Both listeners are part of the pattern** — an app copied from here
  that takes only `input` ships a search box that ignores its own return key.
- **After a hit, the keyboard lands somewhere visible (fix 2 — the other half of
  the same family fix).** Closing a dialog hands the focus back to whatever held
  it before, so a ⌘K pressed from nowhere in particular dropped it on `<body>`.
  In THIS app every hit carries an `id`, so the fault only shows on the one path
  through `goToSearchHit()` that opens no editor: **a shared view**, where there
  is no editor to catch the focus. `goToSearchHit()` now ends by reading
  `document.activeElement` AFTER `render()` — `<body>`, null, or an element with
  no client rects (markup the render threw away) goes onto
  `.tab[data-tab=<the data-tab setTab just wrote>]` with `{ preventScroll: true }`.
  Read the landing off the attribute, not off `h.view`: `setTab()` clamps a name
  it does not know, so the attribute is the only answer that cannot be wrong.
  **The rule is "leave a visible focus alone", not "always focus the tab"** —
  that single sentence is what keeps the entry editor's `f_name` after a hit that
  opens it, and the Find button after a real press on it, with no special case
  for either. Copy the rule, not just the four lines.
- **Testing a shared view needs a SECOND frame** (`bootShared()` in tests.html).
  `viewOnly` is decided from the URL before anything renders and there is no hook
  that flips it, on purpose — a flag a test can set is a flag a bug can set — so
  the suite boots the real app at a real `#share=` link and polls for the
  snapshot banner, because `load` fires before `boot()` has awaited
  `decodeShare()`. An app copied from here that grows a view with no editor
  behind it takes this helper too.

## Two Open Copies: Checked Against the Family's Fix, and Already Right (2026-09-18)

Sprint Predictability, Flow Metrics and Money Map were each found writing a stale board over
another open tab's work (SV's 2026-09-18 review, ported the same day). **The starter never had the
fault, and nothing was ported into it**: its `storage` listener adopts another tab's write the
moment it lands — dialog open or not — and never saves from inside it, which is Golf Handicap's
shape. The siblings' second half (`save()` refusing to write over bytes it did not last read) is
deliberately absent: with a listener that always adopts, a stale copy does not arise, and a marker
every future writer must keep true is a cost with nothing behind it. **An app grown from this keeps
that protection only while the listener adopts unconditionally** — the day somebody adds "not while
a dialog is open" (Sprint Predictability's rule, for its save-as-you-go windows), the `save()` half
becomes necessary; take it from that app, or from Money Map if the new app syncs (it compares the
plan's MEANING, because sync rewrites the same data in different bytes).

One thing WAS wrong, found by reading the editor against that listener: Save re-finds its entry by
id (right), and when the other tab had DELETED it, wrote nothing and still toasted "Entry updated".
It now closes, redraws and says "That entry was deleted in another tab, so there was nothing to
update." Not re-created from the boxes — a delete made on purpose is not undone by a stale window's
Save. The test stubs `save()` for the press; this suite never writes the reader's storage.
EXPECTED 142 → 143.
