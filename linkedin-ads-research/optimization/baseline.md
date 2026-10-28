# LinkedIn Ads baseline

Pulled 2026-10-28 from LinkedIn Ads through Supermetrics (source `LIA`). The window is Supermetrics' `last_90_days`,
which runs up to and including 2026-10-27. "Last 30 days" uses `last_30_days` in the same way. Every number below
comes from those queries; anything calculated from them is marked *(calc)*. Currency is USD, the account currency.

None of the 15 new ads in `creatives/brief/copy.json` are live, so this is the baseline they will be measured against.

## Accounts

| Account | ID | Rows in the last 90 days |
| --- | --- | --- |
| Vionlabs Ad Account | 507013260 | 5 campaigns, 16 creatives |
| Marcus annonskonto | 506029020 | none |
| Albacross | 502548599 | none |

Everything below is from the Vionlabs Ad Account.

## Account totals, last 90 days

| Impressions | Clicks | CTR | CPC | CPM | Spend | Conversions | Leads | Video views | Video completions | Engagements |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 201,948 | 920 | 0.46% | $11.50 | $52.40 | $10,581.70 | 1 | 0 | 9,492 | 1,872 | 1,382 |

- **On the LinkedIn feed only** (all rows minus the Audience Network rows below) *(calc)*: 188,760 impressions, 597 clicks,
  **0.32% CTR**, $8,653.50 spend, **$14.49 CPC**, $45.84 CPM.
- **Engagement rate** came back as 0.6843, which matches 1,382 / 201,948 when read as a percentage (0.68%).
- **Reach:** `approximateUniqueImpressions` came back as 7,690 for the account. Against 201,948 impressions that
  would mean about 26 impressions per person, so check it in Campaign Manager before relying on it.

### By month

| Month | Impressions | Clicks | CTR | CPC | Spend | Video views |
| --- | --- | --- | --- | --- | --- | --- |
| 2026-07 (from 30 Jul) | 5,642 | 29 | 0.51% | $11.35 | $329.01 | 277 |
| 2026-08 | 79,450 | 432 | 0.54% | $12.44 | $5,372.60 | 3,578 |
| 2026-09 | 67,384 | 279 | 0.41% | $10.95 | $3,054.69 | 3,077 |
| 2026-10 (to 27 Oct) | 49,472 | 180 | 0.36% | $10.14 | $1,825.40 | 2,560 |

CTR has fallen every month since August, from 0.54% to 0.36%. The same creatives have run since March and May, so
creative fatigue is a likely cause, though this data doesn't prove it.

## What's running now (campaigns, all ACTIVE)

| Campaign group | Campaign | ID | Objective | Bid | Started | Daily budget |
| --- | --- | --- | --- | --- | --- | --- |
| [Cold][EU+US][v3] Editorial Lab & Creative Lab | [SI][Combined] Editorial Lab | 565806114 | Website visit | CPC | 2026-03-03 | $28 |
| [Cold][EU+US][v3] Editorial Lab & Creative Lab | [SI][Combined] Creative Lab | 565006334 | Website visit | CPC | 2026-03-03 | $23 |
| [Warm] Spotlight | [Spotlight] Warm | 565606004 | Website visit | CPC | 2026-03-03 | $20 |
| [Warm][EU+US] Warm Layer v1 | [SI][Warm] Editorial Lab | 447180054 | Website conversion | CPC | 2025-11-17 | $10 |
| [Cold][EU+US][v3] Editorial Lab & Creative Lab | Video creativves (Plex) | 701403204 | Website visit | CPM | 2026-05-07 | $10 |

The daily budgets add up to $91. None of the campaigns has an end date.

### By campaign, last 90 days

