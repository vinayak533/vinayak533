"""Animated project films. Each scene replays one system doing its job on a single looping clock.

A Film hands out CSS classes whose keyframes are written in seconds. Every class
shares the loop length and a negative delay that starts playback on the finished
frame, so the first paint, reduced motion and non-animating viewers all show the
completed state.
"""
from theme import V, W, MW, P, MP, R, doc, open_button, surface, text, tw

RED, GREEN, AMBER, VIOLET, BLUE = "#FF8A80", "#7EE2A8", "#FFC078", "#B9A6FB", "#8AB4F8"
STAGE, EDGE = "#0A0A0E", "#26262F"
SPRING = "cubic-bezier(.16,1,.3,1)"


class Film:
    def __init__(self, seconds, hold=3.8):
        self.T, self.hold, self.css, self.seen = seconds, hold, [], {}

    def pct(self, t):
        return f"{max(0, min(100, 100 * t / self.T)):.2f}%"

    def track(self, frames, ease="ease"):
        """frames: [(seconds, css declarations)] -> class name. The last frame is also the resting style."""
        key = (tuple(frames), ease)
        if key not in self.seen:
            n = f"k{len(self.seen)}"
            self.seen[key] = n
            body = "".join(f"{self.pct(t)}{{{c}}}" for t, c in frames)
            self.css.append(f"@keyframes {n}{{{body}}}.{n}{{animation:{n} {self.T}s {ease} {self.hold - self.T:.2f}s infinite}}")
        return self.seen[key]

    def enter(self, t, rise=10):
        """Appear at t, stay until the loop's closing fade."""
        e = self.T - .5
        return self.track([(0, f"opacity:0;transform:translateY({rise}px)"), (t, f"opacity:0;transform:translateY({rise}px)"),
                           (t + .55, "opacity:1;transform:none"), (e, "opacity:1;transform:none"), (self.T, "opacity:0;transform:none")], SPRING)

    def between(self, a, b):
        """Visible only from a to b; hidden in the finished frame."""
        return self.track([(0, "opacity:0"), (a, "opacity:0"), (a + .15, "opacity:1"), (b, "opacity:1"), (b + .15, "opacity:0"), (self.T, "opacity:0")])

    def grow(self, a, b, axis="X", ease="linear"):
        z, o = f"transform:scale{axis}(0)", f"transform:scale{axis}(1)"
        return self.track([(0, z), (a, z), (b, o), (self.T - .5, o), (self.T - .45, z), (self.T, z)], ease)

    def sheet(self):
        # Between-only elements are invisible when nothing animates.
        return "".join(self.css) + ".box{transform-box:fill-box}.l{transform-origin:left center}.rt{transform-origin:right center}.b{transform-origin:center bottom}.ctr{transform-origin:center}.gone{opacity:0}"


    def pop(self, t):
        """Land with a small overshoot, for verdicts."""
        e = self.T - .5
        return self.track([(0, "opacity:0;transform:scale(.4)"), (t, "opacity:0;transform:scale(.4)"), (t + .22, "opacity:1;transform:scale(1.18)"),
                           (t + .42, "opacity:1;transform:scale(1)"), (e, "opacity:1;transform:scale(1)"), (self.T, "opacity:0;transform:scale(1)")], "ease-out")

    def flash(self, t, dur=.9, peak=1):
        return self.track([(0, "opacity:0"), (t, "opacity:0"), (t + .12, f"opacity:{peak}"), (t + dur, "opacity:0"), (self.T, "opacity:0")], "ease-out")

    def type(self, a, b):
        """Cover that retracts to the right, so text underneath looks typed."""
        return self.track([(0, "transform:scaleX(1)"), (a, "transform:scaleX(1)"), (b, "transform:scaleX(0)"),
                           (self.T - .02, "transform:scaleX(0)"), (self.T, "transform:scaleX(1)")], "linear")


def beam(w, h, color, seconds=9):
    """A light that travels around the card's edge."""
    r = (f'<rect class="{{c}} motion" x=".75" y=".75" width="{w - 1.5}" height="{h - 1.5}" rx="{R}" fill="none" stroke="{color}" pathLength="100" '
         'stroke-dasharray="{d} {g}" stroke-linecap="round" stroke-width="{s}" stroke-opacity="{o}"/>')
    css = "@keyframes bm{to{stroke-dashoffset:-100}}" + "".join(f".bm{i}{{animation:bm {seconds}s linear {dl:.2f}s infinite}}" for i, dl in enumerate((0, -.18, -.36)))
    body = "".join(r.format(c=f"bm{i}", d=d, g=100 - d, s=s, o=o) for i, (d, s, o) in enumerate(((12, 1.5, .35), (8, 1.5, .6), (4, 2.2, 1))))
    return body, css


