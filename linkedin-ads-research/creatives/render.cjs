// Screenshots every <section class="ad"> in ads.html to png/<id>.png at 1200x1200.
//   node render.cjs            (all ads)
//   node render.cjs a1 c2      (only these ids)
const path = require("path");
const fs = require("fs");
const { chromium } = require("playwright");

(async () => {
  const only = process.argv.slice(2);
  const out = path.join(__dirname, "png");
  fs.mkdirSync(out, { recursive: true });

  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1400, height: 1400 }, deviceScaleFactor: 1 });
  await page.goto("file://" + path.join(__dirname, "ads.html"));
  await page.evaluate(() => document.fonts.ready);

  for (const ad of await page.$$("section.ad")) {
    const id = await ad.getAttribute("id");
    if (only.length && !only.includes(id)) continue;
    await ad.screenshot({ path: path.join(out, `${id}.png`) });
    console.log("rendered", id);
  }
  await browser.close();
})();
