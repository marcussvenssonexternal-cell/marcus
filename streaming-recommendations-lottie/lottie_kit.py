"""Small helpers for hand-building Lottie (Bodymovin 5.x) JSON in Python.

Everything here produces plain dicts that serialise straight to Lottie JSON.
Text is converted to vector outlines (no font dependency at playback), which
keeps the animation identical across lottie-web, lottie-android and lottie-ios.
"""
import math
import re

import uharfbuzz as hb
from fontTools.pens.basePen import BasePen
from fontTools.ttLib import TTFont

# cubic-bezier(x1, y1, x2, y2) -> ((x1, y1), (x2, y2))
EASE = {
    "linear": ((0.0, 0.0), (1.0, 1.0)),
    "io": ((0.42, 0.0), (0.58, 1.0)),
    "smooth": ((0.65, 0.0), (0.35, 1.0)),
    "out": ((0.22, 1.0), (0.36, 1.0)),
    "in": ((0.55, 0.0), (1.0, 0.45)),
}


# ---------------------------------------------------------------- properties

def rgb(hex_color, alpha=1.0):
    h = hex_color.lstrip("#")
    return [round(int(h[i:i + 2], 16) / 255, 4) for i in (0, 2, 4)] + [alpha]


def _arr(v):
    return list(v) if isinstance(v, (list, tuple)) else [v]


def prop(v):
    """Static value, or pass an already-animated property through."""
    if isinstance(v, dict) and "a" in v:
        return v
    return {"a": 0, "k": v}


def anim(keys, ease="io"):
    """keys: [(t, value), (t, value, ease_of_segment_starting_here), ...].

    The ease names a segment that *starts* at that key; "hold" jumps.
    """
    out = []
    for n, key in enumerate(keys):
        t, v = key[0], key[1]
        e = key[2] if len(key) > 2 else ease
        k = {"t": t, "s": _arr(v)}
        if n < len(keys) - 1:
            if e == "hold":
                k["h"] = 1
            else:
                (ox, oy), (ix, iy) = EASE[e]
                k["o"] = {"x": ox, "y": oy}
                k["i"] = {"x": ix, "y": iy}
        out.append(k)
    return {"a": 1, "k": out}


def motion(points, ease="smooth"):
    """Position keyframes that can curve: [(t, [x, y], control_or_None), ...].

    The optional control point bends the segment that starts at that key into a
    quadratic curve (converted to Lottie's spatial tangents).
    """
    out = []
    for n, (t, p, ctrl) in enumerate(points):
        k = {"t": t, "s": list(p)}
        if n < len(points) - 1:
            (ox, oy), (ix, iy) = EASE[ease]
            k["o"] = {"x": ox, "y": oy}
            k["i"] = {"x": ix, "y": iy}
            nxt = points[n + 1][1]
            c = ctrl or p
            k["to"] = [(c[0] - p[0]) * 2 / 3, (c[1] - p[1]) * 2 / 3]
            k["ti"] = [(c[0] - nxt[0]) * 2 / 3, (c[1] - nxt[1]) * 2 / 3] if ctrl else [0, 0]
        out.append(k)
    return {"a": 1, "k": out}


def fade(t0, t1, v0=0, v1=100, ease="io"):
    return anim([(t0, v0), (t1, v1)], ease)


def layer_ks(p=(0, 0), a=(0, 0), s=(100, 100), r=0, o=100):
    return {"o": prop(o), "r": prop(r), "p": prop(list(p) if isinstance(p, tuple) else p),
            "a": prop(list(a) if isinstance(a, tuple) else a),
            "s": prop(list(s) if isinstance(s, tuple) else s)}


# -------------------------------------------------------------------- shapes

def rect(w, h, cx=0, cy=0, r=0):
    return {"ty": "rc", "d": 1, "s": prop([w, h] if not isinstance(w, dict) else w),
            "p": prop([cx, cy] if not isinstance(cx, dict) else cx), "r": prop(r)}


