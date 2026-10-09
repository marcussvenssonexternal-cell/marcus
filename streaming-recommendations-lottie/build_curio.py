"""Builds the Lotties for the Curio landing page (vionlabs.com/curio).

One Lottie per visual slot on the page. Each one highlights, in turn, the
thing the section is about:

  curio-hero                        Hero (1920x1080, 8.4 s). Interstellar's credits
                                    shrink into a mini-player, then the three
                                    cards light up in turn: Because You Watched,
                                    Recommendations and Similar Titles. The loop
                                    is 3 x 2.8 s, the same rhythm as the hero's
                                    rotating headline, and carries markers for
                                    each phase.
  curio-because-you-watched         Three experiences, row 1 (1280x720, 6 s).
                                    What viewers who loved Interstellar watched
                                    next; the top pick lights up.
  curio-personalized-recommendations
                                    Three experiences, row 2 (1280x720, 6 s).
                                    A day-one viewer with two titles watched gets
                                    mood rows; two picks light up.
  curio-similar-titles              Three experiences, row 3 (1280x720, 6 s).
                                    Interstellar's title page; as a similar title
                                    lights up, so do the mood tags they share.

CURIO_BLUR=1 builds the "-blurred" variants with the movie artwork blurred,
matching the screenshots currently on the page.

Run:  python3 build_curio.py && CURIO_BLUR=1 python3 build_curio.py
"""
import json
import os
import tempfile
import zipfile

from PIL import Image, ImageFilter

from curio_ui import (BG, BLUE, FOCUS, GENRE, GENRE_EDGE, I_PAUSE, I_PLAY, I_THUMB, MED, MOOD,
                      MUTED, NAV_BG, PANEL, REG, SEMI, BOLD, TH, TW, bf, build_credits, flip,
                      nav_items, pill, pill_row)
from lottie_kit import (Comp, anim, animation, ellipse, fade, fill, gfill, group, icon, image_asset,
                        layer_ks, mask, rect, rrect, stroke)

HERE = os.path.dirname(os.path.abspath(__file__))
FPS = 30
BLUR = os.environ.get("CURIO_BLUR") == "1"
SUFFIX = "-blurred" if BLUR else ""
ARTWORK = {"interstellar", "interstellar_wide", "topgun", "topgun_hero", "nohardfeelings",
           "spiderverse", "oppenheimer", "martian", "arrival", "2001", "sunshine"}

# Material Design icons (Apache 2.0)
I_GROUP = ("M16 11c1.66 0 2.99-1.34 2.99-3S17.66 5 16 5c-1.66 0-3 1.34-3 3s1.34 3 3 3zm-8 0c1.66 0 "
           "2.99-1.34 2.99-3S9.66 5 8 5C6.34 5 5 6.34 5 8s1.34 3 3 3zm0 2c-2.33 0-7 1.17-7 3.5V19h14"
           "v-2.5c0-2.33-4.67-3.5-7-3.5zm8 0c-.29 0-.62.02-.97.05 1.16.84 1.97 1.97 1.97 3.45V19h6v-2.5"
           "c0-2.33-4.67-3.5-7-3.5z")
I_PERSON = ("M12 12c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm0 2c-2.67 0-8 1.34-8 4v2h16"
            "v-2c0-2.66-5.33-4-8-4z")
I_SPARKLE = ("M19 9l1.25-2.75L23 5l-2.75-1.25L19 1l-1.25 2.75L15 5l2.75 1.25L19 9zm-7.5.5L9 4 6.5 "
             "9.5 1 12l5.5 2.5L9 20l2.5-5.5L17 12l-5.5-2.5zM19 15l-1.25 2.75L15 19l2.75 1.25L19 23"
             "l1.25-2.75L23 19l-2.75-1.25L19 15z")
I_WAVE = "M7 18h2V6H7v12zm4 4h2V2h-2v20zm-8-8h2v-4H3v4zm12 4h2V6h-2v12zm4-8v4h2v-4h-2z"

BACKDROP_CROP = {"oppenheimer": (57, 0, 353, 166)}   # 16:9 crop above the poster title

