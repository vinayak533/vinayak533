#!/usr/bin/env python3
"""Stippled, animated butterfly for the profile hero. Standard library only.

    python scripts/generate_butterfly.py      # writes assets/butterfly.svg

Every shape is built from round dots, like halftone print: dense and bright at
the body and wing bases, sparser, smaller and dimmer toward the wing edges,
with violet on the outer margins. Points are blue-noise sampled (dart throwing
with a density-dependent minimum distance) from a fixed seed, so rebuilds are
byte-stable. Motion is CSS inside the SVG: wings flap as scaleX about the body
axis, the whole butterfly floats, dots twinkle, and violet particles shed on
each wingbeat drift away behind the wings and fade.
All of it stops under prefers-reduced-motion and the first frame is complete.

tools/profile/build.py imports `butterfly()` to draw the same art inside the
hero banner, because GitHub renders README SVGs as images, which cannot load
other files.
"""
import math
import random
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VB_W, VB_H = 520, 420
SEED = 533
BG = "#000000"
FLAP, FLOAT = 2.4, 13  # seconds: one wingbeat, one float loop
INK = {"white": "#FFFFFF", "soft": "#DCD7EA", "violet": "#A78BFA", "deep": "#7C3AED"}

# Left-wing outlines (body axis at x = 0, y grows downward) as closed Catmull-Rom control points.
FORE = [(-4, -34), (-30, -92), (-74, -146), (-128, -178), (-182, -193), (-218, -191), (-238, -176),
        (-232, -150), (-208, -118), (-186, -86), (-166, -56), (-138, -28), (-90, -10), (-44, -4), (-14, -14)]
HIND = [(-6, -6), (-46, -2), (-104, 8), (-156, 28), (-188, 60), (-198, 100), (-186, 140), (-160, 166),
        (-132, 180), (-114, 200), (-98, 212), (-88, 198), (-78, 170), (-60, 138), (-40, 96), (-22, 52), (-9, 18)]


def catmull(pts, steps=14):
    out, n = [], len(pts)
    for i in range(n):
        p0, p1, p2, p3 = pts[i - 1], pts[i], pts[(i + 1) % n], pts[(i + 2) % n]
        for s in range(steps):
            u = s / steps
            u2, u3 = u * u, u * u * u
            out.append(tuple(.5 * (2 * b + (c - a) * u + (2 * a - 5 * b + 4 * c - d) * u2 + (3 * b - a - 3 * c + d) * u3)
                             for a, b, c, d in zip(p0, p1, p2, p3)))
    return out


def seg_dist(px, py, ax, ay, bx, by):
    dx, dy = bx - ax, by - ay
    u = max(0, min(1, ((px - ax) * dx + (py - ay) * dy) / (dx * dx + dy * dy or 1)))
    return math.hypot(px - ax - u * dx, py - ay - u * dy)


