// Original "footage" for the ads: cinematic stills drawn in code, so the big screens in the ads (players, phones,
// the hero frame) show no film, show or actor. Famous titles only appear as small posters among many
// (rights-audit.cjs checks that). Each scene is 1920x1080 with its subject placed so a 9:16 crop still holds it.
//   footage.html?s=dawn      one scene on a canvas; footage.cjs renders them all to img/g-<scene>.jpg
(function () {
  const W = 1920, H = 1080;
  const cv = document.createElement("canvas");
  cv.width = W; cv.height = H; cv.id = "c";
  document.body.appendChild(cv);
  const ctx = cv.getContext("2d");

  // ---------------------------------------------------------------- helpers
  const rand = (seed) => () => (seed = (seed * 16807) % 2147483647) / 2147483647;
  function noise1(seed) {
    const r = rand(seed), v = Array.from({ length: 512 }, r);
    const at = (x) => { const i = Math.floor(x), f = x - i, s = f * f * (3 - 2 * f); return v[i & 511] * (1 - s) + v[(i + 1) & 511] * s; };
    return (x, oct = 5) => { let a = 0, amp = 1, fr = 1, n = 0; for (let o = 0; o < oct; o++) { a += amp * at(x * fr); n += amp; amp *= 0.5; fr *= 2.03; } return a / n; };
  }
  const lin = (y0, y1, stops) => { const g = ctx.createLinearGradient(0, y0, 0, y1); stops.forEach(([o, c]) => g.addColorStop(o, c)); return g; };
  const radial = (x, y, r, stops) => { const g = ctx.createRadialGradient(x, y, 0, x, y, r); stops.forEach(([o, c]) => g.addColorStop(o, c)); return g; };
  function sky(stops) { ctx.fillStyle = lin(0, H, stops); ctx.fillRect(0, 0, W, H); }
  function glow(x, y, r, col, a = 1) { ctx.save(); ctx.globalAlpha = a; ctx.globalCompositeOperation = "screen"; ctx.fillStyle = radial(x, y, r, [[0, col], [1, "rgba(0,0,0,0)"]]); ctx.fillRect(x - r, y - r, 2 * r, 2 * r); ctx.restore(); }
  // a ridge line from fractal noise, filled down to the bottom
  function ridge({ y, amp, freq, seed, fill, oct = 5, sharp = 0, edge = null, x0 = 0, x1 = W }) {
    const n = noise1(seed), pts = [];
    for (let x = x0 - 10; x <= x1 + 10; x += 4) { let v = n(x * freq, oct); if (sharp) v = 1 - Math.abs(v * 2 - 1) * sharp - (1 - sharp) * (1 - v); pts.push([x, y - v * amp]); }
    ctx.beginPath(); ctx.moveTo(x0 - 10, H + 10); pts.forEach(([x, yy]) => ctx.lineTo(x, yy)); ctx.lineTo(x1 + 10, H + 10); ctx.closePath();
    ctx.fillStyle = fill; ctx.fill();
    if (edge) { ctx.save(); ctx.beginPath(); pts.forEach(([x, yy], i) => (i ? ctx.lineTo(x, yy) : ctx.moveTo(x, yy))); ctx.strokeStyle = edge; ctx.lineWidth = 2; ctx.filter = "blur(1.5px)"; ctx.stroke(); ctx.restore(); }
    return (x) => { const i = Math.max(0, Math.min(pts.length - 1, Math.round((x - x0 + 10) / 4))); return pts[i][1]; };
  }
  function haze(y0, y1, col) { ctx.fillStyle = lin(y0, y1, [[0, "rgba(0,0,0,0)"], [0.5, col], [1, "rgba(0,0,0,0)"]]); ctx.fillRect(0, y0, W, y1 - y0); }
  function rays(x, y, col, n, seed, len = 1600, spread = 1.2, dir = Math.PI / 2) {
    const r = rand(seed);
    ctx.save(); ctx.globalCompositeOperation = "screen"; ctx.filter = "blur(18px)";
    for (let i = 0; i < n; i++) {
      const a = dir + (r() - 0.5) * spread, w = 0.01 + r() * 0.035;
      ctx.globalAlpha = 0.05 + r() * 0.1;
      ctx.beginPath(); ctx.moveTo(x, y); ctx.lineTo(x + Math.cos(a - w) * len, y + Math.sin(a - w) * len); ctx.lineTo(x + Math.cos(a + w) * len, y + Math.sin(a + w) * len); ctx.closePath();
      ctx.fillStyle = col; ctx.fill();
    }
    ctx.restore();
  }
  function clouds(seed, y0, y1, col, n = 40, blur = 26, sx = 1) {
    const r = rand(seed);
    ctx.save(); ctx.filter = `blur(${blur}px)`;
    for (let i = 0; i < n; i++) {
      const x = r() * W, y = y0 + r() * (y1 - y0), w = (180 + r() * 420) * sx, h = 14 + r() * 40;
      ctx.globalAlpha = 0.15 + r() * 0.35; ctx.fillStyle = col;
      ctx.beginPath(); ctx.ellipse(x, y, w, h, 0, 0, Math.PI * 2); ctx.fill();
    }
    ctx.restore();
  }
  function stars(seed, n, y1, a = 1) {
    const r = rand(seed);
    for (let i = 0; i < n; i++) { const x = r() * W, y = r() * y1, s = r() < 0.06 ? 2.2 : 0.6 + r() * 1.1; ctx.globalAlpha = a * (0.25 + r() * 0.75) * (1 - y / y1 * 0.6); ctx.fillStyle = "#fff"; ctx.fillRect(x, y, s, s); }
    ctx.globalAlpha = 1;
  }
  function grade(seed, vig = 0.55, grain = 9) {
    // vignette, then film grain
    ctx.fillStyle = radial(W / 2, H / 2, W * 0.62, [[0.45, "rgba(0,0,0,0)"], [1, `rgba(0,0,0,${vig})`]]);
    ctx.fillRect(0, 0, W, H);
    const im = ctx.getImageData(0, 0, W, H), d = im.data, r = rand(seed);
    for (let i = 0; i < d.length; i += 4) { const g = (r() - 0.5) * grain * 2; d[i] += g; d[i + 1] += g; d[i + 2] += g; }
    ctx.putImageData(im, 0, 0);
  }

  // ---------------------------------------------------------------- silhouettes
  // a standing person, feet at (x, y), height h; pose: "stand" | "coat" | "reach" | "sword" | "lantern" | "astro"
  function person(x, y, h, { pose = "stand", fill = "#06070b", lean = 0, face = 1 } = {}) {
    const u = h / 100;
    ctx.save(); ctx.translate(x, y); ctx.scale(face, 1); ctx.rotate(lean); ctx.fillStyle = fill; ctx.strokeStyle = fill; ctx.lineCap = "round"; ctx.lineJoin = "round";
    const P = (pts) => { ctx.beginPath(); pts.forEach(([a, b], i) => (i ? ctx.lineTo(a * u, -b * u) : ctx.moveTo(a * u, -b * u))); ctx.closePath(); ctx.fill(); };
    const limb = (pts, w) => { ctx.lineWidth = w * u; ctx.beginPath(); pts.forEach(([a, b], i) => (i ? ctx.lineTo(a * u, -b * u) : ctx.moveTo(a * u, -b * u))); ctx.stroke(); };
    const astro = pose === "astro";
    // head
    ctx.beginPath(); ctx.ellipse(0.5 * u, -91 * u, (astro ? 9 : 6.2) * u, (astro ? 9 : 7.4) * u, 0, 0, Math.PI * 2); ctx.fill();
    // neck and torso
    if (pose === "coat" || pose === "lantern") P([[-3, 84], [4, 84], [12, 80], [13.5, 62], [14, 40], [17, 20], [-15, 20], [-13, 40], [-13, 62], [-11, 80]]);
    else P([[-3, 84], [4, 84], [12, 80], [13, 62], [10, 46], [-9, 46], [-12, 62], [-11, 80]]);
    if (astro) { P([[-24, 82], [-10, 84], [-10, 50], [-24, 52]]); limb([[-12, 80], [-12, 62]], 10); }
    // legs
    limb([[-4, 47], [-6, 24], [-6, 2]], 8.5); limb([[4, 47], [6, 24], [8, 2]], 8.5);
    P([[-10, 3], [0, 3], [1, 0], [-11, 0]]); P([[4, 3], [13, 3], [14, 0], [3, 0]]);
    // arms
    if (pose === "reach") { limb([[-10, 79], [-26, 92], [-38, 104]], 6.5); limb([[10, 79], [24, 94], [34, 107]], 6.5); }
    else if (pose === "sword") { limb([[-10, 79], [-17, 62], [-16, 47]], 6.5); limb([[10, 79], [18, 95], [22, 112]], 6.5); limb([[22, 110], [25, 160]], 2.4); limb([[17, 112], [28, 112]], 3); }
    else if (pose === "lantern") { limb([[-10, 79], [-15, 62], [-15, 47]], 6.5); limb([[10, 79], [20, 64], [26, 52]], 6.5); limb([[26, 52], [26, 46]], 1.2); }
    else { limb([[-10, 79], [-15, 62], [-14, 46]], 6.5); limb([[10, 79], [15, 62], [14, 46]], 6.5); }
    ctx.restore();
    return { hand: [x + 26 * u * face, y - 42 * u] };
  }
  // a cape blowing in the wind, behind a figure
  function cape(x, y, h, dir = -1, fill = "#06070b") {
    const u = h / 100;
    ctx.save(); ctx.translate(x, y); ctx.fillStyle = fill; ctx.beginPath();
    ctx.moveTo(-9 * u, -80 * u); ctx.quadraticCurveTo(dir * 30 * u, -60 * u, dir * 46 * u, -18 * u); ctx.quadraticCurveTo(dir * 30 * u, -24 * u, dir * 22 * u, -10 * u);
    ctx.quadraticCurveTo(dir * 10 * u, -30 * u, 9 * u, -80 * u); ctx.closePath(); ctx.fill(); ctx.restore();
  }
  function spear(x, y, h, flag = 0, fill = "#06070b", col = "#06070b") {
    ctx.save(); ctx.strokeStyle = fill; ctx.lineWidth = Math.max(1.5, h * 0.022); ctx.beginPath(); ctx.moveTo(x, y); ctx.lineTo(x + h * 0.04, y - h * 1.5); ctx.stroke();
    if (flag) { ctx.fillStyle = col; ctx.beginPath(); const fx = x + h * 0.04, fy = y - h * 1.5; ctx.moveTo(fx, fy); ctx.quadraticCurveTo(fx - flag * 0.5, fy + flag * 0.12, fx - flag, fy + flag * 0.05); ctx.lineTo(fx - flag * 0.9, fy + flag * 0.42); ctx.quadraticCurveTo(fx - flag * 0.45, fy + flag * 0.5, fx, fy + flag * 0.45); ctx.fill(); }
    ctx.restore();
  }
  function pine(x, y, h, fill) {
    // overlapping tiers, widest at the bottom, on a thin trunk
    ctx.fillStyle = fill; const w = h * 0.3, tiers = 6;
    ctx.fillRect(x - h * 0.012, y - h * 0.2, h * 0.024, h * 0.2);
    for (let i = 0; i < tiers; i++) { const k = (i + 1) / tiers, top = y - h + (h * 0.78) * (i / tiers) * 0.92, bot = y - h * 0.12 - (h * 0.78) * (1 - k) * 0.6;
      ctx.beginPath(); ctx.moveTo(x, top); ctx.lineTo(x + w * (0.35 + 0.65 * k), bot); ctx.quadraticCurveTo(x, bot - h * 0.04, x - w * (0.35 + 0.65 * k), bot); ctx.closePath(); ctx.fill(); }
  }

  // ---------------------------------------------------------------- scenes
  const SCENES = {
    // a lone figure on a hilltop at sunrise: hope
    dawn() {
      sky([[0, "#1d2a4d"], [0.32, "#5a4a78"], [0.52, "#d9786a"], [0.64, "#f6b57a"], [0.72, "#ffd9a0"], [1, "#ffd9a0"]]);
      glow(820, 640, 900, "rgba(255,190,120,.9)", 0.8); glow(820, 640, 180, "rgba(255,245,215,1)", 1);
      ctx.fillStyle = "#fff6e0"; ctx.beginPath(); ctx.arc(820, 640, 54, 0, Math.PI * 2); ctx.fill();
      clouds(3, 200, 520, "#f2a58a", 34, 30, 1.4); clouds(4, 120, 330, "#7a5f8f", 20, 30, 1.6);
      ridge({ y: 690, amp: 120, freq: 0.0024, seed: 11, fill: "#b46e78" }); haze(560, 760, "rgba(255,200,160,.5)");
      ridge({ y: 780, amp: 150, freq: 0.002, seed: 12, fill: "#7c4f6b" }); haze(660, 860, "rgba(250,170,150,.45)");
      rays(820, 640, "#ffe2b0", 26, 5, 1500, 2.4, Math.PI * 0.62);
      ridge({ y: 900, amp: 160, freq: 0.0018, seed: 13, fill: "#43304f" }); haze(820, 960, "rgba(220,140,140,.35)");
      // the outcrop the figure stands on
      ctx.fillStyle = "#120d18"; ctx.beginPath(); ctx.moveTo(760, H); ctx.bezierCurveTo(980, 840, 1080, 780, 1190, 772); ctx.lineTo(1270, 778); ctx.bezierCurveTo(1430, 800, 1700, 900, 1960, 930); ctx.lineTo(1960, H); ctx.closePath(); ctx.fill();
      ridge({ y: 1120, amp: 210, freq: 0.0016, seed: 14, fill: "#0b0810" });
      person(1228, 778, 200, { pose: "reach", fill: "#0a070d" });
      glow(1228, 690, 220, "rgba(255,190,140,.35)", 0.6);
      grade(21, 0.5);
    },
    // a figure under a streetlight in a rainy city at night: thriller, drama
    city() {
      sky([[0, "#05080f"], [0.45, "#0d1830"], [0.7, "#28304e"], [1, "#0a0d14"]]);
      glow(960, 760, 1000, "rgba(255,120,80,.35)", 0.7);
      const r = rand(31);
      const layer = (n, base, var_, col, win, alpha, seedOff) => { for (let i = 0; i < n; i++) { const w = 60 + r() * 140, x = (i / n) * W + (r() - 0.5) * 90 - 30, h = base + r() * var_, y = 760 - h;
        ctx.fillStyle = col; ctx.fillRect(x, y, w, h + 400); if (r() < 0.25) ctx.fillRect(x + w * 0.45, y - 40 - r() * 60, 3, 100);
        for (let wy = y + 14; wy < 760; wy += 18) for (let wx = x + 8; wx < x + w - 8; wx += 14) if (r() < win) { ctx.globalAlpha = alpha * (0.4 + r() * 0.6); ctx.fillStyle = r() < 0.75 ? "#ffcf8a" : "#bcd8ff"; ctx.fillRect(wx, wy, 6, 8); ctx.globalAlpha = 1; } } };
      layer(26, 260, 330, "#141a2c", 0.18, 0.45); haze(420, 820, "rgba(80,90,140,.35)");
      layer(18, 140, 280, "#0c101c", 0.22, 0.85); haze(600, 860, "rgba(255,140,90,.18)");
      // wet street with reflections
      ctx.fillStyle = lin(760, H, [[0, "#151a27"], [1, "#05070b"]]); ctx.fillRect(0, 760, W, H - 760);
      ctx.save(); ctx.globalAlpha = 0.35; ctx.filter = "blur(10px)"; ctx.translate(0, 1520); ctx.scale(1, -1); ctx.drawImage(cv, 0, 560, W, 200, 0, 560, W, 200); ctx.restore();
      // streetlight and its cone
      const lx = 700;
      ctx.fillStyle = "#07090e"; ctx.fillRect(lx - 5, 330, 10, 600); ctx.fillRect(lx - 5, 330, 90, 8);
      ctx.save(); ctx.globalCompositeOperation = "screen"; ctx.globalAlpha = 0.42; ctx.filter = "blur(14px)";
      ctx.fillStyle = lin(340, 960, [[0, "rgba(255,214,150,.9)"], [1, "rgba(255,190,120,0)"]]); ctx.beginPath(); ctx.moveTo(775, 342); ctx.lineTo(575, 960); ctx.lineTo(1015, 960); ctx.closePath(); ctx.fill(); ctx.restore();
      glow(780, 345, 120, "rgba(255,226,170,1)", 1);
      ctx.save(); ctx.globalCompositeOperation = "screen"; ctx.globalAlpha = 0.5; ctx.fillStyle = radial(790, 935, 260, [[0, "rgba(255,200,140,.8)"], [1, "rgba(0,0,0,0)"]]); ctx.beginPath(); ctx.ellipse(790, 935, 260, 40, 0, 0, Math.PI * 2); ctx.fill(); ctx.restore();
      person(800, 935, 300, { pose: "coat", fill: "#050609", face: -1 });
      // rain
      ctx.save(); ctx.strokeStyle = "rgba(190,210,255,.22)"; ctx.lineWidth = 1.2; const rr = rand(37);
      for (let i = 0; i < 900; i++) { const x = rr() * W, y = rr() * H, l = 18 + rr() * 30; ctx.beginPath(); ctx.moveTo(x, y); ctx.lineTo(x - l * 0.18, y + l); ctx.stroke(); } ctx.restore();
      grade(33, 0.6, 10);
    },
    // a car on a desert road at sunset: road trip, feel-good
    road() {
      sky([[0, "#2a2350"], [0.3, "#6a3f7a"], [0.5, "#e2706a"], [0.6, "#f8a96a"], [0.66, "#ffd08a"], [1, "#ffd08a"]]);
      glow(960, 700, 900, "rgba(255,170,110,.8)", 0.8); glow(960, 690, 160, "rgba(255,240,200,1)", 1);
      ctx.fillStyle = "#fff0d0"; ctx.beginPath(); ctx.arc(960, 700, 70, Math.PI, 0); ctx.fill();
      clouds(41, 160, 480, "#f19b86", 30, 26, 1.6); clouds(42, 90, 300, "#7e4f86", 18, 30, 1.8);
      // mesas
      ctx.fillStyle = "#8a4a63"; [[180, 560, 640], [1260, 520, 660], [1500, 430, 600]].forEach(([x, w, top]) => { ctx.beginPath(); ctx.moveTo(x, 705); ctx.lineTo(x + 50, top); ctx.lineTo(x + w - 70, top + 6); ctx.lineTo(x + w, 705); ctx.closePath(); ctx.fill(); });
      haze(600, 740, "rgba(255,180,140,.55)");
      ctx.fillStyle = lin(705, H, [[0, "#6d3a50"], [0.35, "#3a2232"], [1, "#130c12"]]); ctx.fillRect(0, 705, W, H - 705);
      // the road to the horizon
      ctx.fillStyle = "#1b1218"; ctx.beginPath(); ctx.moveTo(950, 705); ctx.lineTo(970, 705); ctx.lineTo(1500, H); ctx.lineTo(420, H); ctx.closePath(); ctx.fill();
      ctx.save(); ctx.globalAlpha = 0.25; ctx.fillStyle = lin(705, H, [[0, "#ffd08a"], [1, "rgba(255,208,138,0)"]]); ctx.beginPath(); ctx.moveTo(950, 705); ctx.lineTo(970, 705); ctx.lineTo(1300, H); ctx.lineTo(620, H); ctx.closePath(); ctx.fill(); ctx.restore();
      ctx.fillStyle = "#f2c27a"; for (let k = 0; k < 9; k++) { const a = Math.pow(k / 9, 1.8), b = Math.pow((k + 0.5) / 9, 1.8), y0 = 705 + a * 375, y1 = 705 + b * 375, w0 = 1 + a * 10, w1 = 1 + b * 10;
        ctx.beginPath(); ctx.moveTo(960 - w0 / 2, y0); ctx.lineTo(960 + w0 / 2, y0); ctx.lineTo(960 + w1 / 2, y1); ctx.lineTo(960 - w1 / 2, y1); ctx.closePath(); ctx.fill(); }
      // the car, from behind
      const cx = 1010, cy = 905, s = 1.25;
      ctx.save(); ctx.translate(cx, cy); ctx.scale(s, s); ctx.fillStyle = "#0b0709";
      ctx.beginPath(); ctx.moveTo(-95, 0); ctx.lineTo(-98, -38); ctx.quadraticCurveTo(-96, -54, -78, -56); ctx.lineTo(-56, -58); ctx.quadraticCurveTo(-46, -92, -14, -94); ctx.lineTo(14, -94); ctx.quadraticCurveTo(46, -92, 56, -58);
      ctx.lineTo(78, -56); ctx.quadraticCurveTo(96, -54, 98, -38); ctx.lineTo(95, 0); ctx.closePath(); ctx.fill();
      ctx.fillRect(-90, -6, 30, 22); ctx.fillRect(60, -6, 30, 22);
      ctx.fillStyle = "#2b2228"; ctx.beginPath(); ctx.moveTo(-44, -60); ctx.quadraticCurveTo(-36, -84, -12, -86); ctx.lineTo(12, -86); ctx.quadraticCurveTo(36, -84, 44, -60); ctx.closePath(); ctx.fill();
      // two heads through the rear window
      ctx.fillStyle = "#0b0709"; ctx.beginPath(); ctx.arc(-18, -64, 9, 0, Math.PI * 2); ctx.arc(19, -66, 10, 0, Math.PI * 2); ctx.fill(); ctx.fillRect(-28, -60, 20, 4); ctx.fillRect(9, -60, 22, 4);
      ctx.restore();
      glow(cx - 100, cy - 45, 70, "rgba(255,40,30,.9)", 0.9); glow(cx + 100, cy - 45, 70, "rgba(255,40,30,.9)", 0.9);
      ctx.fillStyle = "#ff3b2e"; ctx.fillRect(cx - 118, cy - 52, 26, 10); ctx.fillRect(cx + 92, cy - 52, 26, 10);
      rays(960, 700, "#ffd9a0", 22, 43, 1400, 2.6, -Math.PI / 2);
      grade(45, 0.5);
    },
    // two people on the shore at golden hour: romance, warm
    sea() {
      sky([[0, "#3b5d8c"], [0.3, "#9b8aa8"], [0.5, "#f0b48a"], [0.6, "#ffd59a"], [1, "#ffd59a"]]);
      glow(700, 610, 900, "rgba(255,190,120,.85)", 0.8); glow(700, 605, 150, "rgba(255,248,225,1)", 1);
      ctx.fillStyle = "#fff4d6"; ctx.beginPath(); ctx.arc(700, 600, 60, 0, Math.PI * 2); ctx.fill();
      clouds(51, 150, 470, "#f6c7a4", 30, 28, 1.6); clouds(52, 80, 260, "#8f8db0", 16, 30, 1.8);
      // the sea, with a glitter path under the sun
      ctx.fillStyle = lin(640, H, [[0, "#c2827a"], [0.25, "#6d5a72"], [1, "#1c1f33"]]); ctx.fillRect(0, 640, W, H - 640);
      ctx.fillStyle = "#e9a582"; ctx.fillRect(0, 638, W, 4);
      const r = rand(53); ctx.save(); ctx.globalCompositeOperation = "screen";
      for (let i = 0; i < 700; i++) { const y = 645 + Math.pow(r(), 1.6) * 330, spread = 30 + (y - 640) * 0.9, x = 700 + (r() - 0.5) * spread * 2 * r(), w = 6 + r() * 30 * (y - 600) / 300;
        ctx.globalAlpha = 0.25 + r() * 0.6; ctx.fillStyle = "#ffe9bf"; ctx.fillRect(x, y, w, 1.6 + (y - 640) / 160); } ctx.restore();
      // wet sand and foam
      ctx.fillStyle = "#24182a"; ctx.beginPath(); ctx.moveTo(0, 900); ctx.bezierCurveTo(500, 870, 1100, 930, 1960, 860); ctx.lineTo(1960, H); ctx.lineTo(0, H); ctx.closePath(); ctx.fill();
      ctx.strokeStyle = "rgba(255,230,200,.5)"; ctx.lineWidth = 3; ctx.beginPath(); ctx.moveTo(0, 898); ctx.bezierCurveTo(500, 868, 1100, 928, 1960, 858); ctx.stroke();
      ctx.save(); ctx.globalAlpha = 0.25; ctx.fillStyle = "#ffd59a"; ctx.beginPath(); ctx.ellipse(1180, 960, 220, 26, 0, 0, Math.PI * 2); ctx.filter = "blur(12px)"; ctx.fill(); ctx.restore();
      person(1140, 955, 250, { pose: "stand", fill: "#120a12" }); person(1205, 958, 268, { pose: "stand", fill: "#120a12", face: -1 });
      ctx.strokeStyle = "#120a12"; ctx.lineWidth = 12; ctx.lineCap = "round"; ctx.beginPath(); ctx.moveTo(1158, 841); ctx.quadraticCurveTo(1172, 852, 1188, 840); ctx.stroke();
      // their reflections on the wet sand
      ctx.save(); ctx.globalAlpha = 0.28; ctx.translate(0, 1912); ctx.scale(1, -1); person(1140, 955, 250, { fill: "#120a12" }); person(1205, 958, 268, { fill: "#120a12", face: -1 }); ctx.restore();
      grade(55, 0.45);
    },
    // a leader raising a sword before an army on a ridge: epic
    epic() {
      sky([[0, "#120b12"], [0.3, "#4a1f22"], [0.55, "#b8442c"], [0.68, "#f08a3a"], [0.75, "#ffc06a"], [1, "#ffc06a"]]);
      glow(1060, 700, 1000, "rgba(255,120,50,.8)", 0.8); glow(1060, 710, 200, "rgba(255,225,170,1)", 0.9);
      clouds(61, 60, 520, "#3a1a1e", 46, 22, 1.8); clouds(62, 300, 600, "#d7653a", 26, 26, 1.6);
      rays(1060, 710, "#ffb070", 30, 63, 1500, 2.8, -Math.PI / 2);
      ridge({ y: 820, amp: 110, freq: 0.003, seed: 64, fill: "#6e2a22" }); haze(700, 860, "rgba(255,130,70,.45)");
      // the army along the ridge
      const top = ridge({ y: 960, amp: 120, freq: 0.0012, seed: 65, fill: "#1c0b0c", oct: 3 });
      const r = rand(66);
      for (let i = 0; i < 90; i++) { const x = 20 + i * 21 + r() * 10; if (Math.abs(x - 960) < 70) continue; const y = top(x) + 6, h = 60 + r() * 26;
        person(x, y, h, { fill: "#1c0b0c", face: r() < 0.5 ? 1 : -1 }); if (r() < 0.7) spear(x + (r() - 0.5) * 10, y - h * 0.4, h, r() < 0.18 ? h * 0.5 : 0, "#1c0b0c", "#1c0b0c"); }
      haze(860, 1000, "rgba(255,140,80,.12)");
      // the leader, closest to camera
      ctx.fillStyle = "#0a0405"; ctx.beginPath(); ctx.moveTo(700, H); ctx.bezierCurveTo(820, 980, 900, 952, 960, 950); ctx.bezierCurveTo(1030, 952, 1100, 990, 1240, H); ctx.closePath(); ctx.fill();
      cape(960, 956, 250, -1, "#0a0405"); person(960, 956, 250, { pose: "sword", fill: "#0a0405" });
      glow(1016, 640, 90, "rgba(255,220,170,.9)", 0.7);
      grade(67, 0.55, 10);
    },
    // a figure with a lantern in a misty forest: mystery
    forest() {
      sky([[0, "#0e1a1f"], [0.5, "#2d4a4c"], [0.75, "#6b8580"], [1, "#2a3a39"]]);
      glow(1500, 120, 900, "rgba(220,240,220,.7)", 0.6);
      rays(1500, 60, "#e8f5e0", 28, 71, 1500, 1.2, Math.PI * 0.72);
      const r = rand(72);
      [[0.32, "#4d6765", 600, 22], [0.5, "#33504f", 720, 18], [0.7, "#1f3536", 860, 14], [1, "#0b1416", 1000, 9]].forEach(([k, col, base, n], li) => {
        for (let i = 0; i < n; i++) { const x = (i + r() * 0.8) * (W / n), h = (260 + r() * 260) * (0.7 + k * 0.9); if (li === 3 && Math.abs(x - 860) < 180) continue; pine(x, base + r() * 30, h, col); }
        ctx.fillStyle = col; ctx.fillRect(0, base + 20, W, H - base - 20);
        if (li < 3) haze(base - 160, base + 80, `rgba(190,215,205,${0.28 - li * 0.06})`);
      });
      ctx.fillStyle = lin(880, H, [[0, "#1b2726"], [1, "#05090a"]]); ctx.fillRect(0, 900, W, H - 900);
      ctx.fillStyle = "#3a4a46"; ctx.beginPath(); ctx.moveTo(820, 905); ctx.lineTo(900, 905); ctx.lineTo(1180, H); ctx.lineTo(560, H); ctx.closePath(); ctx.globalAlpha = 0.6; ctx.fill(); ctx.globalAlpha = 1;
      const { hand } = person(860, 960, 230, { pose: "lantern", fill: "#060a0b" });
      glow(hand[0], hand[1] + 8, 260, "rgba(255,190,110,.9)", 0.8); glow(hand[0], hand[1] + 8, 40, "rgba(255,240,200,1)", 1);
      ctx.fillStyle = "#ffe6b0"; ctx.fillRect(hand[0] - 6, hand[1] + 2, 12, 14);
      haze(820, 1000, "rgba(200,220,210,.18)");
      grade(73, 0.6, 9);
    },
    // an astronaut before a ringed planet: sci-fi
    space() {
      sky([[0, "#02030a"], [0.6, "#0a1028"], [1, "#151a35"]]);
      stars(81, 1400, H, 1);
      glow(1350, 380, 900, "rgba(90,110,255,.35)", 0.6);
      // the planet and its rings
      ctx.save(); ctx.translate(1340, 400); ctx.rotate(-0.32);
      ctx.strokeStyle = "rgba(220,200,255,.35)"; [[560, 120, 18], [520, 108, 6], [610, 132, 4]].forEach(([a, b, w]) => { ctx.lineWidth = w; ctx.beginPath(); ctx.ellipse(0, 0, a, b, 0, Math.PI, Math.PI * 2); ctx.stroke(); });
      ctx.restore();
      ctx.fillStyle = radial(1240, 320, 420, [[0, "#f3c6a0"], [0.45, "#c4637a"], [0.85, "#3a2160"], [1, "#160d2e"]]); ctx.beginPath(); ctx.arc(1340, 400, 330, 0, Math.PI * 2); ctx.fill();
      ctx.save(); ctx.beginPath(); ctx.arc(1340, 400, 330, 0, Math.PI * 2); ctx.clip(); const rb = rand(84); ctx.filter = "blur(6px)"; ctx.strokeStyle = "#fff"; for (let i = -7; i < 8; i++) { ctx.globalAlpha = 0.03 + rb() * 0.08; ctx.lineWidth = 6 + rb() * 26; ctx.beginPath(); ctx.ellipse(1340, 400 + i * 44 + rb() * 20, 440, 26, -0.32, 0, Math.PI * 2); ctx.stroke(); }
      ctx.globalAlpha = 0.55; ctx.filter = "none"; ctx.fillStyle = radial(1520, 560, 420, [[0, "rgba(0,0,0,0)"], [0.5, "rgba(10,5,30,.2)"], [1, "rgba(10,5,30,.9)"]]); ctx.fillRect(1000, 60, 700, 700); ctx.restore();
      ctx.save(); ctx.translate(1340, 400); ctx.rotate(-0.32); ctx.strokeStyle = "rgba(235,215,255,.55)";
      [[560, 120, 18], [520, 108, 6], [610, 132, 4]].forEach(([a, b, w]) => { ctx.lineWidth = w; ctx.beginPath(); ctx.ellipse(0, 0, a, b, 0, 0, Math.PI); ctx.stroke(); }); ctx.restore();
      ctx.fillStyle = radial(900, 900, 900, [[0, "rgba(0,0,0,0)"], [1, "rgba(0,0,0,0)"]]);
      // the rocky ground and the astronaut
      ridge({ y: 900, amp: 90, freq: 0.004, seed: 82, fill: "#1a1830", sharp: 0.6, edge: "rgba(160,150,255,.35)" });
      ridge({ y: 1030, amp: 120, freq: 0.0026, seed: 83, fill: "#0a0914", sharp: 0.5, edge: "rgba(200,170,255,.4)" });
      person(640, 935, 230, { pose: "astro", fill: "#08070f" });
      grade(85, 0.55, 8);
    },
    // a lit tent under the northern lights: nature, wonder
    aurora() {
      sky([[0, "#020812"], [0.5, "#06222e"], [0.8, "#0f3b45"], [1, "#0b1d26"]]);
      stars(91, 1100, 700, 1);
      // the aurora curtains
      ctx.save(); ctx.globalCompositeOperation = "screen"; ctx.filter = "blur(10px)";
      const n = noise1(92);
      for (let x = -40; x < W + 40; x += 3) { const base = 360 + Math.sin(x * 0.0032) * 120 + n(x * 0.004) * 80, h = 180 + n(x * 0.011 + 40) * 320, a = 0.08 + n(x * 0.02 + 9) * 0.25;
        const g = ctx.createLinearGradient(0, base - h, 0, base + 30); g.addColorStop(0, "rgba(160,80,255,0)"); g.addColorStop(0.45, `rgba(120,90,255,${a * 0.6})`); g.addColorStop(0.85, `rgba(70,255,170,${a})`); g.addColorStop(1, "rgba(70,255,170,0)");
        ctx.fillStyle = g; ctx.fillRect(x, base - h, 4, h + 30); }
      ctx.restore();
      ridge({ y: 760, amp: 260, freq: 0.0022, seed: 93, fill: "#203646", sharp: 0.7, edge: "rgba(200,240,255,.5)" }); haze(650, 800, "rgba(90,200,180,.18)");
      ridge({ y: 880, amp: 160, freq: 0.0019, seed: 94, fill: "#b9cddb", oct: 4 });
      ridge({ y: 880, amp: 160, freq: 0.0019, seed: 94, fill: lin(700, 1000, [[0, "rgba(40,70,90,.2)"], [1, "rgba(15,30,45,.9)"]]), oct: 4 });
      ctx.fillStyle = lin(900, H, [[0, "#6b8597"], [1, "#1b2833"]]); ctx.beginPath(); ctx.moveTo(0, 960); ctx.bezierCurveTo(600, 920, 1300, 950, 1960, 900); ctx.lineTo(1960, H); ctx.lineTo(0, H); ctx.closePath(); ctx.fill();
      // the tent, lit from inside, and its glow on the snow
      const tx = 1100, ty = 975;
      glow(tx, ty - 30, 340, "rgba(255,170,90,.8)", 0.7);
      ctx.fillStyle = "#ffb15e"; ctx.beginPath(); ctx.moveTo(tx - 110, ty); ctx.lineTo(tx, ty - 120); ctx.lineTo(tx + 110, ty); ctx.closePath(); ctx.fill();
      ctx.fillStyle = "#ffe0a8"; ctx.beginPath(); ctx.moveTo(tx - 22, ty); ctx.lineTo(tx, ty - 70); ctx.lineTo(tx + 22, ty); ctx.closePath(); ctx.fill();
      person(tx - 220, ty + 6, 170, { pose: "stand", fill: "#0b1219", face: 1 });
      grade(95, 0.5, 8);
    },
  };

  const s = new URLSearchParams(location.search).get("s") || "dawn";
  SCENES[s]();
  window.SCENES = Object.keys(SCENES);
  window.done = true;
})();
