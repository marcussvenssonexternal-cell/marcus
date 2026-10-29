# Film and TV imagery in the LinkedIn ads: rights check

**Status: rule set; revised assets awaiting Marcus's approval (29 Oct 2026).** The board's decision: famous films
and series may appear as **small posters among many, never as one big frame or close-up**; for a big frame, take a
lesser-known film (Arash: "ta lite mindre kända filmer"). Every asset that broke that rule has a rights-safe version
(an `r` in its ID) that keeps the original layout and only swaps the famous title on the big frame for a
lesser-known one. Nothing changes on LinkedIn until Marcus has approved them. Lesser-known titles and small posters
still show real films and actors, so this lowers the risk rather than removing it; a sign-off from whoever handles
legal at Vionlabs is still worth having. This note is not legal advice.

## The rule, and how it is checked

The board gave two examples from Video 4. The rushing wall of thumbnails ("RECIPE APPLIED · 1,646 / 2,431 TITLES")
is fine. The La La Land frame with its 9:16 close-up is not.

- **Famous titles:** no single one may cover more than **7.5% of a square the width of the ad**, about 390×220 px
  in a 1080 px wide ad. The wall's thumbnails peak at 5.0% (1:1) and 7.0% (9:16); the La La Land frame is 19% and
  41%. So the limit is the size of the thumbnails the board approved.
- **Lesser-known titles** may fill a big frame: Papillon (2017), True History of the Kelly Gang, Upgrade, Rescue
  Dawn, Can You Keep a Secret?, Vacation Friends, Shaolin Soccer, Fanboys and The Incredible Burt Wonderstone. The
  same list is in `rights-audit.cjs`, `brief-anim.js` and `brief.js`; change it in all three.
- **How:** `node rights-audit.cjs` measures every famous film or TV image as it is actually drawn (tilted, scaled
  and clipped), in every campaign image and every 0.2 s of every video, and writes `rights-audit.json`.

## What changed

Each revision keeps the original layout, copy and motion; only the image on the big frame changes.

| To be replaced | Rights-safe version | What changed |
| --- | --- | --- |
| `a0-L`, `a0-S` | `a0r-L`, `a0r-S` | Hero frame: Papillon instead of The Shawshank Redemption. Image text "man, sea, cliff." New intro `i5` matches it. |
| `a0-carousel`, `a0b-carousel` | `a0r-carousel` | Card 1's viewfinder shows the Kelly Gang instead of Skyfall (`a0-c1r`); the other cards are unchanged. |
| `ad0-S`, `ad0-V` | `ad0r-S`, `ad0r-V` | Papillon instead of The Shawshank Redemption; the library grid of small posters stays. |
| `a2-carousel` | `a2r-carousel` | Card 3's four sword-fight scenes at 96% size, just under the limit (`a2-c3r`). |
| `a3-L`, `a3-S`, `ad3-S`, `ad3-V` | `a3r-L`, `a3r-S`, `ad3r-S`, `ad3r-V` | The player shows the Kelly Gang instead of Peaky Blinders. |
| `m3-carousel` | `m3r-carousel` | Cards 1–3: the four posters at 96% size (`m3-c1r` to `m3-c3r`). |
| `c3-carousel` | `c3r-carousel` | The reframe and its phone show the Kelly Gang instead of Gladiator (`c3-c3r`); the last phone shows Shaolin Soccer instead of Troy (`c3-c4r`). |
| `o1-carousel`, `o1-L` | `o1r-carousel`, `o1r-L` | Players: the Kelly Gang instead of Peaky Blinders (`o1-c1r`, `o1-c5r`, `o1r-L`), Vacation Friends instead of Succession (`o1-c2r`). Card 3 already shows a lesser-known title and stays. |
| `v1-S/V`, `v1b-S/V` | `v1r-S/V`, `v1br-S/V` | The chosen result is Vacation Friends instead of Ticket to Paradise; the searches nearest the camera in the pull-back show lesser-known titles. |
| `v2-S/V` | `v2r-S/V` | The episode is Upgrade instead of Succession; the episodes nearest the camera in the pull-back are lesser-known titles. |
| `v3-S/V` | `v3r-S/V` | Archive, six moments, reframe and the feed of shorts use lesser-known titles (the clip is the Kelly Gang). The rushing wall stays. |
| `v4-S/V` | `v4r-S/V` | The rejected frames and the finished thumbnail use lesser-known titles (Can You Keep a Secret? instead of La La Land). The wall stays. |

Unchanged, and within the rule: `a1-*`, `a2-L`, `a3b-*`, `m1-*`, `m2-*`, `m3-L`, `m3-S`, `c1-*`, `c2-*`, `c3-L`.
Replaced assets keep their rows in `launch.csv` and `carousel-cards.csv`; the new ones say "awaiting Marcus's
approval" there until he approves them.

Still open:
- C2's intro 2 names Gladiator in the text ("finds a different film inside Gladiator"). That's no image, but it
  ties the ad to a studio's title; swap in a new intro if the board wants no names at all.
- The website uses the same title art and frames, so the same question applies there.

