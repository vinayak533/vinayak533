#!/usr/bin/env python3
"""Render the last year of contributions as assets/svg/activity-{dark,light}.svg.

    GITHUB_TOKEN=... python tools/profile/activity.py     # GraphQL (CI)
    python tools/profile/activity.py                      # public calendar page (local)

Cells light up in calendar order, then each active day links to the next active
day within a week, so streaks read as connected chains. It always uses real data
and exits non-zero rather than inventing a grid.
"""
import datetime as dt
import json
import os
import pathlib
import re
import sys
import urllib.request

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from theme import THEMES, W, doc, panel, text, delay, motion  # noqa: E402

LOGIN = os.environ.get("GH_LOGIN", "vinayak533")
TOKEN = os.environ.get("GITHUB_TOKEN", "")
OUT = pathlib.Path(__file__).resolve().parents[2] / "assets" / "svg"
LEVEL = {"NONE": 0, "FIRST_QUARTILE": 1, "SECOND_QUARTILE": 2, "THIRD_QUARTILE": 3, "FOURTH_QUARTILE": 4}


def fetch_graphql():
    q = """query($l:String!){user(login:$l){contributionsCollection{contributionCalendar{
      totalContributions weeks{contributionDays{date contributionCount contributionLevel}}}}}}"""
    req = urllib.request.Request("https://api.github.com/graphql", data=json.dumps({"query": q, "variables": {"l": LOGIN}}).encode(),
                                 headers={"Authorization": f"bearer {TOKEN}", "Content-Type": "application/json"})
    cal = json.load(urllib.request.urlopen(req, timeout=30))["data"]["user"]["contributionsCollection"]["contributionCalendar"]
    days = [(d["date"], d["contributionCount"], LEVEL[d["contributionLevel"]]) for w in cal["weeks"] for d in w["contributionDays"]]
    return days, cal["totalContributions"]


def fetch_public():
    html = urllib.request.urlopen(f"https://github.com/users/{LOGIN}/contributions", timeout=30).read().decode()
    cells = re.findall(r'data-date="(\d{4}-\d{2}-\d{2})"[^>]*?id="([^"]+)"[^>]*?data-level="(\d)"', html)
    tips = dict(re.findall(r'<tool-tip[^>]*for="([^"]+)"[^>]*>([^<]*)</tool-tip>', html))
    days = []
    for date, cid, lvl in cells:
        m = re.match(r"(\d+) contribution", tips.get(cid, ""))
        days.append((date, int(m.group(1)) if m else 0, int(lvl)))
    days.sort()
    total = re.search(r"([\d,]+)\s+contributions?\s+in the last year", html)
    return days, int(total.group(1).replace(",", "")) if total else sum(c for _, c, _ in days)


