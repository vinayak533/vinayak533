"""The two cards that leave the black stage: the research paper (an ivory page) and the portfolio (Neo, on the site's blue)."""
import base64
from pathlib import Path

from scenes import Film, g
from theme import W, MW, P, MP, R, arrow, doc, rng, text, tw

ROOT = Path(__file__).resolve().parents[2]

# ------------------------------------------------------------------ research paper
PAPER, INK, MUTE, RULE, ACC, WARM = "#F6F2E7", "#1A1710", "#655E4F", "#D8D1BF", "#5B3FD6", "#C2410C"
TITLE_D = ["An AI-Powered Multi-Disease Clinical Risk", "Prediction Platform Using Machine Learning", "and Large Language Model Explanations"]
TITLE_M = ["An AI-Powered Multi-Disease Clinical", "Risk Prediction Platform Using Machine", "Learning and Large Language Model", "Explanations"]
META = [("Author", "Vinayak K V"), ("Published", "17 May 2026, Zenodo"), ("DOI", "10.5281/zenodo.20253956"), ("License", "CC BY 4.0")]
FIGS = [("Fig. 1.", "Diabetes, linear SVM"), ("Fig. 2.", "Stroke, random forest"), ("Fig. 3.", "Heart disease, logistic curve")]
PAPER_DESC = ("Research paper: PredictLab, an AI-powered multi-disease clinical risk prediction platform using machine learning and large language model explanations. "
              "By Vinayak K V, published 17 May 2026 on Zenodo, DOI 10.5281/zenodo.20253956, CC BY 4.0. Animated figures: a linear SVM boundary for diabetes, "
              "a random forest for stroke and a logistic curve for heart disease. Figures are schematic. "
              "Llama 3.1 8B explains each result in plain language, as a risk indicator rather than a diagnosis.")


def serif(x, y, s, size, fill=INK, italic=False, weight=400, anchor="start"):
    return (f'<text x="{x:g}" y="{y:g}" class="f" font-size="{size}" fill="{fill}"{" font-style=" + chr(34) + "italic" + chr(34) if italic else ""}'
            f'{f" font-weight={chr(34)}{weight}{chr(34)}" if weight != 400 else ""}{f" text-anchor={chr(34)}{anchor}{chr(34)}" if anchor != "start" else ""}>{s}</text>')


def draw(f, d, length, a, b, color, width=2.2, extra=""):
    """A path that inks itself between a and b seconds."""
    off, on = f"stroke-dashoffset:{length:.0f}", "stroke-dashoffset:0"
    c = f.track([(0, off), (a, off), (b, on), (f.T - .5, on), (f.T - .4, off), (f.T, off)], "ease-in-out")
    return f'<path class="{c}" d="{d}" fill="none" stroke="{color}" stroke-width="{width}" stroke-linecap="round" stroke-dasharray="{length:.0f}"{extra}/>'


def axes(x, y, w, h):
    return f'<path d="M{x} {y}V{y + h}H{x + w}" fill="none" stroke="{INK}" stroke-opacity=".55" stroke-width="1.2"/>'


