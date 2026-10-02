#!/usr/bin/env python3
"""Render every static profile panel into assets/svg/{name}-{dark,light}.svg.

    python tools/profile/build.py

No dependencies. The contribution panel is separate (activity.py) because it
needs live data and is refreshed by a workflow.
"""
import math
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from theme import THEMES, W, doc, panel, text, delay, line, poly, motion, esc  # noqa: E402

OUT = pathlib.Path(__file__).resolve().parents[2] / "assets" / "svg"


# ------------------------------------------------------------------ hero
NODES = {
    "L1": (52, 58), "L2": (118, 40), "L3": (86, 112), "L4": (40, 176), "L5": (96, 226), "L6": (54, 292), "L7": (128, 322),
    "R1": (828, 52), "R2": (758, 36), "R3": (800, 118), "R4": (846, 184), "R5": (786, 236), "R6": (830, 300), "R7": (748, 326),
    "T1": (250, 34), "T2": (372, 58), "T3": (500, 30), "T4": (626, 54),
    "B1": (270, 332), "B2": (400, 314), "B3": (520, 338), "B4": (640, 320),
}
DESKTOP_ONLY = {"L7", "R7", "B1", "B2", "B3", "B4"}
EDGES = [
    ("L1", "L2"), ("L1", "L3"), ("L2", "L3"), ("L3", "L4"), ("L4", "L5"), ("L5", "L6"), ("L6", "L7"), ("L3", "L5"),
    ("R1", "R2"), ("R1", "R3"), ("R2", "R3"), ("R3", "R4"), ("R4", "R5"), ("R5", "R6"), ("R6", "R7"), ("R3", "R5"),
    ("L2", "T1"), ("T1", "T2"), ("T2", "T3"), ("T3", "T4"), ("T4", "R2"),
    ("L7", "B1"), ("B1", "B2"), ("B2", "B3"), ("B3", "B4"), ("B4", "R7"),
]


def hero(t):
    H = 360
    a = t["accent"]
    css = (
        "@keyframes wipe{from{transform:translateX(-1200px)}to{transform:translateX(0)}}"
        ".wipe{animation:wipe 1.9s cubic-bezier(.6,0,.2,1) 5s both}"
        "@keyframes lsd{from{letter-spacing:34px}to{letter-spacing:16px}}"
        "@keyframes lsm{from{letter-spacing:26px}to{letter-spacing:10px}}"
        ".nd{letter-spacing:16px;animation:lsd 2.2s cubic-bezier(.2,.7,.2,1) 5s both}"
        ".nmb{letter-spacing:10px;animation:lsm 2.2s cubic-bezier(.2,.7,.2,1) 5s both}"
        ".halo{animation:breathe 7s ease-in-out infinite}"
    )
    b = [
        "<defs>"
        f'<pattern id="g" width="40" height="40" patternUnits="userSpaceOnUse"><path d="M40 0H0V40" fill="none" stroke="{t["grid"]}"/></pattern>'
        '<radialGradient id="vg" cx="50%" cy="50%" r="62%"><stop offset="0" stop-color="#fff"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></radialGradient>'
        f'<radialGradient id="glow" cx="50%" cy="50%" r="50%"><stop offset="0" stop-color="{a}" stop-opacity="{t["glow"]}"/><stop offset="1" stop-color="{a}" stop-opacity="0"/></radialGradient>'
        f'<mask id="vm"><rect width="{W}" height="{H}" fill="url(#vg)"/></mask>'
        '<linearGradient id="wg" x1="0" x2="1"><stop offset="0" stop-color="#fff"/><stop offset=".82" stop-color="#fff"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>'
        f'<mask id="wm" maskUnits="userSpaceOnUse" x="0" y="0" width="{W}" height="{H}"><rect class="wipe" x="-200" y="0" width="1400" height="{H}" fill="url(#wg)"/></mask>'
        f'<clipPath id="pc"><rect x="1" y="1" width="{W - 2}" height="{H - 2}" rx="13"/></clipPath>'
        "</defs>",
        panel(t, W, H),
        f'<g clip-path="url(#pc)"><rect width="{W}" height="{H}" fill="url(#g)" mask="url(#vm)" class="fade" style="animation-duration:1.5s"/>'
        f'<ellipse cx="440" cy="200" rx="360" ry="130" fill="url(#glow)" class="fade" style="animation-delay:4.4s;animation-duration:2s"/></g>',
    ]
    for i, (p, q) in enumerate(EDGES):
        (x1, y1), (x2, y2) = NODES[p], NODES[q]
        cls = "draw dsk" if {p, q} & DESKTOP_ONLY else "draw"
        b.append(line(x1, y1, x2, y2, a, cls=cls, d=3.0 + i * 0.07, opacity=.36))
    # the network reaches for the name: brackets and two converging edges (desktop only)
    b.append(line(86, 112, 126, 155, a, cls="draw dsk", d=4.6, opacity=.5))
    b.append(line(800, 118, 754, 155, a, cls="draw dsk", d=4.6, opacity=.5))
    b.append(poly([(134, 126), (126, 126), (126, 184), (134, 184)], t["text3"], cls="draw dsk", d=4.9))
    b.append(poly([(746, 126), (754, 126), (754, 184), (746, 184)], t["text3"], cls="draw dsk", d=4.9))
    for i, (k, (x, y)) in enumerate(NODES.items()):
        cls = "fade dsk" if k in DESKTOP_ONLY else "fade"
        b.append(
            f'<g class="{cls}"{delay(1.5 + i * 0.065)}>'
            f'<circle cx="{x}" cy="{y}" r="9" fill="{a}" fill-opacity=".14" class="halo" style="animation-delay:{3 + (i * 7) % 11 * .5:.1f}s"/>'
            f'<circle cx="{x}" cy="{y}" r="2.6" fill="{a}"/></g>'
        )
    # ambient pulses after the intro
    top = [NODES[k] for k in ("L4", "L3", "L2", "T1", "T2", "T3", "T4", "R2", "R3", "R4")]
    route = top + top[-2::-1]
    stops = [7 + 16 * i / (len(route) - 1) for i in range(len(route))]
    b.append(motion(route, [s - 7 for s in stops], 16, a, r=2.4, begin=7))
    bot = [NODES[k] for k in ("L5", "L6", "L7", "B1", "B2", "B3", "B4", "R7", "R6", "R5")]
    route = bot + bot[-2::-1]
    b.append(f'<g class="dsk">{motion(route, [19 * i / (len(route) - 1) for i in range(len(route))], 19, t["amber"], r=2.2, begin=9)}</g>')

    name = "VINAYAK K V"
    b.append(f'<g mask="url(#wm)"><text x="448" y="172" text-anchor="middle" class="s nd dsk" font-size="60" font-weight="600" fill="{t["text"]}">{name}</text>'
             f'<text x="445" y="140" text-anchor="middle" class="s nmb mob" font-size="82" font-weight="600" fill="{t["text"]}">{name}</text></g>')
    ident = "AI/ML ENGINEER  ·  AGENT SYSTEMS  ·  LLM INFRASTRUCTURE  ·  APPLIED ML"
    l1, l2 = "I build agent systems that run real tools,", "route across models, and refuse to make things up."
    b.append(f'<g class="dsk">'
             + f'<g class="rise"{delay(6.0)}>{text(441, 214, ident, 13, t["text2"], "m", "middle", ls=3)}</g>'
             + f'<g class="rise"{delay(6.4)}>{text(440, 256, l1, 19, t["text"], anchor="middle")}</g>'
             + f'<g class="rise"{delay(6.55)}>{text(440, 282, l2, 19, t["text"], anchor="middle")}</g></g>')
    b.append(f'<g class="mob">'
             + f'<g class="rise"{delay(6.0)}>{text(441, 196, "AI/ML ENGINEER · AGENT SYSTEMS", 25, t["text2"], "m", "middle", ls=2)}'
             + f'{text(441, 230, "LLM INFRASTRUCTURE · APPLIED ML", 25, t["text2"], "m", "middle", ls=2)}</g>'
             + f'<g class="rise"{delay(6.4)}>{text(440, 286, l1, 29, t["text"], anchor="middle")}'
             + f'{text(440, 324, l2, 29, t["text"], anchor="middle")}</g></g>')
    return doc(W, H, "Vinayak K V — AI/ML Engineer",
               f"{ident}. {l1} {l2}", "".join(b), css)


