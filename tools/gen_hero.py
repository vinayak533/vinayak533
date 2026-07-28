#!/usr/bin/env python3
"""Generate hero.svg - a full-width terminal that types a short program, runs it,
and prints AI/ML ENGINEER as the program's own output.

    python tools/gen_hero.py

Deliberately quiet: one accent colour, hairline rules, no glow filters, no
ambient rain / particles / scanlines. Everything is CSS @keyframes so it
animates inside a GitHub README (camo serves the raw SVG untouched).
"""

from pathlib import Path

OUT = Path(__file__).resolve().parent.parent / "assets" / "hero.svg"
OUT.parent.mkdir(parents=True, exist_ok=True)

W, H = 1040, 430
LOOP = 20.0  # seconds, whole timeline

# terminal window
TX, TY, TW, TH = 16, 14, 1008, 402
BAR = 32  # title bar height

# code block
CODE_X = 78     # where the code text starts (after the line-number gutter)
CODE_Y = 78     # first baseline
LINE_H = 22
FS = 13.5
CH = 7.42       # monospace advance width at FS

# stdout block that holds the headline
BOX_Y = 268
BOX_H = 88
HEAD_FS = 46
HEAD_ADV = 37.5   # per-character advance, incl. the extra letter-spacing
BOX_PAD_X = 42

# ------------------------------------------------------------------- palette
PAGE_BG = "#05091a"
TERM_BG = "#080d1c"
BAR_BG = "#0d1424"
PANE_BG = "#0a1122"
RULE = "#1e2a44"
INK = "#c9d5e6"
DIM = "#5d6b85"
FAINT = "#39445c"
ACCENT = "#4FD1E0"

# syntax, all desaturated so the accent stays the only bright thing
K, ID, FN, ST, NU, CM, CL, PR, GUT = (
    "#9d8ad4", "#a8b6cc", "#7fb0e6", "#8fbf8a",
    "#d3a06a", "#465272", "#d7bd7a", ACCENT, "#2c3752",
)

LINES = [
    [("$ ", PR), ("cat engineer.py", ID)],
    [("from ", K), ("pipeline ", ID), ("import ", K), ("Dataset, Model", CL)],
    [("from ", K), ("serving ", ID), ("import ", K), ("API, Container", CL)],
    [("# train it, ship it, then let it introduce itself", CM)],
    [("model ", FN), ("= ", ID), ("Model", CL), ("(arch=", ID), ('"transformer"', ST),
     (", params=", ID), ('"7B"', ST), (")", ID)],
    [("model", FN), (".fit(", ID), ("Dataset", CL), (".load(", ID), ('"corpus"', ST),
     ("), epochs=", ID), ("12", NU), (")", ID)],
    [("API", CL), ("(model).serve(", ID), ("Container", CL), ("(gpu=", ID),
     ("True", NU), ("))", ID)],
    [("print", FN), ("(model.title.upper())", ID)],
    [("$ ", PR), ("python engineer.py", ID)],
]

# (start, end) seconds for the typewriter reveal of each line
TYPE_SLOTS = [
    (0.30, 1.00), (1.10, 2.05), (2.10, 2.95), (3.00, 3.95),
    (4.00, 5.05), (5.10, 6.05), (6.10, 6.95), (7.00, 7.70),
    (7.80, 8.45),
]
BOX_A, BOX_B = 8.7, 9.5        # stdout frame draws itself
CHAR_A = 9.4                   # headline characters start fading up
RULE_A, RULE_B = 11.2, 11.9    # accent rule wipes in
HOLD_B = 17.0                  # everything starts leaving
EXIT_B = 18.4
ERASE_A, ERASE_B = 17.6, 18.6  # code un-types

HEADLINE = "AI/ML ENGINEER"

out = []
a = out.append


def pct(seconds):
    """seconds on the master loop -> keyframe percentage string"""
    return f"{seconds / LOOP * 100:.4g}%"


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


# --------------------------------------------------------------------- geometry
BOX_W = len(HEADLINE) * HEAD_ADV + BOX_PAD_X * 2
BOX_X = TX + (TW - BOX_W) / 2


# --------------------------------------------------------------------- defs / css
def build_defs():
    d = ['<defs>']
    d.append(f'<clipPath id="screen"><rect x="{TX}" y="{TY + BAR}" width="{TW}" '
             f'height="{TH - BAR}" rx="4"/></clipPath>')
    d.append(f'<clipPath id="codeclip"><rect x="{TX + 20}" y="{TY + BAR + 4}" '
             f'width="760" height="{len(LINES) * LINE_H + 12}"/></clipPath>')
    d.append('</defs>')
    return "".join(d)


