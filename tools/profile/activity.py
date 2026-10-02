#!/usr/bin/env python3
"""Render the rolling year of real GitHub contributions as a weekly-volume panel. Never synthetic."""
import datetime as dt
import json
import math
import os
from pathlib import Path
import re
import urllib.request
from theme import PUBLISHED, THEMES, W, MW, P, MP, doc, glass_card, text

LOGIN = os.environ.get("GH_LOGIN", "vinayak533")
OUT = Path(__file__).resolve().parents[2] / "assets/svg"
LEVEL = {"NONE": 0, "FIRST_QUARTILE": 1, "SECOND_QUARTILE": 2, "THIRD_QUARTILE": 3, "FOURTH_QUARTILE": 4}

def fetch():
    token = os.environ.get("GITHUB_TOKEN")
    if token:
        query = 'query($l:String!){user(login:$l){contributionsCollection{contributionCalendar{totalContributions weeks{contributionDays{date contributionCount contributionLevel}}}}}}'
        req = urllib.request.Request("https://api.github.com/graphql", data=json.dumps({"query":query,"variables":{"l":LOGIN}}).encode(), headers={"Authorization":f"bearer {token}","Content-Type":"application/json"})
        with urllib.request.urlopen(req, timeout=30) as response:
            data = json.load(response)
        if data.get("errors"): raise ValueError("GitHub GraphQL returned errors; preserving existing assets")
        cal = data["data"]["user"]["contributionsCollection"]["contributionCalendar"]
        days = [(d["date"],d["contributionCount"],LEVEL[d["contributionLevel"]]) for w in cal["weeks"] for d in w["contributionDays"]]
        return sorted(days), cal["totalContributions"]
    with urllib.request.urlopen(f"https://github.com/users/{LOGIN}/contributions", timeout=30) as response:
        html = response.read().decode()
    cells = re.findall(r'data-date="(\d{4}-\d{2}-\d{2})"[^>]*?id="([^"]+)"[^>]*?data-level="(\d)"',html)
    tips = dict(re.findall(r'<tool-tip[^>]*for="([^"]+)"[^>]*>([^<]*)</tool-tip>',html))
    days = []
    for date,cid,lvl in cells:
        match = re.match(r"([\d,]+) contributions?",tips.get(cid,""))
        zero = tips.get(cid,"").startswith("No contributions")
        if not match and not zero: raise ValueError(f"Unrecognized contribution count for {date}; preserving assets")
        days.append((date,int(match.group(1).replace(",","")) if match else 0,int(lvl)))
    total = re.search(r"([\d,]+)\s+contributions?\s+in the last year",html)
    if not total: raise ValueError("Missing calendar total; preserving assets")
    return sorted(days),int(total.group(1).replace(",",""))

def validate(days,total):
    # The public calendar includes the full first boundary week.
    if not 365 <= len(days) <= 371: raise ValueError(f"Expected a rolling year, got {len(days)} days")
    dates=[dt.date.fromisoformat(d) for d,_,_ in days]
    if any(b-a != dt.timedelta(days=1) for a,b in zip(dates,dates[1:])): raise ValueError("Calendar is not contiguous")
    if any(c < 0 or not 0 <= level <= 4 or (c == 0) != (level == 0) for _,c,level in days): raise ValueError("Invalid contribution data")
    if sum(c for _,c,_ in days) != total: raise ValueError("Calendar counts do not match total")

