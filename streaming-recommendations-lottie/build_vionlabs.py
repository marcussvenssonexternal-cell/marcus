"""Builds vionlabs-recommendations.json / .lottie (Vionlabs demo UI version).

Story (30 fps, 16 s, 1920x1080):
  0.0s  Fullscreen: Interstellar has ended and the end credits roll.
  3.3s  The credits shrink into a mini-player (top left) and the next title,
        Top Gun: Maverick, fills the screen behind it: title, mood tags,
        "Play now" / "Playing preview in" and three cards (Recommended for you,
        Similar titles, Since you watched Interstellar).
  5.3s  "Playing preview in 3-2-1" countdown.
  8.3s  The preview plays full screen.
 11.0s  The page scrolls down to the "Recommended for you" and
        "Similar titles" rails.
 13.1s  Focus lands on The Martian: the card enlarges, plays a preview and shows
        its genres and mood tags.
 15.4s  Fade to black so the loop restarts cleanly.

The movie images in images/ were taken from the Vionlabs demo recording.
Everything else (UI, credits, icons) is vector.

Run:  python3 build_vionlabs.py   (needs fonttools, uharfbuzz, Pillow and Inter)
"""
import json
import os
import random
import zipfile

from lottie_kit import (Comp, Font, anim, animation, ellipse, fade, fill, gfill, group, icon,
                        image_asset, layer_ks, mask, rect, rrect, stroke, trim)

HERE = os.path.dirname(os.path.abspath(__file__))
FONT_DIR = os.environ.get("INTER_DIR", "/usr/share/fonts/opentype/inter")
LIGHT = Font(f"{FONT_DIR}/Inter-Light.otf")
REG = Font(f"{FONT_DIR}/Inter-Regular.otf")
MED = Font(f"{FONT_DIR}/Inter-Medium.otf")
SEMI = Font(f"{FONT_DIR}/Inter-SemiBold.otf")
BOLD = Font(f"{FONT_DIR}/Inter-Bold.otf")
BLACK = Font(f"{FONT_DIR}/Inter-Black.otf")

W, H, FPS, OP = 1920, 1080, 30, 480

# timeline (frames)
T_CHROME_OUT = (90, 102)
T_SHRINK = (98, 134)
T_PAGE = 100
T_UI = 118
T_COUNT = (160, 250)
T_PREVIEW = 250
T_SCROLL = (330, 380)
SCROLL = 740                        # how far the page scrolls (px)
T_HOVER = 394                       # The Martian card in "Similar titles"
T_FADE_OUT = (462, 480)

MINI_X, MINI_Y, MINI_W, MINI_H = 92, 150, 480, 270
MINI_C = (MINI_X + MINI_W / 2, MINI_Y + MINI_H / 2)
MINI_SCALE = 100 * MINI_W / W

# Vionlabs demo palette (sampled from the recording)
BG = "#0e1720"
NAV_BG = "#11171f"
PANEL = "#18212b"
BLUE = "#0070f8"
FOCUS = "#3d9bff"
GENRE, GENRE_EDGE = "#1b2d62", "#34508f"
MOOD = "#e07a6d"
MUTED = "#9aa3b5"

TW, TH = 410, 231                   # card image size
HERO_SCALE = 100 * 288 / TW         # hero cards are 288 px wide
HERO_CARD_X, HERO_CARD_TOP = [949, 1251, 1553], 836
CARD_X = [80 + 434 * k for k in range(4)]
ROW_TOP = (1168, 1474)              # page coordinates (below the hero)

# Material Design icons (Apache 2.0), 24x24 viewBox
I_PLAY = "M8 5v14l11-7z"
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
I_THUMB = ("M1 21h4V9H1v12zm22-11c0-1.1-.9-2-2-2h-6.31l.95-4.57.03-.32c0-.41-.17-.79-.44-1.06"
           "L14.17 1 7.59 7.59C7.22 7.95 7 8.45 7 9v10c0 1.1.9 2 2 2h9c.83 0 1.54-.5 1.84-1.22"
           "l3.02-7.05c.09-.23.14-.47.14-.73v-2z")
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

