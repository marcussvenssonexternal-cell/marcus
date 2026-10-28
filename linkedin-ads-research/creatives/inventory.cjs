// Lists which website images (img/<name>.jpg) each campaign asset and video shows, read from the rendered
// pages so it cannot drift from the ads. Used for the rights check (brief/rights-check.md).
//   node inventory.cjs > brief/rights-inventory.json
const path = require("path");
const { chromium } = require("playwright");
(async () => {
  const dir = __dirname, out = {};
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 1400, height: 1400 } });
  await p.goto("file://" + path.join(dir, "brief.html"));
  await p.evaluate(() => document.fonts.ready);
  Object.assign(out, await p.evaluate(() => Object.fromEntries([...document.querySelectorAll("section.ad")].map((s) =>
    [s.id, [...new Set([...s.querySelectorAll("img")].map((i) => (i.getAttribute("src").match(/img\/(.+)\.jpg/) || [])[1]).filter(Boolean))]]))));
  for (const v of ["ad0-S", "ad3-S", "v1-S", "v1b-S", "v2-S", "v3-S", "v4-S"]) {
    const q = await b.newPage({ viewport: { width: 1080, height: 1080 } });
    await q.goto("file://" + path.join(dir, "brief-anim.html") + "?v=" + v);
    out["video:" + v] = await q.evaluate(() => [...new Set([...document.querySelectorAll("#stage img")].map((i) => (i.getAttribute("src").match(/img\/(.+)\.jpg/) || [])[1]).filter(Boolean))]);
    await q.close();
  }
  console.log(JSON.stringify(out));
  await b.close();
})();
