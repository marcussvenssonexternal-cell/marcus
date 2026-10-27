# An evening in the City: request-a-place page

Landing page for the Vionlabs × Embrace reception on Monday 16 November 2026, 18:30 – 22:00, at
Vinoteca di Sartoria, 21 Bloomberg Arcade, London. Guests request a place through the form, the
request goes to HubSpot, and the hosts confirm each place by email.

The page is in the Vionlabs look, taken from the vionlabs.com Webflow styles: Inter, black
backgrounds with the blue and amber glows, `#0068E0` pill buttons, the gradient-outlined section
label, and the form card and fields from the Book a Demo page. Embrace is named as co-host in the copy.

## Files

| File | What it is |
| --- | --- |
| `index.html` | The whole page: markup, styles, form logic and settings. No build step |
| `assets/` | The Vionlabs logo and `og-image.jpg` for link previews |
| `og/og-image.html` | Source of the 1200×627 link preview. `node og/render_og.cjs` re-renders `assets/og-image.jpg` |

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
| `lastFewPlaces` | `false` | Shows a "Last few places" badge above the headline, to match the reminder post |

A successful request also pushes `event_place_requested` to `dataLayer`, if Google Tag Manager is on the page.

## Publishing

The folder is a static site: upload it as is. Then:

- Make sure the address on the social posts (`embrace.fr/london` in the current drafts) serves or redirects to this page.
- Change `og:image` in `index.html` to the image's absolute URL, so LinkedIn and other link previews show it.
