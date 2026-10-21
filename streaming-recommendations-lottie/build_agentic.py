"""Builds the Lotties for the Agentic Layer landing page (vionlabs.com/agentic-layer).

Same approach as build_curio.py: one Lottie per visual slot, and each one
highlights, in turn, the thing the section is about. One campaign runs through
all of them: a "Space Night" line-up.

  agentic-hero                  Hero (1920x1080, 8.4 s). A request is typed into the
                                agent, then the three results light up in turn:
                                Curated Lists, Clips in Every Ratio and Branded
                                Thumbnails. Same 252-frame timing as curio-hero
                                (beats at 61 / 99 / 183), so the page's rotating
                                headline drives it unchanged.
  agentic-hero-v3               Hero on the page (1920x1080, 18.5 s, transparent).
                                Chat first: the request is typed, the chat grows,
                                docks right, and the workspace opens to its left
                                with each film's scenes reframed to 9:16 clips.
  agentic-curated-lists        What the agent does, row 1 (1280x720, 8 s). The
                                Curation Agent's ranked list; the highlight walks
                                down the titles like a slideshow.
  agentic-clips                 Row 2 (1280x720), used as a still. One scene cut
                                for TV, social feeds and Shorts.
  agentic-branded-thumbnails    Row 3 (1280x720), used as a still. Thumbnails with
                                each title's logo placed, ready to import.

Run:  python3 build_agentic.py
"""
import json
import os
import zipfile

from build_curio import Images, add_fade, on_off
from curio_ui import (BG, BLUE, FOCUS, GENRE, GENRE_EDGE, I_PLAY, LIGHT, MED, MOOD, MUTED, NAV_BG,
                      PANEL, REG, SEMI, BOLD, bf, logo, pill, pill_row)
from lottie_kit import (Comp, Font, anim, animation, ellipse, fade, fill, gfill, group, icon,
                        layer_ks, mask, rect, rrect, stroke)

HERE = os.path.dirname(os.path.abspath(__file__))
FPS = 30
FONT_DIR = os.environ.get("INTER_DIR", "/usr/share/fonts/opentype/inter")
D_XLIGHT = Font(f"{FONT_DIR}/InterDisplay-ExtraLight.otf")
D_BOLD = Font(f"{FONT_DIR}/InterDisplay-Bold.otf")

BUBBLE = "#2f6fe6"
INPUT = "#121a24"
ROW = "#1b2531"
GOOD = "#34d399"

# Material Design icons (Apache 2.0)
I_SPARKLE = ("M19 9l1.25-2.75L23 5l-2.75-1.25L19 1l-1.25 2.75L15 5l2.75 1.25L19 9zm-7.5.5L9 4 6.5 "
             "9.5 1 12l5.5 2.5L9 20l2.5-5.5L17 12l-5.5-2.5zM19 15l-1.25 2.75L15 19l2.75 1.25L19 23"
             "l1.25-2.75L23 19l-2.75-1.25L19 15z")
I_SEND = "M2.01 21L23 12 2.01 3 2 10l15 2-15 2z"
I_CHECK = "M9 16.17L4.83 12l-1.42 1.41L9 19 21 7l-1.41-1.41z"
I_LIST = "M3 13h2v-2H3v2zm0 4h2v-2H3v2zm0-8h2V7H3v2zm4 4h14v-2H7v2zm0 4h14v-2H7v2zM7 7v2h14V7H7z"

# The Space Night line-up: (image, title, genres, moods, relevance)
LINEUP = [
    ("interstellar_wide", "Interstellar", "sci-fi • drama • adventure", ["emotional", "awe-inspiring"], 98),
    ("martian", "The Martian", "sci-fi • adventure • drama", ["survival", "uplifting"], 95),
    ("arrival", "Arrival", "sci-fi • drama • mystery", ["thought-provoking", "emotional"], 93),
    ("sunshine", "Sunshine", "sci-fi • thriller", ["suspenseful", "intense"], 90),
    ("2001", "2001: A Space Odyssey", "sci-fi • adventure", ["hypnotic", "awe-inspiring"], 87),
]
SIZE = {"interstellar_wide": (960, 540), "topgun_hero": (960, 540)}   # every other image is 410x231
PRECOMPS = []                                   # comps made by media() for the Lottie being built


def isize(name):
    return SIZE.get(name, (410, 231))


# ---------------------------------------------------------------- building blocks

def wrap(font, text, size, max_w):
    lines, cur = [], ""
    for word in text.split():
        t = f"{cur} {word}".strip()
        if not cur or font.width(t, size) <= max_w:
            cur = t
        else:
            lines.append(cur)
            cur = word
    return lines + [cur]


def vis(t_in, t_out=None, ramp=10):
    """Opacity: in at t_in, optionally out at t_out."""
    keys = [(t_in, [0]), (t_in + ramp, [100])]
    if t_out:
        keys += [(t_out, [100]), (t_out + 8, [0])]
    return anim(keys)


def rise(t_in, t_out=None, dy=18):
    """Position offset for a parent null: slide up into place, drift up on the way out."""
    keys = [(t_in, [0, dy], "out"), (t_in + 16, [0, 0])]
    if t_out:
        keys += [(t_out, [0, 0], "in"), (t_out + 8, [0, -12])]
    return anim(keys)


def appear(m, name, shapes, t_in, t_out=None, dy=18, ip=0, op=None):
    """A shape layer that slides up and fades in (and optionally out)."""
    return m.shape(name, shapes, ip=ip, op=op, ks=layer_ks(p=rise(t_in, t_out, dy), o=vis(t_in, t_out)))


def media(m, name, img, crop, box, radius, t_in, t_out=None, op_comp=None, drift=None, parent=None,
          ip=0):
    """Shows `crop` (cx, cy, w, h in image px) of an image inside `box` (x, y, w, h).

    The image sits in its own precomp so it can drift slowly (a playing clip)
    while the rounded frame stays put."""
    cx, cy, cw, ch = crop
    x, y, w, h = box
    s = 100 * w / cw
    c = Comp(round(w), round(h), op_comp or m.op, f"comp_{name}")
    PRECOMPS.append(c)
    p0 = [w / 2, h / 2]
    if drift:                                   # (scale gain, dx in image px) over the comp
        g, dx = drift
        c.image("img", img, ks=layer_ks(
            p=p0, a=anim([(0, [cx, cy], "linear"), (c.op, [cx + dx, cy])]),
            s=anim([(0, [s, s], "linear"), (c.op, [s * g, s * g])])))
    else:
        c.image("img", img, ks=layer_ks(p=p0, a=(cx, cy), s=(s, s)))
    layer = m.precomp(name, c, ip=ip, parent=parent, masks=[mask(rrect(0, 0, w, h, radius))],
                      ks=layer_ks(p=(x + w / 2, y + h / 2), a=(w / 2, h / 2), o=vis(t_in, t_out)))
    return c, layer


def full(name, box=None):
    """The whole image, cropped to the box's aspect ratio around the centre."""
    iw, ih = isize(name)
    if box is None:
        return (iw / 2, ih / 2, iw, ih)
    ar = box[2] / box[3]
    if iw / ih > ar:
        return (iw / 2, ih / 2, ih * ar, ih)
    return (iw / 2, ih / 2, iw, iw / ar)


def focus_ring(x, y, w, h, radius, ring=4, glow=10):
    return bf([
        group([rect(w + 2 * glow, h + 2 * glow, x + w / 2, y + h / 2, radius + glow - 2),
               stroke(FOCUS, 9, 28)]),
        group([rect(w + 2 * ring, h + 2 * ring, x + w / 2, y + h / 2, radius + ring - 1),
               stroke(FOCUS, 3)]),
    ])


def title_logo(kind, x, base, size, align="left"):
    """Title lettering in the spirit of each poster (type only, no logo artwork)."""
    if kind == "interstellar_wide":
        return [LIGHT.text("INTERSTELLAR", size, x, base, align=align, tracking=0.3)]
    if kind == "martian":
        return [D_BOLD.text("THE MARTIAN", size * 1.05, x, base, align=align, tracking=0.12)]
    if kind == "arrival":
        return [D_XLIGHT.text("ARRIVAL", size * 1.2, x, base, align=align, tracking=0.46)]
    return [SEMI.text(kind.upper(), size, x, base, align=align, tracking=0.2)]


