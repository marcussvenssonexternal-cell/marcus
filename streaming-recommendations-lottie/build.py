"""Builds streaming-recommendations.json / .lottie.

Story (30 fps, 12 s, 1920x1080):
  0.0s  Fullscreen playback: the last shot of "Sky Pilots", jets fly into the
        sunset, end title fades in, progress bar runs out.
  2.8s  The finished video shrinks into a mini-player (top left) and the
        streaming home screen is revealed behind it.
  3.7s  Hero for the next title ("Wild Road") and three recommendation rails
        slide in: Recommended / Similar titles / Since you watched.
  5.0s  "Playing preview in 3-2-1" countdown.
  8.0s  The hero preview starts playing (parallax road trip), end credits keep
        rolling in the mini-player.
 11.5s  Fade to black so the loop restarts cleanly.

Run:  python3 build.py   (needs fonttools + uharfbuzz and the Inter font)
"""
import json
import os
import random
import zipfile

from lottie_kit import (Comp, Font, anim, animation, ellipse, fade, fill, gfill, group,
                        icon, layer_ks, poly, rect, ridge, sag_line, smooth, stroke, trim)

HERE = os.path.dirname(os.path.abspath(__file__))
FONT_DIR = os.environ.get("INTER_DIR", "/usr/share/fonts/opentype/inter")
REG = Font(f"{FONT_DIR}/Inter-Regular.otf")
MED = Font(f"{FONT_DIR}/Inter-Medium.otf")
SEMI = Font(f"{FONT_DIR}/Inter-SemiBold.otf")
BOLD = Font(f"{FONT_DIR}/Inter-Bold.otf")
BLACK = Font(f"{FONT_DIR}/Inter-Black.otf")

W, H, FPS, OP = 1920, 1080, 30, 360

# timeline (frames)
T_JETS = (0, 96)
T_TITLE = (30, 56)
T_CHROME_OUT = (74, 88)
T_SHRINK = (84, 120)
T_CREDITS = 96
T_COUNT = (150, 240)
T_PREVIEW = 240
T_FADE_OUT = (345, 360)

MINI_C, MINI_W, MINI_H = (332, 285), 480, 270  # mini-player centre / size
MINI_SCALE = 100 * MINI_W / W

BLUE = "#1d6fd6"
FOCUS = "#3d9bff"

# Material Design icons (Apache 2.0), 24x24 viewBox
I_PLAY = "M8 5v14l11-7z"
I_PAUSE = "M6 19h4V5H6v14zm8-14v14h4V5h-4z"
I_VOLUME = ("M3 9v6h4l5 5V4L7 9H3zm13.5 3c0-1.77-1.02-3.29-2.5-4.03v8.05c1.48-.73 2.5-2.25 "
            "2.5-4.02zM14 3.23v2.06c2.89.86 5 3.54 5 6.71s-2.11 5.85-5 6.71v2.06c4.01-.91 "
            "7-4.49 7-8.77s-2.99-7.86-7-8.77z")
I_FULLSCREEN = "M7 14H5v5h5v-2H7v-3zm-2-4h2V7h3V5H5v5zm12 7h-3v2h5v-5h-2v3zM14 5v2h3v3h2V5h-5z"
I_SEARCH = ("M15.5 14h-.79l-.28-.27C15.41 12.59 16 11.11 16 9.5 16 5.91 13.09 3 9.5 3S3 5.91 "
            "3 9.5 5.91 16 9.5 16c1.61 0 3.09-.59 4.23-1.57l.27.28v.79l5 4.99L20.49 19l-4.99-5"
            "zm-6 0C7.01 14 5 11.99 5 9.5S7.01 5 9.5 5 14 7.01 14 9.5 11.99 14 9.5 14z")
I_THUMB = ("M1 21h4V9H1v12zm22-11c0-1.1-.9-2-2-2h-6.31l.95-4.57.03-.32c0-.41-.17-.79-.44-1.06"
           "L14.17 1 7.59 7.59C7.22 7.95 7 8.45 7 9v10c0 1.1.9 2 2 2h9c.83 0 1.54-.5 1.84-1.22"
           "l3.02-7.05c.09-.23.14-.47.14-.73v-2z")


def bf(items):
    """Author back-to-front; Lottie draws the first shape on top."""
    return list(reversed(items))


def scroll(dx, t0=T_PREVIEW, t1=OP):
    """Hold still until the preview starts, then pan linearly."""
    return anim([(t0, [0, 0], "linear"), (t1, [dx, 0])])


# ------------------------------------------------------------------ artwork

JET = [(70, 0), (52, -5), (20, -8), (8, -10), (-18, -48), (-30, -50), (-22, -12), (-42, -11),
       (-56, -30), (-66, -31), (-62, -8), (-70, -6)]
