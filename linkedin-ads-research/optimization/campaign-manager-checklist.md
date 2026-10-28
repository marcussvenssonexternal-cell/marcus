# Campaign Manager checklist (before switching AIBFE on)

These steps can't be done through the API. Open campaign group **AIBFE | AI built for entertainment**:
https://www.linkedin.com/campaignmanager/accounts/507013260/campaigns?campaignGroupIds=%5B1243538664%5D

Everything is paused with a start date of 2 Nov. Do steps 1–4 in each campaign before switching anything on.

## 1. Audience (per campaign → Audience → "Narrow audience further")

Add these three facets in each cold campaign. The countries (17) and English are already set; Greece is
unsupported in the API, so add it by hand if you want it.

- **Industries,** all wave 1 campaigns: Entertainment Providers; Broadcast Media Production and Distribution;
  Movies, Videos, and Sound; Telecommunications.
- **Seniority,** all wave 1 campaigns: Manager, Director, VP, CXO, Partner, Owner. Ad 1 also gets Senior.
- **Job function,** per campaign:

| Campaign (ID) | Job functions |
| --- | --- |
| ad0 image / carousel / video (905768494, 905856434, 905738384) | Product Management, Engineering, Operations, Media and Communication, Business Development |
| ad1 (905846754) | Engineering, Information Technology, Research, Product Management |
| ad2 carousel / image (905787604, 905768504) | Operations, Product Management, Media and Communication, Engineering |
| ad3 (905856444) | Operations, Engineering, Product Management |
| v1 (905748934) | Product Management, Operations, Media and Communication |

The **wave 2 retargeting** campaigns (905748944, 905891324, 905836864, 905728574) already target
`[Warm] Website Visitors (all pages)`. When the AIBFE engagement audiences exist (step 5), add them as well.

**Check:** the forecast panel should show an audience well under 1M for each cold campaign. If it shows tens of
millions, a facet is missing.

## 2. Placement and expansion (per campaign)

- Untick **LinkedIn Audience Network**.
- Untick **Enable Audience Expansion**.

## 3. Carousels and videos (manual upload)

Files are on branch `claude/exciting-cerf-d0xnu7`, under `linkedin-ads-research/creatives/brief/`. Copy and URLs
come from `launch.csv` (match the `ad_name` column).

| Campaign (ID) | Ad name | Files | Copy |
| --- | --- | --- | --- |
| ad0 carousel (905856434) | `ad0/a0-carousel/h1-i1` | `png/a0-c1…c5.png` | ad0 h1, i1 |
| ad0 video (905738384) | `ad0/ad0-S/h1-i1` | `video/ad0-S.mp4` | ad0 h1, i1 |
| ad2 carousel (905787604) | `ad2/a2-carousel/h1-i1` | `png/a2-c1…c5.png` | ad2 h1, i1 |
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

## 6. Switch on (in this order)

1. Clear the claims first. Ad 3 (905856444) can't run until the 278-vs-7-days claim is cleared; its copy depends on
   it. If you launch without it, leave that campaign paused and give its $15 to ad1 and ad2 (for example ad1 $24, ad2 image $17).
2. Switch on the campaign group, then the wave 1 campaigns: ad0 ×3, ad1, ad2 ×2, ad3 and v1, at $91 a day.
3. Then pause the legacy campaign groups: 897508034, 897508214, 800105584, plus the 7 empty Boost_Post groups.
4. Leave the wave 2 campaigns paused until week 4.
