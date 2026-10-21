// Generic, rights-free "film frames" drawn as SVG, so the ads never depend on
// licensed stills. Any element with data-scene="<name>" is filled with one.
(function () {
  const W = 320, H = 180;

  function ridge(y, amp, seed, color, steps = 9) {
    let d = `M0 ${H} L0 ${y}`;
    for (let i = 1; i <= steps; i++) {
      const x = (W / steps) * i;
      const peak = y - amp * Math.abs(Math.sin(seed * 1.7 + i * 1.3) * Math.cos(seed + i * 0.7));
      d += ` L${x - W / steps / 2} ${peak} L${x} ${y + amp * 0.15 * Math.sin(seed + i)}`;
    }
    return `<path d="${d} L${W} ${H} Z" fill="${color}"/>`;
  }

  function sky(id, stops) {
    const s = stops.map((c, i) => `<stop offset="${i / (stops.length - 1)}" stop-color="${c}"/>`).join("");
    return `<defs><linearGradient id="${id}" x1="0" y1="0" x2="0" y2="1">${s}</linearGradient></defs>` +
      `<rect width="${W}" height="${H}" fill="url(#${id})"/>`;
  }

  function stars(n, seed, maxY = H * 0.6) {
    let out = "";
    for (let i = 0; i < n; i++) {
      const x = (Math.sin(seed + i * 12.9898) * 43758.5453 % 1 + 1) % 1 * W;
      const y = (Math.sin(seed + i * 78.233) * 12345.678 % 1 + 1) % 1 * maxY;
      out += `<circle cx="${x}" cy="${y}" r="${i % 5 ? 0.6 : 1.1}" fill="#fff" opacity="${0.4 + (i % 3) * 0.2}"/>`;
    }
    return out;
  }

  function skyline(base, color, lit, seed) {
    let out = "", x = 0, i = 0;
    while (x < W) {
      const w = 14 + ((i * 7 + seed) % 5) * 6;
      const h = 30 + ((i * 13 + seed * 3) % 7) * 12;
      out += `<rect x="${x}" y="${base - h}" width="${w - 2}" height="${h}" fill="${color}"/>`;
      for (let wy = base - h + 6; wy < base - 6; wy += 8)
        for (let wx = x + 3; wx < x + w - 5; wx += 6)
          if ((wx * 3 + wy * 7 + seed) % 5 === 0)
            out += `<rect x="${wx}" y="${wy}" width="2" height="3" fill="${lit}" opacity="0.85"/>`;
      x += w; i++;
    }
    return out;
  }

  function figure(x, base, scale, color) {
    // simple standing silhouette, head + shoulders + body
    const s = scale;
    return `<g fill="${color}">
      <circle cx="${x}" cy="${base - 62 * s}" r="${9 * s}"/>
      <path d="M${x - 16 * s} ${base} Q${x - 18 * s} ${base - 44 * s} ${x - 6 * s} ${base - 50 * s}
               L${x + 6 * s} ${base - 50 * s} Q${x + 18 * s} ${base - 44 * s} ${x + 16 * s} ${base} Z"/>
    </g>`;
  }

  const SCENES = {
    dusk: (id) => sky(id, ["#2b1d52", "#8a3f74", "#f08a5d"]) +
      `<circle cx="215" cy="112" r="26" fill="#ffd27a" opacity="0.95"/>` +
      ridge(118, 46, 1, "#5a2a5e") + ridge(138, 36, 4, "#3a1d47") + ridge(160, 22, 7, "#1f1030"),
    dawn: (id) => sky(id, ["#86b6ff", "#cfe0ff", "#ffd9c4"]) +
      ridge(110, 52, 2, "#8ea6c8") + ridge(130, 34, 5, "#6c85aa") +
      `<rect y="140" width="${W}" height="40" fill="#7b97c4" opacity="0.9"/>` +
      `<rect y="146" width="${W}" height="1.5" fill="#fff" opacity="0.35"/>`,
    night: (id) => sky(id, ["#060b1f", "#13224d", "#26346b"]) + stars(60, 3) +
      `<circle cx="250" cy="40" r="12" fill="#e9efff"/>` +
      skyline(180, "#0a1027", "#ffd76e", 3),
    sunset: (id) => sky(id, ["#ff8a5c", "#ffb36b", "#ffd88f"]) +
      `<circle cx="160" cy="118" r="34" fill="#fff1c9"/>` +
      `<rect y="118" width="${W}" height="62" fill="#2d3561"/>` +
      [0, 1, 2, 3, 4].map(i => `<rect x="${132 - i * 4}" y="${124 + i * 9}" width="${56 + i * 8}" height="2" fill="#ffd88f" opacity="${0.7 - i * 0.12}"/>`).join(""),
    forest: (id) => sky(id, ["#9fd8c6", "#d8f0e4"]) +
      `<rect y="146" width="${W}" height="34" fill="#163626"/>` +
      Array.from({ length: 22 }, (_, i) => {
        const x = i * 15 - 4, h = 60 + (i * 37 % 40), b = 150 + (i % 3) * 10;
        const c = ["#2f6b4f", "#24563f", "#1a4030"][i % 3];
        return `<path d="M${x} ${b} L${x + 11} ${b - h} L${x + 22} ${b} Z" fill="${c}"/>`;
      }).join("") + `<rect y="160" width="${W}" height="20" fill="#163626"/>`,
    desert: (id) => sky(id, ["#f7b267", "#f4845f"]) +
      `<circle cx="80" cy="60" r="20" fill="#fff3d6" opacity="0.9"/>` +
      `<path d="M0 130 Q80 100 170 128 T320 118 L320 180 L0 180 Z" fill="#d9774b"/>` +
      `<path d="M0 156 Q110 128 210 152 T320 146 L320 180 L0 180 Z" fill="#b65a35"/>`,
    snow: (id) => sky(id, ["#b7cde8", "#e8f0fa"]) +
      ridge(112, 58, 3, "#f4f8fd") + ridge(140, 30, 6, "#d5e2f1") +
      `<rect y="158" width="${W}" height="22" fill="#c4d4e8"/>`,
    space: (id) => sky(id, ["#02030a", "#0b1030"]) + stars(90, 9, H) +
      `<circle cx="200" cy="96" r="38" fill="#3d5bd9"/><circle cx="188" cy="86" r="38" fill="#6f8cff" opacity="0.35"/>` +
      `<ellipse cx="200" cy="96" rx="70" ry="12" fill="none" stroke="#c9d4ff" stroke-width="2.5" opacity="0.7" transform="rotate(-14 200 96)"/>`,
    neon: (id) => sky(id, ["#14052e", "#5a0f6b", "#ff4f8b"]) +
      `<circle cx="160" cy="100" r="40" fill="#ffb347" opacity="0.9"/>` +
      `<rect y="112" width="${W}" height="68" fill="#120420"/>` +
      Array.from({ length: 9 }, (_, i) => `<line x1="${160 + (i - 4) * 12}" y1="112" x2="${160 + (i - 4) * 70}" y2="180" stroke="#ff4fd8" stroke-width="1" opacity="0.6"/>`).join("") +
      [118, 128, 142, 162].map(y => `<line x1="0" y1="${y}" x2="${W}" y2="${y}" stroke="#ff4fd8" stroke-width="1" opacity="0.5"/>`).join(""),
    noir: (id) => sky(id, ["#0d1b22", "#1d3b45"]) +
      `<rect x="40" y="30" width="110" height="130" fill="#e7d9a8" opacity="0.18"/>` +
      `<line x1="95" y1="30" x2="95" y2="160" stroke="#0d1b22" stroke-width="5"/>` +
      `<line x1="40" y1="95" x2="150" y2="95" stroke="#0d1b22" stroke-width="5"/>` +
      Array.from({ length: 40 }, (_, i) => `<line x1="${(i * 37) % W}" y1="${(i * 53) % H}" x2="${(i * 37) % W - 4}" y2="${(i * 53) % H + 14}" stroke="#9fc3cf" stroke-width="0.7" opacity="0.35"/>`).join("") +
      figure(230, 180, 1.6, "#071015"),
    concert: (id) => sky(id, ["#120a2e", "#3b1c6e"]) +
      [60, 140, 220, 280].map((x, i) => `<path d="M${x} 0 L${x - 50} 180 L${x + 50} 180 Z" fill="${["#7b5cff", "#ff5ca8", "#5cc8ff", "#ffcf5c"][i]}" opacity="0.18"/>`).join("") +
      Array.from({ length: 26 }, (_, i) => `<circle cx="${i * 13}" cy="${168 - (i % 3) * 4}" r="${7 + (i % 2) * 2}" fill="#0a0518"/>`).join("") +
      `<rect y="170" width="${W}" height="10" fill="#0a0518"/>`,
    portrait: (id) => sky(id, ["#f29e6b", "#f7c59f", "#2e3f6e"]) +
      `<circle cx="210" cy="110" r="20" fill="#fff0d9"/>` +
      `<rect y="128" width="${W}" height="52" fill="#25345f"/>` +
      `<path d="M96 180 L96 150 Q92 128 110 120 L112 108 Q100 104 101 90 Q100 70 118 64 Q140 58 146 80
               Q149 92 144 100 L150 106 L144 110 Q146 120 156 124 Q176 132 180 180 Z" fill="#1b1424"/>`,
  };

  let n = 0;
  window.renderScenes = function () {
    document.querySelectorAll("[data-scene]").forEach((el) => {
      const make = SCENES[el.dataset.scene];
      if (!make) return;
      // Insert behind any overlay children (titles, badges, buttons) rather than replacing them.
      el.insertAdjacentHTML("afterbegin",
        `<svg viewBox="0 0 ${W} ${H}" preserveAspectRatio="xMidYMid slice" style="position:absolute;inset:0;width:100%;height:100%">${make("g" + n++)}</svg>`);
    });
  };
  document.addEventListener("DOMContentLoaded", window.renderScenes);
})();
