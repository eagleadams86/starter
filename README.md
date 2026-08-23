# The family starter

A complete, running single-file web app that already has every shared feature the other apps
in this family took two years to grow. Copy it, replace the middle, keep the edges.

**Live: https://eagleadams86.github.io/starter/**

```bash
git clone --depth 1 https://github.com/eagleadams86/starter ~/claude-newapp
cd ~/claude-newapp && rm -rf .git && git init
python3 -m http.server 8020
```

Then open `http://localhost:8020/` for the app and `/tests.html` for the suite.

**What to change first**, in roughly this order:

1. The three `starter-` localStorage keys — `starter-state`, `starter-theme`, `starter-tab`.
   Two apps sharing a key on one origin overwrite each other.
2. The `starter-shell-` cache prefix in `sw.js` and `sw-kill.js`, for the same reason.
3. The GitHub URLs in `index.html` and `privacy.html`, and the app name in `<title>`, the
   brand line, `manifest.webmanifest` and `NOTICE`.
4. The mark: edit the geometry in `make_icons.py`, re-run it, and copy the same shapes into
   the inline SVG in `<head>` so the two stay one picture.
5. Its own `CLAUDE.md`, recording the decisions this app makes that the family doesn't.

`theme.css` here is a real copy of the pack's, byte-for-byte, not a link. When the palette
moves, `check_consumers.py` in the pack is what notices this repo is behind.

## Why this exists

Until now, "starts from the theme pack" meant *copy `theme.css` and remember everything else*
— and everything else is what the existing apps got wrong. On 2026-08-23 all nine repos were
byte-identical to the pack and **eleven public pages were still running their own type on top
of it**, because a hash proves the file arrived and nothing proved the page read it.

So this is not a template of pretty markup. **Golf Handicap is the reference for the shared
chrome; Golf in turn transcribes Sprint Predictability, which is the design lead for buttons,
dialogs and the header row.** Where a rule is argued at length in one of those repos, the
comment beside it here says so. The app it implements — a list of named numbers with dates —
is deliberately dull: it exists to give the patterns something to hang on.

**A change to the shared chrome belongs in Sprint Predictability too, or the family drifts.**

## What you are inheriting

**The look.** `theme.css` linked, never inlined. Not one literal colour, not one raw pixel
font size. Every size picked by ROLE from the pack's contract, so this page and the other
seven read as one application: page title `xl`, card and dialog headings `md`, body and
buttons `base`, table rows `sm`, chrome and footers `xs`. Buttons, dialogs, tabs, tiles,
pills, fields and the toast are transcribed from Golf Handicap rather than re-invented.

**The features every sibling has:**

| | |
|---|---|
| **Welcome card** | The three choices Money Map opens on, decided before first paint so nothing flashes |
| **Two tabs** | `data-tab` on `<html>` set in `<head>`; CSS switches, a real tablist with arrow keys, both panels print |
| **Summary tiles** | Five, on `subgrid` so labels line up across a row; the spans assume five |
| **A chart** | SVG, so it follows a theme change *and* the print palette for free. Tint fill + full-strength edge (pack rule 3), `--series-*` only (rule 4). Drawn at the box's own pixel size and redrawn when it changes, so nothing is ever scaled |
| **A chart card** | The siblings' anatomy: name, an `i` that opens the help sheet, a sentence saying what is plotted, a 300px box, and a button that lifts the chart out to fill the window (Escape, the button again, or a click outside) |
| **Find** | TWO, as Golf Handicap has: ⌕ in the header (⌘K) searches everything and jumps to the record; the box in the table narrows what you're looking at |
| **Sortable columns** | Flow Metrics' three-state cycle — the column's own direction, reversed, then back to the table's own order |
| **Copy / ⬇ CSV** | On the table, reading the RENDERED DOM so the export is what you're looking at; formula cells defused, thousands quoted |
| **Settings** | A dialog of real settings that survive Start Again |
| **Share** | `#share=` links, deflate-raw + base64url, a trimmed pure-function payload, and a read-only view that strips every edit surface |
| **Back up** | The family's window, identical in all six apps — 700px on 18px padding, JSON, CSV with formula cells defused, and Start Again folded in behind a disclosure |
| **Delete all data** | The family's confirmation, identical in all six apps: 560px on 18px padding, the count of what is going, and **Download Backup First** at the far left — the one route back, which a `confirm()` cannot hold a button for |
| **Install** | `manifest.webmanifest`, three PNG icons from `make_icons.py`, `manifest-src 'self'` |
| **Offline** | `sw.js` network-first over a pinned public-files-only shell, plus `sw-kill.js` |

**The guards on saved data**, which are the part that is easy to skip and expensive to add
later:

| | |
|---|---|
| `SCHEMA` + `haltForNewerData()` | refuses data written by a newer build at **four** entry points instead of silently rebuilding it — and **throws**, so a half-booted app can't save over the good copy |
| `normalizeState()` | an allowlist that rebuilds rather than merges, with every field type-checked because all of it can arrive from a share link |
| `ID_RE` | ids are a key prefix and reach `data-id` attributes, so anything not `[A-Za-z0-9_-]{1,64}` is replaced and every reference rewritten |
| `esc()` | everything rendered, every time |
| `viewOnly` | one flag, checked in `save()` — the single write path |
| the `storage` listener | adopts another tab's write, and never saves from inside it |

**A test suite with a floor.** 99 tests pinning all of the above, and an `EXPECTED` constant
so a test that goes *missing* fails the build — a suite that quietly shrank to three checks
still reports "all 3 tests pass".

