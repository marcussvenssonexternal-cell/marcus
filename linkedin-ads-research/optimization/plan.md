# Optimization plan: AI built for entertainment (AIBFE)

This plan covers how the 15 ads in `creatives/brief/copy.json` get launched, tested, measured and reported. The
numbers it rests on are in [`baseline.md`](baseline.md). The optimization agent proposes; Marcus approves anything
that changes spend, budgets, targeting or what is live. All budget figures below are proposals.

## 0. Before launch: fix measurement

The baseline shows that, as things stand, we couldn't tell which new ad works. These come first:

1. **Make "Book a demo" a conversion.** There is one rule, "Booked a meeting", and it recorded one view-through
   conversion in 90 days. The Insight Tag needs to fire on the demo booking confirmation, not just the page
   visit. Test it with a real booking before launch.
2. **Put the UTM scheme from `AGENTS.md` on every ad.** None of the current ads have UTMs.
3. **Turn off LinkedIn Audience Network** for the new campaigns, or at least report it separately. 93% of the Plex
   video campaign's impressions and 323 of its 324 clicks came from Audience Network. That inflated its CTR to 2.29%
   against 0.10% on the feed.
4. **Clear the "Check before launch" claims.** Ads with an unverified claim can't run as written: `ad0` (3), `ad3` (2),
   `v2` (2), and one each in `v1`, `v3`, `v4`, `ad1`, `ad2`, `m1`, `m2`, `c1`, `o1`. Most of those are rights checks on
   title art.
5. **Keep AIBFE separate from the legacy campaigns.** Put it in its own campaign groups. The five legacy campaigns
   (about $91 a day in budgets) reach the same people. Marcus decides whether they pause, scale down or keep
   running as a control.
6. **Hit Manager-and-up targeting.** Entry level was the second-largest seniority group in the baseline. The brief
   targets Manager and up (Senior and up for Ad 1).

**Asset IDs (29 Oct rights update).** The board allows famous titles only as small posters, so every asset with a big
film frame was retired and replaced by an `r` version: a0-L/S → a0r-L/S, a0-carousel and a0b-carousel →
a0r-carousel, ad0-S/V → ad0r-S/V (Ad 0 copy moves to intro i5), a2-carousel → a2r-carousel, a3-L/S → a3r-L/S,
ad3-S/V → ad3r-S/V, m3/c3/o1 carousels → m3r/c3r/o1r-carousel, o1-L → o1r-L, v1/v1b/v2–v4 videos → v1r, v1br,
v2r–v4r. Unchanged: a1-*, a1b-*, a2-L, a3b-*, m1-*, m2-*, m3-L/S, c1-*, c2-*, c3-L. Source: `creatives/brief/launch.csv`
(status column) on the creative branch.

## 1. KPIs by stage

The funnel follows the brief: Ad 0 builds awareness, Ads 1–3 qualify by audience, follow-ups and the video series
retarget people who engaged. Each stage has one **primary** KPI to judge it on, plus guardrails.

| Stage | Ads | Job | Primary KPI | Secondary / guardrails | Baseline to beat |
| --- | --- | --- | --- | --- | --- |
| Brand | `ad0` (image, carousel, video) | Reach the right decision makers cheaply and build retargeting pools | **Cost per engaged member in target seniority**; reach and frequency | CPM; video view rate and 25%/50% completion; carousel card swipes; share of impressions at Manager+ in target industries | On-feed CPM $45.84; CTR 0.32% (feed, all) |
| Audience | `ad1`, `ad2`, `ad3` | Get the right role to the landing page | **Landing-page CTR** and **CPC** | Dwell time; engagement rate; demo bookings (counted, too few to judge on early) | Cold single image: 0.30%–0.46% CTR, $13.60–$16.66 CPC (median about 0.35%, $15) |
| Follow-ups | `m1`–`m3`, `c1`–`c3`, `o1` | Turn engaged people into demo requests | **Demo bookings** and **cost per booking** once there are any; until then landing-page CTR | CTR; frequency (cap about 3–4 a week) | Warm single image: 0.40%–0.55% CTR, $8.45–$9.28 CPC |
| Video series | `v1`–`v4` (1:1 and 9:16) | Show the product working, build the deepest-intent retargeting pool | **50% completion rate** (of views) and **cost per 50% view** | View rate (views / impressions); 25% hold; CTR; 97%-view audiences for retargeting | Plex videos (mostly Audience Network): 25% hold 59.5%, 50% 36.2%, complete 19.7%. No on-feed baseline yet. |
| Whole program | all | Pipeline | **Demo bookings** attributed by `utm_content` and LinkedIn conversions | Spend against plan | 1 conversion in 90 days |