def build_css():
    c = ['<style>',
         ".m{font-family:'JetBrains Mono','Fira Code',Consolas,'Courier New',monospace}"]

    # ---- typewriter covers: a solid rect slides right, uncovering the line
    for i, (s, e) in enumerate(TYPE_SLOTS):
        n = sum(len(t) for t, _ in LINES[i])
        c.append(
            f"@keyframes t{i}{{"
            f"0%,{pct(s)}{{transform:translateX(0)}}"
            f"{pct(e)},{pct(ERASE_A)}{{transform:translateX({n * CH:.1f}px)}}"
            f"{pct(ERASE_B)},100%{{transform:translateX(0)}}}}")
        c.append(f".t{i}{{animation:t{i} {LOOP}s steps({n},end) infinite both}}")

    # ---- caret hops from line to line as the typing advances
    hops = [f"0%,{pct(TYPE_SLOTS[0][0])}{{transform:translate(0,0)}}"]
    for i, (s, e) in enumerate(TYPE_SLOTS):
        n = sum(len(t) for t, _ in LINES[i])
        hops.append(f"{pct(s + 0.001)}{{transform:translate(0,{i * LINE_H}px)}}")
        hops.append(f"{pct(e)}{{transform:translate({n * CH:.1f}px,{i * LINE_H}px)}}")
        if i + 1 < len(TYPE_SLOTS):
            hops.append(f"{pct(TYPE_SLOTS[i + 1][0] - 0.01)}"
                        f"{{transform:translate({n * CH:.1f}px,{i * LINE_H}px)}}")
    last_n = sum(len(t) for t, _ in LINES[-1])
    hops.append(f"{pct(ERASE_A)}{{transform:translate({last_n * CH:.1f}px,"
                f"{(len(LINES) - 1) * LINE_H}px)}}")
    hops.append(f"{pct(ERASE_B)},100%{{transform:translate(0,0)}}")
    c.append("@keyframes caret{" + "".join(hops) + "}")
    c.append(f".caret{{animation:caret {LOOP}s steps(1,end) infinite both}}")
    c.append("@keyframes blink{0%,45%{opacity:1}50%,95%{opacity:.08}100%{opacity:1}}")
    c.append(".blink{animation:blink 1.05s steps(1,end) infinite}")

    # ---- stdout frame draws itself, then leaves
    c.append(f"@keyframes frame{{0%,{pct(BOX_A)}{{stroke-dashoffset:var(--len);opacity:.9}}"
             f"{pct(BOX_B)},{pct(HOLD_B)}{{stroke-dashoffset:0;opacity:.9}}"
             f"{pct(EXIT_B)},100%{{stroke-dashoffset:var(--len);opacity:0}}}}")
    c.append(f".frame{{animation:frame {LOOP}s cubic-bezier(.4,0,.2,1) infinite both}}")

    # ---- headline characters fade up one after another
    c.append(f"@keyframes och{{0%,{pct(CHAR_A)}{{opacity:0;transform:translateY(7px)}}"
             f"{pct(CHAR_A + 0.55)}{{opacity:1;transform:translateY(0)}}"
             f"{pct(HOLD_B)}{{opacity:1;transform:translateY(0)}}"
             f"{pct(EXIT_B)},100%{{opacity:0;transform:translateY(-5px)}}}}")
    c.append(f".och{{opacity:0;animation:och {LOOP}s cubic-bezier(.2,.7,.3,1) infinite both}}")

    # ---- hairline accent rule under the frame
    c.append(f"@keyframes rule{{0%,{pct(RULE_A)}{{transform:scaleX(0)}}"
             f"{pct(RULE_B)},{pct(HOLD_B)}{{transform:scaleX(1)}}"
             f"{pct(EXIT_B)},100%{{transform:scaleX(0)}}}}")
    c.append(f".rule{{transform-origin:{BOX_X + BOX_W / 2:.1f}px 0;"
             f"animation:rule {LOOP}s cubic-bezier(.3,.8,.3,1) infinite both}}")

    # ---- the "stdout" label arrives with the frame
    c.append(f"@keyframes late{{0%,{pct(BOX_A)}{{opacity:0}}"
             f"{pct(BOX_B)},{pct(HOLD_B)}{{opacity:1}}{pct(EXIT_B)},100%{{opacity:0}}}}")
    c.append(f".late{{opacity:0;animation:late {LOOP}s ease infinite both}}")
    c.append('</style>')
    return "".join(c)


