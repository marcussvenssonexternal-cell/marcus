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
  agentic-curated-lists         What the agent does, row 1 (1280x720, 8 s). The
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
SIZE = {"interstellar_wide": (960, 540)}        # every other image is 410x231
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


def import_button(x, y, w, h=36, label="Import", size=17):
    return bf([group([rect(w, h, x + w / 2, y + h / 2, 8), fill("#2a4fb8")]),
               MED.text(label, size, x + w / 2, y + h / 2 + size * 0.36, align="center")])


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


# --------------------------------------------------------------- hero, v2 draft
#
# Chat first: a single chat card in the middle, the request typed one letter at a
# time; on send the chat docks to the right and the workspace unfolds to its left
# (the Creative Agent's own layout), then the results stream in and get approved.
# Loops on its own (13 s); it is not tied to a rotating headline.

PROMPT2 = "Build a Space Night line-up with clips and branded thumbnails"
SUGGESTIONS = ["Find every rooftop scene in Paris", "Make it 9:16", "A cozier Friday line-up"]
REPLIES2 = REPLIES + [("publish", "Published 9 assets to the Space Night campaign.")]


def typewriter(m, name, text, size, x0, base, t0, op, parent=None):
    """Reveals `text` one character at a time (spaces take a beat longer).

    Returns the frame typing ends and the caret's keyframes."""
    t, mk, ck = t0, [], []
    for j in range(len(text) + 1):
        w = REG.width(text[:j], size) if j else 0
        mk.append((t, rrect(x0 - 2, base - 24, w + 4 if j else 0.1, 32, 0), "hold"))
        ck.append((t, [x0 + w + 2, base - 7], "hold"))
        if j < len(text):
            t += 2 if text[j] == " " else 1
    m.shape(name, [REG.text(text, size, x0, base)], ip=t0, op=op, parent=parent, masks=[mask(anim(mk))])
    return t, ck