def ellipse(w, h, cx=0, cy=0):
    return {"ty": "el", "d": 1, "s": prop([w, h] if not isinstance(w, dict) else w),
            "p": prop([cx, cy])}


def _rnd(pts, nd=1):
    if nd == 0:
        return [[int(round(x)), int(round(y))] for x, y in pts]
    return [[round(x, nd), round(y, nd)] for x, y in pts]


def path(contour, nd=1):
    v, i, o, c = contour
    return {"ty": "sh", "d": 1,
            "ks": prop({"i": _rnd(i, nd), "o": _rnd(o, nd), "v": _rnd(v, nd), "c": c})}


def poly(points, closed=True):
    z = [(0, 0)] * len(points)
    return path((list(points), z, z, closed))


def smooth(points, closed=True, k=1.0):
    """Catmull-Rom spline through points, as one Lottie path."""
    n = len(points)
    ins, outs = [], []
    for j in range(n):
        if closed:
            p0, p2 = points[(j - 1) % n], points[(j + 1) % n]
        else:
            p0 = points[max(j - 1, 0)]
            p2 = points[min(j + 1, n - 1)]
        tx, ty = (p2[0] - p0[0]) / 6 * k, (p2[1] - p0[1]) / 6 * k
        outs.append((tx, ty))
        ins.append((-tx, -ty))
    if not closed:
        ins[0], outs[-1] = (0, 0), (0, 0)
    return path((list(points), ins, outs, closed))


def ridge(points, bottom, k=1.0):
    """Smooth skyline through `points`, closed down to y=bottom."""
    n = len(points)
    ins, outs = [], []
    for j in range(n):
        p0 = points[max(j - 1, 0)]
        p2 = points[min(j + 1, n - 1)]
        tx, ty = (p2[0] - p0[0]) / 6 * k, (p2[1] - p0[1]) / 6 * k
        outs.append((tx, ty))
        ins.append((-tx, -ty))
    v = list(points) + [(points[-1][0], bottom), (points[0][0], bottom)]
    ins += [(0, 0), (0, 0)]
    outs += [(0, 0), (0, 0)]
    ins[0] = (0, 0)
    outs[n - 1] = (0, 0)
    return path((v, ins, outs, True))


def sag_line(x1, y1, x2, y2, sag):
    dx = (x2 - x1) / 3
    return path(([(x1, y1), (x2, y2)], [(0, 0), (-dx, sag)], [(dx, sag), (0, 0)], False))


def fill(color, o=100, rule=1):
    c = rgb(color) if isinstance(color, str) else color
    return {"ty": "fl", "c": prop(c), "o": prop(o), "r": rule}


def stroke(color, w, o=100, cap=2, join=2, dash=None):
    c = rgb(color) if isinstance(color, str) else color
    s = {"ty": "st", "c": prop(c), "o": prop(o), "w": prop(w), "lc": cap, "lj": join, "ml": 4}
    if dash:
        d, g, off = dash
        s["d"] = [{"n": "d", "nm": "dash", "v": prop(d)},
                  {"n": "g", "nm": "gap", "v": prop(g)},
                  {"n": "o", "nm": "offset", "v": prop(off)}]
    return s


def gfill(stops, start, end, radial=False, o=100):
    """stops: [(pos, '#hex', alpha), ...]."""
    colors, alphas = [], []
    for pos, col, a in stops:
        colors += [pos] + rgb(col)[:3]
        alphas += [pos, a]
    k = colors if all(a == 1 for _, _, a in stops) else colors + alphas
    g = {"ty": "gf", "o": prop(o), "r": 1, "s": prop(list(start)), "e": prop(list(end)),
         "t": 2 if radial else 1, "g": {"p": len(stops), "k": prop(k)}}
    if radial:
        g["h"] = prop(0)
        g["a"] = prop(0)
    return g


def trim(s=0, e=100, o=0):
    return {"ty": "tm", "s": prop(s), "e": prop(e), "o": prop(o), "m": 1}


