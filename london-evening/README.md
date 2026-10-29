# An evening in the City: request-a-place page

Landing page for the Embrace × Codemill × Vionlabs reception on Monday 16 November 2026, 17:30 – 20:00, at
Vinoteca di Sartoria, 21 Bloomberg Arcade, London. Guests request a place through the form, the
request goes to HubSpot, and the hosts confirm each place by email.

The page is built on the "K2 · Ticket (navy)" social post: navy `#111B2C` with a pink accent, Space Grotesk
with JetBrains Mono labels, and the paper ticket with the St Paul's drawing in its navy stub. The
form is the guest's half of the ticket: their name and company appear on it as they type, and it
gets a "Requested" stamp once the request is sent.

## Live version in Webflow

The page is also built natively in the Vionlabs Webflow site as the page "An evening in the City" at
`/london`, using classes prefixed `lon-` and a native Webflow form named "London evening request".
It opens with the site's standard "Navbar Primary" component; the page's head code only gives it the
page's navy background, so the component is unchanged on every other page.
Fonts, animations and the ticket script (live guest name, "Requested" stamp, tilt) are in that page's
custom code. Its form submissions land in Webflow under Forms. The page script
"LondonEveningHubSpotSubmit" also sends each one to the HubSpot form "London evening request – 16 Nov
2026", whose follow-up email thanks the guest. The form carries `data-hs-do-not-collect="true"` so
HubSpot's collected forms don't record it a second time. This folder is the standalone version of the
same design.

## Files

| File | What it is |
| --- | --- |
| `index.html` | The whole page: markup, styles, form logic and settings. No build step |
| `assets/` | Both logos as SVG, the St Paul's drawing and `og-image.jpg` for link previews |
| `og/og-image.html` | Source of the 1200×627 link preview. `node og/render_og.cjs` re-renders `assets/og-image.jpg` |

All three logos are white SVGs, 112 units high so they line up at one height:

- Vionlabs: the official wordmark from the brand files, without the tagline.
- Embrace: a vector redraw of the PNG supplied with the social post, since no vector file was at
  hand. Swap in Embrace's own SVG when they send it, here and in Webflow (`london-embrace-logo-white.svg`).
- Codemill: Codemill's own white logo, as they supplied it, set in the same frame. Its strokes are
  lighter than the Vionlabs wordmark's, so its letters sit a little taller (65 of 112 units, against
  61 for Vionlabs and 68.5 for Embrace) to look the same size in the lockup.

To preview, open `index.html` in a browser. Until HubSpot is connected the form runs in preview
mode: it validates and shows the thank-you screen, but sends nothing, and says so above the fields.

## Connect the form to HubSpot

The page posts straight to HubSpot's form submissions API, so it works wherever the page is hosted.

1. In HubSpot, create a form (Marketing → Forms) for this event with these fields. They are all
   default contact properties, so nothing custom is needed:

   | Page field | HubSpot property |
   | --- | --- |
   | First name | `firstname` |
   | Last name | `lastname` |
   | Work email | `email` |
   | Company | `company` |
   | Job title | `jobtitle` |
   | Anything the hosts should know? (optional) | `message` |

   HubSpot rejects a submission that contains a field the form doesn't have, so keep the two lists the same.
2. On that form, turn on email notifications to whoever reviews the requests.
3. Copy the account ID (Settings → Account details) and the form ID (the GUID in the form's URL or
   embed code) into `EVENT_PAGE.hubspot` near the end of `index.html`.
4. Send one test request and check it arrives as a submission on the form.

Each request is a submission on that form, so a list or workflow on "submitted this form" gives
the hosts their review queue. Confirmations are sent by the hosts; the page only promises that they
will follow by email.

The page also sends the consent sentence the guest ticked (`legalConsentOptions`) and the HubSpot
cookie (`hubspotutk`) when the site already loads HubSpot tracking, so the request joins the
visitor's existing contact record.

## Settings

All in `window.EVENT_PAGE` in `index.html`:

| Setting | Default | What it does |
| --- | --- | --- |
| `hubspot.portalId` | empty | HubSpot account ID. Empty = preview mode |
| `hubspot.formId` | empty | ID of the HubSpot form that collects the requests. Empty = preview mode |
| `hubspot.loadTrackingCode` | `false` | Adds the HubSpot tracking code. Leave off where the site loads it already (for example through Google Tag Manager) |
| `hubspot.trackingHost` | `js.hs-scripts.com` | Use `js-eu1.hs-scripts.com` for an EU data centre account |
| `privacyUrl` | `https://www.vionlabs.com/legal` | Where both "privacy notice" links go. Point it at the notice that covers both hosts |
| `lastFewPlaces` | `false` | Shows a "Last few places" badge on the ticket, for the reminder post |

A successful request also pushes `event_place_requested` to `dataLayer`, if Google Tag Manager is on the page.

## Publishing

The folder is a static site: upload it as is. Then:

- The ticket post points to `vionlabs.com/london`, so publish the page there (or redirect that address to it).
- Change `og:image` in `index.html` to the image's absolute URL, so LinkedIn and other link previews show it.
