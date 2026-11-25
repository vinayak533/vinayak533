"""Design tokens and SVG primitives shared by every generated profile asset.

The system: one black stage, the same as behind the hero butterfly, in both
GitHub themes; white type; colour only where something happens. Blue = agent
systems (loom.ai), green = grounded generation (lazyhire), amber = applied ML
(InForge-AI), violet = the butterfly. Two cards leave the stage on purpose: the
research paper is an ivory page and the portfolio is the site's own blue. Cards
use a 24 px radius; padding is 36 px desktop / 24 px compact. All motion is CSS
or SMIL inside the SVG, stops under prefers-reduced-motion, and every panel is
complete on its first frame.
"""
import random
from xml.sax.saxutils import escape

W, MW = 880, 400          # desktop / compact canvas widths
P, MP = 36, 24            # inner padding
R, CR = 24, 16            # card / cover radius
SANS = "-apple-system,BlinkMacSystemFont,'Segoe UI Variable Display','Segoe UI','Noto Sans',Helvetica,Arial,sans-serif"
MONO = "ui-monospace,SFMono-Regular,'SF Mono',Menlo,Consolas,'Liberation Mono',monospace"
SERIF = "Georgia,'Times New Roman',Times,serif"

# Every panel is the same black stage as the butterfly, in both GitHub themes.
TOKENS = {
    "bg": "#000000", "raise": "#101015", "fill": "#1A1A22", "line": "#26262F", "text": "#F4F5F6", "text2": "#B4B8C2",
    "text3": "#8D929D", "inv": "#F4F5F6", "invtext": "#0D0D0D", "dot": "#26262F", "blue": "#8AB4F8", "green": "#7EE2A8",
    "amber": "#FFC078", "violet": "#B9A6FB", "violetlo": "#5C4AA8",
}
V = {k: f"var(--{k})" for k in TOKENS}

# Cover artwork: base colour plus soft light sources (x, y, radius as fractions of the cover, colour, opacity).
COVERS = {
    "blue": ("#2436B8", [(.10, .00, .62, "#5B8CFF", .95), (.95, .10, .60, "#B58CFF", .95), (.55, 1.1, .70, "#37C8F5", .75),
                         (.30, .75, .40, "#6C5CF0", .8), (.80, .72, .34, "#F5B8E8", .6)]),
    "green": ("#0A5F55", [(.05, .05, .62, "#19B394", .95), (.95, .00, .58, "#B7E88A", .85), (.75, 1.1, .66, "#0E8FA8", .85),
                          (.35, .95, .46, "#34C77B", .7), (.62, .34, .30, "#E9F7A6", .45)]),
    "amber": ("#C2410C", [(.05, .00, .60, "#FF8A4C", .95), (.98, .05, .62, "#FFC25C", .95), (.80, 1.1, .62, "#F0567A", .9),
                          (.25, 1.0, .50, "#D9379A", .55), (.58, .30, .30, "#FFE1A8", .55)]),
    "violet": ("#33218F", [(.02, .00, .55, "#5F7BFF", .9), (.98, .10, .62, "#C58BFF", .95), (.70, 1.2, .70, "#FF9EC4", .75),
                           (.30, 1.0, .46, "#3FA9F5", .6)]),
}


def esc(value):
    return escape(str(value), {'"': "&quot;"})


def tw(s, size, mono=False, weight=400):
    """Conservative width estimate, used for layout; labels are centred so any error stays symmetric."""
    if mono:
        return len(s) * size * 0.61
    narrow, wide = set("iljtfr.,:;'|!I ·()[]"), set("mwMWGOQDHNU@%")
    em = sum(.30 if c in narrow else .82 if c in wide else .64 if c.isupper() else .55 for c in s)
    return em * size * (1.05 if weight >= 600 else 1)


def text(x, y, value, size, fill, mono=False, weight=400, anchor="start", ls=0, cls="", extra=""):
    c = ("m " if mono else "s ") + cls
    spacing = f' letter-spacing="{ls}"' if ls else ""
    w = f' font-weight="{weight}"' if weight != 400 else ""
    a = f' text-anchor="{anchor}"' if anchor != "start" else ""
    return (f'<text x="{x:g}" y="{y:g}" class="{c.strip()}" font-size="{size}" fill="{fill}"'
            f'{w}{a}{spacing}{extra}>{esc(value)}</text>')