# ------------------------------------------------------------------ status strip
def status(t):
    H = 104
    css = "@keyframes ring{from{r:4;opacity:.7}to{r:13;opacity:0}}.ring{animation:ring 2.4s ease-out infinite}"
    cells = [("ROLE", "AI/ML Engineer · AMnova", 250), ("BASE", "Kochi, India", 160),
             ("FOCUS", "Agent systems · LLM infra", 270), ("NOW BUILDING", "loom.ai", 200)]
    b = [panel(t, W, H, 12), '<g class="dsk">']
    x = 0
    for i, (lab, val, w) in enumerate(cells):
        if i:
            b.append(f'<path d="M{x} 26V78" stroke="{t["border"]}"/>')
        g = [text(x + 24, 44, lab, 11.5, t["text3"], "m", ls=2.2)]
        if i == 3:
            g.append(f'<circle cx="{x + 28}" cy="67" r="4" fill="{t["amber"]}"/><circle cx="{x + 28}" cy="67" r="4" fill="none" stroke="{t["amber"]}" class="ring"/>')
            g.append(text(x + 42, 73, val, 17, t["text"], weight=500))
        else:
            g.append(text(x + 24, 73, val, 17, t["text"], weight=500))
        b.append(f'<g class="rise"{delay(.15 + i * .1)}>{"".join(g)}</g>')
        x += w
    b.append("</g><g class=\"mob\">")
    b.append(f'<path d="M440 14V90M24 52H856" stroke="{t["border"]}"/>')
    mob = ["AI/ML Engineer · AMnova", "Kochi, India", "Agents · LLM infra", "Building loom.ai"]
    for i, val in enumerate(mob):
        cx, cy = (i % 2) * 440 + 30, (i // 2) * 48 + 40
        if i == 3:
            b.append(f'<circle cx="{cx + 6}" cy="{cy - 9}" r="7" fill="{t["amber"]}"/>')
            b.append(text(cx + 24, cy, val, 26, t["text"], weight=500))
        else:
            b.append(text(cx, cy, val, 26, t["text"], weight=500))
    b.append("</g>")
    return doc(W, H, "Status", "Role: AI/ML Engineer at AMnova. Base: Kochi, India. Focus: agent systems and LLM infrastructure. Now building: loom.ai.",
               "".join(b), css)


# ------------------------------------------------------------------ terminal
def terminal(t):
    H = 380
    a, x0 = t["accent"], 32
    css = (
        "@keyframes cover{from{transform:scaleX(1)}to{transform:scaleX(0)}}"
        ".cv{transform-box:fill-box;transform-origin:100% 50%}"
        ".cur{animation:blink 1.1s steps(1) infinite}"
    )

    def block(lines, fs, lh, y0, cursor_on_last):
        out, y, tm = [], y0, 0.4
        cw = fs * 0.61
        for kind, payload in lines:
            if kind == "cmd":
                n = len(payload)
                dur = 0.05 * n + 0.15
                out.append(text(x0, y, "❯", fs, a, "m"))
                out.append(text(x0 + cw * 2, y, payload, fs, t["text"], "m"))
                out.append(f'<rect x="{x0 + cw * 2 - 1:.1f}" y="{y - fs:.1f}" width="{cw * n + 3:.1f}" height="{fs * 1.45:.1f}" '
                           f'fill="{t["canvas"]}" class="cv" style="animation:cover {dur:.2f}s steps({n}) {tm:.2f}s both"/>')
                tm += dur + 0.35
            else:
                segs = "".join(f'<tspan x="{sx:.1f}" fill="{c}">{esc(s)}</tspan>' for s, c, sx in payload)
                out.append(f'<g class="rise"{delay(tm)}><text y="{y}" class="m" font-size="{fs}" xml:space="preserve">{segs}</text></g>')
                tm += 0.15
            y += lh
        if cursor_on_last:
            cy = y - lh
            last = lines[-1][1]
            end = max(sx + len(s) * fs * .56 for s, c, sx in last) + fs * .3
            out.append(f'<rect x="{end:.1f}" y="{cy - fs * .8:.1f}" width="{cw * .9:.1f}" height="{fs:.1f}" fill="{a}" class="cur" style="animation-delay:{tm:.2f}s"/>')
        else:
            out.append(f'<g class="fade"{delay(tm + .1)}>{text(x0, y, "❯", fs, a, "m")}'
                       f'<rect x="{x0 + cw * 2:.1f}" y="{y - fs * .8:.1f}" width="{cw * .9:.1f}" height="{fs:.1f}" fill="{a}" class="cur" style="animation-delay:{tm + .1:.2f}s"/></g>')
        return "".join(out)

    def o(*segs, x=x0, cw=15 * .61):
        res, cx = [], x
        for s, c in segs:
            res.append((s, c, cx))
            cx += len(s) * cw
        return ("out", res)

    T2, T3 = t["text2"], t["text3"]
    focus = [("agent graphs that run real tools", "loom.ai"), ("one interface over many models, with fallback", "loom.ai"),
             ("retrieval that cites its sources or abstains", "loom.ai"), ("generated text checked for fabrication", "lazyhire")]
    desk = [("cmd", "whoami"), o(("Vinayak K V", t["text"]), (" · AI/ML Engineer · Kochi, India", T2)),
            ("cmd", "ls ~/systems"),
            o(("loom.ai/   lazyhire/   inforge-ai/   nl2sql/   llm-battle-arena/", a)),
            ("cmd", "cat focus.md")]
    for f, repo in focus:
        desk.append(("out", [("- " + f, T2, x0), (repo, T3, 640)]))
    cwm = 24 * .61
    mob = [("cmd", "whoami"), o(("Vinayak K V", t["text"]), (" · AI/ML Engineer · Kochi", T2), cw=cwm),
           ("cmd", "ls ~/systems"), o(("loom.ai/  lazyhire/  inforge-ai/  nl2sql/", a), cw=cwm),
           ("cmd", "cat focus.md"), ("out", [("- agent graphs that run real tools", T2, x0)]),
           ("out", [("- model routing with fallback", T2, x0)]), ("out", [("- answers that cite or abstain", T2, x0)])]
    dots = "".join(f'<circle cx="{24 + i * 18}" cy="20" r="5" fill="{t["border2"]}"/>' for i in range(3))
    b = [panel(t, W, H), f'<path d="M1 40H{W - 1}" stroke="{t["border"]}"/>',
         f'<g class="dsk">{dots}{text(440, 25, "vinayak@kochi: ~", 12, t["text3"], "m", "middle")}{block(desk, 15, 28, 76, False)}</g>',
         f'<g class="mob">{dots}{block(mob, 24, 36, 84, True)}</g>']
    return doc(W, H, "Console", "whoami: Vinayak K V, AI/ML Engineer, Kochi, India. Systems: loom.ai, lazyhire, inforge-ai, nl2sql, llm-battle-arena. "
               "Focus: agent graphs that run real tools; one interface over many models with fallback; retrieval that cites its sources or abstains; generated text checked for fabrication.",
               "".join(b), css)


# ------------------------------------------------------------------ system map
MAP = [
    ("AGENTS & LLMs", [("Agent graphs with real tools", "↳ loom.ai · LangGraph + E2B", "Agent graphs"),
                       ("Model router with fallback", "↳ loom.ai · 8 models, 3 providers", "Model routing"),
                       ("Retrieval with citations", "↳ loom.ai · notebooks", "Cited RAG"),
                       ("LLM-as-judge evaluation", "↳ llm-battle-arena", "LLM-as-judge")]),
    ("PRODUCT SYSTEMS", [("Streaming WebSocket backends", "↳ loom.ai · inforge-ai", "WebSocket APIs"),
                         ("Next.js + TypeScript products", "↳ lazyhire · loom.ai", "Next.js apps"),
                         ("Auth, CSP, CSRF, encryption", "↳ lazyhire", "App security"),
                         ("E2E tests and CI checks", "↳ lazyhire · loom.ai", "E2E testing")]),
    ("DATA & ML", [("Multi-agent analytics pipeline", "↳ inforge-ai · 8 stages", "Agent pipelines"),
                   ("Model benchmarking", "↳ inforge-ai · sklearn + XGBoost", "Benchmarking"),
                   ("Natural language → SQL", "↳ nl2sql · 18/20 own benchmark", "Text-to-SQL"),
                   ("Dataset health profiling", "↳ insightgenie", "Data profiling")]),
]


def system_map(t):
    H = 450
    a = t["accent"]
    b = [panel(t, W, H),
         f'<rect x="350" y="24" width="180" height="40" rx="20" fill="{t["raised"]}" stroke="{t["border2"]}"/>',
         f'<g class="dsk">{text(441, 49, "VINAYAK K V", 13, t["text"], "m", "middle", ls=3)}</g>',
         f'<g class="mob">{text(441, 53, "VINAYAK", 22, t["text"], "m", "middle", ls=3)}</g>',
         line(440, 64, 440, 96, a, d=.2, opacity=.6),
         line(159, 96, 721, 96, a, d=.45, opacity=.6)]
    ys = [196, 262, 328, 394]
    desc = []
    for c, (head, leaves) in enumerate(MAP):
        x0 = 24 + c * 281
        cx = x0 + 135
        b.append(line(cx, 96, cx, 120, a, d=.7, opacity=.6))
        b.append(f'<g class="fade"{delay(.8 + c * .1)}><rect x="{x0}" y="120" width="270" height="44" rx="10" fill="{t["raised"]}" stroke="{t["border"]}"/>'
                 f'<g class="dsk">{text(cx + 1, 147, head, 12.5, a, "m", "middle", ls=2.5)}</g>'
                 f'<g class="mob">{text(cx + 1, 150, head, 21, a, "m", "middle", ls=1.5)}</g></g>')
        b.append(line(x0 + 20, 164, x0 + 20, ys[-1], t["border2"], d=1.0 + c * .1))
        for i, (cap, ev, short) in enumerate(leaves):
            y = ys[i]
            d = 1.3 + c * .1 + i * .12
            b.append(f'<g class="fade"{delay(d)}><path d="M{x0 + 20} {y}H{x0 + 32}" stroke="{t["border2"]}"/>'
                     f'<circle cx="{x0 + 20}" cy="{y}" r="3" fill="{a}"/>'
                     f'<g class="dsk">{text(x0 + 40, y + 5, cap, 14.5, t["text"])}{text(x0 + 40, y + 26, ev, 11.5, t["text3"], "m")}</g>'
                     f'<g class="mob">{text(x0 + 40, y + 8, short, 23, t["text"])}</g></g>')
            desc.append(f"{cap} ({ev[2:]})")
    return doc(W, H, "Engineering system map", "; ".join(desc), "".join(b))


# ------------------------------------------------------------------ feature cards
CARDS = {
    "loom": dict(
        idx="01 · FLAGSHIP SYSTEM", name="loom.ai", repo="vinayak533/loom.ai",
        line="An AI workspace where a coding agent works inside a real Linux sandbox.",
        mob=("An AI workspace where a coding agent", "works inside a real Linux sandbox."),
        flow=[("PROBLEM", ["Chat agents can't run", "the code they write,", "or show their work."]),
              ("SYSTEM", ["WebSocket event stream", "→ LangGraph → tools", "→ E2B Linux sandbox"]),
              ("INTELLIGENCE", ["8 models, 3 providers", "task-classified routing", "fallback on 429 / 5xx"]),
              ("RESULT", ["Live trace + preview", "10 specialist agents", "TTFT 8.9s → 5.0s"])],
        stack="FastAPI · LangGraph · E2B · Supabase + pgvector · Next.js 14 · TypeScript",
        mstack="FastAPI · LangGraph · E2B · Supabase · Next.js"),
    "lazyhire": dict(
        idx="02 · PRODUCT SYSTEM", name="lazyhire", repo="vinayak533/lazyhire",
        line="A private career workspace that ranks Kerala job openings against your CV.",
        mob=("A private career workspace that ranks", "Kerala job openings against your CV."),
        flow=[("PROBLEM", ["Duplicate listings,", "dead apply links,", "inflated CV rewrites."]),
              ("SYSTEM", ["9 sources → validate", "→ dedupe → rank", "Next.js 16 · SQLite"]),
              ("INTELLIGENCE", ["CV review + tailoring", "no-fabrication guard", "knowledge-first tutor"]),
              ("RESULT", ["Explained fit scores", "AES-GCM CV storage", "Playwright E2E suite"])],
        stack="Next.js 16 · React 19 · TypeScript · SQLite + Drizzle · Zod · Playwright",
        mstack="Next.js 16 · TypeScript · SQLite · Playwright"),
    "inforge": dict(
        idx="03 · DATA SYSTEM", name="InForge-AI", repo="vinayak533/InForge-AI",
        line="Eight pipeline agents turn a raw CSV or Excel file into analysis, models and a report.",
        mob=("Eight pipeline agents turn a raw CSV or", "Excel file into analysis, models, a report."),
        flow=[("PROBLEM", ["Hours of profiling", "and cleaning before", "the first insight."]),
              ("SYSTEM", ["8 agents in sequence", "WebSocket progress", "FastAPI + React"]),
              ("INTELLIGENCE", ["sklearn/XGBoost compute", "LLMs write the prose", "heuristics if LLM fails"]),
              ("RESULT", ["Cleaned data + charts", "Benchmarked models", "PDF report + code"])],
        stack="FastAPI · WebSockets · pandas · scikit-learn · XGBoost · React · Gemini / Groq",
        mstack="FastAPI · pandas · scikit-learn · XGBoost · React"),
}


def card(t, key):
    c = CARDS[key]
    H = 330
    a = t["accent"]
    css = "@keyframes flow{to{stroke-dashoffset:-20}}.flow{stroke-dasharray:3 7;animation:flow 1.6s linear infinite}"
    b = [panel(t, W, H), '<g class="dsk">',
         text(32, 46, c["idx"], 11.5, a, "m", ls=2.2),
         text(848, 46, "github.com/" + c["repo"] + " ↗", 11.5, t["text3"], "m", "end"),
         text(32, 92, c["name"], 32, t["text"], weight=600, ls=.5),
         text(32, 124, c["line"], 16, t["text2"])]
    for i, (lab, lines) in enumerate(c["flow"]):
        bx = 32 + i * 210
        b.append(f'<g class="rise"{delay(.3 + i * .15)}><rect x="{bx}" y="150" width="186" height="110" rx="9" fill="{t["raised"]}" stroke="{t["border"]}"/>'
                 + text(bx + 14, 174, lab, 11, a if i < 3 else t["amber"], "m", ls=2)
                 + "".join(text(bx + 14, 198 + j * 20, s, 13.5, t["text"]) for j, s in enumerate(lines)) + "</g>")
        if i < 3:
            b.append(f'<path d="M{bx + 190} 205H{bx + 206}" stroke="{a}" stroke-opacity=".7" class="flow"/>'
                     f'<path d="M{bx + 202} 201L{bx + 206} 205L{bx + 202} 209" stroke="{a}" stroke-opacity=".7" fill="none"/>')
    b.append(f'<path d="M32 280H848" stroke="{t["border"]}"/>')
    b.append(text(32, 308, c["stack"], 12, t["text2"], "m"))
    b.append('</g><g class="mob">')
    b.append(text(32, 66, c["idx"], 21, a, "m", ls=2))
    b.append(text(32, 140, c["name"], 64, t["text"], weight=600))
    b.append(text(32, 204, c["mob"][0], 29, t["text2"]))
    b.append(text(32, 244, c["mob"][1], 29, t["text2"]))
    b.append(text(32, 302, c["mstack"], 21, t["text3"], "m"))
    b.append("</g>")
    flow = " ".join(f"{lab}: {' '.join(lines)}." for lab, lines in c["flow"])
    return doc(W, H, c["name"], f"{c['line']} {flow} Stack: {c['stack']}.", "".join(b), css)


# ------------------------------------------------------------------ loom.ai animated architecture
def arch_loom(t):
    H, LOOP = 430, 12.0
    a, am = t["accent"], t["amber"]
    boxes = {  # name: (x, y, w, h, title, subtitle, windows of activity)
        "browser": (30, 180, 150, 70, "Browser", "Next.js · trace UI", [(0, .5), (9.7, 10.8)]),
        "api": (240, 180, 150, 70, "FastAPI", "/ws/{session} · emitter", [(.7, 1.5), (8.9, 9.6)]),
        "graph": (450, 180, 160, 70, "LangGraph", "StateGraph · checkpoints", [(1.5, 2.2), (3.9, 4.6), (8.2, 8.9)]),
        "router": (450, 40, 160, 70, "Model router", "task class → model", [(2.2, 4.0)]),
        "tools": (660, 180, 150, 70, "Tool nodes", "bash · files · git · web", [(4.6, 5.3), (7.5, 8.2)]),
        "e2b": (660, 320, 150, 70, "E2B sandbox", "Linux · dev server", [(5.9, 7.2)]),
        "db": (240, 320, 150, 70, "Supabase", "Postgres · pgvector", [(9.5, 10.2)]),
    }
    css = ["@keyframes flow{to{stroke-dashoffset:-20}}.flow{stroke-dasharray:3 7;animation:flow 2s linear infinite}"]
    for k, (*_, wins) in boxes.items():
        stops = [f"0%{{stroke:{t['border2']}}}"]
        for s, e in wins:
            p0, p1 = s / LOOP * 100, e / LOOP * 100
            stops.append(f"{max(p0 - .5, 0):.2f}%{{stroke:{t['border2']}}}{p0:.2f}%,{p1:.2f}%{{stroke:{a}}}{min(p1 + 2, 100):.2f}%{{stroke:{t['border2']}}}")
        stops.append(f"100%{{stroke:{t['border2']}}}")
        css.append(f"@keyframes h{k}{{{''.join(stops)}}}.h{k}{{animation:h{k} {LOOP}s linear infinite}}")
    chip = ["OpenCode", "OpenRouter", "Groq"]
    css.append(
        f"@keyframes c0{{0%,20%{{fill:{t['raised']}}}21.5%,26%{{fill:{a};fill-opacity:.35}}27%,100%{{fill:{t['raised']}}}}}"
        f"@keyframes c0b{{0%,26%{{opacity:0}}27%,33%{{opacity:1}}34%,100%{{opacity:0}}}}"
        f"@keyframes c1{{0%,27.5%{{fill:{t['raised']}}}28.5%,33%{{fill:{a};fill-opacity:.35}}34%,100%{{fill:{t['raised']}}}}}"
        ".c0{animation:c0 12s linear infinite}.c1{animation:c1 12s linear infinite}.c0b{animation:c0b 12s linear infinite}"
    )
    b = [panel(t, W, H)]
    # edges
    E = [(180, 215, 240, 215), (390, 215, 450, 215), (530, 180, 530, 110), (610, 75, 650, 75), (610, 215, 660, 215), (735, 250, 735, 320)]
    for i, (x1, y1, x2, y2) in enumerate(E):
        b.append(line(x1, y1, x2, y2, a, d=.4 + i * .1, opacity=.55))
    b.append(f'<path d="M315 250V320" stroke="{t["text3"]}" class="flow"/>')
    b.append(f'<path d="M735 390V412H105V250" stroke="{am}" stroke-opacity=".6" fill="none" class="flow"/>')
    # dots under boxes, so they only show on the edges
    req = [(105, 209), (315, 209), (524, 209), (524, 75), (700, 51), (700, 75), (536, 75), (536, 221), (735, 209), (735, 355)]
    b.append(motion(req, [0, .8, 1.5, 2.2, 2.6, 3.4, 3.8, 4.3, 5.1, 5.9], LOOP, a, r=4))
    evt = [(741, 355), (741, 221), (530, 221), (315, 221), (105, 221)]
    b.append(motion(evt, [7.2, 7.8, 8.5, 9.2, 9.9], LOOP, am, r=4))
    b.append(motion([(735, 355), (735, 412), (105, 412), (105, 215)], [7.2, 7.5, 9.1, 9.6], LOOP, am, r=3))
    b.append(motion([(315, 215), (315, 355)], [9.2, 9.8], LOOP, t["text3"], r=3))
    for k, (x, y, w, h, title, sub, _) in boxes.items():
        cx = x + w / 2
        b.append(f'<g class="fade"{delay(.2)}><rect x="{x}" y="{y}" width="{w}" height="{h}" rx="10" fill="{t["raised"]}" stroke="{t["border2"]}" class="h{k}"/>'
                 f'<g class="dsk">{text(cx, y + 31, title, 15, t["text"], anchor="middle", weight=600)}{text(cx, y + 51, sub, 10.5, t["text3"], "m", "middle")}</g>'
                 f'<g class="mob">{text(cx, y + 44, title, 22, t["text"], anchor="middle", weight=600)}</g></g>')
    for i, name in enumerate(chip):
        y = 40 + i * 24
        cls = f"c{i}" if i < 2 else ""
        b.append(f'<g class="dsk"><rect x="650" y="{y}" width="120" height="21" rx="5" fill="{t["raised"]}" stroke="{t["border"]}" class="{cls}"/>'
                 f'{text(710, y + 15, name, 11, t["text2"], "m", "middle")}</g>')
    b.append(f'<g class="mob"><rect x="650" y="40" width="170" height="70" rx="10" fill="{t["raised"]}" stroke="{t["border"]}"/>{text(735, 84, "3 providers", 22, t["text2"], anchor="middle")}</g>')
    b.append(f'<g class="dsk c0b">{text(780, 55, "429 → fallback", 10.5, am, "m")}</g>')
    labels = [(210, 172, "user_message", "middle"), (420, 205, "state", "middle"), (522, 150, "route", "end"),
              (635, 172, "tool_use", "middle"), (745, 290, "exec", "start"), (325, 290, "fire-and-forget writes", "start"),
              (420, 426, "forwarded port → live preview", "middle")]
    lab = "".join(text(x, y, s, 10.5, t["text3"], "m", an) for x, y, s, an in labels)
    legend = (f'<circle cx="34" cy="30" r="4" fill="{a}"/>{text(46, 34, "request", 11, t["text2"], "m")}'
              f'<circle cx="124" cy="30" r="4" fill="{am}"/>{text(136, 34, "events: tokens · stdout · file_changed", 11, t["text2"], "m")}')
    b.append(f'<g class="dsk fade"{delay(.8)}>{lab}{legend}</g>')
    return doc(W, H, "loom.ai request path",
               "Browser sends user_message over a WebSocket to FastAPI; LangGraph asks the model router, which picks a model by task class and falls back "
               "across OpenCode, OpenRouter and Groq; tool_use routes to tool nodes that execute in an E2B sandbox; events stream back to the browser; "
               "writes to Supabase are fire-and-forget; the sandbox dev server is forwarded to a live preview.", "".join(b), "".join(css))


# ------------------------------------------------------------------ lazyhire + InForge static architecture
def pipeline_row(t, y, label, items, accent, d0):
    out = [text(32, y - 14, label, 11, accent, "m", ls=2)]
    for i, (title, short, sub) in enumerate(items):
        x = 32 + i * 169
        out.append(f'<g class="rise"{delay(d0 + i * .1)}><rect x="{x}" y="{y}" width="140" height="64" rx="9" fill="{t["raised"]}" stroke="{t["border"]}"/>'
                   f'<g class="dsk">{text(x + 70, y + 28, title, 13.5, t["text"], anchor="middle", weight=600)}{text(x + 70, y + 47, sub, 10, t["text3"], "m", "middle")}</g>'
                   f'<g class="mob">{text(x + 70, y + 41, short, 23, t["text"], anchor="middle", weight=600)}</g></g>')
        if i < len(items) - 1:
            out.append(line(x + 142, y + 32, x + 167, y + 32, accent, d=d0 + .3 + i * .1, opacity=.7))
    return "".join(out)


def arch_lazyhire(t):
    H = 310
    row1 = [("Career brief", "Brief", "role · place · skills"), ("9 job sources", "Sources", "Technopark · Infopark …"),
            ("Validate links", "Validate", "posting / ATS URLs only"), ("Merge + dedupe", "Dedupe", "canonical URL + title"),
            ("Rank + explain", "Rank", "fresh · fit · source")]
    row2 = [("Question / CV", "Ask", "tutor · review · tailor"), ("Privacy checks", "Checks", "session · CSRF · consent"),
            ("Authored KB", "Knowledge", "retrieval first"), ("Optional LLM", "LLM", "DeepSeek → Groq"),
            ("Guarded output", "Guard", "no invented numbers")]
    b = [panel(t, W, H), pipeline_row(t, 52, "DISCOVERY", row1, t["accent"], .2), pipeline_row(t, 178, "AI PATH", row2, t["amber"], .6),
         f'<g class="dsk">{text(32, 284, "lib/cv/tailor-guardrails.ts rejects fabricated numbers, unsupported requirements and untraceable changes.", 11, t["text3"], "m")}</g>']
    return doc(W, H, "lazyhire architecture",
               "Discovery: career brief, 9 job sources, apply-link validation, merge and dedupe, rank and explain. AI path: question or CV task, privacy and CSRF checks, "
               "authored knowledge retrieval first, optional LLM (DeepSeek then Groq), guarded output that rejects invented numbers.", "".join(b))


def arch_inforge(t):
    H = 270
    a = t["accent"]
    stages = [("Ingest", "Ingest"), ("Clean", "Clean"), ("EDA", "EDA"), ("Visualize", "Viz"),
              ("ML", "ML"), ("Insights", "Insight"), ("Code", "Code"), ("Chat", "Chat")]
    enrich = {0, 2, 3, 5, 7}
    b = [panel(t, W, H),
         f'<rect x="32" y="28" width="816" height="40" rx="9" fill="none" stroke="{t["amber"]}" stroke-opacity=".7" stroke-dasharray="4 5"/>',
         f'<g class="dsk">{text(48, 53, "LLM ENRICHMENT", 11, t["amber"], "m", ls=2)}{text(186, 53, "OpenRouter · Groq · Gemini — optional; local heuristics when a call fails", 12, t["text2"])}</g>',
         f'<g class="mob">{text(440, 58, "LLM enrichment · optional", 23, t["amber"], anchor="middle")}</g>',
         f'<rect x="32" y="200" width="816" height="40" rx="9" fill="{t["raised"]}" stroke="{t["border2"]}"/>',
         f'<g class="dsk">{text(48, 225, "DETERMINISTIC CORE", 11, a, "m", ls=2)}{text(212, 225, "pandas · NumPy · scikit-learn · XGBoost · Matplotlib · ReportLab", 12, t["text2"])}</g>',
         f'<g class="mob">{text(440, 230, "Deterministic core", 23, a, anchor="middle")}</g>']
    for i, (name, short) in enumerate(stages):
        x = 32 + i * 104
        cx = x + 44
        if i in enrich:
            b.append(f'<path d="M{cx} 68V110" stroke="{t["amber"]}" stroke-opacity=".6" stroke-dasharray="3 4"/>')
        b.append(line(cx, 158, cx, 200, a, d=.5 + i * .06, opacity=.45))
        b.append(f'<g class="rise"{delay(.2 + i * .09)}><rect x="{x}" y="110" width="88" height="48" rx="8" fill="{t["raised"]}" stroke="{t["border"]}"/>'
                 f'<g class="dsk">{text(cx, 129, f"0{i + 1}", 9.5, t["text3"], "m", "middle")}{text(cx, 148, name, 13, t["text"], anchor="middle", weight=600)}</g>'
                 f'<g class="mob">{text(cx, 142, short, 19, t["text"], anchor="middle", weight=600)}</g></g>')
        if i < 7:
            b.append(line(x + 89, 134, x + 103, 134, a, d=.6 + i * .08, opacity=.7))
    return doc(W, H, "InForge-AI architecture",
               "Eight stages run in order: ingest, clean, EDA, visualize, ML, insights, code, chat. A deterministic core (pandas, NumPy, scikit-learn, XGBoost, Matplotlib, ReportLab) "
               "computes results; optional LLM enrichment (OpenRouter, Groq, Gemini) writes prose, with local heuristics when a call fails.", "".join(b))


# ------------------------------------------------------------------ technology constellation
STACK = [  # label, (x, y), placement, desktop lines, mobile line
    ("AGENTS", (150, 104), "up", ["LangGraph · CrewAI", "LlamaIndex · Vanna 2.0"], "LangGraph · CrewAI"),
    ("MODELS", (440, 92), "up", ["Groq · Gemini · OpenRouter", "OpenAI SDK · tiktoken"], "Groq · Gemini · OpenRouter"),
    ("BACKEND", (730, 104), "up", ["Python · FastAPI", "WebSockets · Pydantic"], "Python · FastAPI"),
    ("APPLIED ML", (140, 236), "down", ["pandas · NumPy", "scikit-learn · XGBoost"], "pandas · scikit-learn"),
    ("DATA", (740, 236), "down", ["Supabase Postgres · pgvector", "SQLite · Drizzle ORM"], "Supabase · pgvector"),
    ("FRONTEND", (290, 372), "down", ["TypeScript · Next.js · React", "Tailwind · Framer Motion"], "TypeScript · Next.js"),
    ("DELIVERY", (590, 372), "down", ["E2B · Docker · GitHub Actions", "Playwright · Vercel · Render"], "Docker · E2B · Playwright"),
]


def stack(t):
    H = 470
    a = t["accent"]
    cx, cy = 440, 236
    b = [panel(t, W, H), f'<ellipse cx="{cx}" cy="{cy}" rx="300" ry="140" fill="none" stroke="{t["border"]}" stroke-dasharray="2 6"/>']
    import random
    rnd = random.Random(7)
    for i in range(46):
        x, y = rnd.uniform(20, 860), rnd.uniform(20, 450)
        b.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{rnd.choice([.8, 1, 1.3])}" fill="{t["text3"]}" class="dsk" '
                 f'style="opacity:.5;animation:breathe {rnd.uniform(5, 9):.1f}s ease-in-out {rnd.uniform(0, 6):.1f}s infinite"/>')
    for i, (lab, (x, y), *_rest) in enumerate(STACK):
        b.append(line(cx, cy, x, y, a, d=.3 + i * .08, opacity=.35))
    loop = 14
    for i, (lab, (x, y), *_rest) in enumerate(STACK):
        b.append(motion([(cx, cy), (x, y)], [i * 2, i * 2 + 1.2], loop, a, r=2.4))
    b.append(f'<circle cx="{cx}" cy="{cy}" r="58" fill="{t["raised"]}" stroke="{t["border2"]}"/>'
             f'<circle cx="{cx}" cy="{cy}" r="66" fill="none" stroke="{a}" stroke-opacity=".25"/>'
             f'<g class="dsk">{text(cx, cy - 2, "VINAYAK", 15, t["text"], anchor="middle", weight=600, ls=2)}{text(cx + 1, cy + 18, "ENGINEERING STACK", 9, t["text3"], "m", "middle", ls=1.5)}</g>'
             f'<g class="mob">{text(cx, cy + 8, "STACK", 24, t["text"], "m", "middle", ls=2)}</g>')
    desc = []
    for i, (lab, (x, y), place, lines, mline) in enumerate(STACK):
        d = .9 + i * .1
        b.append(f'<g class="fade"{delay(d)}><circle cx="{x}" cy="{y}" r="9" fill="{a}" fill-opacity=".15"/><circle cx="{x}" cy="{y}" r="3.5" fill="{a}"/>')
        if place == "up":
            dy, my = [y - 52, y - 32, y - 15], [y - 50, y - 18]
        else:
            dy, my = [y + 30, y + 50, y + 67], [y + 40, y + 72]
        b.append(f'<g class="dsk">{text(x + 1, dy[0], lab, 11.5, a, "m", "middle", ls=2.5)}'
                 + "".join(text(x, dy[j + 1], s, 13.5, t["text"], anchor="middle") for j, s in enumerate(lines)) + "</g>")
        b.append(f'<g class="mob">{text(x + 1, my[0], lab, 22, a, "m", "middle", ls=1.5)}{text(x, my[1], mline, 21, t["text"], anchor="middle")}</g></g>')
        desc.append(f"{lab.title()}: {', '.join(lines)}")
    return doc(W, H, "Engineering stack", "; ".join(desc).replace(" · ", ", "), "".join(b))