class Wing:
    """One wing: smooth outline, raster inside-mask, polar extent from the root, and curved veins."""
    CELL = 2.0

    def __init__(self, ctrl, rng, mirror=False, scale=1.0, rot=0.0, jitter=5.0, veins=7):
        rx, ry = ctrl[0]
        c, s = math.cos(math.radians(rot)), math.sin(math.radians(rot))
        pts = []
        for i, (x, y) in enumerate(ctrl):
            if i:
                x, y = x + rng.uniform(-jitter, jitter), y + rng.uniform(-jitter, jitter)
            x, y = rx + (x - rx) * scale, ry + (y - ry) * scale
            x, y = rx + (x - rx) * c - (y - ry) * s, ry + (x - rx) * s + (y - ry) * c
            pts.append((-x if mirror else x, y))
        self.root, self.mirror = pts[0], mirror
        self.outline = catmull(pts)
        xs, ys = [p[0] for p in self.outline], [p[1] for p in self.outline]
        self.box = (min(xs), min(ys), max(xs), max(ys))
        self._mask()
        self._polar()
        self._veins(veins, mirror)

    def _mask(self):
        x0, y0, x1, y1 = self.box
        self.mask = set()
        edges = list(zip(self.outline, self.outline[1:] + self.outline[:1]))
        j = 0
        while y0 + j * self.CELL <= y1:
            y = y0 + (j + .5) * self.CELL
            xs = sorted(ax + (y - ay) * (bx - ax) / (by - ay) for (ax, ay), (bx, by) in edges if (ay <= y) != (by <= y))
            for a, b in zip(xs[::2], xs[1::2]):
                for i in range(int((a - x0) / self.CELL), int((b - x0) / self.CELL) + 1):
                    self.mask.add((i, j))
            j += 1

    def inside(self, x, y):
        return (int((x - self.box[0]) / self.CELL), int((y - self.box[1]) / self.CELL)) in self.mask

    def _polar(self, n=720):
        """Farthest outline crossing along each ray from the root: t = |p - root| / R(angle)."""
        rx, ry = self.root
        self.n, self.R = n, [1.0] * n
        edges = list(zip(self.outline, self.outline[1:] + self.outline[:1]))
        for k in range(n):
            th = -math.pi + 2 * math.pi * k / n
            dx, dy = math.cos(th), math.sin(th)
            best = 1.0
            for (ax, ay), (bx, by) in edges:
                ex, ey = bx - ax, by - ay
                den = dx * ey - dy * ex
                if abs(den) < 1e-9:
                    continue
                t = ((ax - rx) * ey - (ay - ry) * ex) / den
                u = ((ax - rx) * dy - (ay - ry) * dx) / den
                if t > 0 and 0 <= u <= 1:
                    best = max(best, t)
            self.R[k] = best

    def t(self, x, y):
        dx, dy = x - self.root[0], y - self.root[1]
        k = int((math.atan2(dy, dx) + math.pi) / (2 * math.pi) * self.n) % self.n
        return min(1.0, math.hypot(dx, dy) / self.R[k])

    def _veins(self, count, mirror):
        """Curved lines from the root to evenly spaced points on the outer margin (stippled ribs)."""
        rx, ry = self.root
        far = sorted(range(len(self.outline)), key=lambda i: -math.hypot(self.outline[i][0] - rx, self.outline[i][1] - ry))
        reach = math.hypot(self.outline[far[0]][0] - rx, self.outline[far[0]][1] - ry)
        outer = [i for i in range(len(self.outline))
                 if math.hypot(self.outline[i][0] - rx, self.outline[i][1] - ry) > reach * .55]
        self.vein_lines = []
        for v in range(count):
            qx, qy = self.outline[outer[int((v + .5) * len(outer) / count)]]
            mx, my = (rx + qx) / 2, (ry + qy) / 2
            ln = math.hypot(qx - rx, qy - ry)
            bend = (.10 if not mirror else -.10) * ln
            cx, cy = mx - (qy - ry) / ln * bend, my + (qx - rx) / ln * bend
            line = []
            for s in range(13):
                u = s / 12 * .94
                line.append(((1 - u) ** 2 * rx + 2 * (1 - u) * u * cx + u * u * qx,
                             (1 - u) ** 2 * ry + 2 * (1 - u) * u * cy + u * u * qy))
            self.vein_lines.append(line)

    def vein(self, x, y):
        d = min(seg_dist(x, y, *a, *b) for line in self.vein_lines for a, b in zip(line, line[1:]))
        return math.exp(-(d / 4.2) ** 2)

    def density(self, x, y):
        t = self.t(x, y)
        base = math.exp(-math.hypot(x, y - self.root[1]) / 62)
        rim = math.exp(-((1 - t) / .045) ** 2)
        d = .06 + .5 * (1 - t) ** 1.6 + .38 * base + .3 * self.vein(x, y) * (1 - .55 * t) + .2 * rim
        return max(0.0, min(1.0, d)), t, rim