def g(cls, body):
    return f'<g class="{cls}">{body}</g>'


def panel(x, y, w, h, rx=14, fill=STAGE, edge=EDGE):
    return f'<rect x="{x + .5:g}" y="{y + .5:g}" width="{w - 1:g}" height="{h - 1:g}" rx="{rx}" fill="{fill}" stroke="{edge}"/>'


def tick(x, y, c, s=1.0):
    return f'<path d="M{x - 4 * s:.1f} {y:.1f}l{3 * s:.1f} {3 * s:.1f} {5.5 * s:.1f}-{6 * s:.1f}" fill="none" stroke="{c}" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/>'


def cross(x, y, c):
    return f'<path d="M{x - 3.5} {y - 3.5}l7 7m0-7l-7 7" stroke="{c}" stroke-width="1.8" stroke-linecap="round"/>'


def head(name, tag, w, p, m, role):
    b = [text(p, 46 if m else 52, role, 13.5 if m else 14, V["text3"]),
         text(p, 92 if m else 104, name, 40 if m else 46, V["text"], weight=600, ls=-1.2), open_button(w - p - 20, 46 if m else 54, 20)]
    b += [text(p, (126 if m else 140) + i * 24, s, 16.5 if m else 18, V["text2"]) for i, s in enumerate(tag)]
    return "".join(b)


# ------------------------------------------------------------------ loom.ai
CALLS = [("Terminal", "npm create vite@latest pomodoro", "290ms"), ("Write", "pomodoro/src/App.tsx", "141ms"),
         ("Write", "pomodoro/src/Timer.tsx", "155ms"), ("Dev server", "npm run dev · :5173", "240ms")]
CODE = ['import { useEffect, useReducer } from "react";', 'import { Timer } from "./Timer";', "", "const WORK = 25 * 60;", "const BREAK = 5 * 60;", "",
        'type Mode = "work" | "break";', "type State = {", "  mode: Mode;", "  left: number;", "  running: boolean;", "};"]
PATH = [("Next.js", "trace UI"), ("FastAPI", "WebSocket"), ("LangGraph", "StateGraph"), ("Router", "fallback"), ("Tools", "bash, fs, git"), ("E2B", "Linux sandbox")]
LOOM_DESC = ("loom.ai, flagship agent workspace: a coding agent inside a real Linux sandbox that streams every tool call. "
             "Animated replay of the repository's scripted demo turn: a prompt is sent, terminal, write and dev-server calls complete, and App.tsx is written. "
             "Request path: Next.js, FastAPI WebSocket, LangGraph, model router with fallback, tools, E2B sandbox. "
             "A race drawn in real seconds compares median time-to-first-token before, 8.9s, and after prompt caching, 5.0s. "
             "8 models across Groq, OpenRouter and OpenCode; 10 specialist agents with human approval.")


def code_line(x, y, s, size):
    """Mono line with light syntax colour."""
    lead = len(s) - len(s.lstrip())
    words, out = s.lstrip().split(" "), []
    for i, wd in enumerate(words):
        c = VIOLET if wd in ("import", "from", "const", "type") else GREEN if wd.startswith('"') else AMBER if wd.strip(";").isdigit() else "#C9CCD6"
        out.append(f'<tspan fill="{c}">{wd.replace("&", "&amp;").replace("<", "&lt;")}{" " if i < len(words) - 1 else ""}</tspan>')
    return f'<text x="{x + lead * size * .6:g}" y="{y:g}" class="m" font-size="{size}" xml:space="preserve">{"".join(out)}</text>'


