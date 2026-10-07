import sys
sys.path.insert(0, ".")
import math
from shapely.geometry import box as sbox, Polygon, Point, LineString
from shapely.ops import unary_union
import scripts.daata_hamlet.model as dhm

# Test modifying model for expanded Powder Room and Drawing Room entrance
m = dhm.build()

XC_E = dhm.XC_E
XD_W = dhm.XD_W

# 1. Update rooms in m.rooms:
new_rooms = []
for r in m.rooms:
    if r.floor == "GF" and r.name in ("POWDER", "LOUNGE + DINING"):
        continue
    new_rooms.append(r)

powder_new = dhm.R(XC_E, 20.5, 59.125, 27.5).difference(dhm.R(XC_E, 24.125, 55.5, 27.5))
lounge_new = dhm.R(XC_E, 20.5, XD_W, 41.75).intersection(dhm.FP_IN).difference(dhm.R(XC_E, 20.5, 59.5, 27.5))

new_rooms.append(dhm.Room("GF", "POWDER", powder_new, "wet", (56.0, 22.5)))
new_rooms.append(dhm.Room("GF", "LOUNGE + DINING", lounge_new, "hab", (62.0, 32.0)))
m.rooms = new_rooms

# 2. Update partitions in m.walls["GF"]
new_walls = []
for w in m.walls["GF"]:
    if w.layer == "partitions" and abs(w.x0 - 57.125) < 0.1 and abs(w.y0 - 20.5) < 0.1:
        # Replace old 57.125 partition with 59.125 partition:
        new_walls.append(dhm.Box(59.125, 20.5, 0.0, 59.5, 27.5, dhm.WALL_H, "plaster", "partitions", "GF"))
    else:
        new_walls.append(w)
m.walls["GF"] = new_walls

# 3. Update openings in m.openings:
new_openings = []
for o in m.openings:
    if o.floor == "GF" and abs(o.line - 57.3125) < 0.1:
        # Remove old powder door from lounge
        continue
    elif o.floor == "GF" and o.orient == "x" and abs(o.line - 20.125) < 0.1 and abs(o.a - 58.5) < 0.1:
        # Update Drawing to Lounge door to X in [61.0, 64.5]
        new_openings.append(dhm.Opening("GF", "x", 20.125, 61.0, 64.5, 0.0, 7.0, "door", "D1", "a", 1))
    else:
        new_openings.append(o)

# Add new door from Drawing Room into Powder Room:
new_openings.append(dhm.Opening("GF", "x", 20.125, 54.0, 56.5, 0.0, 7.0, "door", "D3", "a", 1))
m.openings = new_openings

# 4. Re-split walls and opening fill
m.boxes = [b for b in m.boxes if not (b.floor == "GF" and b.layer in ("walls", "partitions", "openings"))]
L = dhm.LEVEL["GF"]
ops = [o for o in m.openings if o.floor == "GF"]
for w in m.walls["GF"]:
    m.boxes += dhm.split_wall(w, ops, L)
for o in ops:
    m.boxes += dhm.opening_fill(o)

# 5. Run validate
print(f"Testing layout: powder area = {powder_new.area:.1f}, lounge area = {lounge_new.area:.1f}")
res = dhm.validate(m, verbose=True)
passed = sum(1 for ok, _ in res if ok)
total = len(res)
print(f"\nResult: {passed}/{total} passed")
