// Rights audit. The rule from the board (Oct 2026): famous films and series may appear as small posters among many,
// never as one big screen; a big screen shows a lesser-known title instead (Arash: "ta lite mindre kända filmer").
// This measures every famous film or TV image (img/t-*, img/r-*, except the LESSER titles below) as it is actually
// drawn, in every campaign image and through every video (sampled every 0.2 s), and reports the largest area any
// single one covers, as a share of a square the width of the ad (so a 9:16 video is held to the same on-screen
// size as a 1:1 one). Lesser-known titles and product screenshots don't count.
//   node rights-audit.cjs                  (all images and videos)
//   node rights-audit.cjs a3r-L ad3r-S     (only these)
//   node rights-audit.cjs stills           (every image, no videos; "videos" for the reverse)
// Writes brief/rights-audit.json and prints each asset with OVER or ok.
const path = require("path");
const fs = require("fs");
const { chromium } = require("playwright");

// Calibrated on the board's two examples from Video 4: the rushing wall of thumbnails (fine, about 5% each)
// and the La La Land frame (not fine, 20% and more).
const MAX_AREA = 0.075;

const VIDEOS = ["ad0", "ad3", "v1", "v1b", "v2", "v3", "v4", "ad0r", "ad3r", "v1r", "v1br", "v2r", "v3r", "v4r"].flatMap((k) => [k + "-S", k + "-V"]);

// In the page: the largest famous film image on screen inside the given frame. Its true area is counted by hit-testing
// a grid of points, so tilted, scaled and clipped images count exactly as much as is drawn.
function measure(frame) {
  const fr = frame.getBoundingClientRect(), base = fr.width * fr.width;
  let worst = { area: 0, name: null };
  for (const im of frame.querySelectorAll("img")) {
    const m = (im.getAttribute("src") || "").match(/img\/((?:t|r)-([^/]+))\.jpg$/);
    // lesser-known titles may fill a screen; keep in step with LESSER in brief-anim.js and brief.js
    if (!m || ["pap", "kelly", "upgrade", "rescue", "secret", "vacation", "shaolin", "fanboys", "burt"].includes(m[2])) continue;
    let op = 1, hidden = false;
    for (let e = im; e && e !== frame.parentElement; e = e.parentElement) {
      const cs = getComputedStyle(e);
      op *= +cs.opacity;
      if (cs.visibility === "hidden" || cs.display === "none") hidden = true;
      const blur = cs.filter.match(/blur\(([\d.]+)px\)/);
      if (blur && +blur[1] >= 10) hidden = true; // blurred beyond recognition
    }
    if (hidden || op < 0.2) continue;
    const r = im.getBoundingClientRect();
    const x1 = Math.max(r.left, fr.left), y1 = Math.max(r.top, fr.top), x2 = Math.min(r.right, fr.right), y2 = Math.min(r.bottom, fr.bottom);
    const box = Math.max(0, x2 - x1) * Math.max(0, y2 - y1);
    if (box / base <= Math.max(worst.area, 0.02)) continue; // can't beat the current worst
    const step = Math.max(4, Math.sqrt(box / 900));
    let hits = 0;
    for (let y = y1 + step / 2; y < y2; y += step) for (let x = x1 + step / 2; x < x2; x += step) if (document.elementsFromPoint(x, y).includes(im)) hits++;
    const area = (hits * step * step) / base;
    if (area > worst.area) worst = { area, name: m[1] };
  }
  return worst;
}

(async () => {
  const args = process.argv.slice(2), stills = !args.includes("videos"), videos = !args.includes("stills");
  const only = args.filter((a) => a !== "stills" && a !== "videos");
  const out = {};
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1400, height: 1400 } });
  await page.goto("file://" + path.join(__dirname, "brief.html"));
  await page.evaluate(() => document.fonts.ready);
  await page.waitForLoadState("networkidle");
  const ids = await page.evaluate(() => [...document.querySelectorAll("section.ad")].map((s) => s.id));
  for (const id of ids) {
    if (!stills || (only.length && !only.includes(id))) continue;
    out[id] = await page.evaluate(([id, fn]) => { const s = document.getElementById(id); s.scrollIntoView({ block: "start" }); return (0, eval)(`(${fn})`)(s); }, [id, measure.toString()]);
  }
  for (const v of VIDEOS) {
    if (!videos || (only.length && !only.includes(v))) continue;
    const q = await browser.newPage({ viewport: { width: 1080, height: v.endsWith("-V") ? 1920 : 1080 } });
    await q.goto("file://" + path.join(__dirname, "brief-anim.html") + `?v=${v}`);
    await q.evaluate(() => document.fonts.ready);
    await q.evaluate(() => window.animReady);
    const { duration } = await q.evaluate(() => window.VIDEO);
    if (!duration) { await q.close(); continue; }
    let worst = { area: 0 };
    for (let t = 0; t < duration; t += 0.2) {
      const m = await q.evaluate(([t, fn]) => { window.seek(t); return (0, eval)(`(${fn})`)(document.getElementById("stage")); }, [t, measure.toString()]);
      if (m.area > worst.area) worst = { ...m, t: +t.toFixed(1) };
    }
    out[v] = worst;
    await q.close();
  }
  await browser.close();
  const file = path.join(__dirname, "brief", "rights-audit.json");
  const all = fs.existsSync(file) && (only.length || args.length) ? JSON.parse(fs.readFileSync(file, "utf8")) : {};
  for (const [id, m] of Object.entries(out)) all[id] = { ...m, area: +m.area.toFixed(4), ok: m.area <= MAX_AREA };
  fs.writeFileSync(file, JSON.stringify({ max_area: MAX_AREA, ...Object.fromEntries(Object.entries(all).filter(([k]) => k !== "max_area")) }, null, 1));
  for (const [id, m] of Object.entries(out)) {
    console.log(`${m.area > MAX_AREA ? "OVER " : "ok   "} ${id.padEnd(10)} ${(m.area * 100).toFixed(1).padStart(5)}%  ${m.name || "-"}${m.t !== undefined ? ` at ${m.t}s` : ""}`);
  }
})();
