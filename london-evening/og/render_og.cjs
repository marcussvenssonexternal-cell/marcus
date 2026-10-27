// Renders og-image.html to ../assets/og-image.jpg (1200×627) in headless Chromium.
// Usage: node og/render_og.cjs
const { chromium } = require('playwright');
const path = require('path');

(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1200, height: 627 } });
  await page.goto('file://' + path.join(__dirname, 'og-image.html'), { waitUntil: 'networkidle' });
  await page.evaluate(() => document.fonts.ready);
  await page.locator('.card').screenshot({
    path: path.join(__dirname, '..', 'assets', 'og-image.jpg'),
    type: 'jpeg',
    quality: 90,
  });
  await browser.close();
})();
