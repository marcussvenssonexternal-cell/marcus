// Renders the original footage in footage.js to img/g-<scene>.jpg (1920x1080).
//   node footage.cjs              (all scenes)
//   node footage.cjs dawn city    (only these)
const path = require("path");
const { chromium } = require("playwright");
(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1920, height: 1080 } });
  page.on("pageerror", (e) => console.error("pageerror:", e.message));
  await page.goto("file://" + path.join(__dirname, "footage.html"));
  const names = process.argv.slice(2).length ? process.argv.slice(2) : await page.evaluate(() => window.SCENES);
  for (const s of names) {
    await page.goto("file://" + path.join(__dirname, "footage.html") + `?s=${s}`);
    await page.waitForFunction(() => window.done);
    await (await page.$("#c")).screenshot({ path: path.join(__dirname, "img", `g-${s}.jpg`), type: "jpeg", quality: 90 });
    console.log("rendered g-" + s);
  }
  await browser.close();
})();
