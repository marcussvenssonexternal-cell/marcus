# AIBFE campaign build (drafts)

This is the new account structure for the AI built for entertainment ads. It replaces the current campaigns and keeps
the same total budget: **$91 a day**, which is what the five active legacy campaigns' daily budgets add up to (see
`baseline.md`). Marcus approved building it from scratch and pausing the legacy campaigns (2026-10-28).

**Status: not created yet.** Supermetrics has campaign write access turned off for the Vionlabs Ad Account
(507013260). Marcus turns it on at https://hub.supermetrics.com/write-settings?platform=LIA&team_id=1311511 . The
build runs from `campaign-drafts.json` once that's done. Everything is created **paused**; nothing spends until
Marcus switches it on.

## Structure

There is one campaign group, **`AIBFE | AI built for entertainment`**:
- Lifetime budget: $8,281 (91 days × $91)
- Dates: 2026-11-02 to 2027-01-31

Groups don't carry daily budgets, so the lifetime budget is the cap that holds the total at today's run rate. Each
campaign gets its own daily budget. LinkedIn's minimum is $10 a day per campaign.

LinkedIn fixes the ad format per campaign, so each format test is its own campaign with identical targeting. Run
those as a LinkedIn **A/B test** (Campaign Manager → Test) so the arms don't share an audience.

### Wave 1: live at launch ($91 a day)

| Campaign | Format | Ads (`<ad>/<asset>/<h>-<i>`) | Daily | Objective | Test |
| --- | --- | --- | --- | --- | --- |
| `AIBFE \| ad0 \| decision makers \| image` | Single image | `ad0/a0-L/h1-i1` | $10 | Website visits | T1 format arm |
| `AIBFE \| ad0 \| decision makers \| carousel` | Carousel | `ad0/a0-carousel/h1-i1` (cards `a0-c1`…`c5`) | $10 | Website visits | T1 format arm |
| `AIBFE \| ad0 \| decision makers \| video` | Video | `ad0/ad0-S/h1-i1` | $10 | Website visits | T1 format arm |
| `AIBFE \| ad1 \| AI-ML and rec product` | Single image | `ad1/a1-L/h1-i1`, `ad1/a1b-L/h1-i1` | $16 | Website visits | T2 concept A vs B (rotate evenly) |
| `AIBFE \| ad2 \| content ops and editorial \| carousel` | Carousel | `ad2/a2-carousel/h1-i1` (cards `a2-c1`…`c5`) | $10 | Website visits | T3 format arm |
| `AIBFE \| ad2 \| content ops and editorial \| image` | Single image | `ad2/a2-L/h1-i1` | $10 | Website visits | T3 format arm |
| `AIBFE \| ad3 \| media ops and ad ops` | Single image | `ad3/a3-L/h1-i1`; `ad3/a3b-L/h1-i1` is added once its 278-vs-7-days claim is cleared | $15 | Website visits | T4 visual A vs B (rotate evenly). Until then a3-L runs alone. |
| `AIBFE \| v1 \| editorial search` | Video | `v1/v1-S/h1-i1`, `v1/v1b-S/h1-i1` | $10 | Video views | Hook test: v1 (first text at 3.6 s) vs v1b (opens on the failed search). 50% completion. If v1b wins, the creative agent makes v2b and v3b. 1:1 vs 9:16 comes next. |
| **Total** | | | **$91** | | |

### Wave 2: drafts, switched on from week 4

These run once the AIBFE engagement audiences pass 300 members. The $91 is then re-split (plan: brand 15%, audience
45%, follow-ups 20%, video 20%), so the total stays the same.

| Campaign | Ads | Draft daily | Audience |
| --- | --- | --- | --- |
| `AIBFE \| m1-m3 \| editorial retarget` | `m1/m1-L/h1-i1`, `m2/m2-L/h1-i1`, `m3/m3-L/h1-i1` | $10 | Engaged with ad0/ad1/ad2 + website visitors |
| `AIBFE \| c1-c3 \| creative retarget` | `c1/c1-L/h1-i1`, `c2/c2-L/h1-i1`, `c3/c3-L/h1-i1` | $10 | Engaged with ad2 + website visitors |
| `AIBFE \| o1 \| ops retarget` | `o1/o1-L/h1-i1` | $10 | Engaged with ad0/ad3 + website visitors |
| `AIBFE \| v2-v4 \| video retarget` | `v2`, `v3`, `v4` (`-S`) | $10 | Per `copy.json` retargeting lines |

Until the new engagement audiences exist, the follow-up drafts point at the account's existing retargeting audiences:
- `[Warm] Website Visitors (all pages)` (60827042, about 1,100 members);
- `[Warm] Engaged with Ads` (60835018, listed at 0 members).

## Targeting (all wave 1 campaigns)

- **Locations:** US, GB, IE, SE, NO, DK, FI, DE, AT, CH, FR, BE, NL, ES, PT, IT, PL, GR. This matches the legacy
  "EU+US" footprint in the baseline. Marcus to confirm.
