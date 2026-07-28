#!/usr/bin/env python3
"""Generate about.svg - the About Me story as prose.

    python tools/gen_about.py

Edit STORY below; everything else lays itself out. Words wrapped in *asterisks*
take the aurora gradient, which is the same violet -> cyan -> magenta ramp the
hero wordmark uses, so the two panels read as one design.

Like the hero, the entrance plays once rather than looping - a block of text
that fades itself out and back in every 20 seconds is unreadable.
"""

import re
from pathlib import Path

OUT = Path(__file__).resolve().parent.parent / "assets" / "about.svg"
OUT.parent.mkdir(parents=True, exist_ok=True)

# --------------------------------------------------------------------- content
CHAPTER = "01 — the story so far"

STORY = [
    "Every model I have ever built started the same way: a *messy dataset* "
    "and a question nobody had time to answer.",

    "So I learned to answer them *end to end* — not just the notebook and the "
    "accuracy score, but the pipeline feeding it, the API standing in front of "
    "it, and the container it ships inside.",

    "Then the models started talking back. *Models that reason, retrieve, and "
    "choose their own tools.* I have been building there ever since: an "
    "autonomous analyst that turns raw tables into business intelligence, a "
    "translator that turns plain English into SQL, a *multi-agent desk* that "
    "reads the market while I sleep.",

    "The thread has never changed — take something raw and unreadable, and "
    "hand back something a person can *actually act on*.",
]

CLOSER = "— still shipping, still curious"

# --------------------------------------------------------------------- style
W = 940
PAD_X = 30
HEADER_H = 44

PROSE_X = 62
PROSE_LINE_H = 31
PROSE_FS = 19
PROSE_WRAP = 78         # visible characters per rendered line

BASE = "#070b18"
CARD = "#0a1020"
RULE = "#1e293b"
INK = "#cbd5e1"
DIM = "#94a3b8"
FAINT = "#475569"

VIOLET = "#7C5CFF"
CYAN = "#22D3EE"
MAGENTA = "#F472B6"

SERIF = "Georgia,'Iowan Old Style','Palatino Linotype','Times New Roman',serif"
SANS = "'Segoe UI',Inter,'Helvetica Neue',Helvetica,Arial,sans-serif"

STEP = 0.13             # stagger between lines, seconds

PUNCT = ".,;:!?)"


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def plain(paragraph):
    return paragraph.replace("*", "")


def glued(text):
    """True for tokens that must sit tight against the previous one"""
    return bool(text) and text[0] in PUNCT


def marked_chunks(paragraph):
    """'a *b* c' -> [('a ', False), ('b', True), (' c', False)]"""
    return [(chunk, bool(i % 2))
            for i, chunk in enumerate(re.split(r"\*([^*]+)\*", paragraph))
            if chunk]


def prose_lines():
    """The story wrapped for the serif setting: [[(text, is_em), ...], ...]"""
    out = []
    for p, paragraph in enumerate(STORY):
        if p:
            out.append([])
        words = []
        for chunk, is_em in marked_chunks(paragraph):
            words += [(w, is_em) for w in chunk.split()]
        cur, used = [], 0
        for word, is_em in words:
            sep = "" if glued(word) else " "
            need = len(word) + (len(sep) if cur else 0)
            if cur and used + need > PROSE_WRAP:
                out.append(cur)
                cur, used, sep, need = [], 0, "", len(word)
            if cur and cur[-1][1] == is_em:
                cur[-1] = (cur[-1][0] + sep + word, is_em)
            else:
                if cur and sep:
                    cur.append((sep, cur[-1][1]))
                cur.append((word, is_em))
            used += need
        out.append(cur)
    return out


PROSE = prose_lines()

CONTENT_TOP = HEADER_H + 22
BASELINE0 = CONTENT_TOP + 24
H = BASELINE0 + len(PROSE) * PROSE_LINE_H + 58


def build_defs():
    return (
        "<defs>"
        '<linearGradient id="em" gradientUnits="userSpaceOnUse" '
        f'x1="{PROSE_X}" y1="0" x2="{W - PAD_X}" y2="0">'
        f'<stop offset="0%" stop-color="{VIOLET}"/>'
        f'<stop offset="45%" stop-color="{CYAN}"/>'
        f'<stop offset="100%" stop-color="{MAGENTA}"/>'
        "</linearGradient>"
        '<linearGradient id="spine" x1="0" y1="0" x2="0" y2="1">'
        f'<stop offset="0%" stop-color="{VIOLET}" stop-opacity="0"/>'
        f'<stop offset="20%" stop-color="{VIOLET}" stop-opacity="0.9"/>'
        f'<stop offset="60%" stop-color="{CYAN}" stop-opacity="0.8"/>'
        f'<stop offset="100%" stop-color="{MAGENTA}" stop-opacity="0"/>'
        "</linearGradient>"
        "</defs>")


