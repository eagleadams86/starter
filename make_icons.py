#!/usr/bin/env python3
"""Draw the app's mark: favicon.ico plus the three PNGs the manifest names.

    python3 make_icons.py

THE MARK EXISTS TWICE and the two must stay one picture: this script, and the
inline SVG data URI in index.html's <head>. The SVG is what every current browser
shows in the tab and it needs no sibling file, so it survives file://; the .ico is
the fallback a browser fetches from the site root on its own, and what a bookmark
and the header <img> use. Change the geometry here and change it there.

RE-RUNNING THIS MEANS BUMPING ?v= ON EVERY favicon.ico REFERENCE — index.html's
<link>, the header <img>, and privacy.html's — or the old icon stays cached for
months.

THREE ICONS, THREE JOBS, and the differences are not decoration:

  * icon-192 / icon-512 (`purpose: any`) and favicon.ico are ROUNDED, because
    nothing masks them.
  * icon-512-maskable is FULL BLEED with SQUARE corners, because a launcher crops
    it to its own shape — rounding a picture that is about to be rounded again
    leaves a pale seam inside the curve.
  * The maskable SAFE ZONE is a disc of radius 25.6 in the 64 viewport. This
    mark's furthest point is the end of the longest bar at x=47, which is 15 from
    the centre — comfortably inside. WIDEN THE BARS AND RE-CHECK THAT SUM.

Everything is drawn at 8x and reduced with Lanczos, which is what gives the 16px
version clean edges.

The two extra tints are ARTWORK, NOT PALETTE. They are copied byte-for-byte from
the family's other marks rather than re-picked, so nothing new ever enters the
theme pack — the pack gates colours that carry meaning, and an icon does not.
"""

from PIL import Image, ImageDraw

# The mark, in the SVG's own 64x64 coordinates. Keep in step with index.html.
BG = (10, 14, 26, 255)        # #0a0e1a — midnight, the default theme's page
GLOW = (20, 28, 51, 255)      # #141c33 — the soft disc in the corner
GRAD_FROM = (129, 140, 248)   # #818cf8 — midnight's accent
GRAD_TO = (165, 180, 252)     # #a5b4fc
GRAD_AXIS = ((10, 52), (54, 12))   # where the gradient runs, corner to corner

BARS = [(13, 17, 34, 6), (13, 29, 24, 6), (13, 41, 30, 6)]   # x, y, w, h
DISC = (50, 14, 18)                                          # cx, cy, r
CORNER = 14                                                  # rounded-square radius

SCALE = 8
S = 64 * SCALE


def _lerp(a, b, t):
    return tuple(round(a[i] + (b[i] - a[i]) * t) for i in range(3))


def _gradient_at(x, y):
    """The colour of the accent gradient at a point, in 64-space."""
    (x0, y0), (x1, y1) = GRAD_AXIS
    dx, dy = x1 - x0, y1 - y0
    t = ((x - x0) * dx + (y - y0) * dy) / (dx * dx + dy * dy)
    return _lerp(GRAD_FROM, GRAD_TO, min(1.0, max(0.0, t)))


def draw(rounded):
    """The whole mark at 8x. `rounded` is False for the maskable variant."""
    img = Image.new('RGBA', (S, S), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    if rounded:
        d.rounded_rectangle([0, 0, S - 1, S - 1], radius=CORNER * SCALE, fill=BG)
    else:
        d.rectangle([0, 0, S - 1, S - 1], fill=BG)

    cx, cy, r = DISC
    d.ellipse([(cx - r) * SCALE, (cy - r) * SCALE, (cx + r) * SCALE, (cy + r) * SCALE],
              fill=GLOW)

    # Each bar is filled column by column so it picks up the gradient, the same
    # way the SVG's linearGradient does.
    for (bx, by, bw, bh) in BARS:
        radius = (bh / 2) * SCALE
        for px in range(bx * SCALE, (bx + bw) * SCALE):
            colour = _gradient_at(px / SCALE, by + bh / 2) + (255,)
            d.rectangle([px, by * SCALE, px, (by + bh) * SCALE - 1], fill=colour)
        # Round the ends, in the bar's own colour at each end.
        for end_x, t in ((bx * SCALE + radius, bx), ((bx + bw) * SCALE - radius, bx + bw)):
            colour = _gradient_at(t, by + bh / 2) + (255,)
            d.ellipse([end_x - radius, by * SCALE, end_x + radius, (by + bh) * SCALE - 1],
                      fill=colour)
    return img


def save(img, path, size):
    img.resize((size, size), Image.LANCZOS).save(path)
    print('wrote', path, size)


if __name__ == '__main__':
    rounded = draw(rounded=True)
    square = draw(rounded=False)

    # favicon.ico carries several sizes; a browser picks the one it wants.
    rounded.resize((64, 64), Image.LANCZOS).save(
        'favicon.ico', sizes=[(16, 16), (32, 32), (48, 48), (64, 64)])
    print('wrote favicon.ico')

    save(rounded, 'icon-192.png', 192)
    save(rounded, 'icon-512.png', 512)
    save(square, 'icon-512-maskable.png', 512)