## Inventory of the original assets (before the revision)

54 of the 61 campaign assets (images, carousel cards and videos) show frames or title
art from **45 commercial films and series**, all taken from vionlabs.com. That includes every
single image drafted in LinkedIn except a3b-L (which is on hold for its claim), and all of the videos. Only 7 assets show no film imagery: `a0-c5`, `a0-c5b`, `a3b-L`, `a3b-S`, `m3-c4`, `c3-c1`, `o1-c4`.

| Ad | Assets | Titles shown |
| --- | --- | --- |
| Ad 0 | 9 | American Wedding, Anyone But You, Argo, Braveheart, Candyman (2021), Fanboys, Forrest Gump, Friday Night Lights, Get Hard, Gladiator, Gone in 60 Seconds, Independence Day, John Wick: Chapter 2, King Richard, Kingdom of Heaven, La La Land, Law Abiding Citizen, Lord of War, Papillon (2017), Peaky Blinders (series), Reacher (series), Rescue Dawn, Shaolin Soccer, Skyfall, Spider-Man 3, Spy Game, Succession (series), The Dark Knight, The Fall Guy, The Incredible Burt Wonderstone, The Last Samurai, The Northman, The Secret: Dare to Dream, The Shawshank Redemption, Ticket to Paradise, Troy, True History of the Kelly Gang, Upgrade, Vacation Friends, Valerian and the City of a Thousand Planets, We Bought a Zoo, What Women Want, a Fast & Furious film (title art), a Godzilla film (title art), an X-Men film (title art) |
| Ad 1 | 4 | American Wedding, Anyone But You, Fanboys, Forrest Gump, Get Hard, John Wick: Chapter 2, La La Land, Law Abiding Citizen, Papillon (2017), Reacher (series), Skyfall, The Shawshank Redemption, Ticket to Paradise, True History of the Kelly Gang, Vacation Friends, We Bought a Zoo, What Women Want |
| Ad 2 | 6 | American Wedding, Anyone But You, Argo, Braveheart, Candyman (2021), Fanboys, Forrest Gump, Friday Night Lights, Get Hard, Gladiator, Gone in 60 Seconds, Independence Day, John Wick: Chapter 2, King Richard, Kingdom of Heaven, La La Land, Law Abiding Citizen, Lord of War, Papillon (2017), Peaky Blinders (series), Reacher (series), Rescue Dawn, Shaolin Soccer, Skyfall, Spider-Man 3, Spy Game, Succession (series), The Dark Knight, The Fall Guy, The Incredible Burt Wonderstone, The Last Samurai, The Northman, The Secret: Dare to Dream, The Shawshank Redemption, Ticket to Paradise, Troy, True History of the Kelly Gang, Upgrade, Vacation Friends, Valerian and the City of a Thousand Planets, We Bought a Zoo, What Women Want, a Fast & Furious film (title art), a Godzilla film (title art), an X-Men film (title art) |
| Ad 3 | 5 | Peaky Blinders (series) |
| M1 | 2 | La La Land |
| M2 | 8 | American Wedding, Anyone But You, Argo, Braveheart, Candyman (2021), Fanboys, Forrest Gump, Friday Night Lights, Get Hard, Gladiator, Gone in 60 Seconds, Independence Day, John Wick: Chapter 2, King Richard, Kingdom of Heaven, La La Land, Law Abiding Citizen, Lord of War, Papillon (2017), Peaky Blinders (series), Reacher (series), Rescue Dawn, Shaolin Soccer, Skyfall, Spider-Man 3, Spy Game, Succession (series), The Dark Knight, The Fall Guy, The Incredible Burt Wonderstone, The Last Samurai, The Northman, The Secret: Dare to Dream, The Shawshank Redemption, Ticket to Paradise, Troy, True History of the Kelly Gang, Upgrade, Vacation Friends, Valerian and the City of a Thousand Planets, We Bought a Zoo, What Women Want, a Fast & Furious film (title art), a Godzilla film (title art), an X-Men film (title art) |
| M3 | 6 | Anyone But You, Argo, Friday Night Lights, King Richard, La La Land, Lord of War, Papillon (2017), Rescue Dawn, Shaolin Soccer, Ticket to Paradise, What Women Want |
| C1 | 2 | Gladiator |
| C2 | 3 | Anyone But You, Argo, Forrest Gump, Friday Night Lights, Gladiator, King Richard, La La Land, Papillon (2017), Reacher (series), Skyfall, Succession (series), The Northman, The Secret: Dare to Dream, Ticket to Paradise, Troy, True History of the Kelly Gang, Vacation Friends, We Bought a Zoo, What Women Want |
| C3 | 5 | Braveheart, Gladiator, Kingdom of Heaven, The Last Samurai, The Northman, Troy |
| O1 | 6 | Peaky Blinders (series), Succession (series), The Secret: Dare to Dream |
| Video 1 | 2 | American Wedding, Anyone But You, Argo, Braveheart, Fanboys, Forrest Gump, Get Hard, Gladiator, John Wick: Chapter 2, King Richard, La La Land, Papillon (2017), Peaky Blinders (series), Reacher (series), Rescue Dawn, Shaolin Soccer, Skyfall, Spy Game, Succession (series), The Northman, Ticket to Paradise, Troy, Vacation Friends, We Bought a Zoo, What Women Want |
| Video 2 | 1 | Argo, Candyman (2021), Gladiator, John Wick: Chapter 2, King Richard, La La Land, Lord of War, Peaky Blinders (series), Reacher (series), Skyfall, Spy Game, Succession (series), The Secret: Dare to Dream, Ticket to Paradise, Upgrade |
| Video 3 | 1 | Argo, Braveheart, Forrest Gump, Gladiator, John Wick: Chapter 2, King Richard, Kingdom of Heaven, La La Land, Lord of War, Papillon (2017), Peaky Blinders (series), Reacher (series), Shaolin Soccer, Skyfall, Spy Game, The Last Samurai, The Northman, The Shawshank Redemption, Ticket to Paradise, Troy |
| Video 4 | 1 | American Wedding, Anyone But You, Argo, Braveheart, Candyman (2021), Fanboys, Forrest Gump, Friday Night Lights, Get Hard, Gladiator, Gone in 60 Seconds, Independence Day, John Wick: Chapter 2, King Richard, Kingdom of Heaven, La La Land, Lord of War, Papillon (2017), Peaky Blinders (series), Reacher (series), Shaolin Soccer, Skyfall, Spy Game, Succession (series), The Fall Guy, The Incredible Burt Wonderstone, The Last Samurai, The Northman, The Secret: Dare to Dream, The Shawshank Redemption, Ticket to Paradise, Troy, True History of the Kelly Gang, Upgrade, Vacation Friends, Valerian and the City of a Thousand Planets, We Bought a Zoo, What Women Want, a Fast & Furious film (title art), a Godzilla film (title art), an X-Men film (title art) |