def scrim(x, y, w, h, radius, top=0.35):
    return group([rect(w, h, x + w / 2, y + h / 2, radius), gfill(
        [(0, "#000000", 0), (top, "#000000", 0.1), (1, "#000000", 0.82)], (0, y), (0, y + h))])


def chip_check(text, x, y, size=17, h=30):
    """A small ratio chip with a check mark."""
    w = MED.width(text, size) + 46
    return bf([group([rect(w, h, x + w / 2, y + h / 2, h / 2), fill(GOOD, 12), stroke(GOOD, 1.2, 55)]),
               icon(I_CHECK, 18, x + 18, y + h / 2, color=GOOD),
               MED.text(text, size, x + 32, y + h / 2 + size * 0.36, "#d1fae5")]), w


def agent_bar(m, w, title, right=None, scale=1.0):
    """Top bar of the agent UI: Vionlabs logo, the agent's name, optional campaign label."""
    hb = 64 * scale
    items = [group([rect(w, hb, w / 2, hb / 2), fill(NAV_BG)]),
             group([rect(w, 1, w / 2, hb), fill("#ffffff", 8)])]
    items += logo(36 * scale, 42 * scale, 24 * scale)
    x = 236 * scale
    items += [group([rect(1, 30 * scale, x, hb / 2), fill("#ffffff", 14)]),
              group([rect(38 * scale, 38 * scale, x + 42 * scale, hb / 2, 10 * scale), fill("#1d2a44")]),
              icon(I_SPARKLE, 22 * scale, x + 42 * scale, hb / 2, color=FOCUS),
              SEMI.text(title, 21 * scale, x + 72 * scale, hb / 2 + 7.5 * scale)]
    if right:
        items.append(REG.text(right, 18 * scale, w - 36 * scale, hb / 2 + 6.5 * scale, MUTED, align="right"))
    m.shape("agent-bar", bf(items))


def user_bubble(lines, x, y, w, size=22, lh=31, pad=18):
    h = 2 * pad + lh * (len(lines) - 1) + size
    items = [group([rect(w, h, x + w / 2, y + h / 2, 14), fill(BUBBLE)])]
    items += [REG.text(t, size, x + pad + 2, y + pad + size * 0.8 + k * lh) for k, t in enumerate(lines)]
    return bf(items), h


def agent_reply(tool, lines, x, y, size=22, lh=31):
    """A tool call tag and the agent's answer, plain text like the product UI."""
    items = [MED.text(f"→  {tool}", size * 0.75, x, y, FOCUS, o=85)]
    items += [REG.text(t, size, x, y + 34 + k * lh, o=92) for k, t in enumerate(lines)]
    return items, 34 + lh * (len(lines) - 1) + size * 0.3


