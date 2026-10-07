import shapely.geometry as sg
from shapely.ops import unary_union
from scripts.daata_hamlet.model import PLOT, PLOT_INNER, BUILD, SITE_POINTS

p3 = (24.5949, 26.1267)
p4 = (41.1897, 36.8354)
p5 = (67.6992, 50.7010)
p6 = (84.8373, 57.6678)
p7 = (88.8145, 62.1602)
p0 = (87.9167, 0.0)

XB_W, XB_E = 36.125, 36.875
XC_W, XC_E = 51.375, 52.125
XC_P_W, XC_P_E = 56.625, 57.375
XD_W, XD_E = 68.625, 69.375
XE_W, XE_E = 84.375, 85.125

# 1. Main Lawn
poly_lawn = sg.box(0, 0, XB_W, 60).intersection(PLOT_INNER)
print(f"Lawn area: {poly_lawn.area:.1f} sft")

# 2. Bed 2
poly_bed2 = sg.box(XB_E, 3.75, XC_W, 19.75)
print(f"Bed 2 area: {poly_bed2.area:.1f} sft ({XC_W - XB_E:.1f}' x {19.75 - 3.75:.1f}')")

# 3. Bed 2 Bath & Dress
poly_bed2_bath = sg.box(XC_E, 3.75, XC_P_W, 19.75)
print(f"Bed 2 Bath area: {poly_bed2_bath.area:.1f} sft ({XC_P_W - XC_E:.1f}' x {19.75 - 3.75:.1f}')")

# 4. Car Porch
poly_porch = sg.box(XC_P_E, 0.0, XD_W, 20.5)
print(f"Car Porch area: {poly_porch.area:.1f} sft ({XD_W - XC_P_E:.1f}' x 20.5')")

# 5. Drawing Room
poly_draw = sg.box(XD_E, 3.75, XE_W, 19.75)
print(f"Drawing area: {poly_draw.area:.1f} sft ({XE_W - XD_E:.1f}' x {19.75 - 3.75:.1f}')")

# 6. Drawing Dress & Bath
poly_draw_bath = sg.box(XD_E, 20.5, XE_W, 27.75)
print(f"Drawing Bath area: {poly_draw_bath.area:.1f} sft ({XE_W - XD_E:.1f}' x {27.75 - 20.5:.1f}')")

# 7. Bed Room 1
poly_bed1 = sg.box(XD_E, 28.5, XE_W, 42.0)
print(f"Bed 1 area: {poly_bed1.area:.1f} sft ({XE_W - XD_E:.1f}' x {42.0 - 28.5:.1f}')")

# 8. Bed Room 1 Master Bath & Dress (in corner of P5 and P6)
poly_bed1_bath = sg.box(XD_E, 42.75, XE_W, 58.0).intersection(PLOT.buffer(-2.75))
print(f"Bed 1 Bath area: {poly_bed1_bath.area:.1f} sft")

# 9. Entrance Foyer
poly_foyer = sg.box(XC_P_E, 20.5, 62.625, 25.0)
print(f"Foyer area: {poly_foyer.area:.1f} sft ({62.625 - XC_P_E:.1f}' x 4.5')")

# 10. Powder Room
poly_powder = sg.box(63.375, 20.5, XD_W, 25.0)
print(f"Powder area: {poly_powder.area:.1f} sft ({XD_W - 63.375:.1f}' x 4.5')")

# 11. Staircase Core (reduced width 7'-3\")
poly_stair = sg.box(61.375, 25.0, XD_W, 36.0)
print(f"Stair area: {poly_stair.area:.1f} sft ({XD_W - 61.375:.1f}' x 11.0')")

# 12. Kitchen (south of horizontal wall from P4, west on Line B / boundary)
poly_kit = sg.Polygon([
    (XB_E, 20.5), (XC_W, 20.5), (XC_W, 36.8354), (p4[0], 36.8354),
    (XB_E, 34.0511)
])
print(f"Kitchen area: {poly_kit.area:.1f} sft")

# 13. Kitchen Store (upper triangle till Line C)
poly_store = sg.Polygon([
    (p4[0], 36.8354), (XC_W, 36.8354), (XC_W, 42.1627)
])
print(f"Store area: {poly_store.area:.1f} sft")

# 14. Family TV Lounge
poly_lounge = sg.Polygon([
    (XC_E, 20.5), (XC_P_W, 20.5), (XC_P_W, 25.0), (61.375, 25.0),
    (61.375, 36.0), (XD_W, 36.0), (XD_W, 48.0), (XC_E, 48.0)
])
print(f"Lounge area: {poly_lounge.area:.1f} sft")