def group(items, p=(0, 0), a=(0, 0), s=(100, 100), r=0, o=100, nm="g"):
    tr = {"ty": "tr", "p": prop(list(p) if isinstance(p, tuple) else p),
          "a": prop(list(a) if isinstance(a, tuple) else a),
          "s": prop(list(s) if isinstance(s, tuple) else s), "r": prop(r), "o": prop(o),
          "sk": prop(0), "sa": prop(0)}
    return {"ty": "gr", "nm": nm, "it": list(items) + [tr]}


# --------------------------------------------------------------------- comps

class Comp:
    """Collects layers back-to-front; serialises top-first as Lottie expects."""

    def __init__(self, w, h, op, name):
        self.w, self.h, self.op, self.name = w, h, op, name
        self.layers = []

    def _add(self, layer, name, ip, op, ks, parent, masks=None):
        layer.update({"ddd": 0, "ind": len(self.layers) + 1, "nm": name, "sr": 1,
                      "ks": ks or layer_ks(), "ao": 0, "ip": ip,
                      "op": self.op if op is None else op, "st": 0, "bm": 0})
        if parent is not None:
            layer["parent"] = parent["ind"]
        if masks:
            layer["hasMask"] = True
            layer["masksProperties"] = masks
        self.layers.append(layer)
        return layer

    def shape(self, name, shapes, ip=0, op=None, ks=None, parent=None, masks=None):
        return self._add({"ty": 4, "shapes": list(shapes)}, name, ip, op, ks, parent, masks)

    def precomp(self, name, comp, ip=0, op=None, ks=None, parent=None, masks=None):
        return self._add({"ty": 0, "refId": comp.name, "w": comp.w, "h": comp.h},
                         name, ip, op, ks, parent, masks)

    def image(self, name, asset, ip=0, op=None, ks=None, parent=None, masks=None):
        return self._add({"ty": 2, "refId": asset["id"]}, name, ip, op, ks, parent, masks)

    def null(self, name, ip=0, op=None, ks=None, parent=None):
        return self._add({"ty": 3}, name, ip, op, ks, parent)

    def asset(self):
        return {"id": self.name, "nm": self.name, "layers": self.layers[::-1]}


def image_asset(path, aid):
    """Embed a JPEG/PNG as a base64 image asset."""
    import base64
    from PIL import Image
    with Image.open(path) as im:
        w, h = im.size
    mime = "image/png" if path.lower().endswith(".png") else "image/jpeg"
    with open(path, "rb") as f:
        data = base64.b64encode(f.read()).decode()
    return {"id": aid, "w": w, "h": h, "u": "", "p": f"data:{mime};base64,{data}", "e": 1}


def rrect(x, y, w, h, r):
    """Rounded rectangle as a raw path value (for masks or animated shapes)."""
    k = r * 0.5523
    v = [(x + r, y), (x + w - r, y), (x + w, y + r), (x + w, y + h - r), (x + w - r, y + h),
         (x + r, y + h), (x, y + h - r), (x, y + r)]
    i = [(-k, 0), (0, 0), (0, -k), (0, 0), (k, 0), (0, 0), (0, k), (0, 0)]
    o = [(0, 0), (k, 0), (0, 0), (0, k), (0, 0), (-k, 0), (0, 0), (0, -k)]
    return {"i": _rnd(i, 2), "o": _rnd(o, 2), "v": _rnd(v, 2), "c": True}


def mask(shape, mode="a", o=100):
    return {"inv": False, "mode": mode, "pt": prop(shape), "o": prop(o), "x": prop(0), "nm": "mask"}


def animation(main, precomps, fps, name, images=(), markers=()):
    """markers: [(frame, duration, name), ...] so a page can play named segments."""
    return {"v": "5.12.2", "fr": fps, "ip": 0, "op": main.op, "w": main.w, "h": main.h,
            "nm": name, "ddd": 0, "assets": list(images) + [c.asset() for c in precomps],
            "layers": main.layers[::-1],
            "markers": [{"tm": t, "dr": d, "cm": n} for t, d, n in markers]}


