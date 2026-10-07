import sys
sys.path.insert(0, ".")
from shapely.geometry import box as sbox, Polygon, Point
from shapely.ops import unary_union
from scripts.daata_hamlet.model import (
    XB_O, XB_I, XC_W, XC_E, XD_W, XD_E, XE_I, XE_O,
    FP_IN, bc_block, column_rect, T9, T45
)

# Bay BC zone Y in [20.5, 33.0]
poly = bc_block.intersection(FP_IN).intersection(sbox(XB_I, 20.5, XC_W, 33.75))
print("Total Bay BC service area:", poly.area)

# Let's test Layout 1:
# North zone Y in [26.5, 33.0] or [27.5, 33.0]
# Suppose Foyer enters at Line B: Y in [21.5, 25.5]
# Foyer covers:
# - West entry vestibule: X in [36.875, 43.5], Y in [20.5, 26.5]
# - Lobby/Gallery: X in [43.5, 51.375], Y in [20.5, 33.0]
# - Archway into Lounge at Line C: Y in [28.5, 32.5]
# And Bath + Dress in North-West zone: X in [36.875, 43.5], Y in [26.5, 33.0]
# Wait, let's check Bath area in NW zone:
bath_nw = poly.intersection(sbox(XB_I, 26.5, 43.5, 33.0))
print("Bath NW area:", bath_nw.area, "bounds:", bath_nw.bounds)

# And Foyer area:
foyer_poly = poly.difference(bath_nw)
print("Foyer area:", foyer_poly.area)