JET = JET + [(x, -y) for x, y in reversed(JET[1:])]


def jet(color, p=(0, 0), s=100, r=0, burner=True, trail=0):
    items = []
    if trail:
        items.append(group([poly([(-70, -3), (-70, 3), (-70 - trail, 0)]), fill("#fff3e0", 22)]))
    items.append(group([poly(JET), fill(color)]))
    if burner:
        items.append(group([ellipse(16, 8, -72, 0), fill("#ffd27a", 90)]))
    return group(bf(items), p=p, s=(s, s), r=r, nm="jet")


def truck_body():
    navy, rail, cream = "#2f6690", "#244f70", "#efe3c6"
    driver = group([
        ellipse(32, 38, 40, -201),
        smooth([(22, -210), (30, -224), (48, -226), (60, -214), (56, -204), (24, -204)]),
        poly([(6, -171), (14, -184), (30, -189), (52, -189), (68, -184), (76, -171)]),
        fill("#2b2424")], nm="driver")
    return bf([
        group([poly([(-285, -72), (-285, -150), (-45, -150), (-45, -240), (90, -240),
                     (148, -165), (272, -152), (290, -132), (290, -72)]), fill(navy)], nm="body"),
        group([poly([(-45, -240), (90, -240), (101, -225), (-45, -225)]), fill(cream)]),
        group([rect(575, 13, 2.5, -121), fill(cream)]),
        group([rect(240, 7, -165, -147), fill(rail)]),
        group([poly([(-30, -226), (82, -226), (126, -171), (-30, -171)]), fill("#b9d4e2")]),
        driver,
        group([ellipse(116, 116, -185, -48), ellipse(116, 116, 185, -48), fill("#17232e")]),
        group([poly([(112, -163), (112, -80)], closed=False), stroke("#1d3f5c", 2.5)]),
        group([rect(22, 5, -12, -140, 2), fill("#d5d8db")]),
        group([rect(24, 18, 296, -80, 4), rect(20, 18, -291, -80, 4), fill("#cfd3d6")]),
        group([ellipse(12, 22, 287, -118), fill("#fff1c2")]),
        group([rect(7, 22, -283, -130, 2), fill("#d6453d")]),
    ])


def wheel():
    return bf([
        group([ellipse(96, 96), fill("#1b1b1d")]),
        group([ellipse(56, 56), fill("#c9cdd2")]),
        group([rect(8, 50), rect(50, 8), fill("#8e949b")]),
        group([ellipse(18, 18), fill("#5d6368")]),
        group([ellipse(7, 7, 0, -17), fill("#f0f2f4")]),
    ])


def dog():
    dark, tan = "#3b2a1f", "#a8703f"
    return bf([
        group([smooth([(-178, -150), (-170, -200), (-150, -228), (-122, -238), (-96, -226),
                       (-84, -190), (-80, -150)]), fill(dark)], nm="dog-body"),
        group([smooth([(-100, -224), (-86, -196), (-84, -160), (-100, -160), (-108, -200)]),
               fill(tan)]),
        group([rect(36, 8, 0, 0, 3), fill("#c0392b")], p=(-110, -222), r=-18),
        group([poly([(-128, -262), (-120, -310), (-102, -270)]),
               poly([(-106, -272), (-94, -312), (-82, -264)]), fill("#2a1d15")]),
        group([poly([(-122, -268), (-119, -298), (-109, -272)]),
               poly([(-100, -272), (-94, -300), (-88, -268)]), fill("#7d5539")]),
        group([ellipse(58, 48, -104, -256), fill(dark)]),
        group([ellipse(12, 18, -64, -230), fill("#e2687a")]),
        group([smooth([(-90, -272), (-60, -262), (-48, -252), (-52, -240), (-70, -236),
                       (-92, -242)]), fill("#b07a48")]),
        group([ellipse(13, 11, -50, -253), fill("#141414")]),
        group([ellipse(8, 5, -92, -277), fill(tan)]),
        group([ellipse(8, 8, -94, -266), fill("#111111")]),
        group([ellipse(3, 3, -93, -267), fill("#ffffff")]),
    ])


def full_truck(p, s):
    """Static truck (for thumbnails)."""
    wheels = [group(wheel(), p=(x, -48)) for x in (-185, 185)]
    return group(bf([group(dog()), group(truck_body())] + wheels), p=p, s=(s, s), nm="truck")


def cloud(cx, cy, s, o=70):
    blobs = [(-60, 0, 120, 46), (0, -14, 110, 60), (55, 2, 120, 44), (10, 10, 200, 36)]
    return group([ellipse(w * s, h * s, cx + x * s, cy + y * s) for x, y, w, h in blobs]
                 + [fill("#ffffff", o)])