def fig_svm(f, x, y, w, h):
    r, b = rng(21), [axes(x, y, w, h)]
    for side in (0, 1):
        for i in range(17):
            while True:
                u, v = r.random(), r.random()
                d = u - v
                if (d > .17) if side else (d < -.17):
                    break
            px, py = x + 12 + u * (w - 24), y + h - 10 - v * (h - 20)
            c = f.enter(.3 + i * .05 + side * .4, 0)
            b.append(f'<circle class="{c}" cx="{px:.1f}" cy="{py:.1f}" r="4" fill="{ACC if side else PAPER}" stroke="{ACC if side else INK}" stroke-width="1.5"/>')
    x0, y0, x1, y1 = x + 12, y + h - 10, x + w - 12, y + 10
    ln = ((x1 - x0) ** 2 + (y1 - y0) ** 2) ** .5
    for s in (-1, 1):  # margins, trimmed to the axes
        k0, k1 = (.12, 0) if s < 0 else (0, .12)
        b.append(g(f.enter(3.1, 0), f'<path d="M{x0 + (x1 - x0) * k0 + s * .1 * w:.1f} {y0 + (y1 - y0) * k0:.1f}L{x1 - (x1 - x0) * k1 + s * .1 * w:.1f} {y1 - (y1 - y0) * k1:.1f}" stroke="{INK}" stroke-opacity=".4" stroke-dasharray="3 5"/>'))
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    rot = lambda a, o=1: f"transform:rotate({a}deg);opacity:{o}"
    fit = f.track([(0, rot(52, 0)), (1.1, rot(52, 0)), (1.35, rot(52)), (1.9, rot(-24)), (2.35, rot(13)), (2.7, rot(-5)), (2.95, rot(0)),
                   (f.T - .5, rot(0)), (f.T, rot(0, 0))], "ease-in-out")   # the boundary swings until it separates the classes
    b.append(f'<defs><clipPath id="svm"><rect x="{x}" y="{y - 6}" width="{w}" height="{h + 6}"/></clipPath></defs>'
             f'<g clip-path="url(#svm)"><path class="{fit}" style="transform-origin:{cx}px {cy}px" d="M{x0} {y0}L{x1} {y1}" stroke="{INK}" stroke-width="2.6" stroke-linecap="round"/></g>')
    return "".join(b)