def write(data, name):
    text = json.dumps(data, separators=(",", ":"))
    with open(os.path.join(HERE, f"{name}.json"), "w") as f:
        f.write(text)
    manifest = {"version": "1.0", "generator": "build_agentic.py", "author": "", "revision": 1,
                "animations": [{"id": name, "speed": 1, "loop": True, "autoplay": True,
                                "direction": 1, "playMode": "normal"}]}
    with zipfile.ZipFile(os.path.join(HERE, f"{name}.lottie"), "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr("manifest.json", json.dumps(manifest))
        z.writestr(f"animations/{name}.json", text)
    print(f"wrote {name}.json ({len(text) / 1024:.0f} KB)")


# ------------------------------------------------------------------- hero

PROMPT = "Plan a Space Night line-up with clips for TV and mobile, plus branded thumbnails"
REPLIES = [
    ("curate_list", "Ranked 5 titles from your catalog for Space Night."),
    ("cut_clips", "Cut a 30-second clip for each title, in 16:9 for TV and 9:16 for mobile."),
    ("brand_thumbnails", "Placed each title logo on its thumbnail, in every ratio. Ready for your approval."),
]
STEPS = ["01  Curated Lists", "02  Clips in Every Ratio", "03  Branded Thumbnails"]


def hero_chat(m, t_type, t_send, picks):
    """Left column: the conversation, and the input the request is typed into."""
    px, py, pw, ph = 40, 100, 600, 944
    m.shape("chat-panel", bf([
        group([rect(pw, ph, px + pw / 2, py + ph / 2, 18), fill(PANEL, 70), stroke("#ffffff", 1, 8)]),
        SEMI.text("CONVERSATION", 15, px + 28, py + 48, MUTED, tracking=0.2),
    ]))

    # the request, typed into the input line by line
    ix, iy, iw, ih = px + 24, 892, pw - 48, 128
    m.shape("input", bf([group([rect(iw, ih, ix + iw / 2, iy + ih / 2, 14), fill(INPUT),
                                stroke("#ffffff", 1.2, 14)])]))
    m.shape("input-focus", [group([rect(iw, ih, ix + iw / 2, iy + ih / 2, 14), stroke(FOCUS, 1.6)])],
            ks=layer_ks(o=anim([(t_type[0] - 4, [0]), (t_type[0] + 2, [80]), (t_send, [80]), (t_send + 8, [0])])))
    m.shape("placeholder", [REG.text("Describe what you need…", 21, ix + 22, iy + 44, MUTED, o=80)],
            ks=layer_ks(o=anim([(0, [100]), (t_type[0], [100], "hold"), (t_type[0] + 1, [0]),
                                (t_send + 2, [0]), (t_send + 10, [100])])))
    size, lh = 21, 30
    lines = wrap(REG, PROMPT, size, iw - 104)
    total = sum(len(t) for t in lines)
    t, x0 = t_type[0], ix + 22
    caret = []
    for k, line in enumerate(lines):
        dur = (t_type[1] - t_type[0]) * len(line) / total
        w = REG.width(line, size)
        base = iy + 42 + k * lh
        t1 = t + dur
        m.shape(f"typed {k}", [REG.text(line, size, x0, base)], ip=round(t), op=t_send,
                masks=[mask(anim([(t, rrect(x0 - 2, base - 24, 0.1, 32, 0), "linear"),
                                  (t1, rrect(x0 - 2, base - 24, w + 6, 32, 0))]))])
        caret += [(t, [x0, base - 7], "linear"), (t1 - 0.5, [x0 + w + 2, base - 7], "hold")]
        t = t1
    blink = [(0, [100], "hold"), (8, [0], "hold"), (16, [100], "hold")]
    blink += [(t_type[0], [100], "hold"), (t_type[1], [100], "hold"), (t_type[1] + 6, [0], "hold"),
              (t_type[1] + 12, [100], "hold"), (t_send, [0])]
    m.shape("caret", [group([rect(2.5, 26, 0, 0, 1), fill("#ffffff")])], op=t_send + 1,
            ks=layer_ks(p=anim([(0, caret[0][1], "hold")] + caret), o=anim(blink)))
    sx, sy = ix + iw - 40, iy + ih - 40
    m.shape("send", bf([group([ellipse(48, 48, 0, 0), fill(BLUE)]), icon(I_SEND, 22, 2, 0)]),
            ks=layer_ks(p=(sx, sy), s=anim([(t_send - 4, [100, 100]), (t_send, [86, 86], "out"),
                                             (t_send + 8, [100, 100])])))

    # the conversation
    bx, bw = px + 24, pw - 48
    blines = wrap(REG, PROMPT, 22, bw - 40)
    shapes, bh = user_bubble(blines, bx, 180, bw)
    appear(m, "user-bubble", shapes, t_send + 1, dy=24)
    y = 180 + bh + 52
    dots = [group([ellipse(10, 10, bx + 8 + 18 * k, y - 8), fill("#ffffff")],
                  o=anim([(t_send + 4 + 3 * k, [25]), (t_send + 8 + 3 * k, [90]), (t_send + 12 + 3 * k, [25]),
                          (t_send + 16 + 3 * k, [90]), (t_send + 20 + 3 * k, [25])])) for k in range(3)]
    m.shape("thinking", dots, ip=t_send + 4, op=picks[0])
    for k, (tool, text) in enumerate(REPLIES):
        items, h = agent_reply(tool, wrap(REG, text, 22, bw - 8), bx, y)
        appear(m, f"reply {k}", items, picks[k] + 2, dy=14)
        y += h + 44


def hero_list(m, imgs, t_in, t_out, x0, top):
    """Phase 1: the ranked line-up."""
    null = m.null("list", ks=layer_ks(p=rise(t_in, t_out)))
    appear(m, "list-head", [BOLD.text("Space Night", 34, x0 + 8, top + 40),
                            REG.text("5 titles  ·  ranked by relevance", 20, x0 + 10, top + 74, MUTED)],
           t_in, t_out, dy=0)
    rw, rh, gap, ry0 = 1136, 124, 10, top + 104
    for k, (name, title, genres, moods, score) in enumerate(LINEUP):
        y = ry0 + k * (rh + gap)
        t = t_in + 3 * k
        pills, _ = pill_row(moods, x0 + 286, y + 80, gap=8, size=15, h=28, color=MOOD, fill_o=16,
                            edge=MOOD, edge_o=55, text_color="#ffd9d2")
        bar_x, bar_w = x0 + rw - 236, 200
        m.shape(f"row {k}", bf([
            group([rect(rw, rh, x0 + rw / 2, y + rh / 2, 12), fill(ROW)]),
            BOLD.text(str(k + 1), 28, x0 + 34, y + rh / 2 + 10, align="center", o=70),
            SEMI.text(title, 26, x0 + 286, y + 44),
            REG.text(genres, 18, x0 + 286 + SEMI.width(title, 26) + 16, y + 43, MUTED),
            group(pills),
            group([rect(bar_w, 8, bar_x + bar_w / 2, y + 80, 4), fill("#ffffff", 12)]),
            group([rect(anim([(t + 6, [0.1, 8], "out"), (t + 30, [bar_w * score / 100, 8])]), 0,
                        anim([(t + 6, [bar_x, y + 80], "out"), (t + 30, [bar_x + bar_w * score / 200, y + 80])]),
                        0, 4), fill(FOCUS)]),
            BOLD.text(f"{score}%", 26, bar_x + bar_w, y + 58, align="right"),
            REG.text("relevance", 15, bar_x, y + 58, MUTED),
        ]), parent=null, ks=layer_ks(p=anim([(t, [0, 16], "out"), (t + 16, [0, 0])]), o=vis(t, t_out)))
        media(m, f"row {k} thumb", imgs(name), full(name, (0, 0, 192, 108)), (x0 + 70, y + 8, 192, 108),
              8, t, t_out, parent=null)
    m.shape("row 0 focus", focus_ring(x0, ry0, rw, rh, 12), parent=null,
            ks=layer_ks(o=on_off([(t_in + 12, t_out)])))


def hero_clips(m, imgs, t_in, t_out, x0, top):
    """Phase 2: the top pick cut for TV and for mobile."""
    null = m.null("clips", ks=layer_ks(p=rise(t_in, t_out)))
    appear(m, "clips-head", [BOLD.text("Interstellar  ·  30-second clip", 34, x0 + 8, top + 40),
                             REG.text("Scene-accurate, reframed for every screen", 20, x0 + 10, top + 74, MUTED)],
           t_in, t_out, dy=0)
    y = top + 104
    clip_op = t_out + 10
    tv = (x0, y, 800, 450)
    mob = (x0 + 800 + 36, y, 450 * 9 / 16, 450)
    media(m, "clip 16x9", imgs("interstellar_wide"), (480, 270, 960, 540), tv, 12, t_in, t_out,
          drift=(1.06, -14), parent=null)
    media(m, "clip 9x16", imgs("interstellar_wide"), (470, 270, 540 * 9 / 16, 540), mob, 12, t_in + 4,
          t_out, drift=(1.06, 10), parent=null)
    for k, (bx, by, bw, bh) in enumerate((tv, mob)):
        label = ("16:9  ·  TV", "9:16  ·  Shorts & TikTok")[k]
        pad = 20 if k == 0 else 14
        tx0, tw = bx + pad, bw - 2 * pad
        ty = by + bh - 24
        m.shape(f"clip {k} ui", bf([
            scrim(bx, by, bw, bh, 12, top=0.6),
            group([ellipse(64, 64, bx + bw / 2, by + bh / 2), fill("#000000", 45), stroke("#ffffff", 2, 70)]),
            icon(I_PLAY, 30, bx + bw / 2 + 2, by + bh / 2),
            group([rect(tw, 5, tx0 + tw / 2, ty, 2.5), fill("#ffffff", 30)]),
            group([rect(anim([(t_in + 4, [0.1, 5], "linear"), (clip_op, [tw * 0.55, 5])]), 0,
                        anim([(t_in + 4, [tx0, ty], "linear"), (clip_op, [tx0 + tw * 0.275, ty])]), 0, 2.5),
                   fill(BLUE)]),
            MED.text("0:30", 17, bx + bw - pad, ty - 14, align="right", o=90),
        ]), parent=null, ks=layer_ks(o=vis(t_in + 2 * k, t_out)))
        chip, _ = pill(label, bx, by + bh + 16, size=17, h=34, color=GENRE, edge=GENRE_EDGE)
        appear(m, f"clip {k} label", chip, t_in + 6 + 2 * k, t_out, dy=10)
    m.shape("clip 9x16 focus", focus_ring(*mob, 12), parent=null, ks=layer_ks(o=on_off([(t_in + 16, t_out)])))

    # the rest of the line-up is cut too
    ry = y + 450 + 88
    appear(m, "clips-rest-head", [MED.text("Clips ready for every title", 22, x0 + 8, ry)], t_in + 14, t_out, dy=10)
    for k, (name, title, *_r) in enumerate(LINEUP[1:]):
        x = x0 + k * (272 + 16)
        t = t_in + 18 + 3 * k
        media(m, f"rest {k}", imgs(name), full(name, (0, 0, 272, 153)), (x, ry + 22, 272, 153), 10, t, t_out,
              parent=null)
        m.shape(f"rest {k} ready", bf([
            group([ellipse(34, 34, x + 272 - 26, ry + 22 + 26), fill(GOOD)]),
            icon(I_CHECK, 22, x + 272 - 26, ry + 22 + 26, color="#062b1d"),
        ]), parent=null, ks=layer_ks(o=vis(t + 8, t_out)))


def hero_thumbs(m, imgs, t_in, op, x0, top, t_publish=None):
    """Phase 3: branded thumbnails, then the approval."""
    null = m.null("thumbs", ks=layer_ks(p=rise(t_in)))
    appear(m, "thumbs-head", [BOLD.text("Branded thumbnails", 34, x0 + 8, top + 40),
                              REG.text("Each title logo placed on the scene that matters", 20, x0 + 10, top + 74,
                                       MUTED)], t_in, dy=0)
    y = top + 104
    tw, th, gap = 368, 207, 16
    for k, (name, title, *_r) in enumerate(LINEUP[:3]):
        x = x0 + k * (tw + gap)
        t = t_in + 3 * k
        media(m, f"thumb {k}", imgs(name), full(name, (0, 0, tw, th)), (x, y, tw, th), 10, t, parent=null)
        m.shape(f"thumb {k} logo", bf([scrim(x, y, tw, th, 10)] + title_logo(name, x + 20, y + th - 22, 26)),
                parent=null, ks=layer_ks(o=vis(t + 10)))
        m.shape(f"thumb {k} meta", [SEMI.text(title, 20, x + 2, y + th + 34),
                                    REG.text("16:9  ·  1:1  ·  9:16", 17, x + tw, y + th + 34, MUTED, align="right")],
                parent=null, ks=layer_ks(o=vis(t + 4)))
    # the top pick in the other two ratios
    y2 = y + th + 76
    sq = (x0, y2, 300, 300)
    tall = (x0 + 300 + gap, y2, 169, 300)
    media(m, "thumb 1x1", imgs("interstellar_wide"), (480, 270, 540, 540), sq, 10, t_in + 10, parent=null)
    media(m, "thumb 9x16", imgs("interstellar_wide"), (470, 270, 540 * 9 / 16, 540), tall, 10, t_in + 12,
          parent=null)
    m.shape("thumb 1x1 logo", bf([scrim(*sq, 10)] + title_logo("interstellar_wide", sq[0] + 150, y2 + 272, 22,
                                                               align="center")),
            parent=null, ks=layer_ks(o=vis(t_in + 20)))
    m.shape("thumb 9x16 logo", bf([group([rect(169, 300, tall[0] + 84.5, y2 + 150, 10), gfill(
        [(0, "#000000", 0.75), (0.35, "#000000", 0.05), (1, "#000000", 0)], (0, y2), (0, y2 + 300))])]
        + title_logo("interstellar_wide", tall[0] + 84.5, y2 + 40, 13, align="center")),
        parent=null, ks=layer_ks(o=vis(t_in + 22)))
    for k, (label, bx) in enumerate((("1:1", sq[0]), ("9:16", tall[0]))):
        chip, _ = chip_check(label, bx, y2 + 316)
        m.shape(f"ratio {k}", chip, parent=null, ks=layer_ks(o=vis(t_in + 22 + 2 * k)))

    # ready to approve
    ax = x0 + 300 + gap + 169 + 48
    t_ready = t_in + 22
    m.shape("ready", bf([
        SEMI.text("3 titles  ·  3 ratios  ·  9 assets", 26, ax, y2 + 92),
        REG.text("Nothing is published until you approve it.", 20, ax, y2 + 128, MUTED),
    ]), parent=null, ks=layer_ks(o=vis(t_ready)))
    bx, by, bw, bh = ax, y2 + 170, 300, 60
    m.shape("approve", bf([group([rect(bw, bh, bx + bw / 2, by + bh / 2, 30), fill(BLUE)]),
                           icon(I_CHECK, 24, bx + 36, by + bh / 2),
                           SEMI.text("Approve & publish", 22, bx + 58, by + bh / 2 + 8)]),
            parent=null, ks=layer_ks(o=vis(t_ready + 4, t_publish)))
    if t_publish:                               # approved: the button turns into the result
        c = (bx + bw / 2, by + bh / 2)
        m.shape("published", bf([group([rect(bw, bh, c[0], c[1], 30), fill(GOOD, 16), stroke(GOOD, 2)]),
                                 icon(I_CHECK, 24, bx + 36, c[1], color=GOOD),
                                 SEMI.text("Published", 22, bx + 58, c[1] + 8, "#d1fae5")]),
                parent=null, ip=t_publish, ks=layer_ks(
                    p=c, a=c, s=anim([(t_publish, [92, 92], "out"), (t_publish + 10, [100, 100])]),
                    o=vis(t_publish, ramp=6)))
    t_p = t_ready + 18
    m.shape("approve pulse", [group([rect(bw, bh, bx + bw / 2, by + bh / 2, 30), stroke(FOCUS, 3)])],
            parent=null, ip=t_p, ks=layer_ks(p=(bx + bw / 2, by + bh / 2), a=(bx + bw / 2, by + bh / 2),
                                            s=anim([(t_p, [100, 100], "out"), (t_p + 22, [114, 124])]),
                                            o=anim([(t_p, [90]), (t_p + 22, [0])])))


def build_hero():
    W, H, OP = 1920, 1080, 252                  # 3 x 2.8 s, the headline's rhythm
    PRECOMPS.clear()
    imgs = Images()
    m = Comp(W, H, OP, "main")
    t_type, t_send = (8, 44), 48
    picks = [61, 99, 183]                       # the three results light up here
    m.shape("bg", [group([rect(W, H, W / 2, H / 2), fill(BG)]),
                   group([ellipse(1600, 1100, 1400, 380), gfill([(0, "#1b2a46", 1), (1, BG, 0)],
                                                                (1400, 380), (2150, 380), radial=True)])])
    agent_bar(m, W, "Agentic Layer", right="Space Night campaign", scale=1.25)
    hero_chat(m, t_type, t_send, picks)

    # right: the three steps, then the results of each
    x0, top = 696, 196
    m.shape("canvas", bf([group([rect(1184, 848, x0 - 16 + 592, top + 424, 18), fill(PANEL, 45),
                                 stroke("#ffffff", 1, 7)])]))
    cx, cy = x0 - 16 + 592, top + 424
    m.shape("empty-state", bf([
        group([rect(88, 88, cx, cy - 40, 22), fill("#1d2a44")]),
        icon(I_SPARKLE, 44, cx, cy - 40, color=FOCUS),
        MED.text("Results appear here as the agent works", 24, cx, cy + 50, o=80, align="center"),
        REG.text("Lists, clips and artwork, ready to review", 19, cx, cy + 84, MUTED, align="center"),
    ]), op=picks[0] + 8, ks=layer_ks(o=anim([(0, [100]), (t_send + 4, [100]), (picks[0], [0])])))
    x = x0 - 16
    lit = [[(picks[0], picks[1])], [(picks[1], picks[2])], [(picks[2], None)]]
    for k, label in enumerate(STEPS):
        base, w = pill(label, x, 118, size=19, h=46, color=PANEL, edge="#ffffff", edge_o=12, pad=20)
        on, _ = pill(label, x, 118, size=19, h=46, color="#13233f", edge=FOCUS, pad=20)
        m.shape(f"step {k}", base, ks=layer_ks(o=55))
        m.shape(f"step {k} lit", on, ks=layer_ks(o=on_off(lit[k])))
        x += w + 12

    hero_list(m, imgs, picks[0], picks[1], x0, top)
    hero_clips(m, imgs, picks[1] + 6, picks[2], x0, top)      # each phase starts as the last one has faded
    hero_thumbs(m, imgs, picks[2] + 6, OP, x0, top)

    add_fade(m, OP, 5, 14)
    markers = [(0, 84, "curated-lists"), (84, 84, "clips-in-every-ratio"), (168, 84, "branded-thumbnails")]
    write(animation(m, PRECOMPS, FPS, "Agentic Layer hero", images=imgs.assets.values(), markers=markers),
          "agentic-hero")


# --------------------------------------------------------------- hero, v3
#
# Chat first, with no frame: the question, the input and three suggestions sit
# straight on the page. The request is typed one letter at a time and each
# suggestion lights up as its words are typed. On send the input grows into the
# chat, still alone in the middle; then the chat docks right and the workspace
# opens out to its left (the Creative Agent's own layout). There, each film's
# most intense scenes arrive as 16:9 shots that reframe to 9:16 vertical clips.
# Transparent background, so it sits on the page; loops on its own.

PROMPT3 = "Turn the most intense scenes in 3 sci-fi films into vertical TikTok clips"
REPLIES3 = ["I found 3 sci-fi titles: Arrival, Sunshine and The Martian. Pulled their most intense scenes "
            "and reframed them as 9:16 vertical clips.",
            "Added the top clips to your TikTok list. Open a title in Creative Lab to fine-tune."]

# Material Design icons (Apache 2.0)
I_MOVIE = ("M18 4l2 4h-3l-2-4h-2l2 4h-3l-2-4H8l2 4H7L5 4H4c-1.1 0-1.99.9-1.99 2L2 18c0 1.1.9 2 2 2h16c1.1 0 "
           "2-.9 2-2V4h-4z")
I_PORTRAIT = ("M17 3H7c-1.1 0-1.99.9-1.99 2L5 19c0 1.1.89 2 1.99 2H17c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2zm0 "
              "16H7V5h10v14z")
I_PHONE = ("M17 1.01L7 1c-1.1 0-2 .9-2 2v18c0 1.1.9 2 2 2h10c1.1 0 2-.9 2-2V3c0-1.1-.9-1.99-2-1.99zM17 "
           "19H7V5h10v14z")
I_ARROW = "M12 4l-1.41 1.41L16.17 11H4v2h12.17l-5.58 5.59L12 20l8-8z"
I_CLOSE = ("M19 6.41L17.59 5 12 10.59 6.41 5 5 6.41 10.59 12 5 17.59 6.41 19 12 13.41 17.59 19 19 17.59 "
           "13.41 12z")
I_EXPAND = "M21 11V3h-8l3.29 3.29-10 10L3 13v8h8l-3.29-3.29 10-10z"
I_GRID = ("M3 3v8h8V3H3zm6 6H5V5h4v4zm-6 4v8h8v-8H3zm6 6H5v-4h4v4zm4-16v8h8V3h-8zm6 6h-4V5h4v4zm-6 "
          "4v8h8v-8h-8zm6 6h-4v-4h4v4z")
# (icon, label, the word in the request that picks it)
SUGGESTIONS = [(I_MOVIE, "Scenes by mood", "intense"),
               (I_PORTRAIT, "Vertical 9:16 clips", "vertical"),
               (I_PHONE, "Ready for TikTok", "TikTok")]

# (title, meta, poster crop, clips); a clip is (image, 9:16 crop as cx, cy, height in image px,
# where in the film, relevance, length, added to the list)
TITLES3 = [
    ("Arrival", "2016  ·  Sci-fi  ·  1h 56m", ("arrival", (290, 100, 140, 200)), [
        ("arrival", (128, 115.5, 231), "17m 05s", 96, "0:28", True),
        ("arrival", (290, 100, 200), "81m 40s", 93, "0:24", True),
        ("arrival", (352, 120, 200), "94m 12s", 91, "0:31", False),
        ("arrival", (300, 140, 180), "106m 30s", 88, "0:19", False)]),
    ("Sunshine", "2007  ·  Sci-fi  ·  1h 47m", ("sunshine", (205, 115.5, 161.7, 231)), [
        ("sunshine", (205, 115.5, 231), "72m 18s", 95, "0:26", True),
        ("sunshine", (70, 115.5, 231), "48m 30s", 92, "0:22", True),
        ("sunshine", (205, 120, 170), "91m 05s", 89, "0:30", False),
        ("sunshine", (340, 115.5, 231), "98m 44s", 86, "0:18", False)]),
    ("The Martian", "2015  ·  Sci-fi  ·  2h 21m", ("martian", (205, 115.5, 161.7, 231)), [
        ("martian", (205, 115.5, 231), "38m 12s", 94, "0:27", False),
        ("martian", (70, 115.5, 231), "72m 40s", 90, "0:21", False),
        ("martian", (220, 95, 180), "111m 05s", 87, "0:25", False),
        ("martian", (140, 115.5, 231), "124m 20s", 85, "0:23", False)]),
]

CHAT = (1280, 100, 600, 944)                    # the docked chat
WORK = (40, 100, 1224, 944)                     # the workspace, to its left
SLIDE = 960 - (CHAT[0] + CHAT[2] / 2)           # the chat sits centred until it docks
CHAT_START = (960 - 552 / 2, 524, 552, 128)    # the input at the start: centred, no panel around it
TYPE_SIZE = 21
X0, TOP, GAP = 80, 132, 20                      # workspace content: left edge, first row, card gap
CARD_W = (WORK[2] - 2 * (X0 - WORK[0]) - 3 * GAP) / 4
CARD_H = CARD_W * 16 / 9
ROW_H = 104 + CARD_H + 92                       # header, cards, caption and the gap below
SCROLL = 500


def type_times(text, t0, char=1.25, space=2.25):
    """Frame at which each prefix of `text` is shown; spaces take a beat longer."""
    ts, t = [t0], float(t0)
    for ch in text:
        t += space if ch == " " else char
        ts.append(round(t))
    return ts


def typing(t0):
    """The request's lines with the frames each prefix appears on, and when the typing ends."""
    out, t = [], t0
    for line in wrap(REG, PROMPT3, TYPE_SIZE, CHAT[2] - 48 - 104):
        ts = type_times(line, t)
        out.append((line, ts))
        t = ts[-1] + 2                          # the space at the line break
    return out, t


def typewriter(m, name, text, size, x0, base, ts, op, parent=None, ks=None):
    """Reveals `text` one character at a time on the frames in `ts`; returns the caret's keyframes."""
    mk, ck = [], []
    for j, t in enumerate(ts):
        w = REG.width(text[:j], size) if j else 0
        mk.append((t, rrect(x0 - 2, base - 24, w + 4 if j else 0.1, 32, 0), "hold"))
        ck.append((t, [x0 + w + 2, base - 7], "hold"))
    m.shape(name, [REG.text(text, size, x0, base)], ip=ts[0], op=op, parent=parent, ks=ks,
            masks=[mask(anim(mk))])
    return ck


def suggestion_chip(icon_d, label, x, y, lit=False):
    size, h = 18, 50
    w = MED.width(label, size) + 74
    items = [group([rect(w, h, x + w / 2, y + h / 2, h / 2),
                    fill("#13233f" if lit else "#ffffff", 100 if lit else 4),
                    stroke(FOCUS if lit else "#ffffff", 1.4, 100 if lit else 14)]),
             group([ellipse(34, 34, x + 30, y + h / 2), fill(FOCUS, 30 if lit else 14)]),
             icon(icon_d, 18, x + 30, y + h / 2, color=FOCUS),
             MED.text(label, size, x + 56, y + h / 2 + size * 0.36, "#ffffff" if lit else "#c9d1de")]
    return bf(items), w


def reply_card(lines, x, y, w, size=21, lh=30, pad=20):
    """The agent's answer, in a card like the product's."""
    h = 2 * pad + lh * (len(lines) - 1) + size
    items = [group([rect(w, h, x + w / 2, y + h / 2, 14), fill("#ffffff", 5), stroke("#ffffff", 1, 7)])]
    items += [REG.text(t, size, x + pad, y + pad + size * 0.8 + k * lh, o=92) for k, t in enumerate(lines)]
    return bf(items), h


def hero3_chat(m, T, cam, lines):
    """The chat: frameless in the middle, then one box that grows, then docked on the right."""
    px, py, pw, ph = CHAT
    ix, iw, ih = px + 24, pw - 48, 128
    iy = py + ph - 24 - ih
    sx, sy = CHAT_START[:2]
    g0, g1 = T["grow"]
    o0, o1 = T["open"]
    send = T["send"]

    def grow(start, end):
        return anim([(0, start, "hold"), (g0, start, "smooth"), (g1, end)])

    # a wide oval that fades out completely inside the frame, even at the opening's 150% zoom,
    # so it never meets the edge of the animation on the page
    m.shape("glow", [group([ellipse(660, 660, 960, 540), gfill([(0, "#1d4fa8", 0.34), (0.45, "#1d4fa8", 0.14),
                                                                (1, "#1d4fa8", 0)],
                                                               (960, 540), (1290, 540), radial=True)],
                           p=(960, 540), a=(960, 540), s=(180, 100))],
            parent=cam, ks=layer_ks(o=anim([(0, [100]), (g0, [100]), (g1, [60]), (o1, [0])])))
    # everything in the chat rides on this: centred at first, docked right once the workspace opens
    slide = m.null("chat-slide", parent=cam, ks=layer_ks(
        p=anim([(0, [SLIDE, 0], "hold"), (o0, [SLIDE, 0], "smooth"), (o1, [0, 0])])))
    lx = sx - SLIDE                             # the input's start, in the chat's own coordinates

    # the chat grows out of the input
    m.shape("chat-panel", [group([
        rect(grow([iw, ih], [pw, ph]), 0, grow([lx + iw / 2, sy + ih / 2], [px + pw / 2, py + ph / 2]), 0, 18),
        fill(PANEL), stroke("#ffffff", 1.2, 12)])], parent=slide, ip=g0,
        ks=layer_ks(o=anim([(g0, [0]), (g0 + 8, [100])])))
    # the agent's mark leads the opening, then becomes the chat's header
    hx, hy = px + 44, py + 44
    m.shape("chat-mark", bf([group([rect(38, 38, hx, hy, 10), fill("#1d2a44")]),
                             icon(I_SPARKLE, 22, hx, hy, color=FOCUS)]), parent=slide,
            ks=layer_ks(a=(hx, hy), p=grow([960 - SLIDE, 380], [hx, hy]), s=grow([132, 132], [100, 100])))
    m.shape("chat-header", [SEMI.text("Agentic Layer", 23, px + 76, py + 52),
                            icon(I_CLOSE, 24, px + pw - 40, hy, color=MUTED)], parent=slide,
            ks=layer_ks(o=anim([(0, [0]), (g1 - 10, [0]), (g1 + 2, [100])])))
    m.shape("greeting", [SEMI.text("What do you need from your library?", 36, 960, 462, align="center"),
                         REG.text("Scenes, clips and artwork, ready for you to review.", 21, 960, 498, MUTED,
                                  align="center")],
            parent=cam, ks=layer_ks(o=anim([(0, [100]), (send - 2, [100]), (send + 6, [0])])))

    # the input, typed into one letter at a time; it rides with the growing chat
    bottom = m.null("input-dock", parent=slide, ks=layer_ks(p=grow([lx - ix, sy - iy], [0, 0])))
    m.shape("input", [group([rect(iw, ih, ix + iw / 2, iy + ih / 2, 16), fill(INPUT), stroke("#ffffff", 1.2, 16)])],
            parent=bottom)
    m.shape("input-focus", [group([rect(iw, ih, ix + iw / 2, iy + ih / 2, 16), stroke(FOCUS, 1.6)])],
            parent=bottom, ks=layer_ks(o=anim([(0, [0]), (T["type"] - 6, [0]), (T["type"], [80]), (send, [80]),
                                               (send + 10, [0])])))
    m.shape("placeholder", [REG.text("Describe what you need…", TYPE_SIZE, ix + 22, iy + 44, MUTED, o=80)],
            parent=bottom, op=T["type"])
    m.shape("placeholder-after", [REG.text("Ask anything…", TYPE_SIZE, ix + 22, iy + 44, MUTED, o=80)],
            parent=bottom, ip=g1, ks=layer_ks(o=vis(g1)))
    x0, lh = ix + 22, 30
    caret, typed_at = [], {}
    tb = g1 - 14                                # the request stays in the input until its bubble takes over
    handoff = anim([(0, [100]), (tb - 2, [100]), (tb + 6, [0])])
    for k, (line, ts) in enumerate(lines):
        caret += typewriter(m, f"typed {k}", line, TYPE_SIZE, x0, iy + 42 + k * lh, ts, tb + 8, parent=bottom,
                            ks=layer_ks(o=handoff))
        for _, _, word in SUGGESTIONS:
            if word in line and word not in typed_at:
                typed_at[word] = ts[line.index(word) + len(word)]
    blink = [(f, [100 if n % 2 == 0 else 0], "hold") for n, f in enumerate(range(0, T["type"], 9))]
    blink += [(T["type"], [100], "hold"), (send, [0])]
    m.shape("caret", [group([rect(2.5, 26, 0, 0, 1), fill("#ffffff")])], parent=bottom, op=send + 1,
            ks=layer_ks(p=anim([(0, [x0 + 2, iy + 35], "hold")] + caret), o=anim(blink)))
    m.shape("send", bf([group([ellipse(52, 52, 0, 0), fill(BLUE)]), icon(I_ARROW, 26, 0, 0)]), parent=bottom,
            ks=layer_ks(p=(ix + iw - 42, iy + ih - 42),
                        s=anim([(send - 5, [100, 100]), (send, [86, 86], "out"), (send + 10, [100, 100])])))

    # suggestions under the input; each lights up as its words are typed
    widths = [suggestion_chip(d, label, 0, 0)[1] for d, label, _ in SUGGESTIONS]
    x = 960 - (sum(widths) + 12 * (len(widths) - 1)) / 2
    cy = sy + ih + 34
    gone = anim([(0, [100]), (send, [100]), (send + 10, [0])])
    for k, (d, label, word) in enumerate(SUGGESTIONS):
        base, w = suggestion_chip(d, label, x, cy)
        on, _ = suggestion_chip(d, label, x, cy, lit=True)
        m.shape(f"suggestion {k}", base, parent=cam, op=send + 12, ks=layer_ks(o=gone))
        c = (x + w / 2, cy + 25)
        t_hit = typed_at.get(word, send)
        m.shape(f"suggestion {k} lit", on, parent=cam, ip=t_hit, op=send + 12, ks=layer_ks(
            a=c, p=c, s=anim([(t_hit, [100, 100], "out"), (t_hit + 5, [106, 106]), (t_hit + 14, [100, 100])]),
            o=anim([(t_hit, [0]), (t_hit + 5, [100]), (send, [100]), (send + 10, [0])])))
        x += w + 12

    # the conversation: the request, the agent thinking, then its answers
    bx, bw = px + 24, pw - 48
    uw = bw - 64
    shapes, bh = user_bubble(wrap(REG, PROMPT3, 22, uw - 40), bx + bw - uw, py + 100, uw)
    m.shape("user-bubble", shapes, parent=slide, ip=tb,
            ks=layer_ks(p=anim([(tb, [0, 24], "out"), (tb + 18, [0, 0])]), o=vis(tb)))
    y = py + 100 + bh + 28
    ts = g1 + 6
    dots = [group([ellipse(10, 10, bx + 12 + 18 * k, y + 20), fill("#ffffff")],
                  o=anim([(ts + 3 * k + 9 * n, [25 if n % 2 == 0 else 90]) for n in range(12)])) for k in range(3)]
    m.shape("thinking", dots, parent=slide, ip=ts, op=T["results"])
    for k, (text, t_r) in enumerate(zip(REPLIES3, (T["results"], T["added"] - 6))):
        items, h = reply_card(wrap(REG, text, 21, bw - 40 - 40), bx, y, bw - 40)
        m.shape(f"reply {k}", items, parent=slide, ip=t_r,
                ks=layer_ks(p=anim([(t_r, [0, 16], "out"), (t_r + 18, [0, 0])]), o=vis(t_r)))
        y += h + 16


def clip_card(m, imgs, name, img, crop, box, t_in, parent):
    """A 16:9 shot that reframes to a 9:16 vertical clip around its subject, then plays."""
    x, y, w, h = box
    iw, ih = isize(img)
    cx, cy, ch = crop
    s_wide, s_tall = 100 * w / iw, 100 * h / ch
    hw = w * ih / iw                            # the 16:9 shot's height in the card
    r0, r1 = t_in + 12, t_in + 34
    c = Comp(round(w), round(h), m.op, f"comp_{name}")
    PRECOMPS.append(c)
    c.image("img", imgs(img), ks=layer_ks(
        p=(w / 2, h / 2),
        a=anim([(0, [iw / 2, ih / 2], "hold"), (r0, [iw / 2, ih / 2], "smooth"), (r1, [cx, cy], "linear"),
                (m.op, [cx + 4, cy])]),
        s=anim([(0, [s_wide, s_wide], "hold"), (r0, [s_wide, s_wide], "smooth"), (r1, [s_tall, s_tall], "linear"),
                (m.op, [s_tall * 1.05, s_tall * 1.05])])))
    m.precomp(name, c, ip=t_in, parent=parent, ks=layer_ks(p=(x, y), o=vis(t_in, ramp=8)),
              masks=[mask(anim([(r0, rrect(0, (h - hw) / 2, w, hw, 14), "smooth"), (r1, rrect(0, 0, w, h, 14))]))])
    return r1


def card_ui(m, name, box, t_on, when, score, length, added, t_added, parent):
    """What sits on a clip once it's vertical: list chip, expand, play bar, and the caption below."""
    x, y, w, h = box
    bar_y, bar_w = y + h - 24, w - 32
    m.shape(f"{name} ui", bf([
        group([rect(w, h, x + w / 2, y + h / 2, 14), gfill([(0, "#000000", 0.35), (0.25, "#000000", 0),
                                                           (0.7, "#000000", 0), (1, "#000000", 0.7)],
                                                          (0, y), (0, y + h))]),
        group([rect(40, 40, x + w - 32, y + 36, 12), fill("#ffffff", 16)]),
        icon(I_EXPAND, 18, x + w - 32, y + 36),
        icon(I_PLAY, 26, x + 28, bar_y - 26),
        MED.text(length, 15, x + w - 16, bar_y - 20, align="right", o=90),
        group([rect(bar_w, 4, x + 16 + bar_w / 2, bar_y, 2), fill("#ffffff", 30)]),
        group([rect(anim([(t_on, [0.1, 4], "linear"), (m.op, [bar_w * 0.62, 4])]), 0,
                    anim([(t_on, [x + 16, bar_y], "linear"), (m.op, [x + 16 + bar_w * 0.31, bar_y])]), 0, 2),
               fill("#ffffff")]),
    ]), parent=parent, ip=t_on, ks=layer_ks(o=vis(t_on, ramp=8)))
    m.shape(f"{name} caption", [REG.text(f"{when}  ·  Relevance {score}%", 17, x + 4, y + h + 32, MUTED)],
            parent=parent, ip=t_on, ks=layer_ks(o=vis(t_on, ramp=8)))
    # "Add to list", which the agent then ticks
    off_w = MED.width("Add to list", 15) + 28
    m.shape(f"{name} add", bf([group([rect(off_w, 34, x + 16 + off_w / 2, y + 36, 17), fill("#ffffff", 16)]),
                               MED.text("Add to list", 15, x + 30, y + 41.5, o=85)]), parent=parent, ip=t_on,
            ks=layer_ks(o=anim([(t_on, [0]), (t_on + 8, [100])] + ([(t_added, [100]), (t_added + 4, [0])]
                                                                    if added else []))))
    if added:
        on_w = MED.width("Added to list", 15) + 50
        c = (x + 16 + on_w / 2, y + 36)
        m.shape(f"{name} added", bf([group([rect(on_w, 34, c[0], c[1], 17), fill(BLUE)]),
                                     icon(I_CHECK, 18, x + 32, c[1]),
                                     MED.text("Added to list", 15, x + 46, y + 41.5)]), parent=parent,
                ip=t_added, ks=layer_ks(a=c, p=c, o=vis(t_added, ramp=4),
                                        s=anim([(t_added, [80, 80], "out"), (t_added + 6, [108, 108]),
                                                (t_added + 14, [100, 100])])))


def title_header(m, imgs, k, title, meta, poster, y, t_in, parent):
    """A film's row header: poster, title and year, and the way into Creative Lab."""
    img, crop = poster
    media(m, f"poster {k}", imgs(img), crop, (X0, y, 56, 80), 8, t_in, parent=parent)
    right = WORK[0] + WORK[2] - (X0 - WORK[0])
    tw = MED.width("Open in Creative Lab", 19) + 48
    m.shape(f"head {k}", bf([
        SEMI.text(title, 28, X0 + 76, y + 36),
        REG.text(meta, 19, X0 + 76, y + 68, MUTED),
        group([rect(tw, 48, right - 108 - tw / 2, y + 40, 24), fill("#ffffff", 4), stroke("#ffffff", 1.2, 16)]),
        MED.text("Open in Creative Lab", 19, right - 108 - tw / 2, y + 47, align="center"),
        group([rect(96, 48, right - 48, y + 40, 24), fill("#ffffff", 4), stroke("#ffffff", 1.2, 16)]),
        icon(I_GRID, 20, right - 72, y + 40),
        icon(I_LIST, 20, right - 26, y + 40, color=MUTED),
    ]), parent=parent, ks=layer_ks(o=vis(t_in)))


def hero3_workspace(m, imgs, T, cam):
    """The workspace that opens out of the chat to the left, then fills with vertical clips."""
    o0, o1 = T["open"]
    wx, wy, ww, wh = WORK
    cx0 = CHAT[0] + SLIDE                       # the chat's left edge while it sits centred
    m.shape("workspace", [group([
        rect(anim([(o0, [CHAT[2], wh], "smooth"), (o1, [ww, wh])]), 0,
             anim([(o0, [cx0 + CHAT[2] / 2, wy + wh / 2], "smooth"), (o1, [wx + ww / 2, wy + wh / 2])]), 0, 18),
        fill(PANEL, 55), stroke("#ffffff", 1, 8)])], ip=o0, parent=cam)

    # its contents live in their own comp, clipped to the workspace as it opens and as it scrolls
    ws = Comp(m.w, m.h, m.op, "comp_workspace")
    PRECOMPS.append(ws)
    clip = mask(anim([(o0, rrect(cx0, wy, CHAT[2], wh, 18), "smooth"), (o1, rrect(wx, wy, ww, wh, 18))]))
    m.precomp("workspace-content", ws, ip=o0, parent=cam, masks=[clip])

    # while the agent works: placeholders for the first film
    r = T["results"]
    t_sk = o0 + 12
    pulse = [(t_sk + 9 * n, [100 if n % 2 else 45]) for n in range((r - t_sk) // 9 + 1)]
    sk = [group([rect(56, 80, X0 + 28, TOP + 40, 8), fill("#ffffff", 6)]),
          group([rect(220, 22, X0 + 76 + 110, TOP + 28, 11), fill("#ffffff", 7)]),
          group([rect(160, 16, X0 + 76 + 80, TOP + 62, 8), fill("#ffffff", 5)])]
    for k in range(4):
        x = X0 + k * (CARD_W + GAP)
        sk.append(group([rect(CARD_W, CARD_H, x + CARD_W / 2, TOP + 104 + CARD_H / 2, 14), fill("#ffffff", 5)]))
    ws.shape("skeleton", sk, ip=t_sk, op=r + 10, ks=layer_ks(o=anim(pulse + [(r, [100]), (r + 10, [0])])))

    s0, s1 = T["scroll"]
    feed = ws.null("feed", ks=layer_ks(p=anim([(0, [0, 0], "hold"), (s0, [0, 0], "smooth"), (s1, [0, -SCROLL])])))
    for k, (title, meta, poster, clips) in enumerate(TITLES3):
        y = TOP + k * ROW_H
        t_row = r + 44 * k
        title_header(ws, imgs, k, title, meta, poster, y, t_row, feed)
        for j, (img, crop, when, score, length, added) in enumerate(clips):
            box = (X0 + j * (CARD_W + GAP), y + 104, CARD_W, CARD_H)
            t_in = t_row + 6 + 9 * j
            t_on = clip_card(ws, imgs, f"clip {k}-{j}", img, crop, box, t_in, feed)
            card_ui(ws, f"clip {k}-{j}", box, t_on + 2, when, score, length, added,
                    T["added"] + 8 * j + 16 * k, feed)


def build_hero_v3():
    W, H = 1920, 1080
    PRECOMPS.clear()
    imgs = Images()
    T = {"type": 26}
    lines, t_typed = typing(T["type"])
    send = t_typed + 10
    T.update(send=send, grow=(send + 4, send + 44), open=(send + 62, send + 102))
    T["results"] = T["open"][1] + 20
    T["added"] = T["results"] + 120
    T["scroll"] = (T["added"] + 44, T["added"] + 92)
    OP = T["scroll"][1] + 78
    scene = Comp(W, H, OP, "comp_scene")        # no background: it sits on the page
    g0, g1 = T["grow"]                          # the opening fills the frame, then the view pulls back
    cam = scene.null("camera", ks=layer_ks(p=(W / 2, H / 2), a=(W / 2, H / 2), s=anim(
        [(0, [150, 150], "hold"), (g0, [150, 150], "smooth"), (g1, [100, 100])])))
    # the workspace is drawn first so the chat stays on top of it; it opens out from behind the chat
    hero3_workspace(scene, imgs, T, cam)
    hero3_chat(scene, T, cam, lines)
    # the loop fades the whole scene, so nothing paints over the page
    m = Comp(W, H, OP, "main")
    m.precomp("scene", scene, ks=layer_ks(o=anim([(0, [0]), (6, [100]), (OP - 18, [100]), (OP, [0])])))
    markers = [(0, g0, "chat"), (g0, T["results"] - g0, "expand"), (T["results"], OP - T["results"], "vertical-clips")]
    write(animation(m, [scene] + PRECOMPS, FPS, "Agentic Layer hero (v3)", images=imgs.assets.values(),
                    markers=markers), "agentic-hero-v3")


# ----------------------------------------------------------- section helpers
#
# The section visuals use the hero's look: an "Agentic Layer" window, the request
# in a blue bubble, the agent's answer in a card, and the result underneath.
# Every request reads like one a team would type, and every result shows exactly
# what it asked for. Nothing is imported by hand: the agent does the work and
# people only approve.

SECTION_BG = "#0d1520"


def section_start(op, agent):
    """A 1280x720 Agentic Layer window, with the agent doing the work named on the right."""
    W, H = 1280, 720
    PRECOMPS.clear()
    m = Comp(W, H, op, "main")
    m.shape("bg", [group([rect(W, H, W / 2, H / 2), fill(SECTION_BG)]),
                   group([ellipse(1300, 700, 980, 0), gfill([(0, "#1b2a46", 0.9), (1, SECTION_BG, 0)],
                                                            (980, 0), (1630, 0), radial=True)])])
    aw = MED.width(agent, 17) + 32
    m.shape("header", bf([
        group([rect(40, 40, 56, 46, 11), fill("#1d2a44")]),
        icon(I_SPARKLE, 23, 56, 46, color=FOCUS),
        SEMI.text("Agentic Layer", 23, 88, 54),
        group([rect(aw, 34, W - 48 - aw / 2, 46, 17), fill("#ffffff", 5), stroke("#ffffff", 1, 14)]),
        MED.text(agent, 17, W - 48 - aw / 2, 52, MUTED, align="center"),
        group([rect(W - 72, 1, W / 2, 90), fill("#ffffff", 8)]),
    ]))
    return m, Images()


def section_prompt(m, prompt, reply, t=0):
    """The request (right-aligned bubble) and the agent's answer in a card under it.

    A newline in the request marks where its line should break."""
    size = 24
    lines = [ln for part in prompt.split("\n") for ln in wrap(REG, part, size, 960)]
    bw = max(REG.width(t_, size) for t_ in lines) + 40
    shapes, bh = user_bubble(lines, m.w - 36 - bw, 112, bw, size=size, lh=32, pad=18)
    appear(m, "prompt", shapes, t, dy=16)
    y = 112 + bh + 16
    rlines = wrap(REG, reply, 22, 1000)
    items, h = reply_card(rlines, 36, y, max(REG.width(t_, 22) for t_ in rlines) + 40, size=22)
    appear(m, "reply", items, t + 10, dy=12)
    return y + h + 28


# --------------------------------------------- section: Curated Lists

LIST_FOCUS = [(36, 76), (76, 116), (116, 156), (156, 196), (196, None)]


def build_curated_lists():
    OP = 240
    m, imgs = section_start(OP, "Curation Agent")
    top = section_prompt(m, "Give me 5 space movies for a Friday night line-up",
                         "Ranked 5 titles from your catalog by how well they fit a Friday space night.")
    rw, rh, gap, x0 = 1208, 72, 6, 36
    for k, (name, title, genres, moods, score) in enumerate(LINEUP):
        y = top + k * (rh + gap)
        t = 14 + 3 * k
        gx = x0 + 196 + REG.width(genres, 17) + 16
        pills, _ = pill_row(moods, gx, y + 40, gap=6, size=14, h=26, color=MOOD, fill_o=16,
                            edge=MOOD, edge_o=55, text_color="#ffd9d2", pad=10)
        bar_w = 180
        bar_x = x0 + rw - 24 - bar_w
        ks = layer_ks(p=anim([(t, [0, 14], "out"), (t + 16, [0, 0])]), o=vis(t))
        m.shape(f"row {k}", bf([
            group([rect(rw, rh, x0 + rw / 2, y + rh / 2, 12), fill(ROW)]),
            BOLD.text(str(k + 1), 24, x0 + 26, y + rh / 2 + 9, align="center", o=70),
            SEMI.text(title, 23, x0 + 196, y + 31),
            REG.text(genres, 17, x0 + 196, y + 59, MUTED),
            group(pills),
            group([rect(bar_w, 7, bar_x + bar_w / 2, y + 52, 3.5), fill("#ffffff", 12)]),
            group([rect(anim([(t + 6, [0.1, 7], "out"), (t + 30, [bar_w * score / 100, 7])]), 0,
                        anim([(t + 6, [bar_x, y + 52], "out"), (t + 30, [bar_x + bar_w * score / 200, y + 52])]),
                        0, 3.5), fill(FOCUS)]),
            BOLD.text(f"{score}%", 24, bar_x + bar_w, y + 32, align="right"),
            REG.text("relevance", 15, bar_x, y + 32, MUTED),
        ]), ks=ks)
        media(m, f"row {k} thumb", imgs(name), full(name, (0, 0, 112, 63)), (x0 + 56, y + 4.5, 112, 63), 6, t)
        m.shape(f"row {k} lit", [group([rect(rw, rh, x0 + rw / 2, y + rh / 2, 12), fill("#ffffff", 5)])]
                + focus_ring(x0, y, rw, rh, 12, ring=3, glow=8), ks=layer_ks(o=on_off([LIST_FOCUS[k]])))
    add_fade(m, OP)
    write(animation(m, PRECOMPS, FPS, "Agentic Layer: Curated Lists", images=imgs.assets.values()),
          "agentic-curated-lists")


# --------------------------------------------- section: Clips in Every Ratio

def build_clips():
    """One scene, asked for by name, cut for every screen; the vertical cut is the one in focus."""
    OP = 90
    m, imgs = section_start(OP, "Creative Agent")
    top = section_prompt(m, "Give me a 30-second clip from Top Gun: Maverick of the low-level canyon flight,\n"
                            "for TV, feeds and TikTok",
                         "Found the canyon flight and cut it in 16:9 for TV, 1:1 for feeds and 9:16 for TikTok.")
    h, gap, x = 320, 20, 36
    clips = [("16:9  ·  TV", (480, 270, 960, 540), h * 16 / 9),
             ("1:1  ·  Feeds", (690, 270, 540, 540), h),
             ("9:16  ·  TikTok & Shorts", (790, 270, 540 * 9 / 16, 540), h * 9 / 16)]
    for k, (label, crop, w) in enumerate(clips):
        t = 14 + 4 * k
        box = (x, top, w, h)
        media(m, f"clip {k}", imgs("topgun_hero"), crop, box, 12, t)
        ty = top + h - 20
        tw = w - 32
        m.shape(f"clip {k} ui", bf([
            scrim(x, top, w, h, 12, top=0.62),
            icon(I_PLAY, 26, x + 28, ty - 24),
            MED.text("0:30", 15, x + w - 16, ty - 18, align="right", o=90),
            group([rect(tw, 4, x + 16 + tw / 2, ty, 2), fill("#ffffff", 30)]),
            group([rect(tw * 0.42, 4, x + 16 + tw * 0.21, ty, 2), fill("#ffffff")]),
        ]), ks=layer_ks(o=vis(t)))
        chip, _ = chip_check(label, x, top + h + 16, size=16, h=32)
        appear(m, f"clip {k} label", chip, t + 4, dy=8)
        if k == 2:
            m.shape("clip 9x16 focus", focus_ring(*box, 12, ring=3, glow=8), ks=layer_ks(o=on_off([(t + 16, None)])))
        x += w + gap
    add_fade(m, OP)
    write(animation(m, PRECOMPS, FPS, "Agentic Layer: Clips in Every Ratio", images=imgs.assets.values()),
          "agentic-clips")


# --------------------------------------------- section: Branded Thumbnails

# (image, title, when, crop or None for the whole frame); the scenes match the hero's first clip of each
THUMBS = [("arrival", "Arrival", "Scene at 17m 05s", (115, 112, 230, 129.4)),
          ("sunshine", "Sunshine", "Scene at 72m 18s", None),
          ("martian", "The Martian", "Scene at 38m 12s", None)]


def build_branded():
    """Three titles, a strong scene from each with its logo placed, ready to approve."""
    OP = 90
    m, imgs = section_start(OP, "Creative Agent")
    top = section_prompt(m, "Make 3 thumbnails for Arrival, Sunshine and The Martian and add their logos",
                         "Picked a strong scene from each title and placed its logo, in 16:9, 1:1 and 9:16.")
    gap, x0 = 24, 36
    tw = (m.w - 2 * x0 - 2 * gap) / 3
    th = tw * 9 / 16
    for k, (name, title, scene, crop) in enumerate(THUMBS):
        x = x0 + k * (tw + gap)
        t = 14 + 4 * k
        media(m, f"thumb {k}", imgs(name), crop or full(name, (0, 0, tw, th)), (x, top, tw, th), 12, t)
        m.shape(f"thumb {k} logo", bf([scrim(x, top, tw, th, 12)] + title_logo(name, x + 20, top + th - 22, 26)),
                ks=layer_ks(o=vis(t + 8)))
        cx = x + tw
        chips = []
        for label in ("9:16", "1:1", "16:9"):
            c, w = chip_check(label, 0, 0, size=15, h=28)
            cx -= w
            chips.append(group(c, p=(cx, top + th + 14)))
            cx -= 8
        appear(m, f"thumb {k} meta", [SEMI.text(title, 20, x + 2, top + th + 34),
                                      REG.text(scene, 16, x + 2, top + th + 58, MUTED),
                                      group(chips)], t + 6, dy=8)
    by = top + th + 96
    appear(m, "approve-bar", bf([
        group([rect(m.w - 72, 1, m.w / 2, by - 10), fill("#ffffff", 8)]),
        SEMI.text("3 titles  ·  3 ratios  ·  9 thumbnails ready", 21, x0 + 2, by + 30),
        REG.text("Nothing is published until you approve it.", 17, x0 + 2, by + 56, MUTED),
        group([rect(280, 52, m.w - x0 - 140, by + 24, 26), fill(BLUE)]),
        icon(I_CHECK, 22, m.w - x0 - 280 + 34, by + 24),
        SEMI.text("Approve & publish", 20, m.w - x0 - 280 + 54, by + 31),
    ]), 30, dy=8)
    add_fade(m, OP)
    write(animation(m, PRECOMPS, FPS, "Agentic Layer: Branded Thumbnails", images=imgs.assets.values()),
          "agentic-branded-thumbnails")


if __name__ == "__main__":
    build_hero()
    build_hero_v3()
    build_curated_lists()
    build_clips()
    build_branded()
