import sys
sys.path.insert(0, ".")
from shapely.geometry import box as sbox, Polygon, Point
from shapely.ops import unary_union
from scripts.daata_hamlet.model import (
    XB_O, XB_I, XC_W, XC_E, XD_W, XD_E, XE_I, XE_O,
    GX, GY, COLUMN_SPEC, column_rect, T9, T45, BUILD, PLOT_INNER, PLOT
)

print("Line B inner:", XB_I, "outer:", XB_O)
print("Line C west:", XC_W, "east:", XC_E)
print("Width of Bay BC clear:", XC_W - XB_I)

# Check columns on Grid B around Y=18-28
for name in ["B2", "B3", "B4"]:
    rect = column_rect(name)
    print(f"Col {name}: center Y={GY[name[1]]}, bounds={rect}")

# Check space between B3 and B4
b3_top = column_rect("B3")[3]
b4_bot = column_rect("B4")[1]
print(f"Clear wall on Line B between B3 and B4: Y = {b3_top:.3f} to {b4_bot:.3f} (length = {b4_bot - b3_top:.2f} ft)")

# A door of 4'0" (e.g. Y=21.5 to 25.5) fits with:
print(f"Door 21.5 - 25.5 clears B3 by: {21.5 - b3_top:.2f} ft")
print(f"Door 21.5 - 25.5 clears B4 by: {b4_bot - 25.5:.2f} ft")
