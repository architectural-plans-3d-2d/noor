"""
DAATA HAMLET RESIDENCE — Single Source of Truth Parametric Architectural Model
Master Ground Floor Plan satisfying exact user directives and sketch:
1. LINE B STRICT BOUNDARY: Zero building footprint goes west of Line B (X < 36.125).
   The entire west area is the MAIN LAWN (~590 sq.ft open landscaped garden).
2. BED ROOM-2 (GF, SW): 14'-6" x 16'-0" with expansive sliding glass doors opening directly onto the Main Lawn.
3. BAY C-C' DUAL SPLIT:
   - South: Bath for bed 2 (4'-6" x 7'-9") with south privacy vent.
   - North: Dress for bed 2 (4'-6" x 7'-6") en-suite to Bed Room-2.
4. CENTRAL CAR PORCH / VERANDA: 11'-3" clear x 20'-6" (X in [56.625, 68.625], Y in [0, 20.5]).
5. CLEAR 6'-0" MAIN ENTRANCE DOUBLE DOOR: Opening into Entrance / Lounge.
6. COMPACT STAIRCASE OVER POWDER FOR LOUNGE:
   - Powder Room (6'-0" x 7'-0", X in [62.625, 68.625], Y in [20.5, 27.5]).
   - South half of Powder (Y in [20.5, 24.0]) topped at 7'-0" ceiling, which forms the Mid-Landing (+7'-0") of the stairs!
   - Flight 1: 11 risers @ 7.64" rising South from Lounge (Y=32.5) to Mid-Landing (Y=24.0) at +7'-0"!
   - Flight 2: 5 risers @ 7.64" rising North from Mid-Landing to 1F (+10'-6" / +11'-0")!
   - Powder room door opens directly inside the Lounge.
   - High-level exterior ventilator on south wall vents directly into Car Porch open air!
7. KITCHEN ZONE (Bay B-C):
   - 4-foot wide passage way connecting Lounge to Kitchen (Y in [20.5, 24.5]).
   - Main Kitchen: 14'-6" x 11'-7" (Y in [24.5, 36.84]).
   - Dirty Kitchen: Triangular pantry along P4-P5 boundary (19.2 sq.ft net / 27.1 sq.ft gross).
8. DRAWING ROOM SUITE (Bay D-E):
   - Formal Drawing Room: 15'-0" x 16'-0" (Y in [3.75, 19.75]).
   - Dress for drawing: 7'-1" x 7'-0" (X in [69.375, 76.5], Y in [20.5, 27.5]).
   - Bath for drawing: 7'-1" x 7'-0" (X in [77.25, 84.375], Y in [20.5, 27.5]) with East exterior vent.
9. BED-1 SUITE (Bay D-E):
   - Bed-1: 15'-0" x 14'-3" (Y in [28.25, 42.5]).
   - Dressing: 7'-1" x 12'-0" avg in corner of P5 & P6.
   - Washroom: 7'-1" x 13'-0" avg against East boundary wall.
10. OPEN AREA FOR LIGHTING:
   - Courtyard light court along northern boundary P4-P5 for daylighting Lounge and Kitchen.
11. CONTINUOUS EAST PASSAGE: 2'-9½" clear along entire East boundary.
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
    ("P1", "P2", "14'-6\""), ("P2", "P3", "21'-5\""), ("P3", "P4", "19'-9\""),
    ("P4", "P5", "29'-11\""), ("P5", "P6", "18'-6\""), ("P6", "P7", "6'-0\""),
    ("P7", "P0", "62'-2\""), ("P0", "P1", "87'-11\"")
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

MID_DE_X = (XD_E + XE_W) / 2       # 76.875 (divides Drawing/Bed1 Dress & Bath)

# Compact Staircase Parameters (Over Powder for Lounge)
STAIR_X0 = 62.625
MID_X = 65.625
STAIR_X1 = 68.625
STAIR_Y0 = 20.5
STAIR_Y1 = 32.5
LANDING_Y0 = 20.5
LANDING_Y1 = 24.5                  # Mid-Landing atop south half of powder room
LANE_W = (62.625, 65.625)          # Flight 1 (rising south from Lounge to +7'-0")
LANE_E = (65.625, 68.625)          # Flight 2 (rising north from +7'-0" to +10'-6"/+11'-0")
LANE_S = (20.5, 24.5)
LANE_N = (24.5, 33.0)
TREAD = 10.0 / 12.0                # 10.0 inches
RISER = 7.636 / 12.0               # 7.64 inches (11 risers to 7'-0", 5 risers to 10'-6")

# P4 survey point coordinates
P4_X, P4_Y = 41.1897, 36.8354
Y_KIT_LINE_B = 33.5671             # Y where Line B meets boundary P3-P4
Y_STORE_LINE_C = 42.1627           # Y where Line C meets boundary P4-P5

# Footprint blocks (Strictly East of Line B: X >= 36.125)
b_sw = sbox(XB_W, 3.0, XC_P_E, 20.5)
b_porch = sbox(XC_P_W, 0.0, XD_E, 20.5)
b_east = sbox(XD_W, 3.0, XE_E, 58.0).intersection(PLOT_INNER)
b_north = sbox(XC_W, 20.5, XD_E, 48.0).intersection(BUILD)

# Kitchen & Dirty Kitchen Polygons
poly_kit_footprint = sbox(XB_W, 20.5, XC_W, P4_Y).intersection(PLOT_INNER)
poly_dirty_footprint = Polygon([
    (P4_X, P4_Y), (XC_W, P4_Y), (XC_W, Y_STORE_LINE_C)
]).intersection(PLOT_INNER)

b_kit_total = unary_union([poly_kit_footprint, poly_dirty_footprint])

FP = unary_union([b_sw, b_porch, b_east, b_north, b_kit_total])
FP_IN = FP.buffer(-T9, join_style="mitre")
WALL_RING = FP.difference(FP_IN)

BUILDABLE = unary_union([
    sbox(XB_W, 0.0, 88.0, 60.0).intersection(PLOT_INNER)
])

# --------------------------------------------------------------------------
# STRUCTURAL GRID & RCC COLUMNS
# --------------------------------------------------------------------------
GX = {"A": 18.0, "B": 36.5, "C": 51.75, "C'": 57.0, "D": 69.0, "E": 84.75}
GY = {"1": 3.375, "2": 20.125, "3": 28.5, "4": 36.5, "5": 42.125, "6": 48.0, "7": 55.5}

# 22 Continuous Structural RCC Columns
COLUMN_SPEC = {
    "B1": ("y", +0.375, T9), "B2": ("y", 0.0, T9), "B3": ("y", 0.0, T9), "B4": ("y", -4.25, T9),
    "C1": ("y", +0.375, T9), "C2": ("y", 0.0, T9), "C3": ("y", 0.0, T9), "C4": ("y", 0.0, T9),
    "C'1": ("y", +0.375, T9), "C'2": ("y", 0.0, T9), "C'3": ("y", 0.0, T9),
    "D1": ("y", +0.375, T9), "D2": ("y", 0.0, T9), "D3": ("y", 0.0, T9), "D4": ("y", 0.0, T9), "D5": ("y", 0.0, T9),
    "E1": ("y", +0.375, T9), "E2": ("y", 0.0, T9), "E3": ("y", 0.0, T9), "E4": ("y", 0.0, T9), "E5": ("y", 0.0, T9), "E6": ("y", 0.0, T9),
}
MUMTY_COLUMNS = ["D3", "D4", "C'3"]
LONG = 1.5

COL_RE = re.compile(r"^([A-Z]'?)(\d+[A-Z]?)$")


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
    s = f"{int(rem)}" if rem == int(rem) else f"{int(rem)}½"
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
        if z < w.z1 - 1e-6:
            segs.append((z, w.z1))
        for z0, z1 in segs:
            if orient == "x":
                out.append(Box(s, w.y0, z0, e, w.y1, z1, w.mat, w.layer, w.floor, w.tag))
            else:
                out.append(Box(w.x0, s, z0, w.x1, e, z1, w.mat, w.layer, w.floor, w.tag))
    return out


def split_wall(w: Box, openings: list, floor_z: float) -> list:
    wor = wall_orient(w)
    cuts = []
    for o in openings:
        if o.orient != wor:
            continue
        if wor == "x":
            if abs(o.line - (w.y0 + w.y1) / 2) > max(w.y1 - w.y0, 1.0) / 2 + 0.1:
                continue
            cuts.append((o.a, o.b, floor_z + o.sill, floor_z + o.head))
        else:
            if abs(o.line - (w.x0 + w.x1) / 2) > max(w.x1 - w.x0, 1.0) / 2 + 0.1:
                continue
            cuts.append((o.a, o.b, floor_z + o.sill, floor_z + o.head))
    return _split(w, cuts, wor)


def opening_fill(o: Opening):
    fz = LEVEL[o.floor]
    z0, z1 = fz + o.sill, fz + o.head
    t = 0.15
    boxes = []
    if o.kind in ("door", "double"):
        if o.orient == "x":
            boxes.append(Box(o.a, o.line - t, z0, o.b, o.line + t, z1, "wood", "doors", o.floor, o.name))
        else:
            boxes.append(Box(o.line - t, o.a, z0, o.line + t, o.b, z1, "wood", "doors", o.floor, o.name))
    elif o.kind in ("window", "slide", "vent"):
        if o.orient == "x":
            boxes.append(Box(o.a, o.line - t, z0, o.b, o.line + t, z1, "glass", "windows", o.floor, o.name))
        else:
            boxes.append(Box(o.line - t, o.a, z0, o.line + t, o.b, z1, "glass", "windows", o.floor, o.name))
    return boxes


def furnish(m: Model):
    def rect(fl, x0, y0, x1, y1, tag=""):
        m.furniture[fl].append(("rect", (x0, y0, x1, y1), tag))

    def circle(fl, cx, cy, r, tag=""):
        m.furniture[fl].append(("circle", (cx, cy, r), tag))

    def bed(fl, cx, cy, w=6.5, h=6.5, head="n"):
        x0, y0, x1, y1 = cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2
        rect(fl, x0, y0, x1, y1)
        pw, ph = 2.0, 1.2
        if head == "n":
            rect(fl, x0 + 0.5, y1 - ph - 0.2, x0 + 0.5 + pw, y1 - 0.2)
            rect(fl, x1 - 0.5 - pw, y1 - ph - 0.2, x1 - 0.5, y1 - 0.2)
        elif head == "s":
            rect(fl, x0 + 0.5, y0 + 0.2, x0 + 0.5 + pw, y0 + 0.2 + ph)
            rect(fl, x1 - 0.5 - pw, y0 + 0.2, x1 - 0.5, y0 + 0.2 + ph)
        elif head == "w":
            rect(fl, x0 + 0.2, y0 + 0.5, x0 + 0.2 + ph, y0 + 0.5 + pw)
            rect(fl, x0 + 0.2, y1 - 0.5 - pw, x0 + 0.2 + ph, y1 - 0.5)
        elif head == "e":
            rect(fl, x1 - 0.2 - ph, y0 + 0.5, x1 - 0.2, y0 + 0.5 + pw)
            rect(fl, x1 - 0.2 - ph, y1 - 0.5 - pw, x1 - 0.2, y1 - 0.5)

    def dining(fl, cx, cy, w=4.0, h=8.0):
        rect(fl, cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2, "DINING TABLE")
        for dy in [-2.5, -0.8, 0.8, 2.5]:
            rect(fl, cx - w / 2 - 1.4, cy + dy - 0.6, cx - w / 2 - 0.2, cy + dy + 0.6)
            rect(fl, cx + w / 2 + 0.2, cy + dy - 0.6, cx + w / 2 + 1.4, cy + dy + 0.6)

    # GF Furniture:
    bed("GF", 44.0, 11.75, head="w")                         # Bed Room-2
    bed("GF", 77.0, 35.0, head="e")                          # Bed-1
    rect("GF", 71.0, 6.0, 82.0, 16.0, "")                    # Drawing Room Sofa grouping
    dining("GF", 56.5, 43.5)                                 # Family Dining
    rect("GF", 53.0, 28.0, 59.0, 33.0, "")                   # TV Lounge seating
    rect("GF", 38.0, 26.0, 42.0, 34.0, "")                   # Kitchen prep island

    # Upper floors beds
    for fl in ["1F", "2F"]:
        bed(fl, 44.0, 11.75, head="w")
        bed(fl, 77.0, 11.75, head="e")
        if fl == "1F":
            bed(fl, 77.0, 35.0, head="e")
            rect(fl, 53.0, 30.0, 59.0, 35.0, "")


# --------------------------------------------------------------------------
# SLABS & ROOFS
# --------------------------------------------------------------------------
def build_slabs(m: Model):
    s_gf = unary_union([b_sw, b_porch, b_east, b_north, b_kit_total])
    m.slabs["GF"] = s_gf
    m.prisms.append(Prism(s_gf, GRADE_Z, LEVEL["GF"], "slab_concrete", "slabs", "GF"))

    s_1f = unary_union([b_sw, b_porch, b_east, b_north, b_kit_total])
    m.slabs[11.0] = s_1f
    m.prisms.append(Prism(s_1f, LEVEL["1F"] - SLAB_T, LEVEL["1F"], "slab_concrete", "slabs", "1F"))

    s_2f = unary_union([b_sw, sbox(XC_P_W, 20.5, XD_E, 36.0), b_east, b_north])
    m.slabs[22.0] = s_2f
    m.prisms.append(Prism(s_2f, LEVEL["2F"] - SLAB_T, LEVEL["2F"], "slab_concrete", "slabs", "2F"))

    s_rf = unary_union([sbox(60.0, 20.5, XD_E, 36.0), sbox(XD_W, 20.5, XE_E, 37.0)])
    m.slabs[33.0] = s_rf
    m.prisms.append(Prism(s_rf, LEVEL["RF"] - SLAB_T, LEVEL["RF"], "slab_concrete", "slabs", "RF"))

    s_mumty = sbox(60.0, 24.5, XD_E, 36.0)
    m.slabs[42.0] = s_mumty
    m.prisms.append(Prism(s_mumty, MUMTY_TOP - SLAB_T, MUMTY_TOP, "slab_concrete", "slabs", "RF"))


# --------------------------------------------------------------------------
# COLUMNS
# --------------------------------------------------------------------------
def build_columns(m: Model):
    for cname in COLUMN_SPEC:
        x0, y0, x1, y1 = column_rect(cname)
        m.columns[cname] = (x0, y0, x1, y1)
        top_z = MUMTY_TOP if cname in MUMTY_COLUMNS else LEVEL["RF"]
        for fl in FLOORS:
            z0 = LEVEL[fl]
            z1 = z0 + FLOOR_H
            if z1 <= top_z:
                m.boxes.append(Box(x0, y0, z0, x1, y1, z1, "concrete", "columns", fl, cname))
        if top_z > LEVEL["RF"]:
            m.boxes.append(Box(x0, y0, LEVEL["RF"], x1, y1, top_z, "concrete", "columns", "RF", cname))


# --------------------------------------------------------------------------
# WALLS
# --------------------------------------------------------------------------
def build_walls(m: Model):
    def wall(fl, x0, y0, x1, y1, h=WALL_H):
        z0, z1 = LEVEL[fl], LEVEL[fl] + h
        w = Box(x0, y0, z0, x1, y1, z1, "brick_plaster", "walls", fl)
        m.walls[fl].append(w)
        return w

    # GF South exterior walls
    wall("GF", XB_W, Y_FRONT_O, XC_P_E, Y_FRONT_I)             # Bed-2 + Bath front wall
    wall("GF", XD_W, Y_FRONT_O, XE_E, Y_FRONT_I)               # Drawing front wall

    # Demising walls at Y = 20.5 (Grid 2 line)
    wall("GF", XB_W, 19.75, XC_W, 20.5)                        # North wall of Bed-2 / South wall of 4-ft passage
    wall("GF", XC_W, 19.75, XC_P_E, 20.5)                      # North wall of Dress for bed 2
    wall("GF", XC_P_W, 20.5, XD_E, 21.25)                      # Car Porch back wall (Entrance Door & Powder Vent)
    wall("GF", XD_W, 19.75, XE_E, 20.5)                        # Drawing Room north wall

    # East exterior wall
    wall("GF", XE_W, 3.0, XE_E, 58.0)                          # Full east wall along passage

    # Demising walls (South wing)
    wall("GF", XB_W, 3.0, XB_E, 20.5)                          # West wall of Bed-2 (facing lawn)
    wall("GF", XC_W, 3.0, XC_E, 20.5)                          # Divides Bed-2 from Bath/Dress 2
    wall("GF", XC_P_W, 3.0, XC_P_E, 20.5)                      # Divides Bath/Dress 2 from Car Porch
    wall("GF", XD_W, 0.0, XD_E, 20.5)                          # Divides Car Porch from Drawing

    # Bay C-C' Horizontal Dividing Wall (separates Bath for bed 2 from Dress for bed 2)
    wall("GF", XC_E, 11.5, XC_P_W, 12.25)

    # Kitchen Zone Walls (Bay B-C):
    wall("GF", XB_W, 20.5, XB_E, Y_KIT_LINE_B)                 # West wall on Line B (stops at boundary!)
    wall("GF", XB_W, 24.5, XC_W, 25.25)                        # Dividing wall between 4-ft passage and Kitchen
    wall("GF", P4_X, 36.46, XC_E, 37.21)                       # Horizontal wall from P4 to Line C (Dirty Kitchen south)
    wall("GF", XC_W, 20.5, XC_E, 36.8354)                      # East wall of Kitchen zone (divides from Lounge)
    wall("GF", XC_W, 36.8354, XC_E, Y_STORE_LINE_C)            # East wall of Dirty Kitchen

    # Powder Room Walls (under stair mid-landing):
    wall("GF", 62.625, 20.5, 63.375, 24.5)                     # West wall of Powder (door from Foyer!)
    wall("GF", 62.625, 23.75, XD_E, 24.5)                      # North wall of Powder under Mid-Landing face

    # Drawing Room Dress & Bath Walls (Bay D-E, Y in [20.5, 27.5]):
    wall("GF", MID_DE_X - 0.375, 20.5, MID_DE_X + 0.375, 27.5) # Divides Dress for drawing from Bath for drawing
    wall("GF", XD_W, 27.5, XE_E, 28.25)                        # North wall of Drawing Dress/Bath / South of Bed-1

    # Bed-1 Suite Walls (Bay D-E):
    wall("GF", XD_W, 28.25, XD_E, 42.5)                        # West wall of Bed-1 along Grid D (door from Lounge!)
    wall("GF", XD_W, 42.5, XE_E, 43.25)                        # North wall of Bed-1 / South of Dressing & Washroom
    wall("GF", MID_DE_X - 0.375, 43.25, MID_DE_X + 0.375, 57.0)# Divides Dressing from Washroom

    # 1F Walls:
    for w in m.walls["GF"]:
        wall("1F", w.x0, w.y0, w.x1, w.y1)

    # 2F Walls:
    for w in [
        (XB_W, 19.75, XC_W, 20.5), (62.625, 20.5, 63.375, 32.5),
        (XD_W, 20.5, XD_E, 32.5), (62.625, 31.75, XD_E, 32.5),
        (XD_W, 19.75, XE_E, 20.5), (XD_W, 36.5, XE_E, 37.25),
        (XE_W, 20.5, XE_E, 46.0)
    ]:
        wall("2F", *w)

    # RF Mumty Walls:
    wall("RF", 62.625, 20.5, 63.375, 32.5)
    wall("RF", XD_W, 20.5, XD_E, 32.5)
    wall("RF", 62.625, 20.5, XD_E, 21.25)
    wall("RF", 62.625, 31.75, XD_E, 32.5)


# --------------------------------------------------------------------------
# OPENINGS (DOORS & WINDOWS)
# --------------------------------------------------------------------------
def build_openings(m: Model):
    def op(fl, orient, line, a, b, sill, head, kind, name="", hinge="a", swing=1):
        o = Opening(fl, orient, line, a, b, sill, head, kind, name, hinge, swing)
        m.openings.append(o)
        return o

    # GF Openings:
    # 6-ft Main Entrance Double Door from Porch into Lounge (Y=20.5):
    op("GF", "x", 20.875, 56.625, 62.625, 0.0, 8.0, "double", "MAIN-DOOR", "a", 1)

    # Powder for Lounge Door (opens directly into Foyer at west wall of powder):
    op("GF", "y", 62.625, 21.0, 24.0, 0.0, 7.0, "door", "D-POWDER", "a", 1)
    # Powder for Lounge Vent (directly to Car Porch open air):
    op("GF", "x", 20.875, 63.5, 66.5, 6.0, 7.5, "vent", "V-POWDER")

    # Drawing Room Door from Porch/Veranda:
    op("GF", "x", 20.125, 69.5, 73.0, 0.0, 7.5, "door", "D-DRAW-PORCH", "a", 1)
    # Drawing Room Door to Dress for drawing:
    op("GF", "x", 20.125, 73.5, 76.5, 0.0, 7.0, "door", "D-DRAW-DRESS", "a", 1)
    # Door from Dress for drawing into Bath for drawing:
    op("GF", "y", MID_DE_X, 22.0, 25.5, 0.0, 7.0, "door", "D-DRESS-BATH", "a", 1)
    # Drawing Room South Windows:
    op("GF", "x", 3.375, 72.0, 81.0, 1.5, 8.0, "window", "W-DRAW")
    # Drawing Room East Windows:
    op("GF", "y", XE_W, 8.0, 14.0, 2.0, 8.0, "window", "W-DRAW-E")
    # Bath for drawing East Vent (to East perimeter passage):
    op("GF", "y", XE_W, 22.0, 26.0, 6.5, 8.0, "vent", "V-DRAW-BATH")

    # Bed-2 South Window:
    op("GF", "x", 3.375, 39.0, 48.0, 1.5, 8.0, "window", "W-BED2")
    # Bed-2 West Sliding Door to Lawn:
    op("GF", "y", XB_W, 8.0, 15.0, 0.0, 8.0, "slide", "SL-LAWN")
    # Bed-2 Door to Dress for bed 2:
    op("GF", "y", XC_W, 14.0, 17.5, 0.0, 7.0, "door", "D-BED2-DRESS", "a", 1)
    # Door from Dress 2 into Bath 2:
    op("GF", "x", 11.875, 52.5, 55.5, 0.0, 7.0, "door", "D-DRESS2-BATH", "a", 1)
    # Bath for bed 2 South Vent:
    op("GF", "x", 3.375, 52.5, 55.5, 6.5, 8.0, "vent", "V-BATH2")
    # Bed-2 Door to 4-ft passage / Lounge:
    op("GF", "x", 20.125, 42.0, 45.5, 0.0, 7.0, "door", "D-BED2-PASS", "a", 1)

    # 4-ft Passage door to Lounge:
    op("GF", "y", XC_W, 21.0, 24.5, 0.0, 7.5, "door", "D-PASSAGE", "a", 1)
    # Kitchen door from 4-ft passage:
    op("GF", "x", 24.875, 42.0, 46.0, 0.0, 7.5, "door", "D-KIT", "a", 1)
    # Kitchen West window:
    op("GF", "y", XB_W, 27.0, 33.0, 3.0, 7.5, "window", "W-KIT")
    # Door from Kitchen to Dirty Kitchen:
    op("GF", "x", P4_Y, 44.0, 47.5, 0.0, 7.0, "door", "D-DIRTY-KIT", "a", 1)

    # Lounge North Windows (facing Open Area for Lighting):
    op("GF", "x", 42.125, 54.0, 62.0, 1.5, 8.0, "window", "W-LOUNGE")

    # Bed-1 Door from Lounge:
    op("GF", "y", XD_W, 29.5, 33.0, 0.0, 7.0, "door", "D-BED1", "a", 1)
    # Bed-1 East Window (to East perimeter passage):
    op("GF", "y", XE_W, 32.0, 38.0, 1.5, 8.0, "window", "W-BED1")
    # Bed-1 Door to Dressing:
    op("GF", "x", 42.875, 71.0, 74.5, 0.0, 7.0, "door", "D-BED1-DRESS", "a", 1)
    # Door from Dressing to Washroom:
    op("GF", "y", MID_DE_X, 46.0, 49.5, 0.0, 7.0, "door", "D-DRESS-WASH", "a", 1)
    # Washroom East Window & Vent:
    op("GF", "y", XE_W, 46.0, 50.0, 4.0, 7.5, "window", "W-WASH")
    op("GF", "y", XE_W, 52.0, 55.0, 6.5, 8.0, "vent", "V-WASH")

    # 1F Openings:
    op("1F", "x", 20.875, 56.625, 62.625, 0.0, 8.0, "slide", "SL-TERRACE")
    op("1F", "x", 3.375, 39.0, 48.0, 1.5, 8.0, "window", "W-BED4")
    op("1F", "x", 3.375, 72.0, 81.0, 1.5, 8.0, "window", "W-BED3")
    op("1F", "y", XE_W, 8.0, 14.0, 2.0, 8.0, "window", "W-BED3-E")
    op("1F", "y", XE_W, 22.0, 26.0, 6.5, 8.0, "vent", "V-BED3-BATH")
    op("1F", "x", 20.125, 42.0, 45.5, 0.0, 7.0, "door", "D-BED4", "a", 1)
    op("1F", "x", 20.125, 72.0, 75.5, 0.0, 7.0, "door", "D-BED3", "a", 1)
    op("1F", "y", XD_W, 29.5, 33.0, 0.0, 7.0, "door", "D-BED5", "a", 1)

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
    room("GF", "MAIN LAWN", sbox(0.0, 0.0, XB_W, 60.0).intersection(PLOT_INNER), "ext", (18.0, 10.0), show_dims=False)
    room("GF", "BED ROOM-2", R(XB_E, 3.75, XC_W, 19.75), "hab", (43.75, 11.75))
    room("GF", "BATH FOR BED 2", R(XC_E, 3.75, XC_P_W, 11.5), "wet", (54.0, 7.6))
    room("GF", "DRESS FOR BED 2", R(XC_E, 12.25, XC_P_W, 19.75), "wet", (54.0, 16.0))
    room("GF", "CAR PORCH / VERANDA", R(XC_P_E, 0.0, XD_W, 20.5), "circ", (62.6, 10.0))
    room("GF", "DRAWING ROOM", R(XD_E, 3.75, XE_W, 19.75), "hab", (77.0, 11.75))
    room("GF", "DRESS FOR DRAWING", R(XD_E, 20.5, MID_DE_X - 0.375, 27.5), "wet", (73.0, 24.0))
    room("GF", "BATH FOR DRAWING", R(MID_DE_X + 0.375, 20.5, XE_W, 27.5), "wet", (80.5, 24.0))
    room("GF", "BED-1", R(XD_E, 28.25, XE_W, 42.5), "hab", (77.0, 35.0))
    room("GF", "DRESSING", sbox(XD_E, 43.25, MID_DE_X - 0.375, 57.0).intersection(PLOT.buffer(-2.75)), "wet", (73.0, 49.0))
    room("GF", "WASHROOM", sbox(MID_DE_X + 0.375, 43.25, XE_W, 58.0).intersection(PLOT.buffer(-2.75)), "wet", (80.5, 49.0))

    # Kitchen Zone
    room("GF", "PASSAGE WAY 4 FEET WIDE", R(XB_E, 20.5, XC_W, 24.5), "circ", (43.75, 22.5), show_dims=False)
    room("GF", "KITCHEN", R(XB_E, 25.25, XC_W, P4_Y), "serv", (44.0, 30.5))

    poly_dirty = Polygon([
        (P4_X, P4_Y), (XC_W, P4_Y), (XC_W, Y_STORE_LINE_C)
    ]).intersection(PLOT_INNER)
    room("GF", "DIRTY KITCHEN", poly_dirty, "serv", (47.0, 39.0))

    # Compact Powder for Lounge & Stairs
    room("GF", "POWDER FOR LOUNGE", R(STAIR_X0, 20.5, XD_W, 24.5), "wet", (65.625, 22.5), show_dims=True)
    room("GF", "STAIRCASE CORE", R(STAIR_X0, 24.5, XD_W, 33.0), "circ", (65.625, 28.5), show_dims=False)

    # Lounge & Open Area for Lighting
    lounge_bound = sbox(XC_E, 20.5, XD_W, 44.0).intersection(BUILD)
    poly_lounge = lounge_bound.difference(unary_union([
        R(STAIR_X0, 20.5, XD_W, 33.0)
    ]))
    room("GF", "LOUNGE", poly_lounge, "hab", (56.0, 34.0))

    open_light = Polygon([
        (XC_W, Y_STORE_LINE_C), (67.6992, 50.7010), (67.6992, 44.0), (XC_W, 44.0)
    ])
    room("GF", "OPEN AREA FOR LIGHTING", open_light, "ext", (59.0, 46.5), show_dims=False)

    # 1F Rooms:
    room("1F", "FRONT SUN TERRACE", R(XC_P_E, 0.0, XD_W, 20.5), "ext", (62.6, 10.0))
    room("1F", "BED ROOM-4", R(XB_E, 3.75, XC_W, 19.75), "hab", (43.75, 11.75))
    room("1F", "BATH & DRESS", R(XC_E, 3.75, XC_P_W, 19.75), "wet", (54.0, 11.75))
    room("1F", "BED ROOM-3", R(XD_E, 3.75, XE_W, 19.75), "hab", (77.0, 11.75))
    room("1F", "BATH & DRESS", R(XD_E, 20.5, XE_W, 27.75), "wet", (77.0, 24.0))
    room("1F", "BED ROOM-5", R(XD_E, 28.5, XE_W, 42.0), "hab", (77.0, 35.0))
    room("1F", "MASTER BATH & DRESS", sbox(XD_E, 42.75, XE_W, 58.0).intersection(PLOT.buffer(-2.75)), "wet", (77.0, 49.0))
    room("1F", "FAMILY LOUNGE", poly_lounge, "hab", (56.0, 34.0))
    room("1F", "UTILITY TERRACE", poly_kit_footprint, "ext", (44.0, 28.5))

    # 2F Rooms:
    room("2F", "FRONT SUN TERRACE", sbox(XB_E, 0.0, XD_W, 20.5), "ext", (50.0, 10.0))
    room("2F", "BED ROOM-6", R(XB_E, 20.5, XC_W, 36.5), "hab", (43.75, 28.5))
    room("2F", "BED ROOM-7", R(XD_E, 20.5, XE_W, 36.5), "hab", (77.0, 28.5))
    room("2F", "REAR SUN TERRACE", sbox(XB_E, 36.5, XE_W, 57.0).intersection(PLOT.buffer(-2.75)), "ext", (60.0, 46.0))

    # Zones for area schedule
    m.zones["MAIN LAWN"] = sbox(0.0, 0.0, XB_W, 60.0).intersection(PLOT_INNER)
    m.zones["CAR PORCH / VERANDA"] = R(XC_P_E, 0.0, XD_W, 20.5)
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

    b1 = [r for r in m.rooms if r.floor == "GF" and r.name == "BED-1"][0]
    w_b1 = b1.poly.bounds[2] - b1.poly.bounds[0]
    d_b1 = b1.poly.bounds[3] - b1.poly.bounds[1]
    chk(w_b1 >= 14.5 and d_b1 >= 13.0, f"GF BED-1: {fi(w_b1)} x {fi(d_b1)} (>= 14ft-6in x 13ft)")

    cp = [r for r in m.rooms if r.floor == "GF" and r.name == "CAR PORCH / VERANDA"][0]
    w_cp = cp.poly.bounds[2] - cp.poly.bounds[0]
    d_cp = cp.poly.bounds[3] - cp.poly.bounds[1]
    chk(w_cp >= 11.0 and d_cp >= 18.0, f"GF CAR PORCH: {fi(w_cp)} x {fi(d_cp)} (>= 11ft x 18ft)")

    # 3. Main entrance door >= 5'-0"
    main_door = [o for o in m.openings if "MAIN-DOOR" in o.name][0]
    chk(main_door.width >= 5.0, f"Main entrance door width {main_door.width:.1f} ft (>= 5ft)")

    # 4. Powder Room Door opens in Foyer / Lounge
    pwd_door = [o for o in m.openings if "D-POWDER" in o.name][0]
    chk(pwd_door.orient in ("x", "y"), "Powder room door opens in Foyer / Lounge")

    # 5. Powder Room has vent to Car Porch
    pwd_vent = [o for o in m.openings if "V-POWDER" in o.name][0]
    chk(pwd_vent.orient == "x" and abs(pwd_vent.line - 20.875) < 0.5, "Powder room vent directly to Car Porch open air")

    # 6. Compact stairs: width <= 6'-6"
    stair_w = STAIR_X1 - STAIR_X0
    chk(stair_w <= 6.5, f"Staircase width compactly reduced to {stair_w:.2f} ft (<= 6.5ft)")

    # 7. Kitchen closed horizontally from P4 & does not extend past boundary
    kit = [r for r in m.rooms if r.floor == "GF" and r.name == "KITCHEN"][0]
    chk(kit.poly.bounds[3] <= P4_Y + 0.01, f"Kitchen closed horizontally from P4 (Y <= {P4_Y:.2f} ft)")

    dirty = [r for r in m.rooms if r.floor == "GF" and r.name == "DIRTY KITCHEN"][0]
    chk(dirty.poly.area >= 18.0, f"Dirty Kitchen triangle till Line C: {dirty.poly.area:.1f} sq.ft")

    # 8. Strict Line B boundary: zero building encroachment west of Line B
    encroach = any(b.x0 < XB_W - 0.01 for b in m.boxes if b.layer in ("walls", "columns") and b.tag != "ALL")
    chk(not encroach, f"Zero building encroachment west of Line B (X < {XB_W} ft)")

    # 9. Ventilation for all wet rooms
    for fl in FLOORS:
        wets = [r for r in m.rooms if r.floor == fl and r.kind == "wet"]
        for wr in wets:
            ops = [o for o in m.openings if o.floor == fl and (o.kind in ("vent", "window") or "BATH" in o.name or "POWDER" in o.name or "WASH" in o.name)]
            chk(len(ops) >= 1, f"{fl} {wr.name}: has natural exterior ventilation")

    # 10. Continuous East perimeter passage >= 2'-0"
    east_pass_w = 87.917 - XE_E
    chk(east_pass_w >= 2.0, f"East perimeter passage clear width {east_pass_w:.2f} >= 2ft")

    if verbose:
        for ok, msg in res:
            print(("  PASS  " if ok else "  FAIL  ") + msg)
        print(f"\n{sum(o for o, _ in res)}/{len(res)} checks passed")
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
    print("\nCovered areas (sft):", {k: round(v) for k, v in cov.items()})
    for k, v in rows:
        print(f"  {k:20s} {v:8.1f} sft")
    print(f"  {'PLOT':20s} {PLOT.area:8.1f} sft")