CARD_INFO = {
    "oppenheimer": ("Oppenheimer", "drama • history • thriller", ["intense", "thought-provoking"]),
    "topgun": ("Top Gun: Maverick", "action • adventure • drama", ["high octane", "intense"]),
    "arrival": ("Arrival", "sci-fi • drama • mystery", ["thought-provoking", "emotional"]),
    "martian": ("The Martian", "sci-fi • adventure • drama", ["suspenseful", "survival"]),
}


class Images:
    """Embeds images once per Lottie; derived backdrops are made on the fly."""

    def __init__(self):
        self.assets = {}
        self.tmp = tempfile.mkdtemp(prefix="curio-img-")

    def _prepare(self, name):
        src = os.path.join(HERE, "images", f"{name}.jpg")
        if name.endswith("_bd"):            # soft full-screen backdrop from a thumbnail
            base = name[:-3]
            im = Image.open(os.path.join(HERE, "images", f"{base}.jpg")).convert("RGB")
            im = im.crop(BACKDROP_CROP.get(base, (0, 0, im.width, im.height)))
            im = im.resize((960, 540), Image.LANCZOS).filter(ImageFilter.GaussianBlur(10 if BLUR else 3))
        elif BLUR and name in ARTWORK:
            im = Image.open(src).convert("RGB")
            im = im.filter(ImageFilter.GaussianBlur(10 if im.width > 500 else 6))
        else:
            return src
        out = os.path.join(self.tmp, f"{name}.jpg")
        im.save(out, quality=82, optimize=True)
        return out

    def __call__(self, name):
        if name not in self.assets:
            self.assets[name] = image_asset(self._prepare(name), f"img_{name}")
        return self.assets[name]


# ---------------------------------------------------------------- building blocks

def on_off(intervals, ramp=8, delay=0):
    """Opacity 0/100 that switches on for each (on, off) interval; off=None stays on."""
    keys = []
    for on, off in intervals:
        keys += [(on + delay, [0]), (on + delay + ramp, [100])]
        if off:
            keys += [(off, [100]), (off + ramp, [0])]
    return anim(keys)


def add_card(m, name, img, x, y, w, enter, focus=(), info=None, radius=10, ip=0, parent=None,
             grow=1.08, extra_out=None):
    """A rounded thumbnail. `focus` intervals enlarge it, ring it in blue and show `info`."""
    s = 100 * w / TW
    k = 100 / s                                  # canvas px -> image px
    cx, cy = x + w / 2, y + TH * s / 200
    sk = [(0, [s, s])]
    for on, off in focus:
        sk += [(on, [s, s], "out"), (on + 8, [s * grow] * 2)]
        if off:
            sk += [(off, [s * grow] * 2), (off + 8, [s, s])]
    o = [(enter, [0]), (enter + 12, [100])]
    if extra_out:
        o += [(extra_out[0], [100]), (extra_out[1], [0])]
    layer = m.image(name, img, ip=ip, parent=parent, masks=[mask(rrect(0, 0, TW, TH, radius * k))],
                    ks=layer_ks(p=anim([(enter, [cx, cy + 24], "out"), (enter + 18, [cx, cy])]),
                                a=(TW / 2, TH / 2), s=anim(sk) if focus else (s, s), o=anim(o)))
    if not focus:
        return layer
    if info:
        title, genres, moods = info
        pills, _ = pill_row(moods, 18, 186, gap=8, size=17, h=30, color=MOOD, pad=12)
        m.shape(f"{name} info", bf([
            group([rect(TW, TH, TW / 2, TH / 2, radius * k), gfill(
                [(0, "#000000", 0), (0.4, "#000000", 0.25), (1, "#000000", 0.92)], (0, 40), (0, TH))]),
            BOLD.text(title, 28, 18, 144),
            REG.text(genres, 18, 18, 172, o=88),
            group(pills),
        ]), ip=ip, parent=layer, ks=layer_ks(o=on_off(focus, 8, 4)))
    m.shape(f"{name} focus", bf([
        group([rect(TW + 24 * k, TH + 24 * k, TW / 2, TH / 2, (radius + 10) * k),
               stroke(FOCUS, 10 * k, 28)]),
        group([rect(TW + 10 * k, TH + 10 * k, TW / 2, TH / 2, (radius + 4) * k), stroke(FOCUS, 4 * k)]),
    ]), ip=ip, parent=layer, ks=layer_ks(o=on_off(focus)))
    return layer


