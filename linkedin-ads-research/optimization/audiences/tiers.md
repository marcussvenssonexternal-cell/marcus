# Tier 1 / Tier 2 company targeting

Source: Viktor's "Vionlabs GTM – Big-deal focus accounts" sheet, refined 29 Oct 2026 from the 295-account net list
(https://docs.google.com/spreadsheets/d/1lOaxMtlWE8bt1bFtQ3r2RL_-7IcvQ_MK5Rruv-1r3QU, tab "Focus accounts"). His rule:
**70% of the budget goes to Tier 1.**

| Market | Tier 1 | Tier 2 | Total |
| --- | --- | --- | --- |
| NA | 14 | 10 | 24 |
| EMEA | 18 | 12 | 30 |
| APAC | 8 | 7 | 15 |
| LATAM | 5 | 0 | 5 |
| **Total** | **45** | **29** | **74** |

## Upload files

`aibfe-tier1-companies.csv` and `aibfe-tier2-companies.csv` are in LinkedIn's company-list template. Each row has
the company name, website, email domain and LinkedIn page URL from the sheet. Upload each one in Campaign Manager:
Plan → Audiences → Create audience → Upload a list → Company list. Name them:
- `AIBFE Tier 1 [29.10.26]`
- `AIBFE Tier 2 [29.10.26]`

LinkedIn takes up to 48 hours to match a list, and needs at least 300 matched members to serve.

**Before uploading,** check the 22 rows the sheet marks "Verify". The LinkedIn page URL may be wrong or point to a
parent company:
- Tier 1: Paramount Skydance, Tubi, Versant, ITV, M6, Telefónica, JioStar, Zee, U-NEXT, Hulu Japan, Nine, Globo,
  Record.
- Tier 2: Amazon MGM Studios, Starz, Sky Italia, SonyLIV, TVer, ABEMA, Wavve, Astro, TVB.

## Proposed campaign changes (need Marcus's approval)

1. **Swap the company list.** In every cold AIBFE campaign, replace `Vionlabs – Cold v2 [11.11.25]` (about 3M
   members, Nov 2025) with the Tier 1 list. Job function and seniority stay as set in Campaign Manager.
2. **Add Tier 2 campaigns** that carry 30% of the cold budget: one brand campaign (`ad0` image) and one audience
   campaign (`ad1`–`ad3` image ads together), both on the Tier 2 list. Duplicating every campaign per tier would
   mean many campaigns at LinkedIn's $10-a-day minimum, too thin to learn from.
3. **Split the budget** so the Tier 1 campaigns carry 70% of the cold daily budget and the Tier 2 campaigns 30%,
   within the current total.
4. **Retargeting** (m, c, o1, v2–v4) stays on website visitors and ad engagers. These people already came from the
   lists, so they sit outside the 70/30. Say if Viktor wants them restricted to the lists too.
5. **Widen the countries to match the list.** Today's 17 (US plus Western Europe) miss most of APAC and LATAM.
   - Add: Canada, Mexico, Brazil, Argentina, India, Japan, South Korea, Hong Kong, Australia, Malaysia, UAE, Saudi
     Arabia, Qatar and Luxembourg.
   - Keep the existing 17.
   - The company list does the real filtering, so a wider country list doesn't widen the audience beyond these
     companies.
6. **Language.** Campaigns target English-interface members only, which drops people whose LinkedIn runs in
   Japanese, Korean or Portuguese. Either remove the language filter for APAC and LATAM, or accept the loss: the ads
   are in English.

## Watch-outs

- **Giant companies.** Samsung Electronics, LG Electronics, Comcast, Telefónica, Deutsche Telekom, Orange, Apple,
  Amazon, YouTube, Mercado Libre and América Móvil each employ tens of thousands of people outside video. The job
  function and Manager+ filters are what keep spend on the right people. The dashboard's company and function
  breakdown will show whether that holds.
- **Existing customers.** Paramount and Sony Pictures (via Crunchyroll) are on Tier 1 deliberately, to expand.
- **Sports excluded.** The sheet has no sports companies. Foxtel's note says lead with entertainment, not Kayo.