| Campaign | Impr. | Clicks | CTR | CPC | CPM | Spend | Conv. | Video views | Completions |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| [SI][Combined] Editorial Lab | 79,861 | 270 | 0.34% | $15.79 | $53.39 | $4,263.96 | 0 | – | – |
| [SI][Combined] Creative Lab | 66,284 | 245 | 0.37% | $14.81 | $54.74 | $3,628.14 | 0 | – | – |
| [Spotlight] Warm | 26,700 | 6 | 0.02% | $6.15 | $1.38 | $36.90 | 1 | – | – |
| [SI][Warm] Editorial Lab | 14,939 | 75 | 0.50% | $9.06 | $45.48 | $679.36 | 0 | – | – |
| Video creativves (Plex) | 14,164 | 324 | 2.29% | $6.09 | $139.32 | $1,973.34 | 0 | 9,492 | 1,872 |

### By campaign, last 30 days

| Campaign | Impr. | Clicks | CTR | CPC | Spend | Video views | Completions |
| --- | --- | --- | --- | --- | --- | --- | --- |
| [SI][Combined] Creative Lab | 18,919 | 66 | 0.35% | $11.06 | $730.00 | – | – |
| [SI][Combined] Editorial Lab | 18,627 | 63 | 0.34% | $12.94 | $815.00 | – | – |
| [Spotlight] Warm | 9,717 | 4 | 0.04% | $6.15 | $24.60 | – | – |
| [SI][Warm] Editorial Lab | 5,084 | 25 | 0.49% | $7.34 | $183.39 | – | – |
| Video creativves (Plex) | 3,988 | 46 | 1.15% | $6.61 | $303.96 | 2,850 | 488 |
| **Total** *(calc)* | 56,335 | 204 | | | $2,056.95 | | |

## The Plex video campaign runs almost entirely on Audience Network

| Placement | Impressions | Clicks | CTR *(calc)* | Spend |
| --- | --- | --- | --- | --- |
| Audience Network | 13,188 | 323 | 2.45% | $1,928.20 |
| On LinkedIn | 976 | 1 | 0.10% | $45.14 |

The other four campaigns served 100% on LinkedIn. So the account's best CTR, the video's 2.29%, comes from
Audience Network (third-party apps and sites), not the LinkedIn feed. On the feed the four Plex videos got 976
impressions and one click, which is too little to judge video on LinkedIn either way. The API won't split video
views or completions by placement, so the video numbers below are mostly Audience Network as well.

**Implication:** we have no feed-video baseline yet. Benchmark the new video series (`v1`–`v4`, `ad0` and `ad3`
video) against its own first weeks on the feed, and turn Audience Network off or report it separately.

## By creative, last 90 days

Single image and Spotlight ads, all on LinkedIn:

