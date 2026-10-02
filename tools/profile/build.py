#!/usr/bin/env python3
"""Build every static profile panel: dark/light x desktop/compact. Standard library only.

    python tools/profile/build.py

The contribution panel lives in activity.py because it needs live data.
"""
import base64
import math
import random
from pathlib import Path

from theme import (PUBLISHED, THEMES, W, MW, P, MP, arrow, doc, esc, glass_card, glow_card, glyph, mix,
                   hline, tag, tag_defs, tag_width, text, tw, vline)

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "assets/svg"

PING = ("@keyframes ping{0%{transform:scale(1);opacity:.9}70%,100%{transform:scale(2.6);opacity:0}}"
        ".ping{transform-box:fill-box;transform-origin:center;animation:ping 2.8s ease-out infinite}")
TWINKLE = ("@keyframes tw{0%,100%{opacity:.25;transform:scale(.55)}50%{opacity:1;transform:scale(1.1)}}"
           ".tw{transform-box:fill-box;transform-origin:center;animation:tw 3.4s ease-in-out infinite}")


def status_tag(t, x, y, label, h=28):
    body, _ = tag(t, x, y, label, "green", "dot", 12.5, h)
    return body + (f'<circle class="ping motion" cx="{x + h / 2}" cy="{y + h / 2}" r="{h / 2 - 5}" fill="none" '
                   f'stroke="{t["hues"]["green"]["rim"]}"/>')


# ------------------------------------------------------------------ dot-matrix ring
def _unit(x, y, z):
    n = math.sqrt(x * x + y * y + z * z)
    return x / n, y / n, z / n


def ring(t, cx, cy, k, cell, seed=7, sparkles=7, dust=56):
    """A lit torus (the agent loop) rasterised into a plus-glyph dot matrix, like halftone print."""
    rng = random.Random(seed)
    R0, r0 = 1.0, .40
    ct, st = math.cos(math.radians(-62)), math.sin(math.radians(-62))
    cr, sr = math.cos(math.radians(-14)), math.sin(math.radians(-14))
    L = _unit(-.45, .62, .64)
    hv = _unit(L[0], L[1], L[2] + 1)
    nu, nv = int(2 * math.pi * k * (R0 + r0) / cell * 2.5), int(2 * math.pi * k * r0 / cell * 3)
    best = {}
    for a in range(nu):
        cu, su = math.cos(2 * math.pi * a / nu), math.sin(2 * math.pi * a / nu)
        for b in range(nv):
            cv, sv = math.cos(2 * math.pi * b / nv), math.sin(2 * math.pi * b / nv)
            px, py, pz = (R0 + r0 * cv) * cu, (R0 + r0 * cv) * su, r0 * sv
            nx, ny, nz = cv * cu, cv * su, sv
            py, pz = py * ct - pz * st, py * st + pz * ct
            ny, nz = ny * ct - nz * st, ny * st + nz * ct
            px, py = px * cr - py * sr, px * sr + py * cr
            nx, ny = nx * cr - ny * sr, nx * sr + ny * cr
            key = (round(px * k / cell), round(-py * k / cell))
            if key not in best or pz > best[key][0]:
                lam = max(0, nx * L[0] + ny * L[1] + nz * L[2])
                spec = max(0, nx * hv[0] + ny * hv[1] + nz * hv[2]) ** 24
                fog = .5 + .5 * (pz + 1.4) / 2.8
                best[key] = (pz, min(1, (.05 + .8 * lam + .55 * spec) * fog))
    arm, bar = cell * .34, cell * .17
    sym = (f'<path id="px" d="M{-bar:.2f} {-arm:.2f}h{2 * bar:.2f}v{arm - bar:.2f}h{arm - bar:.2f}v{2 * bar:.2f}h{bar - arm:.2f}'
           f'v{arm - bar:.2f}h{-2 * bar:.2f}v{bar - arm:.2f}h{bar - arm:.2f}v{-2 * bar:.2f}h{arm - bar:.2f}z"/>')
    groups = {k_: [] for k_ in ("dot_lo", "dot_mid", "dot_hi", "dot_warm")}
    faint, lit = [], []
    for (i, j), (_, b) in sorted(best.items()):
        x, y = cx + i * cell, cy + j * cell
        if b < .15:
            faint.append(f'<circle cx="{x:g}" cy="{y:g}" r="{cell * .11:.2f}"/>')
            continue
        tone = "dot_warm" if b > .4 and rng.random() < .035 else "dot_lo" if b < .42 else "dot_mid" if b < .74 else "dot_hi"
        groups[tone].append(f'<use href="#px" x="{x:g}" y="{y:g}" opacity="{.28 + .72 * b:.2f}"/>')
        if b > .55:
            lit.append((x, y))
    out = [f'<g fill="{t["dot_lo"]}" opacity=".45">{"".join(faint)}</g>']
    out += [f'<g fill="{t[tone]}">{"".join(items)}</g>' for tone, items in groups.items() if items]
    span = k * (R0 + r0)
    specks, seen = [], set(best)
    for _ in range(dust * 3):
        if len(specks) >= dust:
            break
        ang, rad = rng.uniform(0, 2 * math.pi), rng.uniform(1.0, 1.45)
        x = span * rad * math.cos(ang)
        y = min(span * rad * .62 * math.sin(ang) + abs(rng.gauss(0, span * .18)), span * .92)
        key = (round(x / cell), round(y / cell))
        if key in seen:
            continue
        seen.add(key)
        specks.append(f'<use href="#px" x="{cx + key[0] * cell:g}" y="{cy + key[1] * cell:g}" opacity="{rng.uniform(.15, .55):.2f}"/>')
    out.append(f'<g fill="{t["dot_mid"]}">{"".join(specks)}</g>')
    for x, y in rng.sample(lit, min(sparkles, len(lit))):
        out.append(f'<g class="tw" style="animation-delay:{rng.uniform(0, 3.4):.2f}s">'
                   + glyph("star", x, y, t["dot_hi"], cell * .21) + "</g>")
    return f"<defs>{sym}</defs>", "".join(out)


