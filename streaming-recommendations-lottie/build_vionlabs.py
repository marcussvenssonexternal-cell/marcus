"""Builds vionlabs-recommendations.json / .lottie (Vionlabs demo UI version).

Story (30 fps, 13 s, 1920x1080):
  0.0s  Fullscreen: Interstellar has ended and the end credits roll.
  3.3s  The credits shrink into a mini-player (top left) and the Vionlabs home
        screen appears behind it: a hero for the next title plus the
        "Recommended for you" and "Similar titles" rails.
  6.1s  Focus lands on Top Gun: Maverick: the card enlarges, plays a preview and
        shows its genres and mood tags.
  9.7s  Focus moves to The Martian in "Similar titles" and the hero follows.
 12.4s  Fade to black so the loop restarts cleanly.

The movie thumbnails in images/ were taken from the Vionlabs demo recording.
Everything else (UI, credits, icons) is vector.

Run:  python3 build_vionlabs.py   (needs fonttools, uharfbuzz, Pillow and Inter)
"""
import json
import os
import random
import zipfile

from lottie_kit import (Comp, Font, anim, animation, ellipse, fade, fill, gfill, group, icon,
                        image_asset, layer_ks, mask, rect, rrect, stroke)

HERE = os.path.dirname(os.path.abspath(__file__))
FONT_DIR = os.environ.get("INTER_DIR", "/usr/share/fonts/opentype/inter")
LIGHT = Font(f"{FONT_DIR}/Inter-Light.otf")
REG = Font(f"{FONT_DIR}/Inter-Regular.otf")
MED = Font(f"{FONT_DIR}/Inter-Medium.otf")
SEMI = Font(f"{FONT_DIR}/Inter-SemiBold.otf")
BOLD = Font(f"{FONT_DIR}/Inter-Bold.otf")
BLACK = Font(f"{FONT_DIR}/Inter-Black.otf")

W, H, FPS, OP = 1920, 1080, 30, 390

# timeline (frames)
T_CHROME_OUT = (90, 102)
T_SHRINK = (98, 134)
T_PAGE = 100
T_HERO = 120
T_ROWS = (136, 150)
T_SWAP = 290                        # hero switches from Top Gun to The Martian
FOCUS = {(0, 0): (182, 292), (1, 0): (296, None)}   # (row, card): (hover in, hover out)
T_FADE_OUT = (372, 390)

MINI_X, MINI_Y, MINI_W, MINI_H = 80, 118, 480, 270
MINI_C = (MINI_X + MINI_W / 2, MINI_Y + MINI_H / 2)
MINI_SCALE = 100 * MINI_W / W

# Vionlabs demo palette (sampled from the recording)
BG = "#0e1720"
NAV_BG = "#11171f"
PANEL = "#18212b"
BLUE = "#0070f8"
GENRE, GENRE_EDGE = "#1b2d62", "#34508f"
TOPIC = "#1d2e6e"
MOOD = "#e07a6d"
MUTED = "#9aa3b5"
ACCENT = "#5b9dff"

TW, TH = 410, 231                   # rail card size
CARD_X = [80 + 434 * k for k in range(4)]
ROW_TOP = (530, 832)

# Material Design icons (Apache 2.0), 24x24 viewBox
I_PAUSE = "M6 19h4V5H6v14zm8-14v14h4V5h-4z"
I_BACK = "M20 11H7.83l5.59-5.59L12 4l-8 8 8 8 1.41-1.41L7.83 13H20v-2z"
I_VOLUME = ("M3 9v6h4l5 5V4L7 9H3zm13.5 3c0-1.77-1.02-3.29-2.5-4.03v8.05c1.48-.73 2.5-2.25 "
            "2.5-4.02zM14 3.23v2.06c2.89.86 5 3.54 5 6.71s-2.11 5.85-5 6.71v2.06c4.01-.91 "
            "7-4.49 7-8.77s-2.99-7.86-7-8.77z")
