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
- Security baseline is the global one and non-negotiable: CSP on every page,
  no third-party scripts ever, escape at every render, sanitize at every
  entry, `SCHEMA` halt at all four entry points, service-worker fetches with
  `cache: 'no-cache'`.