def render(t, days, total):
    H = 236
    a = t["accent"]
    pitch, cell = 14, 11
    first = dt.date.fromisoformat(days[0][0])
    start = first - dt.timedelta(days=(first.weekday() + 1) % 7)  # Sunday-aligned like GitHub
    x0, y0 = 84, 72
    pos = {}
    for date, count, lvl in days:
        d = dt.date.fromisoformat(date)
        off = (d - start).days
        pos[date] = (x0 + (off // 7) * pitch, y0 + (off % 7) * pitch, lvl, count)
    b = [panel(t, W, H),
         f'<g class="dsk">{text(32, 40, "CONTRIBUTIONS · LAST 12 MONTHS", 11.5, t["text3"], "m", ls=2.2)}'
         f'{text(848, 40, f"{total:,} contributions", 14, t["text"], anchor="end", weight=600)}</g>',
         f'<g class="mob">{text(32, 48, f"{total:,} contributions · 12 months", 24, t["text"], weight=600)}</g>']
    seen = set()
    for date, (x, y, lvl, _) in pos.items():
        d = dt.date.fromisoformat(date)
        if d.day <= 7 and d.weekday() == 6 and d.month not in seen and x < 820:
            seen.add(d.month)
            b.append(f'<g class="dsk">{text(x, y0 - 8, d.strftime("%b"), 10, t["text3"], "m")}</g>')
    for i, lab in ((1, "Mon"), (3, "Wed"), (5, "Fri")):
        b.append(f'<g class="dsk">{text(x0 - 34, y0 + i * pitch + 9, lab, 10, t["text3"], "m")}</g>')
    css = "@keyframes lit{from{fill:%s}}" % t["levels"][0]
    for date, (x, y, lvl, _) in pos.items():
        if lvl:
            col = (x - x0) // pitch
            b.append(f'<rect x="{x}" y="{y}" width="{cell}" height="{cell}" rx="2.5" fill="{t["levels"][lvl]}" '
                     f'style="animation:lit .5s ease-out {0.4 + col * 0.045:.2f}s both"/>')
        else:
            b.append(f'<rect x="{x}" y="{y}" width="{cell}" height="{cell}" rx="2.5" fill="{t["levels"][0]}"/>')
    # link each active day to the next active day within 7 days
    active = [d for d in sorted(pos) if pos[d][2]]
    chains, cur = [], []
    for i, d in enumerate(active):
        if cur and (dt.date.fromisoformat(d) - dt.date.fromisoformat(cur[-1])).days > 7:
            chains.append(cur)
            cur = []
        cur.append(d)
    if cur:
        chains.append(cur)
    c = cell / 2
    for ch in chains:
        if len(ch) < 2:
            continue
        pts = " ".join(f"{pos[d][0] + c} {pos[d][1] + c}" for d in ch)
        col = (pos[ch[0]][0] - x0) // pitch
        b.append(f'<path d="M{pts}" class="draw" pathLength="100" stroke="{a}" stroke-opacity=".55" '
                 f'stroke-width="1.1" fill="none" stroke-linejoin="round"{delay(2.8 + col * 0.03)}/>')
    longest = max(chains, key=len) if chains else []
    if len(longest) > 2:
        pts = [(pos[d][0] + c, pos[d][1] + c) for d in longest]
        route = pts + pts[-2::-1]
        n = len(route) - 1
        dur = max(10, min(30, n * 0.5))
        b.append(motion(route, [dur * i / n for i in range(n + 1)], dur, t["amber"], r=2.4, begin=6))
    if active:
        x, y, *_ = pos[active[-1]]
        b.append(f'<circle cx="{x + c}" cy="{y + c}" r="6" fill="none" stroke="{t["amber"]}">'
                 f'<animate attributeName="r" values="5;11" dur="2.6s" repeatCount="indefinite"/>'
                 f'<animate attributeName="opacity" values=".8;0" dur="2.6s" repeatCount="indefinite"/></circle>')
    lx = 848 - 5 * pitch
    b.append(f'<g class="dsk">{text(32, 208, f"Updated {dt.date.today():%d %b %Y} · links join active days less than a week apart", 10.5, t["text3"], "m")}'
             f'{text(lx - 10, 208, "less", 10.5, t["text3"], "m", "end")}'
             + "".join(f'<rect x="{lx + i * pitch}" y="198" width="{cell}" height="{cell}" rx="2.5" fill="{t["levels"][i]}"/>' for i in range(5))
             + f'{text(lx + 5 * pitch + 4, 208, "more", 10.5, t["text3"], "m")}</g>')
    return doc(W, H, f"{total:,} contributions in the last year",
               f"Contribution calendar for {LOGIN}: {total:,} contributions over the last 12 months, {len(active)} active days.",
               "".join(b), css)


def main():
    days, total = fetch_graphql() if TOKEN else fetch_public()
    if len(days) < 300:
        sys.exit(f"expected a year of calendar data, got {len(days)} days; not writing")
    OUT.mkdir(parents=True, exist_ok=True)
    for theme, t in THEMES.items():
        (OUT / f"activity-{theme}.svg").write_text(render(t, days, total), encoding="utf-8")
    print(f"{total} contributions, {sum(1 for d in days if d[2])} active days -> {OUT}")


if __name__ == "__main__":
    main()
