// The "AI built for entertainment" LinkedIn campaign from Viktor's ad brief
// (Vionlabs_Ad_Prompts_AI_built_for_entertainment.pdf), in the same style as ads.html:
// real product screenshots and title art from vionlabs.com, blue accent, audience label.
// S = 1080x1080 single image or carousel card, L = 1200x627 single image.
// Assets with an "r" in the ID (a0r-L, a3r-S, o1-c2r …) are the rights-safe revisions (board, Oct 2026): film and TV
// titles only as small posters among many; every big frame shows our own footage (img/g-*, footage.js) instead.
(function () {
  const WHITE = "logo/vionlabs-white.png", NAVY = "logo/vionlabs-navy.png";
  const ASSETS = [];
  const add = (id, ad, fmt, html, light = false) => ASSETS.push({ id, ad, fmt, html, light });

  // ---------------------------------------------------------------- helpers
  const top = (aud, light) => `<div class="top"><img class="wordmark" src="${light ? NAVY : WHITE}" alt="Vionlabs"><span class="eyebrow"><b></b>${aud}</span></div>`;
  const foot = (cta = true) => `<div class="foot">${cta ? '<span class="cta">Book a demo</span>' : "<span></span>"}<span class="signoff">AI built for entertainment.</span></div>`;
  const img = (name, style = "", pos = "50% 50%", extra = "") => `<div class="frame" data-img="${name}" data-pos="${pos}" style="${style}">${extra}</div>`;
  const tags = (list, cls, fs = 19, pad = "7px 14px", css = "") => list.map((t) => `<span class="tag ${cls}" style="font-size:${fs}px;padding:${pad};${css}">${t}</span>`).join("");
  const glow = (css) => `<div class="glow" style="${css}"></div>`;
  const arrow = (x, y, dir = "right") => dir === "right"
    ? `<svg class="abs" style="left:${x}px;top:${y}px" width="56" height="36"><path d="M0 18 H46 M36 8 L48 18 L36 28" stroke="#3d9bff" stroke-width="4" fill="none"/></svg>`
    : `<svg class="abs" style="left:${x}px;top:${y}px" width="36" height="46"><path d="M18 0 V36 M8 26 L18 38 L28 26" stroke="#3d9bff" stroke-width="4" fill="none"/></svg>`;

  // the story arc from the brief, in the product's coral mood colour
  function curve(pts, w, h) {
    const P = pts.map(([x, y]) => [x * w, y * h]);
    let d = `M${P[0][0]} ${P[0][1]}`;
    for (let i = 0; i < P.length - 1; i++) {
      const p0 = P[i - 1] || P[i], p1 = P[i], p2 = P[i + 1], p3 = P[i + 2] || p2;
      d += ` C${p1[0] + (p2[0] - p0[0]) / 6} ${p1[1] + (p2[1] - p0[1]) / 6} ${p2[0] - (p3[0] - p1[0]) / 6} ${p2[1] - (p3[1] - p1[1]) / 6} ${p2[0]} ${p2[1]}`;
    }
    return { d, P };
  }
  const ARC = [[0, 0.82], [0.12, 0.78], [0.31, 0.5], [0.5, 0.7], [0.73, 0.18], [0.9, 0.62], [1, 0.68]];
  const BEATS = [[1, "Setup"], [2, "Rising tension"], [3, "Turning point"], [4, "Climax"], [5, "Resolution"]];
  function arc(w, h, fs = 14, id = "a") {
    const { d, P } = curve(ARC, w, h);
    return `<svg class="abs" width="${w}" height="${h}" style="overflow:visible"><defs><filter id="ag-${id}"><feGaussianBlur stdDeviation="6"/></filter></defs>
      <path d="${d}" fill="none" stroke="#e07a6d" stroke-width="9" opacity=".5" filter="url(#ag-${id})"/><path d="${d}" fill="none" stroke="#f0907f" stroke-width="3.5" stroke-linecap="round"/>
      ${BEATS.map(([i, t]) => `<circle cx="${P[i][0]}" cy="${P[i][1]}" r="6" fill="#e07a6d"/><circle cx="${P[i][0]}" cy="${P[i][1]}" r="13" fill="#e07a6d" opacity=".25"/>
        <text x="${P[i][0]}" y="${P[i][1] - fs * 1.4}" text-anchor="middle" font-family="Inter" font-size="${fs}" font-weight="700" letter-spacing="1.4" fill="#fff" style="paint-order:stroke" stroke="rgba(0,0,0,.55)" stroke-width="3">${t.toUpperCase()}</text>`).join("")}</svg>`;
  }

  const AXES = ["Enjoyment", "Surprise", "Anticipation", "Sadness", "Fear", "Anger", "Disgust", "Indifference"];
  function radar(vals, size, { fs = 15, emph = [], labels = true, light = false } = {}) {
    const c = size / 2, R = size * (labels ? 0.3 : 0.44), n = AXES.length, grid = light ? "rgba(14,23,32,.14)" : "rgba(255,255,255,.13)";
    const pt = (i, r) => [c + Math.sin((i / n) * Math.PI * 2) * r, c - Math.cos((i / n) * Math.PI * 2) * r];
    return `<svg width="${size}" height="${size}" style="overflow:visible">
      ${[0.25, 0.5, 0.75, 1].map((k) => `<polygon points="${AXES.map((_, i) => pt(i, R * k).join(",")).join(" ")}" fill="none" stroke="${grid}"/>`).join("")}
      ${AXES.map((_, i) => `<line x1="${c}" y1="${c}" x2="${pt(i, R)[0]}" y2="${pt(i, R)[1]}" stroke="${grid}"/>`).join("")}
      <polygon points="${vals.map((v, i) => pt(i, R * v).join(",")).join(" ")}" fill="#e07a6d" fill-opacity=".35" stroke="#e07a6d" stroke-width="3" stroke-linejoin="round"/>
      ${labels ? AXES.map((a, i) => { const [x, y] = pt(i, R * 1.22), an = Math.abs(x - c) < 4 ? "middle" : x > c ? "start" : "end", on = emph.includes(a);
        return `<text x="${x}" y="${y + fs * 0.35}" text-anchor="${an}" font-family="Inter" font-size="${fs}" font-weight="${on ? 700 : 500}" fill="${on ? (light ? "#0e1720" : "#fff") : (light ? "#7a8597" : "#8a94a6")}">${a}</text>`; }).join("") : ""}</svg>`;
  }
  const BROAD = [0.95, 0.78, 0.5, 0.12, 0.1, 0.12, 0.08, 0.15], BITTER = [0.35, 0.22, 0.92, 0.95, 0.3, 0.18, 0.1, 0.25], LALA = [0.7, 0.35, 0.78, 0.72, 0.15, 0.12, 0.05, 0.1];

  const EP = 43 * 60, T = (tc) => { const [m, s] = tc.split(":").map(Number); return ((m * 60 + s) / EP) * 100; };
  function timeline(h, { segs = [], marks = [], chapters = null, flags = [], playhead = null, fs = 14, scale = true, light = false } = {}) {
    const S = segs.map(([a, b, l, col]) => `<div class="seg" style="left:${T(a)}%;width:${T(b) - T(a)}%;background:${col};color:#fff;font-size:${fs}px">${T(b) - T(a) > 7 ? l : ""}</div>`).join("");
    const C = chapters ? chapters.map(([a, b, name], i) => `<div class="seg" style="left:${T(a)}%;width:calc(${T(b) - T(a)}% - 3px);background:${i % 2 ? "#2c4270" : "#24365a"};color:#dbe5ff;font-size:${fs}px">${name}</div>`).join("") : "";
    const M = [...marks, ...flags].map(([tc, col]) => `<div class="marker" style="left:calc(${T(tc)}% - 3px);background:${col};box-shadow:0 0 14px ${col}"></div>`).join("");
    const ph = playhead ? `<div class="playhead" style="left:${T(playhead)}%"></div>` : "";
    const sc = scale ? `<div class="row tc" style="justify-content:space-between;margin-top:9px;font-size:${fs - 1}px;color:${light ? "#7a8597" : "#7d889b"}">${["00:00", "10:00", "20:00", "30:00", "43:00"].map((t) => `<span>${t}</span>`).join("")}</div>` : "";
    return `<div><div class="timeline" style="height:${h}px">${C}${S}${M}${ph}</div>${sc}</div>`;
  }
  function zoom(w, fs) {
    const pc = (tc) => { const [m, s] = tc.split(":").map(Number); return ((m * 60 + s) / 180) * 100; };
    return `<div style="width:${w}px"><div class="tc" style="font-size:${fs - 2}px;color:#7d889b;margin-bottom:6px">ZOOM · 00:00–03:00</div>
      <div class="timeline" style="height:${fs * 2.8}px">
      <div class="seg" style="left:0;width:${pc("01:12")}%;background:#3360d0;color:#fff;font-size:${fs}px">RECAP</div>
      <div class="seg" style="left:${pc("01:12")}%;width:${pc("02:05") - pc("01:12")}%;background:#5a7fe0;color:#fff;font-size:${fs}px">INTRO</div>
      <div class="seg" style="left:${pc("02:05")}%;width:${100 - pc("02:05")}%;color:#7d889b;font-size:${fs}px">EPISODE</div>
      <div class="playhead" style="left:${pc("01:31")}%"></div></div></div>`;
  }
  function player(w, h, name, { at = "14:37", skip = false, fs = 15, pos = "50% 40%", extra = "" } = {}) {
    return img(name, `width:${w}px;height:${h}px`, pos, `
      <div class="abs tc" style="left:16px;top:14px;font-size:${fs - 2}px;letter-spacing:.06em;color:rgba(255,255,255,.9);text-shadow:0 1px 6px #000">S1 E4 · 43:00</div>
      ${skip ? `<span class="abs" style="right:18px;bottom:56px;background:rgba(255,255,255,.94);color:#0b131c;font-weight:600;font-size:${fs + 4}px;padding:10px 18px;border-radius:10px">Skip Intro ⏭</span>` : ""}
      <div class="abs" style="left:0;right:0;bottom:0;height:70px;background:linear-gradient(0deg,rgba(0,0,0,.7),transparent)"></div>
      <div class="abs row" style="left:16px;right:16px;bottom:14px;align-items:center;gap:12px"><span style="color:#fff;font-size:${fs + 2}px">▶</span>
        <div style="flex:1;height:4px;border-radius:2px;background:rgba(255,255,255,.3)"><div style="width:${T(at)}%;height:4px;border-radius:2px;background:#fff"></div></div>
        <span class="tc" style="color:#fff;font-size:${fs - 1}px">${at} / 43:00</span></div>${extra}`);
  }
  function search(q, h, fs, go = "Search library") {
    return `<div class="search" style="height:${h}px;padding:0 ${h * 0.28}px"><span style="font-size:${fs * 1.15}px;color:var(--blue)">⌕</span>
      <span class="q" style="font-size:${fs}px">${q}</span><span class="caret"></span><span class="go" style="font-size:${fs * 0.68}px;padding:${h * 0.14}px ${h * 0.24}px">${go}</span></div>`;
  }
  function phone(w, name, pos, caption) {
    const h = Math.round(w * 2.05);
    return `<div style="position:relative;width:${w}px;height:${h}px;border-radius:${w * 0.13}px;background:#05070b;padding:${w * 0.035}px;box-shadow:0 30px 80px rgba(0,0,0,.6),inset 0 0 0 2px rgba(255,255,255,.14)">
      ${img(name, `width:100%;height:100%;border-radius:${w * 0.1}px`, pos, `
        <div class="abs" style="left:50%;top:${w * 0.03}px;transform:translateX(-50%);width:${w * 0.3}px;height:${w * 0.07}px;border-radius:99px;background:#000"></div>
        <div class="abs col" style="right:${w * 0.05}px;bottom:${w * 0.45}px;gap:${w * 0.07}px">${["♥", "✉", "↗"].map((i) => `<span style="width:${w * 0.12}px;height:${w * 0.12}px;border-radius:50%;background:rgba(0,0,0,.4);display:grid;place-items:center;color:#fff;font-size:${w * 0.06}px">${i}</span>`).join("")}</div>
        <div class="abs" style="left:0;right:0;bottom:0;height:40%;background:linear-gradient(0deg,rgba(0,0,0,.75),transparent)"></div>
        <div class="abs" style="left:${w * 0.06}px;right:${w * 0.22}px;bottom:${w * 0.1}px;color:#fff;font-size:${w * 0.05}px;line-height:1.35"><b>@yourchannel</b><br>${caption}</div>`)}</div>`;
  }

  // ======================================================================== AD 0  AI built for entertainment
  const SHAW_TAGS = (fs) => tags(["Mood: Hopeful", "Scene: Prison yard, day", "Emotion: Anticipation"], "mood", fs, `${fs * 0.4}px ${fs * 0.7}px`);
  add("a0-L", "ad0", "L", `
    <div class="abs bg" data-img="r-shaw" data-pos="50% 35%" style="inset:0"></div>
    <div class="abs bg" style="inset:0;background:linear-gradient(90deg,rgba(11,19,28,.95) 0%,rgba(11,19,28,.75) 40%,rgba(11,19,28,.1) 75%),linear-gradient(0deg,rgba(11,19,28,.9),rgba(11,19,28,0) 50%)"></div>
    ${top("For streamers & broadcasters")}
    <h1 style="margin-top:34px;width:560px">Generic AI sees pixels. <span class="hl">Ours understands stories.</span></h1>
    <div class="abs" style="left:0;top:330px">${arc(1200, 150, 13, "l")}</div>
    <div class="abs row" style="left:470px;top:470px;gap:8px">${SHAW_TAGS(15)}</div>
    ${foot()}`);

  add("a0-S", "ad0", "S", `
    <div class="abs" style="left:0;top:0;width:1080px;height:640px">${img("r-shaw", "width:1080px;height:640px;border-radius:0", "50% 30%")}</div>
    <div class="abs" style="left:0;top:0;width:1080px;height:640px;background:linear-gradient(180deg,rgba(11,19,28,.85),rgba(11,19,28,0) 26%,rgba(11,19,28,0) 55%,#0b131c 100%)"></div>
    ${top("For streamers & broadcasters")}
    <div class="abs" style="left:0;top:430px">${arc(1080, 170, 14, "s")}</div>
    <div class="abs" style="left:72px;right:72px;top:672px">
      <div class="row" style="align-items:baseline;gap:22px"><span class="panel-title" style="width:180px;flex:none;color:var(--faint)">Generic AI</span><h1 style="font-size:50px;color:#7d889b;font-weight:600">two men, wall, sitting.</h1></div>
      <div style="height:1px;background:var(--panel-edge);margin:24px 0"></div>
      <div class="row" style="align-items:baseline;gap:22px"><span class="panel-title" style="width:180px;flex:none;color:var(--sky)">Vionlabs</span><h1 style="font-size:50px">the moment <span class="hl">hope comes back.</span></h1></div></div>
    ${foot()}`);

  // rights-safe: the same idea on our own footage
  const DAWN_TAGS = (fs) => tags(["Mood: Hopeful", "Scene: Hilltop, dawn", "Emotion: Relief"], "mood", fs, `${fs * 0.4}px ${fs * 0.7}px`);
  add("a0r-L", "ad0", "L", `
    <div class="abs bg" data-img="g-dawn" data-pos="50% 50%" style="inset:0"></div>
    <div class="abs bg" style="inset:0;background:linear-gradient(90deg,rgba(11,19,28,.95) 0%,rgba(11,19,28,.75) 40%,rgba(11,19,28,.1) 75%),linear-gradient(0deg,rgba(11,19,28,.9),rgba(11,19,28,0) 50%)"></div>
    ${top("For streamers & broadcasters")}
    <h1 style="margin-top:34px;width:560px">Generic AI sees pixels. <span class="hl">Ours understands stories.</span></h1>
    <div class="abs" style="left:0;top:330px">${arc(1200, 150, 13, "lr")}</div>
    <div class="abs row" style="left:470px;top:470px;gap:8px">${DAWN_TAGS(15)}</div>
    ${foot()}`);
  add("a0r-S", "ad0", "S", `
    <div class="abs" style="left:0;top:0;width:1080px;height:640px">${img("g-dawn", "width:1080px;height:640px;border-radius:0", "50% 55%")}</div>
    <div class="abs" style="left:0;top:0;width:1080px;height:640px;background:linear-gradient(180deg,rgba(11,19,28,.85),rgba(11,19,28,0) 26%,rgba(11,19,28,0) 55%,#0b131c 100%)"></div>
    ${top("For streamers & broadcasters")}
    <div class="abs" style="left:0;top:430px">${arc(1080, 170, 14, "sr")}</div>
    <div class="abs" style="left:72px;right:72px;top:672px">
      <div class="row" style="align-items:baseline;gap:22px"><span class="panel-title" style="width:180px;flex:none;color:var(--faint)">Generic AI</span><h1 style="font-size:50px;color:#7d889b;font-weight:600">person, hill, sky.</h1></div>
      <div style="height:1px;background:var(--panel-edge);margin:24px 0"></div>
      <div class="row" style="align-items:baseline;gap:22px"><span class="panel-title" style="width:180px;flex:none;color:var(--sky)">Vionlabs</span><h1 style="font-size:50px">the moment <span class="hl">hope comes back.</span></h1></div></div>
    ${foot()}`);

  const card = (n, of, aud, head, fact, visual, { cta = false, size = 76, light = false } = {}) => `${top(aud, light)}
    <div class="count" style="margin-top:40px">${String(n).padStart(2, "0")} / ${String(of).padStart(2, "0")}</div>
    <h1 style="margin-top:12px;font-size:${size}px;width:930px">${head}</h1>
    ${fact ? `<p class="sub" style="margin-top:16px;width:936px;font-size:26px">${fact}</p>` : ""}${visual}${foot(cta)}`;

  add("a0-c1", "ad0", "S", card(1, 5, "Our story", "We’re from <span class=\"hl\">entertainment.</span>", "Founded in Stockholm in 2016 by people from film and VFX.", `
    <div class="abs" style="left:72px;top:420px;width:936px;height:500px">${img("r-skyfall-2", "width:936px;height:500px", "50% 35%", `
      <div class="abs" style="inset:36px 54px;border:2px solid rgba(255,255,255,.6)"></div>
      <div class="abs" style="left:50%;top:50%;width:70px;height:70px;transform:translate(-50%,-50%);border:2px solid rgba(255,255,255,.75)"></div>
      <div class="abs tc row" style="left:72px;top:52px;gap:10px;align-items:center;color:#fff;font-size:20px"><span style="width:14px;height:14px;border-radius:50%;background:#ff4a4a;box-shadow:0 0 12px #ff4a4a"></span>REC</div>
      <div class="abs tc" style="right:72px;top:52px;color:#fff;font-size:20px">TC 01:12:44:07</div>
      <div class="abs tc" style="left:72px;bottom:52px;color:rgba(255,255,255,.85);font-size:18px">ISO 800 · 35mm · T2.8</div>
      <div class="abs tc" style="right:72px;bottom:52px;color:rgba(255,255,255,.85);font-size:18px">2.39 : 1</div>`)}</div>`));
  // a0-c1r: the same card on our own footage
  add("a0-c1r", "ad0", "S", card(1, 5, "Our story", "We’re from <span class=\"hl\">entertainment.</span>", "Founded in Stockholm in 2016 by people from film and VFX.", `
    <div class="abs" style="left:72px;top:420px;width:936px;height:500px">${img("g-city", "width:936px;height:500px", "50% 60%", `
      <div class="abs" style="inset:36px 54px;border:2px solid rgba(255,255,255,.6)"></div>
      <div class="abs" style="left:50%;top:50%;width:70px;height:70px;transform:translate(-50%,-50%);border:2px solid rgba(255,255,255,.75)"></div>
      <div class="abs tc row" style="left:72px;top:52px;gap:10px;align-items:center;color:#fff;font-size:20px"><span style="width:14px;height:14px;border-radius:50%;background:#ff4a4a;box-shadow:0 0 12px #ff4a4a"></span>REC</div>
      <div class="abs tc" style="right:72px;top:52px;color:#fff;font-size:20px">TC 01:12:44:07</div>
      <div class="abs tc" style="left:72px;bottom:52px;color:rgba(255,255,255,.85);font-size:18px">ISO 800 · 35mm · T2.8</div>
      <div class="abs tc" style="right:72px;bottom:52px;color:rgba(255,255,255,.85);font-size:18px">2.39 : 1</div>`)}</div>`));

  const hand = (t, x, y, rot = -3, col = "#ffd166", fs = 34) => `<div class="hand" style="left:${x}px;top:${y}px;transform:rotate(${rot}deg);font-size:${fs}px;color:${col}">${t}</div>`;
  add("a0-c2", "ad0", "S", card(2, 5, "Our story", "We started <span class=\"hl\">by hand.</span>", "We analysed content manually before we automated anything.", `
    <div class="abs" style="left:72px;top:430px;width:936px;height:360px;background:#05070a;border-radius:12px;padding:44px 16px">
      <div class="abs row" style="left:0;right:0;top:12px;justify-content:space-around;gap:0">${Array.from({ length: 16 }, () => '<span style="width:22px;height:16px;border-radius:3px;background:#1d222b"></span>').join("")}</div>
      <div class="abs row" style="left:0;right:0;bottom:12px;justify-content:space-around;gap:0">${Array.from({ length: 16 }, () => '<span style="width:22px;height:16px;border-radius:3px;background:#1d222b"></span>').join("")}</div>
      <div class="row" style="gap:10px">${[["r-shaw", "20% 50%"], ["r-shaw", "75% 50%"], ["r-pap", "40% 40%"], ["r-suc", "30% 40%"], ["r-suc", "80% 40%"]].map(([n, p]) => img(n, "width:172px;height:272px;border-radius:4px", p)).join("")}</div></div>
    <svg class="abs" style="left:72px;top:400px" width="936" height="440"><path d="M10 320 C120 300 180 120 300 150 S 460 300 520 260 S 700 30 800 60 S 900 200 930 210" fill="none" stroke="#ffd166" stroke-width="5" stroke-linecap="round"/>
      <ellipse cx="546" cy="250" rx="80" ry="58" fill="none" stroke="#ffd166" stroke-width="4"/></svg>
    ${hand("calm…", 100, 800, -4)}${hand("tension builds", 250, 846, 2)}${hand("turning point!", 520, 812, -2, "#ff9c8a")}${hand("she knows", 770, 846, 3)}`));

  const node = (label, inner, x, y, w, h) => `<div class="panel abs" style="left:${x}px;top:${y}px;width:${w}px;height:${h}px;padding:16px 18px;border-radius:16px"><div class="panel-title" style="font-size:15px">${label}</div>${inner}</div>`;
  const wave = (w, h, n = 60) => { let s = 3; const r = () => ((s = (s * 9301 + 49297) % 233280) / 233280); return `<svg width="${w}" height="${h}">${Array.from({ length: n }, (_, i) => { const v = (0.15 + r() * 0.85) * (0.5 + 0.5 * Math.sin(i / 5)); return `<rect x="${(i * w) / n}" y="${h / 2 - (v * h) / 2}" width="${w / n - 2}" height="${v * h}" rx="2" fill="#6f9bff"/>`; }).join("")}</svg>`; };
  add("a0-c3", "ad0", "S", card(3, 5, "Our story", "Our own AI models <span class=\"hl\">since 2019.</span>", "Built in-house for film and TV. Not a wrapper on a general-purpose model.", `
    ${node("Visuals", img("r-shaw", "width:280px;height:108px;border-radius:8px;margin-top:10px", "50% 40%"), 72, 440, 320, 160)}
    ${node("Non-speech audio", `<div style="margin-top:14px">${wave(280, 80)}</div>`, 72, 616, 320, 145)}
    ${node("Dialogue · 99+ languages", `<div style="margin-top:10px;font-size:19px;line-height:1.45;color:#dfe5ef">“Get busy living,<br>or get busy dying.”</div>`, 72, 779, 320, 140)}
    <svg class="abs" style="left:392px;top:440px" width="100" height="480">${[80, 250, 410].map((y) => `<path d="M0 ${y} C50 ${y} 50 245 100 245" fill="none" stroke="#3d9bff" stroke-width="3" opacity=".75"/>`).join("")}</svg>
    <div class="abs" style="left:492px;top:585px;width:250px;height:200px;border-radius:18px;background:linear-gradient(135deg,#1c2b4d,#101a2e);border:2px solid #3360d0;display:flex;flex-direction:column;justify-content:center;align-items:center;text-align:center;box-shadow:0 0 60px rgba(51,96,208,.4)">
      <img src="${WHITE}" style="height:22px" alt=""><div style="font-size:22px;font-weight:600;margin-top:14px">Our own models</div><div class="tc" style="font-size:16px;color:var(--muted);margin-top:6px">80+ expert networks</div></div>
    <svg class="abs" style="left:742px;top:505px" width="80" height="360">${[60, 180, 300].map((y) => `<path d="M0 180 C40 180 40 ${y} 80 ${y}" fill="none" stroke="#e07a6d" stroke-width="3" opacity=".85"/>`).join("")}</svg>
    <div class="abs col" style="left:822px;top:540px;gap:86px">${tags(["Mood", "Emotion", "Story arc"], "mood", 24, "11px 20px")}</div>`, { size: 72 }));

  const THUMBS = ["troy", "skyfall", "lala", "king", "wick-2", "north", "peaky", "glad", "fast", "zoo", "argo", "forrest", "spy", "ticket", "kingdom", "friday",
    "samurai", "reacher", "any", "lord", "brave", "shaw", "women", "godzilla", "vacation", "xmen", "suc", "law", "upgrade", "american", "burt", "candy",
    "fanboys", "gethard", "rescue", "secret", "shaolin", "val", "kelly", "ind", "fall", "60", "spider", "darkknight", "pap"];
  const mosaic = (cols, rows, w, h, gap, off = 0) => `<div style="display:grid;grid-template-columns:repeat(${cols},${w}px);gap:${gap}px">${Array.from({ length: cols * rows }, (_, i) => img(`t-${THUMBS[(i + off) % THUMBS.length]}`, `width:${w}px;height:${h}px;border-radius:5px`)).join("")}</div>`;
  add("a0-c4", "ad0", "S", card(4, 5, "Our story", "Trained on 1M+ <span class=\"hl\">entertainment assets.</span>", "Mood, emotion and story arc, at scene and asset level.", `
    <div class="abs" style="left:72px;top:420px;width:936px;height:520px;overflow:hidden;border-radius:12px;-webkit-mask-image:linear-gradient(180deg,#000 72%,transparent)">${mosaic(9, 9, 96, 54, 8, 3)}</div>
    <div class="abs" style="left:420px;top:500px;width:430px;background:#0f1824;border:2px solid #3d9bff;border-radius:16px;overflow:hidden;box-shadow:0 30px 80px rgba(0,0,0,.75)">
      ${img("r-pap", "width:426px;height:220px;border-radius:0", "50% 40%")}
      <div style="padding:16px 18px"><div style="font-size:21px;font-weight:600">Scene 14 · 01:31:08</div>
      <div class="row" style="gap:8px;margin-top:12px;flex-wrap:wrap">${tags(["longing", "resolve"], "mood", 17)}${tags(["Turning point"], "genre", 17)}</div></div></div>`, { size: 72 }));
  // a0-c4r: the highlighted scene is our own footage; the library around it stays small
  add("a0-c4r", "ad0", "S", card(4, 5, "Our story", "Trained on 1M+ <span class=\"hl\">entertainment assets.</span>", "Mood, emotion and story arc, at scene and asset level.", `
    <div class="abs" style="left:72px;top:420px;width:936px;height:520px;overflow:hidden;border-radius:12px;-webkit-mask-image:linear-gradient(180deg,#000 72%,transparent)">${mosaic(9, 9, 96, 54, 8, 3)}</div>
    <div class="abs" style="left:420px;top:500px;width:430px;background:#0f1824;border:2px solid #3d9bff;border-radius:16px;overflow:hidden;box-shadow:0 30px 80px rgba(0,0,0,.75)">
      ${img("g-sea", "width:426px;height:220px;border-radius:0", "62% 62%")}
      <div style="padding:16px 18px"><div style="font-size:21px;font-weight:600">Scene 14 · 01:31:08</div>
      <div class="row" style="gap:8px;margin-top:12px;flex-wrap:wrap">${tags(["longing", "resolve"], "mood", 17)}${tags(["Turning point"], "genre", 17)}</div></div></div>`, { size: 72 }));

  add("a0-c5", "ad0", "S", card(5, 5, "Our story", "In production with <span class=\"hl\">global entertainment leaders.</span>", "", `
    <div class="abs row" style="left:72px;top:450px;gap:80px"><div class="stat"><b style="font-size:130px;color:var(--blue-hi)">60+</b><span style="font-size:28px">countries</span></div>
      <div class="stat"><b style="font-size:130px;color:var(--blue-hi)">500M</b><span style="font-size:28px">viewers</span></div></div>
    <div class="abs" style="left:72px;right:72px;top:730px;display:grid;grid-template-columns:repeat(4,1fr);gap:18px">${Array.from({ length: 4 }, () => '<div class="placeholder-logo" style="height:100px;font-size:17px">Approved logo</div>').join("")}</div>`, { size: 72, cta: true }));
  // a0-c5b: the same end card without the logo placeholders, for launch until there is an approved logo list
  add("a0-c5b", "ad0", "S", card(5, 5, "Our story", "In production with <span class=\"hl\">global entertainment leaders.</span>", "", `
    <div class="abs row" style="left:72px;top:520px;gap:80px"><div class="stat"><b style="font-size:150px;color:var(--blue-hi)">60+</b><span style="font-size:30px">countries</span></div>
      <div class="stat"><b style="font-size:150px;color:var(--blue-hi)">500M</b><span style="font-size:30px">viewers</span></div></div>`, { size: 72, cta: true }));

  // ======================================================================== AD 1  Same genre. Different movie.
  const comedy = (name, title, vals, emph, w, h, rs, fs, light) => `<div class="col" style="align-items:center;gap:12px">
      ${img(name, `width:${w}px;height:${h}px`)}<div style="font-size:${fs + 2}px;font-weight:600">${title}</div><span class="tag genre" style="font-size:${fs}px;padding:6px 14px">Genre: Comedy</span>
      ${radar(vals, rs, { emph, fs: fs - 2, light })}</div>`;
  add("a1-L", "ad1", "L", `${glow("width:520px;height:420px;right:-120px;top:120px;background:rgba(51,96,208,.35)")}
    ${top("For AI & ML teams")}
    <h1 style="margin-top:40px;width:420px">Same genre. <span class="hl">Completely different movie.</span></h1>
    <div class="abs row" style="left:540px;top:96px;gap:60px">
      ${comedy("t-vacation", "Vacation Friends", BROAD, ["Enjoyment", "Surprise"], 250, 140, 200, 15)}
      ${comedy("t-zoo", "We Bought a Zoo", BITTER, ["Sadness", "Anticipation"], 250, 140, 200, 15)}</div>
    ${foot()}`);
  add("a1-S", "ad1", "S", `${glow("width:700px;height:500px;right:-200px;top:300px;background:rgba(51,96,208,.3)")}
    ${top("For AI & ML teams")}
    <h1 style="margin-top:44px;width:930px;font-size:76px">Same genre. <span class="hl">Completely different movie.</span></h1>
    <div class="abs row" style="left:72px;right:72px;top:352px;justify-content:space-around">
      ${comedy("t-vacation", "Vacation Friends", BROAD, ["Enjoyment", "Surprise"], 380, 214, 280, 19)}
      ${comedy("t-zoo", "We Bought a Zoo", BITTER, ["Sadness", "Anticipation"], 380, 214, 280, 19)}</div>
    ${foot()}`);

  function clusters(w, h, tw, th, fs) {
    const C = [["Cozy", 0.04, 0.06, ["ticket", "women", "any", "lala"]], ["Tense", 0.54, 0.06, ["skyfall", "wick-2", "reacher", "law"]],
      ["Bittersweet", 0.04, 0.54, ["forrest", "shaw", "pap", "kelly"]], ["Euphoric", 0.54, 0.54, ["vacation", "gethard", "fanboys", "american"]]];
    const spots = [[0, 0.1], [0.55, 0], [0.12, 0.62], [0.62, 0.55]], qw = w * 0.46, qh = h * 0.46 - fs * 2;
    let out = "", pts = {};
    C.forEach(([label, cx, cy, items]) => {
      out += `<div class="abs" style="left:${cx * w}px;top:${cy * h - fs * 0.4}px;font-size:${fs}px;font-weight:700;letter-spacing:.12em;color:var(--sky)">${label.toUpperCase()}</div>`;
      items.forEach((t, i) => { const x = cx * w + spots[i][0] * (qw - tw), y = cy * h + fs * 1.6 + spots[i][1] * (qh - th); pts[t] = [x + tw / 2, y + th / 2];
        out += img(`t-${t}`, `position:absolute;left:${x}px;top:${y}px;width:${tw}px;height:${th}px;border-radius:7px;${t === "forrest" ? "outline:4px solid #3d9bff;z-index:2" : ""}`); });
    });
    const lines = ["shaw", "pap", "kelly"].map((t) => `<line x1="${pts.forrest[0]}" y1="${pts.forrest[1]}" x2="${pts[t][0]}" y2="${pts[t][1]}" stroke="#3d9bff" stroke-width="3" stroke-dasharray="6 6"/>`).join("");
    return `<div style="position:relative;width:${w}px;height:${h}px"><svg class="abs" style="left:0;top:0;z-index:1" width="${w}" height="${h}">${lines}</svg>${out}</div>`;
  }
  add("a1b-L", "ad1", "L", `
    ${top("For AI & ML teams")}
    <h1 style="margin-top:40px;width:450px">Recommendations are only as good as <span class="hl">the embeddings.</span></h1>
    <div class="abs" style="left:560px;top:96px">${clusters(580, 430, 118, 66, 14)}</div>
    ${foot()}`);
  add("a1b-S", "ad1", "S", `
    ${top("For AI & ML teams")}
    <h1 style="margin-top:44px;width:936px;font-size:70px">Recommendations are only as good as <span class="hl">the embeddings.</span></h1>
    <div class="abs" style="left:72px;top:380px">${clusters(936, 520, 180, 101, 18)}</div>
    ${foot()}`);

  // ======================================================================== AD 2  Make every asset come alive
  const FEEL = [["ticket", "Ticket to Paradise"], ["vacation", "Vacation Friends"], ["women", "What Women Want"], ["any", "Anyone But You"], ["zoo", "We Bought a Zoo"], ["american", "American Wedding"]];
  const feelGrid = (w, h, fs, gap) => `<div style="display:grid;grid-template-columns:repeat(3,${w}px);gap:${gap}px">${FEEL.map(([t], i) => `<div class="col" style="gap:9px">${img(`t-${t}`, `width:${w}px;height:${h}px;border-radius:10px`)}
    <div class="row" style="gap:6px">${tags(i % 2 ? ["Feel-good", "Funny"] : ["Romantic", "Feel-good"], "mood", fs, `${fs * 0.35}px ${fs * 0.65}px`)}</div></div>`).join("")}</div>`;
  add("a2-c1", "ad2", "S", card(1, 5, "For product & content ops", "Thousands of titles. <span class=\"hl\">How many does anyone actually find?</span>", "", `
    <div class="abs" style="left:72px;top:450px;display:grid;grid-template-columns:repeat(9,96px);gap:10px">${Array.from({ length: 36 }, (_, i) => [3, 14, 22, 31].includes(i)
      ? img(`t-${THUMBS[i]}`, "width:96px;height:96px;border-radius:8px;box-shadow:0 0 0 2px rgba(255,255,255,.7)")
      : `<div style="width:96px;height:96px;border-radius:8px;background:#18212d;display:grid;align-content:end;padding:10px;gap:6px"><span style="height:6px;width:60%;border-radius:3px;background:#273141"></span><span style="height:6px;width:40%;border-radius:3px;background:#273141"></span></div>`).join("")}</div>`, { size: 70 }));
  add("a2-c2", "ad2", "S", card(2, 5, "For product & content ops", "Search the whole library <span class=\"hl\">by mood.</span>", "", `
    <div class="abs" style="left:72px;right:72px;top:374px">${search("feel-good comedies with a happy ending", 80, 26, "Search")}</div>
    <div class="abs" style="left:72px;top:486px">${feelGrid(296, 160, 17, 22)}</div>`, { size: 70 }));
  const SWORD = [["troy", "Troy", "01:42:10", "50% 40%"], ["glad", "Gladiator", "02:11:36", "60% 40%"], ["kingdom", "Kingdom of Heaven", "01:58:04", "50% 40%"], ["samurai", "The Last Samurai", "02:04:51", "50% 40%"]];
  add("a2-c3", "ad2", "S", card(3, 5, "For product & content ops", "Search down <span class=\"hl\">to the scene.</span>", "", `
    <div class="abs" style="left:72px;right:72px;top:320px">${search("epic sword fights", 84, 27)}</div>
    <div class="abs" style="left:72px;right:72px;top:440px;display:grid;grid-template-columns:repeat(2,1fr);gap:20px">${SWORD.map(([t, name, tc, pos]) => `<div>${img(`r-${t}`, "width:458px;height:200px;border-radius:12px", pos, `<span class="badge tc" style="font-size:16px">${tc}</span>`)}<div style="font-size:22px;font-weight:600;margin-top:9px">${name}</div></div>`).join("")}</div>`, { size: 70 }));
  // a2-c3r: six smaller scenes, so no single title is big
  const SWORD6 = [...SWORD, ["north", "The Northman", "01:47:22", "50% 40%"], ["brave", "Braveheart", "02:21:05", "50% 40%"]];
  add("a2-c3r", "ad2", "S", card(3, 5, "For product & content ops", "Search down <span class=\"hl\">to the scene.</span>", "", `
    <div class="abs" style="left:72px;right:72px;top:320px">${search("epic sword fights", 84, 27)}</div>
    <div class="abs" style="left:72px;top:440px;display:grid;grid-template-columns:repeat(3,296px);gap:22px 24px">${SWORD6.map(([t, name, tc, pos]) => `<div>${img(`r-${t}`, "width:296px;height:166px;border-radius:12px", pos, `<span class="badge tc" style="font-size:15px">${tc}</span>`)}<div style="font-size:20px;font-weight:600;margin-top:8px">${name}</div></div>`).join("")}</div>`, { size: 70 }));
  add("a2-c4", "ad2", "S", card(4, 5, "For product & content ops", "Set the recipe once. <span class=\"hl\">Get every asset.</span>", "", `
    <div class="ui" style="left:72px;top:380px;width:400px;height:290px"><div class="ui-bar"><img src="${WHITE}" alt=""><span class="mod">Recipe</span></div>
      <div style="padding:18px"><div class="panel-title" style="font-size:14px">Hero thumbnails</div><div class="row" style="gap:8px;flex-wrap:wrap;margin-top:14px">${tags(["Lead close-up", "Title placed", "Bright", "16:9 + 9:16"], "ghost", 17, "7px 13px")}</div>
      <div class="btn p" style="display:inline-block;margin-top:22px;padding:11px 18px;font-size:17px;border-radius:10px;background:var(--blue);color:#fff;font-weight:600">Apply to catalogue</div></div></div>
    ${arrow(486, 500)}
    <div class="abs" style="left:556px;top:360px;width:460px;height:580px">${Array.from({ length: 12 }, (_, i) => { const v = i % 4 === 3, w = v ? 96 : 200, h = v ? 170 : 112, x = (i % 3) * 140 + (v ? 40 : 0), y = Math.floor(i / 3) * 128 + (i % 2) * 14;
      return img(v ? `r-${THUMBS[i + 5]}` : `t-${THUMBS[i + 5]}`, `position:absolute;left:${x}px;top:${y}px;width:${w}px;height:${h}px;border-radius:8px;box-shadow:0 10px 30px rgba(0,0,0,.55);transform:rotate(${(i % 3 - 1) * 2}deg)`, "50% 40%", v ? '<span class="play">▶</span>' : ""); }).join("")}</div>`, { size: 70 }));
  add("a2-c5", "ad2", "S", card(5, 5, "For product & content ops", "Metadata, thumbnails and clips <span class=\"hl\">for every title.</span>", "", `
    <div class="abs" style="left:72px;top:450px;width:936px;height:420px;overflow:hidden;border-radius:12px;-webkit-mask-image:linear-gradient(180deg,#000 60%,transparent)">${mosaic(9, 6, 96, 54, 8, 11)}</div>`, { size: 76, cta: true }));
  add("a2-L", "ad2", "L", `
    ${top("For product & content ops", true)}
    <h1 style="margin-top:40px;width:430px">Your whole library. <span class="hl">Searchable by mood.</span></h1>
    <div class="abs" style="left:520px;right:56px;top:46px">${search("feel-good comedies with a happy ending", 58, 18, "Search")}</div>
    <div class="abs" style="left:520px;top:128px">${feelGrid(196, 112, 13, 14)}</div>
    ${foot()}`, true);

  // ======================================================================== AD 3  Every second, time-coded
  const SEGS = [["00:00", "01:12", "RECAP", "#3360d0"], ["01:12", "02:05", "INTRO", "#5a7fe0"], ["41:20", "43:00", "CREDITS", "#3360d0"]];
  const BREAKS = [["14:37", "#e07a6d"], ["28:51", "#e07a6d"]];
  const legend = (fs) => `<div class="row tc" style="gap:18px;flex-wrap:wrap;font-size:${fs}px;color:#c7cfdc"><span>RECAP 00:00–01:12</span><span>INTRO 01:12–02:05</span><span style="color:#f0907f">AD BREAK 14:37</span><span style="color:#f0907f">AD BREAK 28:51</span><span>CREDITS 41:20</span></div>`;
  add("a3-L", "ad3", "L", `
    ${top("For content ops teams")}
    <h1 style="margin-top:40px;width:430px;font-size:48px">Every second of<br>your library, <span class="hl">time&#8209;coded.</span></h1>
    <div class="abs" style="left:510px;top:46px">${player(634, 270, "r-peaky", { skip: true, at: "01:31", fs: 14 })}</div>
    <div class="abs" style="left:510px;top:340px;width:634px">${zoom(634, 13)}<div style="height:14px"></div>${timeline(26, { segs: SEGS, marks: BREAKS, playhead: "01:31", fs: 12 })}<div style="margin-top:10px">${legend(12)}</div></div>
    ${foot()}`);
  add("a3-S", "ad3", "S", `
    ${top("For content ops teams")}
    <h1 style="margin-top:44px;width:930px">Every second of your library, <span class="hl">time-coded.</span></h1>
    <div class="abs" style="left:72px;top:362px">${player(936, 340, "r-peaky", { skip: true, at: "01:31", fs: 17 })}</div>
    <div class="abs" style="left:72px;top:732px;width:936px">${zoom(936, 16)}<div style="height:18px"></div>${timeline(36, { segs: SEGS, marks: BREAKS, playhead: "01:31", fs: 14 })}<div style="margin-top:14px">${legend(16)}</div></div>
    ${foot()}`);
  // rights-safe: the episode in the player is our own footage
  add("a3r-L", "ad3", "L", `
    ${top("For content ops teams")}
    <h1 style="margin-top:40px;width:430px;font-size:48px">Every second of<br>your library, <span class="hl">time&#8209;coded.</span></h1>
    <div class="abs" style="left:510px;top:46px">${player(634, 270, "g-city", { skip: true, at: "01:31", fs: 14, pos: "42% 72%" })}</div>
    <div class="abs" style="left:510px;top:340px;width:634px">${zoom(634, 13)}<div style="height:14px"></div>${timeline(26, { segs: SEGS, marks: BREAKS, playhead: "01:31", fs: 12 })}<div style="margin-top:10px">${legend(12)}</div></div>
    ${foot()}`);
  add("a3r-S", "ad3", "S", `
    ${top("For content ops teams")}
    <h1 style="margin-top:44px;width:930px">Every second of your library, <span class="hl">time-coded.</span></h1>
    <div class="abs" style="left:72px;top:362px">${player(936, 340, "g-city", { skip: true, at: "01:31", fs: 17, pos: "42% 72%" })}</div>
    <div class="abs" style="left:72px;top:732px;width:936px">${zoom(936, 16)}<div style="height:18px"></div>${timeline(36, { segs: SEGS, marks: BREAKS, playhead: "01:31", fs: 14 })}<div style="margin-top:14px">${legend(16)}</div></div>
    ${foot()}`);
  add("a3b-L", "ad3", "L", `${glow("width:600px;height:400px;right:-100px;top:100px;background:rgba(51,96,208,.35)")}
    ${top("For content ops teams")}
    <div class="abs row" style="left:56px;top:130px;align-items:flex-end;gap:60px">
      <div class="stat"><b style="font-size:150px;color:#4b5567;position:relative">278 days<span class="abs" style="left:-8px;right:-8px;top:50%;height:10px;background:#e07a6d;border-radius:5px;transform:rotate(-4deg)"></span></b><span>of manual tagging</span></div>
      <div class="stat"><b style="font-size:150px;color:var(--blue-hi)">7 days</b><span>with Vionlabs</span></div></div>
    <p class="abs sub" style="left:56px;top:420px;font-size:24px;color:var(--text)">65,000 episodes, fully marked.</p>
    ${foot()}`);
  add("a3b-S", "ad3", "S", `${glow("width:700px;height:500px;right:-150px;top:400px;background:rgba(51,96,208,.35)")}
    ${top("For content ops teams")}
    <div class="abs stat" style="left:72px;top:220px"><b style="font-size:200px;color:#4b5567;position:relative;width:fit-content">278 days<span class="abs" style="left:-10px;right:-10px;top:50%;height:14px;background:#e07a6d;border-radius:7px;transform:rotate(-4deg)"></span></b><span style="font-size:28px">of manual tagging</span></div>
    <div class="abs stat" style="left:72px;top:540px"><b style="font-size:240px;color:var(--blue-hi)">7 days</b><span style="font-size:28px">with Vionlabs</span></div>
    <p class="abs sub" style="left:72px;top:880px;color:var(--text)">65,000 episodes, fully marked.</p>
    ${foot()}`);

  // ======================================================================== M1  From zero to hero (La La Land metadata from the sales deck)
  const metaRows = (fs, gap, light) => {
    const r = (k, v) => `<div class="row" style="gap:14px;align-items:flex-start"><span class="panel-title" style="width:${fs * 6.2}px;flex:none;font-size:${fs - 4}px;padding-top:${fs * 0.4}px">${k}</span><div class="row" style="gap:8px;flex-wrap:wrap">${v}</div></div>`;
    const p = `${fs * 0.3}px ${fs * 0.65}px`, ghost = light ? "ghost" : "ghost";
    return `<div class="col" style="gap:${gap}px">
      ${r("Genres", tags(["Music", "Drama", "Romance"], "genre", fs - 2, p))}
      ${r("Moods", tags(["Romantic", "Inspiring", "Uplifting", "Hopeful"], "mood", fs - 2, p))}
      ${r("Keywords", tags(["singer", "musical", "performance", "dance", "dream", "songwriter"], ghost, fs - 2, p, `color:${light ? "#0e1720" : "#dfe5ef"};border-color:${light ? "#c9d2e3" : "rgba(255,255,255,.2)"}`))}
      ${r("Category", tags(["Emotional & Inspiring"], "blue", fs - 2, p))}
      ${r("Summary", `<span style="font-size:${fs}px;line-height:1.4">An aspiring actress and a jazz musician fall in love while chasing their dreams in Los Angeles.</span>`)}</div>`;
  };
  add("m1-L", "m1", "L", `
    ${top("For product & content ops", true)}
    <h1 style="margin-top:30px;font-size:46px;width:1088px">From one genre tag <span class="hl">to full metadata.</span></h1>
    <div class="abs col" style="left:56px;top:178px;gap:8px"><div class="panel-title" style="font-size:13px">What the studio gives you</div>
      ${img("t-lala", "width:250px;height:141px")}<div class="tc" style="font-size:14px;color:var(--light-muted)">La La Land · 2016 · Musical</div></div>
    ${arrow(318, 236)}
    <div class="panel abs" style="left:384px;top:170px;width:760px;height:350px;padding:18px 22px">
      <div class="panel-title" style="font-size:13px;color:var(--blue)">What Vionlabs sees</div>
      <div class="row" style="gap:12px;margin-top:12px"><div style="flex:1">${metaRows(16, 9, true)}</div>
      <div class="col" style="align-items:center;gap:2px;flex:none"><div class="panel-title" style="font-size:11px">Emotion fingerprint</div>${radar(LALA, 150, { labels: false, light: true })}</div></div></div>
    ${foot()}`, true);
  add("m1-S", "m1", "S", `
    ${top("For product & content ops", true)}
    <h1 style="margin-top:44px;width:936px;font-size:72px">From one genre tag <span class="hl">to full metadata.</span></h1>
    <div class="abs col" style="left:72px;top:360px;gap:12px;width:300px"><div class="panel-title" style="font-size:15px;line-height:1.4">What the studio<br>gives you</div>
      ${img("t-lala", "width:300px;height:169px")}<div class="tc" style="font-size:18px;color:var(--light-muted)">La La Land · 2016 · Musical</div>
      <div class="panel-title" style="font-size:14px;margin-top:40px">Emotion fingerprint</div>${radar(LALA, 220, { labels: false, light: true })}</div>
    <div class="panel abs" style="left:400px;top:360px;width:608px;height:570px;padding:26px">
      <div class="panel-title" style="font-size:16px;color:var(--blue)">What Vionlabs sees</div><div style="margin-top:22px">${metaRows(20, 20, true)}</div></div>
    ${foot()}`, true);

  // ======================================================================== M2  From library to editorial lists
  const LISTS = [["Feel-good Sunday", ["ticket", "vacation", "zoo", "women"]], ["Edge-of-your-seat thrillers", ["skyfall", "wick-2", "reacher", "law"]], ["Underdog stories", ["king", "friday", "shaolin", "rescue"]],
    ["Epic battles", ["troy", "glad", "kingdom", "samurai"]], ["Hidden gems", ["kelly", "burt", "candy", "upgrade"]]];
  const rows = (n, tw, th, fs, gap, partial = false) => `<div class="col" style="gap:${gap}px">${LISTS.slice(0, n).map(([name, items], r) => `<div><div style="font-size:${fs}px;font-weight:600;margin-bottom:${gap * 0.5}px">${name}</div><div class="row" style="gap:${gap * 0.6}px">${items.map((t, i) =>
    partial && i > (r % 3) + 1 ? `<div style="width:${tw}px;height:${th}px;border-radius:6px;background:#18212d;border:1.5px dashed #2f3a4c"></div>` : img(`t-${t}`, `width:${tw}px;height:${th}px;border-radius:6px`)).join("")}</div></div>`).join("")}</div>`;
  const chaos = (n, w, h, tw, th, seed = 1) => { let s = seed; const r = () => ((s = (s * 9301 + 49297) % 233280) / 233280);
    return `<div style="position:relative;width:${w}px;height:${h}px">${Array.from({ length: n }, (_, i) => img(`t-${THUMBS[(i * 7 + seed) % THUMBS.length]}`, `position:absolute;left:${r() * (w - tw)}px;top:${r() * (h - th)}px;width:${tw}px;height:${th}px;border-radius:5px;transform:rotate(${(r() - 0.5) * 30}deg);box-shadow:0 6px 18px rgba(0,0,0,.6);opacity:${0.55 + r() * 0.45}`)).join("")}</div>`; };
  const coverage = (fs) => `<div class="row" style="align-items:center;gap:14px"><span class="tc" style="font-size:${fs}px;color:var(--muted)">Library coverage</span><div style="width:${fs * 9}px;height:${fs * 0.55}px;border-radius:99px;background:#1a2433"><div style="width:90%;height:100%;border-radius:99px;background:linear-gradient(90deg,#3360d0,#3d9bff)"></div></div><span class="tc" style="font-size:${fs * 1.3}px;font-weight:700;color:var(--text)">90%</span></div>`;
  add("m2-L", "m2", "L", `
    ${top("For editorial teams")}
    <h1 style="margin-top:40px;width:400px">Every title <span class="hl">in a list.</span></h1>
    <div class="abs" style="left:56px;top:250px">${chaos(18, 360, 230, 96, 54, 3)}</div>
    ${arrow(440, 360)}
    <div class="abs" style="left:520px;top:92px">${rows(5, 112, 56, 14, 10)}</div>
    <div class="abs" style="left:56px;top:494px">${coverage(14)}</div>
    ${foot()}`);
  add("m2-S", "m2", "S", `
    ${top("For editorial teams")}
    <h1 style="margin-top:44px">Every title <span class="hl">in a list.</span></h1>
    <div class="abs" style="left:56px;top:270px">${chaos(26, 340, 600, 120, 68, 4)}</div>
    ${arrow(400, 560)}
    <div class="abs" style="left:470px;top:260px">${rows(5, 125, 70, 19, 15)}</div>
    <div class="abs" style="left:470px;top:900px">${coverage(18)}</div>
    ${foot()}`);
  add("m2-c1", "m2", "S", card(1, 3, "For editorial teams", "Your library, <span class=\"hl\">unsorted.</span>", "", `<div class="abs" style="left:72px;top:330px">${chaos(44, 936, 600, 150, 84, 7)}</div>`));
  add("m2-c2", "m2", "S", card(2, 3, "For editorial teams", "Lists, <span class=\"hl\">curated by AI.</span>", "", `<div class="abs" style="left:72px;top:320px">${rows(5, 210, 82, 22, 14, true)}</div>`));
  add("m2-c3", "m2", "S", card(3, 3, "For editorial teams", "90% of your library, <span class=\"hl\">in front of viewers.</span>", "", `<div class="abs" style="left:72px;top:404px">${rows(3, 210, 100, 24, 18)}</div><div class="abs" style="left:72px;top:884px">${coverage(22)}</div>`, { cta: true, size: 72 }));
  // m2b-L, m2b-S, m2-c3b: the same without the 90% coverage claim, which has no source yet
  add("m2b-L", "m2", "L", `
    ${top("For editorial teams")}
    <h1 style="margin-top:40px;width:400px">Every title <span class="hl">in a list.</span></h1>
    <div class="abs" style="left:56px;top:250px">${chaos(18, 360, 230, 96, 54, 3)}</div>
    ${arrow(440, 360)}
    <div class="abs" style="left:520px;top:92px">${rows(5, 112, 56, 14, 10)}</div>
    ${foot()}`);
  add("m2b-S", "m2", "S", `
    ${top("For editorial teams")}
    <h1 style="margin-top:44px">Every title <span class="hl">in a list.</span></h1>
    <div class="abs" style="left:56px;top:270px">${chaos(26, 340, 600, 120, 68, 4)}</div>
    ${arrow(400, 560)}
    <div class="abs" style="left:470px;top:260px">${rows(5, 125, 70, 19, 15)}</div>
    ${foot()}`);
  add("m2-c3b", "m2", "S", card(3, 3, "For editorial teams", "Every title, <span class=\"hl\">in front of viewers.</span>", "", `<div class="abs" style="left:72px;top:330px">${rows(3, 210, 100, 24, 18)}</div>`, { cta: true, size: 72 }));

  // ======================================================================== M3  Search by feeling
  const Q = [
    ["underdog stories", ["Inspiring", "Triumphant", "Against the odds"], ["king", "friday", "shaolin", "rescue"], "underdog"],
    ["feel-good romantic comedies", ["Romantic", "Funny", "Feel-good"], ["ticket", "any", "women", "lala"], "feel-good"],
    ["tense true stories", ["True story", "Gripping", "Tense"], ["argo", "rescue", "pap", "lord"], "true story"],
  ];
  const qRow = ([q, mood, items], tw, th, fs, light) => `<div><div class="row" style="align-items:center;gap:12px;margin-bottom:10px"><span style="font-size:${fs}px;font-weight:600">“${q}”</span>${tags(mood, "mood", fs - 5, `${fs * 0.22}px ${fs * 0.5}px`)}</div>
    <div class="row" style="gap:10px">${items.map((t) => img(`t-${t}`, `width:${tw}px;height:${th}px;border-radius:8px`)).join("")}</div></div>`;
  add("m3-L", "m3", "L", `
    ${top("For editorial & search teams", true)}
    <h1 style="margin-top:40px;width:420px">Search your library <span class="hl">by mood, not by title.</span></h1>
    <div class="abs col" style="left:520px;top:92px;gap:12px">${Q.map((q) => qRow(q, 145, 76, 16, true)).join("")}</div>
    ${foot()}`, true);
  add("m3-S", "m3", "S", `
    ${top("For editorial & search teams", true)}
    <h1 style="margin-top:44px;width:930px">Search your library <span class="hl">by mood, not by title.</span></h1>
    <div class="abs col" style="left:72px;top:370px;gap:22px">${Q.map((q) => qRow(q, 222, 118, 22, true)).join("")}</div>
    ${foot()}`, true);
  Q.forEach((q, i) => add(`m3-c${i + 1}`, "m3", "S", `${top("For editorial & search teams", true)}
    <div class="count" style="margin-top:40px">0${i + 1} / 04</div>
    <div class="abs" style="left:72px;right:72px;top:220px">${search(q[0], 96, 34)}</div>
    <div class="abs row" style="left:72px;top:356px;gap:10px">${tags(q[1], "mood", 24, "10px 18px")}</div>
    <div class="abs" style="left:72px;top:450px;display:grid;grid-template-columns:repeat(2,458px);gap:20px">${q[2].map((t) => img(`t-${t}`, "width:458px;height:200px;border-radius:12px")).join("")}</div>
    <p class="abs sub" style="left:72px;top:888px;font-size:24px">Matched on mood and theme, even when no metadata says “${q[3]}”.</p>
    ${foot(false)}`, true));
  // m3-c1r … m3-c3r: six smaller posters per search instead of four big ones
  const Q6 = { underdog: ["king", "friday", "shaolin", "rescue", "forrest", "shaw"], "feel-good": ["ticket", "any", "women", "lala", "secret", "american"],
    "true story": ["argo", "rescue", "pap", "lord", "kelly", "friday"] };
  Q.forEach((q, i) => add(`m3-c${i + 1}r`, "m3", "S", `${top("For editorial & search teams", true)}
    <div class="count" style="margin-top:40px">0${i + 1} / 04</div>
    <div class="abs" style="left:72px;right:72px;top:220px">${search(q[0], 96, 34)}</div>
    <div class="abs row" style="left:72px;top:356px;gap:10px">${tags(q[1], "mood", 24, "10px 18px")}</div>
    <div class="abs" style="left:72px;top:450px;display:grid;grid-template-columns:repeat(3,298px);gap:20px">${Q6[q[3]].map((t) => img(`t-${t}`, "width:298px;height:168px;border-radius:12px")).join("")}</div>
    <p class="abs sub" style="left:72px;top:888px;font-size:24px">Matched on mood and theme, even when no metadata says “${q[3]}”.</p>
    ${foot(false)}`, true));
  add("m3-c4", "m3", "S", `${top("For editorial & search teams", true)}
    <div class="count" style="margin-top:40px">04 / 04</div>
    <h1 style="margin-top:12px;font-size:110px">Type a feeling. <span class="hl">Get a list.</span></h1>
    <div class="abs col" style="left:72px;right:72px;top:500px;gap:18px">${["underdog stories", "feel-good romantic comedies", "tense true stories"].map((q, i) => `<div style="opacity:${1 - i * 0.22}">${search(q, 76, 26)}</div>`).join("")}</div>
    ${foot()}`, true);

  // ======================================================================== C1  Every asset, brought to life
  const burst = (cx, cy, sc, n = 26) => { const shapes = [[16, 9], [4, 3], [1, 1], [9, 16]]; let out = "";
    for (let i = 0; i < n; i++) { const a = (i / n) * Math.PI * 2 + 0.3, d = (170 + (i % 3) * 80) * sc, [sw, sh] = shapes[i % 4], base = 80 * sc;
      const w = sw >= sh ? base * 1.4 : base * 0.9, h = (w * sh) / sw, x = cx + Math.cos(a) * d * 1.35 - w / 2, y = cy + Math.sin(a) * d * 0.8 - h / 2;
      out += img(sh > sw ? "r-glad" : i % 2 ? "t-glad" : "r-glad", `position:absolute;left:${x}px;top:${y}px;width:${w}px;height:${h}px;border-radius:6px;box-shadow:0 8px 24px rgba(0,0,0,.6);transform:rotate(${(i % 5 - 2) * 3}deg)`, `${(i * 37) % 100}% 40%`,
        sh > sw ? '<span class="play" style="width:28px;height:28px;font-size:11px">▶</span>' : `<span class="abs tc" style="left:4px;bottom:3px;font-size:${10 * sc}px;color:#fff;text-shadow:0 0 4px #000">${sw}:${sh}</span>`); }
    return out; };
  const strip = (w, h) => `<div style="width:${w}px;height:${h}px;background:#05070a;border-radius:8px;padding:${h * 0.14}px 8px;display:flex;gap:6px;box-shadow:0 0 0 2px #3d9bff,0 0 50px rgba(61,155,255,.45)">${["10%", "30%", "50%", "70%", "90%"].map((p, i) => img(i % 2 ? "t-glad" : "r-glad", "flex:1;height:100%;border-radius:3px", `${p} 40%`)).join("")}</div>`;
  const pipeline = (fs) => `<div class="row" style="align-items:center;gap:${fs * 0.6}px">${["MAM", "Vionlabs API", "Thumbnails & clips", "Your apps"].map((t, i) => `<span class="tag ${i === 1 ? "blue" : "ghost"}" style="font-size:${fs}px;padding:${fs * 0.45}px ${fs * 0.8}px;${i === 1 ? "" : "color:var(--text)"}">${t}</span>`).join(`<span style="color:var(--sky);font-size:${fs * 1.3}px">›</span>`)}</div>`;
  add("c1-L", "c1", "L", `
    ${top("For content & engineering")}
    <h1 style="margin-top:40px;width:420px">Thumbnails and clips for every title. <span class="hl">Automatically.</span></h1>
    <div class="abs" style="left:470px;top:0;width:730px;height:627px">${burst(365, 300, 0.72)}<div class="abs" style="left:205px;top:268px">${strip(320, 64)}</div></div>
    <div class="abs" style="left:56px;top:430px">${pipeline(15)}</div>
    ${foot()}`);
  add("c1-S", "c1", "S", `
    ${top("For content & engineering")}
    <h1 style="margin-top:44px;width:930px">Thumbnails and clips for every title. <span class="hl">Automatically.</span></h1>
    <div class="abs" style="left:0;top:330px;width:1080px;height:560px">${burst(540, 270, 0.92)}<div class="abs" style="left:330px;top:228px">${strip(420, 84)}</div></div>
    <div class="abs" style="left:72px;top:880px">${pipeline(19)}</div>
    ${foot()}`);

  // ======================================================================== C2  Recipes
  const recipe = (fs) => {
    const r = (k, v) => `<div class="row" style="align-items:center;gap:12px;padding:${fs * 0.5}px 0;border-bottom:1px solid var(--panel-edge)"><span style="width:${fs * 7}px;color:var(--muted);font-size:${fs}px">${k}</span><div class="row" style="gap:8px;flex-wrap:wrap">${v}</div></div>`;
    const p = `${fs * 0.32}px ${fs * 0.7}px`;
    return `<div class="panel-title" style="font-size:${fs - 3}px;color:var(--blue-hi)">Recipe · Hero thumbnails</div><div style="margin-top:${fs * 0.4}px">
      ${r("Character", tags(["Leads"], "blue", fs - 1, p))}${r("Mood", tags(["Warm", "Uplifting"], "mood", fs - 1, p))}${r("Shot type", tags(["Medium close-up"], "ghost", fs - 1, p, "color:var(--text)"))}
      ${r("Brightness", `<div style="width:${fs * 9}px;height:6px;border-radius:3px;background:#2a3342"><div style="width:78%;height:6px;border-radius:3px;background:var(--blue)"></div></div>`)}
      ${r("Format", tags(["16:9 ✓"], "blue", fs - 1, p) + tags(["9:16"], "ghost", fs - 1, p))}${r("Title logo", tags(["Placed ✓"], "blue", fs - 1, p))}</div>`;
  };
  const OUT = ["ticket", "lala", "king", "zoo", "skyfall", "friday", "women", "north", "any", "argo", "forrest", "vacation", "secret", "troy", "pap", "suc", "reacher", "kelly"];
  const outGrid = (cols, n, w, h, gap) => `<div style="display:grid;grid-template-columns:repeat(${cols},${w}px);gap:${gap}px">${OUT.slice(0, n).map((t) => img(`t-${t}`, `width:${w}px;height:${h}px;border-radius:6px`)).join("")}</div>`;
  add("c2-L", "c2", "L", `
    ${top("For creative teams", true)}
    <h1 style="margin-top:30px;width:1088px;font-size:46px">One recipe. <span class="hl">Thumbnails for your whole catalogue.</span></h1>
    <div class="ui" style="left:56px;top:170px;width:460px;height:350px"><div class="ui-bar"><img src="${WHITE}" alt=""><span class="mod">Creative Lab</span><span class="ctx">Recipe</span></div><div style="padding:14px 18px">${recipe(15)}</div></div>
    ${arrow(534, 330)}
    <div class="abs" style="left:604px;top:170px">${outGrid(4, 16, 128, 72, 10)}</div>
    ${foot()}`, true);
  add("c2-S", "c2", "S", `
    ${top("For creative teams", true)}
    <h1 style="margin-top:44px;width:936px;font-size:70px">One recipe. <span class="hl">Thumbnails for your whole catalogue.</span></h1>
    <div class="ui" style="left:72px;top:330px;width:936px;height:270px"><div class="ui-bar"><img src="${WHITE}" alt=""><span class="mod">Creative Lab</span><span class="ctx">Recipe</span></div><div style="padding:14px 20px;columns:2;column-gap:30px">${recipe(17)}</div></div>
    <div class="abs" style="left:72px;top:630px">${outGrid(6, 18, 146, 82, 12)}</div>
    ${foot()}`, true);
  const RECIPES = [["Lead close-up · Bright · Title placed · 16:9", "t-glad", 16 / 9, ["30% 50%", "50% 50%", "70% 50%", "40% 30%"]],
    ["Tense · Battle scene · 9:16 · 15-second clip", "r-glad", 9 / 16, ["20% 50%", "55% 50%", "85% 50%"]],
    ["Mood-matched to “Epic battles”", "t-glad", 1, ["20% 50%", "45% 50%", "70% 50%", "90% 50%"]]];
  add("c2b-S", "c2", "S", `
    ${top("For creative teams")}
    <h1 style="margin-top:44px;width:930px">Same film. Three recipes. <span class="hl">Three different stories.</span></h1>
    <div class="abs row" style="left:72px;right:72px;top:340px;gap:22px">${RECIPES.map(([r, name, ar, poss], i) => `<div class="col" style="flex:1;gap:14px">
      <div class="panel" style="padding:16px;height:140px;border-radius:14px"><div class="panel-title" style="font-size:14px;color:var(--blue-hi)">Recipe ${i + 1}</div><div style="font-size:19px;line-height:1.35;margin-top:8px">${r}</div></div>
      <div style="display:grid;grid-template-columns:repeat(${ar < 1 ? 3 : 2},1fr);gap:8px">${poss.map((p) => img(name, `width:100%;aspect-ratio:${ar};border-radius:6px`, p, ar < 1 ? '<span class="play" style="width:28px;height:28px;font-size:11px">▶</span>' : "")).join("")}</div></div>`).join("")}</div>
    <div class="abs tc" style="left:72px;top:880px;font-size:18px;color:var(--muted)">GLADIATOR · ONE TITLE, THREE RESULT SETS</div>
    ${foot()}`);

  // ======================================================================== C3  Find the scene. Ship the short.
  const SCENES6 = [...SWORD, ["north", "The Northman", "01:47:22", "50% 40%"], ["brave", "Braveheart", "02:21:05", "50% 40%"]];
  const sceneGrid = (cols, n, w, h, fs, gap) => `<div style="display:grid;grid-template-columns:repeat(${cols},${w}px);gap:${gap}px">${SCENES6.slice(0, n).map(([t, name, tc, pos]) => `<div>${img(`r-${t}`, `width:${w}px;height:${h}px;border-radius:10px`, pos, `<span class="badge tc" style="font-size:${fs - 4}px">${tc}</span>`)}<div style="font-size:${fs}px;font-weight:600;margin-top:8px">${name}</div></div>`).join("")}</div>`;
  add("c3-c1", "c3", "S", card(1, 4, "For social & digital teams", "Every sword fight in your library. <span class=\"hl\">In seconds.</span>", "", `
    <div class="abs" style="left:72px;right:72px;top:480px">${search("epic sword fights", 104, 38)}</div>
    <div class="abs row" style="left:72px;top:630px;gap:12px">${tags(["scene search", "99+ languages", "whole library"], "ghost", 22, "10px 18px", "color:var(--text)")}</div>`, { size: 72 }));
  add("c3-c2", "c3", "S", card(2, 4, "For social & digital teams", "6 titles. <span class=\"hl\">Every matching moment.</span>", "", `
    <div class="abs" style="left:72px;top:390px">${sceneGrid(3, 6, 296, 200, 21, 22)}</div>`, { size: 70 }));
  add("c3-c3", "c3", "S", card(3, 4, "For social & digital teams", "16:9 in. <span class=\"hl\">9:16 out.</span>", "", `
    <div class="abs" style="left:72px;top:330px;width:580px;height:326px;overflow:hidden;border-radius:12px">${img("r-glad", "width:580px;height:326px;border-radius:12px", "50% 40%")}
      <div class="abs" style="left:300px;top:0;width:184px;height:326px;border:3px solid #3d9bff;box-shadow:0 0 0 2000px rgba(0,0,0,.5)"></div>
      <div class="abs" style="left:322px;top:40px;width:140px;height:240px;border:2px dashed #fff;border-radius:6px"></div>
      <span class="abs tc" style="left:322px;top:14px;font-size:14px;background:#fff;color:#0b131c;padding:2px 8px;border-radius:4px">character tracked</span></div>
    ${arrow(672, 470)}
    <div class="abs" style="left:752px;top:300px">${phone(250, "r-glad", "62% 40%", "Are you not entertained? ⚔️")}</div>
    <p class="abs sub" style="left:72px;top:700px;width:580px;font-size:25px">Automatic vertical conversion with character tracking. Clips arrive with summaries and tags.</p>`, { size: 72 }));
  add("c3-c4", "c3", "S", `${top("For social & digital teams")}
    <div class="count" style="margin-top:40px">04 / 04</div>
    <h1 style="margin-top:12px;width:560px;font-size:76px">Your archive is full of shorts. <span class="hl">Go find them.</span></h1>
    <div class="abs" style="left:660px;top:150px">${phone(320, "r-troy", "45% 40%", "The duel everyone waited for ⚔️ #epic")}</div>
    ${foot()}`);
  // rights-safe: the reframed clip is our own footage
  add("c3-c3r", "c3", "S", card(3, 4, "For social & digital teams", "16:9 in. <span class=\"hl\">9:16 out.</span>", "", `
    <div class="abs" style="left:72px;top:330px;width:580px;height:326px;overflow:hidden;border-radius:12px">${img("g-epic", "width:580px;height:326px;border-radius:12px", "50% 50%")}
      <div class="abs" style="left:198px;top:0;width:184px;height:326px;border:3px solid #3d9bff;box-shadow:0 0 0 2000px rgba(0,0,0,.5)"></div>
      <div class="abs" style="left:238px;top:150px;width:104px;height:150px;border:2px dashed #fff;border-radius:6px"></div>
      <span class="abs tc" style="left:212px;top:14px;font-size:14px;background:#fff;color:#0b131c;padding:2px 8px;border-radius:4px">character tracked</span></div>
    ${arrow(672, 470)}
    <div class="abs" style="left:752px;top:300px">${phone(250, "g-epic", "50% 50%", "Wait for it… ⚔️")}</div>
    <p class="abs sub" style="left:72px;top:700px;width:580px;font-size:25px">Automatic vertical conversion with character tracking. Clips arrive with summaries and tags.</p>`, { size: 72 }));
  add("c3-c4r", "c3", "S", `${top("For social & digital teams")}
    <div class="count" style="margin-top:40px">04 / 04</div>
    <h1 style="margin-top:12px;width:560px;font-size:76px">Your archive is full of shorts. <span class="hl">Go find them.</span></h1>
    <div class="abs" style="left:660px;top:150px">${phone(320, "g-epic", "50% 50%", "The moment everyone waited for ⚔️ #epic")}</div>
    ${foot()}`);
  add("c3-L", "c3", "L", `
    ${top("For social & digital teams")}
    <h1 style="margin-top:40px;width:440px">Every sword fight in your library. <span class="hl">In seconds.</span></h1>
    <div class="abs" style="left:56px;top:330px;width:420px">${search("epic sword fights", 54, 18, "Search")}</div>
    <div class="abs" style="left:510px;top:104px">${sceneGrid(2, 4, 200, 120, 14, 14)}</div>
    <div class="abs" style="left:960px;top:100px">${phone(170, "r-glad", "62% 40%", "Are you not entertained?")}</div>
    ${foot()}`);

  // ======================================================================== O1  Automate QC
  const CH = [["00:00", "11:30", "The arrival"], ["11:30", "24:00", "The argument"], ["24:00", "36:40", "The storm"], ["36:40", "43:00", "The confession"]];
  const oCard = (n, head, frame, tl, extra = "", { tlTop = 800, frTop = 330, cta = false } = {}) => `${top("For media ops & automation")}
    <div class="count" style="margin-top:40px">0${n} / 05</div><h1 style="margin-top:12px;font-size:72px;width:930px">${head}</h1>
    <div class="abs" style="left:72px;top:${frTop}px">${frame}</div><div class="abs" style="left:72px;top:${tlTop}px;width:936px">${tl}</div>${extra}${foot(cta)}`;
  add("o1-c1", "o1", "S", oCard(1, "Binge markers <span class=\"hl\">for every episode.</span>", player(936, 320, "r-peaky", { skip: true, at: "01:31", fs: 17 }),
    `${zoom(936, 16)}<div style="height:16px"></div>${timeline(34, { segs: SEGS, playhead: "01:31", fs: 14 })}<div class="row tc" style="gap:22px;margin-top:12px;font-size:16px;color:#c7cfdc"><span>RECAP 00:00–01:12</span><span>INTRO 01:12–02:05</span><span>CREDITS 41:20–43:00</span></div>`, "", { frTop: 380, tlTop: 740 }));
  const tagPanel = (tc, fs) => `<div style="background:#0f1824;border:1.5px solid rgba(224,122,109,.65);border-radius:12px;padding:${fs * 0.7}px ${fs}px;box-shadow:0 20px 50px rgba(0,0,0,.5)">
    <div class="tc" style="font-size:${fs - 1}px;color:#f0907f">AD BREAK ${tc}</div><div class="col" style="gap:${fs * 0.35}px;margin-top:${fs * 0.5}px;font-size:${fs}px">
    <span><span style="color:var(--muted)">Mood:</span> Uplifting</span><span><span style="color:var(--muted)">IAB:</span> Travel</span><span><span style="color:var(--muted)">Brand-safe:</span> <b style="color:#3ddc97">yes</b></span></div></div>`;
  add("o1-c2", "o1", "S", oCard(2, "Ad breaks that <span class=\"hl\">respect the story.</span>", player(936, 290, "r-suc", { at: "14:37", fs: 17 }),
    timeline(48, { chapters: CH, marks: BREAKS, fs: 14 }),
    `<div class="abs" style="left:${72 + (936 * T("14:37")) / 100 - 100}px;top:700px">${tagPanel("14:37", 17)}</div><div class="abs" style="left:${72 + (936 * T("28:51")) / 100 - 100}px;top:700px">${tagPanel("28:51", 17)}</div>`, { frTop: 380, tlTop: 880 }));
  add("o1-c3", "o1", "S", oCard(3, "Chapters, <span class=\"hl\">generated.</span>", player(936, 330, "r-secret", { at: "24:00", fs: 17, pos: "50% 35%" }),
    `${timeline(56, { chapters: CH, fs: 14 })}<div class="row" style="gap:14px;margin-top:20px">${[["The arrival", "She comes home after ten years."], ["The argument", "Old wounds open at dinner."], ["The storm", "The power goes out; no one leaves."], ["The confession", "She finally tells him the truth."]].map(([t, s]) => `<div class="panel" style="flex:1;padding:14px;border-radius:12px"><div style="font-size:19px;font-weight:600">${t}</div><div style="font-size:16px;color:var(--muted);margin-top:6px;line-height:1.35">${s}</div></div>`).join("")}</div>`, "", { tlTop: 700 }));
  const flagged = (w, h) => `<div style="width:${w}px;height:${h}px;border-radius:12px;background:repeating-linear-gradient(45deg,#18212d 0 14px,#212b39 14px 28px);display:grid;place-items:center;color:var(--muted);font-family:'DejaVu Sans Mono',monospace;font-size:15px;border:1.5px solid var(--panel-edge)">FLAGGED FRAME</div>`;
  add("o1-c4", "o1", "S", oCard(4, "Compliance flags, <span class=\"hl\">frame by frame.</span>", `<div class="row" style="gap:22px">${[["Nudity", "22:10", "High", "#e07a6d"], ["Profanity", "31:45", "Medium", "#f5c451"]].map(([k, tc, sev, col]) => `<div style="width:457px">${flagged(457, 250)}
      <div class="row" style="align-items:center;gap:12px;margin-top:14px"><span class="tag" style="font-size:18px;padding:7px 14px;border:1.5px solid ${col};color:${col}">${k}</span><span class="tc" style="font-size:20px;color:var(--text)">${tc}</span><span style="margin-left:auto;font-size:18px;color:var(--muted)">Severity: <b style="color:var(--text)">${sev}</b></span></div></div>`).join("")}</div>`,
    timeline(48, { chapters: CH, flags: [["22:10", "#e07a6d"], ["31:45", "#f5c451"]], fs: 14 }), "", { frTop: 380, tlTop: 790 }));
  const lanes = (fs, gap) => `<div class="col" style="gap:${gap}px">${[["Binge markers", timeline(fs * 2.2, { segs: SEGS, fs: fs - 3, scale: false })], ["Ad breaks", timeline(fs * 2.2, { marks: BREAKS, scale: false })],
    ["Chapters", timeline(fs * 2.2, { chapters: CH, fs: fs - 3, scale: false })], ["Compliance", timeline(fs * 2.2, { flags: [["22:10", "#e07a6d"], ["31:45", "#f5c451"]], scale: false })]].map(([k, tl]) => `<div class="row" style="align-items:center;gap:16px"><span class="panel-title" style="width:${fs * 8}px;flex:none;font-size:${fs - 3}px">${k}</span><div style="flex:1">${tl}</div></div>`).join("")}
    <div class="row tc" style="justify-content:space-between;margin-left:${fs * 8 + 16}px;font-size:${fs - 3}px;color:#7d889b">${["00:00", "10:00", "20:00", "30:00", "43:00"].map((t) => `<span>${t}</span>`).join("")}</div></div>`;
  add("o1-c5", "o1", "S", `${top("For media ops & automation")}
    <div class="count" style="margin-top:40px">05 / 05</div><h1 style="margin-top:12px;font-size:76px;width:930px">Every second of your library, <span class="hl">QC’d.</span></h1>
    <div class="abs" style="left:72px;top:385px">${player(936, 270, "r-peaky", { at: "36:40", fs: 16 })}</div>
    <div class="abs" style="left:72px;top:690px;width:936px">${lanes(18, 14)}</div>${foot()}`);
  add("o1-L", "o1", "L", `
    ${top("For media ops & automation")}
    <h1 style="margin-top:40px;width:430px">Every second of your library, <span class="hl">QC’d.</span></h1>
    <div class="abs" style="left:510px;top:46px">${player(634, 230, "r-peaky", { at: "36:40", fs: 13 })}</div>
    <div class="abs" style="left:510px;top:300px;width:634px">${lanes(14, 10)}</div>
    ${foot()}`);

  // rights-safe: the same cards with our own footage in every player
  add("o1-c1r", "o1", "S", oCard(1, "Binge markers <span class=\"hl\">for every episode.</span>", player(936, 320, "g-city", { skip: true, at: "01:31", fs: 17, pos: "42% 72%" }),
    `${zoom(936, 16)}<div style="height:16px"></div>${timeline(34, { segs: SEGS, playhead: "01:31", fs: 14 })}<div class="row tc" style="gap:22px;margin-top:12px;font-size:16px;color:#c7cfdc"><span>RECAP 00:00–01:12</span><span>INTRO 01:12–02:05</span><span>CREDITS 41:20–43:00</span></div>`, "", { frTop: 380, tlTop: 740 }));
  add("o1-c2r", "o1", "S", oCard(2, "Ad breaks that <span class=\"hl\">respect the story.</span>", player(936, 290, "g-road", { at: "14:37", fs: 17, pos: "52% 75%" }),
    timeline(48, { chapters: CH, marks: BREAKS, fs: 14 }),
    `<div class="abs" style="left:${72 + (936 * T("14:37")) / 100 - 100}px;top:700px">${tagPanel("14:37", 17)}</div><div class="abs" style="left:${72 + (936 * T("28:51")) / 100 - 100}px;top:700px">${tagPanel("28:51", 17)}</div>`, { frTop: 380, tlTop: 880 }));
  add("o1-c3r", "o1", "S", oCard(3, "Chapters, <span class=\"hl\">generated.</span>", player(936, 330, "g-sea", { at: "24:00", fs: 17, pos: "60% 70%" }),
    `${timeline(56, { chapters: CH, fs: 14 })}<div class="row" style="gap:14px;margin-top:20px">${[["The arrival", "She comes home after ten years."], ["The argument", "Old wounds open at dinner."], ["The storm", "The power goes out; no one leaves."], ["The confession", "She finally tells him the truth."]].map(([t, s]) => `<div class="panel" style="flex:1;padding:14px;border-radius:12px"><div style="font-size:19px;font-weight:600">${t}</div><div style="font-size:16px;color:var(--muted);margin-top:6px;line-height:1.35">${s}</div></div>`).join("")}</div>`, "", { tlTop: 700 }));
  add("o1-c5r", "o1", "S", `${top("For media ops & automation")}
    <div class="count" style="margin-top:40px">05 / 05</div><h1 style="margin-top:12px;font-size:76px;width:930px">Every second of your library, <span class="hl">QC’d.</span></h1>
    <div class="abs" style="left:72px;top:385px">${player(936, 270, "g-forest", { at: "36:40", fs: 16, pos: "45% 80%" })}</div>
    <div class="abs" style="left:72px;top:690px;width:936px">${lanes(18, 14)}</div>${foot()}`);
  add("o1r-L", "o1", "L", `
    ${top("For media ops & automation")}
    <h1 style="margin-top:40px;width:430px">Every second of your library, <span class="hl">QC’d.</span></h1>
    <div class="abs" style="left:510px;top:46px">${player(634, 230, "g-forest", { at: "36:40", fs: 13, pos: "45% 80%" })}</div>
    <div class="abs" style="left:510px;top:300px;width:634px">${lanes(14, 10)}</div>
    ${foot()}`);

  // ---------------------------------------------------------------- mount
  const only = new URLSearchParams(location.search).get("only");
  const list = only ? ASSETS.filter((a) => only.split(",").includes(a.id)) : ASSETS;
  document.body.insertAdjacentHTML("beforeend", list.map((a) => `<section class="ad ${a.fmt}${a.light ? " light" : ""}" id="${a.id}" data-ad="${a.ad}">${a.html}</section>`).join(""));
})();
