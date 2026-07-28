#!/usr/bin/env python3
"""Generate hero.svg - an aurora banner: a drifting multi-colour gradient field
with the AI/ML ENGINEER wordmark sweeping through violet -> cyan -> magenta.

    python tools/gen_hero.py

Motion notes: the banner is ambient, not looping. The aurora blobs drift on long
co-prime durations so the field never visibly repeats, and the wordmark gradient
sweeps continuously. Only the entrance runs once (`both` fill, no `infinite`) -
a restarting entrance animation is the thing that makes a header feel cheap.

The wordmark uses text-anchor="middle" and an objectBoundingBox gradient, so it
stays centred and correctly filled whatever font the viewer actually resolves.
"""

from pathlib import Path

OUT = Path(__file__).resolve().parent.parent / "assets" / "hero.svg"
OUT.parent.mkdir(parents=True, exist_ok=True)

W, H = 1040, 320
PAD = 10                      # inset of the card inside the viewBox
CARD = (PAD, PAD, W - 2 * PAD, H - 2 * PAD)

HEADLINE = "AI/ML ENGINEER"
PITCH = "I build autonomous agents that turn raw data into decisions."

# ------------------------------------------------------------------- palette
BASE = "#070b18"
VIOLET = "#7C5CFF"
CYAN = "#22D3EE"
MAGENTA = "#F472B6"
INDIGO = "#4F46E5"
INK = "#E2E8F0"
DIM = "#94A3B8"

SANS = "'Segoe UI',Inter,'Helvetica Neue',Helvetica,Arial,sans-serif"

# blobs: (cx, cy, rx, ry, colour, drift-x, drift-y, seconds)
BLOBS = [
    (250, 110, 300, 200, VIOLET, 60, 34, 26),
    (760, 90, 320, 190, CYAN, -70, 40, 31),
    (560, 260, 340, 180, MAGENTA, 46, -36, 37),
    (120, 250, 260, 170, INDIGO, 54, -28, 23),
    (900, 250, 240, 160, VIOLET, -40, -30, 29),
]


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def build_defs():
    d = ["<defs>"]

    # each blob gets a radial fade so the edges melt into the field
    for i, (_, _, _, _, col, _, _, _) in enumerate(BLOBS):
        d.append(
            f'<radialGradient id="b{i}">'
            f'<stop offset="0%" stop-color="{col}" stop-opacity="0.85"/>'
            f'<stop offset="55%" stop-color="{col}" stop-opacity="0.35"/>'
            f'<stop offset="100%" stop-color="{col}" stop-opacity="0"/>'
            f"</radialGradient>")

    # wordmark sweep - objectBoundingBox, so it tracks whatever width the font gives
    d.append(
        '<linearGradient id="wm" x1="0" y1="0" x2="1" y2="0">'
        f'<stop offset="0%" stop-color="{VIOLET}"/>'
        f'<stop offset="30%" stop-color="{CYAN}"/>'
        f'<stop offset="62%" stop-color="{MAGENTA}"/>'
        f'<stop offset="100%" stop-color="{VIOLET}"/>'
        '<animate attributeName="x1" values="-1;0;1" dur="9s" repeatCount="indefinite"/>'
        '<animate attributeName="x2" values="0;1;2" dur="9s" repeatCount="indefinite"/>'
        "</linearGradient>")

    d.append(
        '<linearGradient id="rule" x1="0" y1="0" x2="1" y2="0">'
        f'<stop offset="0%" stop-color="{VIOLET}" stop-opacity="0"/>'
        f'<stop offset="30%" stop-color="{CYAN}" stop-opacity="0.9"/>'
        f'<stop offset="70%" stop-color="{MAGENTA}" stop-opacity="0.9"/>'
        f'<stop offset="100%" stop-color="{VIOLET}" stop-opacity="0"/>'
        "</linearGradient>")

    # darkens the corners so the centre reads as lit
    d.append(
        '<radialGradient id="vig" cx="0.5" cy="0.45" r="0.78">'
        '<stop offset="55%" stop-color="#000000" stop-opacity="0"/>'
        f'<stop offset="100%" stop-color="{BASE}" stop-opacity="0.92"/>'
        "</radialGradient>")

    d.append(
        '<filter id="soften" x="-45%" y="-45%" width="190%" height="190%">'
        '<feGaussianBlur stdDeviation="46"/></filter>')

    # faint dot grid: reads as texture rather than as a pattern
    d.append(
        '<pattern id="dots" width="24" height="24" patternUnits="userSpaceOnUse">'
        '<circle cx="1.5" cy="1.5" r="1" fill="#ffffff" opacity="0.05"/></pattern>')

    x, y, w, h = CARD
    d.append(f'<clipPath id="card"><rect x="{x}" y="{y}" width="{w}" height="{h}" '
             f'rx="18"/></clipPath>')
    d.append("</defs>")
    return "".join(d)