How to compute them:
- **CTR** is `clicks / impressions`, using landing-page clicks wherever possible.
- **Video rates** are `videoMidpointCompletions / videoViews`, and the same for each quartile.
- **Never average rates across rows.** Recompute them from the summed counts. LinkedIn returns CTR and CPC already
  aggregated.

## 2. What to test, in order

### Principles

- **Change one thing at a time:** concept, then format, then headline, then intro. The brief's full 3 × 3 copy grid
  is nine arms per asset, more than the budget can read.
- **Use LinkedIn's A/B test** (Campaign Manager, Test → A/B test) for concept and format tests. It splits the
  audience so arms don't overlap. For copy tests inside one campaign, set ad rotation to **rotate evenly**, so
  LinkedIn doesn't pick a winner after a few hundred impressions.
- **Hold targeting, bid, objective and dates the same across arms.** Bid on CPM or maximum delivery so CPC isn't
  biased by the bid type.
- **Treat Audience Network as a separate experiment,** if we run it at all.

### Sample sizes and budget per arm

These are calculated for a two-sided test at 95% confidence and 80% power. Cost assumes the baseline's on-feed CPM
of $45.84.

| Baseline CTR | Lift to detect | Impressions per arm | Cost per arm | Clicks per arm (about) |
| --- | --- | --- | --- | --- |
| 0.35% (cold) | +100% (2×) | 6,700 | ~$310 | 23 |
| 0.35% | +50% | 22,300 | ~$1,020 | 78 |
| 0.35% | +30% | 57,100 | ~$2,620 | 200 |
| 0.50% (warm) | +100% | 4,700 | ~$215 | 23 |
| 0.50% | +50% | 15,600 | ~$715 | 78 |

With budgets near today's $91 a day, we can only detect big differences: about 1.5× or more on cold audiences. So
the tests should be bold (different concepts and formats), not close copy tweaks. The baseline supports this: the
spread between the cold image ads, 0.30%–0.46%, was mostly not significant.

### Decision rules

- **Run each test at least 14 days,** to cover two full weeks of weekday patterns, and until every arm reaches the
  impression target above.
- **Call a winner** at p < 0.05 (two-proportion z-test on clicks over impressions, or completions over views for
  video) and with at least 20 clicks per arm.
- **If there's no winner by 28 days,** call it a tie and keep the cheaper or more on-brief arm.
- **No peeking to stop early,** with one guardrail: flag any arm with **0 clicks after 3,000 impressions** to Marcus
  to pause. At a 0.35% CTR that has well under a 0.1% chance of happening by luck.
- **Video tests** use 50% completion as the metric. Counts there are much larger, so they read in about a week.

### Test roadmap

