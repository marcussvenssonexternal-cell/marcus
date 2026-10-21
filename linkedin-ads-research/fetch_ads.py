"""Pull LinkedIn Ad Library ads for Vionlabs and TwelveLabs via the Apify
actor dltik/linkedin-ad-library, and save them as JSON under data/.

Needs APIFY_TOKEN in the environment and network access to api.apify.com.
Cost is $0.002 per ad returned; a full run tops out around $0.30.

    python3 linkedin-ads-research/fetch_ads.py
"""

import json
import os
import pathlib
import sys
import urllib.request

ACTOR = "dltik~linkedin-ad-library"
ENDPOINT = f"https://api.apify.com/v2/acts/{ACTOR}/run-sync-get-dataset-items"

# LinkedIn serves ~24 ads per query, so each advertiser gets a few query
# spellings; results are deduped by ad_id and filtered to the real advertiser.
ADVERTISERS = {
    "vionlabs": ["Vionlabs", "Vionlabs AB"],
    "twelvelabs": ["Twelve Labs", "TwelveLabs"],
}

OUT_DIR = pathlib.Path(__file__).parent / "data"


def run_actor(token, account_owner):
    body = json.dumps({
        "accountOwner": account_owner,
        "dateOption": "all-time",
        "maxResults": 24,
        "enrichDetails": True,
    }).encode()
    req = urllib.request.Request(
        ENDPOINT,
        data=body,
        headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=300) as resp:
        return json.load(resp)


def normalise(name):
    return "".join(ch for ch in (name or "").lower() if ch.isalnum())


def main():
    token = os.environ.get("APIFY_TOKEN")
    if not token:
        sys.exit("APIFY_TOKEN is not set")
    OUT_DIR.mkdir(exist_ok=True)

    for slug, queries in ADVERTISERS.items():
        ads = {}
        for query in queries:
            items = run_actor(token, query)
            kept = [ad for ad in items if slug in normalise(ad.get("advertiser_name"))]
            print(f"{query!r}: {len(items)} returned, {len(kept)} from {slug}")
            for ad in kept:
                ads[ad["ad_id"]] = ad
        path = OUT_DIR / f"{slug}.json"
        path.write_text(json.dumps(list(ads.values()), indent=2, ensure_ascii=False))
        print(f"saved {len(ads)} ads to {path}")


if __name__ == "__main__":
    main()
