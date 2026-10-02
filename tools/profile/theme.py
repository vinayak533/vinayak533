"""Design tokens and SVG primitives shared by every generated profile asset.

The system: dark glass surfaces lit from below, tinted status pills, and
dot-matrix artwork. Colour carries meaning: blue = agent systems (loom.ai),
green = grounded generation (lazyhire), orange = applied ML (InForge-AI);
other hues appear only inside pills. Cards use a 20 px radius, pills are
fully rounded, padding is 36 px desktop / 24 px compact. All motion is CSS or
SMIL inside the SVG, stops under prefers-reduced-motion, and every panel is
complete on its first frame.
"""
from xml.sax.saxutils import escape

W, MW = 880, 400          # desktop / compact canvas widths
P, MP = 36, 24            # inner padding
R = 20                    # card radius
SANS = "-apple-system,BlinkMacSystemFont,'Segoe UI','Noto Sans',Helvetica,Arial,sans-serif"
MONO = "ui-monospace,SFMono-Regular,'SF Mono',Menlo,Consolas,'Liberation Mono',monospace"
SERIF = "Georgia,'Times New Roman',Times,serif"

_HUES = {  # base (light source), rim (edge highlight), ink (text on tint)
    "dark": {
        "blue": ("#3B82F6", "#93C5FD", "#BFDBFE"), "green": ("#22C55E", "#86EFAC", "#BBF7D0"),
        "orange": ("#F97316", "#FDBA74", "#FED7AA"), "violet": ("#8B5CF6", "#C4B5FD", "#DDD6FE"),
        "cyan": ("#06B6D4", "#67E8F9", "#A5F3FC"), "yellow": ("#EAB308", "#FDE047", "#FEF08A"),
        "pink": ("#EC4899", "#F9A8D4", "#FBCFE8"), "gray": ("#64748B", "#CBD5E1", "#E2E8F0"),
    },
    "light": {
        "blue": ("#3B82F6", "#2563EB", "#1D4ED8"), "green": ("#22C55E", "#16A34A", "#15803D"),
        "orange": ("#F97316", "#EA580C", "#C2410C"), "violet": ("#8B5CF6", "#7C3AED", "#6D28D9"),
        "cyan": ("#06B6D4", "#0891B2", "#0E7490"), "yellow": ("#EAB308", "#CA8A04", "#A16207"),
        "pink": ("#EC4899", "#DB2777", "#BE185D"), "gray": ("#64748B", "#475569", "#334155"),
    },
}

THEMES = {
    "dark": dict(
        dark=True, base="#090C11", base_top="#10151D", line="#FFFFFF", line_op=.10, hi_op=.14,
        glass="#FFFFFF", glass_op=.035, text="#F3F5F8", text2="#A7B0BC", text3="#7D8796",
        name_lo="#A9B3C1", tag_fill=.16, glow=.85, rim_glow=.65, sheen="#93C5FD",
        dot_hi="#FFFFFF", dot_mid="#93C5FD", dot_lo="#8B5CF6", dot_warm="#FDBA74", dot_off="#FFFFFF", dot_off_op=.09,
    ),
    "light": dict(
        dark=False, base="#FFFFFF", base_top="#F6F8FB", line="#0B1220", line_op=.11, hi_op=0,
        glass="#0B1220", glass_op=.03, text="#0F172A", text2="#4B5563", text3="#5F6B7A",
        name_lo="#334155", tag_fill=.09, glow=.42, rim_glow=.38, sheen="#2563EB",
        dot_hi="#0F172A", dot_mid="#2563EB", dot_lo="#8B5CF6", dot_warm="#EA580C", dot_off="#0B1220", dot_off_op=.08,
    ),
}
# The profile is dark in both GitHub colour modes; the light palette is kept so it can be re-enabled here.
PUBLISHED = ("dark",)
for _name, _t in THEMES.items():
    _t["hues"] = {k: dict(zip(("base", "rim", "ink"), v)) for k, v in _HUES[_name].items()}


def esc(value):
    return escape(str(value), {'"': "&quot;"})


def mix(a, b, f):
    pa, pb = [int(a[i:i + 2], 16) for i in (1, 3, 5)], [int(b[i:i + 2], 16) for i in (1, 3, 5)]
    return "#" + "".join(f"{round(x + (y - x) * f):02X}" for x, y in zip(pa, pb))


def tw(s, size, mono=False, weight=400):
    """Conservative width estimate, used for sizing pills and checking fit."""
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