class Stipple:
    """Dart throwing on a shared grid: each pass accepts with probability ~ density and rejects
    anything closer than its own r(density), so earlier passes (rim, fibres) keep their structure."""

    def __init__(self, rng, inside, density, cell=2.4):
        self.rng, self.inside, self.density, self.cell = rng, inside, density, cell
        self.grid, self.pts = {}, []

    def add(self, candidates, rmin, rmax, gate=0.15, tag=0):
        cell = self.cell
        for x, y in candidates:
            if not self.inside(x, y):
                continue
            d, *extra = self.density(x, y)
            if self.rng.random() > gate + (1 - gate) * d:
                continue
            r = rmax - (rmax - rmin) * d ** .8
            gi, gj = int(x // cell), int(y // cell)
            reach = int(math.ceil(r / cell))
            if any(math.hypot(x - px, y - py) < r
                   for i in range(gi - reach, gi + reach + 1) for j in range(gj - reach, gj + reach + 1)
                   for px, py in self.grid.get((i, j), ())):
                continue
            self.grid.setdefault((gi, gj), []).append((x, y))
            self.pts.append((x, y, tag, d, *extra))
        return self


def uniform(rng, box, n):
    x0, y0, x1, y1 = box
    return ((rng.uniform(x0, x1), rng.uniform(y0, y1)) for _ in range(n))


def streamlines(rng, wing, count, bend=.16):
    """Fibres from the wing root out to the margin, dotted ever more sparsely, like the rows in a stipple print."""
    rx, ry = wing.root
    reach = max(wing.R)
    outer = [p for p in wing.outline if math.hypot(p[0] - rx, p[1] - ry) > reach * .42]
    sign = 1 if wing.mirror else -1
    for k in range(count):
        qx, qy = outer[int((k + rng.random()) * len(outer) / count) % len(outer)]
        ln = math.hypot(qx - rx, qy - ry)
        b = sign * bend * ln * rng.uniform(.6, 1.3)
        cx, cy = (rx + qx) / 2 - (qy - ry) / ln * b, (ry + qy) / 2 + (qx - rx) / ln * b
        u = rng.uniform(.0, .04)
        while u < 1:
            x = (1 - u) ** 2 * rx + 2 * (1 - u) * u * cx + u * u * qx
            y = (1 - u) ** 2 * ry + 2 * (1 - u) * u * cy + u * u * qy
            yield x + rng.gauss(0, .45), y + rng.gauss(0, .45)
            u += (2.5 + 6.5 * u ** 1.5) / ln


def rim(rng, wing, step=3.4):
    """Points along the margin, slightly inset, so the flowing edge reads without an outline."""
    out, acc = [], 0.0
    pts = wing.outline
    cx, cy = sum(p[0] for p in pts) / len(pts), sum(p[1] for p in pts) / len(pts)
    reach = max(wing.R)
    for (ax, ay), (bx, by) in zip(pts, pts[1:] + pts[:1]):
        seg = math.hypot(bx - ax, by - ay)
        while acc < seg:
            u = acc / seg
            x, y = ax + (bx - ax) * u, ay + (by - ay) * u
            inset = rng.uniform(1.2, 3.5)
            dx, dy = cx - x, cy - y
            dl = math.hypot(dx, dy) or 1
            if rng.random() < .15 + .85 * (math.hypot(x - wing.root[0], y - wing.root[1]) / reach) ** 1.6:
                out.append((x + dx / dl * inset, y + dy / dl * inset))
            acc += step * rng.uniform(.8, 1.5)
        acc -= seg
    return out


def wing_dots(rng, wing, fill):
    cache = {}

    def dens(x, y):
        key = (int(x // 1.5), int(y // 1.5))
        if key not in cache:
            cache[key] = wing.density(x, y)
        return cache[key]

    st = Stipple(rng, wing.inside, dens)
    st.add(rim(rng, wing), 2.8, 2.8, gate=1, tag=1)
    fibres = list(streamlines(rng, wing, 84))
    rng.shuffle(fibres)
    st.add(fibres, 2.2, 4.4, gate=.4, tag=2)
    st.add(uniform(rng, wing.box, fill), 3.2, 14.0, gate=.06)
    dots = []
    for x, y, tag, d, t, rimv in st.pts:
        roll = rng.random()
        if tag == 1:
            col = "deep" if roll < .35 else "violet" if roll < .85 else "soft"
            r, op = rng.uniform(.85, 1.35), rng.uniform(.55, .95)
        else:
            if t > .6 and roll < .6 * ((t - .6) / .4) ** 1.2:
                col = "deep" if t > .9 and rng.random() < .4 else "violet"
            elif roll < .025:
                col = "violet"
            else:
                col = "white" if d > .45 else "soft"
            r, op = (.72 + 1.4 * d ** .9) * rng.uniform(.85, 1.15), .2 + .8 * d
        dots.append((x, y, r, op, col, d))
    return dots


def body_dots(rng):
    """Head, thorax and tapering abdomen, then two clubbed antennae."""
    def inside(x, y):
        return (math.hypot(x, y + 44) < 7.2 or (x / 6.6) ** 2 + ((y + 18) / 18) ** 2 < 1
                or (x / (5.2 * max(0.15, 1 - max(0, y - 30) / 52))) ** 2 + ((y - 30) / 48) ** 2 < 1)

    def dens(x, y):
        return (1 - min(1, max(0, y - 20) / 70) * .45,)

    st = Stipple(rng, inside, dens).add(uniform(rng, (-8, -52, 8, 80), 5000), 2.4, 3.0, gate=1)
    dots = [(x, y, 1.15 + .65 * d * rng.uniform(.85, 1.1), .95 * d, "white", d) for x, y, _, d in st.pts]
    for side, end, ctrl in ((-1, (-40, -148), (-6, -108)), (1, (44, -142), (11, -104))):
        sx, sy = 2.4 * side, -49
        n = 26
        for s in range(n + 1):
            u = s / n
            x = (1 - u) ** 2 * sx + 2 * (1 - u) * u * ctrl[0] + u * u * end[0]
            y = (1 - u) ** 2 * sy + 2 * (1 - u) * u * ctrl[1] + u * u * end[1]
            dots.append((x, y, 1.05 - .3 * u, .85 - .3 * u, "white", .6))
        for k in range(7):
            a = rng.uniform(0, 2 * math.pi)
            rr = rng.uniform(0, 3.4)
            dots.append((end[0] + rr * math.cos(a), end[1] + rr * math.sin(a), rng.uniform(1.1, 1.6), .9,
                         "violet" if k % 3 == 0 else "white", .8))
    return dots


def ambient_dots(rng, wings, n=110):
    """Loose dots scattered around the silhouette, like the stray stipple around a print."""
    out = []
    while len(out) < n:
        a, rr = rng.uniform(0, 2 * math.pi), rng.uniform(.6, 1.05)
        x, y = 245 * rr * math.cos(a), 200 * rr * math.sin(a) + 10
        if any(w.inside(x, y) for w in wings):
            continue
        out.append((x, y, rng.uniform(.5, 1.0), rng.uniform(.08, .3), "violet" if rng.random() < .35 else "soft", 0))
    return out


def circles(dots, twinkle, uid, rng):
    """Group dots by colour and opacity step; a seeded share gets a twinkle class."""
    groups = {}
    for x, y, r, op, col, d in dots:
        groups.setdefault((col, min(10, max(1, round(op * 10)))), []).append((x, y, r, d))
    out = []
    for (col, op), items in sorted(groups.items()):
        cs = []
        for x, y, r, d in items:
            cls = f' class="{uid}t{rng.randrange(6)}"' if d > .2 and rng.random() < twinkle else ""
            cs.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r:.2f}"{cls}/>')
        out.append(f'<g fill="{INK[col]}" opacity="{op / 10:g}">{"".join(cs)}</g>')
    return "".join(out)


def particles(rng, wings, uid, n=240):
    """Violet specks shed on each wingbeat: each leaves a wing as it opens, then drifts out,
    shrinks and fades behind the butterfly. Delays are multiples of the flap period, so every
    particle launches when the wings are open, about half of them on each beat."""
    out = []
    for i in range(n):
        w = wings[i % len(wings)]
        rx, ry = w.root
        while True:
            x, y = rng.uniform(w.box[0], w.box[2]), rng.uniform(w.box[1], w.box[3])
            if w.inside(x, y) and w.t(x, y) > .5:
                break
        ox, oy = x - rx, y - ry
        ln = math.hypot(ox, oy) or 1
        hx, hy = ox / ln, oy / ln + .45
        ang = math.degrees(math.atan2(hy, hx)) + rng.uniform(-30, 30)
        col = INK["deep"] if rng.random() < .3 else INK["violet"]
        delay = rng.choice((0, FLAP)) + rng.uniform(-.3, .3)
        out.append(f'<g transform="translate({x:.1f} {y:.1f}) rotate({ang:.0f})"><circle class="{uid}p{rng.randrange(4)}" '
                   f'r="{rng.uniform(1.3, 2.4):.2f}" fill="{col}" style="animation-delay:{-delay:.2f}s"/></g>')
    return "".join(out)


def build(uid="bf"):
    """Return (css, art) for a butterfly centred on (0, 0) in a 520 x 420 box."""
    rng = random.Random(SEED)
    lf, lh = Wing(FORE, rng), Wing(HIND, rng, scale=.86, veins=6)
    rf = Wing(FORE, rng, mirror=True, scale=.965, rot=-3, jitter=6)
    rh = Wing(HIND, rng, mirror=True, scale=.9, rot=4, jitter=6, veins=6)
    wings = (lh, rh, lf, rf)
    fill = {lf: 26000, rf: 26000, lh: 20000, rh: 20000}
    parts = [f'<g class="{uid}a">' + circles(ambient_dots(rng, wings), .35, uid, rng) + "</g>",
             f'<g class="motion">{particles(rng, wings, uid)}</g>']  # drawn under the wings: they recede behind them
    for w, cls in ((lh, "h"), (rh, "h"), (lf, "w"), (rf, "w")):
        parts.append(f'<g class="{uid}{cls}">{circles(wing_dots(rng, w, fill[w]), .1, uid, rng)}</g>')
    parts.append(f'<g class="{uid}b">{circles(body_dots(rng), .05, uid, rng)}</g>')
    u = uid
    css = (f"@keyframes {u}f{{0%,100%{{transform:scaleX(1)}}50%{{transform:scaleX(.3)}}}}"
           f".{u}w,.{u}h{{transform-origin:0 0;animation:{u}f {FLAP}s ease-in-out infinite}}.{u}h{{animation-delay:.12s}}"
           f"@keyframes {u}m{{0%,100%{{transform:translate(0,0) rotate(0)}}25%{{transform:translate(6px,-8px) rotate(1.5deg)}}"
           f"50%{{transform:translate(1px,-13px) rotate(0)}}75%{{transform:translate(-6px,-6px) rotate(-1.5deg)}}}}"
           f".{u}m{{transform-origin:0 0;animation:{u}m {FLOAT}s ease-in-out infinite}}"
           f"@keyframes {u}t{{0%,100%{{opacity:1}}50%{{opacity:.18}}}}"
           + "".join(f".{u}t{i}{{animation:{u}t {2.4 + .5 * i:.1f}s ease-in-out {-.7 * i:.1f}s infinite}}" for i in range(6))
           + "".join(f"@keyframes {u}p{i}{{0%{{transform:translate(0,0) scale(1);opacity:0}}8%{{opacity:1}}"
                     f"50%{{opacity:.7}}100%{{transform:translate({46 + 16 * i}px,{(-1) ** i * 12}px) scale(.3);opacity:0}}}}"
                     f".{u}p{i}{{opacity:0;animation:{u}p{i} {2 * FLAP}s cubic-bezier(.2,.6,.4,1) infinite}}" for i in range(4)))
    return css, "".join(parts)


def butterfly(cx, cy, scale, tilt=-6, uid="bf"):
    """Placed butterfly: (css, svg fragment). Drift and tilt pivot on the butterfly's centre."""
    css, art = build(uid)
    return css, (f'<g transform="translate({cx:g} {cy:g})"><g class="{uid}m">'
                 f'<g transform="scale({scale:g}) rotate({tilt:g})">{art}</g></g></g>')


def standalone():
    css, art = butterfly(VB_W / 2, VB_H / 2 + 6, .9)
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{VB_W}" height="{VB_H}" viewBox="0 0 {VB_W} {VB_H}" '
            'role="img" aria-labelledby="title desc"><title id="title">Stippled butterfly</title>'
            '<desc id="desc">A butterfly drawn in white and violet dots on a black background, flapping its wings and drifting.</desc>'
            f'<style>{css}@media(prefers-reduced-motion:reduce){{*{{animation:none!important}}.motion{{display:none}}}}</style>'
            f'<rect width="{VB_W}" height="{VB_H}" rx="20" fill="{BG}"/>{art}</svg>\n')


def main():
    out = ROOT / "assets/butterfly.svg"
    out.write_text(standalone(), encoding="utf-8")
    print(f"Wrote {out.relative_to(ROOT)} ({out.stat().st_size / 1024:.0f} KB)")


if __name__ == "__main__":
    main()