| Creative ID | Ad name in LinkedIn | Headline | Landing page | Campaign | Impr. | Clicks | CTR | CPC | Spend | Avg dwell (s) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1151693524 | Ad_1_4Nov2025 | Turn Your Library into a Discovery Engine | /editorial-lab | Combined Editorial | 43,135 | 131 | 0.30% | $16.20 | $2,122.45 | 20.1 |
| 1287882724 | Ad_3_3May2026 | Fix Discovery Now | /editorial-lab | Combined Creative | 24,935 | 102 | 0.41% | $14.89 | $1,518.63 | 19.9 |
| 1153581124 | Ad_6_1Mar2026 | AI-powered metadata for streaming platforms \| Vionlabs | / | Combined Editorial | 20,352 | 82 | 0.40% | $16.66 | $1,366.32 | 19.2 |
| 1288982434 | Ad_3_3May2026 | Turn Scrolls Into Streams | /editorial-lab | Combined Editorial | 16,374 | 57 | 0.35% | $13.60 | $775.19 | 20.0 |
| 1288182314 | Duplicate_Ad_4_3May2026 | Fix the Moment, Not the Ad | /operations-lab | Combined Creative | 10,022 | 28 | 0.28% | $15.50 | $434.13 | 22.4 |
| 916580114 | Ad_1_4Nov2025 | Turn Your Library into a Discovery Engine | /editorial-lab | Warm Editorial | 9,914 | 55 | 0.55% | $9.28 | $510.44 | 28.5 |
| 1288282904 | Ad_6_3May2026 | Make Every Title Click-Worthy | /creative-lab | Combined Creative | 9,362 | 43 | 0.46% | $14.79 | $635.81 | 19.8 |
| 1153392124 | Duplicate_Ad_1_21Nov2025 | Create visuals that increase engagement | /creative-lab | Combined Creative | 8,402 | 31 | 0.37% | $16.15 | $500.55 | 19.1 |
| 1289482644 | Ad_4_3May2026 | Fix the Moment, Not the Ad | /operations-lab | Combined Creative | 6,902 | 20 | 0.29% | $12.13 | $242.57 | 22.1 |
| 1152894894 | Ad_1_21Nov2025 | Create visuals that increase engagement | /creative-lab | Combined Creative | 6,661 | 21 | 0.32% | $14.12 | $296.46 | 19.5 |
| 916442464 | Ad_3_4Nov2025 | Keep viewers engaged with AI-curated lists | /editorial-lab | Warm Editorial | 5,025 | 20 | 0.40% | $8.45 | $168.92 | 27.5 |
| 1150894804 | (Spotlight, no name) | Viewers Can't Find the Right Title? | / | Spotlight Warm | 26,700 | 6 | 0.02% | $6.15 | $36.90 | – |

Video ads (Plex campaign; about 93% of impressions on Audience Network):

| Creative ID | Ad name / headline | Impr. | Clicks | CTR | Spend | Views | 25% | 50% | 75% | Complete | Avg dwell (s) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1291786884 | The Clear ROI… / The clear ROI of AI metadata at scale | 4,570 | 190 | 4.16% | $1,017.01 | 2,821 | 1,710 | 1,179 | 786 | 663 | 61.7 |
| 1292586694 | Advice for Leveraging… / Advice on picking an AI metadata partner | 4,023 | 40 | 0.99% | $367.67 | 2,818 | 1,745 | 1,065 | 738 | 559 | 79.6 |
| 1291986554 | Key Capabilities… / Why Plex chose machine-generated metadata | 3,041 | 52 | 1.71% | $313.99 | 2,149 | 1,305 | 726 | 521 | 427 | 83.0 |
| 1293285914 | Why Plex Selected… / 100,000 titles. Poor metadata. Here's the fix. | 2,530 | 42 | 1.66% | $274.68 | 1,704 | 889 | 468 | 323 | 223 | 94.3 |

Share of views reaching each point *(calc)*:

| Video | 25% | 50% | 75% | 100% |
| --- | --- | --- | --- | --- |
| The Clear ROI… | 60.6% | 41.8% | 27.9% | 23.5% |
| Advice for Leveraging… | 61.9% | 37.8% | 26.2% | 19.8% |
| Key Capabilities… | 60.7% | 33.8% | 24.2% | 19.9% |
| Why Plex Selected… | 52.2% | 27.5% | 19.0% | 13.1% |
| **All four** | 59.5% | 36.2% | 24.9% | 19.7% |

About 40% of viewers drop off before the 25% mark, the biggest single loss. The video with the most specific,
outcome-led headline (ROI) kept viewers longest and got the most clicks.

### What the creative data does and doesn't show

These are two-proportion z-tests on clicks over impressions *(calc)*. Treat them as directional: ad names, audiences
and run dates all differ between rows.

- **Warm beats cold for the same ad.** "Turn Your Library into a Discovery Engine" got 0.55% CTR in the warm campaign
  and 0.30% in the cold one (p < 0.001), and its CPC was $9.28 against $16.20.
- **Operations angle under-clicks.** "Fix the Moment, Not the Ad" (/operations-lab, 48 clicks on 16,924 impressions,
  0.28%) vs "Make Every Title Click-Worthy" (/creative-lab, 0.46%): p ≈ 0.02.