HERO = dict(title="Top Gun: Maverick", meta="2022  ·  2h 11m  ·  12+",
            genres=["Action", "Adventure", "Drama"], moods=["high octane", "intense", "inspiring"],
            desc=["After more than thirty years of service, Maverick returns to",
                  "train an elite group of Top Gun graduates for a deadly mission."])
HERO_CARDS = [("topgun", ["Recommended for you"]), ("martian", ["Similar titles"]),
              ("2001", ["Since you watched", "Interstellar"])]
ROWS = [("Recommended for you", None, ["topgun", "nohardfeelings", "spiderverse", "oppenheimer"]),
        ("Similar titles", "Because you watched Interstellar",
         ["martian", "arrival", "2001", "sunshine"])]
MARTIAN = dict(title="The Martian", card_genres="science fiction • adventure • drama",
               moods=["suspenseful", "inspiring", "high-stakes"])


def bf(items):
    """Author back-to-front; Lottie draws the first shape on top."""
    return list(reversed(items))


def pill(text, x, y, size=15, h=28, color=GENRE, edge=None, pad=12, align="left"):
    w = MED.width(text, size) + 2 * pad
    if align == "right":
        x -= w
    bg = [rect(w, h, x + w / 2, y + h / 2, h / 2), fill(color)] + ([stroke(edge, 1.2)] if edge else [])
    label = MED.text(text, size, x + w / 2, y + h / 2 + size * 0.36, align="center")
    return bf([group(bg), label]), w


def pill_row(texts, x, y, gap=8, **kw):
    items = []
    for t in texts:
        g, w = pill(t, x, y, **kw)
        items += g
        x += w + gap
    return items, x


def flip(g, cx, cy):
    return group([g], p=(cx, cy), a=(cx, cy), r=180)


def in_out(t, fade_in=16, out=None):
    """Opacity: fade in at t, optionally fade out as the page scrolls away."""
    keys = [(t, [0]), (t + fade_in, [100])]
    if out:
        keys += [(out[0], [100]), (out[1], [0])]
    return anim(keys)


SCROLL_OUT = (T_SCROLL[0], T_SCROLL[0] + 24)   # hero UI fades as it scrolls under the nav


# ------------------------------------------------- scene: Interstellar credits

def build_credits():
    c = Comp(W, H, OP, "comp_credits")
    c.shape("black", [group([rect(W, H, 960, 540), fill("#000000")])])
    rng = random.Random(4)
    stars = [ellipse(s, s, rng.uniform(0, W), rng.uniform(-100, 1700))
             for s in [rng.choice((1.5, 2, 2, 2.5, 3)) for _ in range(120)]]
    c.shape("stars", [group(stars + [fill("#ffffff", 45)])],
            ks=layer_ks(p=anim([(0, [0, 0], "linear"), (OP, [0, -520])])))
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
    c.shape("credits", items, ks=layer_ks(p=anim([(0, [0, 0], "linear"), (OP, [0, -1720])])))
    return c


# ---------------------------------------------------------- hovered card

def build_hover_card(name, img, info, t_in):
    """A 410x231 card that plays a Ken Burns 'preview' and shows its tags from t_in."""
    c = Comp(TW, TH, OP, f"comp_card_{name}")
    centre = [TW / 2, TH / 2]
    zoom = 100 + 11 * (OP - t_in) / 110
    c.image("thumb", img, ks=layer_ks(
        p=anim([(t_in, centre, "linear"), (OP, [centre[0] - 10, centre[1] - 4])]), a=centre,
        s=anim([(t_in, [100, 100], "linear"), (OP, [zoom, zoom])])))
    ov = in_out(t_in + 8, 10)
    c.shape("hover-shade", [group([rect(TW, TH, TW / 2, TH / 2), gfill(
        [(0, "#000000", 0), (0.45, "#000000", 0.15), (1, "#000000", 0.88)], (0, 60), (0, TH))])],
        ks=layer_ks(o=ov))
    pills, _ = pill_row(info["moods"], 16, 198, gap=6, size=12, h=20, color=MOOD, pad=8)
    c.shape("hover-info", [BOLD.text(info["title"], 21, 16, 166),
                           REG.text(info["card_genres"], 14, 16, 188, o=85)] + pills,
            ks=layer_ks(o=ov))
    c.shape("hover-progress", bf([
        group([rect(TW, 3, TW / 2, TH - 1.5), fill("#ffffff", 25)]),
        group([rect(anim([(t_in + 10, [0, 3], "linear"), (OP, [TW * 0.25, 3])]), 0,
                    anim([(t_in + 10, [0, TH - 1.5], "linear"), (OP, [TW * 0.125, TH - 1.5])])),
               fill(BLUE)]),
    ]), ks=layer_ks(o=ov))
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


