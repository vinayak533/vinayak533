#!/usr/bin/env python3
"""Render the rolling year of real GitHub contributions as a weekly-volume panel. Never synthetic."""
import datetime as dt
import json
import math
import os
from pathlib import Path
import re
import urllib.request
from theme import V, W, MW, P, MP, doc, surface, text

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

def render(days,total,m=False):
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
        w,p,rows,yb,big=MW,MP,16,226,28
    else:
        w,p,rows,yb,big=W,P,10,258,30
    pitch=(w-2*p)/len(vals)
    top=yb-(rows-1)*pitch
    h=yb+(52 if m else 54)
    b=[surface(w,h)]
    stats=[(f"{total:,}","last 12 months"),(f"{recent:,}","last 90 days"),(f"{active}","active days")]
    cw=(w-2*p)/3
    for i,(v,label) in enumerate(stats):
        x=p+i*(cw if m else 190)
        b+=[text(x,56,v,big,V["text"],weight=600,ls=-.5),text(x,80,label,14 if m else 14.5,V["text2"])]
    if not m:
        b.append(text(w-p,80,f"{first.day} {first:%b %Y} to {last.day} {last:%b %Y}",14.5,V["text3"],anchor="end"))
    groups={"dot":{},"violetlo":{},"violet":{}}
    for i,v in enumerate(vals):
        lit=math.ceil(rows*v/peak) if v else 0
        x=p+i*pitch+pitch/2
        for r in range(rows):
            on=r<lit
            key=("violet" if i>=cut else "violetlo") if on else "dot"
            groups[key].setdefault(i if on else 0,[]).append(f'<circle cx="{x:.1f}" cy="{yb-r*pitch:.1f}" r="{pitch*(.36 if on else .14 if not m else .18):.2f}"/>')
    # Lit columns ripple left to right, one week at a time; every dot is fully lit on the first frame.
    b+=[f'<g fill="{V[k]}">'+"".join(f'<g class="wv" style="animation-delay:{i*.06:.2f}s">{"".join(v)}</g>' if k!="dot" else "".join(v) for i,v in sorted(c.items()))+"</g>" for k,c in groups.items() if c]
    n=math.ceil(rows*vals[-1]/peak) if vals[-1] else 1
    lx,ly=p+(len(vals)-1)*pitch+pitch/2,yb-(n-1)*pitch
    b.append(f'<circle class="ping motion" cx="{lx:.1f}" cy="{ly:.1f}" r="{pitch*.36:.2f}" fill="none" stroke="{V["violet"]}"/>')
    for i in range(len(vals)):
        d=start+dt.timedelta(weeks=i)
        if d.day<=7 and i and (not m or d.month in (1,4,7,10)):
            b.append(text(p+i*pitch+pitch/2,yb+29,d.strftime("%b"),13,V["text3"],anchor="middle"))
    css=("@keyframes wv{0%,16%,100%{opacity:1;transform:none}7%{opacity:.45;transform:translateY(-5px)}}.wv{animation:wv 6s ease-in-out infinite}"
         "@keyframes ping{0%{transform:scale(1);opacity:.9}70%,100%{transform:scale(2.8);opacity:0}}"
         ".ping{transform-box:fill-box;transform-origin:center;animation:ping 2.8s ease-out infinite}")
    return doc(w,h,f"{LOGIN}: {total:,} contributions in the last year",
               f"Weekly contributions from {first} through {last}: {total} in total across {active} active days, "
               f"{recent} of them in the last 90 days (brighter columns). Each column is one week; lit dots are proportional to that week's total "
               f"(busiest week: {peak}).","".join(b),css)


def main():
    days,total=fetch()
    validate(days,total)
    rendered={f'activity{"-compact" if m else ""}.svg':render(days,total,m) for m in (False,True)}
    OUT.mkdir(parents=True,exist_ok=True)
    for name,svg in rendered.items(): (OUT/name).write_text(svg,encoding="utf-8")
    print(f"Rendered {total} contributions across {len(days)} days in {len(rendered)} variants.")
if __name__=="__main__": main()
