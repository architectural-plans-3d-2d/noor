import sys
from pathlib import Path
sys.path.insert(0, str(Path.cwd()))
import shapely.geometry as sg
from shapely.ops import unary_union
from scripts.daata_hamlet.model import PLOT, SITE_POINTS, R, sbox

print("=== SITE GEOMETRY & BOUNDARIES ===")
for p, x, y in SITE_POINTS:
    print(f"{p}: ({x:.2f}, {y:.2f})")

print(f"\nTotal Plot Area: {PLOT.area:.1f} sq.ft")

# Let's analyze the proposed new spaces:
# 1. Main Lawn (old car porch + front lawn):
# From X = 0 to ~36.125, Y = 0 to ~20.0 (or up to boundary P2-P3)
poly_lawn = sbox(0, 0, 36.125, 20.0).intersection(PLOT)
print(f"Main Lawn Area (approx): {poly_lawn.area:.1f} sq.ft")

# 2. South-West Bedroom (Bed-2):
# Between Lawn (X ~ 36.125) and New Car Porch
# If Bed-2 moves to the south boundary wall (Y = 0 to 16.0 or Y = 0 to 17.0):
# Width: from X = 36.125 to X = 51.375 is 15'-3"
# Depth: from Y = 0 to Y = 16.0 is 16'-0"
# Area: 15.25 * 16.0 = 244 sq.ft!
bed2_poly = sbox(36.125, 0.0, 51.375, 16.0)
print(f"Bed-2 Area: {bed2_poly.area:.1f} sq.ft (15'-3\" x 16'-0\")")

# 3. Bed-2 Bath & Dress:
# Taken from existing drawing room space (between Bed-2 and new Car Porch):
# X in [51.375, 56.625] (width 5'-3"), Y in [0.0, 16.0] (depth 16'-0")
# Or Dress (5'-3" x 8'-0") + Bath (5'-3" x 8'-0") = 84 sq.ft!
bed2_bath_dress = sbox(51.375, 0.0, 56.625, 16.0)
print(f"Bed-2 Bath & Dress: {bed2_bath_dress.area:.1f} sq.ft (5'-3\" x 16'-0\")")

# 4. New Car Porch:
# Sits in the remainder of old drawing room space:
# X in [56.625, 68.625] (width 12'-0"), Y in [0.0, 20.0] (depth 20'-0")
# Standard car porch size: 12'-0" x 20'-0" (fits a full-size SUV like Land Cruiser / Prado)!
new_porch = sbox(56.625, 0.0, 68.625, 20.0)
print(f"New Car Porch: {new_porch.area:.1f} sq.ft (12'-0\" x 20'-0\")")

# 5. Drawing Room (at South-East, where Bed-1 was):
# From new porch (X = 68.625) to East boundary wall (X ~ 87.21):
# Width: 87.21 - 68.625 = 18'-7"!
# Depth: Y in [0.0, 16.0] or [0.0, 18.0]
# Area: 18.58 * 16.0 = 297.3 sq.ft!
dr_poly = sbox(68.625, 0.0, 87.21, 16.0)
print(f"Drawing Room: {dr_poly.area:.1f} sq.ft (18'-7\" x 16'-0\")")

# 6. Central Staircase & Powder Room:
# North of new Car Porch (where old light court + powder were):
# X in [56.625, 68.625], Y in [20.0, 28.5] (12'-0\" x 8'-6\")
# Flights: 3'-6\" wide, landing at Y = 28.5 (7'-0\" headroom for Powder underneath)!
stair_poly = sbox(56.625, 20.0, 68.625, 28.5)
print(f"Central Staircase Core: {stair_poly.area:.1f} sq.ft (12'-0\" x 8'-6\")")

# 7. Entrance Foyer:
# Directly north of Bed-2 and Bed-2 bath/dress:
# X in [36.125, 56.625], Y in [16.0, 24.0] (20'-6\" x 8'-0\")
# Wide open grand foyer entered directly from the new Car Porch!
foyer_poly = sbox(36.125, 16.0, 56.625, 24.0)
print(f"Entrance Foyer: {foyer_poly.area:.1f} sq.ft (20'-6\" x 8'-0\")")

# 8. Kitchen on the Angled Boundary:
# Opposite to Entrance Foyer / Bed-2 along P3-P4:
# X in [24.0, 36.125], Y in [20.0, 34.0] bounded by boundary line P3-P4:
p3 = sg.Point(SITE_POINTS[2][1], SITE_POINTS[2][2])
p4 = sg.Point(SITE_POINTS[3][1], SITE_POINTS[3][2])
seg_p3_p4 = sg.LineString([p3, p4])
kitch_raw = sbox(24.0, 20.0, 36.125, 34.0).intersection(PLOT)
print(f"Kitchen on Angled Boundary: {kitch_raw.area:.1f} sq.ft (trapezoid/triangle)")

# 9. Lounge + Dining:
# Central living space from X = 36.125 to 68.625, Y in [24.0, 48.0] extending to P4-P5:
# With 2'-0\" passage from boundary line P4-P5:
p5 = sg.Point(SITE_POINTS[4][1], SITE_POINTS[4][2])
seg_p4_p5 = sg.LineString([p4, p5])
print(f"P4: {p4.x:.2f}, {p4.y:.2f} to P5: {p5.x:.2f}, {p5.y:.2f}")

# 10. Rear Bedroom Suite (where old stair, kitchen & dirty kitchen were):
# X in [68.625, 87.21], Y in [20.0, 56.0]:
# Bedroom: X in [68.625, 87.21], Y in [20.0, 36.0] or [24.0, 40.0]
# Bath + Dress: Y in [40.0, 56.0] taking the angled slope near P5-P6!
rear_suite_raw = sbox(68.625, 20.0, 87.21, 56.0).intersection(PLOT)
print(f"Rear Master Suite Zone: {rear_suite_raw.area:.1f} sq.ft")