# ---------------------------------------------------------------------- text

class _ContourPen(BasePen):
    def __init__(self, glyph_set):
        super().__init__(glyph_set)
        self.contours = []
        self._v = self._i = self._o = None

    def _moveTo(self, p):
        self._v, self._i, self._o = [p], [(0, 0)], [(0, 0)]

    def _lineTo(self, p):
        self._v.append(p)
        self._i.append((0, 0))
        self._o.append((0, 0))

    def _curveToOne(self, p1, p2, p3):
        last = self._v[-1]
        self._o[-1] = (p1[0] - last[0], p1[1] - last[1])
        self._v.append(p3)
        self._i.append((p2[0] - p3[0], p2[1] - p3[1]))
        self._o.append((0, 0))

    def _qCurveToOne(self, p1, p2):
        p0 = self._v[-1]
        c1 = (p0[0] + 2 / 3 * (p1[0] - p0[0]), p0[1] + 2 / 3 * (p1[1] - p0[1]))
        c2 = (p2[0] + 2 / 3 * (p1[0] - p2[0]), p2[1] + 2 / 3 * (p1[1] - p2[1]))
        self._curveToOne(c1, c2, p2)

    def _closePath(self):
        v, i, o = self._v, self._i, self._o
        if len(v) > 1 and abs(v[0][0] - v[-1][0]) < 1e-6 and abs(v[0][1] - v[-1][1]) < 1e-6:
            i[0] = i[-1]
            v.pop(), i.pop(), o.pop()
        self.contours.append((v, i, o))

    _endPath = _closePath


class Font:
    def __init__(self, path):
        self.tt = TTFont(path)
        self.glyphs = self.tt.getGlyphSet()
        self.order = self.tt.getGlyphOrder()
        self.upem = self.tt["head"].unitsPerEm
        self.hb = hb.Font(hb.Face(hb.Blob.from_file_path(path)))
        self._cache = {}

    def _outline(self, gid):
        if gid not in self._cache:
            pen = _ContourPen(self.glyphs)
            self.glyphs[self.order[gid]].draw(pen)
            self._cache[gid] = pen.contours
        return self._cache[gid]

    def _shape(self, text):
        buf = hb.Buffer()
        buf.add_str(text)
        buf.guess_segment_properties()
        hb.shape(self.hb, buf, {"kern": True, "liga": True})
        return [(i.codepoint, p.x_offset, p.y_offset, p.x_advance)
                for i, p in zip(buf.glyph_infos, buf.glyph_positions)]

    def width(self, text, size, tracking=0.0):
        run = self._shape(text)
        sc = size / self.upem
        return sum(g[3] for g in run) * sc + tracking * size * max(len(run) - 1, 0)

    def paths(self, text, size, x, y, align="left", tracking=0.0, nd=1):
        """Glyph outlines as Lottie paths; (x, y) is the baseline anchor.

        nd is the coordinate precision; 0 halves the size of text that is only
        ever seen small."""
        sc = size / self.upem
        if align != "left":
            w = self.width(text, size, tracking)
            x -= w if align == "right" else w / 2
        out, pen_x = [], 0.0
        for gid, xo, yo, adv in self._shape(text):
            ox, oy = x + (pen_x + xo) * sc, y - yo * sc
            for v, i, o in self._outline(gid):
                out.append(path(([(ox + px * sc, oy - py * sc) for px, py in v],
                                 [(tx * sc, -ty * sc) for tx, ty in i],
                                 [(tx * sc, -ty * sc) for tx, ty in o], True), nd=nd))
            pen_x += adv + tracking * size / sc
        return out

    def text(self, text, size, x, y, color="#ffffff", o=100, align="left", tracking=0.0,
             nm=None, nd=1):
        return group(self.paths(text, size, x, y, align, tracking, nd) + [fill(color, o)],
                     nm=nm or "txt:" + text[:24])


# ---------------------------------------------------------------- svg paths