## Things the comments will tell you that are worth knowing now

- **The toast needs `right: auto; top: auto`.** It is a `popover`, which is the only way it
  can be seen over a modal `<dialog>` (a dialog is in the browser's TOP LAYER, above every
  z-index). But the UA gives a popover `inset: 0; margin: auto`, which beats a bare
  `left`/`bottom` and parks it in the top-left corner of the screen.
- **The footer's colour and size go on `<footer>`**, not on each paragraph — `margin: 34px 0 0`
  per paragraph puts 34px above all three and the block falls apart.
- **A header `<select>` needs `width: auto`.** The base field rule gives every select
  `width: 100%`, which in a wrapping flex row makes the theme picker claim the whole line.
- **`[hidden]` needs `!important`.** The browser's own rule is in the user-agent stylesheet
  and *any* author rule beats it, so a class that sets `display` cancels it. Nothing throws.
  This has cost Golf Handicap twice.
- **A control's border is `--border-control`**, never `--border`. WCAG 1.4.11 asks 3:1 of what
  identifies a component, and for these buttons that is the border. Never fix a weak control
  edge locally — that is the drift the pack exists to prevent.
- **A per-row delete is an `.icon-btn` square, neutral until hovered.** A column of red
  squares reads as a column of warnings. Written `button.icon-btn.danger` so it beats a plain
  `.danger` further up the cascade.
- **A delete confirmation NAMES the record.** A bare "Are you sure?" is a dialog people learn
  to click through.
- **A scroll box needs `position: relative`**, or iOS counts its full width in the document's
  scroll area and the page scrolls sideways into a band of nothing.
- **The sample data is the demo.** A feature isn't finished until it appears there, and rows
  are named for what they show. `Item 1 / Item 2` teaches nothing.
- **Headings are Title Case**; body copy, buttons, table column headers and field labels are
  not. An icon never sits flush against the word it follows.
- **There are TWO page widths in this family and a new app picks one.** 1500px is the default
  and what this starts on; 2400px is the ultra-wide, for a page whose content genuinely fills
  it. Don't invent a third — this file carried 1100 for a day, which made the shell the one
  page in the family at a width nothing else uses, and every app copied from it would have
  inherited that. `--page-w` is read by both `.wrap` and `.headbar`, and they have to be the
  same number or the brand stops lining up with the left edge of the first card.
- **A sortable heading is a BUTTON, not a `th` with a click handler.** It has to be reachable
  from a keyboard and announce itself as pressable, and `aria-sort` on the `th` is what tells
  a screen reader which way the column runs. Three states, not two: a two-state toggle gives
  a reader no way back to the order the table shipped in.
- **The export reads the rendered table, never `state`.** What's on screen is already the
  product of choices the reader made, and a second path built from state would drift from it
  the first time a filter changed. The Back Up window's CSV is a *different* thing — every
  entry, because a backup is not a view — and both are wanted.
- **Decoration is not data.** `cellText()` strips anything `aria-hidden`, which is what keeps
  a row-action glyph out of the export. Without it every exported row ended in a cell
  containing `×`.
- **Find needs two characters.** One matches most of the data, and that list is worse than no
  list; the placeholder and the empty message both say so. The cap reports what it dropped
  rather than truncating silently.
- **The Find window's CSS block is the family's, verbatim.** 700px on 18px of padding, and
  every property of what it shows — the heading, the intro line, the box, the hit and its
  three lines, the "Nothing matches" line — declared inside that block rather than borrowed
  from `.hint` or `dialog p`. Six apps carry it byte for byte (2026-08-23); copy it as it is,
  and if you change it, change it in all six. It deliberately declares no dialog chrome:
  backdrop, shadow and max-height belong to the base `dialog` rule and are shared with every
  other window.
- **If you swap the SVG chart for a CANVAS**, the print CSS stops being enough — a canvas is
  painted once from `getComputedStyle` and print-media values are invisible to it. Swap
  `data-theme` on `beforeprint`, re-render, put it back on `afterprint`, save nothing. See
  `printForPaper()` in Sprint Predictability or the lottery portfolio.

## What is deliberately NOT here

**Cross-device sync.** Two apps had it and it was removed from both in August 2026; the two
that keep it (PAPTrack, Golf Handicap) carry hard-won rules a fresh implementation would not
think of — the Google Identity Services workaround for corporate filters that block
`firebaseapp.com` per hostname, the never-guess-by-timestamp reconciliation, and the
empty-copy-never-wins rule. If you need it, port it from Golf Handicap and read that repo's
CLAUDE.md first.

**A Jira importer, a chart library, multi-record management screens.** All real in at least
one sibling, none needed to start.

## Keeping it honest

This repo is a CONSUMER of `~/claude-theme-pack` like any other app, and is registered in its
`WEB_CONSUMERS` list. That script asks two questions of every repo: is your `theme.css`
byte-identical to the pack's, and do your pages actually USE it — raw pixel type, a local font
stack, an `<html>` tag not opening on Auto. A starter that has quietly stopped following the
pack is worse than no starter, because every app copied from it inherits the drift on day one.

```bash
python3 check_consumers.py      # from the pack root
```

**And when you ship the new app, add IT to `WEB_CONSUMERS` too**, as well as to the Consumers
table in the pack's `CLAUDE.md`. A copy nobody is looking at is the whole failure mode that
script exists to prevent — on 2026-08-22 two apps were found weeks behind on the palette with
every gate green, because nothing was looking at them.