I_FULLSCREEN = "M7 14H5v5h5v-2H7v-3zm-2-4h2V7h3V5H5v5zm12 7h-3v2h5v-5h-2v3zM14 5v2h3v3h2V5h-5z"
I_HOME = "M12 5.69l5 4.5V18h-2v-6H9v6H7v-7.81l5-4.5M12 3L2 12h3v8h6v-6h2v6h6v-8h3L12 3z"
I_NEAR_ME = ("M17.27 6.73l-4.24 10.13-1.32-3.42-.32-.83-.82-.32-3.43-1.33 10.13-4.23M21 3L3 "
             "10.53v.98l6.84 2.65L12.48 21h.98L21 3z")
I_SETTINGS = ("M19.14 12.94c.04-.3.06-.61.06-.94 0-.32-.02-.64-.07-.94l2.03-1.58c.18-.14.23-.41"
              ".12-.61l-1.92-3.32c-.12-.22-.37-.29-.59-.22l-2.39.96c-.5-.38-1.03-.7-1.62-.94l-.36"
              "-2.54c-.04-.24-.24-.41-.48-.41h-3.84c-.24 0-.43.17-.47.41l-.36 2.54c-.59.24-1.13.57"
              "-1.62.94l-2.39-.96c-.22-.08-.47 0-.59.22L2.74 8.87c-.12.21-.08.47.12.61l2.03 1.58c"
              "-.05.3-.09.63-.09.94s.02.64.07.94l-2.03 1.58c-.18.14-.23.41-.12.61l1.92 3.32c.12.22"
              ".37.29.59.22l2.39-.96c.5.38 1.03.7 1.62.94l.36 2.54c.05.24.24.41.48.41h3.84c.24 0 "
              ".44-.17.47-.41l.36-2.54c.59-.24 1.13-.56 1.62-.94l2.39.96c.22.08.47 0 .59-.22l1.92"
              "-3.32c.12-.22.07-.47-.12-.61l-2.01-1.58zM12 15.6c-1.98 0-3.6-1.62-3.6-3.6s1.62-3.6 "
              "3.6-3.6 3.6 1.62 3.6 3.6-1.62 3.6-3.6 3.6z")
I_PLAY_OUTLINE = "M10 8.64L15.27 12 10 15.36V8.64M8 5v14l11-7L8 5z"
I_THUMB = ("M1 21h4V9H1v12zm22-11c0-1.1-.9-2-2-2h-6.31l.95-4.57.03-.32c0-.41-.17-.79-.44-1.06"
           "L14.17 1 7.59 7.59C7.22 7.95 7 8.45 7 9v10c0 1.1.9 2 2 2h9c.83 0 1.54-.5 1.84-1.22"
           "l3.02-7.05c.09-.23.14-.47.14-.73v-2z")
I_THUMB_OUTLINE = ("M13.11 5.72l-.57 2.89c-.12.59.04 1.2.42 1.66.38.46.94.73 1.54.73H20v1.08L17.43 "
                   "18H9.34c-.18 0-.34-.16-.34-.34V9.82l4.11-4.1M14 2L7.59 8.41C7.21 8.79 7 9.3 7 "
                   "9.83v7.83C7 18.95 8.05 20 9.34 20h8.1c.71 0 1.36-.37 1.72-.97l2.67-6.15c.11-.25"
                   ".17-.52.17-.8V11c0-1.1-.9-2-2-2h-5.5l.92-4.65c.05-.22.02-.46-.08-.66-.23-.45-.52"
                   "-.86-.88-1.22L14 2zM4 9H2v11h2c.55 0 1-.45 1-1v-9c0-.55-.45-1-1-1z")
I_BOOKMARK = ("M17 3H7c-1.1 0-1.99.9-1.99 2L5 21l7-3 7 3V5c0-1.1-.9-2-2-2zm0 15l-5-2.18L7 18V5h10"
              "v13z")
I_CHEV_L = "M15.41 7.41L14 6l-6 6 6 6 1.41-1.41L10.83 12z"
I_CHEV_R = "M10 6L8.59 7.41 13.17 12l-4.58 4.59L10 18l6-6z"

CREW = [("Directed by", "Christopher Nolan"),
        ("Written by", "Jonathan Nolan & Christopher Nolan"),
        ("Produced by", "Emma Thomas"), ("", "Christopher Nolan"), ("", "Lynda Obst"),
        ("Director of Photography", "Hoyte van Hoytema"),
        ("Production Designer", "Nathan Crowley"),
        ("Edited by", "Lee Smith"),
        ("Music by", "Hans Zimmer")]
