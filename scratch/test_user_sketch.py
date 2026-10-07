import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import shapely.geometry as sg
from shapely.ops import unary_union
from scripts.daata_hamlet.model import PLOT, PLOT_INNER, BUILD, SITE_POINTS

XB_W, XB_E = 36.125, 36.875
XC_W, XC_E = 51.375, 52.125
XC_P_W, XC_P_E = 56.625, 57.375
XD_W, XD_E = 68.625, 69.375
XE_W, XE_E = 84.375, 85.125

P4_X, P4_Y = 41.1897, 36.8354

print("--- USER SKETCH VERIFICATION ---")

# 1. Main Lawn
lawn = sg.box(0, 0, XB_W, 60).intersection(PLOT_INNER)
print(f"1. Main Lawn: {lawn.area:.1f} sq.ft")

# 2. Bed Room-2
bed2 = sg.box(XB_E, 3.75, XC_W, 19.75)
print(f"2. Bed Room-2: {bed2.area:.1f} sq.ft ({XC_W - XB_E:.1f}' x {19.75 - 3.75:.1f}')")

# 3. Bed 2 Bath & Dress (Split horizontally in Bay C-C')
bath2 = sg.box(XC_E, 3.75, XC_P_W, 11.5)
dress2 = sg.box(XC_E, 12.25, XC_P_W, 19.75)
print(f"3a. Bath for bed 2: {bath2.area:.1f} sq.ft ({XC_P_W - XC_E:.1f}' x {11.5 - 3.75:.1f}')")
print(f"3b. Dress for bed 2: {dress2.area:.1f} sq.ft ({XC_P_W - XC_E:.1f}' x {19.75 - 12.25:.1f}')")

# 4. Car Porch / Veranda
porch = sg.box(XC_P_E, 0, XD_W, 20.5)
print(f"4. Car Porch / Veranda: {porch.area:.1f} sq.ft ({XD_W - XC_P_E:.1f}' x 20.5')")

# 5. Drawing Room
drawing = sg.box(XD_E, 3.75, XE_W, 19.75)
print(f"5. Drawing Room: {drawing.area:.1f} sq.ft ({XE_W - XD_E:.1f}' x {19.75 - 3.75:.1f}')")

# 6. Drawing Dress & Bath (Split in Bay D-E)
mid_de = (XD_E + XE_W) / 2 # 76.875
draw_dress = sg.box(XD_E, 20.5, mid_de - 0.375, 27.5)
draw_bath = sg.box(mid_de + 0.375, 20.5, XE_W, 27.5)
print(f"6a. Dress for drawing: {draw_dress.area:.1f} sq.ft ({mid_de - 0.375 - XD_E:.1f}' x 7.0')")
print(f"6b. Bath for drawing: {draw_bath.area:.1f} sq.ft ({XE_W - (mid_de + 0.375):.1f}' x 7.0')")

# 7. Bed Room 1
bed1 = sg.box(XD_E, 28.25, XE_W, 42.5)
print(f"7. Bed-1: {bed1.area:.1f} sq.ft ({XE_W - XD_E:.1f}' x {42.5 - 28.25:.1f}')")

# 8. Bed 1 Dress & Washroom (in corner of P5-P6)
bed1_dress = sg.box(XD_E, 43.25, mid_de - 0.375, 57.0).intersection(PLOT.buffer(-2.75))
bed1_wash = sg.box(mid_de + 0.375, 43.25, XE_W, 58.0).intersection(PLOT.buffer(-2.75))
print(f"8a. Dressing (Bed-1): {bed1_dress.area:.1f} sq.ft")
print(f"8b. Washroom (Bed-1): {bed1_wash.area:.1f} sq.ft")

# 9. Kitchen Passage (4 feet wide)
kit_pass = sg.box(XB_E, 20.5, XC_W, 24.5)
print(f"9. Passage way 4 feet wide: {kit_pass.area:.1f} sq.ft ({XC_W - XB_E:.1f}' x 4.0')")

# 10. Kitchen (Main)
kit = sg.box(XB_E, 25.25, XC_W, P4_Y)
print(f"10. Kitchen: {kit.area:.1f} sq.ft ({XC_W - XB_E:.1f}' x {P4_Y - 25.25:.1f}')")

# 11. Dirty Kitchen
dirty_kit = sg.Polygon([
    (P4_X, P4_Y), (XC_W, P4_Y), (XC_W, 42.1627)
]).intersection(PLOT_INNER)
print(f"11. Dirty Kitchen: {dirty_kit.area:.1f} sq.ft")

# 12. Powder for Lounge
powder = sg.box(62.625, 20.5, XD_W, 27.5)
print(f"12. Powder for Lounge: {powder.area:.1f} sq.ft ({XD_W - 62.625:.1f}' x 7.0')")

# 13. Open area for lighting
open_light = sg.Polygon([
    (XC_W, 42.1627), (67.6992, 50.7010), (67.6992, 45.0), (XC_W, 45.0)
])
print(f"13. Open area for lighting: {open_light.area:.1f} sq.ft")
