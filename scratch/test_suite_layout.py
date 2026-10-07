import sys
sys.path.insert(0, ".")
from shapely.geometry import box as sbox, Polygon, Point
from shapely.ops import unary_union
from scripts.daata_hamlet.model import (
    XB_O, XB_I, XC_W, XC_E, XD_W, XD_E, XE_I, XE_O,
    FP_IN, bc_block, column_rect, T9, T45
)

# Zone Bay BC Y in [20.5, 33.0]
poly = bc_block.intersection(FP_IN).intersection(sbox(XB_I, 20.5, XC_W, 33.75))

# Let's test Layout:
# 1. Main Entrance Door on Line B: op("y", 36.5, 21.5, 25.5, 0.0, 8.0, "double", "MAIN ENTRANCE")
# 2. Entrance Foyer:
#    Arrival Foyer: Y in [20.5, 26.5]
#    Wait, does Foyer go all the way across X in [36.875, 51.375], Y in [20.5, 26.5]?
#    And how does it connect to Lounge?
#    Line C has Powder room at Y in [20.5, 24.125], VS-1 at [24.5, 27.5].
#    Lounge opens at Line C at Y in [27.5, 33.0]!
#    So Foyer needs to reach Y in [27.5, 33.0] along Line C!
#    Suppose the gallery along Line C is X in [46.0, 51.375], Y in [26.5, 33.0] (width 5'-4.5", clear!).
#    Then Foyer poly = union(
#        sbox(XB_I, 20.5, XC_W, 26.5),
#        sbox(46.0, 26.5, XC_W, 33.0)
#    ).intersection(poly)
#
# 3. North Suite (Bath & Dress):
#    Occupies X in [XB_I, 46.0], Y in [26.5, 33.0]
#    Width = 46.0 - 36.875 = 9.125 ft = 9'-1.5"
#    Depth = 33.0 - 26.5 = 6.5 ft = 6'-6"
#    Let's check its polygon and area:
suite_north = poly.intersection(sbox(XB_I, 26.5, 46.0, 33.0))
print("North Suite area:", suite_north.area)
print("North Suite bounds:", suite_north.bounds)

# Split into Bath and Dress:
# e.g. Bath in west part: X in [XB_I, 41.5] (has NW chamfer + north wall exterior!)
bath = suite_north.intersection(sbox(XB_I, 26.5, 41.5, 33.0))
# Dress in east part: X in [41.5, 46.0], Y in [26.5, 33.0]
dress = suite_north.intersection(sbox(41.5, 26.5, 46.0, 33.0))
print("Bath area:", bath.area, "bounds:", bath.bounds)
print("Dress area:", dress.area, "bounds:", dress.bounds)

foyer = poly.difference(suite_north)
print("Foyer area:", foyer.area, "bounds:", foyer.bounds)
