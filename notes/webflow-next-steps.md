# Vionlabs Webflow: next steps (handoff)

Site: "Vionlabs Video AI", site_id 67978ee27d95b7ff0119d2ea
Staging: vionlabs.webflow.io (publish with customDomains: [] and publishToWebflowSubdomain: true)
Production: vionlabs.com / www.vionlabs.com, publish only with Marcus's explicit OK.

## 1. Remove the "noindex, nofollow" tag (urgent)
- Live pages that use the shared "Book a Demo Form [page end]" component
  (component id 35fd8f54-0f72-7361-818a-f2c88e47dd6b) all show
  robots "noindex,nofollow", plus "author: HubSpot, Inc.", a second viewport tag
  and msapplication-TileColor. Seen on: /, /editorial-lab, /curio.
- /why-vionlabs does not use that component and has none of these tags.
- The 8 Sep 2026 archive of the homepage has none of them either.
- Likely cause: an HTML embed inside the component that holds a full HubSpot page
  snippet, including its meta tags. Confirm this in Webflow, remove the meta tags,
  keep the form, then check that a staging page no longer shows robots noindex.

## 2. Homepage hero layout
- The hero lets the text column size itself to the longest headline line
  ("Your Viewers Are Scrolling"), which squeezes the Editorial Lab screenshot on wide screens.
- Fix: make the two hero columns equal (1fr 1fr, like /editorial-lab) and cap the
  headline width, so it wraps onto 3 lines and the image matches /editorial-lab.
- Homepage hero only. Staging first, send Marcus before/after screenshots.

## Context
- The Why Vionlabs page (/why-vionlabs) uses its own wv-* classes. It is live on
  production and not in the navigation.

## Status, 9 Nov
- Noindex: false alarm. Site and page custom code contain no robots tag. The tag Firecrawl
  reported comes from the HubSpot Meetings iframe (meetings.hubspot.com) inside the
  Book a Demo Form component, which only applies to HubSpot's own page. No change made.
- Homepage hero: fixed on staging. Combo classes `Frame 3458.home-hero-half`,
  `Frame 3320.home-hero-half` (flex 1 1 0, min-width 0; small breakpoint resets to auto)
  and `image 57.home-hero-img` (width 100%). These apply to the homepage only.
  Published to production 9 Nov 13:02 UTC with Marcus's OK; verified live.

## Vionlabs MCP page (/mcp), 9 Nov 2026

- Built on staging only: https://vionlabs.webflow.io/mcp (page id 6af1c886724fe278e134d3ae). Not published to production.
- Made by duplicating /why-vionlabs, so it has the site banner, Navbar Primary and Footer White.
- Sections are native Webflow elements with `mcp-*` classes, so the text can be edited in the Designer.
- Two HTML embeds:
  - one at the top of the page holds the responsive rules, hovers, FAQ +/× toggle and icons;
  - one inside `.mcp-chat` holds the animated assistant demo (vanilla JS, 21.6s loop, respects reduced motion).
- The early-access form is a native Webflow form named "MCP Early Access", so submissions land in Webflow Forms. The design's mailto form was dropped.
- Open: rights for the Spencer stills and romcom posters; who receives form submissions; a nav/footer link to /mcp; an OG image.
- 9 Nov follow-up, staging only:
  - Share thumbnail (1200×630, no film stills) set as the page's OG image (asset 6af1ce0f6908a4a6e96479ef).
  - FAQPage JSON-LD added to /mcp.
  - "Vionlabs MCP" link added to the Footer White component under Integrations & Access, so it shows in the footer on every page.
  - Watch out: the next production publish of anything will also take /mcp and the footer link live.

### MCP go-live check (9 Nov, staging)
Ready:
- Page renders correctly at 390, 768, 1024 and 1440px. Single h1.
- Canonical is https://www.vionlabs.com/mcp.
- Share image and title/description are set.
- FAQPage JSON-LD is now present (the first save hadn't stuck; re-saved and verified).
- All 18 images return 200.
- The docs link https://docs.app.vionlabs.com/mcp is live, and every FAQ answer matches it.
- The form "MCP Early Access" is registered and has Turnstile spam protection.
- Footer link to /mcp.
- The staging noindex comes from webflow.io only; the production page is indexable.

Blockers, Marcus to decide:
1. ~~Rights for the Spencer stills and the six romcom posters.~~ Marcus confirmed on 9 Nov that these can be shown publicly.
2. A notification email for form submissions (Site settings → Forms).
3. Check that the Webflow publish dialog lists only /mcp and the footer as changes.

Nice to have:
- Keep the "Coming soon" wording (Marcus confirmed).
- One test sign-up after launch.