def fig_forest(f, x, y, w, h):
    b, tw3 = [], w / 3
    votes = (1, 0, 1)
    for k in range(3):
        cx, top = x + tw3 * (k + .5), y + 10
        t = 1.0 + k * .45
        lv = [[(cx, top)], [(cx - tw3 * .24, top + 38), (cx + tw3 * .24, top + 38)],
              [(cx - tw3 * .36, top + 76), (cx - tw3 * .12, top + 76), (cx + tw3 * .12, top + 76), (cx + tw3 * .36, top + 76)]]
        path = [(0, 0), (1, votes[k]), (2, votes[k] * 2 + (k % 2))]
        for a in (0, 1):
            for i, (px, py) in enumerate(lv[a + 1]):
                qx, qy = lv[a][i // 2]
                hot = path[a + 1][1] == i
                b.append(f'<path d="M{qx:.1f} {qy}L{px:.1f} {py}" stroke="{INK}" stroke-opacity=".28" stroke-width="1.3"/>')
                if hot:
                    b.append(draw(f, f"M{qx:.1f} {qy}L{px:.1f} {py}", 60, t + a * .45, t + .45 + a * .45, ACC, 2.6))
        for a in range(3):
            for i, (px, py) in enumerate(lv[a]):
                b.append(f'<circle cx="{px:.1f}" cy="{py}" r="4" fill="{PAPER}" stroke="{INK}" stroke-width="1.4"/>')
                if path[a][1] == i:
                    b.append(f'<circle class="{f.enter(t + a * .45, 0)}" cx="{px:.1f}" cy="{py}" r="4.6" fill="{ACC}"/>')
        b.append(draw(f, f"M{path and lv[2][path[2][1]][0]:.1f} {top + 82}C{lv[2][path[2][1]][0]:.1f} {top + 106} {x + w / 2:.1f} {top + 96} {x + w / 2:.1f} {top + 116}", 130, 3.0, 3.8, INK, 1.4))
    b.append(g(f.enter(3.8, 0), f'<circle cx="{x + w / 2}" cy="{y + 134}" r="8" fill="{ACC}"/><circle class="ring motion" cx="{x + w / 2}" cy="{y + 134}" r="8" fill="none" stroke="{ACC}"/>' + text(x + w / 2 + 16, y + 139, "vote", 14, INK)))
    return "".join(b)


def fig_logit(f, x, y, w, h):
    import math
    r, b = rng(8), [axes(x, y, w, h)]
    pts = []
    for k in range(41):
        u = k / 40
        pts.append((x + 8 + u * (w - 16), y + h - 12 - (h - 24) / (1 + math.exp(-(u - .5) * 12))))
    ln = sum(math.dist(a, c) for a, c in zip(pts, pts[1:])) + 3
    for i in range(26):
        u = r.random()
        one = r.random() < 1 / (1 + math.exp(-(u - .5) * 11))
        c = f.enter(.5 + u * .9, 0)
        b.append(f'<circle class="{c}" cx="{x + 8 + u * (w - 16):.1f}" cy="{(y + 12 if one else y + h - 12) + r.gauss(0, 1.5):.1f}" r="4" '
                 f'fill="{ACC if one else PAPER}" stroke="{ACC if one else INK}" stroke-width="1.5"/>')
    b.append(g(f.enter(3.4, 0), f'<path d="M{x + w / 2} {y + 6}V{y + h}" stroke="{INK}" stroke-opacity=".4" stroke-dasharray="3 5"/>'))
    d = "M" + " L".join(f"{a:.1f} {c:.1f}" for a, c in pts)
    b.append(draw(f, d, ln, 1.9, 3.4, INK, 2.6))
    # A new case rides the fitted curve from low to high risk.
    b.append(g(f.track([(0, "opacity:0"), (3.9, "opacity:0"), (4.1, "opacity:1"), (f.T - .6, "opacity:1"), (f.T - .3, "opacity:0"), (f.T, "opacity:0")]) + " motion",
               f'<circle r="11" fill="{ACC}" fill-opacity=".18"><animateMotion dur="3.2s" repeatCount="indefinite" path="{d}" calcMode="spline" keyTimes="0;1" keySplines=".45 0 .55 1" keyPoints="0;1"/></circle>'
               f'<circle r="5" fill="{ACC}"><animateMotion dur="3.2s" repeatCount="indefinite" path="{d}" calcMode="spline" keyTimes="0;1" keySplines=".45 0 .55 1" keyPoints="0;1"/></circle>'))
    return "".join(b)


def sheet(w, h):
    """Ivory page with a faint ruled edge."""
    return f'<rect x=".5" y=".5" width="{w - 1}" height="{h - 1}" rx="{R}" fill="{PAPER}" stroke="{RULE}"/>'


def open_ink(x, y, r=20):
    return f'<circle cx="{x}" cy="{y}" r="{r}" fill="{INK}"/>' + arrow(x + 5, y - 5, PAPER, 10.5, 1.8)


def paper(m=False):
    f, b = Film(11), []
    draws = (fig_svm, fig_forest, fig_logit)
    if m:
        w, p, y = MW, MP, 44
        b += [text(p, 50, "Research paper", 14.5, MUTE), open_ink(w - p - 20, 46), serif(p, 112, "PredictLab", 54)]
        b += [serif(p, 148 + i * 26, s, 19, "#3A3528") for i, s in enumerate(TITLE_M)]
        y = 262
        b.append(f'<path d="M{p} {y}H{w - p}" stroke="{RULE}"/>')
        for i, (k, v) in enumerate(META):
            b += [text(p, y + 34 + i * 30, k, 14.5, MUTE), text(w - p, y + 34 + i * 30, v, 15, INK, weight=600, anchor="end")]
        y += 34 + 4 * 30 + 8
        b.append(f'<path d="M{p} {y - 18}H{w - p}" stroke="{RULE}"/>')
        for i, (fn, (n, cap)) in enumerate(zip(draws, FIGS)):
            b += [fn(f, p + 4, y + 8, w - 2 * p - 8, 148), serif(p, y + 188, f'{n} <tspan font-style="italic">{cap}</tspan>', 16)]
            y += 220
        b += [text(p, y + 8, "Llama 3.1 8B explains each result in", 15.5, "#3A3528"), text(p, y + 30, "plain language, as a risk indicator", 15.5, "#3A3528"),
              text(p, y + 52, "rather than a diagnosis.", 15.5, "#3A3528")]
        h = y + 82
    else:
        w, p, h = W, P, 546
        b += [text(p, 54, "Research paper", 14.5, MUTE), open_ink(w - p - 20, 54), serif(p, 124, "PredictLab", 68)]
        b += [serif(p, 166 + i * 29, s, 22, "#3A3528") for i, s in enumerate(TITLE_D)]
        for i, (k, v) in enumerate(META):
            yy = 136 + i * 30
            b += [text(556, yy, k, 14, MUTE), text(w - p, yy, v, 15, INK, weight=600, anchor="end")]
        b.append(f'<path d="M{p} 256H{w - p}" stroke="{RULE}"/>')
        fw, gap = (w - 2 * p - 64) / 3, 32
        for i, (fn, (n, cap)) in enumerate(zip(draws, FIGS)):
            x = p + i * (fw + gap)
            b += [fn(f, round(x), 284, round(fw), 150), serif(x, 466, f'{n} <tspan font-style="italic">{cap}</tspan>', 15.5)]
        b.append(f'<path d="M{p} 490H{w - p}" stroke="{RULE}"/>')
        b.append(text(p, 521, "Llama 3.1 8B explains each result in plain language, as a risk indicator rather than a diagnosis.", 15.5, "#3A3528"))
    return doc(w, h, "Research paper: PredictLab", PAPER_DESC, sheet(w, h) + "".join(b), f.sheet() +
               "@keyframes rg{0%{transform:scale(1);opacity:.8}70%,100%{transform:scale(2.6);opacity:0}}.ring{transform-box:fill-box;transform-origin:center;animation:rg 2.4s ease-out infinite}")


# ------------------------------------------------------------------ portfolio
SITE = "#2261E9"   # the portfolio's own background, so Neo's edges blend exactly
LINES = [("Hi, I’m Neo. I guide you", "through the work."), ("Live traces and receipts", "for every claim."), ("Ask me about loom.ai,", "LazyHire or PredictLab.")]
PORT_DESC = ("Portfolio: vinayakkv.com. I build agents that run real tools and cite their sources. "
             "Neo, the site's robot guide, floats, blinks and talks: live traces and receipts for every claim.")


def neo(x, y, h):
    """Cutout of the portfolio's robot, 740 x 1050 in its own units, with blinking eyes."""
    k = h / 1050
    data = base64.b64encode((ROOT / "assets/screens/web/neo.webp").read_bytes()).decode()
    lids = "".join(f'<ellipse cx="{cx}" cy="320" rx="{rx}" ry="45" fill="#10131B"/><rect x="{cx - rx + 6}" y="316" width="{2 * rx - 12}" height="8" rx="4" fill="#6FC3F7"/>'
                   for cx, rx in ((249, 38), (439, 43)))
    return (f'<g class="float"><g transform="translate({x} {y}) scale({k:.4f})"><defs><image id="neo" width="740" height="1050" href="data:image/webp;base64,{data}"/>'
            '<clipPath id="nb"><rect y="496" width="740" height="560"/></clipPath><clipPath id="nh"><path d="M0 0H740V470Q370 566 0 470Z"/></clipPath></defs>'
            '<g clip-path="url(#nb)"><use href="#neo"/></g>'
            f'<g class="headtilt"><g clip-path="url(#nh)"><use href="#neo"/></g><g class="lid">{lids}</g></g></g></g>')


def bubble(x, y, w, tail):
    css, out = "", [f'<rect x="{x + 6}" y="{y + 6}" width="{w}" height="78" rx="14" fill="#0B0B0B"/>',
                    f'<rect x="{x}" y="{y}" width="{w}" height="78" rx="14" fill="#FBFAF5" stroke="#0B0B0B" stroke-width="2.5"/>',
                    f'<path d="{tail}" fill="#FBFAF5" stroke="#0B0B0B" stroke-width="2.5" stroke-linejoin="round"/>']
    for i, pair in enumerate(LINES):
        a, e = i * 100 / 3, (i + 1) * 100 / 3
        edge = "0%{opacity:1}" if i == 0 else f"0%,{a:.1f}%{{opacity:0}}{a + 3:.1f}%{{opacity:1}}"
        end = f"{e - 3:.1f}%{{opacity:1}}{e:.1f}%{{opacity:0}}" + ("97%{opacity:0}100%{opacity:1}" if i == 0 else "100%{opacity:0}")
        css += f"@keyframes sp{i}{{{edge}{end}}}.sp{i}{{{'opacity:0;' if i else ''}animation:sp{i} 12s linear infinite}}"
        out.append(f'<g class="sp{i}">' + "".join(text(x + 20, y + 33 + j * 23, s, 16, "#0B0B0B", weight=500) for j, s in enumerate(pair)) + "</g>")
    css += ("@keyframes ht{0%,18%,100%{transform:rotate(0)}26%,46%{transform:rotate(-5deg)}56%,60%{transform:rotate(0)}68%,86%{transform:rotate(4deg)}}"
            ".headtilt{transform-origin:375px 515px;animation:ht 9s cubic-bezier(.5,0,.2,1) infinite}"
            "@keyframes bb{0%,28%,33.4%,61%,66.7%,95%,100%{transform:scale(1)}31.5%,65%,98.5%{transform:scale(1.05)}}.bub{transform-box:fill-box;transform-origin:right center;animation:bb 12s ease-in-out infinite}"
            "@keyframes na{0%,100%{transform:translate(0,0)}50%{transform:translate(3px,-3px)}}.na{animation:na 1.8s ease-in-out infinite}"
            "@keyframes fl{0%,100%{transform:translateY(0)}50%{transform:translateY(-9px)}}.float{animation:fl 4.6s ease-in-out infinite}"
            "@keyframes ld{0%,44%,48%,82%,86%,100%{opacity:0}45%,47%,83%,85%{opacity:1}}.lid{opacity:0;animation:ld 5.2s linear infinite}"
            "@keyframes sd{0%,100%{transform:scaleX(1);opacity:.35}50%{transform:scaleX(.86);opacity:.22}}.shade{transform-box:fill-box;transform-origin:center;animation:sd 4.6s ease-in-out infinite}")
    return f'<g class="bub">{"".join(out)}</g>', css


def portfolio(m=False):
    head = ["I build agents that", "run real tools and", "cite their sources."]
    w, h, p = (MW, 690, MP) if m else (W, 430, P)
    step = 57.6
    lines = "".join(f'<path d="M{i * step + (p if not m else 24):.1f} 0V{h}" stroke="#FFF" stroke-opacity=".10"/>' for i in range(int(w / step) + 1))
    if m:
        size, y0 = 37, 106
        nx, ny, nh = 152, 306, 372
        bub, css = bubble(MP, 290 - 50, 246, "M226 317L256 345L256 317Z")
        bx, by, bw = None, None, None
    else:
        size, y0 = 50, 176
        nx, ny, nh = 584, 48, 400
        bub, css = bubble(340, 42, 250, "M589 84L618 98L589 108Z")
    b = [f'<defs><clipPath id="pc"><rect width="{w}" height="{h}" rx="{R}"/></clipPath></defs><g clip-path="url(#pc)"><rect width="{w}" height="{h}" fill="{SITE}"/>{lines}',
         f'<ellipse class="shade" cx="{nx + nh * .352:.0f}" cy="{ny + nh * .985:.0f}" rx="{nh * .22:.0f}" ry="8" fill="#0B2A7A" opacity=".35"/>', neo(nx, ny, nh), "</g>"]
    b.append(text(p, 54 if not m else 50, "vinayakkv.com", 17, "#FFF", weight=600))
    b += [text(p, y0 + i * size * 1.06, s, size, "#FFF", weight=700, ls=-size * .034) for i, s in enumerate(head)]
    b.append(bub)
    if m:
        bx, by, bw, bh = MP, 614, 184, 50
    else:
        bx, by, bw, bh = P, 336, 196, 54
    b.append(f'<rect x="{bx}" y="{by}" width="{bw}" height="{bh}" rx="{bh / 2}" fill="#FBFAF5"/>'
             + text(bx + bw / 2 - 10, by + bh / 2 + 5.6, "Open portfolio", 16, "#0B0B0B", weight=600, anchor="middle") + f'<g class="na">{arrow(bx + bw - 24, by + bh / 2 - 5, "#0B0B0B", 10, 1.9)}</g>')
    return doc(w, h, "Portfolio: vinayakkv.com", PORT_DESC, "".join(b), css)