def shrub(x, y, s, col="#7c7636"):
    return group([ellipse(60 * s, 34 * s, x - 22 * s, y - 10 * s),
                  ellipse(70 * s, 46 * s, x + 10 * s, y - 18 * s),
                  ellipse(56 * s, 30 * s, x + 38 * s, y - 8 * s), fill(col)])


def rock(x, y, s, col="#a3764e"):
    return group([smooth([(x - 30 * s, y), (x - 22 * s, y - 18 * s), (x + 4 * s, y - 24 * s),
                          (x + 28 * s, y - 12 * s), (x + 32 * s, y)]), fill(col)])


# ------------------------------------------------- scene: the ending video

def build_ending():
    c = Comp(W, H, OP, "comp_ending")
    cam = c.null("camera", ks=layer_ks(p=(960, 540), a=(960, 540),
                                       s=anim([(0, [100, 100], "linear"), (T_CREDITS, [105, 105])])))
    c.shape("sky", [group([rect(W, H, 960, 540), gfill(
        [(0, "#5a2a2e", 1), (0.35, "#a2472c", 1), (0.7, "#d9773a", 1), (1, "#f2b066", 1)],
        (960, 0), (960, 720))])], parent=cam)
    c.shape("sun", bf([
        group([ellipse(1040, 1040, 1180, 690), gfill(
            [(0, "#ffe0a0", 0.95), (0.25, "#ffc070", 0.5), (1, "#ff9a50", 0)],
            (1180, 690), (1700, 690), radial=True)]),
        group([ellipse(130, 130, 1180, 690), fill("#fff0c8")]),
    ]), parent=cam)
    c.shape("hills", bf([
        group([ridge([(-60, 705), (240, 690), (520, 712), (820, 698), (1100, 716), (1400, 694),
                      (1700, 708), (1980, 700)], 1140), fill("#9b4a2f")]),
        group([ridge([(-60, 780), (300, 760), (640, 785), (980, 768), (1320, 790), (1650, 770),
                      (1980, 782)], 1140), fill("#5f2a1d")]),
        group([ridge([(-60, 880), (260, 850), (560, 870), (900, 845), (1240, 872), (1560, 850),
                      (1980, 866)], 1140), fill("#2a120c")]),
    ]), parent=cam)
    # two jets flying into the sunset
    for name, p0, p1, s0, s1, delay in (("jet-2", (150, 330), (1085, 662), 150, 16, 4),
                                        ("jet-1", (280, 260), (1125, 645), 170, 18, 0)):
        t0, t1 = T_JETS[0] + delay, T_JETS[1]
        c.shape(name, [jet("#2a140c", trail=260)], parent=cam, op=104, ks=layer_ks(
            p=anim([(t0, list(p0), "io"), (t1, list(p1))]),
            s=anim([(t0, [s0, s0], "io"), (t1, [s1, s1])]),
            r=22, o=anim([(t1 - 12, 100), (t1 + 6, 0)])))
    c.shape("dim", [group([rect(W, H, 960, 540), fill("#000000")])],
            ks=layer_ks(o=fade(T_CREDITS, 140, 0, 45)))

    roll = anim([(T_CREDITS, [0, 0], "linear"), (OP, [0, -1408])])
    c.shape("end-title", [BLACK.text("SKY PILOTS", 120, 960, 420, align="center", tracking=0.14)],
            ks=layer_ks(p=anim([(T_TITLE[0], [0, 14], "out"), (T_TITLE[1], [0, 0]),
                                (T_CREDITS, [0, 0], "linear"), (OP, [0, -1408])]),
                        o=fade(*T_TITLE)))
    rng = random.Random(7)
    roles, names, y = [], [], 1100
    for k in range(28):
        if k in (6, 15, 23):
            names.append(rect(rng.randint(180, 280), 14, 960, y + 10, 7))
            y += 70
            continue
        rw, nw = rng.randint(90, 200), rng.randint(140, 260)
        roles.append(rect(rw, 14, 935 - rw / 2, y, 7))
        names.append(rect(nw, 14, 985 + nw / 2, y, 7))
        y += 42
    c.shape("credits", [group(roles + [fill("#ffffff", 55)]), group(names + [fill("#ffffff", 90)])],
            ks=layer_ks(p=roll))
    return c


# ------------------------------------------------ scene: hero "Wild Road"

