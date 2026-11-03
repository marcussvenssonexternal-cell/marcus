# Publish hold

Since 3 Nov 2026: no site-wide production publish of vionlabs.com.

The new navbar (a "New" column for the Agentic Layer and Curio) is on staging,
and Marcus wants to check it there before anything goes live. Every page
carries the navbar, so any site-wide publish would ship it.

- Allowed: work on staging, and item-level CMS publishes that do not publish
  the site.
- Not allowed: `publish_site` to the custom domains, even for approved tasks.
  Stage the change and say in the readout that it waits for the hold.
- If something urgent must go live, ask Marcus first and tell him it would
  ship the navbar too.

Remove this file only when Marcus or Atlas says the hold is lifted.
