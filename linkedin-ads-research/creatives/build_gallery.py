"""Builds the review page (gallery.html for the artifact, index.html standalone) and copy.md
from copy.json.

    python3 build_gallery.py
"""

import json
import pathlib

HERE = pathlib.Path(__file__).parent
ADS = json.loads((HERE / "copy.json").read_text())

STATUS = {"site": "On the website", "verify": "Check before launch", "illustrative": "Example values"}


def build_markdown():
    lines = ["# Vionlabs LinkedIn ad copy", "",
             "Single-image ads, 1200×1200. Images in `png/`, sources in `ads.html`.", ""]
    for ad in ADS:
        lines += [f"## {ad['id']} · {ad['product']} · {ad['name']}", "",
                  f"![{ad['name']}](png/{ad['id']}.png)", "",
                  "**Intro text**", "", *[f"> {l}" if l else ">" for l in ad["intro"].split("\n")], "",
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
    data = json.dumps(ADS, ensure_ascii=False).replace("</", "<\\/")
    page = template.replace("/*ADS_JSON*/[]", data)
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
    build_markdown()
    build_gallery()
    print(f"built gallery.html, index.html and copy.md for {len(ADS)} ads")
