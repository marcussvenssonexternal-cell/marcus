#!/usr/bin/env python3
"""Build the Deep Dives page from the content bot's topic files.

    python3 build.py                     # deep-dives/*.json -> bot/index.html + deep-dives/*.md
    python3 build.py --recover PAGE.html # copy topics and packs found in a published page into deep-dives/

Each topic is one file, deep-dives/<id>.json: the pitch (thesis, why now, series plan, evidence)
and, once the bot has written it, the pack (article, posts, carousel brief, fact-check). The
published page holds every topic and pack, so it doubles as the archive: --recover pulls packs
back out of it when a fresh session doesn't have them on disk.

Every piece of a pack gets a permanent id (<topic>-<nn>) the first time it is built. The page
keys the team's status, owner, notes and edits on that id, so never renumber or reorder the
pieces of a pack that has been published.
"""
import argparse
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
TOPICS = HERE.parent / "deep-dives"
BRAND = HERE.parent / "config" / "brand.md"
WATCHLIST = HERE.parent / "config" / "watchlist.yaml"
TEMPLATE = HERE / "template.html"
OUT = HERE / "index.html"
PLACEHOLDER = "/*BOT_DATA*/"

REQUIRED = ["id", "order", "title", "lens", "audience", "thesis", "whyNow", "questions", "bring",
            "needs", "evidence", "series"]
PACK_REQUIRED = ["generated", "summary", "pieces", "factcheck", "coverage"]
ID_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
PILLARS = ["Product & AI Insight", "Industry Trend Commentary", "Founder POV / Build Lessons",
           "Behind the Scenes", "Opinion / Contrarian Take"]
KINDS = {"article", "post", "carousel"}
CHECK = {"confirmed", "check", "unconfirmed"}


def check(t, name):
    """Return a list of problems with one topic file."""
    problems = [f"{name}: missing '{k}'" for k in REQUIRED if k not in t]
    if problems:
        return problems
    if not ID_RE.match(t["id"]):
        problems.append(f"{name}: id '{t['id']}' should be lowercase words joined by dashes")
    for i, s in enumerate(t["series"]):
        if s.get("kind") not in KINDS:
            problems.append(f"{name}: series[{i}] kind '{s.get('kind')}' is not one of {sorted(KINDS)}")
        if s.get("pillar") not in PILLARS:
            problems.append(f"{name}: series[{i}] pillar '{s.get('pillar')}' is not one of {PILLARS}")
    pack = t.get("pack")
    if pack:
        problems += [f"{name}: pack missing '{k}'" for k in PACK_REQUIRED if k not in pack]
        for i, p in enumerate(pack.get("pieces", [])):
            if p.get("kind") not in KINDS:
                problems.append(f"{name}: pieces[{i}] kind '{p.get('kind')}' is not one of {sorted(KINDS)}")
            if p.get("pillar") not in PILLARS:
                problems.append(f"{name}: pieces[{i}] pillar '{p.get('pillar')}' is not one of {PILLARS}")
            for k in ("title", "body"):
                if not p.get(k):
                    problems.append(f"{name}: pieces[{i}] missing '{k}'")
        for i, f in enumerate(pack.get("factcheck", [])):
            if f.get("status") not in CHECK:
                problems.append(f"{name}: factcheck[{i}] status '{f.get('status')}' is not one of {sorted(CHECK)}")
    return problems


def assign_ids(t, path):
    """Give new pack pieces their permanent id and save it back to the topic's file."""
    pieces = (t.get("pack") or {}).get("pieces", [])
    taken = {p["id"] for p in pieces if p.get("id")}
    n, changed = 0, False
    for p in pieces:
        if p.get("id"):
            continue
        n += 1
        while f"{t['id']}-{n:02d}" in taken:
            n += 1
        p["id"] = f"{t['id']}-{n:02d}"
        taken.add(p["id"])
        changed = True
    if changed:
        path.write_text(json.dumps(t, ensure_ascii=False, indent=2) + "\n")


def load_topics():
    topics, problems = [], []
    for path in sorted(TOPICS.glob("*.json")):
        t = json.loads(path.read_text())
        found = check(t, path.name)
        if path.stem != t.get("id"):
            found.append(f"{path.name}: file name doesn't match id '{t.get('id')}'")
        if not found:
            assign_ids(t, path)
        problems += found
        topics.append(t)
    ids = [p.get("id") for t in topics for p in (t.get("pack") or {}).get("pieces", [])]
    problems += [f"piece id '{x}' is used twice" for x in sorted({x for x in ids if ids.count(x) > 1})]
    return sorted(topics, key=lambda t: (t.get("order", 99), t.get("id", ""))), problems


def setting(key):
    m = re.search(rf"^{key}:\s*(\S+)", WATCHLIST.read_text(), re.M) if WATCHLIST.exists() else None
    return m.group(1) if m else ""


def src(items):
    return "; ".join(f"[{s.get('label')}]({s['url']})" + (f" ({s['date']})" if s.get("date") else "") for s in items or [])