# --------------------------------------------------------------------- code block
def build_code():
    p = ['<g clip-path="url(#codeclip)">', f'<g class="m" font-size="{FS}">']
    for i, spans in enumerate(LINES):
        y = CODE_Y + i * LINE_H
        p.append(f'<text x="{TX + 26}" y="{y}" fill="{GUT}" font-size="11.5">{i + 1:>2}</text>')
        p.append(f'<text x="{CODE_X}" y="{y}" xml:space="preserve">')
        for t, col in spans:
            p.append(f'<tspan fill="{col}">{esc(t)}</tspan>')
        p.append('</text>')
        # cover slides right => characters appear one at a time
        p.append(f'<rect class="t{i}" x="{CODE_X}" y="{y - 15}" width="760" '
                 f'height="{LINE_H - 2}" fill="{TERM_BG}"/>')
    p.append('</g>')
    p.append(f'<g class="caret" transform="translate(0,0)">'
             f'<rect class="blink" x="{CODE_X}" y="{CODE_Y - 12}" width="8" height="15" '
             f'fill="{ACCENT}" opacity="0.85"/></g>')
    p.append('</g>')
    return "".join(p)


# --------------------------------------------------------------------- stdout block
def build_output():
    p = []
    # label sitting just above the frame
    p.append(f'<text class="m late" x="{BOX_X:.1f}" y="{BOX_Y - 12}" font-size="10.5" '
             f'fill="{FAINT}" letter-spacing="2">stdout</text>')

    # frame, drawn on with a dash offset
    perim = 2 * (BOX_W + BOX_H)
    p.append(f'<rect class="frame" x="{BOX_X:.1f}" y="{BOX_Y}" width="{BOX_W:.1f}" '
             f'height="{BOX_H}" rx="6" fill="none" stroke="{RULE}" stroke-width="1.2" '
             f'style="--len:{perim:.0f};stroke-dasharray:{perim:.0f}"/>')

    # headline, one <text> per character so each can arrive on its own beat
    baseline = BOX_Y + BOX_H / 2 + HEAD_FS * 0.35
    x0 = BOX_X + BOX_PAD_X + HEAD_ADV / 2
    for i, ch in enumerate(HEADLINE):
        if ch == " ":
            continue
        p.append(f'<text class="m och" x="{x0 + i * HEAD_ADV:.1f}" y="{baseline:.1f}" '
                 f'font-size="{HEAD_FS}" fill="{INK}" text-anchor="middle" '
                 f'style="animation-delay:{i * 0.075:.2f}s">{esc(ch)}</text>')

    # the one bright element on the whole panel
    p.append(f'<rect class="rule" x="{BOX_X:.1f}" y="{BOX_Y + BOX_H + 16}" '
             f'width="{BOX_W:.1f}" height="2" rx="1" fill="{ACCENT}"/>')
    return "".join(p)


# --------------------------------------------------------------------- assemble
def main():
    a(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" '
      f'viewBox="0 0 {W} {H}" role="img" aria-label="AI/ML Engineer">')
    a(build_defs())
    a(build_css())

    a(f'<rect width="{W}" height="{H}" fill="{PAGE_BG}"/>')

    # ---- terminal window
    a(f'<rect x="{TX}" y="{TY}" width="{TW}" height="{TH}" rx="10" fill="{TERM_BG}" '
      f'stroke="{RULE}" stroke-width="1"/>')

    # title bar
    a(f'<path d="M{TX} {TY + 10} a10 10 0 0 1 10 -10 h{TW - 20} a10 10 0 0 1 10 10 '
      f'v{BAR - 10} h-{TW} Z" fill="{BAR_BG}"/>')
    a(f'<line x1="{TX}" y1="{TY + BAR}" x2="{TX + TW}" y2="{TY + BAR}" stroke="{RULE}"/>')
    for i, col in enumerate(["#e06c60", "#e0b457", "#5bb86a"]):
        a(f'<circle cx="{TX + 22 + i * 18}" cy="{TY + BAR / 2}" r="5" fill="{col}" '
          f'opacity="0.75"/>')
    a(f'<text class="m" x="{TX + TW / 2}" y="{TY + BAR / 2 + 4}" font-size="11.5" '
      f'fill="{DIM}" text-anchor="middle">~/ai-lab — engineer.py</text>')

    # ---- screen contents
    a('<g clip-path="url(#screen)">')
    a(build_code())
    a(build_output())
    a('</g>')

    # status bar
    sy = TY + TH - 14
    a(f'<line x1="{TX}" y1="{sy - 18}" x2="{TX + TW}" y2="{sy - 18}" stroke="{RULE}"/>')
    a(f'<text class="m" x="{TX + 26}" y="{sy}" font-size="11" fill="{FAINT}">'
      f'main · 0 errors · build 18ms</text>')
    a(f'<text class="m" x="{TX + TW - 26}" y="{sy}" font-size="11" fill="{FAINT}" '
      f'text-anchor="end">UTF-8  LF  Python 3.13</text>')

    a('</svg>')

    svg = "".join(out)
    OUT.write_text(svg, encoding="utf-8")
    print(f"wrote {OUT}  ({len(svg) / 1024:.1f} KB)")


if __name__ == "__main__":
    main()