| # | When | Test | Arms | Held constant | Metric | Notes |
| --- | --- | --- | --- | --- | --- | --- |
| T1 | Weeks 1–3 | **Ad 0 format:** single image `a0r-L` vs carousel `a0r-carousel` vs video `ad0r-S` (h1/i5 for image and video) | 3 | `h1`/`i1`, the Ad 0 audience | Cost per engaged member in target seniority; CTR | Also starts filling the retargeting pools. Video gets a view-rate readout on the feed for the first time. |
| T2 | Weeks 1–3, in parallel | **Ad 1 concept:** A (`a1-L`) vs B (`a1b-L`) | 2 | `h1`/`i1`, Ad 1 audience | Landing-page CTR | Each audience ad is its own campaign, so T2–T4 run side by side. |
| T3 | Weeks 1–3 | **Ad 2 format:** carousel `a2r-carousel` vs single image `a2-L` | 2 | `h1`/`i1`, Ad 2 audience | Landing-page CTR | |
| T4 | Weeks 1–3 | **Ad 3 visual:** A (`a3r-L`) vs B, number-led (`a3b-L`), plus video `ad3r-S` as a third arm if the budget allows | 2–3 | `h1`/`i1`, Ad 3 audience | Landing-page CTR | The number-led visual depends on the 278-vs-7-days claim being verified. Ops copy was the weakest in the baseline (0.28%), so this one matters. |
| T5 | Weeks 4–6 | **Headlines** `h1` vs `h2` vs `h3` on each audience ad's winning asset | 3 per ad | Winning asset, `i1` | CTR | Rotate evenly. Needs about 22k impressions per arm to read +50%, so run it only on the ad with the most delivery, or accept that only big differences will show. |
| T6 | Weeks 7–9 | **Intros** `i1` vs `i2` vs `i3` with the winning headline | 3 | Winning asset and headline | CTR, dwell time | |
| T7 | From week 3, once pools ≥ 300 members | **Follow-ups:** each one goes to its own pool from `targeting` in `copy.json`. Inside each, test 1:1 vs 1200×627 or carousel vs single image (one test per ad). | 2 | `h1`/`i1` | CTR, then bookings | Follow-up audiences are small. Read them together by angle (editorial `m*`, creative `c*`, ops `o1`) as well as by ad. |
| T8 | From week 3 | **Video series:** 1:1 (`vNr-S`) vs 9:16 (`vNr-V`) on one video first, then compare the four themes on 50% completion | 2, then 4 | Copy `h1`/`i1` | 50% completion, cost per 50% view, CTR | 9:16 only serves on mobile. Check the `impressionDeviceType` split before calling a winner. |
| T9 | Parked (needs Marcus's approval) | **"How our AI stands out" (`ai1`–`ai8`, from Viktor's A1–A8):** cold AI, product and tech leaders on the Tier 1 list. `ai5` goes to CTO/CISO (on-prem), `ai8` to AVOD/CTV monetisation leaders. First test: `ai1-L` (emotion curves), `ai6-L` (built for one industry), `ai2-L` (AI that listens), the creative agent's pick because their `h1`/`i1` carry no unverified claims or customer names; Viktor hasn't weighed in. `ai3` and `ai7` wait for their claims. | 2–3 | `h1`/`i1`, Tier 1 list | Landing-page CTR | Blocked until (1) Marcus approves on the approval page, (2) claims are cleared: 1688 vs 512–1024 dimensions, 2019 and 1M+ videos not on the site, 300M+ viewers / 20+ companies vs Ad 0's 500M / 60+ countries, Plex and Great American Pure Flix named, (3) the tier lists are live and the $127 vs $116/day budget choice is made. Viktor's tip: the Plex P series as retargeting (not built yet). Adding arms splits the Tier 1 budget further; fund it by replacing a losing arm from T1–T4, not on top. |

### Budget split (proposal for Marcus)

This depends on the total monthly budget, which Marcus sets. As shares of the AIBFE budget:

| Stage | Weeks 1–3 | Weeks 4+ |
| --- | --- | --- |
| Brand `ad0` | 30% | 15% |
| Audience `ad1`–`ad3` | 60% (20% each) | 45% |
| Follow-ups | 0% (pools filling) | 20% |
| Video series | 10% (one format test) | 20% |