# ------------------------------------------------------------------ hero
NAME = "VINAYAK"
LOOP = [("route", "cyan", "arrow"), ("execute", "blue", "play"), ("verify", "green", "check"),
        ("cite", "yellow", "cite"), ("trace", "violet", "wave")]
CYCLE = 10
HERO_DESC = ("VINAYAK, AI/ML Engineer at AMnova Technologies, Kochi, India. AI systems that show their work: "
             "agents that run real tools, answers that cite or abstain. Agent loop: route, execute, verify, cite, trace. "
             "HackerRank Orchestrate finalist. Open to AI/ML and LLM roles.")


def name_block(t, x, y, size, ls):
    span = tw(NAME, size, weight=600) + 40
    defs = (f'<linearGradient id="ng" x1="0" y1="{y - size * .72:.0f}" x2="0" y2="{y}" gradientUnits="userSpaceOnUse">'
            f'<stop stop-color="{t["text"]}"/><stop offset="1" stop-color="{t["name_lo"]}"/></linearGradient>'
            f'<linearGradient id="sheen" x1="0" y1="0" x2="{size * 2.6:.0f}" y2="0" gradientUnits="userSpaceOnUse">'
            f'<stop stop-color="{t["sheen"]}" stop-opacity="0"/><stop offset=".5" stop-color="{t["sheen"]}" stop-opacity=".85"/>'
            f'<stop offset="1" stop-color="{t["sheen"]}" stop-opacity="0"/>'
            f'<animateTransform attributeName="gradientTransform" type="translate" dur="12s" repeatCount="indefinite" '
            f'values="{x - size * 3:.0f} 0;{x - size * 3:.0f} 0;{x + span:.0f} 0;{x + span:.0f} 0" keyTimes="0;.6;.8;1"/>'
            '</linearGradient>')
    body = (text(x, y, NAME, size, "url(#ng)", weight=600, ls=ls)
            + text(x, y, NAME, size, "url(#sheen)", weight=600, ls=ls, cls="motion"))
    return defs, body


def statement(t, x, y, size, before, accent="", after=""):
    """Sans headline with one italic serif accent, like editorial poster type."""
    serif = (f'<tspan class="f" font-style="italic" font-weight="400" letter-spacing="0">{esc(accent)}</tspan>' if accent else "")
    return (f'<text x="{x}" y="{y}" class="s" font-size="{size}" fill="{t["text"]}" font-weight="500" letter-spacing="-.5">'
            f'{esc(before)}{serif}{esc(after)}</text>')


def loop_tags(t, x, y, max_w, gap=8, rgap=10, h=28):
    out, cx, cy = [], x, y
    for i, (label, hue, ic) in enumerate(LOOP):
        w = tag_width(label, 12.5, h)
        if cx > x and cx + w > x + max_w:
            cx, cy = x, cy + h + rgap
        body, _ = tag(t, cx, cy, label, hue, ic, 12.5, h)
        out.append(f'<g class="lp{i}">{body}</g>')
        cx += w + gap
    f0 = t["tag_fill"]
    css = f"@keyframes lp{{0%,24%,100%{{fill-opacity:{f0}}}6%,12%{{fill-opacity:{min(f0 * 3, .5):.2f}}}}}"
    css += "".join(f".lp{i} rect{{animation:lp {CYCLE}s ease-in-out {i * CYCLE / 5:.1f}s infinite}}" for i in range(5))
    return "".join(out), css, cy + h


