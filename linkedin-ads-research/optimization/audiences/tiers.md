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

**Tier 1 file, verified 29 Oct.** `aibfe-tier1-companies.csv` (also in Google Sheets: https://docs.google.com/spreadsheets/d/17fe9LiddEGPdGUmz0IhshskfyzeV90z_SqpTP-5A8BY)
has 34 rows: the 32 Tier 1 companies, plus Xfinity next to Comcast and two DPG Media pages (NL for Videoland/RTL
Nederland, and BE). Every LinkedIn page URL was checked by search on 29 Oct. Fixes from Viktor's sheet:
- NBCUniversal → `/company/nbcuniversal-inc-`
- Banijay → `/company/banijay`
- RTL Deutschland → `/company/rtl-deutschland`
- AMC Networks → `/company/amc-global-media` (renamed AMC Global Media)
- MFE → `/company/mfe-mediaforeurope`
- Versant → `/company/versant-media`
- M6 → `/company/groupem6`
- DPG Media → `/company/dpg-media-nl` and `/company/dpg-media-belgie`

Other enrichment: email domains, stock symbols where listed, LinkedIn industry, HQ city and two-letter country code.
The file follows LinkedIn's template: exact headers, at least one identifier per row, vanity URLs. A short list is
allowed; it needs 300 matched members to serve (LinkedIn recommends 1,000+ companies).

**Tier 2 file, verified 29 Oct.** `aibfe-tier2-companies.csv`, 22 companies (also in Google Sheets, "AIBFE Tier 2 –
LinkedIn company list upload"). Every page URL was checked. Fixes from Viktor's sheet:
- Amazon → `/company/primevideoamazonstudios`
- A+E → `/company/aeglobalmedia`
- Bell Media → `/company/bell-media-`
- ARD → `/company/ard-wir-sind-deins`

Enriched the same way as Tier 1.

**Status:**
- Tier 1 uploaded by Marcus as `AIBFE Tier 1 [29.10.26]` (audience 100292544, matching).
- Tier 2 campaign `AIBFE | ad1-ad2 | Tier 2 | image` created (906054044, paused, $20/day). Luxembourg, Saudi Arabia
  and Qatar couldn't be set through the API; add them in Campaign Manager.

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
  Amazon and YouTube each employ tens of thousands of people outside video. The job
  function and Manager+ filters are what keep spend on the right people. The dashboard's company and function
  breakdown will show whether that holds.
- **Existing customers.** Paramount and Sony Pictures (via Crunchyroll) are on Tier 1 deliberately, to expand.
- **Sports excluded.** The sheet has no sports companies. Foxtel's note says lead with entertainment, not Kayo.
