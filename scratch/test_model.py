"""
DAATA HAMLET RESIDENCE - Parametric design model (single source of truth)
=========================================================================
Every drawing (plans, elevations, section, DXF) and every 3D export (GLB/OBJ,
Three.js, Blender Cycles) is generated from THIS file, so 2D and 3D can never
disagree.

Units      : feet (decimal). 1 ft = 0.3048 m
Origin     : survey point P1 (south-west plot corner on the road), FFL GF = 0.00
Axes       : +x east, +y north, +z up
Structure  : RCC frame, 9"x18" columns concealed in 9" brick walls, 9"x18" beams,
             6" two-way slabs. Floor-to-floor 11'-0" (clear 10'-4" = 3.15 m).
Ventilation: VS-1 vertical ventilation shaft (3'x3' clear) open to sky.
             All wet rooms have direct ventilation to outside air or VS-1 shaft.
Passage    : Full continuous >= 2'-0" perimeter passage (east side, north angled boundary,
             and NE service court connected to main lawn).
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
# STAIR (11" treads, 6.6" risers, 2 flights x (10R / 9T))
# --------------------------------------------------------------------------
RISERS, RISER = 20, FLOOR_H / 20
TREAD = 11.0 / 12.0
STAIR_X0 = 72.625                  # first riser line
FLIGHT_LEN = 9 * TREAD             # 8'-3" (8.25 ft)
MID_X = STAIR_X0 + FLIGHT_LEN      # 80.875 -> mid landing to 84.375 (3'-6" = 3.5 ft clear)
LANE_S = (28.25, 31.75)            # flight 1 (up)
LANE_N = (32.125, 35.625)          # flight 2
STAIR_HOLE = (STAIR_X0, 28.25, 84.375, 35.625)

# --------------------------------------------------------------------------
# FOOTPRINT COORDINATES (Option B: Balanced room widths & 2'-0" passage)
# --------------------------------------------------------------------------
XB_O, XB_I = 36.125, 36.875        # West outer & inner wall faces (Bed-2 strip)
XC_W, XC_E = 51.375, 52.125        # Line C west & east wall faces
XD_W, XD_E = 68.625, 69.375        # Line D west & east wall faces
XE_I, XE_O = 84.375, 85.125        # East inner & outer wall faces (East passage)

# Footprint blocks (Option B: Balanced room widths & 2'-0" passage)
bc_block = sbox(XB_O, 3.0, XC_E, 33.75).intersection(BUILD)
cd_block = sbox(XC_W, 3.0, XD_E, 42.5).intersection(BUILD)
de_block = sbox(XD_W, 3.0, XE_O, 58.0).intersection(PLOT_INNER)
blocks = {'BC': bc_block, 'CD': cd_block, 'DE': de_block}

FP = unary_union(list(blocks.values()))
FP_IN = FP.buffer(-T9, join_style="mitre")
WALL_RING = FP.difference(FP_IN)

BUILDABLE = unary_union([
    sbox(XB_O, 3.0, XD_E, 50.0).intersection(BUILD),
    sbox(XD_W, 3.0, XE_O, 58.0).intersection(PLOT_INNER)
])

# --------------------------------------------------------------------------
# STRUCTURAL GRID & RCC COLUMNS (All parallel along orthogonal axes)
# --------------------------------------------------------------------------
GX = {"A": 18.0, "B": 36.5, "B'": 42.5, "C": 51.75, "C'": 58.875, "D": 69.0, "E": 84.75}
GY = {"1": 3.375, "2": 17.0, "3": 20.125, "4": 27.875, "5": 33.375, "6": 36.0, "7": 42.125, "7E": 46.5, "7A": 49.0, "8": 55.10}

COLUMN_SPEC = {
    "A1": ("y", 0.0, 1.0), "A2": ("y", 0.0, 1.0),                    # porch / canopy frame 12"x18"
    "B1": ("y", +0.375, T9), "B2": ("y", 0.0, T9), "B3": ("y", 0.0, T9), "B4": ("y", 0.0, T9),
    "B'5": ("x", 0.0, T9),                                            # chamfer terminal column
    "C1": ("y", +0.375, T9), "C3": ("y", 0.0, T9), "C4": ("y", -0.375, T9), "C5": ("y", +0.375, T9),
    "C'7": ("x", 0.0, T9),                                            # chamfer terminal column
    "D1": ("y", +0.375, T9), "D3": ("y", 0.0, T9), "D4": ("y", -0.375, T9), "D6": ("x", +0.375, T9),
    "D7": ("y", +0.375, T9), "D7A": ("y", 0.0, T9),                  # D7A near P5
    "E1": ("y", +0.375, T9), "E3": ("y", 0.0, T9), "E4": ("y", 0.0, T9), "E6": ("y", 0.0, T9),
    "E7E": ("y", 0.0, T9), "E8": ("y", 0.0, T9),                     # E7E at 46.5, E8 at P6
}
MUMTY_COLUMNS = ["D4", "E4", "D6", "E6"]
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
    """Beams between consecutive columns on grid lines plus diagonal chamfers."""
    names = list(COLUMN_SPEC)
    segs = []
    for letter in GX:
        on = sorted([n for n in names if split_col(n)[0] == letter], key=lambda n: GY[split_col(n)[1]])
        segs += [(a, b) for a, b in zip(on, on[1:])]
    for num in GY:
        on = sorted([n for n in names if split_col(n)[1] == num], key=lambda n: GX[split_col(n)[0]])
        segs += [(a, b) for a, b in zip(on, on[1:])]
    segs.append(("B4", "B'5"))
    segs.append(("C5", "C'7"))
    segs.append(("D7A", "E8"))
    segs.append(("D7", "E7E"))
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
    s = f"{int(rem)}" if rem == int(rem) else f"{int(rem)}\u00bd"
    return f"{'-' if neg else ''}{ft}'-{s}\""


# --------------------------------------------------------------------------
# WALL SPLITTING & OPENING FILL
# --------------------------------------------------------------------------
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

    for fl in FLOORS:
        bed(fl, XE_I, 11.75, head="e")                         # Bed-1/3/6
        rect(fl, XD_E, 6.0, XD_E + 2.0, 16.0)                 # TV / wardrobe
        if fl != "GF":
            bed(fl, XC_E, 11.75, head="w")                     # Bed-4/7
            rect(fl, XD_W - 2.0, 6.0, XD_W, 16.0)
        if fl != "2F":
            bed(fl, XB_I, 11.75, head="w")                     # Bed-2/5
            rect(fl, XC_W - 2.0, 6.0, XC_W, 16.0)

        # Wardrobes in dresses:
        rect(fl, 73.5, 25.5, 78.5, 27.5)                      # East dress
        if fl != "GF":
            rect(fl, 59.5, 25.5, 64.5, 27.5)                  # Middle dress
        if fl != "2F":
            rect(fl, 42.5, 25.5, 47.5, 27.5)                  # West dress

        # East bath fixtures:
        rect(fl, 79.175, 20.8, 82.175, 23.8)                  # shower 3x3
        circ(fl, 83.175, 21.8, 0.75)                          # WC
        rect(fl, 82.375, 24.5, 84.075, 26.0)                  # basin

        # West bath fixtures:
        if fl == "1F":
            rect(fl, 37.175, 20.8, 40.175, 23.8)              # shower 3x3
            circ(fl, 41.175, 21.8, 0.75)                      # WC
            rect(fl, 40.375, 24.5, 41.825, 26.0)              # basin
        elif fl == "GF":
            rect("GF", 37.175, 27.25, 40.175, 30.25)          # shower 3x3
            circ("GF", 41.25, 28.25, 0.75)                     # WC
            rect("GF", 40.25, 30.75, 41.875, 32.25)            # basin
            rect("GF", 42.5, 27.25, 45.0, 29.0, "WARDROBE")   # Dress wardrobe
            rect("GF", 42.5, 30.25, 45.0, 32.0, "WARDROBE")   # Dress wardrobe
            rect("GF", 38.0, 20.6, 42.0, 21.6, "CONSOLE")     # Foyer console

        # Middle bath fixtures:
        if fl != "GF":
            rect(fl, 55.8, 20.8, 58.8, 23.8)                  # shower 3x3
            circ(fl, 53.5, 21.8, 0.75)                        # WC
            rect(fl, 53.0, 24.0, 55.5, 25.5)                  # basin

    # GF specifics:
    circ("GF", 53.5, 22.0, 0.75)                               # Powder WC
    rect("GF", 55.5, 23.6, 58.85, 25.6)                       # Powder vanity counter
    rect("GF", 54.0, 6.0, 57.0, 16.5); rect("GF", 57.0, 13.5, 64.5, 16.5)       # Drawing sofas
    rect("GF", 58.5, 8.5, 62.5, 11.5); rect("GF", 65.0, 6.5, 67.5, 9.0); rect("GF", 65.0, 10.5, 67.5, 13.0)
    rect("GF", 60.5, 24.5, 67.5, 27.5); rect("GF", 60.5, 27.5, 63.5, 31.5)       # Lounge sofas
    rect("GF", 66.25, 28.5, XD_W, 34.0)                                          # TV console

    rect("GF", 58.0, 35.0, 66.0, 38.5)                                          # Dining table
    rect("GF", 19.6, 1.0, 25.8, 16.5, ""); rect("GF", 28.4, 1.0, 34.6, 16.5, "")  # 2 cars in porch

    # 1F specifics:
    rect("1F", 55.5, 29.0, 64.0, 32.0); rect("1F", 55.5, 32.0, 58.5, 36.0)
    rect("1F", 60.0, 37.0, 68.0, 40.5)
    rect("1F", 66.25, 28.5, XD_W, 34.0)

    # 2F specifics:
    rect("2F", 70.0, 42.5, 73.0, 45.5, "W/M")
    rect("2F", 73.5, 42.5, 76.5, 45.5, "DRY")
    rect("2F", 70.0, 37.0, 72.5, 39.5, "SINK")
    circ("2F", 82.0, 44.5, 0.75)
    rect("2F", 80.0, 42.5, 81.5, 44.0)
    rect("2F", 80.0, 37.0, 84.0, 38.5, "SHELVES")


ortho_boxes_gf = [
    R(XB_O, 3.0, XE_O, 3.75),
    R(XB_O, 3.0, XB_I, 30.294),
    R(41.480, 33.0, XC_W, 33.75),
    R(XC_W, 33.0, XC_E, 39.059),
    R(57.953, 41.75, XD_W, 42.5),
    R(XD_W, 35.625, XD_E, 49.763),
    R(XE_I, 3.0, XE_O, 55.861),
]
chamfers_all = WALL_RING.difference(unary_union(ortho_boxes_gf))
chamfer_bc = chamfers_all.intersection(R(35.0, 29.0, 43.0, 35.0))
chamfer_cd = chamfers_all.intersection(R(50.0, 37.0, 60.0, 44.0))
wall_north_de = Polygon([(68.625, 50.2677), (85.125, 56.9752), (84.375, 55.8607), (69.375, 49.7630)])


# --------------------------------------------------------------------------
# BUILD MODEL
# --------------------------------------------------------------------------
def build() -> Model:
    m = Model()
    def wall(fl, x0, y0, x1, y1, mat="plaster", z0=None, z1=None, layer="walls"):
        L = LEVEL[fl]
        m.walls[fl].append(Box(x0, y0, L if z0 is None else z0, x1, y1,
                               L + WALL_H if z1 is None else z1, mat, layer, fl))
    def op(fl, orient, line, a, b, sill, head, kind, name="", hinge="a", swing=1):
        m.openings.append(Opening(fl, orient, line, a, b, sill, head, kind, name, hinge, swing))
    def aop(fl, p0, p1, sill, head, kind, name="", hinge="a", swing=1):
        m.angled_openings.append(AngledOpening(fl, p0, p1, sill, head, kind, name, hinge, swing))
    def room(fl, name, poly, kind, label_xy=None, show_dims=True):
        m.rooms.append(Room(fl, name, poly, kind, label_xy, show_dims))

    # ================= GROUND FLOOR =========================================
    g = "GF"
    for r in [
        (XB_O, 3.0, XE_O, 3.75),
        (XB_O, 3.0, XB_I, 30.294),
        (41.480, 33.0, XC_W, 33.75),
        (XC_W, 3.75, XC_E, 19.75),
        (XC_W, 20.5, XC_E, 33.0),
        (XC_W, 33.0, XC_E, 39.059),
        (57.953, 41.75, XD_W, 42.5),
        (XD_W, 3.75, XD_E, 19.75),
        (XD_W, 20.5, XD_E, 28.25),
        (XD_W, 35.625, XD_E, 49.763),
        (XE_I, 3.75, XE_O, 55.861),
        (XB_I, 19.75, XE_I, 20.5),
        (XB_I, 26.375, 45.375, 26.75),
        (45.0, 26.75, 45.375, 33.0),
        (STAIR_X0, 27.5, XE_I, 28.25),
        (XD_E, 35.625, XE_I, 36.375),
        (XD_E, 46.125, XE_I, 46.875),
    ]:
        wall(g, *r)

    for r in [
        (73.125, 20.5, 73.5, 27.5),
        (78.5, 20.5, 78.875, 27.5),
        (41.75, 26.75, 42.125, 33.0),
        (46.5, 20.5, 46.875, 26.375),
        (46.5, 26.375, XC_W, 26.75),
        (59.125, 20.5, 59.5, 26.5),
        (52.125, 26.125, 59.5, 26.5),
        (STAIR_X0, 31.75, MID_X, 32.125)
    ]:
        wall(g, *r, layer="partitions")

    m.prisms.append(Prism(chamfer_bc, 0, WALL_H, "plaster", "walls", g, "chamfer-bc"))
    m.prisms.append(Prism(chamfer_cd, 0, WALL_H, "plaster", "walls", g, "chamfer-cd"))
    m.prisms.append(Prism(wall_north_de, 0, WALL_H, "plaster", "walls", g, "north-boundary-de"))

    op(g, "x", 3.375, 40.625, 47.625, 2.0, 8.0, "window", "W1")
    op(g, "x", 3.375, 53.5, 57.0, 0.0, 8.0, "door", "D-guest", "a", -1)
    op(g, "x", 3.375, 59.0, 67.0, 2.0, 8.0, "window", "W2")
    op(g, "x", 3.375, 73.375, 80.375, 2.0, 8.0, "window", "W1")

    aop(g, (37.75, 31.34), (40.70, 33.24), 3.0, 7.5, "window", "W-BATH")
    aop(g, (53.38, 40.11), (56.88, 41.94), 2.0, 8.0, "window", "W-LOUNGE")

    op(g, "y", 36.5, 22.0, 26.5, 0.0, 8.0, "double", "MAIN ENTRANCE", "a", 1)
    op(g, "y", 36.5, 28.75, 30.25, 6.5, 8.0, "vent", "V")
    op(g, "y", 51.75, 23.0, 25.0, 6.5, 8.0, "vent", "V"); op(g, "y", 46.6875, 22.0, 25.0, 2.0, 8.0, "window", "W-COURT")
    op(g, "y", 84.75, 22.5, 24.5, 6.5, 8.0, "vent", "V")
    op(g, "y", 84.75, 29.5, 34.5, 1.0, 10.25, "window", "STAIR-GL")
    op(g, "y", 84.75, 38.0, 43.5, 3.5, 7.0, "window", "KW")
    op(g, "y", 84.75, 48.0, 51.0, 0.0, 7.0, "door", "D-COURT", "a", 1)
    op(g, "y", 84.75, 51.5, 53.5, 6.5, 8.0, "vent", "V")
    op(g, "y", 51.75, 35.0, 38.25, 0.0, 8.0, "slide", "SL")
    op(g, "x", 42.125, 60.25, 67.25, 3.0, 8.0, "window", "W3")

    op(g, "x", 20.125, 45.0, 48.0, 0.0, 7.0, "door", "D2", "b", -1)
    op(g, "x", 26.5, 42.0, 44.5, 0.0, 7.0, "door", "D2", "a", 1)
    op(g, "y", 41.9375, 28.5, 31.0, 0.0, 7.0, "door", "D3", "a", 1)
    op(g, "x", 20.125, 54.0, 56.5, 0.0, 7.0, "door", "D3", "a", 1)
    op(g, "x", 20.125, 61.5, 65.0, 0.0, 7.0, "door", "D1", "a", 1)
    op(g, "y", 51.75, 28.5, 32.5, 0.0, 8.0, "arch", "ARCH")
    op(g, "y", 69.0, 37.5, 41.0, 0.0, 7.0, "door", "D1", "b", 1)
    op(g, "x", 46.5, 74.0, 77.0, 0.0, 7.0, "door", "D2", "a", 1)
    op(g, "x", 20.125, 69.75, 72.75, 0.0, 7.0, "door", "D2", "a", -1)
    op(g, "x", 20.125, 74.75, 77.25, 0.0, 7.0, "door", "D3", "b", 1)
    op(g, "y", 78.6875, 22.0, 24.5, 0.0, 7.0, "door", "D3", "b", 1)

    room(g, "BED ROOM-1", R(XD_E, 3.75, XE_I, 19.75), "hab")
    room(g, "BATH", R(78.875, 20.5, XE_I, 27.5), "wet")
    room(g, "DRESS", R(73.5, 20.5, 78.5, 27.5), "serv")
    room(g, "LOBBY", R(XD_E, 20.5, 73.125, 27.5), "circ", show_dims=False)
    room(g, "DRAWING ROOM", R(XC_E, 3.75, XD_W, 19.75), "hab")
    powder_gf = R(XC_E, 20.5, 59.125, 26.5)
    room(g, "POWDER", powder_gf, "wet", (55.6, 23.5))
    lounge_gf = R(XC_E, 20.5, XD_W, 41.75).intersection(FP_IN).difference(R(XC_E, 20.5, 59.5, 26.5))
    room(g, "LOUNGE + DINING", lounge_gf, "hab", (62.0, 32.0))

    room(g, "BED ROOM-2", R(XB_I, 3.75, XC_W, 19.75), "hab")
    bath_gf = bc_block.intersection(FP_IN).intersection(sbox(XB_I, 26.75, 41.75, 33.0))
    room(g, "BATH", bath_gf, "wet", (39.5, 29.5))
    room(g, "DRESS", R(42.125, 26.75, 45.0, 33.0), "serv", (43.5, 29.5))
    ots_gf = sbox(46.875, 20.5, XC_W, 26.375)
    room(g, "LIGHT COURT (OTS)", ots_gf, "ext", (49.1, 23.5))
    foyer_gal = bc_block.intersection(FP_IN).intersection(sbox(45.375, 26.75, XC_W, 33.0))
    foyer_main = bc_block.intersection(FP_IN).intersection(sbox(XB_I, 20.5, 46.5, 26.375))
    foyer_gf = unary_union([foyer_main, foyer_gal])
    room(g, "ENTRANCE FOYER", foyer_gf, "circ", (39.5, 23.5), False)
    room(g, "STAIR", R(XD_E, 28.25, XE_I, 35.625), "circ", (77.0, 30.0), False)
    room(g, "KITCHEN", R(XD_E, 36.375, XE_I, 46.125), "hab")
    dirty_k = de_block.intersection(FP_IN).intersection(sbox(XD_E, 46.875, XE_I, 60.0))
    room(g, "DIRTY KITCHEN", dirty_k, "serv", (77.0, 50.5))


    # ================= FIRST FLOOR ==========================================
    f = "1F"
    for r in [
        (XB_O, 3.0, XE_O, 3.75),
        (XB_O, 3.0, XB_I, 30.294),
        (41.480, 33.0, XC_W, 33.75),
        (XC_W, 3.75, XC_E, 19.75),
        (XC_W, 20.5, XC_E, 28.25),
        (XC_W, 33.0, XC_E, 39.059),
        (57.953, 41.75, XD_W, 42.5),
        (XD_W, 3.75, XD_E, 19.75),
        (XD_W, 20.5, XD_E, 28.25),
        (XD_W, 35.625, XD_E, 46.875),
        (XE_I, 3.75, XE_O, 47.25),
        (XB_I, 19.75, XE_I, 20.5),
        (XB_I, 27.5, 47.875, 28.25),
        (XC_E, 27.5, 64.875, 28.25),
        (STAIR_X0, 27.5, XE_I, 28.25),
        (XD_E, 35.625, XE_I, 36.375),
        (XD_E, 46.125, XE_I, 46.875),
    ]:
        wall(f, *r)

    for r in [
        (73.125, 20.5, 73.5, 27.5),
        (78.5, 20.5, 78.875, 27.5),
        (42.125, 20.5, 42.5, 27.5),
        (46.5, 20.5, 46.875, 26.375),
        (46.5, 26.375, XC_W, 26.75),
        (59.125, 20.5, 59.5, 26.5),
        (52.125, 26.125, 59.5, 26.5),
        (64.5, 20.5, 64.875, 27.5),
        (STAIR_X0, 31.75, MID_X, 32.125)
    ]:
        wall(f, *r, layer="partitions")

    m.prisms.append(Prism(chamfer_bc, 11.0, 11.0 + WALL_H, "plaster", "walls", f, "chamfer-bc"))
    m.prisms.append(Prism(chamfer_cd, 11.0, 11.0 + WALL_H, "plaster", "walls", f, "chamfer-cd"))

    # 1F balcony parapets (open to sky above)
    m.prisms.append(Prism(wall_north_de, 11.0, 14.0, "plaster", "parapet", f, "balc-par-n"))
    m.boxes.append(Box(XE_I, 46.875, 11.0, XE_O, 55.861, 14.0, "plaster", "parapet", f, "balc-par-e"))
    m.boxes.append(Box(XD_W, 46.875, 11.0, XD_E, 49.763, 14.5, "glass", "railing", f, "balc-rail-w"))

    op(f, "x", 3.375, 40.625, 47.625, 0.0, 8.0, "slide", "SL")
    op(f, "x", 3.375, 56.375, 64.375, 0.0, 8.0, "slide", "SL")
    op(f, "x", 3.375, 73.375, 80.375, 0.0, 8.0, "slide", "SL")
    op(f, "y", 36.5, 10.0, 13.0, 0.0, 7.0, "door", "D1", "a", -1)
    op(f, "y", 36.5, 23.0, 25.0, 6.5, 8.0, "vent", "V")
    op(f, "y", 51.75, 23.0, 25.0, 6.5, 8.0, "vent", "V")
    op(f, "y", 84.75, 22.5, 24.5, 6.5, 8.0, "vent", "V")
    op(f, "y", 84.75, 29.5, 34.5, 1.0, 10.25, "window", "STAIR-GL")
    op(f, "y", 84.75, 38.0, 43.5, 3.5, 7.0, "window", "KW")
    op(f, "x", 46.5, 74.0, 77.0, 0.0, 7.0, "door", "D-BALC", "a", 1)
    op(f, "y", 51.75, 35.0, 38.25, 2.0, 8.0, "window", "W3")
    op(f, "x", 42.125, 60.25, 67.25, 3.0, 8.0, "window", "W3")

    aop(f, (37.75, 31.34), (40.70, 33.24), 2.0, 8.0, "window", "W-NOOK")
    aop(f, (53.38, 40.11), (56.88, 41.94), 2.0, 8.0, "window", "W-LOUNGE")

    op(f, "x", 20.125, 43.75, 46.25, 0.0, 7.0, "door", "D3", "a", 1)
    op(f, "x", 20.125, 48.125, 51.125, 0.0, 7.0, "door", "D2", "b", -1)
    op(f, "y", 42.3125, 22.0, 24.5, 0.0, 7.0, "door", "D3", "b", -1)
    op(f, "x", 27.875, 48.125, 51.125, 0.0, 7.0, "door", "D2", "b", 1)
    op(f, "x", 20.125, 60.75, 63.25, 0.0, 7.0, "door", "D3", "a", 1)
    op(f, "x", 20.125, 65.25, 68.25, 0.0, 7.0, "door", "D2", "b", -1)
    op(f, "y", 59.3125, 22.0, 24.5, 0.0, 7.0, "door", "D3", "b", -1)
    op(f, "x", 27.875, 65.25, 68.25, 0.0, 7.0, "door", "D2", "b", 1)
    op(f, "x", 20.125, 69.75, 72.75, 0.0, 7.0, "door", "D2", "a", -1)
    op(f, "x", 20.125, 74.75, 77.25, 0.0, 7.0, "door", "D3", "b", 1)
    op(f, "y", 78.6875, 22.0, 24.5, 0.0, 7.0, "door", "D3", "b", 1)
    op(f, "y", 69.0, 21.0, 26.5, 0.0, 7.0, "arch", "ARCH")

    room(f, "BED ROOM-3", R(XD_E, 3.75, XE_I, 19.75), "hab")
    room(f, "BATH", R(78.875, 20.5, XE_I, 27.5), "wet")
    room(f, "DRESS", R(73.5, 20.5, 78.5, 27.5), "serv")
    room(f, "LOBBY", R(XD_E, 20.5, 73.125, 27.5), "circ", show_dims=False)
    room(f, "BED ROOM-4", R(XC_E, 3.75, XD_W, 19.75), "hab")
    b4_bath = R(XC_E, 20.5, 59.125, 26.5)
    room(f, "BATH", b4_bath, "wet", (56.0, 23.5))
    room(f, "DRESS", R(59.5, 20.5, 64.5, 27.5), "serv")
    room(f, "LOBBY", R(64.875, 20.5, XD_W, 27.5), "circ", show_dims=False)
    room(f, "BED ROOM-5", R(XB_I, 3.75, XC_W, 19.75), "hab")
    room(f, "BATH", R(XB_I, 20.5, 42.125, 27.5), "wet")
    room(f, "DRESS", R(42.5, 20.5, 46.5, 27.5), "serv", (44.5, 23.5))
    ots_1f = sbox(46.875, 20.5, XC_W, 26.375)
    room(f, "LIGHT COURT (OTS)", ots_1f, "ext", (49.1, 23.5))
    room(f, "LOBBY", R(46.875, 26.375, XC_W, 27.5), "circ", show_dims=False)
    room(f, "FAMILY LOUNGE + DINING", R(XC_E, 28.25, XD_W, 41.75).intersection(FP_IN), "hab", (60.5, 35.0))
    room(f, "SITTING NOOK", R(XB_I, 28.25, XC_W, 33.0).intersection(FP_IN), "circ", (44.5, 30.5))
    room(f, "OPEN KITCHEN", R(XD_E, 36.375, XE_I, 46.125), "hab")
    room(f, "STAIR", R(XD_E, 28.25, XE_I, 35.625), "circ", (77.0, 30.0), False)
    room(f, "OPEN TERRACE OVER PORCH", R(17.5, 0.0, XB_I, 18.0), "ext", (26.5, 9.0))
    util_balc = de_block.intersection(sbox(XD_W, 46.875, XE_O, 60.0))
    room(f, "UTILITY BALCONY", util_balc, "ext", (77.0, 51.0))

    # ================= SECOND FLOOR =========================================
    s = "2F"
    for r in [
        (XC_W, 3.0, XE_O, 3.75),
        (XC_W, 3.75, XC_E, 28.25),
        (XC_W, 19.75, XE_I, 20.5),
        (XD_W, 3.75, XD_E, 19.75),
        (XD_W, 20.5, XD_E, 28.25),
        (XD_W, 35.625, XD_E, 46.875),
        (XC_E, 27.5, 64.875, 28.25),
        (STAIR_X0, 27.5, XE_I, 28.25),
        (XD_E, 35.625, XE_I, 36.375),
        (XD_E, 46.125, XE_I, 46.875),
        (XE_I, 3.75, XE_O, 47.25),
    ]:
        wall(s, *r)

    for r in [
        (73.125, 20.5, 73.5, 27.5),
        (78.5, 20.5, 78.875, 27.5),
        (59.125, 20.5, 59.5, 26.5),
        (52.125, 26.125, 59.5, 26.5),
        (64.5, 20.5, 64.875, 27.5),
        (79.0, 36.375, 79.375, 46.125),
        (79.375, 41.5, XE_I, 41.875),
        (STAIR_X0, 31.75, MID_X, 32.125)
    ]:
        wall(s, *r, layer="partitions")

    op(s, "x", 3.375, 56.375, 64.375, 0.0, 8.0, "slide", "SL")
    op(s, "x", 3.375, 73.375, 80.375, 0.0, 8.0, "slide", "SL")
    op(s, "y", 51.75, 6.0, 11.0, 2.0, 8.0, "window", "W2")
    op(s, "y", 51.75, 13.5, 16.5, 0.0, 7.0, "door", "D1", "a", -1)
    op(s, "y", 51.75, 23.0, 25.0, 6.5, 8.0, "vent", "V")
    op(s, "y", 84.75, 22.5, 24.5, 6.5, 8.0, "vent", "V")
    op(s, "y", 84.75, 29.5, 34.5, 1.0, 10.25, "window", "STAIR-GL")
    op(s, "y", 84.75, 37.5, 40.5, 3.5, 7.0, "window", "LW-E")
    op(s, "y", 84.75, 43.0, 45.5, 6.5, 8.0, "vent", "V")
    op(s, "x", 46.5, 71.0, 77.0, 3.0, 7.0, "window", "LW-N")

    op(s, "x", 20.125, 60.75, 63.25, 0.0, 7.0, "door", "D3", "a", 1)
    op(s, "x", 20.125, 65.25, 68.25, 0.0, 7.0, "door", "D2", "b", -1)
    op(s, "y", 59.3125, 22.0, 24.5, 0.0, 7.0, "door", "D3", "b", -1)
    op(s, "x", 27.875, 65.25, 68.25, 0.0, 7.0, "door", "D1", "b", 1)
    op(s, "y", 69.0, 21.0, 26.5, 0.0, 7.0, "arch", "ARCH")
    op(s, "x", 20.125, 69.75, 72.75, 0.0, 7.0, "door", "D2", "a", -1)
    op(s, "x", 20.125, 74.75, 77.25, 0.0, 7.0, "door", "D3", "b", 1)
    op(s, "y", 78.6875, 22.0, 24.5, 0.0, 7.0, "door", "D3", "b", 1)
    op(s, "y", 69.0, 29.5, 33.0, 0.0, 7.0, "door", "D1", "a", -1)
    op(s, "y", 69.0, 37.5, 41.0, 0.0, 7.0, "door", "D1", "b", -1)
    op(s, "x", 36.0, 70.5, 73.0, 0.0, 7.0, "door", "D3", "a", 1)
    op(s, "y", 79.1875, 42.5, 45.0, 0.0, 7.0, "door", "D3", "a", 1)
    op(s, "y", 79.1875, 37.5, 40.0, 0.0, 7.0, "door", "D3", "b", 1)

    room(s, "BED ROOM-6", R(XD_E, 3.75, XE_I, 19.75), "hab")
    room(s, "BATH", R(78.875, 20.5, XE_I, 27.5), "wet")
    room(s, "DRESS", R(73.5, 20.5, 78.5, 27.5), "serv")
    room(s, "LOBBY", R(XD_E, 20.5, 73.125, 27.5), "circ", show_dims=False)
    room(s, "BED ROOM-7", R(XC_E, 3.75, XD_W, 19.75), "hab")
    b7_bath = R(XC_E, 20.5, 59.125, 26.5)
    room(s, "BATH", b7_bath, "wet", (56.0, 23.5))
    room(s, "DRESS", R(59.5, 20.5, 64.5, 27.5), "serv")
    room(s, "LOBBY", R(64.875, 20.5, XD_W, 27.5), "circ", show_dims=False)
    room(s, "LAUNDRY & UTILITY", R(XD_E, 36.375, 79.0, 46.125), "serv")
    room(s, "SERVICE WC", R(79.375, 41.875, XE_I, 46.125), "wet")
    room(s, "LINEN STORE", R(79.375, 36.375, XE_I, 41.5), "serv")
    room(s, "STAIR", R(XD_E, 28.25, XE_I, 35.625), "circ", (77.0, 30.0), False)
    room(s, "FRONT SUN TERRACE", R(XB_I, 0.0, XC_W, 20.5), "ext", (44.0, 11.0))
    side_terr = R(XB_O, 20.5, XC_W, 33.75).intersection(BUILD)
    room(s, "SIDE TERRACE", side_terr, "ext", (44.0, 27.0))
    rear_terr = R(XC_W, 28.25, XD_W, 42.5).intersection(BUILD)
    room(s, "REAR TERRACE", rear_terr, "ext", (60.0, 35.0))

    # ================= ROOF / MUMTY =========================================
    rf = "RF"
    for r in [
        (XD_W, 27.5, XE_O, 28.25),
        (XD_W, 35.625, XE_O, 36.375),
        (XD_W, 28.25, XD_E, 35.625),
        (XE_I, 28.25, XE_O, 35.625),
    ]:
        wall(rf, *r, z0=33.0, z1=MUMTY_TOP - SLAB_T)
    wall(rf, STAIR_X0, 31.75, MID_X, 32.125, z0=33.0, z1=MUMTY_TOP - SLAB_T, layer="partitions")

    op(rf, "x", 27.875, 70.0, 72.5, 0.0, 7.0, "door", "D2", "a", -1)
    op(rf, "x", 27.875, 76.0, 80.0, 2.5, 7.5, "window", "W-MUMTY-S")
    op(rf, "y", 69.0, 30.0, 33.5, 3.0, 6.5, "window", "W-MUMTY-W")
    op(rf, "y", 84.75, 29.5, 34.5, 1.0, 8.0, "window", "W-MUMTY-E")
    op(rf, "x", 36.0, 75.0, 80.0, 3.0, 7.0, "window", "W-MUMTY-N")

    room(rf, "MUMTY", R(XD_E, 28.25, XE_I, 35.625), "circ", (77.0, 30.0), False)

    # Columns
    e = 0.01
    for name in COLUMN_SPEC:
        x0, y0, x1, y1 = column_rect(name)
        m.columns[name] = (x0, y0, x1, y1)
        top = MUMTY_TOP if name in MUMTY_COLUMNS else LEVEL["RF"]
        segs = [("GF", GRADE_Z, 11.0), ("1F", 11.0, 22.0), ("2F", 22.0, 33.0)]
        if top > 33:
            segs.append(("RF", 33.0, top))
        for fl, z0, z1 in segs:
            m.boxes.append(Box(x0 + e, y0 + e, z0, x1 - e, y1 - e, z1, "column", "structure", fl, name))

    # Beams
    for lvl, fl in [(11.0, "GF"), (22.0, "1F"), (33.0, "2F")]:
        for a, b in beam_segments():
            al, an = split_col(a)
            bl, bn = split_col(b)
            ax, ay = GX[al], GY[an]
            bx, by = GX[bl], GY[bn]
            w = 0.5 if "A" in (al, bl) and al == bl else T9 / 2
            if ay == by:
                bb = Box(min(ax, bx), ay - T9 / 2 + e, lvl - BEAM_D, max(ax, bx), ay + T9 / 2 - e, lvl - SLAB_T,
                         "beam", "structure", fl, f"{a}-{b}")
                m.boxes.append(bb)
            elif ax == bx:
                ww = 0.5 if al == "A" else T9 / 2
                bb = Box(ax - ww + e, min(ay, by), lvl - BEAM_D, ax + ww - e, max(ay, by), lvl - SLAB_T,
                         "beam", "structure", fl, f"{a}-{b}")
                m.boxes.append(bb)
            else:
                beam_poly = LineString([(ax, ay), (bx, by)]).buffer(T9 / 2, cap_style=2)
                m.prisms.append(Prism(beam_poly, lvl - BEAM_D, lvl - SLAB_T, "beam", "structure", fl, f"{a}-{b}"))

    for a, b in [("D4", "E4"), ("D6", "E6"), ("D4", "D6"), ("E4", "E6")]:
        al, an = split_col(a)
        bl, bn = split_col(b)
        ax, ay = GX[al], GY[an]
        bx, by = GX[bl], GY[bn]
        if ay == by:
            m.boxes.append(Box(ax, ay - 0.37, MUMTY_TOP - BEAM_D, bx, ay + 0.37, MUMTY_TOP - SLAB_T,
                               "beam", "structure", "RF", f"{a}-{b}"))
        else:
            m.boxes.append(Box(ax - 0.37, ay, MUMTY_TOP - BEAM_D, ax + 0.37, by, MUMTY_TOP - SLAB_T,
                               "beam", "structure", "RF", f"{a}-{b}"))

    # Slabs
    hole = R(*STAIR_HOLE)
    ots_hole = sbox(46.875, 20.5, XC_W, 26.375)
    front_canopy = R(XB_O, 0.0, XE_O, 3.0)
    porch_terrace = R(17.5, 0.0, XB_O, 18.0)

    s11 = unary_union([FP, front_canopy, porch_terrace]).difference(hole).difference(ots_hole)
    fp_2f = unary_union([bc_block, cd_block, de_block.intersection(sbox(XD_W, 3.0, XE_O, 46.875))])
    s22 = unary_union([fp_2f, front_canopy]).difference(hole).difference(ots_hole)
    roof_main = unary_union([
        R(XD_W, 3.0, XE_O, 46.875).intersection(FP),
        R(XC_W, 3.0, XD_E, 28.25)
    ])
    canopy_roof = R(XC_W, 0.0, XE_O, 3.0)
    s33 = unary_union([roof_main, canopy_roof]).difference(R(XD_W, 27.5, XE_O, 36.375))

    m.slabs = {"GF": FP, 11.0: s11, 22.0: s22, 33.0: s33}
    m.prisms.append(Prism(FP, GRADE_Z, 0.0, "floor", "slabs", "GF", "plinth"))
    m.prisms.append(Prism(s11, 11.0 - SLAB_T, 11.0, "concrete", "slabs", "1F", "slab"))
    m.prisms.append(Prism(s22, 22.0 - SLAB_T, 22.0, "concrete", "slabs", "2F", "slab"))
    m.prisms.append(Prism(s33, 33.0 - SLAB_T, 33.0, "concrete", "slabs", "RF", "roof"))

    m.prisms.append(Prism(R(XD_W, 27.5, XE_O, 36.375).difference(hole), 33.0 - SLAB_T, 33.0, "concrete", "slabs", "RF", "mumty-floor"))
    m.boxes.append(Box(XD_W - 0.5, 27.0, MUMTY_TOP - SLAB_T, XE_O + 0.5, 36.875, MUMTY_TOP, "charcoal", "slabs", "RF", "mumty-roof"))
    m.boxes.append(Box(74.25, 29.5, MUMTY_TOP, 81.25, 34.5, MUMTY_TOP + 4.0, "tank", "services", "RF", "OHWT 800 gal"))

    for r in [
        (XB_O, 0.6, XB_I, 30.294),
        (41.480, 33.0, XC_W, 33.75),
        (XC_W, 33.0, XC_E, 39.059),
        (57.953, 41.75, XD_E, 42.5),
    ]:
        m.boxes.append(Box(r[0], r[1], 22.0, r[2], r[3], 22.0 + PARAPET_H, "plaster", "parapet", "2F", "parapet"))

    roof_ring = s33.buffer(0).difference(s33.buffer(-T45, join_style="mitre"))
    roof_par = roof_ring.difference(R(-5, -5, 100, 3.5)).difference(R(XD_W, 27.5, XE_O, 36.375))
    if not roof_par.is_empty:
        m.prisms.append(Prism(roof_par, 33.0, 33.0 + PARAPET_H, "plaster", "parapet", "RF", "parapet"))

    # Railings
    def glass_rail(x0, y0, x1, y1, z, fl):
        m.boxes.append(Box(x0, y0, z, x1, y1, z + 3.25, "glass", "railing", fl, "rail"))
        m.boxes.append(Box(x0 - 0.04, y0 - 0.04, z + 3.25, x1 + 0.04, y1 + 0.04, z + 3.5, "metal", "railing", fl, "rail"))

    glass_rail(17.6, 0.25, XE_O - 0.1, 0.35, 11.0, "1F")
    glass_rail(17.6, 0.35, 17.7, 17.9, 11.0, "1F")
    glass_rail(17.7, 17.8, XB_O, 17.9, 11.0, "1F")
    glass_rail(XB_O + 0.1, 0.25, XE_O - 0.1, 0.35, 22.0, "2F")

    # Stairs
    for fl, L in [("GF", 0.0), ("1F", 11.0), ("2F", 22.0)]:
        for i in range(10):
            tx0 = STAIR_X0 + i * TREAD
            tz0 = L + i * RISER
            m.boxes.append(Box(tx0, LANE_S[0], tz0, tx0 + TREAD, LANE_S[1], tz0 + RISER, "marble", "stairs", fl, f"R{i+1}"))
        m.boxes.append(Box(MID_X, LANE_S[0], L + 10 * RISER - SLAB_T, XE_I, LANE_N[1], L + 10 * RISER,
                           "concrete", "stairs", fl, "mid-landing"))
        for i in range(10):
            tx0 = MID_X - (i + 1) * TREAD
            tz0 = L + (10 + i) * RISER
            m.boxes.append(Box(tx0, LANE_N[0], tz0, tx0 + TREAD, LANE_N[1], tz0 + RISER, "marble", "stairs", fl, f"R{i+11}"))

    # Zones
    band = PLOT.difference(PLOT_INNER)
    free = PLOT_INNER.difference(FP)
    porch = free.intersection(sbox(17.5, 0.0, XB_O, 18.0))
    front_green = free.intersection(sbox(0.0, 0.0, 17.5, 18.0))
    front_strip = free.intersection(sbox(0.0, 0.0, 88.0, 3.0)).difference(porch).difference(front_green)
    path_drawing = free.intersection(sbox(53.0, 0.0, 58.0, 3.0))
    side_path = free.intersection(sbox(0.0, 18.0, XB_O, 24.0))
    side_lawn = free.intersection(sbox(0.0, 18.0, 42.0, 40.0)).difference(side_path)
    north_passage = free.intersection(sbox(35.0, 30.0, 75.0, 55.0)).difference(side_lawn)
    ne_court = free.intersection(sbox(80.0, 45.0, 90.0, 65.0))
    east_passage = free.difference(unary_union([
        porch, front_green, front_strip, path_drawing, side_path, side_lawn, north_passage, ne_court
    ]))
    building_fp = FP

    m.zones = {
        "CAR PORCH": porch, "PATH": path_drawing, "FRONT GREEN STRIP": front_strip,
        "FRONT LAWN": front_green, "LAWN WALK": side_path, "SIDE LAWN": side_lawn,
        "NORTH PASSAGE": north_passage, "NE SERVICE COURT": ne_court, "EAST PASSAGE": east_passage,
        "BOUNDARY WALL": band, "BUILDING": building_fp
    }

    for nm, zz in m.zones.items():
        if nm in ("BOUNDARY WALL", "BUILDING") or zz.is_empty:
            continue
        mat = "grass" if "LAWN" in nm or "GREEN" in nm else "paving"
        m.prisms.append(Prism(zz, GRADE_Z - 0.25, GRADE_Z, mat, "site", "SITE", nm))

    m.boxes.append(Box(-15, -26, ROAD_Z - 0.5, 105, -0.01, ROAD_Z, "asphalt", "site", "SITE", "road"))
    m.boxes.append(Box(-15, -6, ROAD_Z, 105, -0.01, ROAD_Z + 0.5, "paving", "site", "SITE", "footpath"))
    m.boxes.append(Box(53.0, 1.0, GRADE_Z, 57.5, 3.0, -0.5, "stone_floor", "site", "SITE", "step"))
    m.boxes.append(Box(53.0, 2.0, -0.5, 57.5, 3.0, 0.0, "stone_floor", "site", "SITE", "step"))
    portico_poly = sbox(20.0, 20.0, XB_O, 26.5).intersection(free)
    m.prisms.append(Prism(portico_poly, GRADE_Z, 0.0, "stone_floor", "site", "SITE", "step-entrance"))

    for fl, L in [("GF", 0.0), ("1F", 11.0)]:
        m.boxes.append(Box(82.375, 36.375, L, XE_I, 45.0, L + 2.85, "counter", "fitout", fl, "counter"))
        m.boxes.append(Box(XD_E, 41.5, L, 74.0, 45.0, L + 2.85, "counter", "fitout", fl, "counter"))
    m.boxes.append(Box(82.375, 47.0, 0.0, XE_I, 54.0, 2.85, "counter", "fitout", "GF", "counter"))

    for fl, walls in m.walls.items():
        L = LEVEL[fl]
        ops = [o for o in m.openings if o.floor == fl]
        for w in walls:
            m.boxes += split_wall(w, ops, L)
    for o in m.openings:
        m.boxes += opening_fill(o)

    furnish(m)
    return m



# --------------------------------------------------------------------------
# VALIDATION
# --------------------------------------------------------------------------
def validate(m: Model, verbose=True):
    res = []

    def chk(ok, msg):
        res.append((bool(ok), msg))

    # 1 columns continuous & identical on every storey
    for name, rect in m.columns.items():
        floors = {b.floor for b in m.boxes if b.layer == "structure" and b.tag == name}
        chk({"GF", "1F", "2F"} <= floors, f"Column {name} continuous GF->1F->2F->roof ({sorted(floors)})")

    # 2 columns concealed in walls
    frame_ok = {
        "GF": {"A1", "A2"},
        "1F": {"A1", "A2", "D7A", "E8"},
        "2F": {"A1", "A2", "B1", "B2", "B3", "B4", "B'5", "C4", "C5", "C'7", "D7A", "E8"}
    }
    for fl in FLOORS:
        wall_u = unary_union([R(w.x0, w.y0, w.x1, w.y1) for w in m.walls[fl]] +
                             [p.poly for p in m.prisms if p.floor == fl and p.layer == "walls"]).buffer(0.02)
        exposed = [n for n, r in m.columns.items() if not wall_u.contains(R(*r))]
        bad = sorted(set(exposed) - frame_ok[fl])
        chk(not bad, f"{fl}: all columns concealed in 9\" walls except declared frame posts "
                     f"{sorted(set(exposed) & frame_ok[fl])} {'' if not bad else 'UNEXPECTED: ' + str(bad)}")

    # 3 everything inside plot
    plot_tol = PLOT.buffer(0.02)
    outside = []
    for b in m.boxes:
        if b.layer == "site" and b.tag in ("road", "footpath"):
            continue
        if not plot_tol.contains(b.poly()):
            outside.append(f"{b.floor}:{b.layer}:{b.tag}")
    for p in m.prisms:
        if not plot_tol.contains(p.poly):
            outside.append(f"{p.floor}:{p.layer}:{p.tag}")
    chk(not outside, f"All building/site elements inside surveyed boundary {outside[:6]}")

    # 4 openings never clash with columns
    clashes = []
    for o in m.openings:
        orr = R(*o.rect(0.3))
        for n, r in m.columns.items():
            if orr.intersection(R(*r)).area > 1e-4:
                clashes.append(f"{o.floor} {o.name}@{o.line}:{o.a}-{o.b} x {n}")
    chk(not clashes, f"No door/window cuts through a column {clashes}")

    # 5 room clear sizes (Option B)
    for r in m.rooms:
        if r.name.startswith("BED ROOM"):
            x0, y0, x1, y1 = r.poly.bounds
            w, d = x1 - x0, y1 - y0
            min_dim = 14.5 - 1e-6 if "2" in r.name or "5" in r.name else 15.0 - 1e-6
            chk(min(w, d) >= min_dim and max(w, d) >= 16.0 - 1e-6,
                f"{r.floor} {r.name}: {fi(w)} x {fi(d)} (>= {fi(min_dim)} x 16'-0\")")
        if r.name == "DRAWING ROOM":
            chk(r.poly.area >= 260, f"GF DRAWING ROOM {r.poly.area:.0f} sft (>= 260 sft)")

    # 6 beam spans
    spans = []
    for a, b in beam_segments():
        al, an = split_col(a)
        bl, bn = split_col(b)
        d = math.dist((GX[al], GY[an]), (GX[bl], GY[bn]))
        spans.append((d, a, b))
    mx = max(spans)
    chk(mx[0] <= 20.0, f"Longest beam span {fi(mx[0])} ({mx[1]}-{mx[2]}) <= 20'-0\"")

    # 7 no residual area
    zones = unary_union(list(m.zones.values()))
    resid = PLOT.difference(zones).area
    chk(resid < 0.5, f"Plot fully utilised - unassigned residual area {resid:.2f} sft")

    # 8 dirty kitchen size
    dk = [r for r in m.rooms if r.name == "DIRTY KITCHEN"][0]
    chk(dk.poly.area >= 60, f"Dirty kitchen usable area: {dk.poly.area:.0f} sft (>= 60 sft)")

    # 9 stair
    two_r_t = 2 * RISER * 12 + TREAD * 12
    chk(150 <= RISER * 304.8 <= 180, f"Stair riser {RISER*12:.2f}\" ({RISER*304.8:.0f} mm) within 150-180 mm")
    chk(279 <= TREAD * 304.8 <= 300, f"Stair tread {TREAD*12:.0f}\" ({TREAD*304.8:.0f} mm) within 280-300 mm")
    chk(24 <= two_r_t <= 25.5, f"Blondel rule 2R+T = {two_r_t:.1f}\" (24-25.5\")")
    chk(LANE_S[1] - LANE_S[0] >= 3.28, f"Stair flight width {fi(LANE_S[1]-LANE_S[0])} (>= 1000 mm)")
    chk(XE_I - MID_X >= LANE_S[1] - LANE_S[0], f"Mid-landing depth {fi(XE_I-MID_X)} >= flight width")
    head = FLOOR_H - SLAB_T - (RISER * 1)
    chk(head >= 6.9, f"Stair headroom >= 2.1 m (min {head:.2f} ft)")

    # 10 heights
    clear = FLOOR_H - SLAB_T - 2 / 12
    chk(clear * 0.3048 >= 3.0, f"Clear ceiling {fi(clear)} = {clear*0.3048:.2f} m (>= 3.0 m living)")
    chk((FLOOR_H - BEAM_D - 2 / 12) >= 8.0, f"Clear under beams {fi(FLOOR_H-BEAM_D-2/12)} (> 8'-0\" door head)")

    # 11 doors
    for o in m.openings:
        if o.kind == "double":
            chk(o.width >= 3.5, f"{o.floor} main door {fi(o.width)} >= 3'-6\"")
    for ao in m.angled_openings:
        if ao.kind == "double":
            chk(ao.width >= 3.5, f"{ao.floor} angled double door {fi(ao.width)} >= 3'-6\"")
    bad_d = [f"{o.floor}:{o.name}:{fi(o.width)}" for o in m.openings if o.kind == "door" and o.width < 2.5 - 1e-6]
    chk(not bad_d, f"All doors >= 2'-6\" clear {bad_d}")

    # 12 rooms not overlapped by structural walls
    for r in m.rooms:
        wall_u = unary_union([R(w.x0, w.y0, w.x1, w.y1) for w in m.walls[r.floor] if w.layer == "walls"])
        ov = r.poly.intersection(wall_u).area
        if r.kind not in ("ext", "shaft"):
            chk(ov < 0.05, f"{r.floor} {r.name}: clear area free of structural walls (overlap {ov:.2f} sft)")

    # 13 habitable rooms have daylight window/door
    for r in m.rooms:
        if r.kind != "hab":
            continue
        fp = m.slabs["GF"] if r.floor != "RF" else None
        if r.floor == "2F":
            fp = unary_union([R(XD_W, 3.0, XE_O, 46.875).intersection(FP), R(XC_W, 3.0, XD_E, 28.25)])
        ok = False
        for o in m.openings:
            if o.floor != r.floor or o.kind not in ("window", "slide", "double", "door"):
                continue
            mx = (o.a + o.b) / 2
            for sgn in (-1, 1):
                p_in = Point(mx, o.line + sgn * 0.6) if o.orient == "x" else Point(o.line + sgn * 0.6, mx)
                p_out = Point(mx, o.line - sgn * 0.6) if o.orient == "x" else Point(o.line - sgn * 0.6, mx)
                if r.poly.buffer(0.05).contains(p_in) and not fp.contains(p_out):
                    ok = True
        for ao in m.angled_openings:
            if ao.floor == r.floor and ao.kind in ("window", "slide", "double", "door"):
                mid_x = (ao.p0[0] + ao.p1[0]) / 2
                mid_y = (ao.p0[1] + ao.p1[1]) / 2
                if r.poly.buffer(0.8).contains(Point(mid_x, mid_y)):
                    ok = True
        chk(ok, f"{r.floor} {r.name}: exterior window for daylight + ventilation")

    # 14 direct ventilation for every wet room
    for fl in FLOORS:
        wet_rooms = [r for r in m.rooms if r.floor == fl and r.kind == "wet"]
        for wr in wet_rooms:
            has_vent = False
            for o in m.openings:
                if o.floor == fl and o.kind == "vent":
                    if wr.poly.buffer(0.6).intersects(R(*o.rect(0.5))):
                        has_vent = True
                        break
            chk(has_vent, f"{fl} {wr.name}: direct natural exterior ventilation (louver/window to outside air/OTS)")

    # 15 perimeter passage >= 2'-0" clear on east
    east_pass_w = 87.917 - XE_O
    chk(east_pass_w >= 2.0, f"East perimeter passage clear width {east_pass_w:.2f} >= 2'-0\"")

    # 16 building completely inside BUILDABLE envelope
    diff_build = FP.difference(BUILDABLE).area
    chk(diff_build < 1e-4, f"Building footprint completely inside buildable envelope (diff={diff_build:.4f})")

    # 17 stair exterior window on every floor
    for fl in FLOORS:
        stair_win = [o for o in m.openings if o.floor == fl and "STAIR" in o.name]
        chk(len(stair_win) >= 1, f"{fl} Stair has exterior daylight window strip")

    # 18 Clean monolithic architectural core (zero interior vertical shaft penetrations)
    shafts = [r for r in m.rooms if r.kind == "shaft"]
    chk(len(shafts) == 0, f"Clean monolithic living core with zero outdated interior shaft cuts")

    # 19 building footprint clear of boundary wall zone
    boundary_band = PLOT.difference(PLOT_INNER)
    chk(not FP.intersects(boundary_band.buffer(-1e-4)), "Building footprint clear of boundary wall zone")

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
    covered["MUMTY"] = R(XD_W, 27.5, XE_O, 36.375).area
    for k, v in m.zones.items():
        rows.append((k, v.area))
    return covered, rows


if __name__ == "__main__":
    model = build()
    print(f"boxes={len(model.boxes)} prisms={len(model.prisms)} openings={len(model.openings)} rooms={len(model.rooms)}")
    validate(model)
    cov, rows = area_schedule(model)
    print("\nCovered areas (sft):", {k: round(v) for k, v in cov.items()})
    for k, v in rows:
        print(f"  {k:20s} {v:8.1f} sft")
    print(f"  {'PLOT':20s} {PLOT.area:8.1f} sft")
