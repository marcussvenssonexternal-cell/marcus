#!/usr/bin/env node
// Render LinkedIn article covers for the Deep Dives packs.
//
//   node content-engine/bot/cover.js            # every piece with a "cover" in deep-dives/*.json
//   node content-engine/bot/cover.js ad-breaks  # one topic
//
// Each cover is drawn by cover.html at 1920x1080 and saved to deep-dives/<cover.image>, which the
// publish step uploads next to the page. Needs Playwright (installed globally in the cloud sessions).
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
    for (const p of (t.pack || {}).pieces || []) if (p.cover && p.cover.image) jobs.push({ t, p });
  }
  if (!jobs.length) { console.log("No pieces with a cover" + (only ? " in " + only : "")); return; }
  const browser = await playwright().chromium.launch();
  for (const { t, p } of jobs) {
    const page = await browser.newPage({ viewport: { width: 1920, height: 1080 } });
    const spec = { kicker: p.cover.kicker || t.title, by: p.cover.by || "", headline: p.cover.headline || p.title, marks: p.cover.marks || [] };
    await page.addInitScript((s) => { window.COVER = s; }, spec);
    await page.goto("file://" + path.join(__dirname, "cover.html"));
    await page.evaluate(() => document.fonts.ready);
    const out = path.join(dir, p.cover.image);
    fs.mkdirSync(path.dirname(out), { recursive: true });
    await page.screenshot({ path: out });
    await page.close();
    console.log("Wrote " + path.relative(process.cwd(), out));
  }
  await browser.close();
})();