def hero_desktop(t):
    w, h = W, 396
    nd, nb = name_block(t, P, 132, 64, 2)
    rd, rb = ring(t, 712, 172, 96, 8)
    tags, tcss, _ = loop_tags(t, P, 286, 520)
    b = [glass_card(t, w, h, "h", bloom="violet", bloom_at=(712, 172, 300)), tag_defs(t), "<defs>" + nd + "</defs>", rd,
         f'<g clip-path="url(#hk)">{rb}</g>',
         status_tag(t, P, 34, "Open to AI/ML & LLM roles"), nb,
         f'<text x="{P}" y="170" class="s" font-size="19"><tspan fill="{t["hues"]["blue"]["ink"]}" font-weight="500">AI/ML Engineer</tspan>'
         f'<tspan fill="{t["text2"]}"> · AMnova Technologies</tspan></text>',
         statement(t, P, 230, 29, "AI systems that ", "show", " their work."),
         text(P, 262, "Agents that run real tools. Answers that cite or abstain.", 15.5, t["text2"]),
         tags, hline(t, P, 340, w - P),
         text(P, 370, "KOCHI, INDIA", 11.5, t["text3"], True, ls=1.2),
         text(w - P, 370, "HACKERRANK ORCHESTRATE FINALIST", 11.5, t["text3"], True, anchor="end", ls=1.2)]
    return doc(w, h, "VINAYAK — AI/ML Engineer", HERO_DESC, "".join(b), PING + TWINKLE + tcss)


def hero_compact(t):
    w = MW
    nd, nb = name_block(t, MP, 286, 44, 1.5)
    rd, rb = ring(t, 200, 104, 66, 6, sparkles=5, dust=40)
    tags, tcss, ty = loop_tags(t, MP, 506, w - 2 * MP)
    h = ty + 84
    b = [glass_card(t, w, h, "h", bloom="violet", bloom_at=(200, 104, 220)), tag_defs(t), "<defs>" + nd + "</defs>", rd,
         f'<g clip-path="url(#hk)">{rb}</g>',
         status_tag(t, MP, 206, "Open to AI/ML & LLM roles"), nb,
         text(MP, 320, "AI/ML Engineer", 17, t["hues"]["blue"]["ink"], weight=500),
         text(MP, 344, "AMnova Technologies · Kochi, India", 15, t["text2"]),
         statement(t, MP, 398, 31, "AI systems that"),
         statement(t, MP, 434, 31, "", "show", " their work."),
         text(MP, 468, "Agents that run real tools.", 15, t["text2"]),
         text(MP, 490, "Answers that cite or abstain.", 15, t["text2"]),
         tags, hline(t, MP, ty + 26, w - MP),
         text(MP, ty + 54, "HACKERRANK ORCHESTRATE FINALIST", 11, t["text3"], True, ls=1)]
    return doc(w, h, "VINAYAK — AI/ML Engineer", HERO_DESC, "".join(b), PING + TWINKLE + tcss)


# ------------------------------------------------------------------ expertise: three lit cards + principles
FOCUS = [
    ("blue", "nodes", "Agent systems", "loom.ai",
     ["Tool execution in a real Linux", "sandbox; model routing with", "provider fallback."],
     ["Tool execution in a real Linux sandbox;", "model routing with provider fallback."]),
    ("green", "cite", "Grounded generation", "loom.ai · lazyhire",
     ["Answers that cite sources or", "abstain; CV drafts checked", "for invented claims."],
     ["Answers that cite sources or abstain;", "CV drafts checked for invented claims."]),
    ("orange", "bars", "Applied ML", "InForge-AI · InsightGenie",
     ["Cleaning, EDA and model", "benchmarking, with local", "fallbacks when LLMs fail."],
     ["Cleaning, EDA and model benchmarking,", "with local fallbacks when LLMs fail."]),
]
PRINCIPLES = [("bolt", "Deterministic core"), ("target", "Cite or abstain"), ("refresh", "Fail over, not out"), ("doc", "Documented limits")]


def icon_tile(t, x, y, kind, s=42):
    ink = "#FFFFFF" if t["dark"] else t["text"]
    return (f'<rect x="{x:.1f}" y="{y}" width="{s}" height="{s}" rx="12" fill="{t["glass"]}" fill-opacity="{t["glass_op"] * 2:.2f}" '
            f'stroke="{t["line"]}" stroke-opacity="{t["line_op"] * 1.6:.2f}"/>' + glyph(kind, x + s / 2, y + s / 2, ink, s / 15, 1.6))


def cta(t, x, y, label, size=13):
    return text(x, y, label + "  →", size, t["text"], weight=600)


