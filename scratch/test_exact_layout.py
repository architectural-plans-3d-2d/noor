import sys
sys.path.insert(0, ".")
from shapely.geometry import box as sbox, Polygon, Point
from shapely.ops import unary_union
import scripts.daata_hamlet.model as dhm

# Let's inspect the exact walls and partitions we need
# Bay BC on GF:
# Walls:
# Currently in model.py GF:
# (XB_I, 27.5, XC_W, 28.25) -> old wall dividing bath/dress from old foyer
# Partitions:
# (42.125, 20.5, 42.5, 27.5) -> old bath/dress partition
# (47.5, 20.5, 47.875, 27.5) -> old dress/lobby partition

# In NEW layout:
# 1. Main wall dividing North Suite from Foyer at Y = 26.5 to 27.25 (or 26.125 to 26.5):
#    Wait, structural wall or partition?
#    North suite: X in [XB_I, 47.0], Y in [26.5, 33.0]
#    Partition at Y in [26.125, 26.5] from XB_I to 47.0
#    Partition at X in [42.125, 42.5] from 26.5 to 33.0 (dividing Bath and Dress)
#    Partition at X in [47.0, 47.375] from 26.5 to 33.0 (dividing Dress from Foyer Gallery)
# Let's check areas and coordinates!

XB_I = dhm.XB_I
XC_W = dhm.XC_W

print(f"XB_I = {XB_I}, XC_W = {XC_W}")

poly = dhm.bc_block.intersection(dhm.FP_IN).intersection(sbox(XB_I, 20.5, XC_W, 33.75))

# Bath: X in [XB_I, 42.125], Y in [26.5, 33.0]
bath = poly.intersection(sbox(XB_I, 26.5, 42.125, 33.0))
# Dress: X in [42.5, 47.0], Y in [26.5, 33.0]
dress = poly.intersection(sbox(42.5, 26.5, 47.0, 33.0))
# Foyer gallery: X in [47.375, XC_W], Y in [26.5, 33.0]
foyer_gal = poly.intersection(sbox(47.375, 26.5, XC_W, 33.0))
# Foyer main: X in [XB_I, XC_W], Y in [20.5, 26.125]
foyer_main = poly.intersection(sbox(XB_I, 20.5, XC_W, 26.125))

foyer = unary_union([foyer_main, foyer_gal])

print(f"Bath area: {bath.area:.2f} sft, bounds: {bath.bounds}")
print(f"Dress area: {dress.area:.2f} sft, bounds: {dress.bounds}")
print(f"Foyer Gallery width: {XC_W - 47.375:.3f} ft ({dhm.fi(XC_W - 47.375)})")
print(f"Foyer total area: {foyer.area:.2f} sft")