def add_nav(m, w, ip=0, o=None):
    """The Vionlabs demo nav bar, scaled to the canvas width."""
    s = 100 * w / 1920
    m.shape("nav-bg", [group([rect(1920, 76, 960, 38), fill(NAV_BG, 92)])], ip=ip,
            ks=layer_ks(s=(s, s), o=o or 100))
    m.shape("nav", bf(nav_items()), ip=ip, ks=layer_ks(s=(s, s), o=o or 100))


def add_fade(m, op, t_in=8, t_out=12):
    m.shape("fade", [group([rect(m.w, m.h, m.w / 2, m.h / 2), fill("#000000")])], ks=layer_ks(
        o=anim([(0, [100]), (t_in, [0]), (op - t_out, [0]), (op, [100])])))


def write(data, name):
    text = json.dumps(data, separators=(",", ":"))
    out = os.path.join(HERE, f"{name}{SUFFIX}.json")
    with open(out, "w") as f:
        f.write(text)
    manifest = {"version": "1.0", "generator": "build_curio.py", "author": "", "revision": 1,
                "animations": [{"id": name, "speed": 1, "loop": True, "autoplay": True,
                                "direction": 1, "playMode": "normal"}]}
    with zipfile.ZipFile(os.path.join(HERE, f"{name}{SUFFIX}.lottie"), "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr("manifest.json", json.dumps(manifest))
        z.writestr(f"animations/{name}.json", text)
    print(f"wrote {os.path.basename(out)} ({len(text) / 1024:.0f} KB)")


# ------------------------------------------------------------------- hero

HERO_PHASES = [  # (card image, backdrop, card title, hero label, title, reason icon, reason, chips)
    ("oppenheimer", "oppenheimer_bd", "Because You Watched",
     "BECAUSE YOU WATCHED INTERSTELLAR", "Oppenheimer", I_GROUP,
     "Viewers who loved Interstellar went on to watch this",
     ["intense", "thought-provoking", "historical"]),
    ("topgun", "topgun_hero", "Recommendations",
     "RECOMMENDED FOR YOU", "Top Gun: Maverick", I_SPARKLE,
     "Picked for this viewer, even on day one",
     ["high octane", "intense", "inspiring"]),
    ("arrival", "arrival_bd", "Similar Titles",
     "SIMILAR TO INTERSTELLAR", "Arrival", I_WAVE,
     "Feels like Interstellar: pacing, tone and emotional arc",
     ["thought-provoking", "emotional", "awe-inspiring"]),
]


def build_hero():
    W, H, OP = 1920, 1080, 252                  # 3 x 2.8 s, the headline's rhythm
    imgs = Images()
    m = Comp(W, H, OP, "main")
    credits = build_credits(OP, roll=1500, drift=300)
    s0, s1 = 28, 50                             # shrink into the mini-player
    mx, my, mw, mh = 92, 150, 480, 270
    mc = (mx + mw / 2, my + mh / 2)
    picks = [61, 99, 183]                       # each card lights up in its phase
    phase_end = [99, 183, None]
    card_x, card_top, card_w = [949, 1251, 1553], 836, 288

    m.shape("page-bg", [group([rect(W, H, 960, 540), fill(BG)])], ip=s0 - 2)
    for k, (_, bd, *_rest) in enumerate(HERO_PHASES):
        t_on = s0 + 2 if k == 0 else picks[k]
        m.image(f"backdrop {k}", imgs(bd), ip=t_on, op=(picks[k + 1] + 18 if k < 2 else OP),
                ks=layer_ks(p=anim([(t_on, [960, 540], "linear"), (OP, [940, 532])]), a=(480, 270),
                            s=anim([(t_on, [206, 206], "out"), (t_on + 30, [200, 200], "linear"),
                                    (OP, [206, 206])]), o=fade(t_on, t_on + 14)))
    m.shape("hero-scrims", bf([
        group([rect(W, H, 960, 540), fill("#000000", 22)]),
        group([rect(W, H, 960, 540), gfill([(0, "#000000", 0.88), (0.42, "#000000", 0.55),
                                             (0.78, "#000000", 0.05)], (0, 0), (W, 0))]),
        group([rect(W, 560, 960, 800), gfill([(0, BG, 0), (1, BG, 0.92)], (0, 520), (0, 1080))]),
    ]), ip=s0)

    # hero copy, one set per phase
    for k, (_, _, _, label, title, ic, reason, chips) in enumerate(HERO_PHASES):
        t_in = picks[k] + 3
        t_out = phase_end[k]
        op = t_out + 10 if t_out else OP

        def ks(delay):
            t = t_in + delay
            p = [(t, [0, 20], "out"), (t + 16, [0, 0])]
            o = [(t, [0]), (t + 12, [100])]
            if t_out:
                p += [(t_out, [0, 0], "in"), (t_out + 8, [0, -12])]
                o += [(t_out, [100]), (t_out + 8, [0])]
            return layer_ks(p=anim(p), o=anim(o))

        m.shape(f"hero {k}: label", [SEMI.text(label, 18, 112, 690, FOCUS, tracking=0.14)],
                ip=t_in, op=op, ks=ks(0))
        m.shape(f"hero {k}: title", [BOLD.text(title, 80, 106, 780)], ip=t_in, op=op, ks=ks(2))
        pills, _ = pill_row(chips, 112, 850, h=32, size=17, color=MOOD)
        m.shape(f"hero {k}: reason", [icon(ic, 26, 126, 822, color=FOCUS),
                                      MED.text(reason, 23, 150, 830, o=90)] + pills,
                ip=t_in, op=op, ks=ks(5))
    m.shape("hero: play", bf([
        group([rect(220, 58, 218, 939, 8), fill(BLUE)]),
        MED.text("Play now", 23, 148, 947),
        icon(I_PLAY, 28, 290, 939),
    ]), ip=s1, ks=layer_ks(p=anim([(picks[0] + 8, [0, 20], "out"), (picks[0] + 24, [0, 0])]),
                           o=fade(picks[0] + 8, picks[0] + 20)))

    # three cards, titled with the rotating headline's words; the active title brightens
    focus = [[(picks[k], phase_end[k])] for k in range(3)]
    for k in (2, 1, 0):
        name, _, label = HERO_PHASES[k][:3]
        t = 38 + 4 * k
        m.shape(f"card {k}: label", [SEMI.text(label, 22, card_x[k] + 2, 802)], ip=s0, ks=layer_ks(
            p=anim([(t, [0, 24], "out"), (t + 18, [0, 0])]),
            o=anim([(t, [0]), (t + 12, [55])] + sum(
                ([(on, [55]), (on + 8, [100])] + ([(off, [100]), (off + 8, [55])] if off else [])
                 for on, off in focus[k]), []))))
        add_card(m, f"card {k}: {name}", imgs(name), card_x[k], card_top, card_w, t, focus=focus[k],
                 radius=10, ip=s0)

    # mini-player with the credits still rolling
    bottom = my + mh
    m.shape("mini-caption", bf([
        group([rect(mw, 84, mc[0], bottom + 32, 10), fill(PANEL, 94)]),
        SEMI.text("Interstellar  ·  2014", 19, mx + 20, bottom + 32),
        REG.text("Finished  ·  Did you enjoy it?", 15, mx + 20, bottom + 56, MUTED),
        group([ellipse(38, 38, mx + 406, bottom + 37), stroke("#ffffff", 1.5, 45)]),
        icon(I_THUMB, 17, mx + 406, bottom + 37),
        group([ellipse(38, 38, mx + 452, bottom + 37), stroke("#ffffff", 1.5, 45)]),
        flip(icon(I_THUMB, 17, mx + 452, bottom + 38), mx + 452, bottom + 38),
    ]), ip=s1 - 6, ks=layer_ks(p=anim([(s1 - 4, [0, -40], "out"), (s1 + 12, [0, 0])]),
                               o=fade(s1 - 4, s1 + 10)))
    m.shape("mini-shadow", [group([rect(anim([(s0, [W + 20, H + 20], "smooth"), (s1, [mw + 20, mh + 20])]),
                                        0, anim([(s0, [960, 548], "smooth"), (s1, [mc[0], mc[1] + 8])]),
                                        0, 14), fill("#000000", 45)])],
            ip=s0, ks=layer_ks(o=fade(s0 + 4, s1)))
    m.precomp("video", credits, masks=[mask(anim([(s0, rrect(0, 0, W, H, 0), "smooth"),
                                                   (s1, rrect(0, 0, W, H, 10 * W / mw))]))],
              ks=layer_ks(p=anim([(s0, [960, 540], "smooth"), (s1, list(mc))]), a=(960, 540),
                          s=anim([(s0, [100, 100], "smooth"), (s1, [100 * mw / W] * 2)])))
    m.shape("mini-border", [group([rect(anim([(s0, [W, H], "smooth"), (s1, [mw, mh])]), 0,
                                        anim([(s0, [960, 540], "smooth"), (s1, list(mc))]), 0,
                                        anim([(s0, [0], "smooth"), (s1, [10])])),
                                   stroke("#ffffff", 1.5, 22)])], ip=s0, ks=layer_ks(o=fade(s0, s0 + 8)))

    # fixed nav + fullscreen player chrome over the credits
    m.shape("nav-scrim", [group([rect(W, 200, 960, 100), gfill(
        [(0, "#000000", 0.6), (1, "#000000", 0)], (0, 0), (0, 200))])], ip=s0)
    add_nav(m, W, ip=s0, o=fade(s0 + 2, s0 + 14))
    track_x0, track_w, cy = 136, 1504, 1026
    m.shape("player-controls", bf([
        group([rect(W, 220, 960, 970), gfill([(0, "#000000", 0), (1, "#000000", 0.8)],
                                              (0, 860), (0, 1080))]),
        group([ellipse(48, 48, 80, cy), stroke("#ffffff", 2.5)]),
        icon(I_PAUSE, 24, 80, cy),
        group([rect(track_w, 5, track_x0 + track_w / 2, cy, 2.5), fill("#ffffff", 30)]),
        group([rect(anim([(0, [track_w * 0.985, 5], "linear"), (s0, [track_w, 5])]), 0,
                    anim([(0, [track_x0 + track_w * 0.4925, cy], "linear"),
                          (s0, [track_x0 + track_w / 2, cy])]), 0, 2.5), fill(BLUE)]),
        MED.text("-00:01", 21, 1662, 1034),
    ]), op=s0 + 4, ks=layer_ks(o=fade(s0 - 8, s0 + 2, 100, 0)))

    add_fade(m, OP, 5, 14)
    markers = [(0, 84, "because-you-watched"), (84, 84, "recommendations"), (168, 84, "similar-titles")]
    write(animation(m, [credits], FPS, "Curio hero", images=imgs.assets.values(), markers=markers),
          "curio-hero")


# --------------------------------------------- section: Because You Watched

def build_because_you_watched():
    W, H, OP = 1280, 720, 180
    imgs = Images()
    m = Comp(W, H, OP, "main")
    credits = build_credits(OP, roll=900, drift=200)
    m.shape("bg", [group([rect(W, H, W / 2, H / 2), fill(BG)]),
                   group([ellipse(1100, 700, 900, 230), gfill([(0, "#1b2a46", 1), (1, BG, 0)],
                                                              (900, 230), (1450, 230), radial=True)])])
    add_nav(m, W)

    # the title that just finished, still rolling its credits
    mx, my, mw = 60, 84, 384
    mh = mw * 9 / 16
    m.precomp("interstellar credits", credits, masks=[mask(rrect(0, 0, 1920, 1080, 50))],
              ks=layer_ks(p=(mx + mw / 2, my + mh / 2), a=(960, 540), s=(20, 20), o=fade(0, 12)))
    m.shape("finished", bf([
        group([rect(mw, 3, mx + mw / 2, my + mh + 6), fill(BLUE)]),
        SEMI.text("Interstellar", 24, mx, my + mh + 40),
        REG.text("Finished", 20, mx + SEMI.width("Interstellar", 24) + 12, my + mh + 40, MUTED),
    ]), ks=layer_ks(o=fade(4, 16)))

    m.shape("viewers-pill", bf([
        group([rect(470, 52, 735, 192, 26), fill(PANEL), stroke(FOCUS, 1.5, 60)]),
        icon(I_GROUP, 28, 535, 192, color=FOCUS),
        MED.text("Viewers who loved Interstellar", 22, 557, 200),
    ]), ks=layer_ks(p=anim([(16, [0, 16], "out"), (30, [0, 0])]), o=fade(16, 28)))

    # the row they went on to watch
    row_y, cw = 445, 330
    xs = [60, 420, 780, 1140]
    names = ["oppenheimer", "martian", "topgun", "spiderverse"]
    m.shape("row-label", [MED.text("Because you watched Interstellar", 30, 60, row_y - 28)],
            ks=layer_ks(p=anim([(6, [0, 16], "out"), (22, [0, 0])]), o=fade(6, 18)))
    pick = 72
    for k in (3, 2, 1, 0):
        add_card(m, names[k], imgs(names[k]), xs[k], row_y, cw, 8 + 3 * k,
                 focus=[(pick, None)] if k == 0 else (), info=CARD_INFO.get(names[k]) if k == 0 else None)

    add_fade(m, OP)
    write(animation(m, [credits], FPS, "Curio: Because You Watched", images=imgs.assets.values()),
          "curio-because-you-watched")


# ------------------------------------- section: Personalized Recommendations

def build_personalized():
    W, H, OP = 1280, 720, 180
    imgs = Images()
    m = Comp(W, H, OP, "main")
    m.shape("bg", [group([rect(W, H, W / 2, H / 2), fill(BG)])])
    add_nav(m, W)

    # a brand-new viewer with two titles watched
    m.shape("profile", bf([
        group([rect(620, 112, 370, 136, 16), fill(PANEL), stroke("#ffffff", 1, 10)]),
        group([ellipse(68, 68, 116, 136), gfill([(0, "#3d9bff", 1), (1, "#7b5cff", 1)], (82, 102), (150, 170))]),
        icon(I_PERSON, 40, 116, 137),
        SEMI.text("New viewer", 28, 166, 128),
        REG.text("Day one  ·  2 titles watched", 21, 166, 160, MUTED),
    ]), ks=layer_ks(p=anim([(0, [0, 14], "out"), (16, [0, 0])]), o=fade(0, 12)))
    for k, name in enumerate(("interstellar", "topgun")):
        add_card(m, f"watched {name}", imgs(name), 470 + 106 * k, 108, 96, 12 + 4 * k, radius=6)
    m.shape("curio-badge", bf([
        group([rect(330, 46, 1080, 136, 23), fill("#13233f"), stroke(FOCUS, 1.5, 60)]),
        icon(I_SPARKLE, 24, 940, 136, color=FOCUS),
        MED.text("Rows picked by Curio", 21, 962, 143),
    ]), ks=layer_ks(p=anim([(20, [0, 12], "out"), (34, [0, 0])]), o=fade(20, 32)))

    # mood rows assemble
    cw = 330
    xs = [60, 420, 780, 1140]
    rows = [("Thought-Provoking Sci-Fi", 262, ["arrival", "2001", "martian", "sunshine"], 24),
            ("High-Stakes Thrills", 528, ["topgun", "oppenheimer", "spiderverse", "nohardfeelings"], 36)]
    picks = [80, 124]
    focus = {(0, 0): [(picks[0], picks[1])], (1, 0): [(picks[1], None)]}
    for r, (label, top, names, t0) in enumerate(rows):
        f = focus[(r, 0)]
        m.shape(f"row {r}: label", [MED.text(label, 28, 60, top - 26)], ks=layer_ks(
            p=anim([(t0, [0, 14], "out"), (t0 + 16, [0, 0])]), o=fade(t0, t0 + 12)))
        for k in (3, 2, 1, 0):
            add_card(m, f"row {r}: {names[k]}", imgs(names[k]), xs[k], top, cw, t0 + 4 + 3 * k,
                     focus=f if k == 0 else (), info=CARD_INFO.get(names[k]) if k == 0 else None)

    add_fade(m, OP)
    write(animation(m, [], FPS, "Curio: Personalized Recommendations", images=imgs.assets.values()),
          "curio-personalized-recommendations")


# --------------------------------------------------- section: Similar Titles

def build_similar():
    W, H, OP = 1280, 720, 180
    imgs = Images()
    m = Comp(W, H, OP, "main")
    m.shape("bg", [group([rect(W, H, W / 2, H / 2), fill(BG)])])
    m.image("title backdrop", imgs("interstellar_wide"), ks=layer_ks(
        p=anim([(0, [770, 300], "linear"), (OP, [750, 296])]), a=(480, 270),
        s=anim([(0, [125, 125], "linear"), (OP, [131, 131])]), o=fade(0, 14)))
    m.shape("backdrop-scrim", bf([
        group([rect(W, H, W / 2, H / 2), gfill([(0, BG, 1), (0.36, BG, 0.85), (0.75, BG, 0.1)],
                                                (0, 0), (W, 0))]),
        group([rect(W, 400, W / 2, 470), gfill([(0, BG, 0), (0.6, BG, 1)], (0, 300), (0, 560))]),
        group([rect(W, 220, W / 2, 610), fill(BG)]),
    ]))
    add_nav(m, W)

    # Interstellar's title page with its mood tags
    m.shape("title", [BOLD.text("Interstellar", 60, 58, 168)],
            ks=layer_ks(p=anim([(2, [0, 16], "out"), (18, [0, 0])]), o=fade(2, 14)))
    genres, _ = pill_row(["Drama", "Adventure", "Sci-Fi"], 60, 190, h=34, size=18, color=GENRE,
                         edge=GENRE_EDGE)
    m.shape("genres", genres, ks=layer_ks(p=anim([(5, [0, 16], "out"), (21, [0, 0])]), o=fade(5, 17)))
    m.shape("description", [REG.text(line, 20, 60, 262 + 28 * k, o=86) for k, line in enumerate(
        ["A team of explorers travels through a wormhole in", "search of a new home for humanity."])],
        ks=layer_ks(p=anim([(8, [0, 16], "out"), (24, [0, 0])]), o=fade(8, 20)))
    moods = ["thought-provoking", "emotional", "suspenseful", "survival"]
    mood_y = 306
    pos, x = {}, 60
    pills = []
    for t in moods:
        g, w = pill(t, x, mood_y, size=18, h=34, color=MOOD)
        pills += g
        pos[t] = (x, w)
        x += w + 8
    m.shape("moods", pills, ks=layer_ks(p=anim([(11, [0, 16], "out"), (27, [0, 0])]), o=fade(11, 23)))

    # similar titles row
    top, cw = 492, 330
    xs = [60, 420, 780, 1140]
    names = ["2001", "arrival", "martian", "sunshine"]
    m.shape("row-label", [MED.text("Similar titles", 28, 60, top - 24)],
            ks=layer_ks(p=anim([(14, [0, 14], "out"), (30, [0, 0])]), o=fade(14, 26)))
    picks = [62, 118]
    focus = {1: [(picks[0], picks[1])], 2: [(picks[1], None)]}
    shared = {1: ["thought-provoking", "emotional"], 2: ["suspenseful", "survival"]}
    for k in (3, 2, 1, 0):
        add_card(m, names[k], imgs(names[k]), xs[k], top, cw, 18 + 3 * k, focus=focus.get(k, ()),
                 info=CARD_INFO.get(names[k]) if k in focus else None)

    # the tags each highlighted title shares with Interstellar light up too
    for k, tags in shared.items():
        on, off = focus[k][0]
        for tag in tags:
            x0, w = pos[tag]
            px = x0 + w / 2
            m.shape(f"shared {tag}", bf([
                group([rect(w + 18, 52, px, mood_y + 17, 26), stroke(FOCUS, 9, 28)]),
                group([rect(w + 8, 42, px, mood_y + 17, 21), stroke(FOCUS, 3)]),
            ]), ip=on, ks=layer_ks(o=on_off([(on + 2, off)])))

    add_fade(m, OP)
    write(animation(m, [], FPS, "Curio: Similar Titles", images=imgs.assets.values()),
          "curio-similar-titles")


if __name__ == "__main__":
    build_hero()
    build_because_you_watched()
    build_personalized()
    build_similar()
