// Video ads for the brief campaign, in the same style as brief.js, driven frame by frame:
// record.cjs calls window.seek(t) and screenshots #stage.
//   brief-anim.html?v=ad0-S | ad0-V   Ad 0, 12 s: the story arc draws over a real frame, generic AI vs
//                                     Vionlabs reading, mood tags, the 1M+ library, end card.
//   brief-anim.html?v=ad3-S | ad3-V   Ad 3, 8 s: the playhead scrubs an episode and markers snap in.
//   brief-anim.html?v=v1-S … v4-V     The video series modelled on the TwelveLabs references: search by mood,
//                                     ad breaks, shorts, thumbnail recipes (about 21 s each).
(function () {
  const V = new URLSearchParams(location.search).get("v") || "ad0-S";
  const vertical = V.endsWith("-V");
  const W = 1080, H = vertical ? 1920 : 1080, PAD = 72;
  const KEY = V.split("-")[0];
  const DUR = { ad0: 12, ad3: 8, v1: 21, v2: 21.5, v3: 22, v4: 21.5 }[KEY];
  // poster: the frame the review page shows before play
  const POSTER = { ad0: 5.7, ad3: 7.2, v1: 15.9, v2: 15.4, v3: 15.9, v4: 11.2 }[KEY];
  window.VIDEO = { id: V, w: W, h: H, duration: DUR, fps: 30, poster: POSTER };

  const clamp = (x) => Math.max(0, Math.min(1, x));
  const ease = (x) => { x = clamp(x); return x < 0.5 ? 4 * x * x * x : 1 - Math.pow(-2 * x + 2, 3) / 2; };
  const span = (t, a, b) => ease((t - a) / (b - a));
  const popIn = (node, t, a, from = 0.85) => { const k = clamp((t - a) / 0.3); node.style.opacity = k; node.style.transform = `scale(${from + (1 - from) * ease(k) + (k > 0 && k < 1 ? 0.05 * Math.sin(k * Math.PI) : 0)})`; };
  const rise = (node, t, a, b, out = 0) => { const k = span(t, a, b); node.style.opacity = k * (1 - out); node.style.transform = `translateY(${(1 - k) * 22}px)`; };

  const stage = document.createElement("section");
  stage.id = "stage";
  stage.className = `ad ${vertical ? "V" : "S"}`;
  stage.style.padding = "0";
  document.body.appendChild(stage);
  const el = (html) => { const t = document.createElement("template"); t.innerHTML = html.trim(); const n = t.content.firstChild; stage.appendChild(n); return n; };
  const pic = (name, css, pos = "50% 50%", extra = "") => `<div class="frame" style="${css}"><img src="img/${name}.jpg" alt="" style="position:absolute;inset:0;width:100%;height:100%;object-fit:cover;object-position:${pos}">${extra}</div>`;
  const topBar = (aud) => el(`<div class="top abs" style="left:${PAD}px;right:${PAD}px;top:${vertical ? 96 : 64}px;z-index:8"><img class="wordmark" src="logo/vionlabs-white.png" alt="Vionlabs"><span class="eyebrow"><b></b>${aud}</span></div>`);
  const footer = () => el(`<div class="foot" style="opacity:0"><span class="cta">Book a demo</span><span class="signoff">AI built for entertainment.</span></div>`);

  // the story arc, same curve and beats as the stills
  const ARC = [[0, 0.82], [0.12, 0.78], [0.31, 0.5], [0.5, 0.7], [0.73, 0.18], [0.9, 0.62], [1, 0.68]];
  const BEATS = [[1, "Setup"], [2, "Rising tension"], [3, "Turning point"], [4, "Climax"], [5, "Resolution"]];
  function curve(pts, w, h) {
    const P = pts.map(([x, y]) => [x * w, y * h]);
    let d = `M${P[0][0]} ${P[0][1]}`;
    for (let i = 0; i < P.length - 1; i++) {
      const p0 = P[i - 1] || P[i], p1 = P[i], p2 = P[i + 1], p3 = P[i + 2] || p2;
      d += ` C${p1[0] + (p2[0] - p0[0]) / 6} ${p1[1] + (p2[1] - p0[1]) / 6} ${p2[0] - (p3[0] - p1[0]) / 6} ${p2[1] - (p3[1] - p1[1]) / 6} ${p2[0]} ${p2[1]}`;
    }
    return { d, P };
  }

  let seek;

  if (V.startsWith("ad0")) {
    const fh = vertical ? 900 : 700, arcTop = vertical ? 470 : 330, arcH = vertical ? 280 : 240, fs = vertical ? 17 : 15;
    const frame = el(`<div class="abs" style="left:0;top:0;width:${W}px;height:${fh}px;transform-origin:50% 40%">
      ${pic("r-shaw", `position:absolute;inset:0;border-radius:0`, "50% 30%")}
      <div class="abs" style="inset:0;background:linear-gradient(0deg,var(--bg) 0%,rgba(11,19,28,0) 42%),linear-gradient(180deg,rgba(11,19,28,.8) 0%,rgba(11,19,28,0) 24%)"></div></div>`);
    const bar = topBar("For streamers & broadcasters");
    const { d, P } = curve(ARC, W, arcH);
    const arcSvg = el(`<svg class="abs" style="left:0;top:${arcTop}px;overflow:visible" width="${W}" height="${arcH}">
      <defs><filter id="ag"><feGaussianBlur stdDeviation="6"/></filter><clipPath id="ac"><rect id="acr" x="0" y="-300" width="0" height="${arcH + 600}"/></clipPath></defs>
      <g clip-path="url(#ac)"><path d="${d}" fill="none" stroke="#e07a6d" stroke-width="9" opacity=".5" filter="url(#ag)"/><path d="${d}" fill="none" stroke="#f0907f" stroke-width="3.5" stroke-linecap="round"/></g>
      ${BEATS.map(([i, t]) => `<g class="beat" data-x="${P[i][0] / W}" opacity="0"><circle cx="${P[i][0]}" cy="${P[i][1]}" r="6" fill="#e07a6d"/><circle cx="${P[i][0]}" cy="${P[i][1]}" r="13" fill="#e07a6d" opacity=".25"/>
        <text x="${P[i][0]}" y="${P[i][1] - fs * 1.4}" text-anchor="middle" font-family="Inter" font-size="${fs}" font-weight="700" letter-spacing="1.4" fill="#fff" style="paint-order:stroke" stroke="rgba(0,0,0,.55)" stroke-width="3">${t.toUpperCase()}</text></g>`).join("")}</svg>`);

    // generic AI vs Vionlabs, as on the a0-S still
    const rowTop = vertical ? 980 : 760, rowFs = vertical ? 46 : 44, labW = vertical ? 230 : 210;
    const row = (lab, text, y, col) => el(`<div class="abs row" style="left:${PAD}px;right:${PAD}px;top:${y}px;align-items:baseline;gap:0;opacity:0">
      <span style="width:${labW}px;flex:none;font-size:${vertical ? 21 : 19}px;font-weight:600;letter-spacing:.12em;color:${col}">${lab}</span>
      <span style="font-family:'Inter Display','Inter';font-weight:600;letter-spacing:-0.02em;font-size:${rowFs}px;line-height:1.15">${text}</span></div>`);
    const generic = row("GENERIC AI", '<span style="color:var(--muted)">two men, wall, sitting.</span>', rowTop, "var(--muted)");
    const rule = el(`<div class="abs" style="left:${PAD}px;right:${PAD}px;top:${rowTop + rowFs * 1.6}px;height:1px;background:var(--panel-edge);opacity:0"></div>`);
    const ours = row("VIONLABS", 'the moment <span style="color:var(--blue-hi)">hope comes back.</span>', rowTop + rowFs * 2.1, "var(--sky)");
    const tagRow = el(`<div class="abs row" style="left:${PAD}px;top:${vertical ? rowTop + rowFs * 4 : arcTop + 260}px;gap:12px;flex-wrap:wrap;width:${W - 2 * PAD}px">
      ${["Mood: Hopeful", "Scene: Prison yard, day", "Emotion: Anticipation"].map((t) => `<span class="tag mood" style="font-size:${vertical ? 26 : 21}px;padding:9px 18px;opacity:0;transform-origin:left center">${t}</span>`).join("")}</div>`);
    const tags = [...tagRow.children];
    // vertical has room for the brief's Ad 0 headline under the frame
    const claim = vertical ? el(`<h1 class="abs" style="left:${PAD}px;top:1370px;width:${W - 2 * PAD}px;font-size:96px;opacity:0">Generic AI sees pixels. <span class="hl">Ours understands stories.</span></h1>`) : null;

    // the library: real title thumbnails from the website
    const TILES = ["shaw", "skyfall", "glad", "lala", "zoo", "argo", "forrest", "peaky", "troy", "ticket", "wick-2", "king", "vacation", "reacher", "north", "pap",
      "suc", "secret", "any", "kingdom", "brave", "samurai", "friday", "candy"];
    const cols = vertical ? 4 : 6, gw = W - 2 * PAD, gap = 12, cw = (gw - (cols - 1) * gap) / cols, ch = cw * 9 / 16, gTop = vertical ? 580 : 432;
    const libHead = el(`<h1 class="abs" style="left:${PAD}px;top:${vertical ? 260 : 150}px;width:${gw}px;font-size:${vertical ? 88 : 80}px;opacity:0">Our own models. <span class="hl">Trained on 1M+ entertainment assets.</span></h1>`);
    const grid = el(`<div class="abs" style="left:${PAD}px;top:${gTop}px;display:grid;grid-template-columns:repeat(${cols},${cw}px);gap:${gap}px">
      ${TILES.map((t) => pic(`t-${t}`, `width:${cw}px;height:${ch}px;border-radius:8px;opacity:0`)).join("")}</div>`);
    const tiles = [...grid.children];
    const libSub = el(`<div class="abs sub" style="left:${PAD}px;top:${gTop + (ch + gap) * (TILES.length / cols) + 18}px;font-size:${vertical ? 30 : 26}px;opacity:0">Mood, emotion and story arc. Scene by scene, since 2019.</div>`);

    // end card
    const end = el(`<div class="abs" style="inset:0;background:var(--bg);opacity:0">
      <div class="glow" style="width:800px;height:600px;left:140px;top:${H / 2 - 300}px;background:rgba(51,96,208,.32)"></div>
      <div class="abs col" style="left:0;right:0;top:${H / 2 - (vertical ? 170 : 150)}px;align-items:center;gap:${vertical ? 34 : 28}px">
        <img src="logo/vionlabs-white.png" alt="Vionlabs" style="height:${vertical ? 62 : 54}px">
        <div style="font-family:'Inter Display','Inter';font-weight:700;letter-spacing:-0.035em;font-size:${vertical ? 72 : 64}px">AI built for <span style="color:var(--blue-hi)">entertainment.</span></div>
        <span class="cta" style="margin-top:${vertical ? 30 : 22}px">Book a demo</span></div></div>`);
    const cr = document.getElementById("acr");
    const beats = [...stage.querySelectorAll(".beat")];

    seek = (t) => {
      const out = span(t, 6.0, 6.8);
      frame.style.opacity = span(t, 0, 0.6) * (1 - out);
      frame.style.transform = `scale(${1 + 0.05 * clamp(t / 6.8)})`;
      bar.style.opacity = span(t, 0.2, 0.8) * (1 - span(t, 9.6, 10.2));
      const draw = span(t, 0.6, 3.6);
      cr.setAttribute("width", W * draw);
      arcSvg.style.opacity = 1 - out;
      beats.forEach((b) => b.setAttribute("opacity", clamp((draw - (+b.dataset.x - 0.02)) / 0.06)));
      rise(generic, t, 1.4, 2.0, out);
      rule.style.opacity = span(t, 2.6, 3.0) * (1 - out);
      rise(ours, t, 3.0, 3.6, out);
      tags.forEach((g, i) => { popIn(g, t, 3.9 + i * 0.3); g.style.opacity = +g.style.opacity * (1 - out); });
      if (claim) rise(claim, t, 4.7, 5.3, out);
      const libOut = span(t, 9.5, 10.1);
      rise(libHead, t, 6.5, 7.1, libOut);
      tiles.forEach((n, i) => { const k = span(t, 6.6 + i * 0.07, 7.0 + i * 0.07); n.style.opacity = k * (1 - libOut); n.style.transform = `scale(${0.86 + 0.14 * k})`; });
      rise(libSub, t, 8.4, 8.9, libOut);
      end.style.opacity = span(t, 9.8, 10.4);
    };
  }

  if (V.startsWith("ad3")) {
    const EP = 43 * 60, T = (tc) => { const [m, s] = tc.split(":").map(Number); return (m * 60 + s) / EP; };
    const fmt = (s) => `${String(Math.floor(s / 60)).padStart(2, "0")}:${String(Math.floor(s % 60)).padStart(2, "0")}`;
    const pw = W - 2 * PAD, ph = vertical ? 620 : 340, pTop = vertical ? 640 : 362, fs = 17;
    const tlTop = pTop + ph + (vertical ? 90 : 64), tlH = vertical ? 56 : 44;
    topBar("For content ops teams");
    const head = el(`<h1 class="abs" style="left:${PAD}px;top:${vertical ? 270 : 160}px;width:${pw}px;font-size:${vertical ? 96 : 80}px;opacity:0">Every second of your library, <span class="hl">time-coded.</span></h1>`);
    el(pic("r-peaky", `position:absolute;left:${PAD}px;top:${pTop}px;width:${pw}px;height:${ph}px`, "50% 35%", `
      <div class="abs tc" style="left:16px;top:14px;font-size:${fs - 2}px;letter-spacing:.06em;color:rgba(255,255,255,.9);text-shadow:0 1px 6px #000">S1 E4 · 43:00</div>
      <div class="abs" style="left:0;right:0;bottom:0;height:70px;background:linear-gradient(0deg,rgba(0,0,0,.7),transparent)"></div>
      <div class="abs row" style="left:16px;right:16px;bottom:14px;align-items:center;gap:12px"><span style="color:#fff;font-size:${fs + 2}px">▶</span>
        <div style="flex:1;height:4px;border-radius:2px;background:rgba(255,255,255,.3)"><div id="prog" style="width:0;height:4px;border-radius:2px;background:#fff"></div></div>
        <span class="tc" id="tc" style="color:#fff;font-size:${fs - 1}px">00:00 / 43:00</span></div>`));
    const skip = el(`<span class="abs" style="right:${PAD + 18}px;top:${pTop + ph - 56 - 44}px;background:rgba(255,255,255,.94);color:#0b131c;font-weight:600;font-size:${fs + 4}px;padding:10px 18px;border-radius:10px;opacity:0">Skip Intro ⏭</span>`);
    el(`<div class="abs timeline" style="left:${PAD}px;top:${tlTop}px;width:${pw}px;height:${tlH}px"></div>`);
    const MARKS = [
      { at: "00:00", end: "01:12", label: "RECAP 00:00–01:12", col: "#3360d0" },
      { at: "01:12", end: "02:05", label: "INTRO 01:12–02:05", col: "#5a7fe0" },
      { at: "14:37", label: "AD BREAK 14:37", col: "#e07a6d" },
      { at: "28:51", label: "AD BREAK 28:51", col: "#e07a6d" },
      { at: "41:20", end: "43:00", label: "CREDITS 41:20", col: "#3360d0" },
    ];
    const labFs = vertical ? 21 : 16;
    const legend = el(`<div class="abs row tc" style="left:${PAD}px;top:${tlTop + tlH + (vertical ? 34 : 26)}px;width:${pw}px;gap:${vertical ? 14 : 18}px ${vertical ? 26 : 18}px;flex-wrap:wrap;font-size:${labFs}px"></div>`);
    const nodes = MARKS.map((m) => {
      const x = PAD + pw * T(m.at), w = m.end ? Math.max(10, pw * (T(m.end) - T(m.at))) : 6;
      const bar = el(`<div class="abs" style="left:${m.end ? x : x - 3}px;top:${tlTop - (m.end ? 0 : 10)}px;width:${w}px;height:${m.end ? tlH : tlH + 20}px;border-radius:${m.end ? 6 : 3}px;background:${m.col};box-shadow:0 0 14px ${m.col};opacity:0;transform-origin:50% 100%"></div>`);
      const lab = document.createElement("span");
      lab.textContent = m.label;
      lab.style.cssText = `color:${m.col === "#e07a6d" ? "#f0907f" : "#c7cfdc"};opacity:0`;
      legend.appendChild(lab);
      return { m, bar, lab };
    });
    const playhead = el(`<div class="abs" style="left:${PAD}px;top:${tlTop - 14}px;width:3px;height:${tlH + 28}px;background:#fff;box-shadow:0 0 12px rgba(255,255,255,.8)"></div>`);
    const foot = footer();
    const prog = document.getElementById("prog"), tc = document.getElementById("tc");

    seek = (t) => {
      rise(head, t, 0, 0.5);
      const p = span(t, 0.6, 5.6);
      playhead.style.left = `${PAD + pw * p - 1.5}px`;
      prog.style.width = `${p * 100}%`;
      tc.textContent = `${fmt(p * EP)} / 43:00`;
      nodes.forEach(({ m, bar, lab }) => {
        const since = T(m.at) <= p + 0.0001 ? clamp((p - T(m.at)) / 0.04) : 0;
        bar.style.opacity = since; lab.style.opacity = since;
        bar.style.transform = `scaleY(${0.4 + 0.6 * ease(since)})`;
      });
      skip.style.opacity = p > T("01:12") && p < T("02:30") ? 1 : 0;
      foot.style.opacity = span(t, 5.9, 6.5);
    };
  }

  // ======================================================================== video series
  // Four videos that borrow the storytelling and motion of the TwelveLabs references
  // (../references/twelvelabs-videos.md): open on the felt problem, one line of text at a time, the click
  // that solves it, and lots of screens in motion (blurred screens behind the main window, a rushing wall of
  // results, a camera that pulls back over a whole canvas of cards). Each video is about a different Vionlabs
  // product, in our own style, and ends on a line the wordmark completes.
  const MY = vertical ? 1010 : 580, TOP = vertical ? 250 : 150, CW = W - 2 * PAD;
  const vis = (t, a, b, c = 1e9, d = 1e9) => span(t, a, b) * (1 - span(t, c, d));
  const typed = (t, a, b, text) => text.slice(0, Math.round(text.length * clamp((t - a) / (b - a))));
  const kb = (node, t, a, b, s0 = 1, s1 = 1.08) => { node.querySelector("img").style.transform = `scale(${s0 + (s1 - s0) * clamp((t - a) / (b - a))})`; };
  const zoomTo = (t, a, b, s0, s1) => s0 * Math.pow(s1 / s0, span(t, a, b)); // camera zoom feels even when interpolated in log space
  const rand = (seed) => () => (seed = (seed * 16807) % 2147483647) / 2147483647; // seeded, so every render is identical
  const add = (parent, html) => { const tp = document.createElement("template"); tp.innerHTML = html.trim(); const n = tp.content.firstChild; parent.appendChild(n); return n; };
  // a scene is a full-stage layer that fades and zooms through as one
  const layer = (html = "", z = 0) => el(`<div class="abs" style="inset:0;opacity:0;visibility:hidden;transform-origin:${W / 2}px ${MY}px${z ? `;z-index:${z}` : ""}">${html}</div>`);
  const scene = (node, t, a, b, c = 1e9, d = 1e9) => {
    const i = span(t, a, b), o = span(t, c, d), v = i * (1 - o);
    node.style.opacity = v; node.style.visibility = v > 0.001 ? "visible" : "hidden";
    node.style.transform = `scale(${(0.93 + 0.07 * i) * (1 + 0.14 * o)})`;
  };
  const say = (html) => el(`<h1 class="abs" style="left:${PAD}px;right:${PAD}px;top:0;height:${H}px;display:flex;align-items:center;justify-content:center;text-align:center;font-size:${vertical ? 92 : 80}px;opacity:0"><span style="text-wrap:balance;max-width:100%">${html}</span></h1>`);
  const sayAt = (node, t, a, b) => { node.style.opacity = vis(t, a, a + 0.45, b - 0.3, b); node.style.transform = `translateY(${(1 - span(t, a, a + 0.45)) * 24}px) scale(${1 + 0.04 * clamp((t - a) / (b - a))})`; };
  const searchBox = (h, fs, go, q = "") => `<div class="search" style="height:${h}px;padding:0 ${h * 0.28}px"><span style="font-size:${fs * 1.15}px;color:var(--blue)">⌕</span><span class="q" style="font-size:${fs}px">${q}</span><span class="caret"></span>${go ? `<span class="go" style="font-size:${fs * 0.68}px;padding:${h * 0.14}px ${h * 0.24}px">${go}</span>` : ""}</div>`;
  const glowRing = "0 0 0 3px rgba(61,155,255,.6), 0 0 70px rgba(61,155,255,.45), 0 20px 60px rgba(0,0,0,.45)";
  const tagsHtml = (list, cls, fs) => list.map((x) => `<span class="tag ${cls}" style="font-size:${fs}px;padding:${fs * 0.3}px ${fs * 0.7}px">${x}</span>`).join("");
  function endCard(lead) {
    const node = el(`<div class="abs" style="inset:0;background:var(--bg);opacity:0;z-index:30;isolation:isolate">
      <div class="glow" style="width:800px;height:600px;left:140px;top:${H / 2 - 300}px;background:rgba(51,96,208,.3)"></div>
      <div class="abs col" style="left:${PAD}px;right:${PAD}px;top:${H / 2 - (vertical ? 230 : 200)}px;align-items:center;text-align:center;gap:${vertical ? 34 : 28}px">
        <div style="font-family:'Inter Display','Inter';font-weight:700;letter-spacing:-0.035em;line-height:1.05;font-size:${vertical ? 76 : 64}px;text-wrap:balance">${lead}</div>
        <img class="mark" src="logo/vionlabs-white.png" alt="Vionlabs" style="height:${vertical ? 64 : 56}px;opacity:0">
        <div class="so" style="font-size:${vertical ? 32 : 28}px;color:var(--muted);opacity:0">AI built for entertainment.</div>
        <span class="cta" style="margin-top:${vertical ? 20 : 14}px;opacity:0">Book a demo</span></div></div>`);
    const [mark, so, cta] = ["mark", "so", "cta"].map((c) => node.querySelector("." + c));
    return (t, a) => { node.style.opacity = span(t, a, a + 0.5); popIn(mark, t, a + 0.9, 0.7); rise(so, t, a + 1.5, a + 2.0); rise(cta, t, a + 1.9, a + 2.4); };
  }
  function makeCursor() {
    const ripple = el(`<div class="abs" style="left:0;top:0;width:60px;height:60px;margin:-30px 0 0 -30px;border-radius:50%;border:3px solid var(--sky);opacity:0;z-index:21"></div>`);
    const arrow = el(`<svg class="abs" width="34" height="42" viewBox="0 0 34 42" style="left:0;top:0;opacity:0;z-index:22;filter:drop-shadow(0 4px 10px rgba(0,0,0,.6))"><path d="M3 2 L3 34 L11 26 L17 40 L23 37 L17 24 L29 24 Z" fill="#fff" stroke="#0b131c" stroke-width="2.5" stroke-linejoin="round"/></svg>`);
    // path: [[time, x, y], ...]; clicks: times
    return (t, path, clicks = []) => {
      let [, x, y] = path[0];
      for (let i = 0; i < path.length - 1; i++) {
        const [t0, x0, y0] = path[i], [t1, x1, y1] = path[i + 1];
        if (t >= t0) { const k = ease((t - t0) / (t1 - t0)); x = x0 + (x1 - x0) * k; y = y0 + (y1 - y0) * k; }
      }
      const a = path[0][0], b = path[path.length - 1][0];
      arrow.style.opacity = vis(t, a, a + 0.25, b + 0.2, b + 0.45);
      arrow.style.transform = `translate(${x}px,${y}px)`;
      const c = clicks.find((c) => t >= c && t < c + 0.45);
      ripple.style.opacity = c === undefined ? 0 : 1 - (t - c) / 0.45;
      ripple.style.transform = `translate(${x}px,${y}px) scale(${c === undefined ? 0 : 0.35 + (t - c) / 0.45})`;
    };
  }
  const phoneHtml = (w, name, pos, caption) => `<div style="width:${w}px;height:${w * 16 / 9 + 20}px;border-radius:${w * 0.13}px;background:#05080c;padding:10px;box-shadow:0 30px 80px rgba(0,0,0,.6);border:1.5px solid var(--panel-edge)">
    ${pic(name, `position:relative;width:100%;height:100%;border-radius:${w * 0.1}px`, pos, `<div class="abs" style="left:0;right:0;bottom:0;height:40%;background:linear-gradient(0deg,rgba(0,0,0,.75),transparent)"></div>
      <div class="abs" style="left:${w * 0.07}px;right:${w * 0.07}px;bottom:${w * 0.08}px;font-size:${w * 0.055}px;line-height:1.35;color:#fff"><b>@yourchannel</b><br>${caption}</div>`)}</div>`;

  // blurred screens drifting behind the main window, for depth
  function floatHtml(names, seed) {
    const r = rand(seed);
    return names.map((n) => {
      const w = (vertical ? 320 : 270) + r() * 200, h = w * 9 / 16, x = r() * (W + 160) - 80 - w / 2, y = (vertical ? 160 : 90) + r() * (H - (vertical ? 320 : 180)) - h / 2;
      return pic(n, `position:absolute;left:${x}px;top:${y}px;width:${w}px;height:${h}px;border-radius:16px;filter:blur(${3 + r() * 4}px) brightness(.7);opacity:${0.35 + r() * 0.25}`, "50% 40%")
        .replace('class="frame"', `class="frame fl" data-vx="${(r() - 0.5) * 50}" data-vy="${(r() - 0.5) * 36}"`);
    }).join("");
  }
  const drift = (node, t) => node.querySelectorAll(".fl").forEach((f) => (f.style.transform = `translate(${f.dataset.vx * t}px,${f.dataset.vy * t}px)`));

  // a wall of rounded thumbnails, tilted in 3D, that rushes past the camera
  function wall(names, { cols, tw, gap = 18, radius = 34, rx = 16, rz = -9, extra = () => "", label = "" }) {
    const th = tw * 9 / 16, rows = Math.ceil(names.length / cols), ww = cols * tw + (cols - 1) * gap, wh = rows * th + (rows - 1) * gap;
    const node = layer(`<div class="wl abs" style="left:0;top:0;width:${ww}px;height:${wh}px;transform-origin:0 0">${names.map((n, i) => pic(n, `position:absolute;left:${(i % cols) * (tw + gap)}px;top:${Math.floor(i / cols) * (th + gap)}px;width:${tw}px;height:${th}px;border-radius:${radius}px`, "50% 40%", extra(i))).join("")}</div>
      <div class="abs" style="inset:0;background:radial-gradient(ellipse 80% 72% at 50% ${(MY / H) * 100}%, transparent 50%, rgba(11,19,28,.9) 100%)"></div>
      ${label ? `<div class="abs tc" style="left:50%;top:${vertical ? 200 : 120}px;transform:translateX(-50%);white-space:nowrap;font-size:${vertical ? 21 : 18}px;letter-spacing:.12em;color:#c7cfdc;background:rgba(11,19,28,.85);border:1.5px solid var(--panel-edge);padding:10px 18px;border-radius:999px">${label}</div>` : ""}`);
    const wl = node.querySelector(".wl");
    node.move = (dx, dy) => (wl.style.transform = `translate(${W / 2}px,${MY}px) perspective(2000px) rotateX(${rx}deg) rotateZ(${rz}deg) translate(${-ww / 2 + dx}px,${-wh / 2 + dy}px)`);
    node.label = node.querySelector(".tc");
    return node;
  }
  const mix = (pool, n, cols) => Array.from({ length: n }, (_, i) => pool[(i + Math.floor(i / cols) * 4) % pool.length]); // no neighbours repeat

  // a canvas of cards that the camera pulls back over; the nearest spots go to the first items
  function spots(cols, rows, dx, dy) {
    const out = [], mc = (cols - 1) / 2, mr = (rows - 1) / 2;
    for (let c = 0; c < cols; c++) for (let r = 0; r < rows; r++) out.push([(c - mc) * dx, (r - mr) * dy + (Math.abs(c - mc) % 2 === 1 ? dy / 2 : 0)]);
    return out.sort((a, b) => Math.hypot(a[0], a[1]) - Math.hypot(b[0], b[1]));
  }
  function canvas(items, { cols, rows, dx, dy, cw, ch }) {
    const pos = spots(cols, rows, dx, dy);
    const node = layer(`<div class="wd abs" style="left:0;top:0;transform-origin:0 0">${items.map((html, i) => { const [x, y] = pos[i]; const far = Math.hypot(x / dx, y / dy) > 1.7;
        return `<div class="abs cv" style="left:${x - cw / 2}px;top:${y - ch / 2}px;width:${cw}px;${far ? "filter:blur(1.5px);opacity:.7" : ""}">${html}</div>`; }).join("")}</div>
      <div class="abs" style="inset:0;background:radial-gradient(ellipse ${vertical ? "85% 64%" : "74% 74%"} at 50% ${(MY / H) * 100}%, transparent 42%, var(--bg) 97%)"></div>`);
    const wd = node.querySelector(".wd"), imgs = [...node.querySelectorAll(".cv img")];
    node.cam = (x, y, s, t) => {
      wd.style.transform = `translate(${W / 2}px,${MY}px) scale(${s}) translate(${-x}px,${-y}px)`;
      imgs.forEach((im, i) => (im.style.transform = `scale(${1.05 + 0.04 * Math.sin(t * 0.9 + i * 1.7)})`)); // every card keeps playing
    };
    return node;
  }

  // ---------------------------------------------------------------- v1: search by mood (from the favourite, DAM search)
  if (V.startsWith("v1")) {
    topBar("For editorial & search teams");
    const cursor = makeCursor();
    const ROWS = [["ticket", "Ticket to Paradise", "Comedy"], ["skyfall", "Skyfall", "Action"], ["vacation", "Vacation Friends", "Comedy"], ["lala", "La La Land", "Musical"],
      ["glad", "Gladiator", "Action"], ["zoo", "We Bought a Zoo", "Drama"], ["argo", "Argo", "Thriller"], ["any", "Anyone But You", "Comedy"], ["forrest", "Forrest Gump", "Drama"],
      ["king", "King Richard", "Drama"], ["women", "What Women Want", "Comedy"], ["troy", "Troy", "Action"], ["american", "American Wedding", "Comedy"], ["shaolin", "Shaolin Soccer", "Comedy"],
      ["brave", "Braveheart", "Drama"], ["reacher", "Reacher", "Action"]];
    const rowH = vertical ? 108 : 94, th = vertical ? 80 : 68, tw = th * 16 / 9, fsR = vertical ? 27 : 24, boxW = vertical ? CW : 860, boxH = vertical ? 1300 : 760;
    const cols = `${tw}px 1fr ${vertical ? 190 : 160}px ${vertical ? 150 : 120}px`;
    // A: the catalogue, thin metadata, with screens floating behind it
    const A = layer(floatHtml(["r-skyfall", "r-glad", "r-lala", "r-peaky", "r-zoo", "r-argo", "r-troy", "r-king", "r-suc"], 7) + `
      <div class="ui tbl" style="left:${(W - boxW) / 2}px;top:${TOP + (vertical ? 120 : 30)}px;width:${boxW}px;height:${boxH}px">
      <div class="ui-bar"><span>Catalogue</span><span class="ctx">All titles · keyword search</span></div>
      <div class="panel-title" style="display:grid;grid-template-columns:${cols};gap:22px;align-items:center;height:50px;padding:0 22px;border-bottom:1px solid var(--panel-edge);background:#0c131c"><span></span><span style="font-size:17px">Title</span><span style="font-size:17px">Genre</span><span style="font-size:17px">Mood</span></div>
      <div style="position:absolute;left:0;right:0;top:100px;bottom:0;overflow:hidden"><div class="rows">${[...ROWS, ...ROWS].map(([t, name, g]) => `<div style="display:grid;grid-template-columns:${cols};gap:22px;align-items:center;height:${rowH}px;padding:0 22px;border-bottom:1px solid var(--panel-edge)">
        ${pic(`t-${t}`, `position:relative;width:${tw}px;height:${th}px;border-radius:6px`)}<span style="font-size:${fsR}px;font-weight:600">${name}</span><span style="font-size:${fsR - 2}px;color:var(--muted)">${g}</span><span style="font-size:${fsR}px;color:var(--faint)">—</span></div>`).join("")}</div></div></div>`);
    const tbl = A.querySelector(".tbl"), rows = A.querySelector(".rows");
    // B: the keyword search fails
    const Q = "feel-good movie with a happy ending", kwH = vertical ? 104 : 92;
    const B = layer(`<div class="abs kw" style="left:${PAD}px;right:${PAD}px;top:${MY - kwH / 2 - 40}px;height:${kwH}px;display:flex;align-items:center;gap:16px;padding:0 26px;background:#1a2433;border:1.5px solid var(--panel-edge);border-radius:16px">
        <span style="color:var(--faint);font-size:32px">⌕</span><span class="q" style="font-size:${vertical ? 33 : 30}px;color:#c7cfdc;white-space:nowrap"></span><span style="width:3px;height:42px;background:var(--muted)"></span>
        <span style="margin-left:auto;font-size:${vertical ? 20 : 18}px;color:var(--muted);padding:9px 16px;border:1.5px solid var(--panel-edge);border-radius:10px;white-space:nowrap">Keyword search</span></div>
      <div class="abs col none" style="left:0;right:0;top:${MY + 70}px;align-items:center;gap:14px"><div style="font-family:'Inter Display','Inter';font-weight:600;letter-spacing:-0.02em;font-size:${vertical ? 60 : 52}px;color:var(--muted)">No results found</div><div class="tc" style="font-size:${vertical ? 21 : 19}px;color:var(--faint)">matched on title and genre</div></div>`);
    const kw = B.querySelector(".kw"), none = B.querySelector(".none");
    // C: a wall of feel-good titles rushes in behind the Vionlabs search
    const POOL = ["t-ticket", "r-vacation", "t-any", "r-zoo", "t-women", "r-american", "t-king", "r-shaolin", "t-gethard", "r-ticket", "t-vacation", "r-any", "t-zoo", "r-women", "t-american", "r-king", "t-shaolin"];
    const wc = vertical ? 6 : 7, wr = vertical ? 13 : 8;
    const C = wall(mix(POOL, wc * wr, wc), { cols: wc, tw: vertical ? 330 : 300 });
    const sH = vertical ? 112 : 100, sTop = MY - sH / 2 - 40, T1 = vertical ? 400 : TOP;
    const S1 = layer(`<div class="abs vs" style="left:${PAD}px;right:${PAD}px;top:${sTop}px">${searchBox(sH, vertical ? 34 : 31, "Search")}</div>`, 6);
    const vs = S1.querySelector(".vs"); vs.firstChild.style.boxShadow = glowRing;
    // D: an empty player, a row of results, a click, and the title plays with its moods
    const dTop = T1 + sH + (vertical ? 50 : 30), dH = vertical ? 527 : 400, rw = vertical ? 300 : 230, rTop = dTop + dH + (vertical ? 190 : 140);
    const RROW = ["ticket", "vacation", "any", "zoo", "women", "american", "king", "shaolin", "gethard"];
    const D = layer(`<div class="abs" style="left:${PAD}px;top:${dTop}px;width:${CW}px;height:${dH}px;border-radius:18px;background:#141e2b;border:1.5px solid var(--panel-edge)"></div>
      <div class="abs big" style="left:${PAD}px;top:${dTop}px;width:${CW}px;opacity:0">${pic("r-ticket", `position:relative;width:${CW}px;height:${dH}px;border-radius:18px`, "50% 35%")}
        <div class="row" style="align-items:center;gap:14px;margin-top:18px;flex-wrap:wrap"><span style="font-family:'Inter Display','Inter';font-weight:700;font-size:${vertical ? 40 : 34}px;letter-spacing:-0.02em">Ticket to Paradise</span>
        ${tagsHtml(["Feel-good", "Romantic", "Happy ending"], "mood", vertical ? 23 : 20)}</div></div>
      <div class="abs row rrow" style="left:${PAD}px;top:${rTop}px;gap:16px">${RROW.map((n) => pic(`t-${n}`, `position:relative;flex:none;width:${rw}px;height:${rw * 9 / 16}px;border-radius:14px`)).join("")}</div>`);
    const big = D.querySelector(".big"), rrow = D.querySelector(".rrow");
    // E: the camera pulls back over a canvas of searches, each with its match
    const QS = [["feel-good movie with a happy ending", "r-ticket", ["Feel-good", "Happy ending"]], ["underdog stories", "t-king", ["Uplifting"]], ["epic sword fights", "r-glad", ["Epic"]],
      ["tense true stories", "t-argo", ["Tense"]], ["bittersweet endings", "t-forrest", ["Bittersweet"]], ["cozy family movies", "t-zoo", ["Heartwarming"]], ["feel-good romcoms", "t-any", ["Romantic"]],
      ["prison escape stories", "t-pap", ["Tense"]], ["survival against the odds", "t-rescue", ["Gripping"]], ["spy thrillers", "t-spy", ["Suspense"]], ["road trip comedies", "t-fanboys", ["Funny"]],
      ["Vikings and revenge", "t-north", ["Intense"]], ["kung fu comedies", "t-shaolin", ["Funny"]], ["bittersweet romance", "t-lala", ["Bittersweet"]], ["relentless action", "t-wick-2", ["Intense"]]];
    const cw = 320, chh = 54 + 12 + cw * 9 / 16 + 10 + 30;
    const E = canvas(QS.map(([q, img, mood]) => `<div class="search" style="height:54px;padding:0 16px;gap:10px;border-radius:14px;box-shadow:0 0 0 2px rgba(61,155,255,.45),0 10px 30px rgba(0,0,0,.4)"><span style="color:var(--blue);font-size:22px">⌕</span><span class="q" style="font-size:19px">${q}</span></div>
      ${pic(img, `position:relative;width:${cw}px;height:${cw * 9 / 16}px;border-radius:14px;margin-top:12px`, "50% 40%")}<div class="row" style="gap:8px;margin-top:10px">${tagsHtml(mood, "mood", 16)}</div>`),
      { cols: vertical ? 3 : 5, rows: vertical ? 5 : 3, dx: 370, dy: chh + 50, cw, ch: chh });
    const end = endCard('Search your library <span style="color:var(--blue-hi)">by mood</span>, with');

    seek = (t) => {
      scene(A, t, 0, 0.35, 3.0, 3.3); drift(A, t);
      tbl.style.transform = `scale(${1 + 0.035 * clamp(t / 3.3)})`;
      rows.style.transform = `translateY(${-span(t, 0.3, 3.1) * ROWS.length * rowH * 0.55}px)`;
      scene(B, t, 3.25, 3.55, 6.6, 6.9);
      kw.querySelector(".q").textContent = typed(t, 3.6, 4.9, Q);
      const sh = t > 5.1 && t < 5.6 ? Math.sin((t - 5.1) * 60) * 14 * (5.6 - t) * 2 : 0;
      kw.style.transform = `translateX(${sh}px)`; kw.style.borderColor = t > 5.1 ? "rgba(224,122,109,.8)" : "var(--panel-edge)";
      rise(none, t, 5.2, 5.6);
      scene(S1, t, 6.85, 7.15, 13.2, 13.5);
      vs.querySelector(".q").textContent = typed(t, 7.15, 8.1, Q);
      vs.style.transform = `translateY(${-(sTop - T1) * span(t, 8.25, 8.75)}px)`;
      scene(C, t, 8.35, 8.65, 9.95, 10.3);
      C.move(260 - 520 * clamp((t - 8.35) / 1.95), 380 - 900 * clamp((t - 8.35) / 1.95));
      scene(D, t, 10.0, 10.35, 13.2, 13.5);
      rrow.style.transform = `translateX(${(1 - span(t, 10.1, 10.8)) * 500 - clamp((t - 10.8) / 2.5) * 120}px)`;
      const r0 = { x: PAD + rw / 2 - clamp((t - 10.8) / 2.5) * 120, y: rTop + rw * 9 / 32 };
      cursor(t, [[10.5, W - 180, H - 120], [11.0, r0.x, r0.y], [11.5, r0.x + 10, r0.y + 20]], [11.05]);
      big.style.opacity = span(t, 11.15, 11.5);
      kb(big, t, 11.15, 13.5, 1, 1.08);
      scene(E, t, 13.3, 13.6, 16.6, 16.9);
      E.cam(-30 * clamp((t - 15.4) / 1.5), (chh * 0.1) + 24 * clamp((t - 15.4) / 1.5), zoomTo(t, 13.45, 15.6, 2.0, vertical ? 0.9 : 0.74), t);
      end(t, 16.9);
    };
  }

  // ---------------------------------------------------------------- v2: ad breaks that respect the story (from the ad-break video)
  if (V.startsWith("v2")) {
    topBar("For ad ops & monetisation");
    const cursor = makeCursor();
    const EP = 43 * 60, T = (tc) => { const [m, s] = tc.split(":").map(Number); return (m * 60 + s) / EP; };
    const fmt = (s) => `${String(Math.floor(s / 60)).padStart(2, "0")}:${String(Math.floor(s % 60)).padStart(2, "0")}`;
    // an arc whose quiet valleys sit at the two break points, 14:37 and 28:51
    const ARC2 = [[0, 0.72], [0.18, 0.3], [T("14:37"), 0.82], [0.52, 0.28], [T("28:51"), 0.8], [0.85, 0.1], [1, 0.6]];
    // A: the episode builds to its climax, with other episodes floating behind
    const T2 = vertical ? 380 : TOP, ph = vertical ? 620 : 470, aTop = T2 + ph + (vertical ? 120 : 60), aH = vertical ? 300 : 200;
    const { d: dA, P: PA } = curve(ARC2, CW, aH);
    const A = layer(floatHtml(["r-peaky", "r-reacher", "r-secret", "r-skyfall", "r-wick-2", "r-spy", "r-argo", "r-lord"], 11) + pic("r-suc", `position:absolute;left:${PAD}px;top:${T2}px;width:${CW}px;height:${ph}px;box-shadow:0 30px 80px rgba(0,0,0,.6)`, "50% 40%", `
      <div class="abs tc" style="left:18px;top:16px;font-size:16px;letter-spacing:.06em;color:rgba(255,255,255,.9);text-shadow:0 1px 6px #000">S1 E4 · 43:00</div>
      <div class="abs" style="left:0;right:0;bottom:0;height:80px;background:linear-gradient(0deg,rgba(0,0,0,.7),transparent)"></div>
      <div class="abs row" style="left:18px;right:18px;bottom:16px;align-items:center;gap:12px"><span style="color:#fff;font-size:20px">▶</span>
        <div style="flex:1;height:5px;border-radius:3px;background:rgba(255,255,255,.3)"><div class="prog" style="height:5px;border-radius:3px;background:#fff"></div></div><span class="tc tcv" style="color:#fff;font-size:17px"></span></div>`).replace('class="frame"', 'class="frame player"') + `
      <svg class="abs arcA" style="left:${PAD}px;top:${aTop}px;overflow:visible" width="${CW}" height="${aH}">
        <text x="0" y="-18" font-family="DejaVu Sans Mono" font-size="17" letter-spacing="2" fill="#7d889b">STORY ARC</text>
        <defs><filter id="ag2"><feGaussianBlur stdDeviation="6"/></filter></defs>
        <path d="${dA}" fill="none" stroke="#e07a6d" stroke-width="9" opacity=".45" filter="url(#ag2)"/><path class="arcPath" d="${dA}" fill="none" stroke="#f0907f" stroke-width="3.5" stroke-linecap="round"/>
        <circle class="dot" r="11" fill="#fff" style="filter:drop-shadow(0 0 10px #fff)"/>
        <text class="peak" x="${PA[5][0]}" y="${PA[5][1] - 26}" text-anchor="middle" font-family="Inter" font-weight="700" font-size="${vertical ? 22 : 19}" letter-spacing="1.5" fill="#fff" opacity="0">CLIMAX</text></svg>`);
    const player = A.querySelector(".player"), dot = A.querySelector(".dot"), peak = A.querySelector(".peak"), prog = A.querySelector(".prog"), tcv = A.querySelector(".tcv");
    const pathEl = A.querySelector(".arcPath"), len = pathEl.getTotalLength();
    const at = (x) => { let lo = 0, hi = len; for (let i = 0; i < 24; i++) { const m = (lo + hi) / 2; (pathEl.getPointAtLength(m).x < x * CW ? (lo = m) : (hi = m)); } return pathEl.getPointAtLength(lo); };
    // B: the ad that interrupts
    const slam = el(`<div class="abs" style="inset:0;background:#ffd400;color:#111;opacity:0;z-index:25;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;overflow:hidden">
      <span class="abs tc" style="right:40px;top:40px;font-size:22px;background:rgba(0,0,0,.82);color:#fff;padding:8px 14px;border-radius:8px">Ad · 0:30</span>
      <div style="font-family:'Inter Display','Inter';font-weight:800;font-size:${vertical ? 200 : 180}px;letter-spacing:-0.05em;line-height:.88;transform:rotate(-4deg)">MEGA<br>SALE!</div>
      <div style="font-weight:800;font-size:${vertical ? 62 : 54}px;background:#e3262f;color:#fff;padding:10px 28px;transform:rotate(-4deg);margin-top:30px">50% OFF EVERYTHING</div>
      <span class="abs" style="right:40px;bottom:40px;font-size:24px;background:rgba(0,0,0,.82);color:#fff;padding:12px 20px;border-radius:8px">Skip in 5</span></div>`);
    const ignore = say('Ad breaks that <span style="color:#f0907f">ignore the story.</span>');
    // D: the story view of the episode
    const sTop = T2 + (vertical ? 170 : 110), sH = vertical ? 380 : 260, tlTop = sTop + sH + (vertical ? 60 : 44), tlH = vertical ? 56 : 46;
    const { d: dS, P: PS } = curve(ARC2, CW, sH);
    const CH = [["00:00", "11:30", "The arrival"], ["11:30", "24:00", "The argument"], ["24:00", "36:40", "The storm"], ["36:40", "43:00", "The confession"]];
    const D = layer(`<div class="abs" style="left:${PAD}px;top:${sTop}px;width:${CW}px">
      <div class="tc" style="position:absolute;top:-46px;left:0;font-size:${vertical ? 20 : 17}px;letter-spacing:.12em;color:#7d889b">S1 E4 · STORY ARC AND SCENES</div>
      <svg width="${CW}" height="${sH}" style="overflow:visible;display:block"><defs><clipPath id="sc2"><rect class="scr" x="-20" y="-60" width="0" height="${sH + 120}"/></clipPath><filter id="sg2"><feGaussianBlur stdDeviation="6"/></filter></defs>
        <g clip-path="url(#sc2)"><path d="${dS}" fill="none" stroke="#e07a6d" stroke-width="9" opacity=".45" filter="url(#sg2)"/><path d="${dS}" fill="none" stroke="#f0907f" stroke-width="3.5"/></g></svg>
      <div class="timeline" style="height:${tlH}px;margin-top:${tlTop - sTop - sH}px">${CH.map(([a, b, n], i) => `<div class="seg" style="left:${T(a) * 100}%;width:calc(${(T(b) - T(a)) * 100}% - 3px);background:${i % 2 ? "#2c4270" : "#24365a"};color:#dbe5ff;font-size:${vertical ? 17 : 15}px">${n}</div>`).join("")}</div>
      <div class="row tc" style="justify-content:space-between;margin-top:10px;font-size:15px;color:#7d889b">${["00:00", "10:00", "20:00", "30:00", "43:00"].map((x) => `<span>${x}</span>`).join("")}</div></div>`);
    const scr = D.querySelector(".scr");
    // fixed-timer breaks every 10 minutes, struck out; then story-aware breaks drop into the valleys
    const timers = ["10:00", "20:00", "30:00", "40:00"].map((tc) => add(D, `<div class="abs col" style="left:${PAD + CW * T(tc) - 2}px;top:${sTop - 10}px;height:${tlTop - sTop + tlH + 20}px;align-items:center;opacity:0">
      <div style="flex:1;border-left:3px dashed #7d889b"></div><span style="position:absolute;top:-34px;font-size:28px;line-height:1;color:#ff9b9b">✕</span></div>`));
    const timerLab = add(D, `<div class="abs tc" style="left:${PAD}px;top:${tlTop + tlH + (vertical ? 70 : 52)}px;font-size:${vertical ? 20 : 17}px;color:#9aa3b5;opacity:0">✕ FIXED TIMER: A BREAK EVERY 10 MINUTES, WHEREVER THE STORY IS</div>`);
    const BR = ["14:37", "28:51"];
    const breaks = BR.map((tc, i) => { const p = PS[i === 0 ? 2 : 4]; return add(D, `<div class="abs" style="left:${PAD + p[0] - 3}px;top:${sTop + p[1]}px;width:6px;height:${tlTop - sTop - p[1] + tlH + 12}px;border-radius:3px;background:#e07a6d;box-shadow:0 0 16px #e07a6d;transform-origin:50% 0;opacity:0"></div>`); });
    const panW = vertical ? 330 : 290, fsP = vertical ? 22 : 19;
    const panels = BR.map((tc) => { const x = Math.min(W - PAD - panW, Math.max(PAD, PAD + CW * T(tc) - panW / 2));
      return add(D, `<div class="abs" style="left:${x}px;top:${tlTop + tlH + (vertical ? 70 : 52)}px;width:${panW}px;background:#0f1824;border:1.5px solid rgba(224,122,109,.65);border-radius:14px;padding:${fsP * 0.75}px ${fsP}px;box-shadow:0 20px 50px rgba(0,0,0,.5);opacity:0">
        <div class="tc" style="font-size:${fsP - 1}px;color:#f0907f">AD BREAK ${tc}</div><div class="col" style="gap:${fsP * 0.35}px;margin-top:${fsP * 0.5}px;font-size:${fsP}px">
        <span><span style="color:var(--muted)">Between:</span> two scenes</span><span><span style="color:var(--muted)">Mood:</span> Uplifting</span><span><span style="color:var(--muted)">IAB:</span> Travel</span><span><span style="color:var(--muted)">Brand-safe:</span> <b style="color:#3ddc97">yes</b></span></div></div>`); });
    const btnTop = tlTop + tlH + (vertical ? 70 : 52) + (vertical ? 260 : 220);
    const btn = add(D, `<span class="abs btn" style="right:${PAD}px;top:${btnTop}px;font-size:${vertical ? 26 : 23}px;padding:14px 24px;background:var(--blue);color:#fff;opacity:0">Send breaks to ad server</span>`);
    // E: pull back over the whole catalogue, every episode with its arc and breaks
    const EPS = [["t-suc", "Succession"], ["t-peaky", "Peaky Blinders"], ["t-reacher", "Reacher"], ["t-skyfall", "Skyfall"], ["t-wick-2", "John Wick"], ["t-spy", "Spy Game"], ["t-argo", "Argo"],
      ["t-glad", "Gladiator"], ["t-lala", "La La Land"], ["t-ticket", "Ticket to Paradise"], ["t-king", "King Richard"], ["t-upgrade", "Upgrade"], ["t-candy", "Candyman"], ["t-lord", "Lord of War"], ["t-secret", "The Secret"]];
    const ecw = 320, ech = ecw * 9 / 16 + 12 + 56 + 6 + 10 + 12 + 24;
    const epCard = ([img, title], k) => {
      const r = rand(101 + k * 7), pts = [[0, 0.55 + r() * 0.2]];
      for (let i = 1; i <= 6; i++) pts.push([Math.min(1, i / 6 + (i < 6 ? (r() - 0.5) * 0.06 : 0)), i % 2 ? 0.12 + r() * 0.25 : 0.68 + r() * 0.25]);
      const { d, P } = curve(pts, ecw, 56);
      return `${pic(img, `position:relative;width:${ecw}px;height:${ecw * 9 / 16}px;border-radius:12px`, "50% 40%")}
        <svg width="${ecw}" height="56" style="display:block;margin-top:12px;overflow:visible"><path d="${d}" fill="none" stroke="#f0907f" stroke-width="2.5"/>${[2, 4].map((i) => `<line x1="${P[i][0]}" x2="${P[i][0]}" y1="${P[i][1]}" y2="70" stroke="#e07a6d" stroke-width="3"/>`).join("")}</svg>
        <div style="position:relative;height:10px;border-radius:5px;background:#1a2433;margin-top:6px">${[2, 4].map((i) => `<span class="abs" style="left:${P[i][0] - 3}px;top:-5px;width:6px;height:20px;border-radius:3px;background:#e07a6d;box-shadow:0 0 10px #e07a6d"></span>`).join("")}</div>
        <div class="row" style="justify-content:space-between;align-items:center;margin-top:12px"><span style="font-size:18px;font-weight:600">${title}</span><span class="tc" style="color:#f0907f;font-size:13px">2 BREAKS</span></div>`;
    };
    const E = canvas(EPS.map(epCard), { cols: vertical ? 3 : 5, rows: vertical ? 5 : 3, dx: 370, dy: ech + 60, cw: ecw, ch: ech });
    const respect = say('Ad breaks that <span class="hl">respect the story.</span>');
    const end = endCard("Place every ad break with");

    seek = (t) => {
      const before = t < 4.3;
      A.style.opacity = before ? span(t, 0, 0.4) : 0; A.style.visibility = before ? "visible" : "hidden";
      A.style.transform = `scale(${1 + 0.04 * clamp(t / 4.3)})`; drift(A, t);
      const x = 0.55 + 0.3 * span(t, 0.8, 4.2), p = at(x);
      dot.setAttribute("cx", p.x); dot.setAttribute("cy", p.y);
      peak.setAttribute("opacity", span(t, 3.8, 4.1));
      prog.style.width = `${x * 100}%`; tcv.textContent = `${fmt(x * EP)} / 43:00`;
      kb(player, t, 0, 4.3, 1, 1.1);
      const on = t >= 4.3 && t < 6.5;
      slam.style.opacity = on ? 1 : 0;
      slam.style.transform = on ? `scale(${1 + 0.12 * (1 - span(t, 4.3, 4.5))}) translateX(${t < 4.8 ? Math.sin(t * 90) * 10 * (4.8 - t) : 0}px)` : "none";
      sayAt(ignore, t, 6.6, 8.6);
      scene(D, t, 8.7, 9.1, 13.7, 14.05);
      scr.setAttribute("width", (CW + 40) * span(t, 8.9, 10.0));
      timers.forEach((n, i) => { n.style.opacity = vis(t, 9.9 + i * 0.12, 10.1 + i * 0.12, 10.9, 11.2); });
      timerLab.style.opacity = vis(t, 9.9, 10.2, 10.9, 11.2);
      breaks.forEach((n, i) => { const k = span(t, 11.2 + i * 0.35, 11.6 + i * 0.35); n.style.opacity = k; n.style.transform = `scaleY(${k})`; });
      panels.forEach((n, i) => popIn(n, t, 11.9 + i * 0.4));
      btn.style.opacity = span(t, 12.5, 12.8);
      const sent = t >= 13.2;
      btn.textContent = sent ? "✓ Sent to ad server" : "Send breaks to ad server";
      btn.style.background = sent ? "#17785f" : "var(--blue)";
      const bx = W - PAD - (vertical ? 170 : 150), by = btnTop + 30;
      cursor(t, [[12.4, W / 2, H - 120], [13.0, bx, by], [13.5, bx + 20, by + 30]], [13.1]);
      scene(E, t, 13.85, 14.15, 15.7, 16.0);
      E.cam(24 * clamp((t - 15) / 1), ech * 0.05, zoomTo(t, 13.95, 15.3, 1.9, vertical ? 0.88 : 0.72), t);
      sayAt(respect, t, 16.0, 17.8);
      end(t, 17.9);
    };
  }

  // ---------------------------------------------------------------- v3: one library, endless shorts (from the broadcast video)
  if (V.startsWith("v3")) {
    topBar("For social & digital teams");
    const cursor = makeCursor(), cursor2 = makeCursor();
    const FR = [["troy", "Troy", "01:42:10", "Epic", "#3360d0"], ["glad", "Gladiator", "02:11:36", "Triumphant", "#e07a6d"], ["kingdom", "Kingdom of Heaven", "01:58:04", "Tense", "#c98a1b"],
      ["samurai", "The Last Samurai", "02:04:51", "Intense", "#7b5cd6"], ["north", "The Northman", "01:47:22", "Intense", "#7b5cd6"], ["brave", "Braveheart", "02:21:05", "Epic", "#3360d0"]];
    // A: scrubbing the archive, with other films floating behind
    const fh = vertical ? 620 : 520, A3 = vertical ? 450 : TOP + 20;
    const A = layer(floatHtml(["r-lala", "r-ticket", "r-skyfall", "r-pap", "r-forrest", "r-shaw", "r-wick-2", "r-king"], 23) + `<div class="ui" style="left:${PAD}px;top:${A3}px;width:${CW}px;height:${fh + 130}px">
      <div class="ui-bar"><span>Archive</span><span class="ctx">Feature films</span></div>
      <div class="abs" style="left:0;right:0;top:50px;height:${fh}px">${FR.map(([t]) => pic(`r-${t}`, `position:absolute;inset:0;opacity:0`, "50% 40%").replace('class="frame"', 'class="frame sf"')).join("")}
        <div class="abs tc lab" style="left:18px;top:16px;font-size:17px;color:#fff;text-shadow:0 1px 6px #000"></div></div>
      <div class="abs" style="left:24px;right:24px;top:${fh + 84}px;height:6px;border-radius:3px;background:rgba(255,255,255,.18)"><div class="fill" style="height:6px;border-radius:3px;background:#fff"></div>
        <div class="knob abs" style="top:-9px;width:24px;height:24px;margin-left:-12px;border-radius:50%;background:#fff;box-shadow:0 0 12px rgba(255,255,255,.7)"></div></div></div>`);
    const frames = [...A.querySelectorAll(".sf")], lab = A.querySelector(".lab"), fill = A.querySelector(".fill"), knob = A.querySelector(".knob");
    const need = say('Need one epic moment <span class="hl">for social?</span>');
    // C: moments rush past, tagged by mood
    const MPOOL = ["r-troy", "r-glad", "r-kingdom", "r-samurai", "r-north", "r-brave", "r-lord", "r-skyfall", "r-wick-2", "r-peaky", "r-reacher", "r-argo", "r-spy", "r-pap", "r-lala", "r-ticket", "r-king", "r-forrest"];
    const MOODS = [["Epic", "#3360d0"], ["Triumphant", "#e07a6d"], ["Tense", "#c98a1b"], ["Intense", "#7b5cd6"], ["Funny", "#17785f"], ["Bittersweet", "#5b6b8c"]];
    const mwc = vertical ? 6 : 7, mwr = vertical ? 13 : 8;
    const Cw = wall(mix(MPOOL, mwc * mwr, mwc), { cols: mwc, tw: vertical ? 330 : 300, rz: 8, label: "MOMENTS FOUND ACROSS YOUR ARCHIVE",
      extra: (i) => { const [m, c] = MOODS[(i * 5) % MOODS.length]; return `<span class="abs tag" style="left:14px;bottom:12px;font-size:16px;padding:4px 10px;background:${c};color:#fff">${m}</span>`; } });
    // C2: six moments, ready to use
    const gc = vertical ? 2 : 3, gw = (CW - (gc - 1) * 24) / gc, gh = gw * 9 / 16, gTop = vertical ? 400 : TOP + 40, gPitch = gh + (vertical ? 110 : 84);
    const rectGrid = (i) => ({ x: PAD + (i % gc) * (gw + 24), y: gTop + Math.floor(i / gc) * gPitch, w: gw, h: gh });
    const C2 = layer(FR.map(([t, name, tc, mood, col], i) => { const r = rectGrid(i); return `<div class="abs gi" style="left:${r.x}px;top:${r.y}px;width:${gw}px">${pic(`r-${t}`, `position:relative;width:${gw}px;height:${gh}px;border-radius:12px`, "50% 40%")}
      <div class="col" style="gap:6px;margin-top:10px"><span style="font-size:${vertical ? 24 : 20}px;font-weight:600;white-space:nowrap">${name}</span>
      <div class="row" style="align-items:center;gap:10px"><span class="tc" style="font-size:${vertical ? 17 : 15}px;color:var(--muted)">${tc}</span><span class="tag" style="font-size:${vertical ? 17 : 15}px;padding:4px 10px;background:${col};color:#fff">${mood}</span></div></div></div>`; }).join(""));
    const gis = [...C2.querySelectorAll(".gi")];
    // D: 16:9 in, 9:16 out
    const bw = vertical ? CW : 580, bh = bw * 9 / 16, bx = PAD, by = vertical ? TOP + 60 : TOP + 230;
    const pW = vertical ? 330 : 250, pX = vertical ? (W - pW) / 2 : W - PAD - pW - 10, pY = vertical ? by + bh + 90 : by + bh / 2 - (pW * 16 / 9 + 20) / 2;
    const eTop = vertical ? pY + pW * 16 / 9 + 60 : by + bh + 60, eX = vertical ? (W - 300) / 2 : bx;
    const D = layer(`<div class="abs bigv" style="left:${bx}px;top:${by}px;width:${bw}px;height:${bh}px;overflow:hidden;border-radius:12px">${pic("r-glad", `position:absolute;inset:0`, "50% 40%")}
        <div class="abs crop" style="top:0;width:${bh * 9 / 16}px;height:${bh}px;border:3px solid #3d9bff;box-shadow:0 0 0 2000px rgba(0,0,0,.5)"><span class="abs tc" style="left:8px;top:8px;font-size:14px;background:#fff;color:#0b131c;padding:2px 8px;border-radius:4px;white-space:nowrap">character tracked</span></div></div>
      <svg class="abs arw" style="left:${vertical ? W / 2 - 18 : bx + bw + 22}px;top:${vertical ? by + bh + 20 : by + bh / 2 - 18}px" width="${vertical ? 36 : 56}" height="${vertical ? 46 : 36}">${vertical ? '<path d="M18 0 V36 M8 26 L18 38 L28 26" stroke="#3d9bff" stroke-width="4" fill="none"/>' : '<path d="M0 18 H46 M36 8 L48 18 L36 28" stroke="#3d9bff" stroke-width="4" fill="none"/>'}</svg>
      <div class="abs ph" style="left:${pX}px;top:${pY}px">${phoneHtml(pW, "r-glad", "62% 40%", "Are you not entertained? ⚔️")}</div>
      <span class="abs btn exp" style="left:${eX}px;top:${eTop}px;width:${vertical ? 300 : 280}px;font-size:${vertical ? 26 : 23}px;padding:14px 22px;background:var(--blue);color:#fff">Export 9:16 clip</span>`);
    const bigv = D.querySelector(".bigv"), crop = D.querySelector(".crop"), arw = D.querySelector(".arw"), ph = D.querySelector(".ph"), exp = D.querySelector(".exp");
    // E: pull back over a feed's worth of shorts
    const PH = [["r-glad", "62% 40%", "Are you not entertained? ⚔️"], ["r-troy", "45% 40%", "Wait for it… ⚔️"], ["r-lala", "75% 30%", "This scene. 🎶"], ["r-brave", "50% 40%", "Goosebumps."],
      ["r-ticket", "50% 35%", "Tag your travel buddy 🌴"], ["r-wick-2", "50% 40%", "Iconic. 🔥"], ["r-skyfall", "50% 40%", "Best opening ever?"], ["r-peaky", "60% 35%", "Watch till the end 👀"],
      ["r-shaolin", "50% 40%", "😂😂😂"], ["r-king", "50% 40%", "Underdog energy."], ["r-north", "50% 40%", "Chills."], ["r-forrest", "50% 40%", "Classic."], ["r-samurai", "50% 40%", "The standoff."],
      ["r-kingdom", "50% 40%", "Epic."], ["r-pap", "50% 40%", "Hold your breath."]];
    const pcw = 250, pch = pcw * 16 / 9 + 20;
    const E = canvas(PH.map(([n, pos, cap]) => phoneHtml(pcw, n, pos, cap)), { cols: vertical ? 3 : 5, rows: vertical ? 5 : 3, dx: 320, dy: pch + 60, cw: pcw, ch: pch });
    const endless = say('One library. <span class="hl">Endless shorts.</span>');
    const end = endCard("Find every moment worth sharing, with");

    seek = (t) => {
      scene(A, t, 0, 0.35, 3.4, 3.7); drift(A, t);
      const k = Math.floor(t / 0.42) % FR.length;
      frames.forEach((f, i) => (f.style.opacity = i === k ? 1 : 0));
      const scrub = 0.5 + 0.42 * Math.sin(t * 2.3) * Math.cos(t * 0.9);
      fill.style.width = `${scrub * 100}%`; knob.style.left = `${scrub * 100}%`;
      lab.textContent = `${FR[k][1]} · ${FR[k][2]}`;
      const kx = PAD + 24 + (CW - 48) * scrub, ky = A3 + fh + 84 + 3;
      cursor(t, [[0.2, kx, ky], [3.3, kx, ky]], []);
      sayAt(need, t, 3.8, 5.8);
      scene(Cw, t, 5.85, 6.15, 7.3, 7.65);
      Cw.move(-240 + 480 * clamp((t - 5.85) / 1.8), 420 - 880 * clamp((t - 5.85) / 1.8));
      scene(C2, t, 7.45, 7.8, 10.3, 10.7);
      gis.forEach((g, i) => { popIn(g, t, 7.5 + i * 0.09, 0.85); if (i !== 1) g.style.opacity = +g.style.opacity * (1 - span(t, 9.9, 10.2)); });
      const g1 = rectGrid(1);
      cursor2(t, [[8.9, W - 160, H - 200], [9.6, g1.x + g1.w / 2, g1.y + g1.h / 2], [10.1, g1.x + g1.w / 2 + 10, g1.y + g1.h / 2 + 20], [12.6, W / 2, H - 150],
        [13.3, eX + 150, eTop + 28], [14.0, eX + 170, eTop + 50]], [9.65, 13.4]);
      scene(D, t, 10.45, 10.85, 14.45, 14.75);
      kb(bigv, t, 10.45, 14.7, 1, 1.06);
      crop.style.left = `${(bw - bh * 9 / 16) * (0.15 + 0.4 * span(t, 11.0, 12.0))}px`;
      arw.style.opacity = span(t, 11.9, 12.2);
      ph.style.opacity = span(t, 12.1, 12.6); ph.style.transform = `translateY(${(1 - span(t, 12.1, 12.6)) * 30}px)`;
      exp.style.opacity = span(t, 12.5, 12.8);
      const done = t >= 13.45;
      exp.textContent = done ? "✓ Exported · tagged" : "Export 9:16 clip";
      exp.style.background = done ? "#17785f" : "var(--blue)";
      scene(E, t, 14.55, 14.85, 16.45, 16.75);
      E.cam(20 * clamp((t - 15.8) / 0.9), 0, zoomTo(t, 14.65, 16.0, vertical ? 1.3 : 1.6, vertical ? 0.75 : 0.68), t);
      sayAt(endless, t, 16.75, 18.4);
      end(t, 18.5);
    };
  }

  // ---------------------------------------------------------------- v4: one recipe, every title (from the editors video)
  if (V.startsWith("v4")) {
    topBar("For creative teams");
    const cursor = makeCursor(), cursor2 = makeCursor();
    // A: rejecting frames by hand, with more titles waiting behind
    const B4 = vertical ? 420 : TOP, ph = vertical ? 620 : 440, sTop = B4 + ph + (vertical ? 120 : 90), sw = (CW - 3 * 16) / 4, sh = sw * 9 / 16;
    const BAD = [["r-skyfall-2", "Blurry", "blur(7px)", ""], ["r-peaky", "Too dark", "brightness(.22)", ""], ["r-suc", "Text on screen", "", "PREVIOUSLY ON…"], ["r-shaw", "Motion blur", "blur(4px) brightness(.8)", ""]];
    const A = layer(floatHtml(["r-lala", "r-ticket", "r-zoo", "r-king", "r-glad", "r-argo", "r-any", "r-forrest"], 41) + `
      <div class="abs tc" style="left:${PAD}px;top:${B4 - 8}px;font-size:${vertical ? 20 : 17}px;letter-spacing:.1em;color:#7d889b">PICK A THUMBNAIL · TITLE 1 OF 2,431</div>
      <div class="abs prev" style="left:${PAD}px;top:${B4 + 30}px;width:${CW}px;height:${ph}px;border-radius:14px;overflow:hidden;box-shadow:0 30px 80px rgba(0,0,0,.6)">${BAD.map(([n, , f, txt]) => `<div class="pv abs" style="inset:0;opacity:0">${pic(n, `position:absolute;inset:0;filter:${f || "none"}`, "50% 40%")}${txt ? `<span class="abs" style="left:28px;bottom:26px;font-size:${vertical ? 44 : 36}px;font-weight:800;letter-spacing:.06em;color:#fff;text-shadow:0 2px 10px #000">${txt}</span>` : ""}</div>`).join("")}</div>
      ${BAD.map(([n, why, f, txt], i) => `<div class="abs st" style="left:${PAD + i * (sw + 16)}px;top:${sTop}px;width:${sw}px">
        <div style="position:relative;height:${sh}px;border-radius:10px;overflow:hidden">${pic(n, `position:absolute;inset:0;filter:${f || "none"}`, "50% 40%")}${txt ? `<span class="abs" style="left:8px;bottom:6px;font-size:11px;font-weight:800;color:#fff">${txt}</span>` : ""}
          <div class="x abs" style="inset:0;display:grid;place-items:center;background:rgba(224,62,62,.35);opacity:0"><span style="font-size:${sh * 0.6}px;color:#fff;line-height:1;font-weight:300">✕</span></div></div>
        <span class="why tag" style="margin-top:10px;font-size:${vertical ? 17 : 15}px;padding:5px 11px;background:rgba(224,62,62,.18);border:1.5px solid rgba(224,62,62,.6);color:#ff9b9b;opacity:0">${why}</span></div>`).join("")}`);
    const pvs = [...A.querySelectorAll(".pv")], strip = [...A.querySelectorAll(".st")], prev = A.querySelector(".prev");
    const hand = say('Picking thumbnails by hand <span class="hl">doesn’t scale.</span>');
    // C: the recipe
    const rW = vertical ? CW : 820, rX = (W - rW) / 2, rY = vertical ? 560 : TOP + 40, fs = vertical ? 24 : 21;
    const RROWS = [["Character", tagsHtml(["Leads"], "blue", fs - 2)], ["Mood", tagsHtml(["Warm", "Uplifting"], "mood", fs - 2)], ["Shot type", tagsHtml(["Medium close-up"], "ghost", fs - 2)],
      ["Brightness", `<div style="width:${rW * 0.3}px;height:8px;border-radius:4px;background:#1a2433"><div style="width:72%;height:8px;border-radius:4px;background:var(--blue-hi)"></div></div>`],
      ["Format", tagsHtml(["16:9 ✓", "9:16 ✓"], "blue", fs - 2)], ["Title logo", tagsHtml(["Placed ✓"], "blue", fs - 2)], ["Filters", tagsHtml(["No blur", "No on-screen text", "No nudity"], "ok", fs - 4)]];
    const C = layer(`<div class="ui" style="left:${rX}px;top:${rY}px;width:${rW}px">
      <div class="ui-bar"><img src="logo/vionlabs-white.png" alt="Vionlabs"><span class="mod">Creative Lab</span><span class="ctx">Recipe</span></div>
      <div style="padding:${fs}px ${fs * 1.2}px"><div class="tc" style="font-size:${fs - 6}px;letter-spacing:.12em;color:var(--blue-hi);margin-bottom:${fs * 0.6}px">RECIPE · HERO THUMBNAILS</div>
      ${RROWS.map(([k, v]) => `<div class="rr row" style="align-items:center;gap:16px;min-height:${fs * 2.7}px;border-bottom:1px solid var(--panel-edge);opacity:0"><span style="width:${fs * 7}px;flex:none;font-size:${fs}px;color:var(--muted)">${k}</span><div class="row" style="gap:10px;flex-wrap:wrap">${v}</div></div>`).join("")}
      <span class="apply btn" style="margin-top:${fs * 1.1}px;font-size:${fs + 2}px;padding:14px 24px;background:var(--blue);color:#fff">Apply to catalogue</span></div></div>`);
    const rrows = [...C.querySelectorAll(".rr")], apply = C.querySelector(".apply");
    // D: the whole catalogue comes back done, rushing past
    const TPOOL = ["ticket", "skyfall", "lala", "zoo", "argo", "forrest", "peaky", "troy", "vacation", "reacher", "north", "pap", "suc", "secret", "any", "kingdom", "brave", "samurai",
      "friday", "candy", "king", "women", "american", "shaolin", "wick-2", "glad", "fall", "spy", "lord", "val", "xmen", "ind", "60", "fast", "godzilla", "upgrade", "kelly", "burt", "gethard", "fanboys"].map((n) => `t-${n}`);
    const dwc = vertical ? 6 : 7, dwr = vertical ? 13 : 8;
    const D = wall(mix(TPOOL, dwc * dwr, dwc), { cols: dwc, tw: vertical ? 330 : 300, rz: -7, radius: 24,
      extra: () => `<span class="abs" style="right:12px;top:12px;width:30px;height:30px;border-radius:50%;background:#17785f;color:#fff;font-size:18px;display:grid;place-items:center;box-shadow:0 4px 12px rgba(0,0,0,.4)">✓</span>`,
      label: "RECIPE APPLIED" });
    // E: one result up close, in both formats
    const zW = vertical ? CW : 640, zH = zW * 9 / 16, vW = vertical ? 300 : zH * 9 / 16, zY = vertical ? TOP + 100 : TOP + 120;
    const E = layer(`<div class="abs" style="left:${PAD}px;top:${zY}px;width:${CW}px">
      <div class="row" style="gap:${vertical ? 0 : 22}px;align-items:flex-end;${vertical ? "flex-direction:column;align-items:center;gap:30px" : ""}">
        ${pic("t-lala", `position:relative;width:${zW}px;height:${zH}px;border-radius:14px`)}${pic("r-lala", `position:relative;width:${vW}px;height:${vW * 16 / 9}px;border-radius:14px;flex:none`, "75% 30%")}</div>
      <div class="row" style="gap:10px;margin-top:24px;flex-wrap:wrap;${vertical ? "justify-content:center" : ""}">${tagsHtml(["Leads ✓", "Warm ✓", "Medium close-up ✓", "Title placed ✓", "16:9 + 9:16 ✓"], "blue", vertical ? 23 : 20)}</div></div>`);
    const every = say('One recipe. <span class="hl">Every title.</span>');
    const end = endCard("Thumbnails for every title, with");
    const sx = (i) => PAD + i * (sw + 16) + sw / 2, sy2 = sTop + sh / 2;

    seek = (t) => {
      scene(A, t, 0, 0.3, 3.5, 3.8); drift(A, t);
      prev.style.transform = `scale(${1 + 0.03 * clamp(t / 3.8)})`;
      const clicks = [0.6, 1.3, 2.0, 2.7], cur = clicks.filter((c) => t >= c).length - 1;
      pvs.forEach((p, i) => (p.style.opacity = i === Math.max(0, cur) ? 1 : 0));
      strip.forEach((s, i) => {
        s.style.opacity = span(t, 0.1 + i * 0.06, 0.4 + i * 0.06);
        s.querySelector(".x").style.opacity = span(t, clicks[i] + 0.25, clicks[i] + 0.4);
        s.querySelector(".why").style.opacity = span(t, clicks[i] + 0.3, clicks[i] + 0.5);
      });
      cursor(t, [[0.2, W / 2, H - 120], ...clicks.flatMap((c, i) => [[c - 0.05, sx(i), sy2], [c + 0.3, sx(i) + 6, sy2 + 8]]), [3.3, sx(3) + 6, sy2 + 8]], clicks);
      sayAt(hand, t, 3.9, 5.9);
      scene(C, t, 6.0, 6.4, 9.45, 9.8);
      rrows.forEach((r, i) => rise(r, t, 6.3 + i * 0.28, 6.6 + i * 0.28));
      const ar = apply.getBoundingClientRect(), sr = stage.getBoundingClientRect();
      const ax = ar.left - sr.left + ar.width * 0.6, ay = ar.top - sr.top + ar.height * 0.6;
      cursor2(t, [[8.3, W - 160, H - 140], [9.0, ax, ay], [9.4, ax + 8, ay + 12]], [9.05]);
      apply.style.background = t >= 9.1 ? "#17785f" : "var(--blue)";
      apply.textContent = t >= 9.1 ? "✓ Applying…" : "Apply to catalogue";
      scene(D, t, 9.7, 10.0, 13.15, 13.5);
      D.move(260 - 520 * clamp((t - 9.7) / 3.8), 500 - 1000 * clamp((t - 9.7) / 3.8));
      D.label.textContent = `RECIPE APPLIED · ${Math.round(2431 * span(t, 9.9, 12.6)).toLocaleString("en-US")} / 2,431 TITLES`;
      scene(E, t, 13.35, 13.75, 15.4, 15.7);
      sayAt(every, t, 15.8, 17.5);
      end(t, 17.6);
    };
  }

  window.seek = seek;
  window.animReady = Promise.all([...document.images].map((i) => (i.complete ? 0 : new Promise((r) => (i.onload = i.onerror = r))))).then(() => seek(0));
})();