def loom_trace(f, x, y, w, m):
    """The agent's turn: prompt, then timed tool calls."""
    b, fs = [], 13.5 if m else 13
    prompt = ["Build a Pomodoro timer with React and", "Vite, then start it so I can try it."]
    pw = 292 if m else 300
    b.append(g(f.enter(.5), panel(x + w - pw, y, pw, 58, 14, "#1D1D27", "#33333F")
               + "".join(text(x + w - pw + 16, y + 24 + i * 20, s, fs, "#F4F5F6") for i, s in enumerate(prompt))
               + "".join(f'<rect class="box rt {f.type(.8 + i * .55, 1.35 + i * .55)}" style="transform:scaleX(0)" x="{x + w - pw + 12}" y="{y + 9 + i * 20}" '
                         f'width="{pw - 24}" height="20" fill="#1D1D27"/>' for i in range(2))))
    rowy, rh = y + 74, 44
    for i, (tool, arg, ms) in enumerate(CALLS):
        t, yy = 2.1 + i * 1.0, rowy + i * rh
        b.append(g(f.enter(t), panel(x, yy, w, 37, 10, "#111118")
                   + text(x + 38, yy + 23.5, tool, fs, "#F4F5F6", weight=600)
                   + text(x + (112 if not m else 116), yy + 23.5, arg if not m else arg.replace("pomodoro/", ""), fs - 1 if not m else fs - 1.5, "#A9ADBA", True)
                   + (text(x + w - 14, yy + 23.5, ms, fs, "#8D929B", anchor="end") if not m else "")))
        b.append(g(f.between(t + .1, t + .7) + " gone", f'<circle cx="{x + 19}" cy="{yy + 18.5}" r="6" fill="none" stroke="{BLUE}" stroke-width="2" '
                   f'stroke-dasharray="22 16"><animateTransform attributeName="transform" type="rotate" from="0 {x + 19} {yy + 18.5}" to="360 {x + 19} {yy + 18.5}" dur=".7s" repeatCount="indefinite"/></circle>'))
        b.append(f'<rect class="{f.flash(t + .72, .8, .5)} gone" x="{x + .5}" y="{yy + .5}" width="{w - 1}" height="36" rx="10" fill="{GREEN}" fill-opacity=".12" stroke="{GREEN}"/>')
        b.append(f'<g class="box ctr {f.pop(t + .72)}">{tick(x + 19, yy + 18.5, GREEN, 1.15)}</g>')
    yy = rowy + 4 * rh + 20
    b.append(g(f.enter(6.3), text(x, yy, "The timer is live on port 5173.", fs + 1, "#F4F5F6", weight=600)))
    return "".join(b)


def loom_code(f, x, y, w, lines, size):
    b = [text(x, y, "App.tsx", 13, "#F4F5F6", weight=600), g(f.enter(3.1, 0), text(x + w, y, "modified", 12.5, AMBER, anchor="end")),
         f'<path d="M{x} {y + 14}H{x + w}" stroke="{EDGE}"/>']
    lh, t0 = size + 7.6, 3.2
    fr = [(0, "transform:translateY(0);opacity:0"), (t0 - .05, "transform:translateY(0);opacity:0")]
    for i in range(lines):
        fr += [(t0 + i * .17, f"transform:translateY({i * lh:.1f}px);opacity:1"), (t0 + i * .17 + .16, f"transform:translateY({i * lh:.1f}px);opacity:1")]
    fr += [(t0 + lines * .17 + .5, f"transform:translateY({(lines - 1) * lh:.1f}px);opacity:0"), (f.T, f"transform:translateY({(lines - 1) * lh:.1f}px);opacity:0")]
    b.append(f'<rect class="{f.track(fr, "linear")} gone" x="{x - 8}" y="{y + 38 - lh * .74:.1f}" width="{w + 16}" height="{lh:.1f}" rx="5" fill="{VIOLET}" fill-opacity=".16"/>')
    for i, s in enumerate(CODE[:lines]):
        yy = y + 38 + i * (size + 7.6)
        b.append(text(x + 14, yy, str(i + 1), size - 1, "#555A66", True, anchor="end"))
        if s:
            b.append(g(f.enter(3.2 + i * .17, 0), code_line(x + 28, yy, s, size)))
    return "".join(b)


def race(f, x, y, w, m):
    """Both bars run at the true speed of the measurement: 8.9 and 5.0 wall-clock seconds."""
    start, k = .6, w / 8.9
    b = [text(x, y, "Median time to first token, raced in real seconds" if not m else "Time to first token, in real seconds", 14.5, V["text2"])]
    for i, (lab, sec, col) in enumerate((("before", 8.9, "#3A3A46"), ("with prompt caching", 5.0, VIOLET))):
        yy = y + 18 + i * 46
        bw = sec * k
        b.append(f'<rect x="{x}" y="{yy}" width="{w}" height="36" rx="10" fill="#0F0F15"/>')
        b.append(text(x + 14, yy + 23.5, lab, 14, "#C9CCD6", weight=600))
        b.append(f'<rect class="box l {f.grow(start, start + sec)}" x="{x}" y="{yy}" width="{bw:.1f}" height="36" rx="10" fill="{col}"/>')
        if not i:
            b.append(text(x + 14, yy + 23.5, lab, 14, "#E4E6EC", weight=600))
        if i:   # the label turns dark exactly where the bar has passed
            b.append(f'<defs><clipPath id="lb"><rect class="box l {f.grow(start, start + sec)}" x="{x}" y="{yy}" width="{bw:.1f}" height="36"/></clipPath></defs>'
                     f'<g clip-path="url(#lb)">{text(x + 14, yy + 23.5, lab, 14, "#120A2E", weight=600)}</g>')
        num = f"{sec:.1f}s"
        nx, n, row = (x + bw + 14 if i else x + w - 14), round(sec * 10), 26
        strip = "".join(text(nx, yy + 24.5 + (k - n) * row, f"{k / 10:.1f}s", 18, "#F4F5F6", weight=600, anchor="start" if i else "end") for k in range(n + 1))
        up, dn = f"transform:translateY({n * row}px)", "transform:translateY(0)"
        roll = f.track([(0, up), (start, up + f";animation-timing-function:steps({n})"), (start + sec, dn), (f.T - .5, dn), (f.T - .45, up), (f.T, up)], "linear")
        b.append(f'<defs><clipPath id="rc{i}"><rect x="{nx - (4 if i else 70)}" y="{yy + 6}" width="74" height="{row - 2}"/></clipPath></defs>'
                 f'<g clip-path="url(#rc{i})"><g class="{roll}">{strip}</g></g>')
        b.append(f'<rect class="{f.flash(start + sec, 1.3)} gone" x="{x + .75}" y="{yy + .75}" width="{bw - 1.5:.1f}" height="34.5" rx="10" fill="none" stroke="#FFF" stroke-width="2"/>')
    return "".join(b)