- **Nothing else** among the cold single-image ads (0.30%–0.46%) separates clearly at these volumes.

## Conversions and leads

- **One conversion rule exists:** "Booked a meeting" (type BOOK_APPOINTMENT, enabled).
- **It recorded one conversion in 90 days.** That was a view-through conversion, credited to the Spotlight campaign.
  There were no post-click conversions.
- **No Lead Gen Form leads** were recorded (`oneClickLeads` = 0).
- **No destination URL has UTM parameters.** The creatives link to vionlabs.com, /editorial-lab, /creative-lab,
  /operations-lab and /customer-stories with no UTMs.

So there is no working bottom-of-funnel number to optimise on yet. Clicks and landing-page clicks are the only
reliable outcome in the data.

## Who the ads reached, last 90 days

LinkedIn's demographic breakdowns are approximate and don't add up to the totals: summed rows come to more than the
account's impressions and spend. Read them as shares and rates, not totals. They include Audience Network delivery.

**Job function** (top 10 by impressions):

| Function | Impr. | Clicks | CTR |
| --- | --- | --- | --- |
| Product Management | 97,733 | 418 | 0.43% |
| Business Development | 34,209 | 162 | 0.47% |
| Media and Communication | 30,416 | 167 | 0.55% |
| Operations | 25,837 | 123 | 0.48% |
| Engineering | 24,297 | 152 | 0.63% |
| Arts and Design | 22,489 | 140 | 0.62% |
| Information Technology | 19,214 | 131 | 0.68% |
| Sales | 18,566 | 69 | 0.37% |
| Marketing | 17,742 | 53 | 0.30% |
| Customer Success and Support | 6,808 | 16 | 0.24% |

**Seniority:**

| Seniority | Impr. | Clicks | CTR |
| --- | --- | --- | --- |
| Director | 48,408 | 210 | 0.43% |
| Entry | 43,733 | 190 | 0.43% |
| Senior | 42,902 | 208 | 0.48% |
| Manager | 41,708 | 218 | 0.52% |
| Owner | 13,402 | 57 | 0.43% |
| CXO | 11,249 | 63 | 0.56% |
| VP | 8,573 | 56 | 0.65% |
| Partner | 6,820 | 21 | 0.31% |
| Training | 207 | 0 | 0% |

Entry level is the second-largest seniority by impressions. The new brief targets Manager and up (Senior and up
for Ad 1).

**Top job titles:**

| Job title | Impr. | Clicks | CTR |
| --- | --- | --- | --- |
| Product Manager | 39,909 | 148 | 0.37% |
| Product Owner | 20,104 | 62 | 0.31% |
| Senior Product Manager | 16,112 | 107 | 0.66% |
| Engineering Manager | 8,501 | 62 | 0.73% |
| Programming Manager | 6,917 | 21 | 0.30% |
| Head of Product | 5,898 | 17 | 0.29% |
| Head of Media | 4,606 | 8 | 0.17% |
| Broadcast Director | 2,654 | 27 | 1.02% |
| Vice President of Distribution | 2,546 | 25 | 0.98% |
| Head of Artificial Intelligence | 2,404 | 8 | 0.33% |
| Chief Technology Officer | 2,383 | 3 | 0.13% |

**Industry** (top 15 by impressions):

| Industry | Impr. | Clicks | CTR |
| --- | --- | --- | --- |
| Media and Telecommunications | 157,997 | 741 | 0.47% |
| Technology, Information and Internet | 111,494 | 507 | 0.45% |
| Entertainment Providers | 41,992 | 283 | 0.67% |
| IT Services and IT Consulting | 32,937 | 109 | 0.33% |
| Business Consulting and Services | 30,678 | 82 | 0.27% |
| Recreational Facilities | 19,442 | 163 | 0.84% |
| Advertising Services | 14,778 | 65 | 0.44% |
| Computers and Electronics Manufacturing | 13,177 | 43 | 0.33% |
| Holding Companies | 10,842 | 95 | 0.88% |
| Hospitality | 10,443 | 87 | 0.83% |
| Retail Office Supplies and Gifts | 10,437 | 89 | 0.85% |
| Performing Arts and Spectator Sports | 10,296 | 91 | 0.88% |
| Retail Apparel and Fashion | 10,214 | 79 | 0.77% |
| Apparel Manufacturing | 9,921 | 88 | 0.89% |
| Financial Services | 7,157 | 34 | 0.48% |

