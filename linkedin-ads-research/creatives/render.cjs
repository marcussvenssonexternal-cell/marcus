// Screenshots every <section class="ad"> in a page to <out>/<id>.png at its own size.
//   node render.cjs                              (ads.html -> png/)
//   node render.cjs a1 c2                        (only these ids)
//   PAGE=brief.html OUT=brief/png node render.cjs  (the ad-brief campaign)
const path = require("path");
const fs = require("fs");
const { chromium } = require("playwright");

(async () => {
  const only = process.argv.slice(2);
  const out = path.join(__dirname, process.env.OUT || "png");
  fs.mkdirSync(out, { recursive: true });

  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1400, height: 1400 }, deviceScaleFactor: 1 });
  page.on("pageerror", (e) => console.error("pageerror:", e.message));
  await page.goto("file://" + path.join(__dirname, process.env.PAGE || "ads.html"));
  await page.evaluate(() => document.fonts.ready);
  await page.waitForLoadState("networkidle");
  await page.evaluate(() => Promise.all([...document.images].map((i) => i.complete ? 0 : new Promise((r) => (i.onload = i.onerror = r)))));

  for (const ad of await page.$$("section.ad")) {
    const id = await ad.getAttribute("id");
    if (only.length && !only.includes(id)) continue;
    await ad.screenshot({ path: path.join(out, `${id}.png`) });
    console.log("rendered", id);
  }
  await browser.close();
})();