def expertise(t, m=False):
    b = []
    if m:
        w, ch, gap = MW, 186, 14
        for i, (hue, ic, title, ev, _, lines) in enumerate(FOCUS):
            y = i * (ch + gap)
            b.append(glow_card(t, w, ch, hue, f"e{i}", 0, y, strength=.9))
            b += [icon_tile(t, 20, y + 20, ic, 40), text(20, y + 98, title, 20, t["text"], weight=600)]
            b += [text(20, y + 122 + j * 20, s, 14, t["text2"]) for j, s in enumerate(lines)]
            b.append(cta(t, 20, y + 172, ev))
        y0 = 3 * ch + 3 * gap
        b.append(f'<g transform="translate(0 {y0})">{glass_card(t, w, 84, "p")}</g>')
        for i, (ic, label) in enumerate(PRINCIPLES):
            x, y = 20 + (i % 2) * 190, y0 + 35 + (i // 2) * 28
            b += [glyph(ic, x + 6, y - 5, t["text3"], 1.1), text(x + 20, y, label, 13.5, t["text2"])]
        h = y0 + 84
    else:
        gap, ch = 16, 240
        cw = (W - 2 * gap) / 3
        w = W
        for i, (hue, ic, title, ev, lines, _) in enumerate(FOCUS):
            x = i * (cw + gap)
            b.append(glow_card(t, cw, ch, hue, f"e{i}", x, 0))
            b += [icon_tile(t, x + 22, 22, ic), text(x + 22, 116, title, 21, t["text"], weight=600, ls=-.3)]
            b += [text(x + 22, 142 + j * 20, s, 13.5, t["text2"]) for j, s in enumerate(lines)]
            b.append(cta(t, x + 22, 214, ev))
        b.append(f'<g transform="translate(0 {ch + gap})">{glass_card(t, w, 50, "p", rx=25)}</g>')
        seg = w / len(PRINCIPLES)
        for i, (ic, label) in enumerate(PRINCIPLES):
            x = i * seg + (seg - 20 - tw(label, 13.5)) / 2
            b += [glyph(ic, x + 6, ch + gap + 20, t["text3"], 1.1), text(x + 20, ch + gap + 30, label, 13.5, t["text2"])]
        h = ch + gap + 50
    desc = " ".join(f"{title} ({ev}): {' '.join(lines)}" for _, _, title, ev, _, lines in FOCUS)
    desc += " Principles: " + ", ".join(p for _, p in PRINCIPLES) + "."
    return doc(w, h, "Engineering expertise", desc, "".join(b))


# ------------------------------------------------------------------ project cards
def card_header(t, w, p, label, hue, ic, repo, m):
    body, _ = tag(t, p, 26 if m else 30, label, hue, ic, 12 if m else 12.5, 26 if m else 28)
    out = [body, arrow(w - p, 32 if m else 37, t["text2"])]
    if not m:
        out.append(text(w - p - 21, 48, repo, 11.5, t["text2"], True, anchor="end"))
    return "".join(out)


LOOM_PATH = [("Next.js", "trace UI"), ("FastAPI", "WebSocket"), ("LangGraph", "StateGraph"),
             ("Router", "fallback"), ("Tools", "bash · fs · git"), ("E2B", "Linux sandbox")]
LOOM_STATS = [("8.9s → 5.0s", "median time-to-first-token"), ("8 models", "across Groq, OpenRouter, OpenCode"),
              ("10 agents", "specialists with human approval")]
LOOM_DESC = ("loom.ai, flagship agent workspace: a coding agent inside a real Linux sandbox that streams every tool call. "
             "Request path: Next.js trace UI, FastAPI WebSocket, LangGraph StateGraph, model router with fallback, tools, E2B sandbox; "
             "events stream back over the same WebSocket. Median time-to-first-token 8.9s to 5.0s with prompt caching; "
             "8 models across Groq, OpenRouter and OpenCode; 10 specialist agents with human approval.")


def box(t, x, y, w, h, title, sub, ts=14, ss=10.5):
    fill = mix(t["base"], t["glass"], .045 if t["dark"] else .025)
    return (f'<rect x="{x:.1f}" y="{y}" width="{w:.1f}" height="{h}" rx="12" fill="{fill}" '
            f'stroke="{t["line"]}" stroke-opacity="{t["line_op"] * 1.5:.2f}"/>'
            + text(x + w / 2, y + h / 2 - 2, title, ts, t["text"], weight=600, anchor="middle")
            + text(x + w / 2, y + h / 2 + 15, sub, ss, t["text3"], True, anchor="middle"))


def chevron(x, y, color, d="r"):
    s = {"r": f"M{x - 4:.1f} {y - 4}l4 4-4 4", "l": f"M{x + 4:.1f} {y - 4}l-4 4 4 4",
         "d": f"M{x - 4:.1f} {y - 4:.1f}l4 4 4-4", "u": f"M{x - 4:.1f} {y + 4:.1f}l4-4 4 4"}[d]
    return f'<path d="{s}" fill="none" stroke="{color}" stroke-width="1.4" stroke-linecap="round" stroke-linejoin="round"/>'


FLOW = "@keyframes flow{to{stroke-dashoffset:-10}}.flow{stroke-dasharray:3 7;animation:flow 1.1s linear infinite}"


def card_loom(t, m=False):
    blue, violet = t["hues"]["blue"]["rim"], t["hues"]["violet"]["rim"]
    b, css = [tag_defs(t)], FLOW
    if m:
        w = MW
        b += [card_header(t, w, MP, "Flagship", "blue", "star", "", True),
              text(MP, 92, "loom.ai", 34, t["text"], weight=600, ls=-1),
              text(MP, 124, "A coding agent inside a real Linux", 16, t["text2"]),
              text(MP, 147, "sandbox that streams every tool call.", 16, t["text2"])]
        gap, bh = 22, 50
        bw = (w - 2 * MP - 2 * gap) / 3
        rows = (174, 254)
        xs = [MP + i * (bw + gap) for i in range(3)]
        cells = [(xs[0], rows[0]), (xs[1], rows[0]), (xs[2], rows[0]), (xs[2], rows[1]), (xs[1], rows[1]), (xs[0], rows[1])]
        mid0, mid1 = rows[0] + bh / 2, rows[1] + bh / 2
        for i in range(2):
            x1, x2 = xs[i] + bw, xs[i + 1]
            b.append(f'<path class="flow" d="M{x1:.1f} {mid0}H{x2 - 2:.1f}" stroke="{blue}"/>' + chevron(x2 - 2, mid0, blue))
        cx = xs[2] + bw / 2
        b.append(f'<path class="flow" d="M{cx:.1f} {rows[0] + bh}V{rows[1] - 2}" stroke="{blue}"/>' + chevron(cx, rows[1] - 3, blue, "d"))
        for i in (2, 1):
            x1, x2 = xs[i], xs[i - 1] + bw
            b.append(f'<path class="flow" d="M{x1:.1f} {mid1}H{x2 + 2:.1f}" stroke="{blue}"/>' + chevron(x2 + 2, mid1, blue, "l"))
        b += [box(t, x, y, bw, bh, ti, su, 13.5, 10) for (x, y), (ti, su) in zip(cells, LOOM_PATH)]
        b += [text(MP, 330, "EVENTS STREAM BACK OVER ONE WEBSOCKET", 10.5, t["text3"], True, ls=.6), hline(t, MP, 352, w - MP)]
        for i, (v, lab) in enumerate(LOOM_STATS):
            y = 390 + i * 54
            b += [text(MP, y, v, 21, t["text"], weight=600, ls=-.3), text(MP, y + 21, lab, 13.5, t["text2"])]
        h = 390 + 2 * 54 + 21 + 34
    else:
        w, h = W, 380
        b += [card_header(t, w, P, "Flagship · agent workspace", "blue", "star", "vinayak533/loom.ai", False),
              text(P, 106, "loom.ai", 38, t["text"], weight=600, ls=-1.2),
              text(P, 138, "A coding agent inside a real Linux sandbox that streams every tool call.", 17, t["text2"])]
        y0, bh, n, gap = 166, 58, len(LOOM_PATH), 26
        bw = (w - 2 * P - gap * (n - 1)) / n
        xs = [P + i * (bw + gap) for i in range(n)]
        my, lane = y0 + bh / 2, y0 + bh + 24
        c0, c5 = xs[0] + bw / 2, xs[-1] + bw / 2
        label = "STREAMED BACK: TOKENS · TOOL OUTPUT · DIFFS · PREVIEW"
        half = (tw(label, 10.5, True) + len(label) * .6) / 2 + 14
        mx = (c0 + c5) / 2
        b += [hline(t, x + bw, my, x + bw + gap - 3, .22) for x in xs[:-1]]
        b.append(f'<circle class="req motion" cx="{c0:.1f}" cy="{my}" r="3.5" fill="{blue}"/>')
        b.append(f'<path class="flow" d="M{c5:.1f} {y0 + bh}V{lane}H{mx + half:.1f}M{mx - half:.1f} {lane}H{c0:.1f}V{y0 + bh + 4}" '
                 f'fill="none" stroke="{violet}" stroke-opacity=".85"/>' + chevron(c0, y0 + bh + 4, violet, "u"))
        b.append(text(mx, lane + 4, label, 10.5, t["text3"], True, anchor="middle", ls=.6))
        b += [chevron(x - 3, my, t["text3"]) for x in xs[1:]]
        b += [box(t, x, y0, bw, bh, ti, su) for x, (ti, su) in zip(xs, LOOM_PATH)]
        b.append(hline(t, P, 280, w - P))
        cw = (w - 2 * P) / 3
        for i, (v, lab) in enumerate(LOOM_STATS):
            x = P + i * cw + (24 if i else 0)
            if i:
                b.append(vline(t, P + i * cw, 298, 352))
            b += [text(x, 324, v, 25, t["text"], weight=600, ls=-.5), text(x, 348, lab, 13, t["text2"])]
        travel = c5 - c0
        css += (f"@keyframes req{{0%{{transform:translateX(0);opacity:0}}4%{{opacity:1}}62%{{transform:translateX({travel:.1f}px);opacity:1}}"
                f"68%,100%{{transform:translateX({travel:.1f}px);opacity:0}}}}.req{{animation:req 6s cubic-bezier(.45,0,.25,1) infinite}}")
    return doc(w, h, "loom.ai", LOOM_DESC, glow_card(t, w, h, "blue", "c") + "".join(b), css)


PROJECTS = {
    "lazyhire": dict(
        hue="green", icon="check", label="Career workspace", name="lazyhire", repo="vinayak533/lazyhire",
        tagline="A private career workspace that ranks Kerala job listings against your CV.",
        compact=["A private career workspace that ranks", "Kerala job listings against your CV."],
        steps=["9 sources", "validate apply links", "dedupe", "rank + explain", "guarded CV drafts"],
        stack="Next.js 16 · React 19 · TypeScript · SQLite + Drizzle · Playwright",
        prop="zero-fabrication CV guardrails"),
    "inforge": dict(
        hue="orange", icon="bars", label="Analytics pipeline", name="InForge-AI", repo="vinayak533/InForge-AI",
        tagline="Eight pipeline agents turn a CSV or Excel file into analysis, models and a report.",
        compact=["Eight pipeline agents turn a CSV or Excel", "file into analysis, models and a report."],
        steps=["ingest", "clean", "EDA", "visualize", "ML benchmark", "insights", "code", "chat"],
        stack="FastAPI · WebSockets · pandas · scikit-learn · XGBoost · React",
        prop="completes without an LLM provider"),
}


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


def check(x, y, color):
    return f'<path d="M{x:g} {y - 3:g}l3 3 6-6.5" fill="none" stroke="{color}" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/>'


def card_project(t, key, m=False):
    d = PROJECTS[key]
    c = t["hues"][d["hue"]]
    cs, ch, aw = 11.5, 28, 22
    steps = [(s, tag_width(s, cs, ch, False, True)) for s in d["steps"]]
    b = [tag_defs(t)]

    def step(x, y, s, wd):
        return tag(t, x, y, s, d["hue"], None, cs, ch, True, w=wd)[0]

    if m:
        w = MW
        b += [card_header(t, w, MP, d["label"], d["hue"], d["icon"], "", True), text(MP, 90, d["name"], 28, t["text"], weight=600, ls=-.8)]
        b += [text(MP, 120 + i * 22, s, 15.5, t["text2"]) for i, s in enumerate(d["compact"])]
        y = 164
        for row in wrap_tokens(steps, w - 2 * MP, aw):
            x = MP
            for j, (s, wd) in enumerate(row):
                if j:
                    b.append(chevron(x - aw / 2 + 2, y + ch / 2, t["text3"]))
                b.append(step(x, y, s, wd))
                x += wd + aw
            y += ch + 10
        y += 12
        b.append(hline(t, MP, y, w - MP))
        parts = [(p, tw(p, 11.5, True)) for p in d["stack"].split(" · ")]
        for row in wrap_tokens(parts, w - 2 * MP, tw(" · ", 11.5, True)):
            y += 24
            b.append(text(MP, y, " · ".join(p for p, _ in row), 11.5, t["text2"], True))
        y += 28
        b += [check(MP + 1, y - 4, c["ink"]), text(MP + 18, y, d["prop"], 13.5, c["ink"], weight=500)]
        h = y + 32
    else:
        w, h = W, 262
        b += [card_header(t, w, P, d["label"], d["hue"], d["icon"], d["repo"], False),
              text(P, 102, d["name"], 32, t["text"], weight=600, ls=-.9),
              text(P, 133, d["tagline"], 16, t["text2"])]
        x, y = P, 158
        for j, (s, wd) in enumerate(steps):
            if j:
                b.append(chevron(x - aw / 2 + 2, y + ch / 2, t["text3"]))
            b.append(step(x, y, s, wd))
            x += wd + aw
        pw = tw(d["prop"], 13.5, weight=500)
        b += [hline(t, P, 210, w - P), text(P, 238, d["stack"], 11.5, t["text2"], True),
              check(w - P - pw - 18, 234, c["ink"]), text(w - P - pw, 238, d["prop"], 13.5, c["ink"], weight=500)]
    desc = f'{d["name"]}: {d["tagline"]} Pipeline: {" → ".join(d["steps"])}. Stack: {d["stack"]}. {d["prop"].capitalize()}.'
    return doc(w, h, d["name"], desc, glow_card(t, w, h, d["hue"], "c", strength=.85) + "".join(b))


# ------------------------------------------------------------------ framed screenshot
def screen(t, png, label, alt):
    raw = png.read_bytes()
    iw, ih = int.from_bytes(raw[16:20], "big"), int.from_bytes(raw[20:24], "big")
    bar, w = 36, W
    img_h = (w - 2) * ih / iw
    h = math.ceil(bar + img_h + 1)
    data = base64.b64encode(raw).decode()
    ln = f'stroke="{t["line"]}" stroke-opacity="{t["line_op"] * 1.3:.2f}"'
    dots = "".join(f'<circle cx="{22 + i * 16}" cy="18" r="4.5" fill="{t["line"]}" fill-opacity="{t["line_op"] * 1.8:.2f}"/>' for i in range(3))
    body = (f'<defs><clipPath id="win"><rect x="1" y="1" width="{w - 2}" height="{h - 2}" rx="19"/></clipPath></defs>'
            f'<g clip-path="url(#win)"><rect width="{w}" height="{h}" fill="{t["base_top"]}"/>'
            f'<image x="1" y="{bar}" width="{w - 2}" height="{img_h:.2f}" preserveAspectRatio="none" href="data:image/png;base64,{data}"/></g>'
            f'{dots}{text(w / 2, 22, label, 11, t["text3"], True, anchor="middle")}'
            f'<path d="M1 {bar - .5}H{w - 1}" {ln}/>'
            f'<rect x=".5" y=".5" width="{w - 1}" height="{h - 1}" rx="20" fill="none" {ln}/>')
    return doc(w, h, label, alt, body)


# ------------------------------------------------------------------ stack
STACK = [
    ("AI / ML", "orange", "bars", ["pandas", "NumPy", "scikit-learn", "XGBoost"]),
    ("LLMs & agents", "blue", "nodes", ["LangGraph", "CrewAI", "LlamaIndex", "Vanna 2.0", "OpenAI SDK"]),
    ("Model APIs", "violet", "swap", ["Groq", "Gemini", "OpenRouter"]),
    ("Backend", "cyan", "server", ["Python", "FastAPI", "WebSockets", "Pydantic"]),
    ("Frontend", "pink", "window", ["TypeScript", "Next.js", "React", "Tailwind CSS"]),
    ("Data", "yellow", "db", ["PostgreSQL", "Supabase", "pgvector", "SQLite", "Drizzle"]),
    ("Cloud & delivery", "green", "cloud", ["E2B", "Docker", "GitHub Actions", "Playwright", "Vercel", "Render"]),
]


def plain_chip(t, x, y, w, h, label, size=13):
    return (f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h}" rx="{h / 2}" fill="{t["glass"]}" '
            f'fill-opacity="{t["glass_op"] * 1.6:.2f}" stroke="{t["line"]}" stroke-opacity="{t["line_op"] * 1.4:.2f}"/>'
            + text(x + w / 2, y + h / 2 + size * .36, label, size, t["text"], anchor="middle"))