def loom(m=False):
    f, b = Film(14.8), []
    if m:
        w, p = MW, MP
        b.append(head("loom.ai", ["A coding agent in a real Linux", "sandbox that streams every tool call."], w, p, True, "Flagship"))
        b += [panel(12, 180, w - 24, 310), loom_trace(f, 28, 198, w - 56, True)]
        b += [panel(12, 502, w - 24, 206), loom_code(f, 28, 530, w - 56, 7, 11.5)]
        y = 748
        for i, (a, s) in enumerate(PATH):
            yy = y + (i // 2) * 52
            x = p + (i % 2) * 178
            b += [g(f.enter(.9 + i * .35), text(x, yy, a, 16, V["text"], weight=600) + text(x, yy + 20, s, 13.5, V["text3"]))]
        b.append(race(f, p, y + 170, w - 2 * p, True))
        y2 = y + 170 + 148
        b += [text(p, y2, "8 models", 24, V["text"], weight=600, ls=-.4), text(p, y2 + 22, "across three providers", 14, V["text2"]),
              text(p + 178, y2, "10 agents", 24, V["text"], weight=600, ls=-.4), text(p + 178, y2 + 22, "with human approval", 14, V["text2"])]
        h = y2 + 50
    else:
        w, p, h = W, P, 758
        b.append(head("loom.ai", ["A coding agent inside a real Linux sandbox that streams every tool call."], w, p, False, "Flagship"))
        b += [panel(20, 172, w - 40, 312), f'<path d="M500 172V484" stroke="{EDGE}"/>',
              loom_trace(f, 44, 196, 432, False), loom_code(f, 524, 206, 312, 12, 11.5)]
        y, seg = 520, (w - 2 * p - 92) / 5
        b.append(f'<path d="M{p + 6} {y}H{p + 6 + seg * 5}" stroke="{EDGE}" stroke-width="2"/>')
        b.append(f'<rect class="box l {f.grow(.9, 3.2)}" x="{p + 6}" y="{y - 1}" width="{seg * 5:.1f}" height="2" fill="{BLUE}"/>')
        for i, (a, s) in enumerate(PATH):
            x = p + 6 + i * seg
            b += [f'<circle cx="{x:.1f}" cy="{y}" r="5.5" fill="#000" stroke="{EDGE}" stroke-width="2"/>',
                  f'<circle class="{f.enter(.9 + i * .46, 0)}" cx="{x:.1f}" cy="{y}" r="5.5" fill="{BLUE}"/>',
                  text(x - 6, y + 30, a, 15, V["text"], weight=600), text(x - 6, y + 50, s, 13, V["text3"])]
        b.append(f'<path d="M{p} 594H{w - p}" stroke="{EDGE}"/>')
        b.append(race(f, p, 626, 556, False))
        for i, (v, lab) in enumerate((("8 models", "Groq, OpenRouter, OpenCode"), ("10 agents", "specialists, human approval"))):
            b += [text(640, 640 + i * 60, v, 26, V["text"], weight=600, ls=-.5), text(640, 662 + i * 60, lab, 14, V["text2"])]
    bm, bcss = beam(w, h, BLUE)
    return doc(w, h, "loom.ai", LOOM_DESC, surface(w, h) + "".join(b) + bm, f.sheet() + bcss)


# ------------------------------------------------------------------ lazyhire
SRC = ["Technopark", "Infopark", "UL CyberPark", "Indeed India", "Evanios Jobs", "Google Jobs"]
FATE = {1: (1, "dead link"), 3: (2, "duplicate"), 4: (1, "dead link")}
WIN = [(0, "React Platform Engineer", "Matched: react, typescript"), (2, "Frontend Quality Engineer", "Matched: playwright, react"), (5, "Ranked lower", "")]
LAZY_DESC = ("lazyhire: a private career workspace that ranks Kerala job listings against your CV. Animated illustration with fixture listings: "
             "postings from several of its nine sources move through apply-link validation, deduplication and ranking; dead links and duplicates drop out, "
             "and survivors are ranked with the reason they match. A CV draft line that cannot be traced to the source CV is struck out and rejected. "
             "Next.js 16, React 19, TypeScript, SQLite with Drizzle, Playwright. Zero-fabrication CV guardrails.")


def lazyhire(m=False):
    f, b = Film(13.8), []
    if m:
        w, p = MW, MP
        b.append(head("lazyhire", ["A private career workspace that ranks", "Kerala job listings against your CV."], w, p, True, "Career workspace"))
        sx, sy, sw, sh, rowh, pill, g1, g2, end = 12, 180, w - 24, 296, 38, 104, 150, 240, 272
        ox, oy = sx + 14, sy + 52
        cards = (12, 488, w - 24, 72)
    else:
        w, p = W, P
        b.append(head("lazyhire", ["A private career workspace that ranks Kerala job listings against your CV."], w, p, False, "Career workspace"))
        sx, sy, sw, sh, rowh, pill, g1, g2, end = 20, 172, w - 40, 286, 36, 112, 206, 340, 376
        ox, oy = sx + 20, sy + 54
        cards = (sx + 544, sy + 46, 276, 70)
    b.append(panel(sx, sy, sw, sh))
    labels = [(ox, "9 sources"), (ox + g1 - 8, "validate" if m else "validate links"), (ox + g2 - 8, "dedupe")]
    b += [text(x, sy + 30, s, 13, V["text3"]) for x, s in labels]
    for gx in (g1, g2):
        b.append(f'<path d="M{ox + gx - 8} {sy + 44}V{sy + sh - 18}" stroke="{EDGE}" stroke-width="1.5" stroke-dasharray="2 6" stroke-linecap="round"/>')
    for i, s in enumerate(SRC):
        yy = oy + i * rowh + 2
        t0 = .4 + i * .28
        fate = FATE.get(i)
        col, dist = ("#17171F", end)
        if fate:
            stop, why = (g1 if fate[0] == 1 else g2) - pill - 4, fate[1]
            t1 = t0 + (1.5 if fate[0] == 1 else 2.5)
            mv = f.track([(0, "opacity:0;transform:translateX(0)"), (t0, "opacity:0;transform:translateX(0)"), (t0 + .3, "opacity:1;transform:translateX(0)"),
                          (t1, f"opacity:1;transform:translateX({stop}px)"), (t1 + .07, f"opacity:1;transform:translateX({stop - 9}px)"),
                          (t1 + .15, f"opacity:1;transform:translateX({stop + 3}px)"), (t1 + .23, f"opacity:.8;transform:translateX({stop - 3}px)"),
                          (t1 + .6, f"opacity:.28;transform:translateX({stop}px)"),
                          (f.T - .5, f"opacity:.28;transform:translateX({stop}px)"), (f.T, f"opacity:0;transform:translateX({stop}px)")], "ease-in-out")
            base = f' style="transform:translateX({stop}px);opacity:.28"'
        else:
            t1 = t0 + 3.4
            mv = f.track([(0, "opacity:0;transform:translateX(0)"), (t0, "opacity:0;transform:translateX(0)"), (t0 + .3, "opacity:1;transform:translateX(0)"),
                          (t1, f"opacity:1;transform:translateX({end if not m else end - 30}px)"),
                          (f.T - .5, f"opacity:1;transform:translateX({end if not m else end - 30}px)"), (f.T, f"opacity:0;transform:translateX({end if not m else end - 30}px)")], "ease-in-out")
            base = f' style="transform:translateX({end if not m else end - 30}px)"'
        body = (f'<rect x="{ox}" y="{yy}" width="{pill}" height="28" rx="14" fill="{col}" stroke="{"#33333F" if fate else "#2F6B4A"}"/>'
                + text(ox + pill / 2, yy + 18.6, s, 13, "#E6E8EE" if fate else "#CFF5DD", weight=500, anchor="middle"))
        b.append(f'<g class="{mv}"{base}>{body}</g>')
        if fate:
            xx = ox + stop + pill + 18
            gx = ox + (g1 if fate[0] == 1 else g2) - 8
            b.append(f'<path class="{f.flash(t1, .9)} gone" d="M{gx} {sy + 44}V{sy + sh - 18}" stroke="{RED}" stroke-width="2"/>')
            b.append(f'<g class="box ctr {f.pop(t1 + .08)}">{cross(xx, yy + 14, RED)}{text(xx + 12, yy + 18.6, why, 13, RED, weight=500)}</g>')
        else:
            xx = ox + (end if not m else end - 30)
    cx, cy, cw, ch = cards
    if not m:
        b.append(f'<path d="M{cx - 22} {sy}V{sy + sh}" stroke="{EDGE}"/>')
        b.append(text(cx, sy + 30, "rank and explain", 13, V["text3"]))
    for i, (_, title, why) in enumerate(WIN):
        yy = cy + i * (ch + 8)
        t = 4.9 + i * .55
        op = 1 if i < 2 else .5
        inner = (panel(cx, yy, cw, ch, 12, "#101B16" if i < 2 else "#0F0F14", "#25523A" if i < 2 else EDGE)
                 + text(cx + 18, yy + ch / 2 + 8, str(i + 1), 24, GREEN if i < 2 else V["text3"], weight=600)
                 + text(cx + 50, yy + (28 if why else 42), title, 15.5, "#F4F5F6" if i < 2 else V["text3"], weight=600))
        if why:
            inner += text(cx + 50, yy + 49, why, 13.5, GREEN)
        if i < 2:
            fit = cw - 100
            inner += (f'<rect x="{cx + 50}" y="{yy + ch - 8}" width="{fit}" height="3" rx="1.5" fill="#1E3A2B"/>'
                      f'<rect class="box l {f.grow(t + .4, t + 1.3, "X", "ease-out")}" x="{cx + 50}" y="{yy + ch - 8}" width="{fit * .93:.0f}" height="3" rx="1.5" fill="{GREEN}"/>')
        b.append(g(f.enter(t, 26), inner))
    yg = (cy + 3 * (ch + 8) + 14) if m else sy + sh + 14
    gh = 168 if m else 112
    b.append(panel(sx, yg, sw, gh))
    gx = sx + 20
    b.append(text(gx, yg + 30, "CV draft check", 13, V["text3"]))
    good, bad = "Built React dashboards with tests", "Led a team of 40 engineers"
    if m:
        l1, l2 = (gx, yg + 60), (gx, yg + 118)
    else:
        l1, l2 = (gx, yg + 66), (gx + 420, yg + 66)
    t = 7.0
    b.append(g(f.enter(t), text(l1[0] + 20, l1[1], good, 16, "#F4F5F6")) + g(f.enter(t + .7, 0), tick(l1[0] + 4, l1[1] - 5, GREEN, 1.2)
             + text(l1[0] + 20, l1[1] + 21, "traced to the source CV", 13, GREEN)))
    bw = tw(bad, 16) * .97
    for (lx, ly), ts in ((l1, t + .2), (l2, t + 1.4)):   # a reading light passes over each claim before its verdict
        mv = f.track([(0, "opacity:0;transform:translateX(0)"), (ts, "opacity:0;transform:translateX(0)"), (ts + .05, "opacity:1;transform:translateX(0)"),
                      (ts + .6, "opacity:1;transform:translateX(210px)"), (ts + .65, "opacity:0;transform:translateX(210px)"), (f.T, "opacity:0;transform:translateX(210px)")], "ease-in-out")
        b.append(f'<rect class="{mv} gone" x="{lx + 18}" y="{ly - 18}" width="26" height="25" rx="5" fill="#FFF" fill-opacity=".22"/>')
    b.append(g(f.enter(t + 1.2), text(l2[0] + 20, l2[1], bad, 16, "#F4F5F6"))
             + f'<rect class="box l {f.grow(t + 2, t + 2.5)}" x="{l2[0] + 18}" y="{l2[1] - 6.5}" width="{bw:.0f}" height="2" rx="1" fill="{RED}"/>'
             + g(f.enter(t + 2.5, 0), cross(l2[0] + 4, l2[1] - 5, RED) + text(l2[0] + 20, l2[1] + 21, "not in the source CV, rejected", 13, RED)))
    yf = yg + gh + 34
    if m:
        b += [text(p, yf, "Next.js 16, React 19, TypeScript,", 14.5, V["text2"]), text(p, yf + 21, "SQLite with Drizzle, Playwright", 14.5, V["text2"]),
              text(p, yf + 52, "Zero-fabrication CV guardrails", 16, GREEN, weight=600)]
        h = yf + 78
    else:
        b += [text(p, yf + 2, "Next.js 16, React 19, TypeScript, SQLite with Drizzle, Playwright", 14.5, V["text2"]),
              text(w - p, yf + 2, "Zero-fabrication CV guardrails", 16, GREEN, weight=600, anchor="end")]
        h = yf + 30
    bm, bcss = beam(w, h, GREEN)
    return doc(w, h, "lazyhire", LAZY_DESC, surface(w, h) + "".join(b) + bm, f.sheet() + bcss)


# ------------------------------------------------------------------ InForge-AI
STEPS = ["ingest", "clean", "EDA", "visualize", "benchmark", "insights", "code", "chat"]
INF_DESC = ("InForge-AI: eight pipeline agents turn a CSV or Excel file into analysis, models and a report. Animated illustration: "
            "ingest, clean, EDA, visualize, ML benchmark, insights, code and chat run in order; missing cells are repaired, a trend is drawn, candidate models are compared. "
            "At insights the LLM provider fails, a local fallback takes over, and the run still completes. "
            "FastAPI, WebSockets, pandas, scikit-learn, XGBoost, React. Completes without an LLM provider.")


def inforge(m=False):
    f, b = Film(13.8), []
    at = [.6 + i * .95 for i in range(8)]
    at = [t + (1.1 if i > 5 else 0) for i, t in enumerate(at)]
    run = [t + (1.1 if i == 5 else 0) for i, t in enumerate(at)]       # insights pauses while it fails over
    role = "Analytics pipeline"
    if m:
        w, p = MW, MP
        b.append(head("InForge-AI", ["Eight agents turn a CSV or Excel file", "into analysis, models and a report."], w, p, True, role))
        for i, s in enumerate(STEPS):
            x, y = p + (i % 4) * 92, 190 + (i // 4) * 48
            b += [f'<rect x="{x}" y="{y}" width="80" height="4" rx="2" fill="{EDGE}"/>',
                  f'<rect class="box l {f.grow(run[i], run[i] + .8)}" x="{x}" y="{y}" width="80" height="4" rx="2" fill="{AMBER}"/>',
                  text(x, y + 24, s, 14, V["text"], weight=500)]
        boxes = [(12, 296, w - 24, 190), (12, 498, w - 24, 190), (12, 700, w - 24, 190)]
        log = (12, 902, w - 24, 112)
    else:
        w, p = W, P
        b.append(head("InForge-AI", ["Eight pipeline agents turn a CSV or Excel file into analysis, models and a report."], w, p, False, role))
        seg = (w - 2 * p + 12) / 8
        for i, s in enumerate(STEPS):
            x = p + i * seg
            b += [f'<rect x="{x:.1f}" y="178" width="{seg - 12:.1f}" height="4" rx="2" fill="{EDGE}"/>',
                  f'<rect class="box l {f.grow(run[i], run[i] + .8)}" x="{x:.1f}" y="178" width="{seg - 12:.1f}" height="4" rx="2" fill="{AMBER}"/>',
                  text(x, 205, s, 14.5, V["text"], weight=500)]
        bw = (w - 40 - 24) / 3
        boxes = [(20 + i * (bw + 12), 226, bw, 190) for i in range(3)]
        log = (20, 428, w - 40, 64)
    titles = ["Cleaned data", "Trend", "Model benchmark"]
    for (x, y, bw, bh), s in zip(boxes, titles):
        b += [panel(x, y, bw, bh), text(x + 18, y + 30, s, 13.5, V["text3"])]
    # 1: a table whose missing cells get repaired
    x, y, bw, bh = boxes[0]
    cols, rows = 5, 5
    cw = (bw - 36 + 6) / cols
    missing = {(1, 1), (3, 0), (2, 3), (4, 2), (0, 4)}
    for r in range(rows):
        for c in range(cols):
            xx, yy = x + 18 + c * cw, y + 46 + r * 26
            ln = cw - 6
            if (c, r) in missing:
                t = at[1] + .15 * (c + r)
                b.append(g(f.enter(at[0] + .04 * (c + r), 0), f'<rect x="{xx:.1f}" y="{yy}" width="{ln:.1f}" height="19" rx="5" fill="none" stroke="{RED}" stroke-opacity=".55" stroke-dasharray="3 3"/>'))
                b.append(f'<rect class="box ctr {f.grow(t, t + .3, "", "ease-out")}" x="{xx - 1:.1f}" y="{yy - 1}" width="{ln + 2:.1f}" height="21" rx="6" fill="{AMBER}"/>')
            else:
                b.append(g(f.enter(at[0] + .04 * (c + r), 0), f'<rect x="{xx:.1f}" y="{yy}" width="{ln:.1f}" height="19" rx="5" fill="#22222C"/>'))
    # 2: scatter, then the fitted trend draws itself
    x, y, bw, bh = boxes[1]
    from theme import rng
    r = rng(11)
    x0, x1, y0, y1 = x + 20, x + bw - 20, y + bh - 24, y + 52
    for i in range(34):
        u = (i + .5) / 34
        px, py = x0 + (x1 - x0) * u, y0 + (y1 - y0) * (u ** 1.5 * .88 + .05) + r.gauss(0, 11)
        py = min(max(py, y + 44), y + bh - 14)
        b.append(f'<circle class="{f.enter(at[2] + u * .7, 0)}" cx="{px:.1f}" cy="{py:.1f}" r="2.8" fill="#8F8F9C"/>')
    pts = [(x0 + (x1 - x0) * k / 16, y0 + (y1 - y0) * ((k / 16) ** 1.5 * .88 + .05)) for k in range(17)]
    ln = sum(((a[0] - c[0]) ** 2 + (a[1] - c[1]) ** 2) ** .5 for a, c in zip(pts, pts[1:])) + 4
    dr = f.track([(0, f"stroke-dashoffset:{ln:.0f}"), (at[3], f"stroke-dashoffset:{ln:.0f}"), (at[3] + 1, "stroke-dashoffset:0"),
                  (f.T - .5, "stroke-dashoffset:0"), (f.T - .4, f"stroke-dashoffset:{ln:.0f}"), (f.T, f"stroke-dashoffset:{ln:.0f}")], "ease-in-out")
    b.append(f'<path class="{dr}" d="M{" L".join(f"{a:.1f} {c:.1f}" for a, c in pts)}" fill="none" stroke="{AMBER}" stroke-width="3" stroke-linecap="round" stroke-dasharray="{ln:.0f}"/>')
    # 3: candidates compared, the best one kept
    x, y, bw, bh = boxes[2]
    n, hs = 5, [.52, .70, .61, .93, .78]
    cw = (bw - 40) / n
    for i, v in enumerate(hs):
        bh2 = 108 * v
        xx, yb = x + 20 + i * cw + 5, y + bh - 20
        best = v == max(hs)
        b.append(f'<rect class="box b {f.grow(at[4] + i * .1, at[4] + .6 + i * .1, "Y", "ease-out")}" x="{xx:.1f}" y="{yb - bh2:.1f}" width="{cw - 10:.1f}" height="{bh2:.1f}" rx="6" fill="{"#33333F" if not best else AMBER}"/>')
        if best:
            b.append(g(f.enter(at[4] + 1, 4), text(xx + (cw - 10) / 2, yb - bh2 - 9, "kept", 13.5, AMBER, weight=600, anchor="middle")))
    # log: the provider fails, the run does not
    x, y, lw, lh = log
    b.append(panel(x, y, lw, lh))
    t = at[5]
    b.append(f'<rect class="{f.flash(t, 1.0)} gone" x="{x + .75}" y="{y + .75}" width="{lw - 1.5}" height="{lh - 1.5}" rx="14" fill="{RED}" fill-opacity=".10" stroke="{RED}" stroke-width="1.5"/>')
    b.append(f'<rect class="{f.flash(at[7] + .9, 1.4)} gone" x="{x + .75}" y="{y + .75}" width="{lw - 1.5}" height="{lh - 1.5}" rx="14" fill="{GREEN}" fill-opacity=".08" stroke="{GREEN}" stroke-width="1.5"/>')
    if m:
        ix, iy, iw = p + 92, 238, 80
    else:
        ix, iy, iw = p + 5 * seg, 178, seg - 12
    stuck = f.track([(0, "opacity:0"), (t, "opacity:0"), (t + .1, "opacity:1"), (t + .3, "opacity:.3"), (t + .5, "opacity:1"), (t + .7, "opacity:.3"), (t + .9, "opacity:1"),
                     (t + 1.1, "opacity:0"), (f.T, "opacity:0")])
    b.append(f'<rect class="{stuck} gone" x="{ix:.1f}" y="{iy}" width="{iw:.1f}" height="4" rx="2" fill="{RED}"/>')
    parts = [(t, RED, "LLM provider unavailable", cross), (t + .9, AMBER, "Local fallback takes over", None), (at[7] + .9, GREEN, "Report complete", tick)]
    for i, (tt, c, s, mark) in enumerate(parts):
        if m:
            xx, yy = x + 22, y + 32 + i * 29
        else:
            xx, yy = x + 24 + i * 272, y + 37
        mk = mark(xx + 4, yy - 5, c) if mark else f'<path d="M{xx} {yy - 5}h9m-4-4l4 4-4 4" fill="none" stroke="{c}" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/>'
        b.append(g(f.enter(tt), mk + text(xx + 22, yy, s, 16, c, weight=600)))
    yf = y + lh + 36
    if m:
        b += [text(p, yf, "FastAPI, WebSockets, pandas,", 14.5, V["text2"]), text(p, yf + 21, "scikit-learn, XGBoost, React", 14.5, V["text2"]),
              text(p, yf + 52, "Completes without an LLM provider", 16, AMBER, weight=600)]
        h = yf + 78
    else:
        b += [text(p, yf, "FastAPI, WebSockets, pandas, scikit-learn, XGBoost, React", 14.5, V["text2"]),
              text(w - p, yf, "Completes without an LLM provider", 16, AMBER, weight=600, anchor="end")]
        h = yf + 28
    bm, bcss = beam(w, h, AMBER)
    return doc(w, h, "InForge-AI", INF_DESC, surface(w, h) + "".join(b) + bm, f.sheet() + bcss)