def hero2_chat(m, T, cam):
    """The chat: a card in the middle that docks to the right as the workspace opens."""
    px, py, pw, ph = 1280, 100, 600, 944        # docked
    sx, sy, sh = 660, 330, 420                  # the opening card
    e0, e1 = T["expand"]

    def dock(dy):
        return layer_ks(p=anim([(0, [sx - px, dy], "hold"), (e0, [sx - px, dy], "smooth"), (e1, [0, 0])]))

    m.shape("card-glow", [group([ellipse(1100, 760, 960, 540), gfill([(0, "#1d4fa8", 0.55), (1, BG, 0)],
                                                                      (960, 540), (1510, 540), radial=True)])],
            parent=cam, ks=layer_ks(o=anim([(0, [100]), (e0, [100]), (e1, [0])])))
    m.shape("chat-panel", [group([
        rect(anim([(e0, [pw, sh], "smooth"), (e1, [pw, ph])]), 0,
             anim([(e0, [sx + pw / 2, sy + sh / 2], "smooth"), (e1, [px + pw / 2, py + ph / 2])]), 0, 18),
        fill(PANEL), stroke("#ffffff", 1.2, 12)])], parent=cam)
    top = m.null("chat-top", ks=dock(sy - py), parent=cam)
    iy = py + ph - 24 - 128                     # the input, at the bottom of the panel
    bottom = m.null("chat-bottom", ks=dock(sy + sh - 24 - 128 - iy), parent=cam)

    m.shape("chat-head", bf([
        group([rect(38, 38, px + 47, py + 44, 10), fill("#1d2a44")]),
        icon(I_SPARKLE, 22, px + 47, py + 44, color=FOCUS),
        SEMI.text("Vionlabs Agentic Layer", 21, px + 78, py + 52),
    ]), parent=top)
    m.shape("greeting", [SEMI.text("What do you need from your library?", 30, px + 28, py + 150),
                         REG.text("Lists, clips and artwork, ready for you to review.", 20, px + 28, py + 186, MUTED)],
            parent=top, ks=layer_ks(o=anim([(0, [100]), (T["send"] - 4, [100]), (T["send"] + 1, [0])])))

    # suggestions under the card, gone once typing starts
    x, chips = 0, []
    for s in SUGGESTIONS:
        g, w = pill(s, 0, 0, size=17, h=38, color="#ffffff", fill_o=4, edge="#ffffff", edge_o=16, pad=16,
                    text_color="#c9d1de")
        chips.append((g, w))
        x += w + 10
    x = 960 - (x - 10) / 2
    items = [MED.text("Try asking", 16, 960, sy + sh + 48, MUTED, align="center", tracking=0.08)]
    for g, w in chips:
        items.append(group(g, p=(x, sy + sh + 72)))
        x += w + 10
    m.shape("suggestions", items, parent=cam,
            ks=layer_ks(o=anim([(0, [100]), (T["type"], [100]), (T["type"] + 10, [0])])))

    # the input, typed into one letter at a time
    ix, iw, ih = px + 24, pw - 48, 128
    m.shape("input", [group([rect(iw, ih, ix + iw / 2, iy + ih / 2, 14), fill(INPUT), stroke("#ffffff", 1.2, 14)])],
            parent=bottom)
    m.shape("input-focus", [group([rect(iw, ih, ix + iw / 2, iy + ih / 2, 14), stroke(FOCUS, 1.6)])], parent=bottom,
            ks=layer_ks(o=anim([(0, [0]), (T["type"] - 6, [0]), (T["type"], [80]), (T["send"], [80]),
                                (T["send"] + 8, [0])])))
    m.shape("placeholder", [REG.text("Describe what you need…", 21, ix + 22, iy + 44, MUTED, o=80)], parent=bottom,
            op=T["type"])
    m.shape("placeholder-after", [REG.text("Ask a follow-up…", 21, ix + 22, iy + 44, MUTED, o=80)], parent=bottom,
            ip=T["send"] + 2, ks=layer_ks(o=vis(T["send"] + 2)))
    size, lh, x0 = 21, 30, ix + 22
    t, caret = T["type"], []
    for k, line in enumerate(wrap(REG, PROMPT2, size, iw - 104)):
        t, keys = typewriter(m, f"typed {k}", line, size, x0, iy + 42 + k * lh, t, T["send"], parent=bottom)
        caret += keys
        t += 2                                  # the space at the line break
    blink = [(f, [100 if n % 2 == 0 else 0], "hold") for n, f in enumerate(range(0, T["type"], 8))]
    blink += [(T["type"], [100], "hold"), (T["send"], [0])]
    m.shape("caret", [group([rect(2.5, 26, 0, 0, 1), fill("#ffffff")])], parent=bottom, op=T["send"] + 1,
            ks=layer_ks(p=anim([(0, [x0 + 2, iy + 35], "hold")] + caret), o=anim(blink)))
    sx_, sy_ = ix + iw - 40, iy + ih - 40
    m.shape("send", bf([group([ellipse(48, 48, 0, 0), fill(BLUE)]), icon(I_SEND, 22, 2, 0)]), parent=bottom,
            ks=layer_ks(p=(sx_, sy_), s=anim([(T["send"] - 4, [100, 100]), (T["send"], [86, 86], "out"),
                                               (T["send"] + 8, [100, 100])])))

    # the conversation
    bx, bw = px + 24, pw - 48
    shapes, bh = user_bubble(wrap(REG, PROMPT2, 22, bw - 40), bx, py + 96, bw)
    tb = T["send"] + 2
    m.shape("user-bubble", shapes, parent=top, ip=tb,
            ks=layer_ks(p=anim([(tb, [0, 24], "out"), (tb + 16, [0, 0])]), o=vis(tb)))
    y = py + 96 + bh + 52
    ts = T["send"] + 6
    dots = [group([ellipse(10, 10, bx + 8 + 18 * k, y - 8), fill("#ffffff")],
                  o=anim([(ts + 3 * k + 8 * n, [25 if n % 2 == 0 else 90]) for n in range(8)])) for k in range(3)]
    m.shape("thinking", dots, parent=top, ip=ts, op=T["phases"][0])
    for k, (tool, text) in enumerate(REPLIES2):
        items, h = agent_reply(tool, wrap(REG, text, 22, bw - 8), bx, y)
        t_r = T["phases"][k] + 2
        m.shape(f"reply {k}", items, parent=top, ip=t_r,
                ks=layer_ks(p=anim([(t_r, [0, 14], "out"), (t_r + 16, [0, 0])]), o=vis(t_r)))
        y += h + 44