- **Language:** English.
- **Industries:** Entertainment Providers (`urn:li:industry:28`), Broadcast Media Production and Distribution (36),
  Movies, Videos, and Sound (35), Telecommunications (8).
- **Seniority:** Manager (`urn:li:seniority:5`), Director (6), VP (7), CXO (8), Partner (9), Owner (10). Ad 1 adds
  Senior (4). Entry and Training are left out; Entry took a large share of the baseline.
- **Job functions,** per `copy.json`:

  | Campaign | Functions |
  | --- | --- |
  | ad0 | Product Management (19), Engineering (8), Operations (18), Media and Communication (16), Business Development (4) |
  | ad1 | Engineering, Information Technology (13), Research (24), Product Management |
  | ad2 | Operations, Product Management, Media and Communication, Engineering |
  | ad3 | Operations, Engineering, Product Management |
  | v1 | Product Management, Operations, Media and Communication |

- **Audience Network:** off. LinkedIn's API doesn't expose this setting, so untick it in Campaign Manager for each
  campaign.
- **Audience expansion:** off.

Facets combine with AND and values within a facet with OR. The job title lists in `copy.json` are left out on
purpose: titles AND functions AND industry would be too narrow for $10–16 a day. Titles can be a later test.

## Ads

- **Copy:** every ad uses `h1` and `i1` from `creatives/brief/copy.json`. Headline and intro tests come later
  (T5, T6).
- **CTA:** **Request demo**. That's LinkedIn's closest button to the brief's "Book a demo".
- **Images:** pinned to creative-branch commit `2954e0d`, so a later re-render doesn't change a running ad.
- **URLs:** `<landing page>?utm_source=linkedin&utm_medium=paid_social&utm_campaign=ai-built-for-entertainment&utm_content=<ad>-<asset>-h1-i1`.

| Ads | Landing page |
| --- | --- |
| ad0 | /our-ai |
| ad1 | /embeddings-api |
| ad2, m1–m3, v1 | /editorial-lab |
| ad3, o1, v2 | /operations-lab |
| c1–c3, v3, v4 | /creative-lab |

These pages come from the `destination` field in `copy.json`. Every ad's full URL is in `creatives/brief/launch.csv`
(creative commit `2954e0d`). Check before launch that `/our-ai` and `/embeddings-api` load. This container can't
reach vionlabs.com, so I couldn't check them myself.

**Telco variant:** `ad0` now also has `i4`, written for pay-TV and telco operators. It's ready for a telco-only ad0
cell, for example a later test splitting Telecommunications out of the ad0 audience.

The exact payloads (names, copy, URLs, images) are in `campaign-drafts.json`.

## What the API can't do (manual in Campaign Manager)

The Supermetrics LinkedIn connector creates **single-image ads only**. These steps are manual:
1. Add the carousels (`a0-c1…c5`, `a2-c1…c5`) and videos (`ad0-S`, `v1-S`, `v1b-S`) to their campaigns. The files
   are in `creatives/brief/png/` and `creatives/brief/video/`. Use the names and UTMs above.
2. Set up the A/B tests (T1 ad0 format, T3 ad2 format). Set ad rotation to **rotate evenly** in the ad1 and ad3
   campaigns.
3. Untick Audience Network in every campaign.
4. Create the engagement audiences for wave 2: video viewers 50%+ and ad engagers for each AIBFE campaign.
5. Point the "Booked a meeting" conversion at the demo booking confirmation. When it fires, switch the follow-ups to
   the Website conversion objective.

## Legacy campaigns

These get paused when AIBFE goes live, not before, so the account doesn't go dark while the drafts are finished:

| Campaign group | Group ID | Campaigns | Daily |
| --- | --- | --- | --- |
| [Cold][EU+US][v3] Editorial Lab & Creative Lab | 897508034 | [SI][Combined] Editorial Lab (565806114), [SI][Combined] Creative Lab (565006334), Video creativves (Plex) (701403204) | $28 + $23 + $10 |
| [Warm] Spotlight | 897508214 | [Spotlight] Warm (565606004) | $20 |
| [Warm][EU+US] Warm Layer v1 | 800105584 | [SI][Warm] Editorial Lab (447180054) | $10 |

Seven more `Boost_Post_*` campaign groups are also enabled (IDs 1042200084, 1003225674, 1002535004, 899408464,
891301804, 882000604, 881801024). None of them spent anything in the last 90 days. Pause them at the same time to
tidy up.

## Before switching on (blockers)

- "Check before launch" claims cleared: `ad0` (3), `ad3` (2, including the number-led `a3b`), and one each in `ad1`,
  `ad2`, `v1`. Most are title-art rights.
- Demo booking conversion firing. The creative agent found no Google tag in the Webflow site settings, so check
  that the LinkedIn Insight Tag is on the site at all.
- Manual steps 1–3 above done.
