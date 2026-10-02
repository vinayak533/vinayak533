"""Design tokens and SVG helpers shared by every generated panel.

Every panel is rendered twice (dark, light) and picked by a <picture> element in
the README. Every panel also carries two layouts: `.dsk` for normal widths and
`.mob` for when GitHub draws the image narrower than MOBILE px (a phone). The
switch is a media query *inside* the SVG, which evaluates against the image's
own rendered width.
"""
from xml.sax.saxutils import escape

SANS = "-apple-system,BlinkMacSystemFont,'Segoe UI','Helvetica Neue',Helvetica,Arial,sans-serif"
MONO = "ui-monospace,SFMono-Regular,'SF Mono',Menlo,Consolas,'Liberation Mono',monospace"
W = 880
MOBILE = 560

THEMES = {
    "dark": dict(
        canvas="#0B0E14", raised="#10141B", border="#232A34", border2="#323B47", grid="#161C25",
        text="#E6EDF3", text2="#9BA6B2", text3="#6B7580", accent="#8AB4F8", amber="#F2B45A",
        glow=".10", levels=["#161C25", "#1C355E", "#2A5596", "#4A82D6", "#8AB4F8"],
    ),
    "light": dict(
        canvas="#FBFCFD", raised="#F2F5F8", border="#D8DEE5", border2="#C3CBD5", grid="#E9EDF2",
        text="#1F2328", text2="#57606A", text3="#848D97", accent="#1A73E8", amber="#B25E00",
        glow=".06", levels=["#EBEFF4", "#C6DAFC", "#8AB4F8", "#4285F4", "#1A73E8"],
    ),
}


def esc(s):
    return escape(str(s), {'"': "&quot;"})


def base_css():
    return (
        f".s{{font-family:{SANS}}}.m{{font-family:{MONO};white-space:pre}}"
        f".mob{{display:none}}@media (max-width:{MOBILE}px){{.dsk{{display:none}}.mob{{display:inline}}}}"
        "@keyframes fade{from{opacity:0}to{opacity:1}}"
        "@keyframes rise{from{opacity:0;transform:translateY(8px)}to{opacity:1;transform:translateY(0)}}"
        "@keyframes draw{from{stroke-dashoffset:100}to{stroke-dashoffset:0}}"
        "@keyframes blink{0%,49%{opacity:1}50%,100%{opacity:0}}"
        "@keyframes breathe{0%,100%{opacity:.35}50%{opacity:1}}"
        ".fade{animation:fade .9s ease-out both}"
        ".rise{animation:rise .8s cubic-bezier(.2,.7,.2,1) both}"
        ".draw{stroke-dasharray:100;animation:draw 1.2s cubic-bezier(.65,0,.25,1) both}"
        "@media (prefers-reduced-motion:reduce){*{animation:none!important}}"
    )


def doc(w, h, title, desc, body, css=""):
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" '
        f'role="img" aria-labelledby="t d"><title id="t">{esc(title)}</title><desc id="d">{esc(desc)}</desc>'
        f"<style>{base_css()}{css}</style>{body}</svg>\n"
    )


def panel(t, w, h, rx=14):
    return f'<rect x=".5" y=".5" width="{w - 1}" height="{h - 1}" rx="{rx}" fill="{t["canvas"]}" stroke="{t["border"]}"/>'


def text(x, y, s, size, fill, cls="s", anchor=None, weight=None, ls=None, extra=""):
    x, y = round(x, 1), round(y, 1)
    a = f' text-anchor="{anchor}"' if anchor else ""
    wt = f' font-weight="{weight}"' if weight else ""
    sp = f' letter-spacing="{ls}"' if ls is not None else ""
    return f'<text x="{x}" y="{y}" class="{cls}" font-size="{size}" fill="{fill}"{a}{wt}{sp}{extra}>{esc(s)}</text>'


def delay(s):
    return f' style="animation-delay:{s:.2f}s"'


def line(x1, y1, x2, y2, stroke, cls="draw", d=0.0, width=1, opacity=1.0, dash=None):
    da = f' stroke-dasharray="{dash}"' if dash else ""
    return (
        f'<path d="M{x1} {y1}L{x2} {y2}" pathLength="100" class="{cls}" stroke="{stroke}" '
        f'stroke-width="{width}" stroke-opacity="{opacity}" fill="none"{da}{delay(d)}/>'
    )


def poly(points, stroke, cls="draw", d=0.0, width=1, opacity=1.0, dash=None):
    p = "M" + "L".join(f"{x} {y}" for x, y in points)
    da = f' stroke-dasharray="{dash}"' if dash else ""
    return (
        f'<path d="{p}" pathLength="100" class="{cls}" stroke="{stroke}" stroke-width="{width}" '
        f'stroke-opacity="{opacity}" fill="none" stroke-linejoin="round"{da}{delay(d)}/>'
    )


def motion(points, stops, loop, color, r=3.2, begin=0.0):
    """A dot that travels a polyline. stops[i] is the time (s) it reaches points[i]."""
    import math
    seg = [math.dist(points[i], points[i + 1]) for i in range(len(points) - 1)]
    total = sum(seg) or 1
    cum = [0.0]
    for s in seg:
        cum.append(cum[-1] + s)
    kt, kp = ["0"], ["0"]
    for c, t in zip(cum, stops):
        kt.append(f"{t / loop:.4f}")
        kp.append(f"{c / total:.4f}")
    kt.append("1")
    kp.append("1")
    path = "M" + "L".join(f"{x} {y}" for x, y in points)
    vis_on, vis_off = stops[0] / loop, stops[-1] / loop
    return (
        f'<circle r="{r}" fill="{color}" opacity="0">'
        f'<animateMotion dur="{loop}s" begin="{begin}s" repeatCount="indefinite" calcMode="linear" '
        f'keyTimes="{";".join(kt)}" keyPoints="{";".join(kp)}" path="{path}"/>'
        f'<animate attributeName="opacity" dur="{loop}s" begin="{begin}s" repeatCount="indefinite" '
        f'keyTimes="0;{vis_on:.4f};{min(vis_on + .005, vis_off):.4f};{vis_off:.4f};{min(vis_off + .005, 1):.4f};1" '
        f'values="0;0;1;1;0;0"/></circle>'
    )