def hline(t, x1, y, x2, op=None):
    return f'<path d="M{x1:g} {y:g}H{x2:g}" stroke="{t["line"]}" stroke-opacity="{op or t["line_op"]}"/>'


def vline(t, x, y1, y2, op=None):
    return f'<path d="M{x:g} {y1:g}V{y2:g}" stroke="{t["line"]}" stroke-opacity="{op or t["line_op"]}"/>'


def arrow(x, y, color, s=11, width=1.5):
    """North-east arrow whose top-right corner sits at (x, y)."""
    return (f'<path d="M{x-s:g} {y:g}H{x:g}V{y+s:g}M{x:g} {y:g}L{x-s:g} {y+s:g}" stroke="{color}" '
            f'stroke-width="{width}" fill="none" stroke-linecap="round" stroke-linejoin="round"/>')


# ------------------------------------------------------------------ surfaces
def glass_card(t, w, h, uid="c", rx=R, bloom=None, bloom_at=None):
    """Neutral glass panel; an optional soft bloom of one hue (position in user units)."""
    x1, x2 = rx + 6, w - rx - 6
    defs = (f'<linearGradient id="{uid}b" x1="0" y1="0" x2="0" y2="{h}" gradientUnits="userSpaceOnUse">'
            f'<stop stop-color="{t["base_top"]}"/><stop offset=".6" stop-color="{t["base"]}"/></linearGradient>'
            f'<linearGradient id="{uid}e" x1="{x1}" y1="0" x2="{x2}" y2="0" gradientUnits="userSpaceOnUse">'
            f'<stop stop-color="#FFFFFF" stop-opacity="0"/><stop offset=".5" stop-color="#FFFFFF" stop-opacity="{t["hi_op"]}"/>'
            f'<stop offset="1" stop-color="#FFFFFF" stop-opacity="0"/></linearGradient>'
            f'<clipPath id="{uid}k"><rect x="1" y="1" width="{w-2}" height="{h-2}" rx="{rx-1}"/></clipPath>')
    body = f'<rect x=".5" y=".5" width="{w-1}" height="{h-1}" rx="{rx}" fill="url(#{uid}b)"/>'
    if bloom:
        hue = t["hues"][bloom]
        bx, by, br = bloom_at
        defs += (f'<radialGradient id="{uid}g" cx="{bx}" cy="{by}" r="{br}" gradientUnits="userSpaceOnUse">'
                 f'<stop stop-color="{hue["base"]}" stop-opacity="{t["glow"] * .32:.2f}"/>'
                 f'<stop offset="1" stop-color="{hue["base"]}" stop-opacity="0"/></radialGradient>')
        body += f'<g clip-path="url(#{uid}k)"><circle cx="{bx}" cy="{by}" r="{br}" fill="url(#{uid}g)"/></g>'
    body += (f'<rect x=".5" y=".5" width="{w-1}" height="{h-1}" rx="{rx}" fill="none" stroke="{t["line"]}" stroke-opacity="{t["line_op"]}"/>'
             f'<path d="M{x1} 1H{x2}" stroke="url(#{uid}e)"/>')
    return f"<defs>{defs}</defs>{body}"