**Worked example.** At $3,000 a month, weeks 1–3 come to roughly $2,100. That puts about $420 on each audience ad,
around $210 per arm. Enough to spot a 2× difference, not a 1.5× one. Reading +50% differences per audience ad
needs about $2,000 per ad over the three weeks.

## 3. How names and UTMs feed reporting

The scheme in `AGENTS.md` is the join key between LinkedIn, the website and these reports:

| Where | Value | Example | What we read it with |
| --- | --- | --- | --- |
| Campaign group | `AIBFE` | – | `campaignGroupName` filters AIBFE from legacy |
| Campaign name | `AIBFE \| <ad> \| <audience>` | `AIBFE \| v2 \| ad ops` | `campaignName` → stage and ad |
| Ad name | `<ad>/<asset>/<headline>-<intro>` | `v1/v1-S/h2-i1` | `creativeDscName` → ad, asset, copy variant |
| Carousel card | position 1–5 | `a2-c3` = card 3 | `creativeCardIndex` |
| `utm_content` | `<ad>-<asset>-<headline>-<intro>` | `v1-v1-S-h2-i1` | Website analytics: sessions and demo bookings per variant |
| `utm_campaign` | `ai-built-for-entertainment` | – | Separates AIBFE traffic from everything else |

**Parsing.** The ad name splits on `/` into ad, asset and copy. The copy part splits on `-` into headline and intro.
For `utm_content`, the first token is the ad, the last two are headline and intro, and everything in between is the
asset (asset IDs contain hyphens).

**Rollups this enables:**
- by **stage** (ad ID prefix: `ad0`; `ad1`–`ad3`; `m`/`c`/`o`; `v`);
- by **ad**, **format** (asset suffix: `-L`, `-S`, `-V`, `-cN`, and `b` for concept B) and **copy variant**;
- by **angle** (editorial, creative, operations) across follow-ups and video.

**Rules that keep it working:**
- **Exact IDs only.** No `Duplicate_` prefixes, no dates in names, no renaming after launch. Case matters in
  `utm_content`: `v1-S` and `v1-s` would split into two rows.
- **Name Spotlight and dynamic ads too.** The legacy Spotlight ad has an empty name in the API.
- **Duplicating an ad to another campaign keeps its ad name;** the campaign name tells the copies apart.
- **Check every live URL once** with a link checker, to confirm UTMs survive any redirect on vionlabs.com.

## 4. Weekly reporting routine

**Every Monday,** covering the previous Monday–Sunday plus launch to date:

1. **Pull from Supermetrics `LIA`** for account 507013260, filtered to `campaignGroupName` containing `AIBFE`:
   - by campaign and by creative (`creativeDscName`): impressions, clicks, landingPageClicks, spend, conversions,
     videoViews and the quartiles, average_dwell_time;
   - by `servingLocation` and `impressionDeviceType`;
   - `memberSeniority`, `memberJobFunction` and `memberIndustry`, launch to date;
   - website sessions and bookings by `utm_content`, once web analytics is connected.
2. **Check the guardrails:**
   - delivery against budget;
   - share of impressions at Manager+ and in target industries;
   - frequency;
   - any arm with 0 clicks after 3,000 impressions;
   - CTR on any ad down 30% or more from its own first two weeks (fatigue).
3. **Update tests:** progress against the sample size, and the significance of any arm that has reached it.
4. **Write `optimization/reports/YYYY-Www.md`** with:
   - a KPI table per stage, this week and to date, compared with the baseline;
   - test status;
   - decisions needed from Marcus (pauses, budget shifts, targeting);
   - creative requests.
5. **Message the creative agent** with any requests, by ad or asset ID, with the numbers and dates behind them.
6. **Summarise for Marcus:** three lines plus the decisions he needs to make.

**Monthly:** a funnel review (brand → audience → follow-up → booking), a check on retargeting pool sizes, and a
budget re-split proposal.
