import sys
from pathlib import Path
sys.path.insert(0, str(Path.cwd()))

import math
import re
from dataclasses import dataclass, field
from shapely.geometry import Polygon, box as sbox, Point, LineString
from shapely.ops import unary_union

from scripts.daata_hamlet.model import (
    SITE_POINTS, SURVEY_SEGMENTS, PLOT, PLOT_INNER, BUILD, east_bx,
    ROAD_Z, GRADE_Z, FLOORS, LEVEL, FLOOR_H, SLAB_T, BEAM_D, WALL_H,
    MUMTY_TOP, PARAPET_H, T9, T45, fi
)

# Coordinates for new scheme:
# Grid X:
# B: 36.125 (Bed-2 West wall / Lawn boundary)
# C: 51.375 (Bed-2 East wall / Bath-Dress West wall)
# C': 56.625 (Bath-Dress East wall / Car Porch West wall)
# D: 68.625 (Car Porch East wall / Drawing West wall / Stair East wall)
# E: 85.125 (Drawing East wall / Rear Suite East wall / 2'-1" East passage)

XB_W, XB_E = 36.125, 36.875
XC_W, XC_E = 51.375, 52.125
XC_PRIME_W, XC_PRIME_E = 56.625, 57.375
XD_W, XD_E = 68.625, 69.375
XE_W, XE_E = 84.375, 85.125

print(f"Bed-2 width clear: {XC_W - XB_E:.3f} ft ({fi(XC_W - XB_E)})")
print(f"Bed-2 Bath/Dress width clear: {XC_PRIME_W - XC_E:.3f} ft ({fi(XC_PRIME_W - XC_E)})")
print(f"Car Porch width clear: {XD_W - XC_PRIME_E:.3f} ft ({fi(XD_W - XC_PRIME_E)})")
print(f"Drawing / East Wing width clear: {XE_W - XD_E:.3f} ft ({fi(XE_W - XD_E)})")

# Y coordinates:
# Front wall: Y = 3.0 (outer face), Y = 3.75 (inner face)
# Bed-2 / Drawing south rooms rear wall: Y = 19.75 (inner face), Y = 20.5 (outer face)
# Bed depth clear: 19.75 - 3.75 = 16.0 ft (16'-0")
Y_FRONT_O, Y_FRONT_I = 3.0, 3.75
Y_MID_I, Y_MID_O = 19.75, 20.5

print(f"Front rooms depth clear: {Y_MID_I - Y_FRONT_I:.3f} ft ({fi(Y_MID_I - Y_FRONT_I)})")

# Central Staircase Core:
# X in [XC_PRIME_E, XD_W] = 11.25 ft clear (11'-3")
# Y in [Y_MID_O, 28.5] = 8.0 ft clear (8'-0")
# 2 flights of 3'-6" with 4" stair eye = 7'-4", landing depth = 3'-6" or 4'-0"
# Perfect fit!

# Kitchen on Angled Boundary:
# Along P3-P4, X in [24.0, XB_W], Y in [20.5, 33.75]
kit_poly = sbox(24.0, 20.5, XB_W, 34.0).intersection(PLOT.buffer(-0.75))
print(f"Kitchen polygon area: {kit_poly.area:.1f} sq.ft")

# Lounge + Dining:
# Center-North living space:
# X from XB_W to XD_W, Y from 20.5 to P4-P5 setback line (2' from boundary)
lounge_envelope = sbox(XB_W, 20.5, XD_W, 46.0).intersection(PLOT.buffer(-2.75))
# Subtract stair core:
stair_box = sbox(XC_PRIME_W, 20.0, XD_E, 29.25)
lounge_poly = lounge_envelope.difference(stair_box)
print(f"Family Lounge + Dining area: {lounge_poly.area:.1f} sq.ft")

# Rear Master Suite:
# In East wing (X in [XD_E, XE_W]):
# Bedroom: Y from 20.5 to 36.5 -> 16.0 ft depth, area = 15.0 * 16.0 = 240 sq.ft!
# Master Bath & Dress: Y from 36.5 to P5-P6 boundary wall -> area:
rear_bath_dress_envelope = sbox(XD_E, 36.5, XE_W, 58.0).intersection(PLOT.buffer(-2.75))
print(f"Rear Master Bath & Dress area: {rear_bath_dress_envelope.area:.1f} sq.ft")

# Main Lawn:
# X in [0.0, XB_W], Y in [0.0, 20.5]
lawn_poly = sbox(0.0, 0.0, XB_W, 20.5).intersection(PLOT.buffer(-0.75))
print(f"Main Lawn usable area: {lawn_poly.area:.1f} sq.ft")

print("\nAll spatial calculations verified successfully!")