def markdown(t):
    """The topic and its pack as a readable brief, for people who'd rather not open the page."""
    out = [f"# {t['title']}", "", f"_{t['lens']} · for {', '.join(t['audience'])}_", "", f"**{t['thesis']}**", "",
           "## Why now", "", t["whyNow"], "", "## Questions the series answers", ""]
    out += [f"- {q}" for q in t["questions"]]
    out += ["", "## What Vionlabs brings", "", t["bring"], "", "## Get before publishing", ""]
    out += [f"- {n}" for n in t["needs"]]
    if t.get("events"):
        out += ["", "## Events", ""] + [f"- {e}" for e in t["events"]]
    out += ["", "## Series plan", ""]
    out += [f"{i + 1}. **{s['working']}** ({s['format']}, {s['pillar']})" for i, s in enumerate(t["series"])]
    out += ["", "## Evidence", ""] + [f"- {src([e])}" for e in t["evidence"]]
    if t.get("radar"):
        out += ["", "## From the Content Radar", ""] + [f"- {r}" for r in t["radar"]]
    pack = t.get("pack")
    if pack:
        out += ["", "---", "", f"# The pack (written {pack['generated']})", "", pack["summary"], ""]
        for p in pack["pieces"]:
            meta = " · ".join(x for x in (p.get("slot"), p.get("format"), p["pillar"]) if x)
            out += [f"## {p['title']}", "", f"_{p['id']} · {meta}_", ""]
            if p.get("subtitle"):
                out += [f"*{p['subtitle']}*", ""]
            out += [p["body"].strip(), ""]
            if p.get("sources"):
                out += [f"**Sources:** {src(p['sources'])}", ""]
        if pack.get("voiceNote"):
            out += ["## Voice note prompts for Arash", ""] + [f"- {v}" for v in pack["voiceNote"]] + [""]
        out += ["## Fact-check before posting", "", "| Claim | Source | Status |", "| --- | --- | --- |"]
        out += [f"| {f['claim']} | [{f.get('source', 'source')}]({f.get('url', '')}) {f.get('date', '')} | {f['status']} |"
                for f in pack["factcheck"]]
        out += ["", "## How this was made", ""] + [f"- {c}" for c in pack["coverage"]]
    return "\n".join(out) + "\n"


def build():
    topics, problems = load_topics()
    if problems:
        sys.exit("Fix these before publishing:\n  " + "\n  ".join(problems))
    if not topics:
        sys.exit(f"No topics found in {TOPICS}")
    for t in topics:
        (TOPICS / f"{t['id']}.md").write_text(markdown(t))
    data = {"topics": topics, "url": setting("deepdives_url"), "radarUrl": setting("radar_url"),
            "brand": BRAND.read_text() if BRAND.exists() else ""}
    # "</" would end the <script> block early; "<\/" is the same string in JSON.
    payload = json.dumps(data, ensure_ascii=False, indent=1).replace("</", "<\\/")
    template = TEMPLATE.read_text()
    if template.count(PLACEHOLDER) != 1:
        sys.exit(f"{TEMPLATE.name} must contain {PLACEHOLDER} exactly once")
    OUT.write_text(template.replace(PLACEHOLDER, payload))
    packs = [t["id"] for t in topics if t.get("pack")]
    print(f"Wrote {OUT} with {len(topics)} topic(s); packs: {', '.join(packs) or 'none yet'}")
    covers = [p["cover"]["image"] for t in topics for p in (t.get("pack") or {}).get("pieces", []) if (p.get("cover") or {}).get("image")]
    for c in covers:
        if (TOPICS / c).exists():
            print(f"Cover to publish with the page: {c} <- {(TOPICS / c).relative_to(HERE.parent.parent)}")
        else:
            print(f"Warning: cover {c} is missing; run `node content-engine/bot/cover.js` (the page keeps any copy already published)")


def recover(page):
    html = Path(page).read_text()
    m = re.search(r'<script type="application/json" id="bot-data">(.*?)</script>', html, re.S)
    if not m:
        sys.exit(f"No bot data block found in {page}")
    TOPICS.mkdir(exist_ok=True)
    changed = []
    for t in json.loads(m.group(1)).get("topics", []):
        path = TOPICS / f"{t['id']}.json"
        disk = json.loads(path.read_text()) if path.exists() else None
        live = (t.get("pack") or {}).get("generated", "")
        have = ((disk or {}).get("pack") or {}).get("generated", "")
        # A pack only lives on the page until it's committed; take the page's copy when it's newer.
        if disk is None or live > have:
            path.write_text(json.dumps(t, ensure_ascii=False, indent=2) + "\n")
            changed.append(t["id"] + (" (pack)" if live else ""))
    print("Recovered: " + (", ".join(changed) if changed else "nothing new (disk is up to date)"))


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--recover", metavar="PAGE", help="published page to pull topics and packs from")
    args = ap.parse_args()
    recover(args.recover) if args.recover else build()
