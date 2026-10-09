"""Shared pieces of the Vionlabs / Curio demo UI used by the Lottie build scripts.

Fonts, palette, Material icons, pills, the Vionlabs nav bar, the Interstellar
end-credits scene and rounded thumbnail layers.
"""
import os
import random

from lottie_kit import Font, anim, ellipse, fill, group, icon, layer_ks, mask, rect, rrect, stroke, Comp

W, H = 1920, 1080                   # the credits scene is always full HD
FONT_DIR = os.environ.get("INTER_DIR", "/usr/share/fonts/opentype/inter")
LIGHT = Font(f"{FONT_DIR}/Inter-Light.otf")
REG = Font(f"{FONT_DIR}/Inter-Regular.otf")
MED = Font(f"{FONT_DIR}/Inter-Medium.otf")
SEMI = Font(f"{FONT_DIR}/Inter-SemiBold.otf")
BOLD = Font(f"{FONT_DIR}/Inter-Bold.otf")
BLACK = Font(f"{FONT_DIR}/Inter-Black.otf")

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



def build_credits(op, roll=1720, drift=520):
    c = Comp(W, H, op, "comp_credits")
    c.shape("black", [group([rect(W, H, 960, 540), fill("#000000")])])
    rng = random.Random(4)
    stars = [ellipse(s, s, rng.uniform(0, W), rng.uniform(-100, 1700))
             for s in [rng.choice((1.5, 2, 2, 2.5, 3)) for _ in range(120)]]
    c.shape("stars", [group(stars + [fill("#ffffff", 45)])],
            ks=layer_ks(p=anim([(0, [0, 0], "linear"), (op, [0, -drift])])))
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
    c.shape("credits", items, ks=layer_ks(p=anim([(0, [0, 0], "linear"), (op, [0, -roll])])))
    return c



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



def card_image(m, name, img, scale, radius, ks_extra, parent, ip):
    """A rounded thumbnail as an image layer (no precomp needed)."""
    ks = layer_ks(a=(TW / 2, TH / 2), s=scale, **ks_extra)
    return m.image(name, img, ip=ip, parent=parent, ks=ks,
                   masks=[mask(rrect(0, 0, TW, TH, radius))])