def hline(x1, y, x2, color=V["line"]):
    return f'<path d="M{x1:g} {y:g}H{x2:g}" stroke="{color}"/>'


def vline(x, y1, y2, color=V["line"]):
    return f'<path d="M{x:g} {y1:g}V{y2:g}" stroke="{color}"/>'


def arrow(x, y, color, s=11, width=1.5):
    """North-east arrow whose top-right corner sits at (x, y)."""
    return (f'<path d="M{x-s+1.5:g} {y:g}H{x:g}V{y+s-1.5:g}M{x:g} {y:g}L{x-s:g} {y+s:g}" stroke="{color}" '
            f'stroke-width="{width}" fill="none" stroke-linecap="round" stroke-linejoin="round"/>')


def check(x, y, color):
    return f'<path d="M{x:g} {y - 3:g}l3 3 6-6.5" fill="none" stroke="{color}" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/>'


# ------------------------------------------------------------------ surfaces
def surface(w, h, x=0, y=0, rx=R):
    return (f'<rect x="{x + .5:g}" y="{y + .5:g}" width="{w - 1:g}" height="{h - 1:g}" rx="{rx}" '
            f'fill="{V["bg"]}" stroke="{V["line"]}"/>')


def open_button(x, y, r=18):
    """Round affordance in a card's corner: this whole card opens something."""
    return f'<circle cx="{x}" cy="{y}" r="{r}" fill="{V["fill"]}"/>' + arrow(x + 4.5, y - 4.5, V["text"], 9.5, 1.7)


def cover(x, y, w, h, hue, art, uid="k", rx=CR, shade=0):
    """Artwork panel: soft fields of light with fine grain, the same in both themes. art is drawn inside the clip."""
    base, lights = COVERS[hue]
    defs = (f'<clipPath id="{uid}c"><rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}"/></clipPath>'
            f'<filter id="{uid}n" x="0" y="0" width="100%" height="100%"><feTurbulence type="fractalNoise" baseFrequency=".85" numOctaves="2" seed="5"/>'
            '<feColorMatrix values="0 0 0 0 1 0 0 0 0 1 0 0 0 0 1 0 0 0 .55 -.18"/></filter>')
    body = f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{base}"/>'
    for i, (fx, fy, fr, col, op) in enumerate(lights):
        defs += (f'<radialGradient id="{uid}{i}"><stop stop-color="{col}" stop-opacity="{op}"/>'
                 f'<stop offset=".45" stop-color="{col}" stop-opacity="{op * .5:.2f}"/><stop offset="1" stop-color="{col}" stop-opacity="0"/></radialGradient>')
        body += (f'<ellipse class="dr{i}" cx="{x + fx * w:.0f}" cy="{y + fy * h:.0f}" rx="{fr * w:.0f}" ry="{fr * max(h, w * .6):.0f}" fill="url(#{uid}{i})"/>')
    body += f'<rect x="{x}" y="{y}" width="{w}" height="{h}" filter="url(#{uid}n)" opacity=".16"/>'
    if shade:
        defs += (f'<linearGradient id="{uid}s" x1="0" y1="0" x2="0" y2="1"><stop stop-color="#000" stop-opacity="0"/>'
                 '<stop offset="1" stop-color="#000" stop-opacity=".55"/></linearGradient>')
        body += f'<rect x="{x}" y="{y + h - shade}" width="{w}" height="{shade}" fill="url(#{uid}s)"/>'
    return f'<defs>{defs}</defs><g clip-path="url(#{uid}c)">{body}{art}</g>'


def rng(seed):
    return random.Random(seed)