def stack(t, m=False):
    cs, ch, gap = 13, 28, 8
    b = [tag_defs(t)]
    if m:
        w, y = MW, 6
        for i, (group, hue, ic, items) in enumerate(STACK):
            if i:
                b.append(hline(t, MP, y + 4, w - MP))
            y += 18
            b.append(tag(t, MP, y, group, hue, ic, 12, 26)[0])
            y += 26 + 10
            chips = [(s, tw(s, cs) + 26) for s in items]
            for row in wrap_tokens(chips, w - 2 * MP, gap):
                x = MP
                for s, wd in row:
                    b.append(plain_chip(t, x, y, wd, ch, s, cs))
                    x += wd + gap
                y += ch + gap
            y += 4
        h = y + 16
    else:
        w, rh, top = W, 48, 20
        h = top * 2 + rh * len(STACK)
        for i, (group, hue, ic, items) in enumerate(STACK):
            y = top + i * rh
            if i:
                b.append(hline(t, P, y, w - P))
            b.append(tag(t, P, y + 10, group, hue, ic, 12.5, 28, w=158)[0])
            x = 220
            for s in items:
                wd = tw(s, cs) + 26
                b.append(plain_chip(t, x, y + 10, wd, ch, s, cs))
                x += wd + gap
    desc = "; ".join(f"{g}: {', '.join(items)}" for g, _, _, items in STACK)
    return doc(w, h, "Tech stack", desc, glass_card(t, w, h, "s") + "".join(b))