def build_css():
    return (
        "<style>"
        f".ser{{font-family:{SERIF};font-style:italic}}"
        f".s{{font-family:{SANS}}}"
        "@keyframes fin{from{opacity:0;transform:translateX(-14px)}"
        "to{opacity:1;transform:translateX(0)}}"
        ".fin{opacity:0;animation:fin .75s cubic-bezier(.2,.7,.3,1) both}"
        "@keyframes tall{from{transform:scaleY(0)}to{transform:scaleY(1)}}"
        f".tall{{transform-origin:0 {CONTENT_TOP}px;"
        "animation:tall 1.2s cubic-bezier(.2,.8,.25,1) both}"
        "</style>")


def main():
    label = esc(" ".join(plain(p) for p in STORY))
    s = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" '
         f'viewBox="0 0 {W} {H}" role="img" aria-label="{label}">']
    s.append(build_defs())
    s.append(build_css())

    s.append(f'<rect width="{W}" height="{H}" rx="16" fill="{CARD}"/>')
    s.append(f'<rect width="{W}" height="{H}" rx="16" fill="none" stroke="{RULE}"/>')

    # header
    s.append(f'<circle cx="{PAD_X + 14}" cy="{HEADER_H / 2 + 2}" r="4" fill="{CYAN}" '
             f'opacity="0.9"/>')
    s.append(f'<text class="s" x="{PAD_X + 28}" y="{HEADER_H / 2 + 6}" font-size="11.5" '
             f'fill="{FAINT}" letter-spacing="2.4">{esc(CHAPTER.upper())}</text>')
    s.append(f'<line x1="{PAD_X}" y1="{HEADER_H}" x2="{W - PAD_X}" y2="{HEADER_H}" '
             f'stroke="{RULE}"/>')

    # gradient spine down the margin
    s.append(f'<rect class="tall" x="{PROSE_X - 26}" y="{CONTENT_TOP}" width="2.5" '
             f'height="{len(PROSE) * PROSE_LINE_H}" rx="1.25" fill="url(#spine)"/>')

    # drop cap
    first_word = PROSE[0][0][0]
    s.append(f'<text class="ser fin" x="{PROSE_X}" y="{BASELINE0 + 13}" font-size="50" '
             f'fill="url(#em)" style="animation-delay:.1s">{esc(first_word[0])}</text>')

    for i, spans in enumerate(PROSE):
        if not spans:
            continue
        y = BASELINE0 + i * PROSE_LINE_H
        x = PROSE_X + (34 if i == 0 else 0)
        s.append(f'<text class="ser fin" x="{x}" y="{y}" font-size="{PROSE_FS}" '
                 f'fill="{INK}" style="animation-delay:{0.15 + i * STEP:.2f}s" '
                 f'xml:space="preserve">')
        for j, (text, is_em) in enumerate(spans):
            if i == 0 and j == 0:
                text = text[1:]     # the drop cap already stands in for this letter
            if is_em:
                s.append(f'<tspan fill="url(#em)" font-style="normal" '
                         f'font-weight="600">{esc(text)}</tspan>')
            else:
                s.append(f'<tspan>{esc(text)}</tspan>')
        s.append("</text>")

    cy = BASELINE0 + len(PROSE) * PROSE_LINE_H + 20
    delay = 0.15 + len(PROSE) * STEP
    s.append(f'<line class="fin" x1="{PROSE_X}" y1="{cy - 18}" x2="{PROSE_X + 110}" '
             f'y2="{cy - 18}" stroke="{RULE}" style="animation-delay:{delay:.2f}s"/>')
    s.append(f'<text class="s fin" x="{PROSE_X}" y="{cy + 4}" font-size="12.5" '
             f'fill="{DIM}" style="animation-delay:{delay:.2f}s">{esc(CLOSER)}</text>')

    s.append("</svg>")

    svg = "".join(s)
    OUT.write_text(svg, encoding="utf-8")
    print(f"wrote {OUT}  ({len(svg) / 1024:.1f} KB)  {len([l for l in PROSE if l])} lines")


if __name__ == "__main__":
    main()
