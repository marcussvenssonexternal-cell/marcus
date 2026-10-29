# Vionlabs LinkedIn ads

The **AI built for entertainment** campaign from Viktor's ad brief (11 ads: a brand ad, three audience
ads and seven feature follow-ups), plus the earlier single-image drafts. Every ad has its copy,
targeting and a source check on every claim.

| Path | What it is |
| --- | --- |
| `creatives/brief/png/` | Campaign images, ready for LinkedIn Campaign Manager: `-S` 1080×1080 (single image and carousel cards), `-L` 1200×627 |
| `creatives/brief/video/` | Campaign videos, 1:1 (`-S`) and 9:16 (`-V`): Ad 0 (12 s), Ad 3 (8 s), and the video series `v1`–`v4` (about 21 s each) |
| `creatives/brief/copy.md` | Three headlines and three intro texts per ad, with assets, targeting and claim sources |
| `creatives/png/`, `creatives/copy.md` | The earlier drafts (1200×1200) and their copy |
| `creatives/index.html` | The review page: the campaign first, then the earlier drafts |
| `creatives/share/` | One page per campaign ad, each published as its own link so a single ad can be sent on its own; `links.json` holds the links |
| `creatives/brief.html`, `creatives/brief-anim.html` | Sources for the campaign images and videos; `ads.html` for the drafts; `img/` holds the website images they use |
| `references/` | Notes on reference ads, such as the TwelveLabs videos the series is modelled on |
| `AGENTS.md` | How the creative and optimization agents work together: sessions, ad IDs, naming and UTMs |
| `fetch_ads.py` | Pulls ads from the LinkedIn Ad Library through Apify (needs `APIFY_TOKEN`) |

## Changing an ad

1. Edit the campaign ad in `creatives/brief.js` (videos: `creatives/brief-anim.js`), or its copy in
   `creatives/brief/copy.json`. The earlier drafts live in `creatives/ads.html` and `creatives/copy.json`.
2. Re-render the images from `creatives/`:
   `PAGE=brief.html OUT=brief/png node render.cjs` (add ids such as `a1-S m2-c3` to render only those);
   `node render.cjs` for the drafts. `node record.cjs` re-records the videos (`node record.cjs ad3-V` for one).
   `node rights-audit.cjs` checks every image and video against the board's rule for film and TV imagery.
3. `python3 creatives/build_gallery.py` rebuilds the review page and both `copy.md` files, and checks
   the brief's copy limits (headlines ≤ 70 characters, intro texts ≤ 600 ending on the sign-off).

## Hosting the review page

GitHub Pages serves this branch as a website. The root `index.html` redirects to
`linkedin-ads-research/creatives/`, and `.nojekyll` makes Pages serve the files as they are.

To turn it on (once): repository **Settings → Pages → Build and deployment**, set **Source** to
**Deploy from a branch**, pick this branch and **/ (root)**, and save. The page is then at
<https://marcussvenssonexternal-cell.github.io/marcus/> and updates on every push to the branch.

The repository is public, so the page and everything in it can be opened by anyone with the
link. The page asks search engines not to index it.