# ------------------------------------------------------------------ contact
EMAIL = "vinayakkvjob@gmail.com"


def button(t, x, y, w, h):
    """Bevelled key, like a poster CTA: light on dark, dark on light."""
    if t["dark"]:
        top, bot, ink, edge = "#F5F6F8", "#C9CDD4", "#0B0F14", "#FFFFFF"
    else:
        top, bot, ink, edge = "#273244", "#0B1220", "#FFFFFF", "#475569"
    return (f'<defs><linearGradient id="key" x1="0" y1="{y}" x2="0" y2="{y + h}" gradientUnits="userSpaceOnUse">'
            f'<stop stop-color="{top}"/><stop offset="1" stop-color="{bot}"/></linearGradient></defs>'
            f'<rect x="{x:.1f}" y="{y + 3}" width="{w:.1f}" height="{h}" rx="12" fill="#000000" fill-opacity=".35"/>'
            f'<rect x="{x:.1f}" y="{y}" width="{w:.1f}" height="{h}" rx="12" fill="url(#key)" stroke="{edge}" stroke-opacity=".55"/>'
            f'<path d="M{x + 12:.1f} {y + 1.5}H{x + w - 12:.1f}" stroke="#FFFFFF" stroke-opacity=".7"/>'
            + text(x + w / 2 - 9, y + h / 2 + 4.8, EMAIL, 13.5, ink, True, 600, "middle")
            + arrow(x + w / 2 + tw(EMAIL, 13.5, True) / 2 + 9, y + h / 2 - 5, ink, 9, 1.7))