CAST = [("Cooper", "Matthew McConaughey"), ("Brand", "Anne Hathaway"),
        ("Murph", "Jessica Chastain"), ("Old Murph", "Ellen Burstyn"),
        ("Professor Brand", "Michael Caine"), ("Tom", "Casey Affleck"),
        ("Young Murph", "Mackenzie Foy"), ("Romilly", "David Gyasi"), ("Doyle", "Wes Bentley"),
        ("Getty", "Topher Grace"), ("Donald", "John Lithgow"), ("Mann", "Matt Damon"),
        ("TARS (voice)", "Bill Irwin")]

TITLES = {
    "topgun": dict(
        label="RECOMMENDED FOR YOU", title="Top Gun: Maverick",
        genres=["Action", "Adventure", "Drama"], card_genres="action • adventure • drama",
        desc=["After more than thirty years of service, Maverick returns",
              "to train an elite group of Top Gun graduates for a",
              "high-stakes mission that demands the ultimate sacrifice."],
        topics=["fighter jets", "aviation", "mentorship", "rivalry"],
        moods=["high octane", "intense", "inspiring"]),
    "martian": dict(
        label="SIMILAR TO INTERSTELLAR", title="The Martian",
        genres=["Science Fiction", "Adventure", "Drama"],
        card_genres="science fiction • adventure • drama",
        desc=["Stranded on Mars after a storm forces his crew to leave,",
              "astronaut Mark Watney must rely on his ingenuity to",
              "survive and signal to Earth that he is still alive."],
        topics=["mars", "space", "survival", "ingenuity"],
        moods=["suspenseful", "inspiring", "high-stakes"]),
}
ROWS = [("Recommended for you", None, ["topgun", "nohardfeelings", "spiderverse", "oppenheimer"]),
        ("Similar titles", "Because you watched Interstellar",
         ["martian", "arrival", "2001", "sunshine"])]


def bf(items):
    """Author back-to-front; Lottie draws the first shape on top."""
    return list(reversed(items))


def pill(text, x, y, size=15, h=28, color=TOPIC, edge=None, pad=12, align="left"):
    w = MED.width(text, size) + 2 * pad
    if align == "right":
        x -= w
    bg = [rect(w, h, x + w / 2, y + h / 2, h / 2), fill(color)] + ([stroke(edge, 1.2)] if edge else [])
    label = MED.text(text, size, x + w / 2, y + h / 2 + size * 0.36, align="center")
    return bf([group(bg), label]), w


def pill_row(texts, x, y, gap=8, align="left", **kw):
    items = []
    for t in (reversed(texts) if align == "right" else texts):
        g, w = pill(t, x, y, align=align, **kw)
        items += g
        x += -(w + gap) if align == "right" else w + gap
    return items


def flip(g, cx, cy):
    return group([g], p=(cx, cy), a=(cx, cy), r=180)


# ------------------------------------------------- scene: Interstellar credits

def build_credits():
    c = Comp(W, H, OP, "comp_credits")
    c.shape("black", [group([rect(W, H, 960, 540), fill("#000000")])])
    rng = random.Random(4)
    stars = [ellipse(s, s, rng.uniform(0, W), rng.uniform(-100, 1500))
             for s in [rng.choice((1.5, 2, 2, 2.5, 3)) for _ in range(110)]]
    c.shape("stars", [group(stars + [fill("#ffffff", 45)])],
            ks=layer_ks(p=anim([(0, [0, 0], "linear"), (OP, [0, -420])])))
    items = [LIGHT.text("INTERSTELLAR", 92, 960, 500, align="center", tracking=0.32)]
    y = 660
    for role, name in CREW:
        if role:
            items.append(MED.text(role.upper(), 19, 930, y, MUTED, align="right", tracking=0.12, nd=0))
        items.append(REG.text(name, 32, 990, y, nd=0))
        y += 52
    y += 70
    items.append(SEMI.text("CAST", 21, 960, y, MUTED, align="center", tracking=0.3, nd=0))
    y += 72
    for role, name in CAST:
        items.append(REG.text(role, 26, 930, y, MUTED, align="right", nd=0))
        items.append(REG.text(name, 32, 990, y, nd=0))
        y += 50
    c.shape("credits", items, ks=layer_ks(p=anim([(0, [0, 0], "linear"), (OP, [0, -1400])])))
    return c


