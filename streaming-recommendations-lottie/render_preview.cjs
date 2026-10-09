// Renders the Lottie to PNG frames with lottie-web (SVG renderer) in headless Chromium.
//   node render_preview.cjs <anim.json> <out-dir> [--width 1920] [--step 1] [--frames 0,90,120]
// Then e.g.: ffmpeg -framerate 30 -i out/frame_%04d.png -pix_fmt yuv420p preview.mp4
const fs = require("fs");
const path = require("path");
const { chromium } = require("playwright");

const args = process.argv.slice(2);
const opt = (name, dflt) => {
  const i = args.indexOf(`--${name}`);
  return i >= 0 ? args[i + 1] : dflt;
};
const [jsonPath, outDir] = args;
const width = Number(opt("width", 1920));
const step = Number(opt("step", 1));
const only = opt("frames", "");
const lottieJs = require.resolve(opt("lottie", "lottie-web/build/player/lottie.min.js"));

(async () => {
  const data = JSON.parse(fs.readFileSync(jsonPath, "utf8"));
  const height = Math.round((width * data.h) / data.w);
  fs.mkdirSync(outDir, { recursive: true });
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width, height } });
  await page.setContent(
    `<html><body style="margin:0;background:#000"><div id="c" style="width:${width}px;height:${height}px"></div></body></html>`
  );
  await page.addScriptTag({ path: lottieJs });
  await page.evaluate((d) => {
    window.anim = lottie.loadAnimation({
      container: document.getElementById("c"),
      renderer: "svg",
      loop: false,
      autoplay: false,
      animationData: d,
    });
  }, data);
  await page.waitForFunction(() => window.anim && window.anim.isLoaded);
  const frames = only
    ? only.split(",").map(Number)
    : Array.from({ length: Math.ceil((data.op - data.ip) / step) }, (_, i) => data.ip + i * step);
  const el = await page.$("#c");
  for (const f of frames) {
    await page.evaluate((fr) => window.anim.goToAndStop(fr, true), f);
    await el.screenshot({ path: path.join(outDir, `frame_${String(f).padStart(4, "0")}.png`) });
  }
  await browser.close();
  console.log(`rendered ${frames.length} frames to ${outDir}`);
})();
