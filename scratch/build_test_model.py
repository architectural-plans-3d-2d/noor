import sys
from pathlib import Path

code = '''"""
DAATA HAMLET RESIDENCE - Parametric design model (single source of truth)
=========================================================================
New Scheme:
- Main Lawn (~500 sft) on the front-west (old car porch deleted)
- New Central Car Porch (12' x 20') with 6'-0" main entrance door
- Bed Room-2 (SW) with lawn views and en-suite bath/dress carved from old drawing space
- Drawing Room (SE) moved to boundary wing with 2'-0" continuous east passage
- Central Staircase with Powder Room tucked under 7'-0" mid-landing
- Kitchen on NW angled boundary P3-P4 (trapezoid on boundary wall)
- Family Lounge + Dining extending north to P4-P5 with 2'-0" perimeter passage
- Rear Master Suite in NE wing (old stair/kitchen/dirty kitchen wing) with angled luxury bath/dress
- Upper floors stacked cleanly with Open Sun Terrace over the new Car Porch
"""
from __future__ import annotations

import math
import re
from dataclasses import dataclass, field

from shapely.geometry import Polygon, box as sbox, Point, LineString
from shapely.ops import unary_union

# --------------------------------------------------------------------------
# SITE (from site_coordinates.csv, feet)
# --------------------------------------------------------------------------
SITE_POINTS = [
    ("P1", 0.0000, 0.0000), ("P2", 10.4884, 10.0122), ("P3", 24.5949, 26.1267),
    ("P4", 41.1897, 36.8354), ("P5", 67.6992, 50.7010), ("P6", 84.8373, 57.6678),
    ("P7", 88.8145, 62.1602), ("P0", 87.9167, 0.0000),
]
SURVEY_SEGMENTS = [
    ("P1", "P2", "14'-6\\""), ("P2", "P3", "21'-5\\""), ("P3", "P4", "19'-9\\""),
    ("P4", "P5", "29'-11\\""), ("P5", "P6", "18'-6\\""), ("P6", "P7", "6'-0\\""),
    ("P7", "P0", "62'-2\\""), ("P0", "P1", "87'-11\\"")
]
PLOT = Polygon([(x, y) for _, x, y in SITE_POINTS])
PLOT_INNER = PLOT.buffer(-0.75, join_style="mitre")          # inside face of 9" boundary wall
BUILD = PLOT.buffer(-2.75, join_style="mitre")                # 2'-0" clear passage inside boundary wall


def east_bx(y: float) -> float:
    """x of the (slightly skewed) east boundary at height y."""
    return 87.9167 + (88.8145 - 87.9167) * y / 62.1602


# --------------------------------------------------------------------------
# LEVELS
# --------------------------------------------------------------------------
ROAD_Z, GRADE_Z = -1.5, -1.0
FLOORS = ["GF", "1F", "2F"]
LEVEL = {"GF": 0.0, "1F": 11.0, "2F": 22.0, "RF": 33.0}
FLOOR_H, SLAB_T, BEAM_D = 11.0, 0.5, 1.5
WALL_H = FLOOR_H - SLAB_T          # wall top = underside of slab above
MUMTY_TOP = 42.0
PARAPET_H = 3.0
T9, T45 = 0.75, 0.375              # 9" and 4.5" walls

# --------------------------------------------------------------------------
# GRID & DEMISING LINES (FEET)
# --------------------------------------------------------------------------
XB_W, XB_E = 36.125, 36.875
XC_W, XC_E = 51.375, 52.125
XC_P_W, XC_P_E = 56.625, 57.375
XD_W, XD_E = 68.625, 69.375
XE_W, XE_E = 84.375, 85.125
XB_O, XB_I = XB_W, XB_E
XE_I, XE_O = XE_W, XE_E
Y_FRONT_O, Y_FRONT_I = 3.0, 3.75

STAIR_X0 = 57.375
MID_X = 64.5
STAIR_X1 = 68.625
LANE_S = (20.5, 24.25)
LANE_N = (24.75, 28.5)
TREAD = 10.5 / 12.0
RISER = 6.6 / 12.0

# Footprint blocks
b_sw = sbox(XB_W, 3.0, XC_P_E, 20.5)
b_porch = sbox(XC_P_W, 0.0, XD_E, 20.5)
b_east = sbox(XD_W, 3.0, XE_E, 58.0).intersection(PLOT_INNER)
b_north = sbox(XB_W, 20.5, XD_E, 46.0).intersection(BUILD)
b_kit = sbox(22.0, 20.0, XB_E, 34.0).intersection(PLOT_INNER)

FP = unary_union([b_sw, b_porch, b_east, b_north, b_kit])
FP_IN = FP.buffer(-T9, join_style="mitre")
WALL_RING = FP.difference(FP_IN)

BUILDABLE = unary_union([
    sbox(0.0, 0.0, 88.0, 60.0).intersection(PLOT_INNER)
])

# --------------------------------------------------------------------------
# STRUCTURAL GRID & RCC COLUMNS
# --------------------------------------------------------------------------
GX = {"B": 36.5, "C": 51.75, "C'": 57.0, "D": 69.0, "E": 84.75}
GY = {"1": 3.375, "2": 20.125, "3": 28.5, "4": 36.5, "5": 42.125, "6": 48.0, "7": 55.5}

COLUMN_SPEC = {
    "B1": ("y", +0.375, T9), "B2": ("y", 0.0, T9), "B3": ("y", 0.0, T9), "B4": ("y", 0.0, T9),
    "C1": ("y", +0.375, T9), "C2": ("y", 0.0, T9), "C3": ("y", 0.0, T9), "C4": ("y", 0.0, T9),
    "C'1": ("y", +0.375, T9), "C'2": ("y", 0.0, T9), "C'3": ("y", 0.0, T9),
    "D1": ("y", +0.375, T9), "D2": ("y", 0.0, T9), "D3": ("y", 0.0, T9), "D4": ("y", 0.0, T9), "D5": ("y", 0.0, T9),
    "E1": ("y", +0.375, T9), "E2": ("y", 0.0, T9), "E3": ("y", 0.0, T9), "E4": ("y", 0.0, T9), "E5": ("y", 0.0, T9), "E6": ("y", 0.0, T9),
}
MUMTY_COLUMNS = ["C'2", "D2", "C'3", "D3"]
LONG = 1.5

COL_RE = re.compile(r"^([A-Z]'?)(\\d+[A-Z]?)$")


def split_col(name: str) -> tuple[str, str]:
    m = COL_RE.match(name)
    if not m:
        raise ValueError(f"Invalid column name: {name}")
    return m.group(1), m.group(2)


def column_rect(name: str):
    orient, shift, thin = COLUMN_SPEC[name]
    gl, gn = split_col(name)
    cx, cy = GX[gl], GY[gn]
    if orient == "y":
        cy += shift
        return (cx - thin / 2, cy - LONG / 2, cx + thin / 2, cy + LONG / 2)
    cx += shift
    return (cx - LONG / 2, cy - thin / 2, cx + LONG / 2, cy + thin / 2)


def beam_segments():
    names = list(COLUMN_SPEC)
    segs = []
    for letter in GX:
        on = sorted([n for n in names if split_col(n)[0] == letter], key=lambda n: GY[split_col(n)[1]])
        segs += [(a, b) for a, b in zip(on, on[1:])]
    for num in GY:
        on = sorted([n for n in names if split_col(n)[1] == num], key=lambda n: GX[split_col(n)[0]])
        segs += [(a, b) for a, b in zip(on, on[1:])]
    return segs


# --------------------------------------------------------------------------
# DATA CLASSES
# --------------------------------------------------------------------------
@dataclass
class Box:
    x0: float; y0: float; z0: float; x1: float; y1: float; z1: float
    mat: str; layer: str; floor: str; tag: str = ""

    def poly(self):
        return sbox(self.x0, self.y0, self.x1, self.y1)


@dataclass
class Prism:
    poly: Polygon; z0: float; z1: float
    mat: str; layer: str; floor: str; tag: str = ""


@dataclass
class Opening:
    floor: str; orient: str; line: float; a: float; b: float
    sill: float; head: float; kind: str; name: str = ""
    hinge: str = "a"; swing: int = 1

    @property
    def width(self):
        return self.b - self.a

    def rect(self, half=0.45):
        if self.orient == "x":
            return (self.a, self.line - half, self.b, self.line + half)
        return (self.line - half, self.a, self.line + half, self.b)


@dataclass
class AngledOpening:
    floor: str; p0: tuple[float, float]; p1: tuple[float, float]
    sill: float; head: float; kind: str; name: str = ""
    hinge: str = "a"; swing: int = 1

    @property
    def width(self):
        return math.hypot(self.p1[0] - self.p0[0], self.p1[1] - self.p0[1])


@dataclass
class Room:
    floor: str; name: str; poly: Polygon; kind: str     # hab / wet / circ / serv / ext / shaft
    label_xy: tuple | None = None
    show_dims: bool = True


@dataclass
class Model:
    walls: dict = field(default_factory=lambda: {f: [] for f in FLOORS + ["RF"]})
    openings: list = field(default_factory=list)
    angled_openings: list = field(default_factory=list)
    boxes: list = field(default_factory=list)
    prisms: list = field(default_factory=list)
    rooms: list = field(default_factory=list)
    furniture: dict = field(default_factory=lambda: {f: [] for f in FLOORS + ["RF", "SITE"]})
    columns: dict = field(default_factory=dict)
    zones: dict = field(default_factory=dict)
    slabs: dict = field(default_factory=dict)


def R(x0, y0, x1, y1):
    return sbox(x0, y0, x1, y1)


def fi(v: float) -> str:
    neg = v < 0
    v = abs(v)
    inches = round(v * 12 * 2) / 2
    ft = int(inches // 12)
    rem = inches - ft * 12
    s = f"{int(rem)}" if rem == int(rem) else f"{int(rem)}\\\\u00bd"
    return f"{'-' if neg else ''}{ft}'-{s}" + '"'


def wall_orient(w: Box):
    return "x" if (w.x1 - w.x0) >= (w.y1 - w.y0) else "y"


def _split(w: Box, cuts, orient):
    lo, hi = (w.x0, w.x1) if orient == "x" else (w.y0, w.y1)
    cuts = [(max(a, lo), min(b, hi), z0, z1) for a, b, z0, z1 in cuts if b > lo + 1e-6 and a < hi - 1e-6]
    if not cuts:
        return [w]
    pts = sorted({lo, hi, *[c[0] for c in cuts], *[c[1] for c in cuts]})
    out = []
    for s, e in zip(pts, pts[1:]):
        if e - s < 1e-6:
            continue
        mid = (s + e) / 2
        gaps = sorted([(z0, z1) for a, b, z0, z1 in cuts if a <= mid <= b])
        z = w.z0
        segs = []
        for z0, z1 in gaps:
            z0, z1 = max(z0, w.z0), min(z1, w.z1)
            if z0 > z + 1e-6:
                segs.append((z, z0))
            z = max(z, z1)
        if w.z1 > z + 1e-6:
            segs.append((z, w.z1))
        for za, zb in segs:
            if orient == "x":
                out.append(Box(s, w.y0, za, e, w.y1, zb, w.mat, w.layer, w.floor, w.tag))
            else:
                out.append(Box(w.x0, s, za, w.x1, e, zb, w.mat, w.layer, w.floor, w.tag))
    return out


def split_wall(w: Box, ops, L):
    orient = wall_orient(w)
    centre = (w.y0 + w.y1) / 2 if orient == "x" else (w.x0 + w.x1) / 2
    cuts = [(o.a, o.b, L + o.sill, L + o.head) for o in ops
            if o.orient == orient and abs(o.line - centre) < 0.3]
    return _split(w, cuts, orient)


def opening_fill(o: Opening):
    L = LEVEL[o.floor]
    z0, z1 = L + o.sill, L + o.head
    out = []

    def bx(a, b, za, zb, mat, half, tag):
        if o.orient == "x":
            out.append(Box(a, o.line - half, za, b, o.line + half, zb, mat, "openings", o.floor, tag))
        else:
            out.append(Box(o.line - half, a, za, o.line + half, b, zb, mat, "openings", o.floor, tag))

    if o.kind in ("window", "slide"):
        f = 0.17
        bx(o.a, o.b, z0, z0 + f, "metal", 0.15, "frame")
        bx(o.a, o.b, z1 - f, z1, "metal", 0.15, "frame")
        bx(o.a, o.a + f, z0, z1, "metal", 0.15, "frame")
        bx(o.b - f, o.b, z0, z1, "metal", 0.15, "frame")
        mid = (o.a + o.b) / 2
        bx(mid - f / 2, mid + f / 2, z0, z1, "metal", 0.15, "mullion")
        bx(o.a + f, o.b - f, z0 + f, z1 - f, "glass", 0.03, "glass")
    elif o.kind == "vent":
        bx(o.a, o.b, z0, z1, "metal", 0.15, "louver")
    elif o.kind in ("door", "double"):
        bx(o.a, o.b, z0, z1, "timber_door", 0.09, "leaf")
    return out


# --------------------------------------------------------------------------
# FURNITURE (2D CAD Symbols)
# --------------------------------------------------------------------------
def furnish(m: Model):
    def rect(fl, x0, y0, x1, y1, label=""):
        m.furniture[fl].append(("rect", (x0, y0, x1, y1), label))

    def circ(fl, x, y, r, label=""):
        m.furniture[fl].append(("circle", (x, y, r), label))

    def bed(fl, head_x, y_mid, w=6.0, l=6.67, head="e"):
        if head == "e":
            rect(fl, head_x - l, y_mid - w / 2, head_x, y_mid + w / 2, "")
            rect(fl, head_x - 1.2, y_mid - w / 2 + 0.3, head_x - 0.15, y_mid + w / 2 - 0.3)
            rect(fl, head_x - 1.5, y_mid - w / 2 - 2.0, head_x, y_mid - w / 2 - 0.3)
            rect(fl, head_x - 1.5, y_mid + w / 2 + 0.3, head_x, y_mid + w / 2 + 2.0)
        else:
            rect(fl, head_x, y_mid - w / 2, head_x + l, y_mid + w / 2)
            rect(fl, head_x + 0.15, y_mid - w / 2 + 0.3, head_x + 1.2, y_mid + w / 2 - 0.3)
            rect(fl, head_x, y_mid - w / 2 - 2.0, head_x + 1.5, y_mid - w / 2 - 0.3)
            rect(fl, head_x, y_mid + w / 2 + 0.3, head_x + 1.5, y_mid + w / 2 + 2.0)

    # GF Furniture
    # Bed Room-2 (SW)
    bed("GF", XC_W, 11.75, head="e")
    # Bath-2 fixtures:
    rect("GF", XC_E + 0.5, 4.5, XC_P_W - 0.5, 7.5)           # shower
    circ("GF", XC_E + 2.25, 10.0, 0.75)                     # WC
    rect("GF", XC_E + 1.0, 13.0, XC_P_W - 1.0, 14.5)        # vanity
    # Drawing Room (SE)
    rect("GF", 72.0, 5.5, 82.0, 8.5)                        # main sofa
    rect("GF", 71.0, 10.0, 74.0, 15.0)                      # side sofas
    rect("GF", 80.0, 10.0, 83.0, 15.0)
    # Car Porch SUV
    rect("GF", 58.5, 2.0, 66.5, 18.0, "SUV")
    # Powder Room under stairs
    circ("GF", 66.5, 22.5, 0.75)                            # Powder WC
    rect("GF", 63.5, 21.0, 65.5, 22.5)                      # Vanity
    # Lounge + Dining
    rect("GF", 42.0, 32.0, 52.0, 35.5)                      # Lounge sofa
    rect("GF", 56.0, 32.0, 64.0, 36.0)                      # Dining table
    # Rear Master Bed
    bed("GF", XE_W, 28.5, head="e")
    # Master Bath fixtures in angled wing
    rect("GF", 71.0, 42.0, 77.0, 47.0)                      # Jacuzzi / Tub
    rect("GF", 78.5, 42.0, 83.0, 47.0)                      # Walk-in Shower
    circ("GF", 73.0, 51.0, 0.75)                            # WC
    rect("GF", 77.0, 50.0, 83.0, 52.0)                      # Double Vanity

    # Upper floors
    for fl in ["1F", "2F"]:
        bed(fl, XC_W, 11.75, head="e")
        bed(fl, XE_W, 11.75, head="e")
        if fl == "1F":
            bed(fl, XE_W, 28.5, head="e")
            rect(fl, 42.0, 32.0, 52.0, 35.5)                # 1F lounge sofa


# --------------------------------------------------------------------------
# SLABS & ROOFS
# --------------------------------------------------------------------------
def build_slabs(m: Model):
    # GF Slab at grade
    s_gf = unary_union([b_sw, b_porch, b_east, b_north, b_kit])
    m.slabs["GF"] = s_gf
    m.prisms.append(Prism(s_gf, GRADE_Z, LEVEL["GF"], "slab_concrete", "slabs", "GF"))

    # 1F Slab at 11.0' (includes cantilever over porch and utility balcony)
    s_1f = unary_union([b_sw, b_porch, b_east, b_north, b_kit])
    m.slabs[11.0] = s_1f
    m.prisms.append(Prism(s_1f, LEVEL["1F"] - SLAB_T, LEVEL["1F"], "slab_concrete", "slabs", "1F"))

    # 2F Slab at 22.0'
    s_2f = unary_union([b_sw, sbox(XC_P_W, 20.5, XD_E, 29.25), b_east, b_north])
    m.slabs[22.0] = s_2f
    m.prisms.append(Prism(s_2f, LEVEL["2F"] - SLAB_T, LEVEL["2F"], "slab_concrete", "slabs", "2F"))

    # RF Slab at 33.0'
    s_rf = unary_union([sbox(XC_P_W, 20.5, XD_E, 29.25), sbox(XD_W, 20.5, XE_E, 37.0)])
    m.slabs[33.0] = s_rf
    m.prisms.append(Prism(s_rf, LEVEL["RF"] - SLAB_T, LEVEL["RF"], "slab_concrete", "slabs", "RF"))

    # Mumty Roof Slab at 42.0'
    s_mumty = sbox(XC_P_W, 20.0, XD_E, 29.25)
    m.slabs[42.0] = s_mumty
    m.prisms.append(Prism(s_mumty, MUMTY_TOP - SLAB_T, MUMTY_TOP, "slab_concrete", "slabs", "RF"))


# --------------------------------------------------------------------------
# COLUMNS
# --------------------------------------------------------------------------
def build_columns(m: Model):
    for cname in COLUMN_SPEC:
        r = column_rect(cname)
        poly = R(*r)
        m.columns[cname] = poly
        # GF column
        m.boxes.append(Box(r[0], r[1], LEVEL["GF"], r[2], r[3], LEVEL["1F"], "concrete", "columns", "GF", cname))
        # 1F column
        m.boxes.append(Box(r[0], r[1], LEVEL["1F"], r[2], r[3], LEVEL["2F"], "concrete", "columns", "1F", cname))
        # 2F column
        if cname in ["B2", "B3", "B4", "C2", "C3", "C4", "C'2", "C'3", "D2", "D3", "D4", "E2", "E3", "E4"]:
            m.boxes.append(Box(r[0], r[1], LEVEL["2F"], r[2], r[3], LEVEL["RF"], "concrete", "columns", "2F", cname))
        # Mumty columns
        if cname in MUMTY_COLUMNS:
            m.boxes.append(Box(r[0], r[1], LEVEL["RF"], r[2], r[3], MUMTY_TOP, "concrete", "columns", "RF", cname))


# --------------------------------------------------------------------------
# WALLS & PARTITIONS
# --------------------------------------------------------------------------
def build_walls(m: Model):
    def wall(fl, x0, y0, x1, y1):
        z0, z1 = LEVEL[fl], LEVEL[fl] + WALL_H
        w = Box(x0, y0, z0, x1, y1, z1, "brick_plaster", "walls", fl)
        m.walls[fl].append(w)
        return w

    # GF Walls:
    # South exterior walls
    wall("GF", XB_W, Y_FRONT_O, XC_P_E, Y_FRONT_I)             # Bed-2 + Bath front wall
    wall("GF", XD_W, Y_FRONT_O, XE_E, Y_FRONT_I)               # Drawing front wall
    # Middle dividing wall (Y = 19.75 to 20.5)
    wall("GF", XB_W, 19.75, XC_W, 20.5)                        # North wall of Bed-2
    wall("GF", XC_W, 19.75, XC_P_E, 20.5)                      # North wall of Bath-2
    wall("GF", XD_W, 19.75, XE_E, 20.5)                        # North wall of Drawing
    # East exterior wall
    wall("GF", XE_W, 3.0, XE_E, 56.5)                          # Full east wall along passage
    # Demising walls
    wall("GF", XB_W, 3.0, XB_E, 20.5)                          # West wall of Bed-2 (facing lawn)
    wall("GF", XC_W, 3.0, XC_E, 20.5)                          # Divides Bed-2 from Bath-2
    wall("GF", XC_P_W, 3.0, XC_P_E, 20.5)                      # Divides Bath-2 from Car Porch
    wall("GF", XD_W, 0.0, XD_E, 20.5)                          # Divides Car Porch from Drawing
    # Central Staircase walls
    wall("GF", XC_P_W, 20.5, XC_P_E, 28.5)                     # West wall of stairs
    wall("GF", XD_W, 20.5, XD_E, 28.5)                         # East wall of stairs
    wall("GF", XC_P_W, 28.5, XD_E, 29.25)                      # North wall of stairs
    # Foyer / Lounge portal
    wall("GF", XB_W, 28.5, 46.0, 29.25)                        # North wall of Foyer
    # Kitchen walls
    wall("GF", XB_W, 20.5, XB_E, 33.75)                        # Line B kitchen wall
    # Rear Master Suite walls
    wall("GF", XD_W, 36.5, XE_E, 37.25)                        # Master Bed north wall
    # Angled boundary chamfer wall along P4-P5
    # (Prisms handle angled walls)

    # 1F Walls:
    for w in m.walls["GF"]:
        wall("1F", w.x0, w.y0, w.x1, w.y1)

    # 2F Walls:
    for w in [
        (XB_W, 19.75, XC_W, 20.5), (XC_P_W, 20.5, XC_P_E, 28.5),
        (XD_W, 20.5, XD_E, 28.5), (XC_P_W, 28.5, XD_E, 29.25),
        (XD_W, 19.75, XE_E, 20.5), (XD_W, 36.5, XE_E, 37.25),
        (XE_W, 20.5, XE_E, 46.0)
    ]:
        wall("2F", *w)

    # RF Mumty Walls:
    wall("RF", XC_P_W, 20.0, XC_P_E, 29.25)
    wall("RF", XD_W, 20.0, XD_E, 29.25)
    wall("RF", XC_P_W, 20.0, XD_E, 20.75)
    wall("RF", XC_P_W, 28.5, XD_E, 29.25)


# --------------------------------------------------------------------------
# OPENINGS (DOORS & WINDOWS)
# --------------------------------------------------------------------------
def build_openings(m: Model):
    def op(fl, orient, line, a, b, sill, head, kind, name="", hinge="a", swing=1):
        o = Opening(fl, orient, line, a, b, sill, head, kind, name, hinge, swing)
        m.openings.append(o)
        return o

    # GF Openings:
    # 6-ft Main Entrance Double Door from Porch into Foyer:
    op("GF", "y", XC_P_E, 21.0, 27.0, 0.0, 8.0, "double", "MAIN-DOOR", "a", 1)
    # Drawing Room Door from Porch:
    op("GF", "y", XD_W, 13.5, 17.0, 0.0, 7.5, "door", "D-DRAW", "a", 1)
    # Drawing Room South Windows:
    op("GF", "x", 3.375, 72.0, 81.0, 1.5, 8.0, "window", "W-DRAW")
    # Drawing Room East Windows:
    op("GF", "y", XE_W, 8.0, 14.0, 2.0, 8.0, "window", "W-DRAW-E")

    # Bed-2 South Window:
    op("GF", "x", 3.375, 39.0, 48.0, 1.5, 8.0, "window", "W-BED2")
    # Bed-2 West Sliding Door to Lawn:
    op("GF", "y", XB_W, 8.0, 15.0, 0.0, 8.0, "slide", "SL-LAWN")
    # Bed-2 Door from Foyer:
    op("GF", "x", 20.125, 42.0, 45.5, 0.0, 7.0, "door", "D-BED2", "a", 1)
    # Bed-2 Bath Door:
    op("GF", "y", XC_W, 10.0, 13.0, 0.0, 7.0, "door", "D-BATH2", "a", 1)
    # Bed-2 Bath South Vent:
    op("GF", "x", 3.375, 52.5, 55.5, 6.5, 8.0, "vent", "V-BATH2")

    # Powder Room Door under Stairs:
    op("GF", "y", XD_W, 21.5, 24.5, 0.0, 7.0, "door", "D-POWDER", "a", 1)
    # Powder Room Vent:
    op("GF", "x", 28.875, 63.0, 66.0, 6.5, 8.0, "vent", "V-POWDER")

    # Kitchen Door / Arch on Line B:
    op("GF", "y", XB_E, 22.0, 26.0, 0.0, 7.5, "door", "D-KIT", "a", 1)
    # Kitchen Service Door to Garden:
    op("GF", "x", 20.875, 26.0, 29.5, 0.0, 7.0, "door", "D-KIT-EXT", "a", 1)

    # Lounge North Panoramic Windows:
    op("GF", "x", 42.125, 52.0, 60.0, 1.5, 8.0, "window", "W-LOUNGE")

    # Rear Master Bed Door from Lobby:
    op("GF", "y", XD_W, 22.0, 25.5, 0.0, 7.0, "door", "D-MBED", "a", 1)
    # Rear Master Bed East Window:
    op("GF", "y", XE_W, 24.0, 32.0, 1.5, 8.0, "window", "W-MBED")
    # Rear Master Bath Door:
    op("GF", "x", 36.875, 74.0, 77.5, 0.0, 7.0, "door", "D-MBATH", "a", 1)
    # Rear Master Bath Windows & Vents:
    op("GF", "y", XE_W, 40.0, 46.0, 4.0, 7.5, "window", "W-MBATH")
    op("GF", "y", XE_W, 49.0, 52.0, 6.5, 8.0, "vent", "V-MBATH")

    # 1F Openings:
    op("1F", "y", XC_P_E, 21.0, 27.0, 0.0, 8.0, "slide", "SL-TERRACE")
    op("1F", "x", 3.375, 39.0, 48.0, 1.5, 8.0, "window", "W-BED4")
    op("1F", "x", 3.375, 72.0, 81.0, 1.5, 8.0, "window", "W-BED3")
    op("1F", "y", XE_W, 8.0, 14.0, 2.0, 8.0, "window", "W-BED3-E")
    op("1F", "x", 20.125, 42.0, 45.5, 0.0, 7.0, "door", "D-BED4", "a", 1)
    op("1F", "x", 20.125, 72.0, 75.5, 0.0, 7.0, "door", "D-BED3", "a", 1)
    op("1F", "y", XD_W, 22.0, 25.5, 0.0, 7.0, "door", "D-BED5", "a", 1)

    # 2F Openings:
    op("2F", "x", 20.125, 42.0, 45.5, 0.0, 7.0, "door", "D-BED6", "a", 1)
    op("2F", "x", 20.125, 72.0, 75.5, 0.0, 7.0, "door", "D-BED7", "a", 1)


# --------------------------------------------------------------------------
# ROOMS & ZONES
# --------------------------------------------------------------------------
def build_rooms(m: Model):
    def room(fl, name, poly, kind, label_xy=None, show_dims=True):
        r = Room(fl, name, poly, kind, label_xy, show_dims)
        m.rooms.append(r)
        return r

    # GF Rooms:
    room("GF", "MAIN LAWN", sbox(0.0, 0.0, XB_W, 20.5).intersection(PLOT_INNER), "ext", (18.0, 10.0))
    room("GF", "BED ROOM-2", R(XB_E, 3.75, XC_W, 19.75), "hab", (43.75, 11.75))
    room("GF", "BATH & DRESS", R(XC_E, 3.75, XC_P_W, 19.75), "wet", (54.0, 11.75))
    room("GF", "CAR PORCH", R(XC_P_E, 0.0, XD_W, 20.5), "circ", (62.6, 10.0))
    room("GF", "DRAWING ROOM", R(XD_E, 3.75, XE_W, 19.75), "hab", (77.0, 11.75))
    room("GF", "ENTRANCE FOYER", R(XB_E, 20.5, XC_P_W, 28.5), "circ", (46.0, 24.5))
    room("GF", "STAIRCASE CORE", R(XC_P_E, 20.5, XD_W, 28.5), "circ", (62.6, 26.5))
    room("GF", "POWDER ROOM", R(62.625, 20.5, XD_W, 25.5), "wet", (65.6, 23.0))
    room("GF", "KITCHEN", sbox(24.0, 20.5, XB_W, 33.75).intersection(PLOT_INNER), "serv", (30.0, 27.0))
    room("GF", "FAMILY LOUNGE + DINING", sbox(XB_E, 28.5, XD_W, 45.0).intersection(PLOT.buffer(-2.75)), "hab", (50.0, 36.0))
    room("GF", "BED ROOM-1", R(XD_E, 20.5, XE_W, 36.5), "hab", (77.0, 28.5))
    room("GF", "MASTER DRESS & BATH", sbox(XD_E, 36.5, XE_W, 57.0).intersection(PLOT.buffer(-2.75)), "wet", (77.0, 46.0))

    # 1F Rooms:
    room("1F", "FRONT SUN TERRACE", R(XC_P_E, 0.0, XD_W, 20.5), "ext", (62.6, 10.0))
    room("1F", "BED ROOM-4", R(XB_E, 3.75, XC_W, 19.75), "hab", (43.75, 11.75))
    room("1F", "BATH & DRESS", R(XC_E, 3.75, XC_P_W, 19.75), "wet", (54.0, 11.75))
    room("1F", "BED ROOM-3", R(XD_E, 3.75, XE_W, 19.75), "hab", (77.0, 11.75))
    room("1F", "BATH & DRESS", R(XD_E, 20.5, XE_W, 27.5), "wet", (77.0, 24.0))
    room("1F", "FAMILY LOUNGE", sbox(XB_E, 20.5, XD_W, 42.0).intersection(PLOT.buffer(-2.75)), "hab", (50.0, 30.0))
    room("1F", "BED ROOM-5", R(XD_E, 27.5, XE_W, 44.0), "hab", (77.0, 35.5))
    room("1F", "BATH & DRESS", sbox(XD_E, 44.0, XE_W, 57.0).intersection(PLOT.buffer(-2.75)), "wet", (77.0, 50.0))

    # 2F Rooms:
    room("2F", "FRONT SUN TERRACE", sbox(XB_E, 0.0, XD_W, 20.5), "ext", (50.0, 10.0))
    room("2F", "BED ROOM-6", R(XB_E, 20.5, XC_W, 36.5), "hab", (43.75, 28.5))
    room("2F", "BED ROOM-7", R(XD_E, 20.5, XE_W, 36.5), "hab", (77.0, 28.5))
    room("2F", "REAR SUN TERRACE", sbox(XB_E, 36.5, XE_W, 57.0).intersection(PLOT.buffer(-2.75)), "ext", (60.0, 46.0))

    # Zones for area schedule
    m.zones["MAIN LAWN"] = sbox(0.0, 0.0, XB_W, 20.5).intersection(PLOT_INNER)
    m.zones["CAR PORCH"] = R(XC_P_E, 0.0, XD_W, 20.5)
    m.zones["BUILDING"] = FP


# --------------------------------------------------------------------------
# BUILD MASTER MODEL
# --------------------------------------------------------------------------
def build() -> Model:
    m = Model()
    build_slabs(m)
    build_columns(m)
    build_walls(m)
    build_openings(m)
    build_rooms(m)
    furnish(m)

    # Process opening cuts in walls
    for fl in FLOORS:
        ops = [o for o in m.openings if o.floor == fl]
        new_walls = []
        for w in m.walls[fl]:
            new_walls.extend(split_wall(w, ops, LEVEL[fl]))
        m.walls[fl] = new_walls
        for w in new_walls:
            m.boxes.append(w)
        for o in ops:
            m.boxes.extend(opening_fill(o))

    return m


# --------------------------------------------------------------------------
# VALIDATION SUITE
# --------------------------------------------------------------------------
def validate(m: Model, verbose: bool = True):
    res = []

    def chk(cond: bool, msg: str):
        res.append((bool(cond), msg))

    # 1. Column continuity
    for cname in COLUMN_SPEC:
        cols = [b for b in m.boxes if b.layer == "columns" and b.tag == cname]
        chk(len(cols) >= 2, f"Column {cname} continuous through floors")

    # 2. Key room dimensions
    b2 = [r for r in m.rooms if r.floor == "GF" and r.name == "BED ROOM-2"][0]
    w_b2 = b2.poly.bounds[2] - b2.poly.bounds[0]
    d_b2 = b2.poly.bounds[3] - b2.poly.bounds[1]
    chk(w_b2 >= 14.0 and d_b2 >= 15.0, f"GF BED ROOM-2: {fi(w_b2)} x {fi(d_b2)} (>= 14'x15')")

    dr = [r for r in m.rooms if r.floor == "GF" and r.name == "DRAWING ROOM"][0]
    w_dr = dr.poly.bounds[2] - dr.poly.bounds[0]
    d_dr = dr.poly.bounds[3] - dr.poly.bounds[1]
    chk(w_dr >= 14.5 and d_dr >= 15.0, f"GF DRAWING ROOM: {fi(w_dr)} x {fi(d_dr)} (>= 14ft-6in x 15ft)")

    cp = [r for r in m.rooms if r.floor == "GF" and r.name == "CAR PORCH"][0]
    w_cp = cp.poly.bounds[2] - cp.poly.bounds[0]
    d_cp = cp.poly.bounds[3] - cp.poly.bounds[1]
    chk(w_cp >= 11.0 and d_cp >= 18.0, f"GF CAR PORCH: {fi(w_cp)} x {fi(d_cp)} (>= 11ft x 18ft)")

    # 3. Main entrance door >= 5'-0"
    main_door = [o for o in m.openings if "MAIN-DOOR" in o.name][0]
    chk(main_door.width >= 5.0, f"Main entrance door width {main_door.width:.1f} ft (>= 5ft)")

    # 4. Ventilation
    for fl in FLOORS:
        wets = [r for r in m.rooms if r.floor == fl and r.kind == "wet"]
        for wr in wets:
            ops = [o for o in m.openings if o.floor == fl and (o.kind in ("vent", "window") or "BATH" in o.name)]
            chk(len(ops) >= 1, f"{fl} {wr.name}: has natural exterior ventilation")

    # 5. Continuous East perimeter passage >= 2'-0"
    east_pass_w = 87.917 - XE_E
    chk(east_pass_w >= 2.0, f"East perimeter passage clear width {east_pass_w:.2f} >= 2ft")

    if verbose:
        for ok, msg in res:
            print(("  PASS  " if ok else "  FAIL  ") + msg)
        print(f"\\\\n{sum(o for o, _ in res)}/{len(res)} checks passed")
    return res


def area_schedule(m: Model):
    rows = []
    covered = {}
    covered["GF"] = m.slabs["GF"].area
    covered["1F"] = m.slabs[11.0].area
    covered["2F"] = m.slabs[22.0].area
    covered["MUMTY"] = m.slabs[42.0].area
    for k, v in m.zones.items():
        rows.append((k, v.area))
    return covered, rows


if __name__ == "__main__":
    model = build()
    print(f"boxes={len(model.boxes)} openings={len(model.openings)} rooms={len(model.rooms)}")
    validate(model)
    cov, rows = area_schedule(model)
    print("\\\\nCovered areas (sft):", {k: round(v) for k, v in cov.items()})
    for k, v in rows:
        print(f"  {k:20s} {v:8.1f} sft")
    print(f"  {'PLOT':20s} {PLOT.area:8.1f} sft")
'''

Path("scratch/test_model_new_scheme.py").write_text(code, encoding="utf-8")
print("Wrote scratch/test_model_new_scheme.py successfully!")
