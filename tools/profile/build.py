#!/usr/bin/env python3
"""Build every static profile panel, desktop and compact. Standard library only.

    python tools/profile/build.py

Project films live in scenes.py, the paper and portfolio cards in pages.py. The contribution panel lives
in activity.py because it needs live data.
"""
import math
import sys
from pathlib import Path

import pages
import scenes
from theme import MATRIX_CSS, V, W, MW, P, MP, R, arrow, cover, doc, esc, glyph, hline, matrix, surface, text, tw

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "assets/svg"
sys.path.insert(0, str(ROOT / "scripts"))
from generate_butterfly import flying, smooth  # noqa: E402  (shared with the standalone assets/butterfly.svg)

PING = ("@keyframes ping{0%{transform:scale(1);opacity:.9}70%,100%{transform:scale(2.6);opacity:0}}"
        ".ping{transform-box:fill-box;transform-origin:center;animation:ping 2.8s ease-out infinite}")

# ------------------------------------------------------------------ hero: pure black in both themes, behind the butterfly
NAME = "VINAYAK"
LOOP = ["route", "execute", "verify", "cite", "trace"]
CYCLE = 10
INK, SUB, DIM = "#F4F5F6", "#B4B8C0", "#8D929B"
HERO_DESC = ("VINAYAK, AI/ML Engineer at AMnova Technologies, Kochi, India. AI systems that show their work: "
             "agents that run real tools, answers that cite or abstain. Agent loop: route, execute, verify, cite, trace. "
             "HackerRank Orchestrate finalist. A butterfly drawn in white and violet dots flies across the banner behind the text, trailing violet stardust.")


def hero_card(w, h):
    return (f'<defs><clipPath id="hk"><rect x="1" y="1" width="{w - 2}" height="{h - 2}" rx="{R - 1}"/></clipPath></defs>'
            f'<rect x=".5" y=".5" width="{w - 1}" height="{h - 1}" rx="{R}" fill="#000" stroke="#FFF" stroke-opacity=".14"/>')


def name_block(x, y, size, ls):
    span = tw(NAME, size, weight=600) + 40
    defs = (f'<linearGradient id="ng" x1="0" y1="{y - size * .72:.0f}" x2="0" y2="{y}" gradientUnits="userSpaceOnUse">'
            '<stop stop-color="#FFFFFF"/><stop offset="1" stop-color="#B9BDC8"/></linearGradient>'
            f'<linearGradient id="sheen" x1="0" y1="0" x2="{size * 2.6:.0f}" y2="0" gradientUnits="userSpaceOnUse">'
            '<stop stop-color="#B9A6FB" stop-opacity="0"/><stop offset=".5" stop-color="#B9A6FB" stop-opacity=".85"/>'
            '<stop offset="1" stop-color="#B9A6FB" stop-opacity="0"/>'
            f'<animateTransform attributeName="gradientTransform" type="translate" dur="12s" repeatCount="indefinite" '
            f'values="{x - size * 3:.0f} 0;{x - size * 3:.0f} 0;{x + span:.0f} 0;{x + span:.0f} 0" keyTimes="0;.6;.8;1"/>'
            '</linearGradient>')
    body = (text(x, y, NAME, size, "url(#ng)", weight=600, ls=ls)
            + text(x, y, NAME, size, "url(#sheen)", weight=600, ls=ls, cls="motion"))
    return f"<defs>{defs}</defs>{body}"


def statement(x, y, size, before, accent="", after="", fill=INK):
    """Sans headline with one italic serif accent, like editorial poster type."""
    serif = (f'<tspan class="f" font-style="italic" font-weight="400" letter-spacing="0">{esc(accent)}</tspan>' if accent else "")
    return (f'<text x="{x}" y="{y}" class="s" font-size="{size}" fill="{fill}" font-weight="500" letter-spacing="-.5">'
            f'{esc(before)}{serif}{esc(after)}</text>')