def build_hero():
    c = Comp(W, H, OP, "comp_hero")
    c.shape("sky", [group([rect(W, 640, 960, 320), gfill(
        [(0, "#4f8fcb", 1), (0.5, "#8dbbe0", 1), (0.92, "#e9dcc0", 1), (1, "#f2d7ae", 1)],
        (960, 0), (960, 620))])])
    c.shape("sun", bf([
        group([ellipse(760, 760, 1580, 250), gfill(
            [(0, "#fff4d6", 0.85), (0.3, "#fff0cc", 0.35), (1, "#ffffff", 0)],
            (1580, 250), (1960, 250), radial=True)]),
        group([ellipse(110, 110, 1580, 250), fill("#fff8e6")]),
    ]))
    c.shape("clouds", [cloud(330, 190, 1.0, 55), cloud(860, 120, 0.8, 50), cloud(1240, 300, 0.6, 45),
                       cloud(2050, 170, 0.9, 50)], ks=layer_ks(p=scroll(-40)))
    c.shape("mesas", [group([poly([
        (-100, 610), (-100, 560), (80, 560), (130, 520), (380, 515), (420, 560), (700, 565),
        (760, 500), (1050, 495), (1090, 545), (1300, 550), (1350, 530), (1500, 528),
        (1540, 560), (1800, 565), (1850, 510), (2100, 505), (2150, 560), (2400, 565),
        (2400, 610)]), fill("#c9a48c")])], ks=layer_ks(p=scroll(-60)))
    c.shape("hills", [group([ridge([(-100, 600), (200, 585), (500, 595), (800, 578), (1100, 592),
                                    (1400, 580), (1700, 590), (2000, 582), (2300, 594),
                                    (2600, 588)], 650), fill("#c99466")])],
            ks=layer_ks(p=scroll(-140)))
    c.shape("ground", [group([rect(W, 480, 960, 840), gfill(
        [(0, "#e4b57e", 1), (1, "#c58a52", 1)], (960, 600), (960, 1080))])])
    poles, wires = [], []
    for k in range(7):
        x = -60 + 540 * k
        poles += [rect(7, 177, x, 566.5), rect(64, 6, x, 492)]
        wires += [sag_line(x - 28, 494, x + 512, 494, 26), sag_line(x + 28, 494, x + 568, 494, 26)]
    c.shape("poles", [group(wires + [stroke("#5a3d2c", 1.6, 70)]),
                      group(poles + [fill("#6d4c36")])], ks=layer_ks(p=scroll(-1000)))
    rng = random.Random(3)
    c.shape("roadside", [shrub(x + rng.randint(-80, 80), 652, 0.45, "#8e7f45")
                         for x in range(0, 5600, 420)], ks=layer_ks(p=scroll(-3600)))
    c.shape("road", bf([
        group([rect(W + 40, 110, 960, 710), fill("#4b474e")]),
        group([rect(W + 40, 4, 960, 657), rect(W + 40, 4, 960, 763), fill("#e8e0cf", 75)]),
        group([poly([(-300, 712), (2300, 712)], closed=False),
               stroke("#f3cd55", 7, dash=(70, 70, anim([(T_PREVIEW, 0, "linear"),
                                                         (OP, 3600)])))]),
    ]))
    fg = []
    for x in range(60, 7300, 520):
        x += rng.randint(-120, 120)
        y = rng.randint(820, 900)
        fg.append(rock(x + 70, y + 6, 0.8, "#9c7049") if rng.random() < 0.35
                  else shrub(x, y, 1.2, "#7a7038"))
    c.shape("foreground", fg, ks=layer_ks(p=scroll(-5200)))

    tx, ty = 1320, 738
    c.shape("truck-shadow", [group([ellipse(640, 24, tx, ty + 4), fill("#000000", 25)])])
    for n, off in enumerate((0, 4, 7, 11, 14, 18)):
        pos, sc, op = [], [], []
        t = T_PREVIEW + off
        while t < OP:  # 21-frame puffs kicked up behind the rear wheel
            pos += [(t, [tx - 230, ty - 10 + 4 * (n % 3)], "out"), (t + 20, [tx - 410, ty - 34], "hold")]
            sc += [(t, [40, 40], "out"), (t + 20, [160, 160], "hold")]
            op += [(t, [0], "linear"), (t + 4, [40], "linear"), (t + 20, [0], "hold")]
            t += 21
        c.shape(f"dust-{n}", [group([ellipse(40, 40), fill("#ecd5ab")])], ip=T_PREVIEW + off,
                ks=layer_ks(p=anim(pos), s=anim(sc), o=anim(op)))

    bounce = [(0, [tx, ty], "io")]
    pattern = [0, -3, 0, -2, -1, -4, 0, -2, 1, -3]
    for k, t in enumerate(range(T_PREVIEW, OP + 1, 5)):
        bounce.append((t, [tx, ty + pattern[k % len(pattern)]], "io"))
    truck = c.null("truck", ks=layer_ks(p=anim(bounce)))
    nod = [(T_PREVIEW, [0])] + [(t, [(4, -2, 3, -1)[k % 4]]) for k, t in
                                enumerate(range(T_PREVIEW + 8, OP + 1, 8))]
    c.shape("dog", dog(), parent=truck, ks=layer_ks(p=(-115, -190), a=(-115, -190), r=anim(nod)))
    c.shape("truck-body", truck_body(), parent=truck)
    for x in (-185, 185):
        c.shape("wheel", wheel(), parent=truck, ks=layer_ks(
            p=(x, -48), r=anim([(T_PREVIEW, [0], "linear"), (OP, [3000])])))
    return c