# ---------------------------------------------------------- rail cards

def build_card(name, img, info=None, hover=None):
    """A 410x231 card; with `hover` it plays a Ken Burns 'preview' and shows its tags."""
    c = Comp(TW, TH, OP, f"comp_card_{name}")
    centre = [TW / 2, TH / 2]
    ks = None
    if hover:
        t_in, t_out = hover
        end = t_out or OP
        zoom = 100 + 11 * (end - t_in) / 110
        s = [(t_in, [100, 100], "linear"), (end, [zoom, zoom])]
        p = [(t_in, centre, "linear"), (end, [centre[0] - 10, centre[1] - 4])]
        if t_out:
            s.append((t_out + 10, [100, 100]))
            p.append((t_out + 10, centre))
        ks = layer_ks(p=anim(p), a=centre, s=anim(s))
    c.image("thumb", img, ks=ks)
    if not hover:
        return c
    t_in, t_out = hover
    ov = [(t_in + 8, [0]), (t_in + 18, [100])] + ([(t_out - 4, [100]), (t_out + 4, [0])] if t_out else [])
    c.shape("hover-shade", [group([rect(TW, TH, TW / 2, TH / 2), gfill(
        [(0, "#000000", 0), (0.45, "#000000", 0.15), (1, "#000000", 0.88)], (0, 60), (0, TH))])],
        ks=layer_ks(o=anim(ov)))
    c.shape("hover-info", [BOLD.text(info["title"], 21, 16, 166),
                           REG.text(info["card_genres"], 14, 16, 188, o=85)]
            + pill_row(info["moods"], 16, 198, gap=6, size=12, h=20, color=MOOD, pad=8),
            ks=layer_ks(o=anim(ov)))
    end = t_out or OP
    c.shape("hover-progress", bf([
        group([rect(TW, 3, TW / 2, TH - 1.5), fill("#ffffff", 25)]),
        group([rect(anim([(t_in + 10, [0, 3], "linear"), (end, [TW * 0.3, 3])]), 0,
                    anim([(t_in + 10, [0, TH - 1.5], "linear"), (end, [TW * 0.15, TH - 1.5])])),
               fill(BLUE)]),
    ]), ks=layer_ks(o=anim(ov)))
    return c


# ------------------------------------------------------------- main comp

def logo(x, base, size):
    w_vi = BLACK.width("VI", size, 0.02) + size * 0.05
    d = size * 0.76
    ox, oy = x + w_vi + d / 2, base - size * 0.364
    return [BLACK.text("VI", size, x, base, tracking=0.02),
            group([ellipse(d, d, ox, oy), fill("#ffffff")]),
            group([ellipse(d * 0.36, d * 0.36, ox - d * 0.2, oy - d * 0.2), fill(NAV_BG)]),
            BLACK.text("NLABS", size, ox + d / 2 + size * 0.06, base, tracking=0.02)]


def nav_bar():
    items = [group([rect(W, 76, 960, 38), fill(NAV_BG, 88)])] + logo(60, 50, 30)
    x = 262
    for ic, label in ((I_HOME, "Home"), (I_NEAR_ME, "Mood Walk"), (None, "My Content")):
        if ic:
            items.append(icon(ic, 22, x + 11, 38, o=95))
            x += 30
        items.append(MED.text(label, 18, x, 45, o=100 if label == "Home" else 85))
        x += MED.width(label, 18) + 30
    items += [group([ellipse(34, 34, 1712, 38), fill("#1e6fff")]),
              icon(I_SETTINGS, 20, 1768, 38, o=90), MED.text("Settings", 18, 1786, 45, o=90)]
    return items