def loop_chips(x, y, max_w, gap=8, h=30):
    """The agent loop as neutral chips; a soft light steps through them in order."""
    out, cx, cy = [], x, y
    for i, label in enumerate(LOOP):
        w = tw(label, 13, weight=500) + 26
        if cx > x and cx + w > x + max_w:
            cx, cy = x, cy + h + gap
        out.append(f'<g><rect class="lp{i}" x="{cx:.1f}" y="{cy}" width="{w:.1f}" height="{h}" rx="{h / 2}" fill="#FFF" fill-opacity=".09" '
                   f'stroke="#FFF" stroke-opacity=".16"/>{text(cx + w / 2, cy + h / 2 + 4.6, label, 13, INK, weight=500, anchor="middle")}</g>')
        cx += w + gap
    css = "@keyframes lp{0%,24%,100%{fill:#FFF;fill-opacity:.09;stroke-opacity:.16}6%,12%{fill:#A78BFA;fill-opacity:.42;stroke-opacity:.5}}"
    css += "".join(f".lp{i}{{animation:lp {CYCLE}s ease-in-out {i * CYCLE / 5:.1f}s infinite}}" for i in range(5))
    return "".join(out), css, cy + h


ROLL = ["show their work.", "run real tools.", "cite or abstain.", "fail over, not out."]


def roller(x, y, size, uid="rl"):
    """Second headline line: four true endings turn over like a departure board, then rest on the first."""
    n, step, hold = len(ROLL), size * 1.5, 100 / len(ROLL)
    frames = ""
    for i in range(n + 1):
        a, b = i * hold, (i + .82) * hold
        frames += f"{a:.2f}%{{transform:translateY({-i * step:.1f}px)}}" + (f"{b:.2f}%{{transform:translateY({-i * step:.1f}px)}}" if i < n else "")
    lines = "".join(f'<text x="{x}" y="{y + i * step:.1f}" class="f" font-style="italic" font-size="{size}" fill="{"#C9BBFF" if i % n == 0 else INK}">{esc(t)}</text>'
                    for i, t in enumerate(ROLL + ROLL[:1]))
    css = f"@keyframes {uid}{{{frames}}}.{uid}{{animation:{uid} 14s cubic-bezier(.7,0,.2,1) infinite}}"
    return (f'<defs><clipPath id="{uid}c"><rect x="{x - 8}" y="{y - size * 1.02:.1f}" width="620" height="{size * 1.38:.1f}"/></clipPath>'
            f'<linearGradient id="{uid}g" x1="0" y1="0" x2="0" y2="1"><stop stop-color="#000"/><stop offset=".1" stop-color="#FFF"/><stop offset=".9" stop-color="#FFF"/><stop offset="1" stop-color="#000"/></linearGradient>'
            f'<mask id="{uid}m" maskUnits="userSpaceOnUse" x="{x - 8}" y="{y - size * .88:.1f}" width="620" height="{size * 1.3:.1f}"><rect x="{x - 8}" y="{y - size * .88:.1f}" width="620" height="{size * 1.3:.1f}" fill="url(#{uid}g)"/></mask></defs>'
            f'<g mask="url(#{uid}m)"><g class="{uid}">{lines}</g></g>'), css