# --------------------------------------------------------- thumbnails

TW, TH = 288, 162


def build_card_wild():
    c = Comp(TW, TH, OP, "comp_card_wild")
    c.shape("art", bf([
        group([rect(TW, 112, 144, 56), gfill([(0, "#5b9bd5", 1), (1, "#f0dcb4", 1)], (0, 0),
                                              (0, 110))]),
        group([ellipse(120, 120, 236, 34), gfill([(0, "#fff6dc", 0.9), (1, "#ffffff", 0)],
                                                  (236, 34), (296, 34), radial=True)]),
        group([poly([(0, 112), (0, 96), (40, 96), (52, 86), (110, 85), (120, 96), (176, 97),
                     (190, 82), (250, 81), (262, 95), (288, 96), (288, 112)]), fill("#c9a48c")]),
        group([rect(TW, 52, 144, 136), gfill([(0, "#dcaa70", 1), (1, "#c38a52", 1)], (0, 110),
                                              (0, 162))]),
        group([rect(TW, 26, 144, 127), fill("#4b474e")]),
        group([poly([(0, 127), (288, 127)], closed=False), stroke("#f3cd55", 2, dash=(14, 14, 0))]),
        full_truck((92, 137), 27),
        group([rect(TW, 72, 144, 126), gfill([(0, "#000000", 0), (1, "#000000", 0.6)], (0, 90),
                                              (0, 162))]),
        group([BLACK.text("WILD", 36, 278, 114, "#000000", 45, "right")], p=(2, 2)),
        group([BLACK.text("ROAD", 36, 278, 150, "#000000", 45, "right")], p=(2, 2)),
        BLACK.text("WILD", 36, 278, 114, "#ffd23f", align="right"),
        BLACK.text("ROAD", 36, 278, 150, "#ffd23f", align="right"),
    ]))
    return c


def build_card_sky():
    c = Comp(TW, TH, OP, "comp_card_sky")
    w = BLACK.width("SKY PILOTS ", 26)
    c.shape("art", bf([
        group([rect(TW, TH, 144, 81), gfill(
            [(0, "#6e2a1c", 1), (0.45, "#d0703a", 1), (0.8, "#f4b766", 1), (1, "#7d3b22", 1)],
            (0, 0), (0, 162))]),
        group([ellipse(260, 260, 214, 132), gfill([(0, "#fff2c8", 0.95), (1, "#ffd27a", 0)],
                                                   (214, 132), (344, 132), radial=True)]),
        group([ridge([(0, 140), (70, 132), (150, 142), (220, 130), (288, 138)], 162),
               fill("#3a1c12")]),
        jet("#24140e", p=(96, 108), s=48, r=-12, trail=90),
        jet("#24140e", p=(196, 74), s=118, r=-12, trail=160),
        BLACK.text("SKY PILOTS", 26, 14, 38),
        BLACK.text("II", 26, 14 + w, 38, "#ffd27a"),
        SEMI.text("NEXT GENERATION", 9.5, 15, 54, o=85, tracking=0.22),
    ]))
    return c


def build_card_deck():
    c = Comp(TW, TH, OP, "comp_card_deck")
    rng = random.Random(11)
    stars = [ellipse(s, s, rng.uniform(0, TW), rng.uniform(4, 84))
             for s in [rng.choice((1.5, 2, 2.5)) for _ in range(30)]]
    dashes, lights = [], []
    for k in range(7):
        t = ((k + 1) / 7) ** 1.7
        dashes.append(rect(1 + 4 * t, 2 + 9 * t, 144, 100 + 62 * t))
    for k in range(9):
        t = ((k + 1) / 9) ** 1.4
        d = 1.4 + 3.6 * t
        lights += [ellipse(d, d, 136 - 98 * t, 100 + 62 * t), ellipse(d, d, 152 + 98 * t, 100 + 62 * t)]
    c.shape("art", bf([
        group([rect(TW, 100, 144, 50), gfill(
            [(0, "#08122e", 1), (0.6, "#1c2b5c", 1), (1, "#6b3f80", 1)], (0, 0), (0, 100))]),
        group(stars + [fill("#ffffff", 70)]),
        group([ellipse(340, 90, 144, 100), gfill([(0, "#c062a8", 0.6), (1, "#c062a8", 0)],
                                                  (144, 100), (314, 100), radial=True)]),
        group([rect(TW, 62, 144, 131), fill("#10172b")]),
        group([poly([(136, 100), (152, 100), (250, 162), (38, 162)]), fill("#2b3150")]),
        group(dashes + [fill("#ffffff", 80)]),
        group(lights + [fill("#ffd27a")]),
        jet("#dfe5f5", p=(214, 50), s=42, r=-26, burner=False),
        BLACK.text("FLIGHT DECK", 25, 14, 38),
        group([rect(80, 16, 54, 55, 3), fill("#e5484d")]),
        BOLD.text("NEW SERIES", 9, 54, 58.4, align="center", tracking=0.1),
    ]))
    return c


