# Tier 1 / Tier 2 company targeting

Source: Viktor's "Vionlabs GTM – Big-deal focus accounts" sheet, refined 29 Oct 2026 from the 295-account net list
(https://docs.google.com/spreadsheets/d/1lOaxMtlWE8bt1bFtQ3r2RL_-7IcvQ_MK5Rruv-1r3QU, tab "Focus accounts"). His rule:
**70% of the budget goes to Tier 1.**

**29 Oct: Marcus dropped APAC and LATAM.** The lists below are North America and EMEA only.

| Market | Tier 1 | Tier 2 | Total |
| --- | --- | --- | --- |
| NA | 14 | 10 | 24 |
| EMEA | 18 | 12 | 30 |
| **Total** | **32** | **22** | **54** |

## Upload files

`aibfe-tier1-companies.csv` and `aibfe-tier2-companies.csv` are in LinkedIn's company-list template. Each row has
the company name, website, email domain and LinkedIn page URL from the sheet. Upload each one in Campaign Manager:
Plan → Audiences → Create audience → Upload a list → Company list. Name them:
- `AIBFE Tier 1 [29.10.26]`
- `AIBFE Tier 2 [29.10.26]`

LinkedIn takes up to 48 hours to match a list, and needs at least 300 matched members to serve.

**Before uploading,** check the 9 rows the sheet marks "Verify". The LinkedIn page URL may be wrong or point to a
parent company:
- Tier 1: Paramount Skydance, Tubi, Versant, ITV, M6, Telefónica.
- Tier 2: Amazon MGM Studios, Starz, Sky Italia.

## Agreed changes (Marcus, 29 Oct)

1. **Swap the company list.** Every cold AIBFE campaign switches from `Vionlabs – Cold v2 [11.11.25]` to the Tier 1
   list once it has matched.
2. **One Tier 2 campaign,** `AIBFE | ad1-ad2 | Tier 2 | image`, with `ad1/a1-L/h1-i1` and `ad2/a2-L/h1-i1` (assets
   not affected by the rights rework), at $20 a day. It was created paused through the API on 29 Oct, pending
   Supermetrics approval. The Tier 2 list and its job functions get added in Campaign Manager:
   - functions: Engineering, Information Technology, Research, Product Management, Operations, Media and
     Communication;
   - seniority: Manager+.
3. **70/30 budget.** Cold AIBFE image campaigns run $67 a day today (ad0 $17, ad1 $20, ad2 $14, ad3 $16). With
   Tier 2 at $20, the split is $67 / $20 = 77/23. To land on 70/30 within the same total ($87), Tier 1 goes to $61
   (ad0 $15, ad1 $18, ad2 $14, ad3 $14) and Tier 2 to $26. This is applied when Tier 2 goes live.
4. **Retargeting:** no change (Marcus: "no need to do").
5. **Countries:** add Canada, Luxembourg, UAE, Saudi Arabia and Qatar (Bell Media, RTL Group, MBC, OSN, beIN) to
   the existing 17. Applied together with the list swap.
6. **Language:** English stays. All remaining markets are NA and EMEA.

## Watch-outs

- **Giant companies.** Samsung Electronics, LG Electronics, Comcast, Telefónica, Deutsche Telekom, Orange, Apple,
  Amazon, YouTube, Mercado Libre and América Móvil each employ tens of thousands of people outside video. The job
  function and Manager+ filters are what keep spend on the right people. The dashboard's company and function
  breakdown will show whether that holds.
- **Existing customers.** Paramount and Sony Pictures (via Crunchyroll) are on Tier 1 deliberately, to expand.
- **Sports excluded.** The sheet has no sports companies. Foxtel's note says lead with entertainment, not Kayo.