def hero_layers(m, d, t_in, t_out):
    def ks(delay):
        t = t_in + delay
        p = [(t, [0, 22], "out"), (t + 20, [0, 0])]
        o = [(t, [0]), (t + 16, [100])]
        if t_out:
            p += [(t_out, [0, 0], "in"), (t_out + 10, [0, -14])]
            o += [(t_out, [100]), (t_out + 10, [0])]
        return layer_ks(p=anim(p), o=anim(o))

    op = t_out + 12 if t_out else None
    key = d["title"]
    m.shape(f"{key}: label", [SEMI.text(d["label"], 15, 632, 170, ACCENT, tracking=0.14)],
            ip=t_in, op=op, ks=ks(0))
    m.shape(f"{key}: title", [BOLD.text(d["title"], 60, 629, 234)], ip=t_in, op=op, ks=ks(3))
    m.shape(f"{key}: genres", pill_row(d["genres"], 632, 252, h=30, color=GENRE, edge=GENRE_EDGE),
            ip=t_in, op=op, ks=ks(6))
    m.shape(f"{key}: description",
            [REG.text(line, 19, 632, 318 + 26 * k, o=88) for k, line in enumerate(d["desc"])],
            ip=t_in, op=op, ks=ks(9))
    m.shape(f"{key}: tags", pill_row(d["topics"], 1792, 392, align="right")
            + pill_row(d["moods"], 1792, 430, align="right", color=MOOD), ip=t_in, op=op, ks=ks(14))