def live_dot(t, x, y):
    g = t["hues"]["green"]["rim"]
    return (f'<circle cx="{x}" cy="{y}" r="3.5" fill="{g}"/>'
            f'<circle class="ping motion" cx="{x}" cy="{y}" r="3.5" fill="none" stroke="{g}"/>')


def contact(t, m=False):
    b = []
    if m:
        w, h = MW, 286
        b += [statement(t, MP, 64, 27, "Let’s build AI that"), statement(t, MP, 98, 27, "", "shows its work."),
              live_dot(t, MP + 4, 134), text(MP + 18, 139, "Open to AI/ML and LLM engineering roles.", 14.5, t["text2"]),
              text(MP, 162, "Remote · Bangalore · Kochi · Hyderabad", 14.5, t["text2"]),
              button(t, MP, 196, w - 2 * MP, 50)]
    else:
        w, h = W, 184
        bw = tw(EMAIL, 13.5, True) + 72
        b += [statement(t, P, 78, 27, "Let’s build AI that ", "shows its work."),
              live_dot(t, P + 4, 112), text(P + 18, 117, "Open to AI/ML and LLM engineering roles.", 15, t["text2"]),
              text(P, 141, "Remote · Bangalore · Kochi · Hyderabad", 15, t["text2"]),
              button(t, w - P - bw, 66, bw, 50)]
    return doc(w, h, "Contact", "Let’s build AI that shows its work. Open to AI/ML and LLM engineering roles: remote, Bangalore, "
               f"Kochi or Hyderabad. Email {EMAIL}.", glow_card(t, w, h, "violet", "c", strength=.8) + "".join(b), PING)