Most used: Ticket to Paradise (29), Gladiator (28), Skyfall (25), King Richard (25), What Women Want (24), Vacation Friends (24), We Bought a Zoo (23), Anyone But You (23). The per-asset list is in
`rights-inventory.json`. `node inventory.cjs` regenerates it from the rendered pages, so it can't drift from the ads.

## What the rules say

- **Copyright and trademark.** Film frames, posters and title art belong to the studio or distributor, whatever
  the film's size or age. LinkedIn's Ads Agreement makes the advertiser warrant it holds all rights to its ads,
  and its Advertising Policies send copyright and trademark owners to a takedown process.
- **People in ads (Sweden).** Lag (1978:800) om namn och bild i reklam: a business may not use an identifiable
  person's image in its marketing without that person's consent. Intent or gross negligence can mean fines and
  damages. Every frame showing a recognisable actor is covered, in a big film or a small one.
- **Older films.** In the EU a film is protected until 70 years after the death of the last of its director,
  screenwriter, dialogue writer and composer. "Old" rarely means free, and US public-domain status doesn't carry over.

So **choosing less-known films lowers the chance of a complaint, not the legal exposure**. Even the smaller titles
in our set star well-known actors (Christian Bale in Rescue Dawn, Russell Crowe in True History of the Kelly
Gang, Nicolas Cage in Lord of War, Rami Malek in Papillon).

## Options if the board later wants no film imagery at all

1. **Licensed stock footage and stills** (e.g. Shutterstock, Adobe Stock, Artgrid, Storyblocks), on a licence that
   covers advertising and with model releases for the people shown. It looks like real film scenes, and it is
   what TwelveLabs' own video ads use. We'd give the "titles" made-up names on title cards. Cost: a stock
   subscription or per-clip licences.
2. **Open films under Creative Commons Attribution** (Blender Studio's open movies, e.g. Sintel, Spring, Charge,
   Sprite Fright, Agent 327). Commercial use is allowed with a credit line, at no cost. Prefer the animated
   ones: CC licences don't cover actors' personality rights. There are about 10–15 titles; with stock they could
   fill a catalogue. Check each film's exact licence on its Blender Studio page; one source lists Cosmos Laundromat as
   share-alike.
3. **Customer or partner content with written permission**, e.g. titles from a customer happy to be shown.
   Sales would need to ask.
4. **Smaller films, as the board suggested**: only frames with no recognisable faces (wide shots, backs,
   landscapes, objects), and no posters or title art. This is risk reduction, not clearance, and still needs
   legal sign-off.

**Recommendation before the board's rule:** options 1 and 2 for everything that runs as paid media. They keep the "real film" look the
ads need without anyone else's rights in them. The current versions can stay on the review page as internal drafts.
The website uses the same title art, so the same question applies there.

## Changing the imagery

The ads are built from data, so new imagery means new image files and a re-render. The layouts and copy don't
change, and every changed asset gets a new ID (see `../../AGENTS.md`). Blender Studio, Wikimedia Commons and
stock sites are blocked from the creative agent's environment, so files have to be uploaded, shared on Google
Drive, or those domains allowed in the environment's network settings.