def build_main(credits, cards, imgs):
    m = Comp(W, H, OP, "main")
    s0, s1 = T_SHRINK

    # page + hero backdrop (blurred still of the focused title)
    m.shape("page", [group([rect(W, H, 960, 540), fill(BG)])], ip=s0 - 4)
    zoom = anim([(T_PAGE, [205, 205], "linear"), (OP, [216, 216])])
    m.image("backdrop: Top Gun", imgs["topgun_backdrop"], ip=T_PAGE, op=T_SWAP + 24,
            ks=layer_ks(p=(960, 300), a=(480, 270), s=zoom, o=fade(T_PAGE, T_PAGE + 24)))
    m.image("backdrop: The Martian", imgs["martian_backdrop"], ip=T_SWAP,
            ks=layer_ks(p=(960, 300), a=(480, 270), s=zoom, o=fade(T_SWAP, T_SWAP + 22)))
    m.shape("backdrop-scrim", bf([
        group([rect(W, H, 960, 540), fill("#000000", 30)]),
        group([rect(W, 700, 960, 350), gfill([(0, "#000000", 0.92), (0.45, "#000000", 0.55),
                                               (1, "#000000", 0.12)], (0, 0), (W, 0))]),
        group([rect(W, 360, 960, 470), gfill([(0, BG, 0), (1, BG, 1)], (0, 330), (0, 650))]),
        group([rect(W, 440, 960, 860), fill(BG)]),
    ]), ip=T_PAGE)
    m.shape("nav", bf(nav_bar()), ip=T_PAGE, ks=layer_ks(o=fade(T_PAGE, T_PAGE + 16)))

    # hero copy: Top Gun first, then The Martian when focus moves
    hero_layers(m, TITLES["topgun"], T_HERO, T_SWAP)
    hero_layers(m, TITLES["martian"], T_SWAP + 8, None)
    bt = T_HERO + 12
    m.shape("hero-buttons", bf([
        group([rect(170, 48, 717, 420, 8), fill(BLUE)]),
        icon(I_PLAY_OUTLINE, 22, 664, 420),
        MED.text("Watch Now", 18, 682, 426),
        icon(I_THUMB_OUTLINE, 24, 840, 420, o=90),
        icon(I_BOOKMARK, 24, 884, 420, o=90),
    ]), ip=T_HERO, ks=layer_ks(p=anim([(bt, [0, 22], "out"), (bt + 20, [0, 0])]),
                               o=fade(bt, bt + 16)))

    # rails
    for r, (label, sub, names) in enumerate(ROWS):
        top, t0 = ROW_TOP[r], T_ROWS[r]
        head = [REG.text(label, 25, 84, top - 28)]
        if sub:
            head.append(REG.text(sub, 18, 84 + REG.width(label, 25) + 16, top - 28, MUTED))
        for cx, ic in ((1726, I_CHEV_L), (1772, I_CHEV_R)):
            head += bf([group([ellipse(40, 40, cx, top - 36), fill(PANEL)]), icon(ic, 22, cx, top - 36)])
        m.shape(f"rail {r}: header", head, ip=T_PAGE,
                ks=layer_ks(p=anim([(t0, [0, 24], "out"), (t0 + 20, [0, 0])]), o=fade(t0, t0 + 16)))
        for k in (3, 2, 1, 0):  # first card last, so it sits on top when it grows
            t = t0 + 4 + 4 * k
            centre = [CARD_X[k] + TW / 2, top + TH / 2]
            hover = FOCUS.get((r, k))
            scale = (100, 100)
            if hover:
                t_in, t_out = hover
                sk = [(t_in, [100, 100], "out"), (t_in + 12, [110, 110])]
                if t_out:
                    sk += [(t_out, [110, 110], "io"), (t_out + 10, [100, 100])]
                scale = anim(sk)
                glow = [(t_in, [0]), (t_in + 12, [100])] + ([(t_out, [100]), (t_out + 10, [0])]
                                                           if t_out else [])
            card_ks = layer_ks(p=anim([(t, [centre[0], centre[1] + 40], "out"), (t + 22, centre)]),
                               a=(TW / 2, TH / 2), o=fade(t, t + 16), s=scale)
            if hover:
                shadow = m.null(f"rail {r}: card {k} anchor", ip=T_PAGE, ks=card_ks)
                m.shape(f"rail {r}: card {k} shadow", [group([rect(TW + 12, TH + 12, TW / 2, TH / 2 + 8, 14),
                                                              fill("#000000", 35)])],
                        ip=T_PAGE, parent=shadow, ks=layer_ks(o=anim(glow)))
            card = m.precomp(f"rail {r}: {names[k]}", cards[names[k]], ip=T_PAGE, ks=card_ks,
                             masks=[mask(rrect(0, 0, TW, TH, 10))])
            if hover:
                m.shape(f"rail {r}: card {k} focus", [group([rect(TW + 8, TH + 8, TW / 2, TH / 2, 13),
                                                             stroke("#ffffff", 3)])],
                        ip=T_PAGE, parent=card, ks=layer_ks(o=anim(glow)))

    # mini-player
    mx, my = MINI_C
    m.shape("mini-caption", bf([
        group([rect(MINI_W, 84, mx, MINI_Y + MINI_H + 32, 10), fill(PANEL)]),
        group([rect(MINI_W, 3, mx, MINI_Y + MINI_H + 1.5), fill("#ffffff", 15)]),
        group([rect(anim([(s1, [MINI_W * 0.985, 3], "linear"), (OP, [MINI_W, 3])]), 0,
                    anim([(s1, [MINI_X + MINI_W * 0.4925, MINI_Y + MINI_H + 1.5], "linear"),
                          (OP, [mx, MINI_Y + MINI_H + 1.5])])), fill(BLUE)]),
        SEMI.text("Interstellar", 19, 100, 420),
        REG.text("Finished  ·  Did you enjoy it?", 15, 100, 444, MUTED),
        group([ellipse(38, 38, 486, 425), stroke("#ffffff", 1.5, 45)]),
        icon(I_THUMB, 17, 486, 425),
        group([ellipse(38, 38, 532, 425), stroke("#ffffff", 1.5, 45)]),
        flip(icon(I_THUMB, 17, 532, 426), 532, 426),
    ]), ip=s1 - 6, ks=layer_ks(p=anim([(s1 - 4, [0, -50], "out"), (s1 + 16, [0, 0])]),
                               o=fade(s1 - 4, s1 + 12)))

    size = anim([(s0, [W, H], "smooth"), (s1, [MINI_W, MINI_H])])
    centre = anim([(s0, [960, 540], "smooth"), (s1, list(MINI_C))])
    radius = anim([(s0, [0], "smooth"), (s1, [10])])
    m.shape("mini-shadow", [group([rect(anim([(s0, [W + 20, H + 20], "smooth"),
                                              (s1, [MINI_W + 20, MINI_H + 20])]), 0,
                                        anim([(s0, [960, 548], "smooth"), (s1, [mx, my + 8])]), 0,
                                        14), fill("#000000", 45)])],
            ip=s0, ks=layer_ks(o=fade(s0 + 6, s1)))
    m.precomp("video", credits, masks=[mask(anim([(s0, rrect(0, 0, W, H, 0), "smooth"),
                                                   (s1, rrect(0, 0, W, H, 10 * W / MINI_W))]))],
              ks=layer_ks(p=centre, a=(960, 540),
                          s=anim([(s0, [100, 100], "smooth"), (s1, [MINI_SCALE, MINI_SCALE])])))
    m.shape("mini-border", [group([rect(size, 0, centre, 0, radius), stroke("#ffffff", 1.5, 22)])],
            ip=s0, ks=layer_ks(o=fade(s0, s0 + 10)))

    # fullscreen player controls over the credits
    track_x0, track_w, cy = 136, 1504, 1026

    def remaining(k, t_in, t_out):
        o = anim([(0, [0], "hold"), (t_in, [100], "hold"), (t_out, [0])]) if t_in else \
            anim([(0, [100], "hold"), (t_out, [0])])
        return group([MED.text(f"-00:0{k}", 21, 1662, 1034)], o=o)

    m.shape("player-controls", bf([
        group([rect(W, 180, 960, 90), gfill([(0, "#000000", 0.7), (1, "#000000", 0)],
                                             (0, 0), (0, 180))]),
        icon(I_BACK, 32, 68, 64),
        SEMI.text("Interstellar", 26, 106, 73),
        group([rect(W, 220, 960, 970), gfill([(0, "#000000", 0), (1, "#000000", 0.8)],
                                              (0, 860), (0, 1080))]),
        group([ellipse(48, 48, 80, cy), stroke("#ffffff", 2.5)]),
        icon(I_PAUSE, 24, 80, cy),
        group([rect(track_w, 5, track_x0 + track_w / 2, cy, 2.5), fill("#ffffff", 30)]),
        group([rect(anim([(0, [track_w * 0.982, 5], "linear"), (s0, [track_w, 5])]), 0,
                    anim([(0, [track_x0 + track_w * 0.491, cy], "linear"),
                          (s0, [track_x0 + track_w / 2, cy])]), 0, 2.5), fill(BLUE)]),
        group([ellipse(18, 18, 0, 0), fill("#ffffff")],
              p=anim([(0, [track_x0 + track_w * 0.982, cy], "linear"), (s0, [track_x0 + track_w, cy])])),
        remaining(3, 0, 30), remaining(2, 30, 60), remaining(1, 60, 90), remaining(0, 90, 200),
        icon(I_VOLUME, 34, 1772, cy),
        icon(I_FULLSCREEN, 34, 1846, cy),
    ]), op=T_CHROME_OUT[1] + 2, ks=layer_ks(o=fade(*T_CHROME_OUT, 100, 0)))

    m.shape("fade", [group([rect(W, H, 960, 540), fill("#000000")])], ks=layer_ks(
        o=anim([(0, [100]), (10, [0]), (T_FADE_OUT[0], [0]), (T_FADE_OUT[1], [100])])))
    return m


