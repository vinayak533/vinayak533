#!/usr/bin/env python3
"""Generate a contribution-snake SVG with a scatter burst on every cell eaten.

Platane/snk has no particle effect, so this renders the animation from
scratch: the snake walks a serpentine path over the contribution grid and
each contribution cell explodes into drifting particles as it is consumed.

Contribution data comes from the public (unauthenticated) endpoint
https://github.com/users/<user>/contributions
"""

import re
import sys
import urllib.request

USER = sys.argv[1] if len(sys.argv) > 1 else "vinayak533"
OUT = sys.argv[2] if len(sys.argv) > 2 else "assets/snake.svg"

CELL, GAP = 12, 3
PITCH = CELL + GAP
OX, OY = 12, 12
STEP = 0.05          # seconds the snake spends per cell
LEAD = 6             # off-screen cells before/after, so the loop wraps unseen
SNAKE_LEN = 6
PARTICLES = 6
BURST_PX = 15.0

EMPTY = "#0b1533"
LEVELS = {1: "#0e4a7a", 2: "#1c7fc4", 3: "#36BCF7", 4: "#00F7FF"}
SNAKE = "#00F7FF"


def fetch_grid(user):
    """Return {(row, col): level} plus the max column index."""
    url = f"https://github.com/users/{user}/contributions"
    req = urllib.request.Request(url, headers={"User-Agent": "snake-gen"})
    with urllib.request.urlopen(req, timeout=30) as r:
        html = r.read().decode("utf-8", "replace")

    grid, max_col = {}, 0
    for td in re.findall(r"<td[^>]*class=\"ContributionCalendar-day\"[^>]*>", html):
        mid = re.search(r'id="contribution-day-component-(\d+)-(\d+)"', td)
        mlv = re.search(r'data-level="(\d+)"', td)
        if not (mid and mlv):
            continue
        row, col = int(mid.group(1)), int(mid.group(2))
        grid[(row, col)] = int(mlv.group(1))
        max_col = max(max_col, col)
    if not grid:
        raise SystemExit("no contribution cells parsed - page layout changed?")
    return grid, max_col


def serpentine(max_col):
    """Column-by-column path, alternating down and up."""
    for col in range(max_col + 1):
        rows = range(7) if col % 2 == 0 else range(6, -1, -1)
        for row in rows:
            yield row, col


def main():
    grid, max_col = fetch_grid(USER)
    order = list(serpentine(max_col))
    step_of = {rc: i for i, rc in enumerate(order)}

    width = OX * 2 + (max_col + 1) * PITCH
    height = OY * 2 + 7 * PITCH

    def cx(col):
        return OX + col * PITCH + CELL / 2

    def cy(row):
        return OY + row * PITCH + CELL / 2

    # Path: lead-in at row 0, the serpentine, then lead-out.
    pts = [(cx(-LEAD + i), cy(0)) for i in range(LEAD)]
    pts += [(cx(c), cy(r)) for r, c in order]
    last_r, last_c = order[-1]
    pts += [(cx(last_c + 1 + i), cy(last_r)) for i in range(LEAD)]

    total = (len(pts) - 1) * STEP
    half = total / 2
    path = "M" + " L".join(f"{x:.1f} {y:.1f}" for x, y in pts)

    # A cell is eaten once the snake's head reaches it.
    def eat_delay(rc):
        return (LEAD + step_of[rc]) * STEP - half

    out = []
    out.append(
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" '
        f'height="{height}" viewBox="0 0 {width} {height}">'
    )

    css = [
        "<style>",
        f".c{{rx:2.5px;}}",
        # Each level steps to EMPTY halfway through the loop; the per-cell
        # animation-delay slides that step to the moment the snake arrives.
        # Negative delays are what let one keyframe set serve every cell.
    ]
    for lv, col in LEVELS.items():
        css.append(
            f"@keyframes e{lv}{{0%,49.99%{{fill:{col}}}50%,100%{{fill:{EMPTY}}}}}"
        )
        css.append(
            f".l{lv}{{fill:{col};animation:e{lv} {total:.2f}s linear infinite;"
            "animation-fill-mode:backwards}"
        )
    import math

    for p in range(PARTICLES):
        ang = 2 * math.pi * p / PARTICLES
        dx, dy = BURST_PX * math.cos(ang), BURST_PX * math.sin(ang)
        css.append(
            f"@keyframes b{p}{{0%,49.99%{{opacity:0;transform:translate(0,0)}}"
            f"50%{{opacity:.95;transform:translate(0,0)}}"
            f"57%,100%{{opacity:0;transform:translate({dx:.1f}px,{dy:.1f}px)}}}}"
        )
        css.append(
            f".p{p}{{animation:b{p} {total:.2f}s linear infinite;"
            "animation-fill-mode:backwards;opacity:0}"
        )
    css.append("</style>")
    out.append("".join(css))

    out.append(f'<rect width="{width}" height="{height}" fill="#000428" rx="10"/>')

    # cells
    out.append("<g>")
    for (row, col), lv in sorted(grid.items()):
        x, y = OX + col * PITCH, OY + row * PITCH
        if lv == 0:
            out.append(
                f'<rect class="c" x="{x}" y="{y}" width="{CELL}" '
                f'height="{CELL}" fill="{EMPTY}"/>'
            )
        else:
            d = eat_delay((row, col))
            out.append(
                f'<rect class="c l{lv}" x="{x}" y="{y}" width="{CELL}" '
                f'height="{CELL}" style="animation-delay:{d:.2f}s"/>'
            )
    out.append("</g>")

    # scatter particles, only for cells that actually hold contributions
    out.append(f'<g fill="{SNAKE}">')
    for (row, col), lv in sorted(grid.items()):
        if lv == 0:
            continue
        d = eat_delay((row, col))
        px, py = cx(col), cy(row)
        r = 1.1 + 0.35 * lv
        for p in range(PARTICLES):
            out.append(
                f'<circle class="p{p}" cx="{px:.1f}" cy="{py:.1f}" '
                f'r="{r:.1f}" style="animation-delay:{d:.2f}s"/>'
            )
    out.append("</g>")

    # snake: head plus trailing segments, each lagging by one step
    out.append(
        '<g><filter id="g"><feGaussianBlur stdDeviation="2.2" result="b"/>'
        '<feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/>'
        "</feMerge></filter>"
    )
    for i in range(SNAKE_LEN):
        size = CELL - i * 1.15
        op = 1.0 - i * 0.13
        rad = (CELL / 2) - i * 0.5
        out.append(
            f'<rect x="{-size/2:.2f}" y="{-size/2:.2f}" width="{size:.2f}" '
            f'height="{size:.2f}" rx="{rad:.2f}" fill="{SNAKE}" '
            f'opacity="{op:.2f}" filter="url(#g)">'
            f'<animateMotion dur="{total:.2f}s" repeatCount="indefinite" '
            f'begin="-{(total - i * STEP):.2f}s" path="{path}"/></rect>'
        )
    out.append("</g></svg>")

    with open(OUT, "w", encoding="utf-8") as f:
        f.write("".join(out))

    lit = sum(1 for v in grid.values() if v > 0)
    print(f"wrote {OUT}: {len(grid)} cells, {lit} lit, loop {total:.1f}s")


if __name__ == "__main__":
    main()