# ------------------------------------------------------------------ section dividers + footer
SECTIONS = [("01", "CONSOLE"), ("02", "SYSTEM MAP"), ("03", "SELECTED SYSTEMS"), ("04", "ARCHITECTURE"),
            ("05", "ENGINEERING NOTES"), ("06", "STACK"), ("07", "ACTIVITY"), ("08", "PRINCIPLES"),
            ("09", "CREDENTIALS"), ("10", "CONTACT")]


def divider(t, num, label):
    H = 48
    a = t["accent"]
    end_d = 36 + len(label) * (12 * .6 + 3) + 14
    end_m = 64 + len(label) * (24 * .6 + 3) + 18
    b = [f'<g class="dsk">{text(2, 30, num, 12, a, "m")}{text(36, 30, label, 12, t["text2"], "m", ls=3)}'
         f'{line(round(end_d), 26, 862, 26, t["border2"], d=.1)}<circle cx="868" cy="26" r="3" fill="{a}"/></g>',
         f'<g class="mob">{text(2, 34, num, 24, a, "m")}{text(64, 34, label, 24, t["text2"], "m", ls=3)}'
         f'{line(round(end_m), 26, 856, 26, t["border2"], d=.1, width=2)}<circle cx="866" cy="26" r="6" fill="{a}"/></g>']
    return doc(W, H, f"{num} {label.title()}", f"Section {num}: {label.title()}", "".join(b))