def main():
    img_dir = os.path.join(HERE, "images")
    names = [n for _, _, row in ROWS for n in row] + ["topgun_backdrop", "martian_backdrop"]
    imgs = {n: image_asset(os.path.join(img_dir, f"{n}.jpg"), f"img_{n}") for n in names}
    hovers = {ROWS[r][2][k]: v for (r, k), v in FOCUS.items()}
    cards = {n: build_card(n, imgs[n], TITLES.get(n), hovers.get(n)) for _, _, row in ROWS for n in row}
    credits = build_credits()
    main_comp = build_main(credits, cards, imgs)
    data = animation(main_comp, [credits] + list(cards.values()), FPS,
                     "Vionlabs recommendations", images=imgs.values())
    text = json.dumps(data, separators=(",", ":"))
    out_json = os.path.join(HERE, "vionlabs-recommendations.json")
    with open(out_json, "w") as f:
        f.write(text)
    manifest = {"version": "1.0", "generator": "build_vionlabs.py", "author": "", "revision": 1,
                "animations": [{"id": "vionlabs-recommendations", "speed": 1, "loop": True,
                                "autoplay": True, "direction": 1, "playMode": "normal"}]}
    with zipfile.ZipFile(os.path.join(HERE, "vionlabs-recommendations.lottie"), "w",
                         zipfile.ZIP_DEFLATED) as z:
        z.writestr("manifest.json", json.dumps(manifest))
        z.writestr("animations/vionlabs-recommendations.json", text)
    print(f"wrote {out_json} ({len(text) / 1024:.0f} KB)")


if __name__ == "__main__":
    main()