# ------------------------------------------------------------- main comp

def nav_bar():
    items = [icon(I_SEARCH, 40, 66, 55, nm="search"),
             group([rect(46, 38, 168, 55, 5), stroke("#ffffff", 2.5)]),
             BOLD.text("TV", 16, 168, 61, align="center")]
    x = 290
    for label in ("HOME", "LIVE TV", "MY LIST", "LIBRARY", "MOVIES", "SERIES", "SPORT", "KIDS"):
        w = MED.width(label, 23, 0.04)
        items.append(MED.text(label, 23, x, 63, o=100 if label == "LIBRARY" else 88, tracking=0.04))
        if label == "LIBRARY":
            items.append(group([rect(w, 3, x + w / 2, 78), fill("#ffffff")]))
        x += w + 92
    items.append(group([ellipse(44, 44, 1858, 55), fill("#5b6b8c")]))
    items.append(SEMI.text("M", 20, 1858, 62, align="center"))
    return items


def build_main(ending, hero, cards):
    m = Comp(W, H, OP, "main")
    s0, s1 = T_SHRINK

    # hero background (revealed behind the shrinking video)
    m.precomp("hero", hero, ip=80, ks=layer_ks(p=(960, 540), a=(960, 540), s=anim([
        (s0, [108, 108], "out"), (140, [100, 100]), (T_PREVIEW, [100, 100], "linear"),
        (OP, [103, 103])])))
    m.shape("hero-scrim-left", [group([rect(W, H, 960, 540), gfill(
        [(0, "#000000", 0.85), (0.38, "#000000", 0.55), (1, "#000000", 0)], (0, 540),
        (1150, 540))])], ip=80)
    m.shape("hero-scrim-bottom", [group([rect(W, 460, 960, 850), gfill(
        [(0, "#000000", 0), (1, "#000000", 0.78)], (0, 620), (0, 1080))])], ip=80)

    # preview player bar (after countdown)
    p0 = T_PREVIEW
    m.shape("preview-bar", bf([
        group([rect(1896, 36, 960, 1046, 4), fill("#000000", 55), stroke("#ffffff", 1, 12)]),
        icon(I_PAUSE, 22, 34, 1046),
        group([rect(1700, 4, 1000, 1046, 2), fill("#ffffff", 25)]),
        group([rect(anim([(p0, [0, 4], "linear"), (OP, [60, 4])]), 0,
                    anim([(p0, [150, 1046], "linear"), (OP, [180, 1046])]), 0, 2),
               fill("#ffffff", 90)]),
    ] + [group([MED.text(f"00:0{k}", 17, 56, 1052)],
               o=anim([(0, [0], "hold"), (p0 + 30 * k, [100], "hold"), (p0 + 30 * k + 30, [0])])
               if k < 3 else anim([(0, [0], "hold"), (p0 + 90, [100])])) for k in range(4)]),
        ip=p0, ks=layer_ks(o=fade(p0 + 2, p0 + 12)))

    # hero copy
    def enter(t, dy=30):
        return layer_ks(p=anim([(t, [0, dy], "out"), (t + 22, [0, 0])]), o=fade(t, t + 18))

    m.shape("title", [BOLD.text("Wild Road", 104, 108, 768)], ip=100, ks=enter(112))
    m.shape("meta", [MED.text("2022  ·  1h 41m  ·  Adventure", 25, 114, 812, o=88)],
            ip=100, ks=enter(116))
    desc = ["A retired ranger and his loyal dog take", "a road trip across the desert to say",
            "goodbye to an old friend."]
    m.shape("description", [REG.text(line, 23, 114, 852 + 31 * k, o=86) for k, line in enumerate(desc)],
            ip=100, ks=enter(120))

    bt = 124
    buttons = m.shape("buttons", bf([
        group([rect(210, 60, 213, 968, 3), rect(310, 60, 485, 968, 3), fill(BLUE)]),
        MED.text("Play now", 25, 146, 977),
        icon(I_PLAY, 30, 284, 968),
    ]), ip=100, ks=enter(bt))
    vis = anim([(bt, [0]), (bt + 18, [100]), (p0, [100]), (p0 + 8, [0])])
    m.shape("countdown-sweep", [group([rect(anim([(T_COUNT[0], [0, 60], "linear"),
                                                  (T_COUNT[1], [310, 60])]), 0,
                                            anim([(T_COUNT[0], [330, 968], "linear"),
                                                  (T_COUNT[1], [485, 968])]), 0, 3),
                                       fill("#ffffff", 16)])],
            ip=100, op=p0 + 10, parent=buttons, ks=layer_ks(o=vis))
    m.shape("countdown-label", [MED.text("Playing preview in", 25, 362, 977)],
            ip=100, op=p0 + 10, parent=buttons, ks=layer_ks(o=vis))
    m.shape("countdown-ring", bf([
        group([ellipse(30, 30, 600, 968), stroke("#ffffff", 2, 35)]),
        group([ellipse(30, 30, 600, 968), stroke("#ffffff", 2.4),
               trim(e=anim([(T_COUNT[0], [100], "linear"), (T_COUNT[1], [0])]))]),
    ]), ip=100, op=p0 + 10, parent=buttons, ks=layer_ks(o=vis))
    cuts = [100, 177, 207, 237, p0 + 10]
    for k, n in enumerate("3210"):
        t_in, t_out = cuts[k], cuts[k + 1]
        o = vis if k in (0, 3) else 100
        m.shape(f"countdown-{n}", [SEMI.text(n, 17, 600, 974, align="center")], ip=t_in, op=t_out,
                parent=buttons, ks=layer_ks(p=(600, 968), a=(600, 968), o=o, s=anim(
                    [(t_in, [60, 60], "out"), (t_in + 7, [100, 100])]) if k else (100, 100)))
    rng = random.Random(5)
    bars = []
    for k, x in enumerate((593, 600, 607)):
        keys = [(t, [4, rng.choice((6, 9, 12, 15, 18))]) for t in range(p0, OP + 1, 4)]
        bars.append(group([rect(anim(keys), 0, x, 968, 2), fill("#ffffff")]))
    m.shape("preview-playing", [MED.text("Preview playing", 25, 362, 977)] + bars,
            ip=p0, parent=buttons, ks=layer_ks(o=fade(p0 + 4, p0 + 14)))

    # recommendation rails
    labels = [["Recommended"], ["Similar titles"], ["Since you watched", "Sky Pilots"]]
    for k, (comp, lines) in enumerate(zip(cards, labels)):
        cx, t = 1096 + 302 * k, 118 + 5 * k
        txt = [MED.text(line, 22, cx, 815 - 28 * (len(lines) - 1 - j), o=92, align="center")
               for j, line in enumerate(lines)]
        m.shape(f"rail-label-{k}", txt, ip=100, ks=layer_ks(
            p=anim([(t, [90, 0], "out"), (t + 22, [0, 0])]), o=fade(t, t + 16)))
        card = m.precomp(f"card-{k}", comp, ip=100, ks=layer_ks(
            p=anim([(t, [cx + 90, 917], "out"), (t + 22, [cx, 917])]), a=(144, 81),
            o=fade(t, t + 16),
            s=anim([(148, [100, 100], "out"), (160, [106, 106])]) if k == 0 else (100, 100)))
        if k == 0:
            m.shape("focus-ring", [group([rect(294, 168, 0, 0, 4), stroke(FOCUS, 4)])], ip=140,
                    parent=card, ks=layer_ks(p=(144, 81), o=fade(148, 158)))

    # mini-player chrome
    mx, my = MINI_C
    m.shape("mini-caption", bf([
        group([rect(MINI_W, 104, mx, 474), fill("#000000", 52)]),
        MED.text("Sky Pilots  ·  1986", 22, 126, 482),
        group([ellipse(46, 46, 520, 474), stroke("#ffffff", 2.5)]),
        icon(I_THUMB, 22, 520, 474),
    ]), ip=110, ks=layer_ks(p=anim([(114, [0, -50], "out"), (136, [0, 0])]), o=fade(114, 132)))

    size = anim([(s0, [W, H], "smooth"), (s1, [MINI_W, MINI_H])])
    size_pad = anim([(s0, [W + 16, H + 16], "smooth"), (s1, [MINI_W + 16, MINI_H + 16])])
    centre = anim([(s0, [960, 540], "smooth"), (s1, list(MINI_C))])
    centre_pad = anim([(s0, [960, 546], "smooth"), (s1, [mx, my + 6])])
    m.shape("mini-shadow", [group([rect(size_pad, 0, centre_pad, 0, 8), fill("#000000", 28)])],
            ip=s0, ks=layer_ks(o=fade(s0 + 6, s1)))
    m.precomp("video", ending, ks=layer_ks(
        p=centre, a=(960, 540),
        s=anim([(s0, [100, 100], "smooth"), (s1, [MINI_SCALE, MINI_SCALE])])))
    fill_w = anim([(s1, [MINI_W * 0.97, 4], "linear"), (OP, [MINI_W * 0.995, 4])])
    fill_x = anim([(s1, [92 + MINI_W * 0.485, my + 133], "linear"), (OP, [92 + MINI_W * 0.4975, my + 133])])
    m.shape("mini-progress", bf([
        group([rect(MINI_W, 4, mx, my + 133), fill("#ffffff", 25)]),
        group([rect(fill_w, 0, fill_x, 0), fill(FOCUS)]),
    ]), ip=s1, ks=layer_ks(o=fade(s1, s1 + 12)))
    m.shape("mini-border", [group([rect(size, 0, centre, 0), stroke("#ffffff", 3, 90)])],
            ip=s0, ks=layer_ks(o=fade(s0, s0 + 8)))

    # fullscreen player controls
    track_x0, track_w, cy = 136, 1504, 1026

    def remaining(k, t_in, t_out):
        o = anim([(0, [0], "hold"), (t_in, [100], "hold"), (t_out, [0])]) if t_in else \
            anim([(0, [100], "hold"), (t_out, [0])])
        return group([MED.text(f"-00:0{k}", 21, 1662, 1034)], o=o)

    m.shape("player-controls", bf([
        group([rect(W, 220, 960, 970), gfill([(0, "#000000", 0), (1, "#000000", 0.75)],
                                              (0, 860), (0, 1080))]),
        group([ellipse(48, 48, 80, cy), stroke("#ffffff", 2.5)]),
        icon(I_PAUSE, 24, 80, cy),
        group([rect(track_w, 5, track_x0 + track_w / 2, cy, 2.5), fill("#ffffff", 30)]),
        group([rect(anim([(0, [track_w * 0.94, 5], "linear"), (s0, [track_w, 5])]), 0,
                    anim([(0, [track_x0 + track_w * 0.47, cy], "linear"),
                          (s0, [track_x0 + track_w / 2, cy])]), 0, 2.5), fill("#2f86ff")]),
        group([ellipse(18, 18, 0, 0), fill("#ffffff")],
              p=anim([(0, [track_x0 + track_w * 0.94, cy], "linear"), (s0, [track_x0 + track_w, cy])])),
        remaining(3, 0, 24), remaining(2, 24, 54), remaining(1, 54, 84), remaining(0, 84, 200),
        icon(I_VOLUME, 34, 1772, cy),
        icon(I_FULLSCREEN, 34, 1846, cy),
    ]), op=T_CHROME_OUT[1] + 2, ks=layer_ks(o=fade(*T_CHROME_OUT, 100, 0)))

    m.shape("nav-scrim", [group([rect(W, 200, 960, 100), gfill(
        [(0, "#000000", 0.65), (1, "#000000", 0)], (0, 0), (0, 200))])])
    m.shape("nav", bf(nav_bar()))
    m.shape("fade", [group([rect(W, H, 960, 540), fill("#000000")])], ks=layer_ks(
        o=anim([(0, [100]), (10, [0]), (T_FADE_OUT[0], [0]), (T_FADE_OUT[1], [100])])))
    return m


def main():
    ending, hero = build_ending(), build_hero()
    cards = [build_card_wild(), build_card_sky(), build_card_deck()]
    main_comp = build_main(ending, hero, cards)
    data = animation(main_comp, [ending, hero] + cards, FPS, "Streaming recommendations")
    text = json.dumps(data, separators=(",", ":"))
    out_json = os.path.join(HERE, "streaming-recommendations.json")
    with open(out_json, "w") as f:
        f.write(text)
    manifest = {"version": "1.0", "generator": "build.py", "author": "", "revision": 1,
                "animations": [{"id": "streaming-recommendations", "speed": 1, "loop": True,
                                "autoplay": True, "direction": 1, "playMode": "normal"}]}
    with zipfile.ZipFile(os.path.join(HERE, "streaming-recommendations.lottie"), "w",
                         zipfile.ZIP_DEFLATED) as z:
        z.writestr("manifest.json", json.dumps(manifest))
        z.writestr("animations/streaming-recommendations.json", text)
    print(f"wrote {out_json} ({len(text) / 1024:.0f} KB)")


if __name__ == "__main__":
    main()
