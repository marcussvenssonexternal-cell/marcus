"""Builds gallery.html (the review page) and copy.md from copy.json.

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
    (HERE / "gallery.html").write_text(template.replace("/*ADS_JSON*/[]", data))


if __name__ == "__main__":
    build_markdown()
    build_gallery()
    print(f"built gallery.html and copy.md for {len(ADS)} ads")
