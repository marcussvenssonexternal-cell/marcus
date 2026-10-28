#!/usr/bin/env python3
"""Turn a long read into a post for the Vionlabs blog (vionlabs.com/news, Webflow's "News" collection).

    python3 webflow.py ad-breaks-01 > item.json

Prints the item's fieldData as JSON, ready for the Webflow connector's data_cms_tool
create_collection_items (stage it with isDraft true) or update_collection_items. Arash approves
the Google Doc; then publish_collection_items puts the post live.

The piece needs a "website" block: title, slug, summary, url, and "assets", which maps each image
path in the pack (the cover, every figure) to the Webflow asset it was uploaded as
({"fileId": ..., "url": ...}). Upload images with data_assets_tool create_asset and a multipart
POST of the file to the S3 uploadUrl it returns. The script refuses to build while an image has no
asset or the text still has [check], [Arash: …] or [Team: …] markers.
"""
import html
import json
import re
import sys
from datetime import datetime, timezone

from gdoc import OPEN, TOPICS, inline, kept_out, public_text

SITE_ID = "67978ee27d95b7ff0119d2ea"        # Vionlabs Video AI (vionlabs.com)
NEWS_COLLECTION = "67978ee27d95b7ff0119d37e"  # "News": the blog at vionlabs.com/news/<slug>
AUTHORS = {"Arash Pendari": "6989e53a9c61c3baec3826fa"}
FIGURE = ('<figure class="w-richtext-figure-type-image w-richtext-align-fullwidth" data-rt-type="image" '
          'data-rt-align="fullwidth"><div><img alt="{alt}" src="{src}" width="auto" height="auto" loading="lazy"></div></figure>')


def rt(s):
    """Inline Markdown in the tags Webflow's editor writes."""
    return inline(s).replace("<b>", "<strong>").replace("</b>", "</strong>").replace("<i>", "<em>").replace("</i>", "</em>")


def rich_text(src, assets):
    """Markdown body -> Webflow rich text: plain tags, no inline styles, figures in Webflow's markup."""
    out = []
    for b in [x.strip("\n") for x in src.split("\n\n") if x.strip()]:
        lines = b.split("\n")
        im = re.match(r"^!\[([^\]]*)\]\(([^)\s]+)\)$", b)
        m = re.match(r"^(#{2,4})\s+(.*)$", b)
        if im:
            if im.group(2) not in assets:
                sys.exit(f"Upload {im.group(2)} to Webflow and add it to website.assets first")
            out.append(FIGURE.format(alt=html.escape(im.group(1)), src=html.escape(assets[im.group(2)]["url"])))
        elif m and "\n" not in b:
            lv = len(m.group(1))
            out.append(f"<h{lv}>{rt(m.group(2))}</h{lv}>")
        elif all(re.match(r"^\s*[-*]\s+", l) for l in lines):
            out.append("<ul>" + "".join(f"<li>{rt(re.sub(r'^\s*[-*]\s+', '', l))}</li>" for l in lines) + "</ul>")
        elif all(re.match(r"^\s*\d+[.)]\s+", l) for l in lines):
            out.append("<ol>" + "".join(f"<li>{rt(re.sub(r'^\s*\d+[.)]\s+', '', l))}</li>" for l in lines) + "</ol>")
        else:
            out.append("<p>" + "<br>".join(rt(l) for l in lines) + "</p>")
    return "".join(out)


def field_data(piece_id, published=None):
    for path in TOPICS.glob("*.json"):
        for p in (json.loads(path.read_text()).get("pack") or {}).get("pieces", []):
            if p.get("id") != piece_id:
                continue
            web, cover = p.get("website") or {}, p.get("cover") or {}
            missing = [k for k in ("title", "slug", "summary") if not web.get(k)]
            if p.get("kind") != "article" or missing:
                sys.exit(f"{piece_id} isn't a long read with website fields (missing: {', '.join(missing) or 'kind article'})")
            left = sorted(set(OPEN.findall(p["body"])))
            if left:
                sys.exit(f"{piece_id} still has open markers: {', '.join(left)}")
            named = kept_out(public_text(p))
            if named:
                sys.exit(f"{piece_id} names {', '.join(named)}, which we keep out of public content (brand.md)")
            assets = web.get("assets") or {}
            data = {"name": web["title"], "slug": web["slug"], "post-summary": web["summary"],
                    "post-body": rich_text(p["body"], assets),
                    "author": AUTHORS[web.get("author", "Arash Pendari")],
                    "original-published-on-date": published or datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.000Z")}
            if cover.get("image"):
                if cover["image"] not in assets:
                    sys.exit(f"Upload {cover['image']} to Webflow and add it to website.assets first")
                img = {"fileId": assets[cover["image"]]["fileId"], "url": assets[cover["image"]]["url"], "alt": cover.get("alt", "")}
                data["main-image"] = data["thumbnail-image"] = img
            return data
    sys.exit(f"No piece with id {piece_id}")


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    if len(args) != 1:
        sys.exit(__doc__)
    print(json.dumps(field_data(args[0]), ensure_ascii=False, indent=1))
