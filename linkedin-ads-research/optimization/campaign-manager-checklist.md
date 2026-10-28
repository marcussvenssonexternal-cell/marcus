# Campaign Manager checklist (before switching AIBFE on)

These steps can't be done through the API. Open campaign group **AIBFE | AI built for entertainment**:
https://www.linkedin.com/campaignmanager/accounts/507013260/campaigns?campaignGroupIds=%5B1243538664%5D

Everything is paused with a start date of 2 Nov. Do steps 1–4 in each campaign before switching anything on.

## 1. Audience (per campaign → Audience)

All 8 wave 1 campaigns already target, through the API:
- the **company audience the legacy cold campaigns used**, `Vionlabs – Cold v2 [11.11.25]` (60850047), so the
  same companies as before;
- the 17 countries and English.

In Campaign Manager, add on top of that:
- **Seniority,** all 8: Manager, Director, VP, CXO, Partner, Owner. Ad 1 also gets Senior. This drops the Entry
  level, which was a large share of the baseline.
- **Job function,** per campaign:

| Campaign (ID) | Job functions |
| --- | --- |
| ad0 image / carousel / video (905768494, 905856434, 905738384) | Product Management, Engineering, Operations, Media and Communication, Business Development |
| ad1 (905846754) | Engineering, Information Technology, Research, Product Management |
| ad2 carousel / image (905787604, 905768504) | Operations, Product Management, Media and Communication, Engineering |
| ad3 (905856444) | Operations, Engineering, Product Management |
| v1 (905748934) | Product Management, Operations, Media and Communication |

**No industry facet.** The company audience already decides which companies are in. Adding an industry filter
would drop listed companies that LinkedIn files under, for example, "Technology, Information and Internet" (the
second-largest industry in the baseline).

The **wave 2 retargeting** campaigns (905748944, 905891324, 905836864, 905728574) target
`[Warm] Website Visitors (all pages)`. Add the AIBFE engagement audiences when they exist (step 5).

**Check:** the forecast audience for each cold campaign should be well under the 3M of the company audience on its
own. Ad 1 will be the smallest.

## 2. Placement and expansion (per campaign)

- Untick **LinkedIn Audience Network**.
- Untick **Enable Audience Expansion**.

## 3. Carousels and videos (manual upload)

Files are on branch `claude/exciting-cerf-d0xnu7`, under `linkedin-ads-research/creatives/brief/`. Copy and URLs
come from `launch.csv` (match the `ad_name` column).

| Campaign (ID) | Ad name | Files | Copy |
| --- | --- | --- | --- |
| ad0 carousel (905856434) | `ad0/a0b-carousel/h1-i1` | `png/a0-c1…c4.png` + `png/a0-c5b.png` | ad0 i1; card headlines and URLs from `carousel-cards.csv` |
| ad0 video (905738384) | `ad0/ad0-S/h1-i1` | `video/ad0-S.mp4` | ad0 h1, i1 |
| ad2 carousel (905787604) | `ad2/a2-carousel/h1-i1` | `png/a2-c1…c5.png` | ad2 i1; card headlines and URLs from `carousel-cards.csv` |
| v1 (905748934) | `v1/v1-S/h1-i1`, `v1/v1b-S/h1-i1` | `video/v1-S.mp4`, `video/v1b-S.mp4` | v1 h1, i1 |
| v2-v4 (905728574) | `v2/v2-S/h1-i1`, `v3/v3-S/h1-i1`, `v4/v4-S/h1-i1` | `video/v2-S.mp4` etc. | each video's h1, i1 |

- **CTA:** Request demo.
- **Name every ad** exactly as in the table. Ads created through the API show only their IDs; you can rename those
  too, using `campaigns.md`.

## 4. Tests and rotation

- **ad0** image, carousel and video: set up a Campaign Manager **A/B test** (Test → Create test → Ad format), or
  leave them as three campaigns with identical targeting.
- **ad2** carousel vs image: the same.
- **ad1, ad3 and v1:** Campaign → Ads → **Rotate ads evenly**.

## 5. Audiences and tracking

- **Engagement audiences:** create them in Audiences → Create audience → Retargeting:
  - "AIBFE video viewers 50%", from the ad0, v1 and v2-v4 video campaigns;
  - "AIBFE ad engagers", from all wave 1 campaigns.
- **Insight Tag:** confirm it's on vionlabs.com, and that "Booked a meeting" fires on the demo booking confirmation.

## 6. Switch on: BLOCKED (rights check, 2026-10-28)

The board has flagged the film and TV imagery: frames and title art from Succession, Gladiator, Troy and others.
54 of the 61 campaign assets use it, which covers every single image and every video in AIBFE. No ad should
serve until Marcus confirms the rights are cleared, or the creative agent supplies replacement assets under new IDs.

**State at 14:15 UTC on 28 Oct:** the campaign group and most AIBFE campaigns are already **enabled** in Campaign
Manager. That includes wave 2, plus new manual campaigns: "ad0 video 2", "ad0 carousel 2", "ad2 carousel 2",
"v1 video 2" and "v2-v4 video retarget 2". The group's lifetime budget is now $10,950. They are held only by the
group start date, **2 Nov 2026**. Unless the rights are cleared before then, pause the group, or move its start
date, by 1 Nov.

**Marcus's decision (28 Oct):** keep the group enabled; he clears the rights before 2 Nov. Wave 2 runs from day one
at the $10,950 lifetime budget (about $120 a day), not the $91-a-day plan.

Once cleared:
1. Switch on the wave 1 campaigns. Keep wave 2 paused until week 4.
2. Pause the legacy campaign groups (897508034, 897508214, 800105584) and the seven empty Boost_Post groups.
