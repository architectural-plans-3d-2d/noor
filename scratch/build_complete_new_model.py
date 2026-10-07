"""
Complete Single-Source-of-Truth Model for Daata Hamlet Residence (New Scheme)
"""
from __future__ import annotations
import math
import re
from dataclasses import dataclass, field
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

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
# XB: Bed-2 West wall / Lawn East edge
# XC: Bed-2 East wall / Bath-Dress West wall
# XC_PRIME: Bath-Dress East wall / Car Porch West wall
# XD: Car Porch East wall / Stair East wall / Drawing West wall
# XE: East wing wall (2'-1" clear passage from east boundary)

XB_W, XB_E = 36.125, 36.875
XC_W, XC_E = 51.375, 52.125
XC_P_W, XC_P_E = 56.625, 57.375
XD_W, XD_E = 68.625, 69.375
XE_W, XE_E = 84.375, 85.125

# Footprint envelope blocks
b_lawn = sbox(0.0, 0.0, XB_W, 20.5).intersection(PLOT_INNER)
b_sw = sbox(XB_W, 3.0, XC_P_E, 20.5).intersection(BUILD)
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
    s = f"{int(rem)}" if rem == int(rem) else f"{int(rem)}\u00bd"
    return f"{'-' if neg else ''}{ft}'-{s}\""


print("Data classes and grid defined.")
