#!/usr/bin/env python3
"""Generate about.svg - the About Me story, told twice.

    python tools/gen_about.py

First the panel types out `about.html` - the story as real markup, with the
emphasised phrases sitting in <em> tags. Once the file is fully written it is
"rendered": the code drops away and the same sentences fade up as prose, one
line at a time.

STORY below is the single source for both halves, so the code view and the
rendered view can never drift apart. Words wrapped in *asterisks* become <em>
in the markup and take the accent colour in the prose.
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

    "Then the models started talking back. *LLMs, retrieval, agents* that "
    "choose their own tools. I have been building there ever since: an "
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
HEADER_H = 46

# code half
CODE_LINE_H = 21
CODE_FS = 13
CODE_CH = 7.15          # monospace advance at CODE_FS
CODE_WRAP = 92          # visible characters per source line
GUTTER = 40

# prose half
PROSE_LINE_H = 30
PROSE_FS = 19
PROSE_WRAP = 80         # visible characters per rendered line
PROSE_X = 54

CARD_BG = "#070c1a"
PANE_BG = "#0a1122"
RULE = "#1e2a44"
INK = "#c3d0e2"
DIM = "#5d6b85"
FAINT = "#39445c"
ACCENT = "#4FD1E0"

TAG, ATTR, STR, TXT, GUT = "#7fb0e6", "#d7bd7a", "#8fbf8a", "#8896ad", "#2c3752"
SERIF = "Georgia,'Iowan Old Style','Palatino Linotype','Times New Roman',serif"
MONO = "'JetBrains Mono','Fira Code',Consolas,'Courier New',monospace"

# --------------------------------------------------------------------- timeline
LOOP = 24.0
TYPE_A, TYPE_B = 0.4, 10.0     # window the whole file is typed inside
CODE_OUT_A, CODE_OUT_B = 11.0, 11.8
PROSE_A = 11.6                 # first prose line starts arriving
PROSE_STEP = 0.16              # stagger between prose lines
PROSE_HOLD = 21.4              # prose starts leaving
PROSE_OUT = 22.9


def pct(seconds):
    return f"{seconds / LOOP * 100:.4g}%"


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def plain(paragraph):
    return paragraph.replace("*", "")


PUNCT = ".,;:!?)"


def glued(text):
    """True for tokens that must sit tight against the previous one"""
    return bool(text) and text[0] in PUNCT


# --------------------------------------------------------------------- tokenising
def marked_chunks(paragraph):
    """'a *b* c' -> [('a ', False), ('b', True), (' c', False)]"""
    return [(chunk, bool(i % 2))
            for i, chunk in enumerate(re.split(r"\*([^*]+)\*", paragraph))
            if chunk]


def wrap_tokens(tokens, width, indent, hang):
    """Greedy-wrap (text, kind) tokens into lines of rendered spans.

    Tokens join with a space, except that nothing separates a tag from the text
    it opens or closes - which is what makes the output read as real markup.
    """
    lines, cur, used = [], [], indent
    for text, kind in tokens:
        glue = not cur or kind == "close" or cur[-1][1] == "open" or glued(text)
        need = len(text) + (0 if glue else 1)
        if cur and used + need > width:
            lines.append(cur)
            cur, used, glue = [], hang, True
            need = len(text)
        if not glue:
            cur.append((" ", "text"))
        cur.append((text, kind))
        used += need
    if cur:
        lines.append(cur)
    return [[(" " * (indent if i == 0 else hang), "text")] + ln
            for i, ln in enumerate(lines)]


def html_lines():
    """The story as an about.html source listing: [[(text, kind), ...], ...]"""
    out = [[("<section", "sect"), (" class", "attr"), ("=", "sect"),
            ('"story"', "str"), (">", "sect")],
           [("  ", "text"), ("<h2>", "open"), (CHAPTER, "text"), ("</h2>", "close")],
           []]

    for paragraph in STORY:
        tokens = [("<p>", "open")]
        for chunk, is_em in marked_chunks(paragraph):
            words = chunk.split()
            if is_em:
                tokens.append(("<em>", "open"))
                tokens += [(w, "em") for w in words]
                tokens.append(("</em>", "close"))
            else:
                tokens += [(w, "text") for w in words]
        tokens.append(("</p>", "close"))
        out += wrap_tokens(tokens, CODE_WRAP, 2, 5)
        out.append([])

    out.append([("</section>", "sect")])
    return out


def prose_lines():
    """The story wrapped for the serif rendering: [[(text, is_em), ...], ...]"""
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


CODE = html_lines()
PROSE = prose_lines()

CODE_COLOUR = {"sect": TAG, "open": TAG, "close": TAG, "em": ACCENT,
               "attr": ATTR, "str": STR, "text": TXT}

# --------------------------------------------------------------------- geometry
CONTENT_TOP = HEADER_H + 20
CODE_H = len(CODE) * CODE_LINE_H + 26
PROSE_H = len(PROSE) * PROSE_LINE_H + 14
H = CONTENT_TOP + max(CODE_H, PROSE_H) + 62

CODE_X = PAD_X + GUTTER
CODE_Y = CONTENT_TOP + 24
PANE_W = W - 2 * PAD_X
COVER_W = PAD_X + PANE_W - CODE_X - 10   # stop the covers at the pane edge

# typing slots, apportioned by line length so long lines take longer
_typed = [i for i, ln in enumerate(CODE) if ln]
_chars = {i: sum(len(t) for t, _ in CODE[i]) for i in _typed}
_total = sum(_chars.values())
_gap = 0.05
_budget = (TYPE_B - TYPE_A) - _gap * (len(_typed) - 1)

SLOTS, _cursor = {}, TYPE_A
for _i in _typed:
    _span = _budget * _chars[_i] / _total
    SLOTS[_i] = (_cursor, _cursor + _span)
    _cursor += _span + _gap


# --------------------------------------------------------------------- css
def build_css():
    c = ['<style>',
         f".m{{font-family:{MONO}}}",
         f".ser{{font-family:{SERIF};font-style:italic}}"]

    # typewriter covers over each source line
    for i in _typed:
        s, e = SLOTS[i]
        n = _chars[i]
        c.append(
            f"@keyframes t{i}{{0%,{pct(s)}{{transform:translateX(0)}}"
            f"{pct(e)},{pct(CODE_OUT_A)}{{transform:translateX({n * CODE_CH:.1f}px)}}"
            f"{pct(CODE_OUT_B)},100%{{transform:translateX(0)}}}}")
        c.append(f".t{i}{{animation:t{i} {LOOP}s steps({n},end) infinite both}}")

    # the whole code half drops away once the file is written
    c.append(f"@keyframes cfade{{0%,{pct(CODE_OUT_A)}{{opacity:1}}"
             f"{pct(CODE_OUT_B)},100%{{opacity:0}}}}")
    c.append(f".cfade{{animation:cfade {LOOP}s ease infinite both}}")

    # caret rides down the file as it is written
    hops = [f"0%,{pct(TYPE_A)}{{transform:translate(0,0)}}"]
    for i in _typed:
        s, e = SLOTS[i]
        n = _chars[i]
        hops.append(f"{pct(s + 0.001)}{{transform:translate(0,{i * CODE_LINE_H}px)}}")
        hops.append(f"{pct(e)}{{transform:translate({n * CODE_CH:.1f}px,{i * CODE_LINE_H}px)}}")
    hops.append(f"{pct(CODE_OUT_B)},100%{{transform:translate(0,0)}}")
    c.append("@keyframes caret{" + "".join(hops) + "}")
    c.append(f".caret{{animation:caret {LOOP}s steps(1,end) infinite both}}")
    c.append("@keyframes blink{0%,45%{opacity:1}50%,95%{opacity:.08}100%{opacity:1}}")
    c.append(".blink{animation:blink 1.05s steps(1,end) infinite}")

    # rendered prose arrives exactly the way it always has
    c.append(f"@keyframes pin{{0%,{pct(PROSE_A)}{{opacity:0;transform:translateX(-12px)}}"
             f"{pct(PROSE_A + 0.6)}{{opacity:1;transform:translateX(0)}}"
             f"{pct(PROSE_HOLD)}{{opacity:1;transform:translateX(0)}}"
             f"{pct(PROSE_OUT)},100%{{opacity:0;transform:translateX(0)}}}}")
    c.append(f".pin{{opacity:0;animation:pin {LOOP}s ease-out infinite both}}")

    # hairline rule down the prose margin
    c.append(f"@keyframes grow{{0%,{pct(PROSE_A)}{{transform:scaleY(0)}}"
             f"{pct(PROSE_A + 0.9)},{pct(PROSE_HOLD)}{{transform:scaleY(1)}}"
             f"{pct(PROSE_OUT)},100%{{transform:scaleY(0)}}}}")
    c.append(f".grow{{transform-origin:0 {CONTENT_TOP}px;"
             f"animation:grow {LOOP}s cubic-bezier(.3,.8,.3,1) infinite both}}")

    # the tab label swaps from about.html to the rendered view
    c.append(f"@keyframes tabA{{0%,{pct(CODE_OUT_A)}{{opacity:1}}"
             f"{pct(CODE_OUT_B)},100%{{opacity:0}}}}")
    c.append(f"@keyframes tabB{{0%,{pct(CODE_OUT_A)}{{opacity:0}}"
             f"{pct(CODE_OUT_B)},100%{{opacity:1}}}}")
    c.append(f".tabA{{animation:tabA {LOOP}s ease infinite both}}")
    c.append(f".tabB{{opacity:0;animation:tabB {LOOP}s ease infinite both}}")
    c.append('</style>')
    return "".join(c)


# --------------------------------------------------------------------- pieces
def build_header():
    p = [f'<line x1="0" y1="{HEADER_H}" x2="{W}" y2="{HEADER_H}" stroke="{RULE}"/>']
    p.append(f'<circle cx="{PAD_X + 5}" cy="{HEADER_H / 2 - 1}" r="4" fill="{ACCENT}" '
             f'opacity="0.8"/>')
    p.append(f'<text class="m tabA" x="{PAD_X + 20}" y="{HEADER_H / 2 + 3}" font-size="12" '
             f'fill="{DIM}">about.html</text>')
    p.append(f'<text class="m tabB" x="{PAD_X + 20}" y="{HEADER_H / 2 + 3}" font-size="12" '
             f'fill="{DIM}">about.html — rendered</text>')
    p.append(f'<text class="m" x="{W - PAD_X}" y="{HEADER_H / 2 + 3}" font-size="11" '
             f'fill="{FAINT}" text-anchor="end" letter-spacing="2">'
             f'{esc(CHAPTER.upper())}</text>')
    return "".join(p)


def build_code():
    p = [f'<g class="cfade">']
    p.append(f'<rect x="{PAD_X}" y="{CONTENT_TOP}" width="{PANE_W}" height="{CODE_H}" '
             f'rx="8" fill="{PANE_BG}"/>')
    p.append(f'<line x1="{CODE_X - 14}" y1="{CONTENT_TOP + 10}" x2="{CODE_X - 14}" '
             f'y2="{CONTENT_TOP + CODE_H - 10}" stroke="{RULE}"/>')
    p.append(f'<g class="m" font-size="{CODE_FS}" clip-path="url(#pane)">')

    for i, spans in enumerate(CODE):
        y = CODE_Y + i * CODE_LINE_H
        p.append(f'<text x="{CODE_X - 24}" y="{y}" fill="{GUT}" font-size="10.5" '
                 f'text-anchor="end">{i + 1}</text>')
        if not spans:
            continue
        p.append(f'<text x="{CODE_X}" y="{y}" xml:space="preserve">')
        for text, kind in spans:
            p.append(f'<tspan fill="{CODE_COLOUR[kind]}">{esc(text)}</tspan>')
        p.append('</text>')
        p.append(f'<rect class="t{i}" x="{CODE_X}" y="{y - 14}" width="{COVER_W}" '
                 f'height="{CODE_LINE_H - 2}" fill="{PANE_BG}"/>')

    p.append('</g>')
    p.append(f'<g class="caret" transform="translate(0,0)">'
             f'<rect class="blink" x="{CODE_X}" y="{CODE_Y - 11}" width="7" height="14" '
             f'fill="{ACCENT}" opacity="0.85"/></g>')
    p.append('</g>')
    return "".join(p)


def build_prose():
    p = []
    p.append(f'<rect class="grow" x="{PROSE_X - 22}" y="{CONTENT_TOP}" width="2" '
             f'height="{len(PROSE) * PROSE_LINE_H}" rx="1" fill="{ACCENT}" opacity="0.5"/>')

    first_word = PROSE[0][0][0]
    baseline0 = CONTENT_TOP + 26

    # drop cap, set from the first letter of the story
    p.append(f'<text class="ser pin" x="{PROSE_X}" y="{baseline0 + 12}" font-size="48" '
             f'fill="{ACCENT}">{esc(first_word[0])}</text>')

    for i, spans in enumerate(PROSE):
        if not spans:
            continue
        y = baseline0 + i * PROSE_LINE_H
        x = PROSE_X + (32 if i == 0 else 0)
        delay = i * PROSE_STEP
        p.append(f'<text class="ser pin" x="{x}" y="{y}" font-size="{PROSE_FS}" fill="{INK}" '
                 f'style="animation-delay:{delay:.2f}s" xml:space="preserve">')
        for j, (text, is_em) in enumerate(spans):
            if i == 0 and j == 0:
                text = text[1:]     # the drop cap already stands in for this letter
            if is_em:
                p.append(f'<tspan fill="{ACCENT}" font-style="normal" '
                         f'font-weight="600">{esc(text)}</tspan>')
            else:
                p.append(f'<tspan>{esc(text)}</tspan>')
        p.append('</text>')

    cy = baseline0 + len(PROSE) * PROSE_LINE_H + 18
    p.append(f'<line class="pin" x1="{PROSE_X}" y1="{cy - 18}" x2="{PROSE_X + 110}" '
             f'y2="{cy - 18}" stroke="{RULE}" '
             f'style="animation-delay:{len(PROSE) * PROSE_STEP:.2f}s"/>')
    p.append(f'<text class="m pin" x="{PROSE_X}" y="{cy + 4}" font-size="12.5" fill="{DIM}" '
             f'style="animation-delay:{len(PROSE) * PROSE_STEP:.2f}s">{esc(CLOSER)}</text>')
    return "".join(p)


# --------------------------------------------------------------------- assemble
def main():
    label = esc(" ".join(plain(p) for p in STORY))
    s = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" '
         f'viewBox="0 0 {W} {H}" role="img" aria-label="{label}">']
    s.append(f'<defs><clipPath id="pane"><rect x="{PAD_X}" y="{CONTENT_TOP}" '
             f'width="{PANE_W}" height="{CODE_H}" rx="8"/></clipPath></defs>')
    s.append(build_css())
    s.append(f'<rect width="{W}" height="{H}" rx="12" fill="{CARD_BG}"/>')
    s.append(f'<rect width="{W}" height="{H}" rx="12" fill="none" stroke="{RULE}"/>')
    s.append(build_header())
    s.append(build_code())
    s.append(build_prose())
    s.append('</svg>')

    svg = "".join(s)
    OUT.write_text(svg, encoding="utf-8")
    print(f"wrote {OUT}  ({len(svg) / 1024:.1f} KB)  "
          f"{len(CODE)} source lines -> {len([l for l in PROSE if l])} prose lines")


if __name__ == "__main__":
    main()