def glow_card(t, w, h, hue, uid="g", x=0, y=0, rx=R, strength=1.0):
    """Glass card lit from below by one hue: tinted body, bottom bloom, bright lower rim."""
    c = t["hues"][hue]
    k = strength
    dark = t["dark"]
    top, mid, bot = t["base_top"], mix(t["base"], c["base"], .07 if dark else .03), mix(t["base"], c["base"], (.30 if dark else .13) * k)
    cx, cy = x + w / 2, y + h
    defs = (f'<linearGradient id="{uid}b" x1="0" y1="{y}" x2="0" y2="{y + h}" gradientUnits="userSpaceOnUse">'
            f'<stop stop-color="{top}"/><stop offset=".55" stop-color="{mid}"/><stop offset="1" stop-color="{bot}"/></linearGradient>'
            f'<radialGradient id="{uid}g" cx="0" cy="0" r="1" gradientUnits="userSpaceOnUse" '
            f'gradientTransform="translate({cx:.1f} {cy + h * .06:.1f}) scale({w * .62:.1f} {h * .58:.1f})">'
            f'<stop stop-color="{c["base"]}" stop-opacity="{t["glow"] * k:.2f}"/>'
            f'<stop offset=".45" stop-color="{c["base"]}" stop-opacity="{t["glow"] * k * .32:.2f}"/>'
            f'<stop offset="1" stop-color="{c["base"]}" stop-opacity="0"/></radialGradient>'
            f'<linearGradient id="{uid}r" x1="0" y1="{y}" x2="0" y2="{y + h}" gradientUnits="userSpaceOnUse">'
            f'<stop stop-color="{t["line"]}" stop-opacity="{t["line_op"] * 1.1:.2f}"/>'
            f'<stop offset=".5" stop-color="{c["rim"]}" stop-opacity="{.22 if dark else .2}"/>'
            f'<stop offset="1" stop-color="{c["rim"]}" stop-opacity="{.95 if dark else .75}"/></linearGradient>'
            f'<clipPath id="{uid}k"><rect x="{x + 1}" y="{y + 1}" width="{w - 2}" height="{h - 2}" rx="{rx - 1}"/></clipPath>'
            f'<filter id="{uid}f" x="-20%" y="-200%" width="140%" height="500%"><feGaussianBlur stdDeviation="9"/></filter>')
    body = (f'<rect x="{x + .75}" y="{y + .75}" width="{w - 1.5}" height="{h - 1.5}" rx="{rx}" fill="url(#{uid}b)"/>'
            f'<g clip-path="url(#{uid}k)"><rect x="{x}" y="{y}" width="{w}" height="{h}" fill="url(#{uid}g)"/>'
            f'<ellipse cx="{cx:.1f}" cy="{cy:.1f}" rx="{w * .40:.1f}" ry="13" fill="{c["rim"]}" opacity="{t["rim_glow"] * k:.2f}" filter="url(#{uid}f)"/></g>'
            f'<rect x="{x + .75}" y="{y + .75}" width="{w - 1.5}" height="{h - 1.5}" rx="{rx}" fill="none" stroke="url(#{uid}r)" stroke-width="1.5"/>')
    if dark:
        body += f'<path d="M{x + rx + 6} {y + 1.5}H{x + w - rx - 6}" stroke="#FFFFFF" stroke-opacity=".10"/>'
    return f"<defs>{defs}</defs>{body}"


# ------------------------------------------------------------------ glyphs and pills
_STROKE = {
    "arrow": "M-3 0H3M.5-2.5L3 0 .5 2.5", "check": "M-3 .2L-1 2.2 3-2", "cite": "M-1.2-3H-3V3H-1.2M1.2-3H3V3H1.2",
    "wave": "M-4 0H-2.4L-1.2-2.6.6 2.6 1.8 0H4", "refresh": "M3-1.2A3.2 3.2 0 1 0 3.2 1.4M3.4-3.6V-1.1H.9",
    "doc": "M-2.6-3.6H1L2.8-1.8V3.6H-2.6ZM-1.2 0H1.4M-1.2 1.8H1.4", "window": "M-3.6-3H3.6V3H-3.6ZM-3.6-1.2H3.6",
    "server": "M-3.4-3.4H3.4V-.6H-3.4ZM-3.4.6H3.4V3.4H-3.4Z", "db": "M-3.2-2.4V2.4A3.2 1.2 0 0 0 3.2 2.4V-2.4",
    "cloud": "M-2.4 2.6H2.6A1.8 1.8 0 0 0 2.4-1A2.6 2.6 0 0 0-2.4-.6 1.6 1.6 0 0 0-2.4 2.6Z",
    "swap": "M-3-1.5H3M1.5-3L3-1.5 1.5 0M3 1.5H-3M-1.5 0L-3 1.5-1.5 3", "bars": "M-2.8 3V.4M0 3V-3M2.8 3V-1.2",
    "globe": "M-3.6 0H3.6M0-3.6A1.6 3.6 0 0 1 0 3.6A1.6 3.6 0 0 1 0-3.6", "mail": "M-3.6-2.8H3.6V2.8H-3.6ZM-3.2-2.2L0 .5 3.2-2.2",
    "plus": "M-3 0H3M0-3V3", "linkedin": "M-1.8-.6V2.6M.4 2.6V-.6M.4 .8C.4-.2 1-.7 1.8-.7S3.1-.2 3.1.8V2.6",
}
_FILL = {
    "play": "M-2-3L3 0-2 3Z", "star": "M0-4Q.5-.5 4 0Q.5.5 0 4Q-.5.5-4 0Q-.5-.5 0-4Z",
    "bolt": "M.8-4L-2.6.6H0L-.8 4 2.6-.6H0Z", "dot": "M0-2.4A2.4 2.4 0 1 1 0 2.4A2.4 2.4 0 1 1 0-2.4Z",
}


