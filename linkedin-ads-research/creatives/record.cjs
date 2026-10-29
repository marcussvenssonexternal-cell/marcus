// Records the brief campaign videos: renders brief-anim.html?v=<id> frame by frame and encodes MP4
// to brief/video/, plus a poster PNG for the review page.
//   node record.cjs                  (all of them: the rights-safe "r" versions, which are the ones to run)
//   node record.cjs ad0-S ad3-V      (only these, e.g. a retired original)
const path = require("path");
const fs = require("fs");
const { execFileSync } = require("child_process");
const { chromium } = require("playwright");

(async () => {
  const ids = process.argv.slice(2).length ? process.argv.slice(2)
    : ["ad0r", "ad3r", "v1r", "v1br", "v2r", "v3r", "v4r"].flatMap((k) => [k + "-S", k + "-V"]);
  const outDir = path.join(__dirname, "brief", "video");
  fs.mkdirSync(outDir, { recursive: true });
  const browser = await chromium.launch();
  for (const id of ids) {
    const vertical = id.endsWith("-V");
    const page = await browser.newPage({ viewport: { width: 1080, height: vertical ? 1920 : 1080 }, deviceScaleFactor: 1 });
    page.on("pageerror", (e) => console.error("pageerror:", e.message));
    await page.goto("file://" + path.join(__dirname, "brief-anim.html") + `?v=${id}`);
    await page.evaluate(() => document.fonts.ready);
    await page.evaluate(() => window.animReady);
    await page.waitForLoadState("networkidle");
    const { duration, fps, poster } = await page.evaluate(() => window.VIDEO);
    const frames = fs.mkdtempSync(path.join(require("os").tmpdir(), `rec-${id}-`));
    const stage = await page.$("#stage");
    const n = Math.round(duration * fps);
    for (let i = 0; i < n; i++) {
      await page.evaluate((t) => window.seek(t), i / fps);
      await stage.screenshot({ path: path.join(frames, `f${String(i).padStart(4, "0")}.png`) });
    }
    const out = path.join(outDir, `${id}.mp4`);
    execFileSync("ffmpeg", ["-y", "-loglevel", "error", "-framerate", String(fps), "-i", path.join(frames, "f%04d.png"),
      "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "20", "-preset", "medium", "-movflags", "+faststart", out]);
    // poster frame for the review page
    fs.copyFileSync(path.join(frames, `f${String(Math.min(n - 1, Math.round(poster * fps))).padStart(4, "0")}.png`), path.join(outDir, `${id}.png`));
    fs.rmSync(frames, { recursive: true, force: true });
    console.log("recorded", id, n, "frames");
    await page.close();
  }
  await browser.close();
})();
