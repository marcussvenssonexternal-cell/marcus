"""Builds the review page (gallery.html for the artifact, index.html standalone) and the copy decks
(brief/copy.md for the campaign, copy.md for the earlier drafts) from the two copy.json files.

    python3 build_gallery.py
"""

import json
import pathlib

HERE = pathlib.Path(__file__).parent
BRIEF = json.loads((HERE / "brief" / "copy.json").read_text())
ADS = json.loads((HERE / "copy.json").read_text())

STATUS = {"site": "On the website", "verify": "Check before launch", "illustrative": "Example values",
          "brief": "From the brief", "example": "Example values"}
SIGNOFF = "Vionlabs. AI built for entertainment."


def check_brief():
    # The brief's copy rules: 3 headlines of max 70 characters, 3 intro texts of max 600 that end on the sign-off.
    for ad in BRIEF:
        assert len(ad["headlines"]) == 3 and len(ad["intros"]) == 3, ad["id"]
        for h in ad["headlines"]:
            assert len(h) <= 70, (ad["id"], h)
        for i in ad["intros"]:
            assert len(i) <= 600 and i.endswith(SIGNOFF), (ad["id"], i[:40])


def quote(text):
    return [f"> {l}" if l else ">" for l in text.split("\n")]


def build_brief_markdown():
    lines = ["# AI built for entertainment: LinkedIn campaign copy", "",
             "From Viktor's ad brief. Images in `png/` (S = 1080×1080, L = 1200×627), videos in `video/`; "
             "sources in `../brief.html` and `../brief-anim.html`. CTA on every ad: **Book a demo**.", ""]
    for ad in BRIEF:
        lines += [f"## {ad['num']} · {ad['name']}", "", f"**Lab:** {ad['lab']}  ", f"**Audience:** {ad['audience']}  ",
                  f"**Targeting:** {ad['targeting']}", ""]
        if ad.get("note"):
            lines += [f"_{ad['note']}_", ""]
        lines += ["**Assets**", ""]
        for a in ad["assets"]:
            if "id" in a:
                lines.append(f"- {a['label']}: `png/{a['id']}.png`")
            elif "carousel" in a:
                lines.append(f"- {a['label']}: " + ", ".join(f"`png/{c}.png`" for c in a["carousel"]))
            else:
                lines.append(f"- {a['label']}: `video/{a['video']}.mp4`")
        lines += ["", "**Headlines**", ""] + [f"{n}. {h} ({len(h)})" for n, h in enumerate(ad["headlines"], 1)] + [""]
        for n, intro in enumerate(ad["intros"], 1):
            lines += [f"**Intro text {n}** ({len(intro)} characters)", "", *quote(intro), ""]
        lines += ["**Claims**", ""] + [f"- {c['text']}: {c['source']} ({STATUS[c['status']]})" for c in ad["claims"]] + [""]
    (HERE / "brief" / "copy.md").write_text("\n".join(lines))


def build_drafts_markdown():
    lines = ["# Vionlabs LinkedIn ad copy: earlier drafts", "",
             "Single-image ads, 1200×1200. Images in `png/`, sources in `ads.html`.", ""]
    for ad in ADS:
        lines += [f"## {ad['id']} · {ad['product']} · {ad['name']}", "",
                  f"![{ad['name']}](png/{ad['id']}.png)", "",
                  "**Intro text**", "", *quote(ad["intro"]), "",
                  f"**Headline:** {ad['headline']}  ",
                  f"**CTA button:** {ad['cta']}  ",
                  f"**Audience:** {ad['audience']}  ",
                  f"**Inspired by:** {ad['inspired']}", "",
                  "**Claims**", ""]
        lines += [f"- {c['text']}: {c['source']} ({STATUS[c['status']]})" for c in ad["claims"]]
        lines.append("")
    (HERE / "copy.md").write_text("\n".join(lines))


def build_gallery():
    template = (HERE / "gallery.template.html").read_text()
    js = lambda data: json.dumps(data, ensure_ascii=False).replace("</", "<\\/")
    page = template.replace("/*BRIEF_JSON*/[]", js(BRIEF)).replace("/*ADS_JSON*/[]", js(ADS))
    # gallery.html is published as a claude.ai artifact, which adds the document shell itself.
    (HERE / "gallery.html").write_text(page)
    # index.html is the same page as a standalone document, for GitHub Pages or any static host.
    head, body = page.split('<div class="wrap">', 1)
    (HERE / "index.html").write_text(
        '<!doctype html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n'
        '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n'
        '<meta name="robots" content="noindex">\n<style>body { margin: 0; } img { max-width: 100%; }</style>\n'
        + head + '</head>\n<body>\n<div class="wrap">' + body + '</body>\n</html>\n')


if __name__ == "__main__":
    check_brief()
    build_brief_markdown()
    build_drafts_markdown()
    build_gallery()
    print(f"built gallery.html, index.html, brief/copy.md and copy.md for {len(BRIEF)} campaign ads and {len(ADS)} drafts")
