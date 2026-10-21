# Vionlabs LinkedIn ads

Draft single-image LinkedIn ads (1200×1200) for every Vionlabs product, with intro text,
headlines, CTAs and a source check on every claim.

| Path | What it is |
| --- | --- |
| `creatives/png/` | The finished ad images, ready to upload to LinkedIn Campaign Manager |
| `creatives/copy.md` | Intro text, headline, CTA, audience and claim sources for each ad |
| `creatives/index.html` | The review page (all ads with their copy) |
| `creatives/ads.html` | Source for every ad; `img/` holds the website images they use |
| `fetch_ads.py` | Pulls ads from the LinkedIn Ad Library through Apify (needs `APIFY_TOKEN`) |

## Changing an ad

1. Edit the ad in `creatives/ads.html`, or its copy in `creatives/copy.json`.
2. `node creatives/render.cjs` re-renders every PNG (or `node creatives/render.cjs ag1 cu2` for some).
3. `python3 creatives/build_gallery.py` rebuilds the review page and `copy.md`.

## Hosting the review page

GitHub Pages serves this branch as a website. The root `index.html` redirects to
`linkedin-ads-research/creatives/`, and `.nojekyll` makes Pages serve the files as they are.

To turn it on (once): repository **Settings → Pages → Build and deployment**, set **Source** to
**Deploy from a branch**, pick this branch and **/ (root)**, and save. The page is then at
<https://marcussvenssonexternal-cell.github.io/marcus/> and updates on every push to the branch.

The repository is public, so the page and everything in it can be opened by anyone with the
link. The page asks search engines not to index it.