def glyph(kind, cx, cy, color, s=1.0, width=1.3):
    g = f'<g transform="translate({cx:.1f} {cy:.1f}) scale({s:g})">'
    sw = f'stroke-width="{width / s:.2f}"'
    if kind in _FILL:
        g += f'<path d="{_FILL[kind]}" fill="{color}"/>'
    elif kind == "nodes":
        g += (f'<path d="M0-2.6L-2.6 2 2.6 2Z" fill="none" stroke="{color}" {sw} stroke-opacity=".7"/>'
              + "".join(f'<circle cx="{x}" cy="{y}" r="1.25" fill="{color}"/>' for x, y in ((0, -2.6), (-2.6, 2), (2.6, 2))))
    elif kind == "target":
        g += f'<circle r="3.4" fill="none" stroke="{color}" {sw}/><circle r="1.2" fill="{color}"/>'
    else:
        extra = ""
        if kind == "db":
            extra = f'<ellipse cy="-2.4" rx="3.2" ry="1.2" fill="none" stroke="{color}" {sw}/>'
        elif kind == "globe":
            extra = f'<circle r="3.6" fill="none" stroke="{color}" {sw}/>'
        elif kind == "linkedin":
            extra = f'<rect x="-3.8" y="-3.8" width="7.6" height="7.6" rx="1.8" fill="none" stroke="{color}" {sw}/><circle cx="-1.8" cy="-2" r=".6" fill="{color}"/>'
        g += (extra + f'<path d="{_STROKE[kind]}" fill="none" stroke="{color}" {sw} '
              'stroke-linecap="round" stroke-linejoin="round"/>')
    return g + "</g>"


def tag_defs(t):
    """Per-hue border gradients for pills: brighter on top, like light on a glass edge."""
    out = []
    for name, c in t["hues"].items():
        a, b = (1, .45) if t["dark"] else (.75, .35)
        out.append(f'<linearGradient id="tg-{name}" x1="0" y1="0" x2="0" y2="1">'
                   f'<stop stop-color="{c["rim"]}" stop-opacity="{a}"/><stop offset="1" stop-color="{c["rim"]}" stop-opacity="{b}"/></linearGradient>')
    return "<defs>" + "".join(out) + "</defs>"


def tag_width(label, size=12.5, h=28, icon=True, mono=False, ls=0):
    return (h + 1 if icon else 12) + tw(label, size, mono, 500) + len(label) * ls + 12


def tag(t, x, y, label, hue, icon=None, size=12.5, h=28, mono=False, ls=0, w=None, solid=False):
    """Tinted pill: hue fill, gradient border, filled icon disc, tinted label. solid adds an opaque base for any page colour."""
    c = t["hues"][hue]
    w = w or tag_width(label, size, h, bool(icon), mono, ls)
    out = (f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h}" rx="{h / 2}" fill="{t["base"]}"/>' if solid else "") + (f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h}" rx="{h / 2}" fill="{c["base"]}" '
           f'fill-opacity="{t["tag_fill"]}" stroke="url(#tg-{hue})"/>')
    tx = x + 12
    if icon:
        r = h / 2 - 5
        out += (f'<circle cx="{x + h / 2:.1f}" cy="{y + h / 2:.1f}" r="{r:.1f}" fill="{c["rim"]}"/>'
                + glyph(icon, x + h / 2, y + h / 2, t["base"] if t["dark"] else "#FFFFFF", r / 5.2, 1.5))
        tx = x + h + 1
    ls_attr = ls if ls else 0
    return out + text(tx, y + h / 2 + size * .36, label, size, c["ink"], mono, 500, ls=ls_attr), w


def doc(w, h, title, desc, body, css=""):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" '
            f'role="img" aria-labelledby="title desc"><title id="title">{esc(title)}</title>'
            f'<desc id="desc">{esc(desc)}</desc><style>.s{{font-family:{SANS}}}.m{{font-family:{MONO}}}.f{{font-family:{SERIF}}}'
            f'{css}@media(prefers-reduced-motion:reduce){{*{{animation:none!important}}.motion{{display:none}}}}'
            f'</style>{body}</svg>\n')
