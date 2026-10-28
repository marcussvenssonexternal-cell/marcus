#!/usr/bin/env node
// Render the images for the Deep Dives packs: blog post covers, in-article figures and LinkedIn images.
//
//   node content-engine/bot/cover.js            # every piece with a "cover", "figures" or "social" in deep-dives/*.json
//   node content-engine/bot/cover.js ad-breaks  # one topic
//
// Covers are drawn by cover.html at 1920x1080, figures by figure.html at 1600x900 and the LinkedIn feed
// image that shares a long read by social.html at 1080x1350, then saved to deep-dives/<image>. The
// publish step uploads them next to the page, and the Google Doc loads them from GitHub, so push before
// exporting. Needs Playwright (installed globally in the cloud sessions).
const fs = require("fs");
const path = require("path");
const { execSync } = require("child_process");

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
    }
  }
  if (!jobs.length) { console.log("No pieces with images" + (only ? " in " + only : "")); return; }
  const browser = await playwright().chromium.launch();
  for (const j of jobs) {
    const page = await browser.newPage({ viewport: { width: j.w, height: j.h } });
    await page.addInitScript(([k, s]) => { window[k] = s; }, [j.key, j.spec]);
    await page.goto("file://" + path.join(__dirname, j.html));
    await page.evaluate(() => document.fonts.ready);
    const out = path.join(dir, j.image);
    fs.mkdirSync(path.dirname(out), { recursive: true });
    await page.screenshot({ path: out });
    await page.close();
    console.log("Wrote " + path.relative(process.cwd(), out));
  }
  await browser.close();
})();