def render(t,days,total,m=False):
    """Dot-matrix weekly columns: lit cells are proportional to each week's real total."""
    first,last=(dt.date.fromisoformat(days[i][0]) for i in (0,-1))
    start=first-dt.timedelta(days=(first.weekday()+1)%7)  # Sunday-aligned weeks, as on GitHub
    weeks={}
    for date,count,_ in days:
        i=(dt.date.fromisoformat(date)-start).days//7
        weeks[i]=weeks.get(i,0)+count
    vals=[weeks.get(i,0) for i in range(max(weeks)+1)]
    peak=max(vals) or 1
    active=sum(c>0 for _,c,_ in days)
    recent=sum(c for _,c,_ in days[-90:])
    cut=((last-dt.timedelta(days=89))-start).days//7
    if m:
        w,p,rows,yb,big,lab=MW,MP,14,226,30,14.5
    else:
        w,p,rows,yb,big,lab=W,P,9,232,34,15
    pitch=(w-2*p)/len(vals)
    top=yb-(rows-1)*pitch
    h=yb+(44 if m else 46)
    span=(f"{first:%b %Y} – {last:%b %Y}" if m else f"{first:%d %b %Y} – {last:%d %b %Y}").upper()
    b=[glass_card(t,w,h,"a",bloom="violet",bloom_at=(w-p-60,yb,260 if not m else 180)),
       f'<text x="{p}" y="{46 if m else 50}" class="s"><tspan font-size="{big}" font-weight="600" fill="{t["text"]}">{total:,}</tspan>'
       f'<tspan dx="10" font-size="{lab}" fill="{t["text2"]}">contributions{"" if m else " in the last year"}</tspan></text>',
       text(p,70 if m else 76,span,10.5 if m else 11,t["text3"],True,ls=1),
       text(w-p,44 if m else 48,f"{active}",20 if m else 22,t["text"],weight=600,anchor="end"),
       text(w-p,64 if m else 70,"ACTIVE DAYS",10.5,t["text3"],True,anchor="end",ls=1)]
    bx=p+cut*pitch
    violet=t["hues"]["violet"]["base"]
    b.append(f'<rect x="{bx:.1f}" y="{top-pitch/2-(10 if m else 20):.1f}" width="{w-p-bx:.1f}" height="{yb-top+pitch+(10 if m else 20):.1f}" '
             f'rx="10" fill="{violet}" fill-opacity="{.07 if t["dark"] else .05}" stroke="{t["hues"]["violet"]["rim"]}" stroke-opacity=".25"/>')
    label=f"LAST 90 DAYS · {recent}"
    ink=t["hues"]["violet"]["ink"]
    b.append(text(w-p,top-pitch/2-18,label,10.5,ink,True,anchor="end",ls=.8) if m
             else text(bx+10,top-pitch/2-6,label,10.5,ink,True,ls=.8))
    arm,bar=pitch*.27,pitch*.12
    plus=(f'<path id="px" d="M{-bar:.2f} {-arm:.2f}h{2*bar:.2f}v{arm-bar:.2f}h{arm-bar:.2f}v{2*bar:.2f}h{bar-arm:.2f}'
          f'v{arm-bar:.2f}h{-2*bar:.2f}v{bar-arm:.2f}h{bar-arm:.2f}v{-2*bar:.2f}h{arm-bar:.2f}z"/>')
    b.append(f"<defs>{plus}</defs>")
    tones={"lo":[],"mid":[],"hi":[]}
    off=[]
    for i,v in enumerate(vals):
        lit=math.ceil(rows*v/peak) if v else 0
        x=p+i*pitch+pitch/2
        for r in range(rows):
            y=yb-r*pitch
            if r<lit:
                f=r/(rows-1)
                tone="mid" if f<.34 else "lo" if f<.67 else "hi"
                tones[tone].append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{pitch*.3:.2f}"/>' if m
                                   else f'<use href="#px" x="{x:.1f}" y="{y:.1f}"/>')
            else:
                off.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{pitch*(.13 if m else .08):.2f}"/>')
    b.append(f'<g fill="{t["dot_off"]}" fill-opacity="{t["dot_off_op"]*2:.2f}">{"".join(off)}</g>')
    b+= [f'<g fill="{t[{"lo":"dot_lo","mid":"dot_mid","hi":"dot_hi"}[k]]}">{"".join(v)}</g>' for k,v in tones.items() if v]
    n=math.ceil(rows*vals[-1]/peak) if vals[-1] else 1
    lx,ly=p+(len(vals)-1)*pitch+pitch/2,yb-n*pitch
    b.append(f'<circle cx="{lx:.1f}" cy="{ly:.1f}" r="2.4" fill="{t["hues"]["violet"]["rim"]}"/>'
             f'<circle class="ping motion" cx="{lx:.1f}" cy="{ly:.1f}" r="2.4" fill="none" stroke="{t["hues"]["violet"]["rim"]}"/>')
    for i in range(len(vals)):
        d=start+dt.timedelta(weeks=i)
        if d.day<=7 and i and (not m or d.month in (1,4,7,10)):
            b.append(text(p+i*pitch+pitch/2,yb+26 if not m else yb+24,d.strftime("%b"),10.5,t["text3"],True,anchor="middle"))
    css=("@keyframes ping{0%{transform:scale(1);opacity:.9}70%,100%{transform:scale(2.8);opacity:0}}"
         ".ping{transform-box:fill-box;transform-origin:center;animation:ping 2.8s ease-out infinite}")
    return doc(w,h,f"{LOGIN}: {total:,} contributions in the last year",
               f"Weekly contributions from {first} through {last}: {total} in total across {active} active days, "
               f"{recent} of them in the last 90 days. Each column is one week; lit cells are proportional to that week's total "
               f"(busiest week: {peak}).","".join(b),css)


def main():
    days,total=fetch()
    validate(days,total)
    rendered={f'activity-{theme}{"-compact" if m else ""}.svg':render(t,days,total,m) for theme,t in ((k,THEMES[k]) for k in PUBLISHED) for m in (False,True)}
    OUT.mkdir(parents=True,exist_ok=True)
    for name,svg in rendered.items(): (OUT/name).write_text(svg,encoding="utf-8")
    print(f"Rendered {total} contributions across {len(days)} days in {len(rendered)} variants.")
if __name__=="__main__": main()
