#!/usr/bin/env python3
"""Build the Content Radar page from the weekly JSON reports.

    python3 build.py                     # reports/*.json -> radar/index.html + reports/*.md
    python3 build.py --recover PAGE.html # copy weeks found in a published page into reports/

Each week is one file, reports/<ISO week>.json (e.g. 2026-W43.json). The page holds every
week, newest first, so the published artifact doubles as the archive: --recover pulls past
weeks back out of it when a fresh session doesn't have them on disk.
"""
import argparse
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPORTS = HERE.parent / "reports"
TEMPLATE = HERE / "template.html"
OUT = HERE / "index.html"
PLACEHOLDER = "/*RADAR_DATA*/"

REQUIRED = ["week", "generated", "headline", "summary", "ideas", "gaps", "themes", "events",
            "mentions", "stats", "competitors", "coverage"]
WEEK_RE = re.compile(r"^\d{4}-W\d{2}$")
PILLARS = ["Product & AI Insight", "Industry Trend Commentary", "Founder POV / Build Lessons",
           "Behind the Scenes", "Opinion / Contrarian Take"]
STATUSES = {"going", "tbd", "not-going", "recent"}


def check(week, name):
    """Return a list of problems with one week's report."""
    problems = [f"{name}: missing '{k}'" for k in REQUIRED if k not in week]
    if problems:
        return problems
    if not WEEK_RE.match(week["week"]):
        problems.append(f"{name}: week '{week['week']}' is not like 2026-W43")
    for i, idea in enumerate(week["ideas"]):
        for k in ("hook", "pillar"):
            if not idea.get(k):
                problems.append(f"{name}: ideas[{i}] missing '{k}'")
        if idea.get("pillar") and idea["pillar"] not in PILLARS:
            problems.append(f"{name}: ideas[{i}] pillar '{idea['pillar']}' is not one of {PILLARS}")
    for i, ev in enumerate(week["events"]):
        if ev.get("status") not in STATUSES:
            problems.append(f"{name}: events[{i}] status '{ev.get('status')}' is not one of {sorted(STATUSES)}")
    return problems


def load_weeks():
    weeks, problems = [], []
    for path in sorted(REPORTS.glob("*.json")):
        week = json.loads(path.read_text())
        problems += check(week, path.name)
        if path.stem != week.get("week"):
            problems.append(f"{path.name}: file name doesn't match week '{week.get('week')}'")
        weeks.append(week)
    return sorted(weeks, key=lambda w: w["week"], reverse=True), problems


def src(items):
    return "; ".join(f"[{s.get('label') or s.get('title')}]({s['url']})" + (f" ({s['date']})" if s.get("date") else "")
                     for s in items or [])


def markdown(w):
    """The same week as a readable brief, for people who'd rather not open the page."""
    out = [f"# Content Radar {w['week']}", "", f"_Generated {w['generated']} · window {w.get('window', '')}_", "",
           f"**{w['headline']}**", ""] + [f"- {s}" for s in w["summary"]] + ["", "## Content ideas", ""]
    for i in w["ideas"]:
        meta = " · ".join(x for x in (i["pillar"], i.get("format"), i.get("timing"), i.get("event")) if x)
        out += [f"### {i['hook']}", "", f"_{meta}_", ""]
        out += [i[k] + "\n" for k in ("angle",) if i.get(k)]
        out += [f"**Bring:** {i['proof']}\n"] if i.get("proof") else []
        out += [f"**Reacts to:** {src(i.get('reactsTo'))}", ""]
    out += ["## Gaps nobody is covering", ""]
    for g in w["gaps"]:
        out += [f"- **{g['title']}.** {g['detail']} {src(g.get('evidence'))}"]
    out += ["", "## What competitors are saying", ""]
    for t in w["themes"]:
        out += [f"- **{t['title']}** ({', '.join(t.get('who', []))}). {t['detail']} {src(t.get('sources'))}"]
    out += ["", "## Events", ""]
    for e in sorted(w["events"], key=lambda e: e.get("start", "")):
        dates = e.get("start", "") + (f" to {e['end']}" if e.get("end") and e["end"] != e.get("start") else "")
        out += [f"### {e['name']} ({dates}, {e.get('city', '')}) [{e['status']}]", ""]
        out += [x + "\n" for x in (e.get("role"), e.get("agenda")) if x]
        out += [f"- {h}" for h in e.get("hooks", [])] + [""]
    out += ["## Mentions", "", "| Date | Who / where | What | Do |", "| --- | --- | --- | --- |"]
    out += [f"| {m['date']} | [{m['who']}]({m['url']}) ({m['where']}) | {m['summary']} | {m.get('action', '')} |" for m in w["mentions"]]
    out += ["", "## Stats bank", "", "| Number | What | Source |", "| --- | --- | --- |"]
    out += [f"| {s['value']} | {s['what']} | [{s['source']}]({s['url']}) {s.get('date', '')} |" for s in w["stats"]]
    out += ["", "## How this was made", ""] + [f"- {c}" for c in w["coverage"]]
    return "\n".join(out) + "\n"


def build():
    weeks, problems = load_weeks()
    if problems:
        sys.exit("Fix these before publishing:\n  " + "\n  ".join(problems))
    if not weeks:
        sys.exit(f"No reports found in {REPORTS}")
    for w in weeks:
        (REPORTS / f"{w['week']}.md").write_text(markdown(w))
    # "</" would end the <script> block early; "<\/" is the same string in JSON.
    payload = json.dumps({"weeks": weeks}, ensure_ascii=False, indent=1).replace("</", "<\\/")
    template = TEMPLATE.read_text()
    if template.count(PLACEHOLDER) != 1:
        sys.exit(f"{TEMPLATE.name} must contain {PLACEHOLDER} exactly once")
    OUT.write_text(template.replace(PLACEHOLDER, payload))
    print(f"Wrote {OUT} with {len(weeks)} week(s): {', '.join(w['week'] for w in weeks)}")


def recover(page):
    html = Path(page).read_text()
    m = re.search(r'<script type="application/json" id="radar-data">(.*?)</script>', html, re.S)
    if not m:
        sys.exit(f"No radar data block found in {page}")
    REPORTS.mkdir(exist_ok=True)
    added = []
    for week in json.loads(m.group(1)).get("weeks", []):
        path = REPORTS / f"{week['week']}.json"
        if not path.exists():
            path.write_text(json.dumps(week, ensure_ascii=False, indent=2) + "\n")
            added.append(week["week"])
    print("Recovered: " + (", ".join(added) if added else "nothing new (all weeks already on disk)"))


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--recover", metavar="PAGE", help="published page to pull past weeks from")
    args = ap.parse_args()
    recover(args.recover) if args.recover else build()