def build_css():
    c = ["<style>", f".s{{font-family:{SANS}}}"]

    for i, (_, _, _, _, _, dx, dy, secs) in enumerate(BLOBS):
        c.append(
            f"@keyframes d{i}{{"
            f"0%{{transform:translate(0,0) scale(1)}}"
            f"50%{{transform:translate({dx}px,{dy}px) scale(1.12)}}"
            f"100%{{transform:translate(0,0) scale(1)}}}}")
        c.append(f".d{i}{{animation:d{i} {secs}s ease-in-out infinite}}")

    # entrance plays once - see the note at the top of the file
    c.append("@keyframes rise{from{opacity:0;transform:translateY(16px)}"
             "to{opacity:1;transform:translateY(0)}}")
    c.append(".rise{opacity:0;animation:rise .9s cubic-bezier(.2,.7,.3,1) both}")
    c.append("@keyframes widen{from{transform:scaleX(0)}to{transform:scaleX(1)}}")
    c.append(f".widen{{transform-origin:{W / 2}px 0;"
             "animation:widen 1.1s cubic-bezier(.2,.8,.25,1) both}")
    c.append("</style>")
    return "".join(c)


def main():
    x, y, w, h = CARD
    s = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" '
         f'viewBox="0 0 {W} {H}" role="img" '
         f'aria-label="{esc(HEADLINE)} - {esc(PITCH)}">']
    s.append(build_defs())
    s.append(build_css())

    s.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="18" fill="{BASE}"/>')

    # ---- aurora field
    s.append('<g clip-path="url(#card)">')
    s.append('<g filter="url(#soften)">')
    for i, (bx, by, rx, ry, _, _, _, _) in enumerate(BLOBS):
        s.append(f'<ellipse class="d{i}" cx="{bx}" cy="{by}" rx="{rx}" ry="{ry}" '
                 f'fill="url(#b{i})"/>')
    s.append("</g>")
    s.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="url(#dots)"/>')
    s.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="url(#vig)"/>')
    s.append("</g>")

    # ---- wordmark
    s.append(f'<text class="s rise" x="{W / 2}" y="{H / 2 + 4}" text-anchor="middle" '
             f'font-size="66" font-weight="800" letter-spacing="7" '
             f'fill="url(#wm)" style="animation-delay:.1s">{esc(HEADLINE)}</text>')

    s.append(f'<rect class="widen" x="{W / 2 - 210}" y="{H / 2 + 30}" width="420" '
             f'height="2.5" rx="1.25" fill="url(#rule)" style="animation-delay:.5s"/>')

    s.append(f'<text class="s rise" x="{W / 2}" y="{H / 2 + 70}" text-anchor="middle" '
             f'font-size="17" fill="{DIM}" letter-spacing="0.4" '
             f'style="animation-delay:.7s">{esc(PITCH)}</text>')

    # hairline edge, keeps the card from bleeding into a dark README
    s.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="18" fill="none" '
             f'stroke="{INK}" stroke-opacity="0.09"/>')

    s.append("</svg>")

    svg = "".join(s)
    OUT.write_text(svg, encoding="utf-8")
    print(f"wrote {OUT}  ({len(svg) / 1024:.1f} KB)")


if __name__ == "__main__":
    main()
