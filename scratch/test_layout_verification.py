"""
Verify the New Complete Layout in Python
"""
from shapely.geometry import box as sbox, Polygon
from shapely.ops import unary_union

SITE_POINTS = [
    ("P1", 0.0000, 0.0000), ("P2", 10.4884, 10.0122), ("P3", 24.5949, 26.1267),
    ("P4", 41.1897, 36.8354), ("P5", 67.6992, 50.7010), ("P6", 84.8373, 57.6678),
    ("P7", 88.8145, 62.1602), ("P0", 87.9167, 0.0000),
]
PLOT = Polygon([(x, y) for _, x, y in SITE_POINTS])
PLOT_INNER = PLOT.buffer(-0.75, join_style="mitre")
BUILD = PLOT.buffer(-2.75, join_style="mitre")

XB_W, XB_E = 36.125, 36.875
XC_W, XC_E = 51.375, 52.125
XC_P_W, XC_P_E = 56.625, 57.375
XD_W, XD_E = 68.625, 69.375
XE_W, XE_E = 84.375, 85.125

print("Plot area:", PLOT.area, "sq.ft")

# 1. Main Lawn: West of Line B
lawn = sbox(0.0, 0.0, XB_W, 60.0).intersection(PLOT_INNER)
print(f"Main Lawn Area (West of Line B): {lawn.area:.1f} sq.ft")

# 2. Bed Room-2: Bay B-C, South
bed2 = sbox(XB_E, 3.75, XC_W, 19.75)
print(f"Bed Room-2: {XC_W - XB_E:.2f}' x {19.75 - 3.75:.2f}' = {bed2.area:.1f} sq.ft")

# 3. Bed-2 Bath/Dress: Bay C-C', South
bath2 = sbox(XC_E, 3.75, XC_P_W, 19.75)
print(f"Bed-2 Bath: {XC_P_W - XC_E:.2f}' x {19.75 - 3.75:.2f}' = {bath2.area:.1f} sq.ft")

# 4. Car Porch: Bay C'-D, South
porch = sbox(XC_P_E, 0.0, XD_W, 20.5)
print(f"Car Porch: {XD_W - XC_P_E:.2f}' x {20.5 - 0.0:.2f}' = {porch.area:.1f} sq.ft")

# 5. Drawing Room: Bay D-E, South
draw = sbox(XD_E, 3.75, XE_W, 19.75)
print(f"Drawing Room: {XE_W - XD_E:.2f}' x {19.75 - 3.75:.2f}' = {draw.area:.1f} sq.ft")

# 6. Powder Room: on Car Porch wall, Bay C'-D
# X in [62.625, 68.625], Y in [20.5, 25.0]
powder = sbox(62.625, 20.5, XD_W, 25.0)
print(f"Powder Room: {XD_W - 62.625:.2f}' x {25.0 - 20.5:.2f}' = {powder.area:.1f} sq.ft")

# 7. Main Entrance Door & Foyer: on Car Porch wall, Bay C'-D
# Door on Y = 20.5, X in [56.625, 62.625] (6.0 ft door)
# Foyer: X in [51.375, 62.625], Y in [20.5, 25.0]
foyer = sbox(XC_W, 20.5, 62.625, 25.0)
print(f"Entrance Foyer: {62.625 - XC_W:.2f}' x {25.0 - 20.5:.2f}' = {foyer.area:.1f} sq.ft")

# 8. Staircase Core:
# Behind powder/foyer: X in [57.375, 68.625], Y in [25.0, 32.5]
stair = sbox(XC_P_E, 25.0, XD_W, 32.5)
print(f"Staircase Core: {XD_W - XC_P_E:.2f}' x {32.5 - 25.0:.2f}' = {stair.area:.1f} sq.ft")

# 9. Kitchen: Bay B-C, North (opposite Bed-2, strictly east of Line B)
# Bounded by Line B (36.125), Line C (51.375), Y in [24.0, 36.0]
kit = sbox(XB_E, 24.0, XC_W, 36.0).intersection(PLOT.buffer(-2.75))
print(f"Kitchen: {kit.area:.1f} sq.ft (trapezoid on boundary wall, strictly EAST of Line B!)")

# 10. Master Bedroom (Bed-1): Bay D-E, Middle
mbed = sbox(XD_E, 20.5, XE_W, 36.5)
print(f"Master Bed: {XE_W - XD_E:.2f}' x {36.5 - 20.5:.2f}' = {mbed.area:.1f} sq.ft")

# 11. Master Bath & Dress: Bay D-E, North
mbath = sbox(XD_E, 36.5, XE_W, 58.0).intersection(PLOT.buffer(-2.75))
print(f"Master Bath & Dress: {mbath.area:.1f} sq.ft")

# 12. Lounge + Dining: Central
lounge = sbox(XB_E, 20.5, XD_W, 44.0).intersection(PLOT.buffer(-2.75)).difference(
    unary_union([bed2, bath2, porch, draw, powder, foyer, stair, kit])
)
print(f"Family Lounge + Dining: {lounge.area:.1f} sq.ft")

total_covered = unary_union([bed2, bath2, porch, draw, powder, foyer, stair, kit, mbed, mbath, lounge]).area
print(f"Total GF Covered Area: {total_covered:.1f} sq.ft")