# ------------------------------------------------------------------ link pills
LINKS = {"linkedin": ("LinkedIn", "blue", "linkedin"), "portfolio": ("Portfolio", "violet", "globe"), "email": ("Email", "green", "mail")}


def link_pill(t, key):
    label, hue, ic = LINKS[key]
    h = 34
    w = math.ceil(tag_width(label, 13.5, h)) + 2
    body, _ = tag(t, 1, .5, label, hue, ic, 13.5, h - 1, w=w - 2, solid=True)
    return doc(w, h, label, label, tag_defs(t) + body)


# ------------------------------------------------------------------
def main():
    OUT.mkdir(parents=True, exist_ok=True)
    responsive = {"hero": lambda t, m: hero_compact(t) if m else hero_desktop(t), "expertise": expertise,
                  "card-loom": card_loom, "card-lazyhire": lambda t, m: card_project(t, "lazyhire", m),
                  "card-inforge": lambda t, m: card_project(t, "inforge", m), "stack": stack, "contact": contact}
    count = 0
    for theme in PUBLISHED:
        t = THEMES[theme]
        for name, render in responsive.items():
            for m in (False, True):
                (OUT / f'{name}-{theme}{"-compact" if m else ""}.svg').write_text(render(t, m), encoding="utf-8")
                count += 1
        for key in LINKS:
            (OUT / f"link-{key}-{theme}.svg").write_text(link_pill(t, key), encoding="utf-8")
            count += 1
        (OUT / f"screen-loom-{theme}.svg").write_text(
            screen(t, ROOT / "assets/screens/loom-agent-trace.png", "loom.ai — Code workspace",
                   "loom.ai's Code workspace: timed tool calls in the agent trace beside the file the agent wrote. "
                   "Real interface; scripted demo turn."), encoding="utf-8")
        count += 1
    print(f"Built {count} profile assets.")


if __name__ == "__main__":
    main()
