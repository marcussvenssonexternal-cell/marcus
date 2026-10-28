"""Builds the review page (gallery.html for the artifact, index.html standalone), one share page per
campaign ad (share/<id>.html, each published as its own artifact so a single ad can be sent on its own),
and the copy decks (brief/copy.md for the campaign, copy.md for the earlier drafts) from the two copy.json
files. share/links.json holds each share page's published link; the review page shows them per ad.
brief/launch.csv lists every LinkedIn ad to build (asset × headline × intro) with its ad name and tracked URL.

    python3 build_gallery.py
"""

import csv
import json
import pathlib

HERE = pathlib.Path(__file__).parent
BRIEF = json.loads((HERE / "brief" / "copy.json").read_text())
ADS = json.loads((HERE / "copy.json").read_text())
LINKS_FILE = HERE / "share" / "links.json"
LINKS = json.loads(LINKS_FILE.read_text()) if LINKS_FILE.exists() else {}

# Share-page titles: a short name for each ad, used as the artifact's title.
SHORT = {"ad0": "AI built for entertainment", "ad1": "Same genre, different movie", "ad2": "Every asset, alive",
         "ad3": "Every second, time-coded", "m1": "From zero to hero", "m2": "Editorial lists", "m3": "Search by feeling",
         "c1": "Assets brought to life", "c2": "Thumbnail recipes", "c3": "Find the scene", "o1": "Automate QC",
         "v1": "Search by mood", "v2": "Story-aware ad breaks", "v3": "Endless shorts", "v4": "One recipe"}

STATUS = {"site": "On the website", "verify": "Check before launch", "illustrative": "Example values",
          "brief": "From the brief", "example": "Example values"}
SIGNOFF = "Vionlabs. AI built for entertainment."

# Tracking, as agreed in ../AGENTS.md. The first test wave (optimization/plan.md) runs h1/i1 on these assets.
UTM = "utm_source=linkedin&utm_medium=paid_social&utm_campaign=ai-built-for-entertainment"
FIRST_WAVE = {("ad0", "a0-L"), ("ad0", "a0-carousel"), ("ad0", "ad0-S"), ("ad1", "a1-L"), ("ad1", "a1b-L"),
              ("ad2", "a2-carousel"), ("ad2", "a2-L"), ("ad3", "a3-L"), ("ad3", "a3b-L"), ("ad3", "ad3-S")}


def check_brief():
    # The brief's copy rules: 3 headlines of max 70 characters, 3 intro texts (or more, for a targeted extra)
    # of max 600 that end on the sign-off; every ad has a destination.
    for ad in BRIEF:
        assert len(ad["headlines"]) == 3 and len(ad["intros"]) >= 3 and ad["destination"].startswith("https://"), ad["id"]
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
                  f"**Targeting:** {ad['targeting']}  ", f"**Destination:** {ad['destination']}", ""]
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


def linkedin_ads(ad):
    # One LinkedIn ad per single image, carousel or video; a carousel's ID is its card prefix plus "-carousel".
    for a in ad["assets"]:
        if "id" in a:
            yield a["id"], a["label"]
        elif "carousel" in a:
            yield a["carousel"][0].rsplit("-c", 1)[0] + "-carousel", a["label"]
        else:
            yield a["video"], a["label"]


def build_launch_csv():
    with open(HERE / "brief" / "launch.csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["ad", "asset", "format", "headline_id", "intro_id", "ad_name", "headline", "url", "first_wave"])
        for ad in BRIEF:
            for asset, label in linkedin_ads(ad):
                for h, headline in enumerate(ad["headlines"], 1):
                    for i in range(1, len(ad["intros"]) + 1):
                        tag = f"{ad['id']}-{asset}-h{h}-i{i}"
                        first = (ad["id"], asset) in FIRST_WAVE and h == 1 and i == 1
                        w.writerow([ad["id"], asset, label, f"h{h}", f"i{i}", f"{ad['id']}/{asset}/h{h}-i{i}", headline,
                                    f"{ad['destination']}?{UTM}&utm_content={tag}", "yes" if first else ""])


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


def js(data):
    return json.dumps(data, ensure_ascii=False).replace("</", "<\\/")


def build_share_pages():
    # One page per campaign ad, with only that ad, for sending to a teammate.
    template = (HERE / "gallery.template.html").read_text()
    out = HERE / "share"
    out.mkdir(exist_ok=True)
    for ad in BRIEF:
        title = f"{ad['num']} · {SHORT[ad['id']]}"
        page = (template.replace("<title>Vionlabs LinkedIn Ads</title>", f"<title>{title}</title>")
                .replace("/*BRIEF_JSON*/[]", js([ad])).replace("/*ADS_JSON*/[]", "[]")
                .replace("/*ONLY*/null", js(ad["id"])).replace("/*LINKS_JSON*/{}", "{}"))
        (out / f"{ad['id']}.html").write_text(page)


def build_gallery():
    template = (HERE / "gallery.template.html").read_text()
    page = (template.replace("/*BRIEF_JSON*/[]", js(BRIEF)).replace("/*ADS_JSON*/[]", js(ADS))
            .replace("/*LINKS_JSON*/{}", js(LINKS)))
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
    build_share_pages()
    build_launch_csv()
    print(f"built gallery.html, index.html, {len(BRIEF)} share pages, brief/copy.md and copy.md "
          f"for {len(BRIEF)} campaign ads and {len(ADS)} drafts ({len(LINKS)} share links)")
