#!/usr/bin/env python3
"""Turn one pack piece into HTML for a Google Doc.

    python3 gdoc.py ad-breaks-01 > piece.html             # review copy for the team
    python3 gdoc.py ad-breaks-01 --approval > piece.html  # clean copy for Arash to approve

Upload the output with the Google Drive connector's create_file (contentMimeType "text/html"),
which converts it to a Google Doc: headings, links, lists, images and the LinkedIn table come
through as native formatting. Then save the Doc's link on the piece ("googleDoc", or
"approvalDoc" for the copy Arash approves) and rebuild, so the Deep Dives page links to it.
Images load from GitHub, so push them before uploading.

The approval copy has no review notes and refuses to build while the text still has [check],
[Arash: …] or [Team: …] markers: Arash gets a draft he can approve as it stands.
"""
import html
import json
import re
import sys
from pathlib import Path

TOPICS = Path(__file__).resolve().parent.parent / "deep-dives"
RAW = "https://raw.githubusercontent.com/marcussvenssonexternal-cell/marcus/{branch}/content-engine/deep-dives/{image}"
P = '<p style="margin-top:0pt;margin-bottom:12pt;line-height:1.5">'
H = 'style="margin-top:20pt;margin-bottom:8pt;page-break-after:avoid"'
CHK = '<span style="background-color:#fff2cc">[check]</span>'
OPEN = re.compile(r"\[check\]|\[(?:Arash|Team):[^\]]*\]")


def inline(s):
    s = html.escape(s, quote=False)
    s = re.sub(r"\[([^\]]+)\]\((https?://[^\s)]+)\)", lambda m: f'<a href="{m.group(2)}">{m.group(1)}</a>', s)
    s = re.sub(r"\*\*([^*]+)\*\*", r"<b>\1</b>", s)
    s = re.sub(r"(^|[\s(])\*([^*\s][^*]*)\*", r"\1<i>\2</i>", s)
    s = re.sub(r"\[((?:Arash|Team):[^\]]*)\]", r'<span style="background-color:#fce5cd">[\1]</span>', s)
    return s.replace("[check]", CHK)


def image(src, alt, branch):
    url = src if src.startswith("https://") else RAW.format(branch=branch, image=src)
    return f'{P}<img src="{html.escape(url)}" alt="{html.escape(alt)}" width="624" height="351"></p>'


def body(src, branch):
    out = []
    for b in [x.strip("\n") for x in src.split("\n\n") if x.strip()]:
        lines = b.split("\n")
        im = re.match(r"^!\[([^\]]*)\]\(([^)\s]+)\)$", b)
        m = re.match(r"^(#{1,4})\s+(.*)$", b)
        if im:
            out.append(image(im.group(2), im.group(1), branch))
        elif m and "\n" not in b:
            lv = min(4, len(m.group(1)))
            out.append(f"<h{lv} {H}>{inline(m.group(2))}</h{lv}>")
        elif all(re.match(r"^\s*[-*]\s+", l) for l in lines):
            out.append("<ul>" + "".join(f'<li style="margin-bottom:6pt;line-height:1.5">{inline(re.sub(r"^\s*[-*]\s+", "", l))}</li>' for l in lines) + "</ul>")
        elif all(re.match(r"^\s*\d+[.)]\s+", l) for l in lines):
            out.append("<ol>" + "".join(f"<li>{inline(re.sub(r'^\s*\d+[.)]\s+', '', l))}</li>" for l in lines) + "</ol>")
        else:
            out.append(P + "<br>".join(inline(l) for l in lines) + "</p>")
    return "\n".join(out)


def linkedin_fields(p, heading):
    li, cover = p.get("linkedin"), p.get("cover") or {}
    if not li:
        return []
    rows = [("Headline", li.get("headline")), ("SEO title", li.get("seoTitle")),
            ("SEO description", li.get("seoDescription")), ("Cover alt text", cover.get("alt"))]
    out = [f"{heading}<table border=\"1\" cellpadding=\"6\" style=\"border-collapse:collapse\">"
           + "".join(f'<tr><td width="28%"><b>{k}</b></td><td>{html.escape(v)}</td></tr>' for k, v in rows if v) + "</table>"]
    if li.get("shareText"):
        out.append(f"{P}<b>Post text when the article is published:</b></p>"
                   + "".join(f"{P}{inline(x)}</p>" for x in li["shareText"].split("\n\n")))
    return out


def piece_html(piece_id, approval=False, branch="claude/practical-fermi-gatt4t"):
    for path in TOPICS.glob("*.json"):
        t = json.loads(path.read_text())
        for p in (t.get("pack") or {}).get("pieces", []):
            if p.get("id") != piece_id:
                continue
            kind = {"article": "LinkedIn article", "post": "LinkedIn post", "carousel": "Carousel brief"}[p["kind"]]
            words = len(re.sub(r"^!\[[^\]]*\]\([^)]*\)$", "", p["body"], flags=re.M).split())
            cover = p.get("cover") or {}
            h = [f"<h1>{html.escape(p['title'])}</h1>"]
            if approval:
                left = sorted(set(OPEN.findall(p["body"])))
                if left:
                    sys.exit(f"{piece_id} still has open markers, so it isn't ready for Arash: {', '.join(left)}")
                h.append(f"{P}<i>Draft for approval. {kind} by Arash Pendari, about {max(1, round(words / 230))} minutes to read.</i></p>")
            else:
                h.append(f"{P}<i>Draft for review. {kind} by Arash Pendari, part of the series “{html.escape(t['title'])}”"
                         + (f", scheduled for {html.escape(p['slot'])}" if p.get("slot") else "")
                         + f". {words:,} words. Notes for review are at the end.</i></p>")
            if cover.get("image"):
                h.append(image(cover["image"], cover.get("alt", ""), branch))
            h.append(body(p["body"], branch))
            if approval:
                h += linkedin_fields(p, f'<hr><h2 {H}>Ready to publish</h2>')
            else:
                checks = p.get("checks") or []  # what is still open in this piece, one line each
                h.append(f"<hr><h2 {H}>Notes for review</h2>")
                if "[check]" in p["body"]:
                    h.append(f"{P}<b>Before posting:</b> facts marked {CHK} still need a look at their source."
                             + ("" if checks else " The fact-check list is on the Deep Dives page.") + "</p>")
                    if checks:
                        h.append("<ol>" + "".join(f'<li style="margin-bottom:6pt">{inline(c)}</li>' for c in checks) + "</ol>")
                h += linkedin_fields(p, '<h3 style="margin-top:16pt;margin-bottom:6pt;page-break-after:avoid">Publishing on LinkedIn</h3>')
            return '<html><head><meta charset="utf-8"></head><body>\n' + "\n".join(h) + "\n</body></html>"
    sys.exit(f"No piece with id {piece_id}")


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    if len(args) != 1:
        sys.exit(__doc__)
    print(piece_html(args[0], approval="--approval" in sys.argv))