def hero2_workspace(m, imgs, T, cam):
    """The workspace that unfolds to the left of the chat, then fills with results."""
    e0, e1 = T["expand"]
    wx0, wx1, py, ph = 40, 1264, 100, 944
    m.shape("workspace", [group([
        rect(anim([(e0, [0.1, 420], "smooth"), (e1, [wx1 - wx0, ph])]), 0,
             anim([(e0, [644, 540], "smooth"), (e1, [(wx0 + wx1) / 2, py + ph / 2])]), 0, 18),
        fill(PANEL, 55), stroke("#ffffff", 1, 8)])], ip=e0, parent=cam)
    m.shape("logo", logo(wx0 + 4, 64, 22), parent=cam, ks=layer_ks(o=vis(e1 - 6)))

    # while the agent works: placeholders, clipped to the workspace as it opens
    x0, top = 72, 196
    t_sk, t_list = e0 + 10, T["phases"][0]
    pulse = [(t_sk + 8 * n, [100 if n % 2 else 45]) for n in range((t_list - t_sk) // 8 + 1)]
    clip = mask(anim([(e0, rrect(644, 330, 0.1, 420, 18), "smooth"), (e1, rrect(wx0, py, wx1 - wx0, ph, 18))]))
    sk = []
    for k in range(4):
        y = top + 104 + k * 134
        sk += [group([rect(1136, 124, x0 + 568, y + 62, 12), fill("#ffffff", 4)]),
               group([rect(192, 108, x0 + 70 + 96, y + 62, 8), fill("#ffffff", 6)]),
               group([rect(300 - 40 * k, 18, x0 + 286 + 150 - 20 * k, y + 40, 9), fill("#ffffff", 7)]),
               group([rect(200, 14, x0 + 286 + 100, y + 76, 7), fill("#ffffff", 5)])]
    m.shape("skeleton", sk, ip=t_sk, op=t_list + 8, parent=cam, masks=[clip],
            ks=layer_ks(o=anim(pulse + [(t_list, [100]), (t_list + 8, [0])])))

    p = T["phases"]
    lit = [[(p[0], p[1])], [(p[1], p[2])], [(p[2], None)]]
    x = x0 - 8
    for k, label in enumerate(STEPS):
        base, w = pill(label, x, 122, size=19, h=46, color=PANEL, edge="#ffffff", edge_o=12, pad=20)
        on, _ = pill(label, x, 122, size=19, h=46, color="#13233f", edge=FOCUS, pad=20)
        m.shape(f"step {k}", base, ks=layer_ks(o=anim([(e1 - 4, [0]), (e1 + 6, [55])])))
        m.shape(f"step {k} lit", on, ks=layer_ks(o=on_off(lit[k])))
        x += w + 12

    hero_list(m, imgs, p[0], p[1], x0, top)
    hero_clips(m, imgs, p[1] + 6, p[2], x0, top)
    hero_thumbs(m, imgs, p[2] + 6, m.op, x0, top, t_publish=p[3])


def build_hero_v2():
    W, H, OP = 1920, 1080, 390
    PRECOMPS.clear()
    imgs = Images()
    m = Comp(W, H, OP, "main")
    T = {"type": 22, "send": 96, "expand": (104, 134), "phases": [140, 210, 280, 342]}
    m.shape("bg", [group([rect(W, H, W / 2, H / 2), fill(BG)])])
    e0, e1 = T["expand"]                        # the opening card fills the frame, then the view pulls back
    cam = m.null("camera", ks=layer_ks(p=(W / 2, H / 2), a=(W / 2, H / 2), s=anim(
        [(0, [150, 150], "hold"), (e0, [150, 150], "smooth"), (e1, [100, 100])])))
    hero2_workspace(m, imgs, T, cam)
    hero2_chat(m, T, cam)
    add_fade(m, OP, 5, 18)
    markers = [(0, T["expand"][0], "chat"), (T["expand"][0], T["phases"][0] - T["expand"][0], "expand"),
               (T["phases"][0], OP - T["phases"][0], "results")]
    write(animation(m, PRECOMPS, FPS, "Agentic Layer hero (v2 draft)", images=imgs.assets.values(),
                    markers=markers), "agentic-hero-v2")


# ----------------------------------------------------------- section helpers

def section_start(op, agent):
    """A 1280x720 section canvas with the agent's top bar."""
    W, H = 1280, 720
    PRECOMPS.clear()
    m = Comp(W, H, op, "main")
    m.shape("bg", [group([rect(W, H, W / 2, H / 2), fill(BG)]),
                   group([ellipse(1100, 700, 900, 260), gfill([(0, "#1b2a46", 1), (1, BG, 0)],
                                                              (900, 260), (1450, 260), radial=True)])])
    agent_bar(m, W, agent, right="Space Night campaign")
    return m, Images()


def section_prompt(m, prompt, tool, reply, t=0):
    """The request (right-aligned bubble) and the agent's answer under it."""
    size = 21
    lines = wrap(REG, prompt, size, 700)
    bw = max(REG.width(t_, size) for t_ in lines) + 40
    shapes, bh = user_bubble(lines, m.w - 60 - bw, 84, bw, size=size, lh=29, pad=16)
    appear(m, "prompt", shapes, t, dy=16)
    y = 84 + bh + 34
    items, h = agent_reply(tool, [reply], 60, y, size=21)
    appear(m, "reply", items, t + 10, dy=12)
    return y + h + 24


# --------------------------------------------- section: Curated Lists

LIST_FOCUS = [(36, 76), (76, 116), (116, 156), (156, 196), (196, None)]


def build_curated_lists():
    OP = 240
    m, imgs = section_start(OP, "Curation Agent")
    top = section_prompt(m, "Build a Space Night line-up for Friday", "curate_list",
                         "Ranked 5 titles from your catalog by relevance.")
    rw, rh, gap, x0 = 1160, 80, 7, 60
    for k, (name, title, genres, moods, score) in enumerate(LINEUP):
        y = top + k * (rh + gap)
        t = 14 + 3 * k
        gx = x0 + 208 + REG.width(genres, 17) + 16
        pills, _ = pill_row(moods, gx, y + 44, gap=6, size=14, h=26, color=MOOD, fill_o=16,
                            edge=MOOD, edge_o=55, text_color="#ffd9d2", pad=10)
        bar_w = 180
        bar_x = x0 + rw - 24 - bar_w
        ks = layer_ks(p=anim([(t, [0, 14], "out"), (t + 16, [0, 0])]), o=vis(t))
        m.shape(f"row {k}", bf([
            group([rect(rw, rh, x0 + rw / 2, y + rh / 2, 10), fill(ROW)]),
            BOLD.text(str(k + 1), 24, x0 + 26, y + rh / 2 + 9, align="center", o=70),
            SEMI.text(title, 24, x0 + 208, y + 34),
            REG.text(genres, 17, x0 + 208, y + 63, MUTED),
            group(pills),
            group([rect(bar_w, 7, bar_x + bar_w / 2, y + 56, 3.5), fill("#ffffff", 12)]),
            group([rect(anim([(t + 6, [0.1, 7], "out"), (t + 30, [bar_w * score / 100, 7])]), 0,
                        anim([(t + 6, [bar_x, y + 56], "out"), (t + 30, [bar_x + bar_w * score / 200, y + 56])]),
                        0, 3.5), fill(FOCUS)]),
            BOLD.text(f"{score}%", 24, bar_x + bar_w, y + 36, align="right"),
            REG.text("relevance", 15, bar_x, y + 36, MUTED),
        ]), ks=ks)
        media(m, f"row {k} thumb", imgs(name), full(name, (0, 0, 128, 72)), (x0 + 56, y + 4, 128, 72), 6, t)
        m.shape(f"row {k} lit", [group([rect(rw, rh, x0 + rw / 2, y + rh / 2, 10), fill("#ffffff", 5)])]
                + focus_ring(x0, y, rw, rh, 10, ring=3, glow=8), ks=layer_ks(o=on_off([LIST_FOCUS[k]])))
    add_fade(m, OP)
    write(animation(m, PRECOMPS, FPS, "Agentic Layer: Curated Lists", images=imgs.assets.values()),
          "agentic-curated-lists")


# --------------------------------------------- section: Clips in Every Ratio

def build_clips():
    OP = 90
    m, imgs = section_start(OP, "Creative Agent")
    top = section_prompt(m, "Cut a 30-second clip from Interstellar for TV, feeds and Shorts", "cut_clips",
                         "Found the scene and reframed it for every screen.")
    h, gap, x = 336, 20, 60
    clips = [("16:9  ·  TV", (480, 270, 960, 540), h * 16 / 9),
             ("1:1  ·  Social feed", (480, 270, 540, 540), h),
             ("9:16  ·  Shorts & TikTok", (470, 270, 540 * 9 / 16, 540), h * 9 / 16)]
    for k, (label, crop, w) in enumerate(clips):
        t = 14 + 4 * k
        box = (x, top, w, h)
        media(m, f"clip {k}", imgs("interstellar_wide"), crop, box, 10, t)
        ty = top + h - 18
        tw = w - 28
        m.shape(f"clip {k} ui", bf([
            scrim(x, top, w, h, 10, top=0.6),
            group([ellipse(56, 56, x + w / 2, top + h / 2), fill("#000000", 45), stroke("#ffffff", 2, 70)]),
            icon(I_PLAY, 26, x + w / 2 + 2, top + h / 2),
            group([rect(tw, 4, x + 14 + tw / 2, ty, 2), fill("#ffffff", 30)]),
            group([rect(tw * 0.4, 4, x + 14 + tw * 0.2, ty, 2), fill(BLUE)]),
            MED.text("0:30", 15, x + w - 14, ty - 12, align="right", o=90),
        ]), ks=layer_ks(o=vis(t)))
        chip, _ = pill(label, x, top + h + 14, size=16, h=32, color=GENRE, edge=GENRE_EDGE, pad=12)
        appear(m, f"clip {k} label", chip, t + 4, dy=8)
        appear(m, f"clip {k} import", import_button(x, top + h + 60, w), t + 8, dy=8)
        if k == 2:
            m.shape("clip 9x16 focus", focus_ring(*box, 10, ring=3, glow=8), ks=layer_ks(o=on_off([(t + 16, None)])))
        x += w + gap
    add_fade(m, OP)
    write(animation(m, PRECOMPS, FPS, "Agentic Layer: Clips in Every Ratio", images=imgs.assets.values()),
          "agentic-clips")


# --------------------------------------------- section: Branded Thumbnails

def build_branded():
    OP = 90
    m, imgs = section_start(OP, "Creative Agent")
    top = section_prompt(m, "Make Space Night thumbnails and add each title logo",
                         "brand_thumbnails", "Picked the strongest scene for each title and placed its logo.")
    tw, th, gap, x0 = 368, 207, 28, 60
    scenes = ["Scene at 01:12:40", "Scene at 00:48:05", "Scene at 00:21:37"]
    for k, (name, title, *_r) in enumerate(LINEUP[:3]):
        x = x0 + k * (tw + gap)
        t = 14 + 4 * k
        media(m, f"thumb {k}", imgs(name), full(name, (0, 0, tw, th)), (x, top, tw, th), 10, t)
        m.shape(f"thumb {k} logo", bf([scrim(x, top, tw, th, 10)] + title_logo(name, x + 18, top + th - 20, 24)),
                ks=layer_ks(o=vis(t + 8)))
        cx = x
        chips = []
        for label in ("16:9", "1:1", "9:16"):
            c, w = chip_check(label, cx, top + th + 50, size=15, h=28)
            chips += c
            cx += w + 8
        appear(m, f"thumb {k} meta", [SEMI.text(title, 20, x + 2, top + th + 32),
                                      REG.text(scenes[k], 16, x + tw, top + th + 32, MUTED, align="right"),
                                      group(chips)], t + 6, dy=8)
        appear(m, f"thumb {k} import", import_button(x, top + th + 94, tw), t + 10, dy=8)
        if k == 0:
            m.shape("thumb 0 focus", focus_ring(x, top, tw, th, 10, ring=3, glow=8),
                    ks=layer_ks(o=on_off([(t + 18, None)])))
    by = top + th + 154
    appear(m, "approve-bar", bf([
        group([rect(1160, 1, 640, by - 14), fill("#ffffff", 8)]),
        SEMI.text("3 titles  ·  3 ratios  ·  9 assets ready", 21, 62, by + 34),
        REG.text("Nothing is published until you approve it.", 17, 62, by + 60, MUTED),
        group([rect(280, 52, 1220 - 140, by + 26, 26), fill(BLUE)]),
        icon(I_CHECK, 22, 1220 - 280 + 34, by + 26),
        SEMI.text("Approve & publish", 20, 1220 - 280 + 54, by + 33),
    ]), 30, dy=8)
    add_fade(m, OP)
    write(animation(m, PRECOMPS, FPS, "Agentic Layer: Branded Thumbnails", images=imgs.assets.values()),
          "agentic-branded-thumbnails")


if __name__ == "__main__":
    build_hero()
    build_hero_v2()
    build_curated_lists()
    build_clips()
    build_branded()
