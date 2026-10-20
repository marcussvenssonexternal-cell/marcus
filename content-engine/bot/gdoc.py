#!/usr/bin/env python3
"""Turn one pack piece into HTML for a Google Doc.

    python3 gdoc.py ad-breaks-01 > piece.html

Upload the output with the Google Drive connector's create_file (contentMimeType "text/html"),
which converts it to a Google Doc: headings, links, lists and the LinkedIn table come through as
native formatting. Then save the Doc's link on the piece as "googleDoc" and rebuild, so the Deep
Dives page links to it. The cover image is referenced from GitHub, so push it before uploading.
"""
import html
import json
import re
import sys
from pathlib import Path

TOPICS = Path(__file__).resolve().parent.parent / "deep-dives"
RAW = "https://raw.githubusercontent.com/marcussvenssonexternal-cell/marcus/{branch}/content-engine/deep-dives/{image}"
P = '<p style="margin-top:0pt;margin-bottom:8pt">'
CHK = '<span style="background-color:#fff2cc">[check]</span>'


def inline(s):
    s = html.escape(s, quote=False)
    s = re.sub(r"\[([^\]]+)\]\((https?://[^\s)]+)\)", lambda m: f'<a href="{m.group(2)}">{m.group(1)}</a>', s)
    s = re.sub(r"\*\*([^*]+)\*\*", r"<b>\1</b>", s)
    s = re.sub(r"(^|[\s(])\*([^*\s][^*]*)\*", r"\1<i>\2</i>", s)
    s = re.sub(r"\[((?:Arash|Team):[^\]]*)\]", r'<span style="background-color:#fce5cd">[\1]</span>', s)
    return s.replace("[check]", CHK)


def body(src):
    out = []
    for b in [x.strip("\n") for x in src.split("\n\n") if x.strip()]:
        lines = b.split("\n")
        m = re.match(r"^(#{1,4})\s+(.*)$", b)
        if m and "\n" not in b:
            lv = min(4, len(m.group(1)))
            out.append(f'<h{lv} style="page-break-after:avoid">{inline(m.group(2))}</h{lv}>')
        elif all(re.match(r"^\s*[-*]\s+", l) for l in lines):
            out.append("<ul>" + "".join(f"<li>{inline(re.sub(r'^\s*[-*]\s+', '', l))}</li>" for l in lines) + "</ul>")
        elif all(re.match(r"^\s*\d+[.)]\s+", l) for l in lines):
            out.append("<ol>" + "".join(f"<li>{inline(re.sub(r'^\s*\d+[.)]\s+', '', l))}</li>" for l in lines) + "</ol>")
        else:
            out.append(P + "<br>".join(inline(l) for l in lines) + "</p>")
    return "\n".join(out)


def piece_html(piece_id, branch="claude/practical-fermi-gatt4t"):
    for path in TOPICS.glob("*.json"):
        t = json.loads(path.read_text())
        for p in (t.get("pack") or {}).get("pieces", []):
            if p.get("id") != piece_id:
                continue
            kind = {"article": "LinkedIn article", "post": "LinkedIn post", "carousel": "Carousel brief"}[p["kind"]]
            checks = p.get("checks") or []  # what is still open in this piece, one line each
            h = [f"<h1>{html.escape(p['title'])}</h1>",
                 f"{P}<i>Draft for review. {kind} by Arash Pendari, part of the series “{html.escape(t['title'])}”"
                 + (f", scheduled for {html.escape(p['slot'])}" if p.get("slot") else "")
                 + f". {len(p['body'].split()):,} words.</i></p>"]
            if "[check]" in p["body"]:
                h.append(f"{P}<b>Before posting:</b> facts marked {CHK} still need a look at their source."
                         + ("" if checks else " The fact-check list is on the Deep Dives page.") + "</p>")
                if checks:
                    h.append("<ol>" + "".join(f"<li>{inline(c)}</li>" for c in checks) + "</ol>")
            cover = p.get("cover") or {}
            if cover.get("image"):
                h.append(f'{P}<img src="{RAW.format(branch=branch, image=cover["image"])}" alt="{html.escape(cover.get("alt", ""))}" width="624" height="351"></p>')
            h.append(body(p["body"]))
            li = p.get("linkedin")
            if li:
                rows = [("Headline", li.get("headline")), ("SEO title", li.get("seoTitle")),
                        ("SEO description", li.get("seoDescription")), ("Cover alt text", cover.get("alt"))]
                h.append('<hr><h2 style="page-break-after:avoid">Publishing on LinkedIn</h2><table border="1" cellpadding="6" style="border-collapse:collapse">'
                         + "".join(f'<tr><td width="28%"><b>{k}</b></td><td>{html.escape(v)}</td></tr>' for k, v in rows if v) + "</table>")
                if li.get("shareText"):
                    h.append(f"{P}<b>Post text when the article is published:</b></p>"
                             + "".join(f"{P}{inline(x)}</p>" for x in li["shareText"].split("\n\n")))
            return '<html><head><meta charset="utf-8"></head><body>\n' + "\n".join(h) + "\n</body></html>"
    sys.exit(f"No piece with id {piece_id}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    print(piece_html(sys.argv[1]))