def footer(t):
    H = 210
    a = t["accent"]
    pts = [(300, 34), (352, 70), (396, 24), (484, 26), (528, 70), (580, 36)]
    b = []
    for i, (x, y) in enumerate(pts):
        b.append(line(x, y, 440, 56, a, d=.2 + i * .1, opacity=.35))
        b.append(f'<circle cx="{x}" cy="{y}" r="2.5" fill="{a}" class="fade"{delay(.1 + i * .08)}/>')
    b.append(f'<circle cx="440" cy="56" r="5" fill="{t["amber"]}"/>'
             f'<circle cx="440" cy="56" r="5" fill="none" stroke="{t["amber"]}"><animate attributeName="r" values="5;16" dur="2.8s" repeatCount="indefinite"/>'
             f'<animate attributeName="opacity" values=".7;0" dur="2.8s" repeatCount="indefinite"/></circle>')
    b.append(f'<g class="dsk rise"{delay(.6)}>{text(443, 132, "SYSTEMS THAT SHOW THEIR WORK", 28, t["text"], anchor="middle", weight=600, ls=5)}'
             f'{text(441, 164, "TRACES  ·  CITATIONS  ·  TESTS  ·  DOCUMENTED LIMITS", 12, t["text3"], "m", "middle", ls=2)}</g>')
    b.append(f'<g class="mob">{text(443, 136, "SYSTEMS THAT", 44, t["text"], anchor="middle", weight=600, ls=4)}'
             f'{text(443, 188, "SHOW THEIR WORK", 44, t["text"], anchor="middle", weight=600, ls=4)}</g>')
    return doc(W, H, "Systems that show their work", "Traces, citations, tests, documented limits.", "".join(b))


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    panels = {"hero": hero, "status": status, "terminal": terminal, "system-map": system_map,
              "card-loom": lambda t: card(t, "loom"), "card-lazyhire": lambda t: card(t, "lazyhire"),
              "card-inforge": lambda t: card(t, "inforge"), "arch-loom": arch_loom,
              "arch-lazyhire": arch_lazyhire, "arch-inforge": arch_inforge, "stack": stack, "footer": footer}
    for num, label in SECTIONS:
        panels[f"sec-{num}"] = (lambda n, l: (lambda t: divider(t, n, l)))(num, label)
    for name, fn in panels.items():
        for theme, t in THEMES.items():
            (OUT / f"{name}-{theme}.svg").write_text(fn(t), encoding="utf-8")
    print(f"wrote {len(panels) * 2} files to {OUT}")


if __name__ == "__main__":
    main()