def nav_items():
    items = logo(60, 50, 30)
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


def card_image(m, name, img, centre, scale, radius, ks_extra, page, ip=T_PAGE):
    """A rounded thumbnail as an image layer (no precomp needed)."""
    ks = layer_ks(a=(TW / 2, TH / 2), s=scale, **ks_extra)
    return m.image(name, img, ip=ip, parent=page, ks=ks,
                   masks=[mask(rrect(0, 0, TW, TH, radius))])


def build_main(credits, martian_card, imgs):
    m = Comp(W, H, OP, "main")
    s0, s1 = T_SHRINK
    p0 = T_PREVIEW
    scroll = [(T_SCROLL[0], [0, 0], "io"), (T_SCROLL[1], [0, -SCROLL])]

    m.shape("page-bg", [group([rect(W, H, 960, 540), fill(BG)])], ip=s0 - 4)

    # full-screen hero preview (scrolls at half speed for parallax)
    parallax = m.null("parallax", ks=layer_ks(p=anim([(T_SCROLL[0], [0, 0], "io"),
                                                       (T_SCROLL[1], [0, -SCROLL / 2])])))
    m.image("hero: Top Gun preview", imgs["topgun_hero"], ip=T_PAGE, parent=parallax, ks=layer_ks(
        p=anim([(p0, [960, 540], "linear"), (OP, [930, 528])]), a=(480, 270),
        s=anim([(s0, [206, 206], "out"), (150, [200, 200]), (p0, [200, 200], "linear"),
                (OP, [216, 216])]), o=fade(T_PAGE, T_PAGE + 12)))
    m.shape("hero-scrims", bf([
        group([rect(W, H, 960, 540), fill("#000000")], o=anim([(p0, [30]), (p0 + 14, [0])])),
        group([rect(W, H, 960, 540), gfill([(0, "#000000", 0.85), (0.4, "#000000", 0.5),
                                             (0.75, "#000000", 0)], (0, 0), (W, 0))]),
        group([rect(W, 562, 960, 800), gfill([(0, BG, 0), (0.55, BG, 0.55), (1, BG, 1)],
                                              (0, 520), (0, 1080))]),
        group([rect(W, 1204, 960, 1678), fill(BG)]),
    ]), ip=T_PAGE, parent=parallax)

    page = m.null("page", ks=layer_ks(p=anim(scroll)))

    # rails below the hero (come into view when the page scrolls)
    for r, (label, sub, names) in enumerate(ROWS):
        top = ROW_TOP[r]
        t0 = T_SCROLL[0] + 8 + 12 * r
        head = [REG.text(label, 25, 84, top - 28)]
        if sub:
            head.append(REG.text(sub, 18, 84 + REG.width(label, 25) + 16, top - 28, MUTED))
        for cx, ic in ((1726, I_CHEV_L), (1772, I_CHEV_R)):
            head += bf([group([ellipse(40, 40, cx, top - 36), fill(PANEL)]), icon(ic, 22, cx, top - 36)])
        m.shape(f"rail {r}: header", head, ip=T_SCROLL[0], parent=page, ks=layer_ks(
            p=anim([(t0, [0, 30], "out"), (t0 + 22, [0, 0])]), o=in_out(t0)))
        for k in (3, 2, 1, 0):  # first card last, so it sits on top when it grows
            t = t0 + 3 * k
            centre = [CARD_X[k] + TW / 2, top + TH / 2]
            pos = anim([(t, [centre[0], centre[1] + 30], "out"), (t + 22, centre)])
            if (r, k) != (1, 0):
                card_image(m, f"rail {r}: {names[k]}", imgs[names[k]], centre, (100, 100), 10,
                           dict(p=pos, o=in_out(t)), page, ip=T_SCROLL[0])
                continue
            hover = anim([(T_HOVER, [100, 100], "out"), (T_HOVER + 12, [110, 110])])
            glow = in_out(T_HOVER, 12)
            ks = layer_ks(p=pos, a=(TW / 2, TH / 2), o=in_out(t), s=hover)
            anchor = m.null("rail 1: martian anchor", ip=T_SCROLL[0], parent=page, ks=ks)
            m.shape("rail 1: martian shadow", [group([rect(TW + 12, TH + 12, TW / 2, TH / 2 + 8, 14),
                                                      fill("#000000", 40)])],
                    ip=T_SCROLL[0], parent=anchor, ks=layer_ks(o=glow))
            card = m.precomp("rail 1: martian", martian_card, ip=T_SCROLL[0], parent=page, ks=ks,
                             masks=[mask(rrect(0, 0, TW, TH, 10))])
            m.shape("rail 1: martian focus", [group([rect(TW + 10, TH + 10, TW / 2, TH / 2, 14),
                                                     stroke(FOCUS, 4)])],
                    ip=T_SCROLL[0], parent=card, ks=layer_ks(o=glow))

    # hero copy, bottom left
    def enter(t, dy=24):
        return layer_ks(p=anim([(t, [0, dy], "out"), (t + 22, [0, 0])]), o=in_out(t, out=SCROLL_OUT))

    m.shape("hero: title", [BOLD.text(HERO["title"], 84, 108, 742)], ip=T_PAGE, parent=page,
            ks=enter(T_UI))
    m.shape("hero: meta", [MED.text(HERO["meta"], 23, 112, 784, o=88)], ip=T_PAGE, parent=page,
            ks=enter(T_UI + 4))
    genres, x = pill_row(HERO["genres"], 112, 802, h=30, color=GENRE, edge=GENRE_EDGE)
    moods, _ = pill_row(HERO["moods"], x + 8, 802, h=30, color=MOOD)
    m.shape("hero: tags", genres + moods, ip=T_PAGE, parent=page, ks=enter(T_UI + 8))
    m.shape("hero: description", [REG.text(line, 21, 112, 872 + 28 * k, o=88)
                                  for k, line in enumerate(HERO["desc"])],
            ip=T_PAGE, parent=page, ks=enter(T_UI + 12))

    bt = T_UI + 16
    buttons = m.shape("hero: buttons", bf([
        group([rect(210, 58, 213, 957, 8), rect(310, 58, 485, 957, 8), fill(BLUE)]),
        MED.text("Play now", 23, 146, 965),
        icon(I_PLAY, 28, 284, 957),
    ]), ip=T_PAGE, parent=page, ks=enter(bt))
    vis = anim([(bt, [0]), (bt + 16, [100]), (p0, [100]), (p0 + 8, [0])])
    m.shape("countdown-sweep", [group([rect(anim([(T_COUNT[0], [0, 58], "linear"),
                                                  (T_COUNT[1], [310, 58])]), 0,
                                            anim([(T_COUNT[0], [330, 957], "linear"),
                                                  (T_COUNT[1], [485, 957])]), 0, 8),
                                       fill("#ffffff", 16)])],
            ip=T_PAGE, op=p0 + 10, parent=buttons, ks=layer_ks(o=vis))
    m.shape("countdown-label", [MED.text("Playing preview in", 23, 362, 965)],
            ip=T_PAGE, op=p0 + 10, parent=buttons, ks=layer_ks(o=vis))
    m.shape("countdown-ring", bf([
        group([ellipse(30, 30, 602, 957), stroke("#ffffff", 2, 35)]),
        group([ellipse(30, 30, 602, 957), stroke("#ffffff", 2.4),
               trim(e=anim([(T_COUNT[0], [100], "linear"), (T_COUNT[1], [0])]))]),
    ]), ip=T_PAGE, op=p0 + 10, parent=buttons, ks=layer_ks(o=vis))
    cuts = [T_PAGE, T_COUNT[0] + 30, T_COUNT[0] + 60, p0 - 2, p0 + 10]
    for k, n in enumerate("3210"):
        t_in, t_out = cuts[k], cuts[k + 1]
        m.shape(f"countdown-{n}", [SEMI.text(n, 17, 602, 963, align="center")], ip=t_in, op=t_out,
                parent=buttons, ks=layer_ks(p=(602, 957), a=(602, 957), o=vis if k in (0, 3) else 100,
                                            s=anim([(t_in, [60, 60], "out"), (t_in + 7, [100, 100])])
                                            if k else (100, 100)))
    rng = random.Random(5)
    bars = []
    for x in (595, 602, 609):
        keys = [(t, [4, rng.choice((6, 9, 12, 15, 18))]) for t in range(p0, OP + 1, 4)]
        bars.append(group([rect(anim(keys), 0, x, 957, 2), fill("#ffffff")]))
    m.shape("preview-playing", [MED.text("Preview playing", 23, 362, 965)] + bars,
            ip=p0, parent=buttons, ks=layer_ks(o=in_out(p0 + 4, 10, SCROLL_OUT)))

    # the three hero cards, bottom right
    for k, (name, lines) in enumerate(HERO_CARDS):
        t = T_UI + 6 + 5 * k
        cx, cy = HERO_CARD_X[k] + 144, HERO_CARD_TOP + 81
        txt = [MED.text(line, 20, cx, 814 - 26 * (len(lines) - 1 - j), o=92, align="center")
               for j, line in enumerate(lines)]
        m.shape(f"hero card {k}: label", txt, ip=T_PAGE, parent=page, ks=layer_ks(
            p=anim([(t, [80, 0], "out"), (t + 22, [0, 0])]), o=in_out(t, out=SCROLL_OUT)))
        scale = (HERO_SCALE, HERO_SCALE)
        if k == 0:
            scale = anim([(156, [HERO_SCALE] * 2, "out"), (168, [HERO_SCALE * 1.06] * 2)])
        card = card_image(m, f"hero card {k}: {name}", imgs[name], (cx, cy), scale, 14, dict(
            p=anim([(t, [cx + 80, cy], "out"), (t + 22, [cx, cy])]), o=in_out(t, out=SCROLL_OUT)),
            page)
        if k == 0:
            m.shape("hero card 0: focus", [group([rect(TW + 14, TH + 14, TW / 2, TH / 2, 20),
                                                  stroke(FOCUS, 4 * 100 / HERO_SCALE)])],
                    ip=T_PAGE, parent=card, ks=layer_ks(o=anim([(156, [0]), (166, [100]),
                                                                (SCROLL_OUT[0], [100]),
                                                                (SCROLL_OUT[1], [0])])))

    # preview player bar at the bottom of the hero
    m.shape("preview-bar", bf([
        group([rect(1892, 36, 960, 1046, 6), fill("#000000", 55), stroke("#ffffff", 1, 12)]),
        icon(I_PAUSE, 22, 36, 1046),
        group([rect(1700, 4, 1000, 1046, 2), fill("#ffffff", 25)]),
        group([rect(anim([(p0, [0, 4], "linear"), (OP, [140, 4])]), 0,
                    anim([(p0, [150, 1046], "linear"), (OP, [220, 1046])]), 0, 2),
               fill("#ffffff", 90)]),
    ] + [group([MED.text(f"00:0{k}", 17, 58, 1052)],
               o=anim([(0, [0], "hold"), (p0 + 30 * k, [100], "hold"), (p0 + 30 * k + 30, [0])]))
         for k in range(3)]),
        ip=p0, parent=page, ks=layer_ks(o=anim([(p0 + 2, [0]), (p0 + 12, [100]),
                                                (T_SCROLL[0], [100]), (T_SCROLL[0] + 12, [0])])))

    # mini-player with the credits still rolling
    mx, my = MINI_C
    bottom = MINI_Y + MINI_H
    m.shape("mini-caption", bf([
        group([rect(MINI_W, 84, mx, bottom + 32, 10), fill(PANEL, 94)]),
        SEMI.text("Interstellar  ·  2014", 19, MINI_X + 20, bottom + 32),
        REG.text("Finished  ·  Did you enjoy it?", 15, MINI_X + 20, bottom + 56, MUTED),
        group([ellipse(38, 38, MINI_X + 406, bottom + 37), stroke("#ffffff", 1.5, 45)]),
        icon(I_THUMB, 17, MINI_X + 406, bottom + 37),
        group([ellipse(38, 38, MINI_X + 452, bottom + 37), stroke("#ffffff", 1.5, 45)]),
        flip(icon(I_THUMB, 17, MINI_X + 452, bottom + 38), MINI_X + 452, bottom + 38),
    ]), ip=s1 - 6, parent=page, ks=layer_ks(
        p=anim([(s1 - 4, [0, -50], "out"), (s1 + 16, [0, 0])]), o=fade(s1 - 4, s1 + 12)))

    size = anim([(s0, [W, H], "smooth"), (s1, [MINI_W, MINI_H])])
    centre = anim([(s0, [960, 540], "smooth"), (s1, list(MINI_C))])
    m.shape("mini-shadow", [group([rect(anim([(s0, [W + 20, H + 20], "smooth"),
                                              (s1, [MINI_W + 20, MINI_H + 20])]), 0,
                                        anim([(s0, [960, 548], "smooth"), (s1, [mx, my + 8])]), 0,
                                        14), fill("#000000", 45)])],
            ip=s0, parent=page, ks=layer_ks(o=fade(s0 + 6, s1)))
    m.precomp("video", credits, parent=page,
              masks=[mask(anim([(s0, rrect(0, 0, W, H, 0), "smooth"),
                                (s1, rrect(0, 0, W, H, 10 * W / MINI_W))]))],
              ks=layer_ks(p=centre, a=(960, 540),
                          s=anim([(s0, [100, 100], "smooth"), (s1, [MINI_SCALE, MINI_SCALE])])))
    m.shape("mini-controls", bf([
        group([rect(MINI_W - 20, 28, mx, bottom - 24, 6), fill("#000000", 60)]),
        icon(I_PAUSE, 16, MINI_X + 28, bottom - 24),
        group([rect(MINI_W - 80, 3, mx + 18, bottom - 24, 1.5), fill("#ffffff", 30)]),
        group([rect(anim([(s1, [(MINI_W - 80) * 0.975, 3], "linear"), (OP, [MINI_W - 80, 3])]), 0,
                    anim([(s1, [MINI_X + 58 + (MINI_W - 80) * 0.4875, bottom - 24], "linear"),
                          (OP, [mx + 18, bottom - 24])]), 0, 1.5), fill(BLUE)]),
    ]), ip=s1, parent=page, ks=layer_ks(o=fade(s1 + 2, s1 + 14)))
    m.shape("mini-border", [group([rect(size, 0, centre, 0, anim([(s0, [0], "smooth"), (s1, [10])])),
                                   stroke("#ffffff", 1.5, 22)])],
            ip=s0, parent=page, ks=layer_ks(o=fade(s0, s0 + 10)))

    # fixed navigation bar
    m.shape("nav-scrim", [group([rect(W, 200, 960, 100), gfill(
        [(0, "#000000", 0.6), (1, "#000000", 0)], (0, 0), (0, 200))])], ip=T_PAGE,
        ks=layer_ks(o=fade(T_PAGE, T_PAGE + 16)))
    m.shape("nav-bg", [group([rect(W, 76, 960, 38), fill(NAV_BG)])], ip=T_PAGE, ks=layer_ks(
        o=anim([(T_PAGE, [0]), (T_PAGE + 16, [70]), (T_SCROLL[0], [70]), (T_SCROLL[0] + 20, [96])])))
    m.shape("nav", bf(nav_items()), ip=T_PAGE, ks=layer_ks(o=fade(T_PAGE, T_PAGE + 16)))

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
    names = sorted({n for _, _, row in ROWS for n in row} | {"topgun_hero"})
    imgs = {n: image_asset(os.path.join(img_dir, f"{n}.jpg"), f"img_{n}") for n in names}
    credits = build_credits()
    martian_card = build_hover_card("martian", imgs["martian"], MARTIAN, T_HOVER)
    main_comp = build_main(credits, martian_card, imgs)
    data = animation(main_comp, [credits, martian_card], FPS, "Vionlabs recommendations",
                     images=imgs.values())
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
