import sys
sys.path.insert(0, ".")
import math
from shapely.geometry import box as sbox, Polygon, Point, LineString
from shapely.ops import unary_union
import scripts.daata_hamlet.model as dhm

m = dhm.build()

# Remove old angled entrance
m.angled_openings = [ao for ao in m.angled_openings if not (ao.floor == "GF" and ao.name == "MAIN ENTRANCE")]

# Remove old openings in GF Bay BC:
m.openings = [o for o in m.openings if not (
    o.floor == "GF" and (
        (o.orient == "y" and abs(o.line - 36.5) < 0.1 and abs(o.a - 23.0) < 0.5) or
        (o.orient == "x" and abs(o.line - 20.125) < 0.1 and 40.0 < o.a < 52.0) or
        (o.orient == "x" and abs(o.line - 27.875) < 0.1 and 45.0 < o.a < 52.0) or
        (o.orient == "y" and abs(o.line - 42.3125) < 0.1)
    )
)]

# Add new openings:
# 1. Main entrance double door on Line B:
m.openings.append(dhm.Opening("GF", "y", 36.5, 21.5, 25.5, 0.0, 8.0, "double", "MAIN ENTRANCE", "a", 1))

# 2. Door to Bed Room-2 from Foyer:
m.openings.append(dhm.Opening("GF", "x", 20.125, 45.0, 48.0, 0.0, 7.0, "door", "D2", "b", -1))

# 3. Door to Dress:
m.openings.append(dhm.Opening("GF", "x", 26.75, 43.5, 46.5, 0.0, 7.0, "door", "D2", "a", 1))

# 4. Door from Dress to Bath:
m.openings.append(dhm.Opening("GF", "y", 43.5, 28.5, 31.0, 0.0, 7.0, "door", "D3", "a", 1))

# 5. Vent on Line B for Bath:
m.openings.append(dhm.Opening("GF", "y", 36.5, 28.75, 30.25, 6.5, 8.0, "vent", "V"))

# 6. Window on NW chamfer for Bath:
m.angled_openings.append(dhm.AngledOpening("GF", (37.75, 31.34), (40.70, 33.24), 3.0, 7.5, "window", "W-BATH"))

# Update walls in m.walls["GF"]
new_walls = []
for w in m.walls["GF"]:
    if abs(w.y0 - 27.5) < 0.1 and abs(w.y1 - 28.25) < 0.1 and abs(w.x0 - dhm.XB_I) < 0.1:
        # South wall of bath/dress suite:
        new_walls.append(dhm.Box(dhm.XB_I, 26.375, 0.0, 47.0, 26.75, dhm.WALL_H, "plaster", "walls", "GF"))
        # East wall of dress (separating dress from foyer gallery):
        new_walls.append(dhm.Box(46.625, 26.75, 0.0, 47.0, 33.0, dhm.WALL_H, "plaster", "walls", "GF"))
    elif w.layer == "partitions" and (
        (abs(w.x0 - 42.125) < 0.1 and abs(w.y0 - 20.5) < 0.1) or
        (abs(w.x0 - 47.5) < 0.1 and abs(w.y0 - 20.5) < 0.1)
    ):
        continue
    else:
        new_walls.append(w)

# Add partition dividing Bath and Dress at X in [43.125, 43.5]:
new_walls.append(dhm.Box(43.125, 26.75, 0.0, 43.5, 33.0, dhm.WALL_H, "plaster", "partitions", "GF"))
m.walls["GF"] = new_walls

# Update rooms in m.rooms:
new_rooms = []
for r in m.rooms:
    if r.floor == "GF" and r.name in ("BATH", "DRESS", "LOBBY", "ENTRANCE FOYER"):
        if r.poly.bounds[0] < 52.0 and r.poly.bounds[1] > 20.0:
            continue
    new_rooms.append(r)
    
poly = dhm.bc_block.intersection(dhm.FP_IN).intersection(sbox(dhm.XB_I, 20.5, dhm.XC_W, 33.75))
bath_poly = poly.intersection(sbox(dhm.XB_I, 26.75, 43.125, 33.0))
dress_poly = poly.intersection(sbox(43.5, 26.75, 46.625, 33.0))
foyer_gal = poly.intersection(sbox(47.0, 26.75, dhm.XC_W, 33.0))
foyer_main = poly.intersection(sbox(dhm.XB_I, 20.5, dhm.XC_W, 26.375))
foyer_poly = unary_union([foyer_main, foyer_gal])

new_rooms.append(dhm.Room("GF", "BATH", bath_poly, "wet", (40.0, 29.5)))
new_rooms.append(dhm.Room("GF", "DRESS", dress_poly, "serv", (45.0, 29.5)))
new_rooms.append(dhm.Room("GF", "ENTRANCE FOYER", foyer_poly, "circ", (44.5, 24.0)))

m.rooms = new_rooms

# Re-split walls and opening fill
m.boxes = [b for b in m.boxes if not (b.floor == "GF" and b.layer in ("walls", "partitions", "openings"))]
L = dhm.LEVEL["GF"]
ops = [o for o in m.openings if o.floor == "GF"]
for w in m.walls["GF"]:
    m.boxes += dhm.split_wall(w, ops, L)
for o in ops:
    m.boxes += dhm.opening_fill(o)

# Step entrance
new_prisms = []
free = dhm.PLOT_INNER.difference(dhm.FP)
for p in m.prisms:
    if p.tag == "step-entrance":
        portico_poly = sbox(20.0, 20.0, dhm.XB_O, 26.5).intersection(free)
        new_prisms.append(dhm.Prism(portico_poly, dhm.GRADE_Z, 0.0, "stone_floor", "site", "SITE", "step-entrance"))
    else:
        new_prisms.append(p)
m.prisms = new_prisms

# Run validate:
print(f"Bath: {bath_poly.area:.1f} sft, Dress: {dress_poly.area:.1f} sft, Foyer: {foyer_poly.area:.1f} sft")
res = dhm.validate(m, verbose=True)
passed = sum(1 for ok, _ in res if ok)
total = len(res)
print(f"\nResult: {passed}/{total} passed")
