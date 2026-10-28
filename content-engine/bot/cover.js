#!/usr/bin/env node
// Render the images for the Deep Dives packs: blog post covers, news grid thumbnails, in-article figures
// and LinkedIn images.
//
//   node content-engine/bot/cover.js            # every piece with a "cover", "figures", "social" or "thumb" in deep-dives/*.json
//   node content-engine/bot/cover.js ad-breaks  # one topic
//
// Covers are drawn by cover.html at 1920x1080, figures by figure.html at 1600x900, the LinkedIn feed
// image that shares a long read by social.html at 1080x1350 and the thumbnail for the vionlabs.com/news
// grid (cards are about 1.27:1) by thumb.html at 1600x1260, then saved to deep-dives/<image>. The
// publish step uploads them next to the page, and the Google Doc loads them from GitHub, so push before
// exporting. Needs Playwright (installed globally in the cloud sessions).
const fs = require("fs");
const path = require("path");
const crypto = require("crypto");
const { execSync } = require("child_process");

// Every image carries the official Vionlabs logo, loaded from assets/ and never redrawn ("The logo" in
// config/brand.md). These are the files as taken from the website; a render stops if one has changed or
// a template doesn't show one.
const LOGOS = {
  "vionlabs-logo-white.svg": "d917a594a882f7928e581e1218b37477",
  "vionlabs-logo-black.png": "3b518caf27b7da8b3fa05a57607e4a66",
  "vionlabs-eye-icon.png": "a21b1ae9a5ca00ddfe85a3a98a48c544",
};

function playwright() {
  try { return require("playwright"); } catch (e) {
    return require(path.join(execSync("npm root -g").toString().trim(), "playwright"));
  }
}

(async () => {
  const dir = path.join(__dirname, "..", "deep-dives");
  const only = process.argv[2];
  const jobs = [];
  for (const f of fs.readdirSync(dir).filter((f) => f.endsWith(".json"))) {
    const t = JSON.parse(fs.readFileSync(path.join(dir, f), "utf8"));
    if (only && t.id !== only) continue;
    for (const p of (t.pack || {}).pieces || []) {
      if (p.cover && p.cover.image) {
        jobs.push({ image: p.cover.image, html: "cover.html", w: 1920, h: 1080, key: "COVER",
          spec: { kicker: p.cover.kicker || t.title, by: p.cover.by || "", headline: p.cover.headline || p.title, marks: p.cover.marks || [] } });
      }
      for (const f of p.figures || []) if (f.image) jobs.push({ image: f.image, html: "figure.html", w: 1600, h: 900, key: "FIGURE", spec: f });
      if (p.social && p.social.image) {
        jobs.push({ image: p.social.image, html: "social.html", w: 1080, h: 1350, key: "SOCIAL",
          spec: { kicker: p.social.kicker || t.title, by: p.social.by || "", headline: p.social.headline || p.title, cta: p.social.cta || "Read on vionlabs.com", marks: p.social.marks || [] } });
      }
      if (p.thumb && p.thumb.image) {
        jobs.push({ image: p.thumb.image, html: "thumb.html", w: 1600, h: 1260, key: "THUMB",
          spec: { kicker: p.thumb.kicker || t.title, headline: p.thumb.headline || p.title, marks: p.thumb.marks || [] } });
      }
    }
  }
  if (!jobs.length) { console.log("No pieces with images" + (only ? " in " + only : "")); return; }
  for (const [f, md5] of Object.entries(LOGOS)) {
    const got = crypto.createHash("md5").update(fs.readFileSync(path.join(__dirname, "assets", f))).digest("hex");
    if (got !== md5) throw new Error("assets/" + f + " isn't the official logo file any more; restore it from the website's assets");
  }
  const browser = await playwright().chromium.launch();
  for (const j of jobs) {
    const page = await browser.newPage({ viewport: { width: j.w, height: j.h } });
    await page.addInitScript(([k, s]) => { window[k] = s; }, [j.key, j.spec]);
    await page.goto("file://" + path.join(__dirname, j.html));
    await page.evaluate(() => document.fonts.ready);
    const logo = await page.$$eval("img", (els, files) => els.some((e) => files.includes((e.getAttribute("src") || "").replace(/^assets\//, ""))
      && (e.getAttribute("src") || "").startsWith("assets/") && e.complete && e.naturalWidth > 0), Object.keys(LOGOS));
    if (!logo) throw new Error(j.html + " doesn't show an official Vionlabs logo from assets/");
    const out = path.join(dir, j.image);
    fs.mkdirSync(path.dirname(out), { recursive: true });
    await page.screenshot({ path: out });
    await page.close();
    console.log("Wrote " + path.relative(process.cwd(), out));
  }
  await browser.close();
})();