# ------------------------------------------------------------------ glyphs
_STROKE = {
    "refresh": "M3-1.2A3.2 3.2 0 1 0 3.2 1.4M3.4-3.6V-1.1H.9", "doc": "M-2.6-3.6H1L2.8-1.8V3.6H-2.6ZM-1.2 0H1.4M-1.2 1.8H1.4",
    "globe": "M-3.6 0H3.6M0-3.6A1.6 3.6 0 0 1 0 3.6A1.6 3.6 0 0 1 0-3.6", "mail": "M-3.6-2.8H3.6V2.8H-3.6ZM-3.2-2.2L0 .5 3.2-2.2",
    "linkedin": "M-1.8-.6V2.4M.3 2.4V-.6M.3 .8C.3-.2 .9-.7 1.6-.7S2.6-.2 2.6.8V2.4",
}
_FILL = {"bolt": "M.8-4L-2.6.6H0L-.8 4 2.6-.6H0Z"}


def glyph(kind, cx, cy, color, s=1.0, width=1.3):
    g = f'<g transform="translate({cx:.1f} {cy:.1f}) scale({s:g})">'
    sw = f'stroke-width="{width / s:.2f}"'
    if kind in _FILL:
        g += f'<path d="{_FILL[kind]}" fill="none" stroke="{color}" {sw} stroke-linejoin="round"/>'
    elif kind == "target":
        g += f'<circle r="3.4" fill="none" stroke="{color}" {sw}/><circle r="1.2" fill="{color}"/>'
    else:
        extra = ""
        if kind == "globe":
            extra = f'<circle r="3.6" fill="none" stroke="{color}" {sw}/>'
        elif kind == "linkedin":
            extra = f'<rect x="-3.8" y="-3.8" width="7.6" height="7.6" rx="1.8" fill="none" stroke="{color}" {sw}/><circle cx="-1.8" cy="-2" r=".6" fill="{color}"/>'
        g += (extra + f'<path d="{_STROKE[kind]}" fill="none" stroke="{color}" {sw} '
              'stroke-linecap="round" stroke-linejoin="round"/>')
    return g + "</g>"


# 11 x 11 dot-matrix icons, the same dots the butterfly and the activity panel are made of.
MATRIX = {
    "prompt": ("...........", ".X.........", ".XX........", "..XX.......", "...XX......", "....XX.....", "...XX......", "..XX.......",
               ".XX..XXXXX.", ".X...XXXXX.", "..........."),
    "cite": (".XXX...XXX.", ".X.......X.", ".X...X...X.", ".X..XX...X.", ".X...X...X.", ".X...X...X.", ".X...X...X.", ".X...X...X.",
             ".X..XXX..X.", ".X.......X.", ".XXX...XXX."),
    "bars": ("...........", "........XX.", "........XX.", "........XX.", "....XX..XX.", "....XX..XX.", "....XX..XX.", "XX..XX..XX.",
             "XX..XX..XX.", "XX..XX..XX.", "..........."),
}


def matrix(kind, x, y, color, pitch=4.6):
    on, off = {}, []
    for r, row in enumerate(MATRIX[kind]):
        for c, v in enumerate(row):
            (on.setdefault(c, []) if v == "X" else off).append(f'<circle cx="{x + c * pitch:.1f}" cy="{y + r * pitch:.1f}" r="{pitch * (.40 if v == "X" else .16):.2f}"/>')
    lit = "".join(f'<g class="mx{c}">' + "".join(d) + "</g>" for c, d in sorted(on.items()))
    return f'<g fill="{V["dot"]}">{"".join(off)}</g><g fill="{color}">{lit}</g>'


# A wave of light crosses the icon, one column at a time.
MATRIX_CSS = ("@keyframes mx{0%,30%,100%{opacity:1}12%{opacity:.25}}" + "".join(f".mx{c}{{animation:mx 3.6s ease-in-out {c * .13:.2f}s infinite}}" for c in range(11)))


def doc(w, h, title, desc, body, css=""):
    tokens = "".join(f"--{k}:{v};" for k, v in TOKENS.items())
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" '
            f'role="img" aria-labelledby="title desc"><title id="title">{esc(title)}</title>'
            f'<desc id="desc">{esc(desc)}</desc><style>:root{{{tokens}}}'
            f'.s{{font-family:{SANS}}}.m{{font-family:{MONO}}}.f{{font-family:{SERIF}}}'
            f'{css}@media(prefers-reduced-motion:reduce){{*{{animation:none!important}}.motion{{display:none}}}}'
            f'</style>{body}</svg>\n')
