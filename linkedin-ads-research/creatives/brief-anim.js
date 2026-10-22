// Video ads for the brief campaign, in the same style as brief.js, driven frame by frame:
// record.cjs calls window.seek(t) and screenshots #stage.
//   brief-anim.html?v=ad0-S | ad0-V   Ad 0, 12 s: the story arc draws over a real frame, generic AI vs
//                                     Vionlabs reading, mood tags, the 1M+ library, end card.
//   brief-anim.html?v=ad3-S | ad3-V   Ad 3, 8 s: the playhead scrubs an episode and markers snap in.
(function () {
  const V = new URLSearchParams(location.search).get("v") || "ad0-S";
  const vertical = V.endsWith("-V");
  const W = 1080, H = vertical ? 1920 : 1080, PAD = 72;
  const DUR = { ad0: 12, ad3: 8 }[V.split("-")[0]];
  window.VIDEO = { id: V, w: W, h: H, duration: DUR, fps: 30 };

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
  const topBar = (aud) => el(`<div class="top abs" style="left:${PAD}px;right:${PAD}px;top:${vertical ? 96 : 64}px"><img class="wordmark" src="logo/vionlabs-white.png" alt="Vionlabs"><span class="eyebrow"><b></b>${aud}</span></div>`);
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

  window.seek = seek;
  window.animReady = Promise.all([...document.images].map((i) => (i.complete ? 0 : new Promise((r) => (i.onload = i.onerror = r))))).then(() => seek(0));
})();
