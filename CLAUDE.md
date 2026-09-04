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

- **Every comment is a teaching comment.** The copier reads this file's
  comments as documentation of family rules, so a stale one doesn't just
  mislead a reader — it mis-teaches every future app. When code changes, the
  comments beside it move in the same commit (2026-08-31 caught four that
  hadn't: the five-tile grid, the "?" help sheet, the ResizeObserver's
  position, the 1px test frame).
- **README.md is part of the product.** It is the first thing a copier reads
  and it makes checkable claims (ports, key names, feature lists, the
  what-to-change-first list). Keep it in lockstep with the code, same commit.
- The suite pins `EXPECTED` (127 as of 2026-08-31) — bump it when adding a
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