def hero_desktop():
    w, h = W, 470
    # Figure-eight over the whole card: near and bright on the right, small and dim behind the text.
    bcss, art = flying(lambda u: (440 + 320 * math.sin(2 * math.pi * u + math.pi / 2) + 14 * math.sin(6 * math.pi * u),
                                  220 + 125 * math.sin(4 * math.pi * u) + 16 * math.sin(10 * math.pi * u + 1)),
                       lambda x, y: smooth((x - 260) / 480), w, h, (690, 200, .52))
    chips, tcss, _ = loop_chips(P, 356, 520)
    roll, rcss = roller(P, 286, 52)
    b = [hero_card(w, h), f'<g clip-path="url(#hk)">{art}</g>', name_block(P, 82, 38, 3),
         f'<text x="{P}" y="116" class="s" font-size="18"><tspan fill="{INK}" font-weight="500">AI/ML Engineer</tspan>'
         f'<tspan fill="{SUB}"> at AMnova Technologies</tspan></text>',
         text(P, 222, "AI systems that", 56, INK, weight=600, ls=-1.8), roll,
         chips, '<path d="M36 414H844" stroke="#FFF" stroke-opacity=".12"/>',
         text(P, 444, "Kochi, India", 14, DIM), text(w - P, 444, "HackerRank Orchestrate finalist", 14, DIM, anchor="end")]
    return doc(w, h, "VINAYAK — AI/ML Engineer", HERO_DESC, "".join(b), bcss + tcss + rcss)


def hero_compact():
    w = MW
    chips, tcss, ty = loop_chips(MP, 478, w - 2 * MP)
    h = ty + 82
    # Vertical figure-eight: near at the top where the art sits, far as it sinks behind the text.
    bcss, art = flying(lambda u: (200 + 120 * math.sin(4 * math.pi * u) + 10 * math.sin(6 * math.pi * u),
                                  h * .42 - h * .32 * math.cos(2 * math.pi * u)),
                       lambda x, y: smooth((h * .5 - y) / (h * .38)), w, h, (200, 118, .4))
    roll, rcss = roller(MP, 428, 37)
    b = [hero_card(w, h), f'<g clip-path="url(#hk)">{art}</g>', name_block(MP, 264, 32, 2.5),
         text(MP, 296, "AI/ML Engineer", 17, INK, weight=500), text(MP, 320, "AMnova Technologies, Kochi, India", 15.5, SUB),
         text(MP, 384, "AI systems that", 41, INK, weight=600, ls=-1.2), roll,
         chips, f'<path d="M{MP} {ty + 24}H{w - MP}" stroke="#FFF" stroke-opacity=".12"/>',
         text(MP, ty + 53, "HackerRank Orchestrate finalist", 14.5, DIM)]
    return doc(w, h, "VINAYAK — AI/ML Engineer", HERO_DESC, "".join(b), bcss + tcss + rcss)


# ------------------------------------------------------------------ proof band: four verified numbers roll into place
PROOF = [("44%", "less time to first token", "loom.ai, 8.9s to 5.0s", "blue"), ("10", "specialist agents", "with human approval", "violet"),
         ("18/20", "correct SQL answers", "NL2SQL, own benchmark", "amber"), ("1", "published paper", "Zenodo DOI, sole author", "green")]


def odometer(x, y, value, size, color, uid):
    """Digits spin up once and stop; without animation they already rest on the true value."""
    out, css, cx = [], "", x
    for k, ch in enumerate(value):
        if ch.isdigit():
            n = int(ch)
            col = "".join(f'<text x="{cx + size * .28:.1f}" y="{y + (d - 10 - n) * size * 1.2:.1f}" class="s" font-size="{size}" font-weight="600" '
                          f'text-anchor="middle" fill="{color}">{d % 10}</text>' for d in range(n, n + 11))
            c = f"{uid}{k}"
            css += (f"@keyframes {c}{{from{{transform:translateY({12 * size:.0f}px)}}to{{transform:none}}}}"
                    f".{c}{{animation:{c} {1.6 + .25 * k:.2f}s cubic-bezier(.16,1,.3,1) .3s backwards}}")
            out.append(f'<g class="{c}">{col}</g>')
        else:
            out.append(text(cx + (size * .06 if ch == "%" else 0), y, ch, size, color, weight=600))
        cx += size * (.57 if ch.isdigit() else .42)
    return (f'<defs><clipPath id="{uid}c"><rect x="{x - 4}" y="{y - size * .9:.1f}" width="{cx - x + size * .6:.0f}" height="{size * 1.06:.1f}"/></clipPath></defs>'
            f'<g clip-path="url(#{uid}c)">{"".join(out)}</g>'), css