_TOK = re.compile(r"[MmLlHhVvCcSsQqTtZz]|[-+]?(?:\d+\.?\d*|\.\d+)(?:[eE][-+]?\d+)?")


def svg_path(d, scale=1.0, dx=0.0, dy=0.0):
    """Parse an SVG path (no arcs) into Lottie paths, scaled then offset."""
    toks = _TOK.findall(d)
    contours = []
    cur = None
    x = y = sx = sy = 0.0
    last_c2 = None
    cmd = None
    i = 0

    def num():
        nonlocal i
        v = float(toks[i])
        i += 1
        return v

    def begin(px, py):
        nonlocal cur
        if cur is not None:
            contours.append((cur, False))
        cur = ([(px, py)], [(0, 0)], [(0, 0)])

    def line(px, py):
        cur[0].append((px, py))
        cur[1].append((0, 0))
        cur[2].append((0, 0))

    def cubic(c1, c2, p):
        lx, ly = cur[0][-1]
        cur[2][-1] = (c1[0] - lx, c1[1] - ly)
        cur[0].append(p)
        cur[1].append((c2[0] - p[0], c2[1] - p[1]))
        cur[2].append((0, 0))

    def close():
        nonlocal cur
        v, ii, oo = cur
        if len(v) > 1 and abs(v[0][0] - v[-1][0]) < 1e-6 and abs(v[0][1] - v[-1][1]) < 1e-6:
            ii[0] = ii[-1]
            v.pop(), ii.pop(), oo.pop()
        contours.append((cur, True))
        cur = None

    while i < len(toks):
        if toks[i].isalpha():
            cmd = toks[i]
            i += 1
            if cmd in "Zz":
                close()
                x, y = sx, sy
                last_c2 = None
                continue
        rel = cmd.islower()
        c = cmd.upper()
        bx, by = (x, y) if rel else (0.0, 0.0)
        if c == "M":
            x, y = bx + num(), by + num()
            sx, sy = x, y
            begin(x, y)
            cmd = "l" if rel else "L"
            last_c2 = None
        elif c == "L":
            x, y = bx + num(), by + num()
            line(x, y)
            last_c2 = None
        elif c == "H":
            x = bx + num()
            line(x, y)
            last_c2 = None
        elif c == "V":
            y = (y if rel else 0.0) + num()
            line(x, y)
            last_c2 = None
        elif c == "C":
            c1 = (bx + num(), by + num())
            c2 = (bx + num(), by + num())
            x, y = bx + num(), by + num()
            cubic(c1, c2, (x, y))
            last_c2 = c2
        elif c == "S":
            c1 = (2 * x - last_c2[0], 2 * y - last_c2[1]) if last_c2 else (x, y)
            c2 = (bx + num(), by + num())
            x, y = bx + num(), by + num()
            cubic(c1, c2, (x, y))
            last_c2 = c2
        elif c == "Q":
            q = (bx + num(), by + num())
            p0 = (x, y)
            x, y = bx + num(), by + num()
            cubic((p0[0] + 2 / 3 * (q[0] - p0[0]), p0[1] + 2 / 3 * (q[1] - p0[1])),
                  (x + 2 / 3 * (q[0] - x), y + 2 / 3 * (q[1] - y)), (x, y))
            last_c2 = None
        else:
            raise ValueError("unsupported path command " + cmd)
    if cur is not None:
        contours.append((cur, False))

    out = []
    for (v, ii, oo), closed in contours:
        out.append(path(([(dx + px * scale, dy + py * scale) for px, py in v],
                         [(tx * scale, ty * scale) for tx, ty in ii],
                         [(tx * scale, ty * scale) for tx, ty in oo], closed), nd=2))
    return out


def icon(d, size, cx, cy, color="#ffffff", o=100, nm="icon"):
    """A 24x24 Material-style icon path, centred on (cx, cy) at `size` px."""
    sc = size / 24
    return group(svg_path(d, sc, cx - 12 * sc, cy - 12 * sc) + [fill(color, o, rule=2)], nm=nm)


def deg(a):
    return math.radians(a)
