"""Builds the review page (gallery.html for the artifact, index.html standalone), one share page per
campaign ad (share/<id>.html, each published as its own artifact so a single ad can be sent on its own),
and the copy decks (brief/copy.md for the campaign, copy.md for the earlier drafts) from the two copy.json
files. share/links.json holds each share page's published link; the review page shows them per ad.
brief/launch.csv lists every LinkedIn ad to build (asset × headline × intro) with its ad name and tracked URL;
brief/carousel-cards.csv gives each carousel card its headline and tracked URL. Retired assets (copy.json "retired",
e.g. the big film frames replaced by their rights-safe "r" versions) keep their rows, so past results stay traceable,
with a status saying what to use instead; the review page folds them away.

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
          "brief": "From the brief", "example": "Example values", "board": "Board decision"}
SIGNOFF = "Vionlabs. AI built for entertainment."

# Tracking, as agreed in ../AGENTS.md. The first test wave (optimization/plan.md) runs one headline and intro per asset:
# h1/i1, except Ad 0's new hero image and video, whose i5 describes what they show. The rights-safe "r" assets
# took the places of the retired ones (Oct 2026).
UTM = "utm_source=linkedin&utm_medium=paid_social&utm_campaign=ai-built-for-entertainment"
FIRST_WAVE = {("ad0", "a0r-L"): (1, 5), ("ad0", "a0r-carousel"): (1, 1), ("ad0", "ad0r-S"): (1, 5), ("ad1", "a1-L"): (1, 1),
              ("ad1", "a1b-L"): (1, 1), ("ad2", "a2r-carousel"): (1, 1), ("ad2", "a2-L"): (1, 1), ("ad3", "a3r-L"): (1, 1),
              ("ad3", "a3b-L"): (1, 1), ("ad3", "ad3r-S"): (1, 1)}


def check_brief():
    # The brief's copy rules: 3 headlines of max 70 characters, 3 intro texts (or more, for a targeted extra)
    # of max 600 that end on the sign-off; every ad has a destination.
    for ad in BRIEF:
        assert len(ad["headlines"]) == 3 and len(ad["intros"]) >= 3 and ad["destination"].startswith("https://"), ad["id"]
        for h in ad["headlines"]:
            assert len(h) <= 70, (ad["id"], h)
        for i in ad["intros"]:
            assert len(i) <= 600 and i.endswith(SIGNOFF), (ad["id"], i[:40])
        live = {asset_id(a) for a in ad["assets"] if not a.get("retired")}
        for a in ad["assets"]:
            # a retired asset names a live replacement in the same ad
            assert not a.get("retired") or a.get("replaced_by") in live, (ad["id"], asset_id(a))
            # LinkedIn carousel cards: one headline each, at most 45 characters
            if "carousel" in a:
                assert len(a["cards"]) == len(a["carousel"]) and all(len(c) <= 45 for c in a["cards"]), (ad["id"], a["carousel"][0])


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
                line = f"- {a['label']}: `png/{a['id']}.png`"
            elif "carousel" in a:
                line = f"- {a['label']}: " + ", ".join(f"`png/{c}.png`" for c in a["carousel"])
            else:
                line = f"- {a['label']}: `video/{a['video']}.mp4`"
            lines.append(f"- ~~{line[2:]}~~ retired, use `{a['replaced_by']}`" if a.get("retired") else line)
        lines += ["", "**Headlines**", ""] + [f"{n}. {h} ({len(h)})" for n, h in enumerate(ad["headlines"], 1)] + [""]
        for n, intro in enumerate(ad["intros"], 1):
            lines += [f"**Intro text {n}** ({len(intro)} characters)", "", *quote(intro), ""]
        lines += ["**Claims**", ""] + [f"- {c['text']}: {c['source']} ({STATUS[c['status']]})" for c in ad["claims"]] + [""]
    (HERE / "brief" / "copy.md").write_text("\n".join(lines))


def linkedin_ads(ad):
    # One LinkedIn ad per single image, carousel or video, with its status ("" if it can run).
    for a in ad["assets"]:
        yield asset_id(a), a["label"], status(a)


def carousel_id(a):
    # A carousel's ID is its card prefix plus "-carousel", unless it sets its own ("cid"), as a revised card set does.
    return a.get("cid") or a["carousel"][0].rsplit("-c", 1)[0] + "-carousel"


def asset_id(a):
    return a.get("id") or a.get("video") or carousel_id(a)


def status(a):
    return f"retired (big film frame): use {a['replaced_by']}" if a.get("retired") else ""


def build_launch_csv():
    with open(HERE / "brief" / "launch.csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["ad", "asset", "format", "headline_id", "intro_id", "ad_name", "headline", "url", "first_wave", "status"])
        for ad in BRIEF:
            for asset, label, st in linkedin_ads(ad):
                for h, headline in enumerate(ad["headlines"], 1):
                    for i in range(1, len(ad["intros"]) + 1):
                        tag = f"{ad['id']}-{asset}-h{h}-i{i}"
                        first = FIRST_WAVE.get((ad["id"], asset)) == (h, i)
                        w.writerow([ad["id"], asset, label, f"h{h}", f"i{i}", f"{ad['id']}/{asset}/h{h}-i{i}", headline,
                                    f"{ad['destination']}?{UTM}&utm_content={tag}", "yes" if first else "", st])


def build_carousel_cards_csv():
    # LinkedIn carousels have no ad-level headline: each card carries its own headline and URL. The ad name keeps
    # "h1" so it matches the carousel's row in launch.csv; utm_content adds the card number.
    with open(HERE / "brief" / "carousel-cards.csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["ad", "carousel", "intro_id", "ad_name", "card", "card_asset", "card_headline", "card_url", "status"])
        for ad in BRIEF:
            for a in ad["assets"]:
                if "carousel" not in a:
                    continue
                cid = carousel_id(a)
                for i in range(1, len(ad["intros"]) + 1):
                    for n, (card, headline) in enumerate(zip(a["carousel"], a["cards"]), 1):
                        tag = f"{ad['id']}-{cid}-h1-i{i}-c{n}"
                        w.writerow([ad["id"], cid, f"i{i}", f"{ad['id']}/{cid}/h1-i{i}", n, card, headline,
                                    f"{ad['destination']}?{UTM}&utm_content={tag}", status(a)])


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
    build_carousel_cards_csv()
    print(f"built gallery.html, index.html, {len(BRIEF)} share pages, brief/copy.md and copy.md "
          f"for {len(BRIEF)} campaign ads and {len(ADS)} drafts ({len(LINKS)} share links)")