def proof(m=False):
    b, css = [], ""
    w, h = (MW, 316) if m else (W, 178)
    for i, (v, a, sub, hue) in enumerate(PROOF):
        if m:
            x, y, size = MP + (i % 2) * 184, 78 + (i // 2) * 146, 52
        else:
            x, y, size = P + i * 208, 86, 58
        o, c = odometer(x, y, v, size, V[hue], f"o{i}")
        css += c
        b += [o, text(x, y + 34, a, 16, V["text"], weight=600), text(x, y + 56, sub, 13.5, V["text3"])]
    desc = "; ".join(f"{v} {a} ({sub})" for v, a, sub, _ in PROOF)
    return doc(w, h, "Measured results", desc, surface(w, h) + "".join(b), css)


# ------------------------------------------------------------------ expertise
FOCUS = [
    ("blue", "prompt", "Agent systems", "loom.ai",
     ["Tool execution in a real Linux", "sandbox; model routing with", "provider fallback."],
     ["Tool execution in a real Linux sandbox;", "model routing with provider fallback."]),
    ("green", "cite", "Grounded generation", "loom.ai, lazyhire",
     ["Answers that cite sources or", "abstain; CV drafts checked", "for invented claims."],
     ["Answers that cite sources or abstain;", "CV drafts checked for invented claims."]),
    ("amber", "bars", "Applied ML", "InForge-AI, InsightGenie",
     ["Cleaning, EDA and model", "benchmarking, with local", "fallbacks when LLMs fail."],
     ["Cleaning, EDA and model benchmarking,", "with local fallbacks when LLMs fail."]),
]
PRINCIPLES = [("bolt", "Deterministic core"), ("target", "Cite or abstain"), ("refresh", "Fail over, not out"), ("doc", "Documented limits")]


def expertise(m=False):
    b = []
    if m:
        w, ch, gap = MW, 174, 12
        for i, (hue, ic, title, ev, _, lines) in enumerate(FOCUS):
            y = i * (ch + gap)
            b += [surface(w, ch, 0, y, 20), matrix(ic, MP + 2, y + 26, V[hue], 3.6),
                  text(MP + 58, y + 50, title, 20, V["text"], weight=600, ls=-.3)]
            b += [text(MP, y + 94 + j * 22, s, 15.5, V["text2"]) for j, s in enumerate(lines)]
            b.append(text(MP, y + 150, f"Shown in {ev}", 13.5, V["text3"]))
        y0 = 3 * (ch + gap)
        b.append(surface(w, 92, 0, y0, 20))
        for i, (ic, label) in enumerate(PRINCIPLES):
            x, y = MP + (i % 2) * 184, y0 + 39 + (i // 2) * 30
            b += [glyph(ic, x + 6, y - 5, V["text3"], 1.5, 1.4), text(x + 22, y, label, 14.5, V["text2"])]
        h = y0 + 92
    else:
        gap, ch, w = 14, 236, W
        cw = (W - 2 * gap) / 3
        for i, (hue, ic, title, ev, lines, _) in enumerate(FOCUS):
            x = i * (cw + gap)
            b += [surface(cw, ch, x, 0, 20), matrix(ic, x + 26, 30, V[hue], 4),
                  text(x + 24, 112, title, 20, V["text"], weight=600, ls=-.3)]
            b += [text(x + 24, 140 + j * 21, s, 14.5, V["text2"]) for j, s in enumerate(lines)]
            b.append(text(x + 24, 212, f"Shown in {ev}", 13, V["text3"]))
        b.append(surface(w, 54, 0, ch + gap, 20))
        seg = w / len(PRINCIPLES)
        for i, (ic, label) in enumerate(PRINCIPLES):
            x = i * seg + (seg - 24 - tw(label, 14)) / 2
            b += [glyph(ic, x + 7, ch + gap + 27, V["text3"], 1.5, 1.4), text(x + 24, ch + gap + 32, label, 14, V["text2"])]
        h = ch + gap + 54
    desc = " ".join(f"{title} ({ev}): {' '.join(lines)}" for _, _, title, ev, _, lines in FOCUS)
    desc += " Principles: " + ", ".join(p for _, p in PRINCIPLES) + "."
    return doc(w, h, "Engineering expertise", desc, "".join(b), MATRIX_CSS)


# ------------------------------------------------------------------ stack
STACK = [
    ("AI / ML", ["pandas", "NumPy", "scikit-learn", "XGBoost"]),
    ("LLMs and agents", ["LangGraph", "CrewAI", "LlamaIndex", "Vanna 2.0", "OpenAI SDK"]),
    ("Model APIs", ["Groq", "Gemini", "OpenRouter"]),
    ("Backend", ["Python", "FastAPI", "WebSockets", "Pydantic"]),
    ("Frontend", ["TypeScript", "Next.js", "React", "Tailwind CSS"]),
    ("Data", ["PostgreSQL", "Supabase", "pgvector", "SQLite", "Drizzle"]),
    ("Cloud and delivery", ["E2B", "Docker", "GitHub Actions", "Playwright", "Vercel", "Render"]),
]


def wrap_tokens(items, width, sep_w):
    rows, row, used = [], [], 0
    for item, wd in items:
        need = wd if not row else used + sep_w + wd
        if row and need > width:
            rows.append(row)
            row, need = [], wd
        row.append((item, wd))
        used = need
    return rows + [row] if row else rows


def stack(m=False):
    b = []
    if m:
        w, y = MW, 8
        for i, (group, items) in enumerate(STACK):
            if i:
                b.append(hline(MP, y + 14, w - MP))
            y += 44
            b.append(text(MP, y, group, 14.5, V["text3"]))
            for row in wrap_tokens([(s, tw(s, 18, weight=600)) for s in items], w - 2 * MP, 20):
                y += 30
                x = MP
                for s, wd in row:
                    b.append(text(x, y, s, 18, V["text"], weight=500))
                    x += wd + 20
        h = y + 32
    else:
        w, rh, top = W, 58, 14
        h = top * 2 + rh * len(STACK)
        for i, (group, items) in enumerate(STACK):
            y = top + i * rh
            if i:
                b.append(hline(P, y, w - P))
            b.append(text(P, y + rh / 2 + 5, group, 14.5, V["text3"]))
            x = 210
            for s in items:
                b.append(text(x, y + rh / 2 + 6.5, s, 18, V["text"], weight=500))
                x += tw(s, 18, weight=600) + 20
    desc = "; ".join(f"{g}: {', '.join(items)}" for g, items in STACK)
    return doc(w, h, "Tech stack", desc, surface(w, h) + "".join(b))


# ------------------------------------------------------------------ contact
EMAIL = "vinayakkvjob@gmail.com"


def button(x, y, w, h):
    return (f'<rect x="{x:.1f}" y="{y}" width="{w:.1f}" height="{h}" rx="{h / 2}" fill="#FFF"/>'
            + text(x + w / 2 - 9, y + h / 2 + 5.2, EMAIL, 15, "#0D0D0D", weight=600, anchor="middle")
            + f'<g class="na">{arrow(x + w - 24, y + h / 2 - 5, "#0D0D0D", 10, 1.8)}</g>')


# The lights behind the contact copy drift slowly, like an aurora; the button catches a sheen.
DRIFT = ("".join(f"@keyframes d{i}{{to{{transform:translate({x}px,{y}px) scale({s})}}}}.dr{i}{{transform-box:fill-box;transform-origin:center;animation:d{i} {t}s ease-in-out infinite alternate}}"
                 for i, (x, y, s, t) in enumerate(((150, 30, 1.2, 9), (-190, 46, 1.15, 11), (-160, -40, 1.25, 13), (220, -34, 1.3, 10))))
         + "@keyframes na{0%,100%{transform:translate(0,0)}50%{transform:translate(3px,-3px)}}.na{animation:na 1.8s ease-in-out infinite}")


def contact(m=False):
    live = lambda x, y: (f'<circle cx="{x}" cy="{y}" r="4" fill="#7EF0B0"/>'
                         f'<circle class="ping motion" cx="{x}" cy="{y}" r="4" fill="none" stroke="#7EF0B0"/>')
    if m:
        w, h = MW, 276
        b = [statement(MP, 66, 30, "Let’s build AI that", fill="#FFF"), statement(MP, 102, 30, "", "shows its work.", fill="#FFF"),
             live(MP + 5, 141), text(MP + 20, 146, "Open to AI/ML roles", 17, "#FFF", weight=500),
             button(MP, 190, w - 2 * MP, 52)]
    else:
        w, h = W, 200
        b = [statement(P, 92, 31, "Let’s build AI that ", "shows its work.", fill="#FFF"),
             live(P + 5, 130), text(P + 20, 136, "Open to AI/ML roles", 18, "#FFF", weight=500),
             button(w - P - 262, 74, 262, 52)]
    # A soft dark field behind the copy keeps white text readable on the brighter lights.
    veil = (f'<defs><linearGradient id="vl" x1="0" y1="0" x2="1" y2="0"><stop stop-color="#140A3C" stop-opacity=".62"/>'
            f'<stop offset="{1 if m else .75}" stop-color="#140A3C" stop-opacity="{.4 if m else 0}"/></linearGradient></defs>'
            f'<rect width="{w}" height="{h}" fill="url(#vl)"/>')
    return doc(w, h, "Contact", "Let’s build AI that shows its work. Open to AI/ML roles. "
               f"Email {EMAIL}.", cover(0, 0, w, h, "violet", veil, rx=R) + "".join(b), PING + DRIFT)


# ------------------------------------------------------------------ link buttons
LINKS = {"resume": ("Resume", "doc", True), "portfolio": ("Portfolio", "globe", False), "linkedin": ("LinkedIn", "linkedin", False), "email": ("Email", "mail", False)}


def link_button(key):
    label, ic, primary = LINKS[key]
    h = 36
    tx = tw(label, 14, weight=600)
    w = math.ceil(tx + 50)
    fill, ink, line = (V["inv"], V["invtext"], V["inv"]) if primary else (V["bg"], V["text"], V["line"])
    body = (f'<rect x=".5" y=".5" width="{w - 1}" height="{h - 1}" rx="{(h - 1) / 2}" fill="{fill}" stroke="{line}"/>'
            + glyph(ic, 21, h / 2, ink, 1.75, 1.5) + text(34 + tx / 2, h / 2 + 5, label, 14, ink, weight=600, anchor="middle"))
    return doc(w + 3, h, label, label, body)  # 3 px of air, so buttons need no &nbsp; between them


# ------------------------------------------------------------------
def main():
    OUT.mkdir(parents=True, exist_ok=True)
    responsive = {"hero": lambda m: hero_compact() if m else hero_desktop(), "expertise": expertise,
                  "proof": proof, "card-loom": scenes.loom, "card-lazyhire": scenes.lazyhire, "card-inforge": scenes.inforge,
                  "card-paper": pages.paper, "card-portfolio": pages.portfolio, "stack": stack, "contact": contact}
    out = {f'{name}{"-compact" if m else ""}': render(m) for name, render in responsive.items() for m in (False, True)}
    out.update({f"link-{key}": link_button(key) for key in LINKS})
    for name, svg in out.items():
        (OUT / f"{name}.svg").write_text(svg, encoding="utf-8")
    print(f"Built {len(out)} profile assets.")


if __name__ == "__main__":
    main()
