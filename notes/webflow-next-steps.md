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