Several off-target industries (retail, apparel, hospitality, holding companies) show high CTRs. That pattern looks
like Audience Network traffic, but the breakdown can't be split by placement to confirm it.

**Companies** (top 20 by impressions): streamers and studios click more than telcos.

| Company | Impr. | Clicks | CTR |
| --- | --- | --- | --- |
| Vodafone | 10,408 | 31 | 0.30% |
| The Walt Disney Company | 9,878 | 82 | 0.83% |
| Netflix | 9,663 | 58 | 0.60% |
| NBCUniversal | 9,050 | 74 | 0.82% |
| Warner Bros. Discovery | 8,952 | 68 | 0.76% |
| Deutsche Telekom | 5,799 | 12 | 0.21% |
| Telia | 5,736 | 13 | 0.23% |
| OTE Group | 4,828 | 14 | 0.29% |
| Paramount | 4,482 | 42 | 0.94% |
| NOS SGPS | 4,194 | 15 | 0.36% |
| Groupe TF1 | 3,600 | 7 | 0.19% |
| France Télévisions | 3,415 | 11 | 0.32% |
| TV 2 Danmark | 3,174 | 11 | 0.35% |
| CANAL+ Group | 2,842 | 9 | 0.32% |
| VodafoneZiggo | 2,602 | 4 | 0.15% |
| Sky Italia | 2,562 | 6 | 0.23% |
| TIM | 2,384 | 4 | 0.17% |
| RTE | 2,112 | 8 | 0.38% |
| Prime Video & Amazon MGM Studios | 2,100 | 12 | 0.57% |
| O2 Czech Republic | 2,087 | 7 | 0.34% |

*(calc)*: Disney, Netflix, NBCUniversal, WBD and Paramount together had 0.77% CTR (324 / 42,025). Vodafone, Deutsche
Telekom, Telia, VodafoneZiggo and TIM together had 0.24% (64 / 26,929); p < 0.001.

**Country** (top 12 by impressions):

| Country | Impr. | Clicks | CTR | Spend |
| --- | --- | --- | --- | --- |
| United States | 62,247 | 497 | 0.80% | $5,252.50 |
| France | 20,464 | 58 | 0.28% | $941.79 |
| Sweden | 16,487 | 36 | 0.22% | $503.26 |
| Germany | 10,807 | 30 | 0.28% | $625.14 |
| Netherlands | 9,744 | 33 | 0.34% | $542.71 |
| Poland | 8,738 | 19 | 0.22% | $336.18 |
| Spain | 8,690 | 23 | 0.26% | $377.46 |
| Greece | 8,588 | 33 | 0.38% | $617.63 |
| Italy | 8,417 | 31 | 0.37% | $503.24 |
| Portugal | 7,879 | 36 | 0.46% | $619.69 |
| Denmark | 6,157 | 16 | 0.26% | $282.56 |
| Belgium | 5,235 | 17 | 0.32% | $244.09 |

## What's missing from the data

- **Conversions.** Only one has been recorded, and there are no lead forms. The "Book a demo" CTA can't be measured
  until the Insight Tag conversion fires on the demo booking.
- **UTMs.** No destination URL carries them, so web analytics can't attribute sessions to specific ads.
- **Video on the LinkedIn feed.** It had 976 impressions in 90 days.
- **LinkedIn Pages** (organic) isn't connected. Revenue attribution (CRM) wasn't queried.
