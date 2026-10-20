#!/usr/bin/env python3
"""Flag sentences that may read like LLM output, for the human-prose pass.

    python3 prose_check.py draft.md              # a Markdown or text file
    python3 prose_check.py deep-dives/ad-breaks.json   # every piece in a topic's pack

It prints hints, not verdicts: a flagged line can be fine. The rules are in
.claude/skills/human-prose/SKILL.md.
"""
import json
import re
import sys
from pathlib import Path

CHECKS = [
    ("em-dash", re.compile(r"—|\s–\s")),
    ("negative parallelism", re.compile(
        r"\b(it|this|that)(’s|'s| is) not\b[^.?!]*[,;]\s*(it|this|that)(’s|'s| is)\b"
        r"|\bnot (only|just) [^.?!]*\bbut\b"
        r"|\bno \w+, no \w+"
        r"|\b(isn’t|isn't|aren’t|aren't|wasn’t|wasn't)\b[^.?!]{0,80}[.;]\s*(it|this|that|they)(’s|'s| is| are)\b"
        r"|,\s+not\s+[\w\s'’-]{1,40}[.,]"
        r"|\bnot [\w'’-]+, but\b", re.I)),
    ("easy/hard foil", re.compile(r"\b(anyone|everyone|any \w+) can\b|\bthe hard part\b|\bthe easy part\b", re.I)),
]
KICKER_MAX_WORDS = 7


def sentences(par):
    return [s for s in re.split(r"(?<=[.?!])\s+", par.strip()) if s]


def check_text(text, label=""):
    hits = []
    pars = [p for p in re.split(r"\n\s*\n", text) if p.strip()]
    for n, par in enumerate(pars, 1):
        if re.match(r"^\s*(#|[-*] |\d+[.)] |\*\*)", par):
            continue  # headings, lists and labelled lines: only the pattern checks below matter
        for name, rx in CHECKS:
            for m in rx.finditer(par):
                hits.append((n, name, par[max(0, m.start() - 40): m.end() + 40].replace("\n", " ")))
        ss = sentences(par)
        if len(ss) > 1 and len(ss[-1].split()) <= KICKER_MAX_WORDS and not ss[-1].endswith("?"):
            hits.append((n, "possible kicker", ss[-1]))
    for n, name, snip in hits:
        print(f"{label}¶{n:<3} {name:<22} …{snip.strip()}…")
    return len(hits)


def main(path):
    p = Path(path)
    total = 0
    if p.suffix == ".json":
        t = json.loads(p.read_text())
        for piece in (t.get("pack") or {}).get("pieces", []):
            total += check_text(piece["body"], f"{piece.get('id', '?')} ")
    else:
        total = check_text(p.read_text())
    print(f"{total} hint(s). Each is a place to look, not a rule broken.")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    main(sys.argv[1])
