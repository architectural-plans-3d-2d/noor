"""
Test script to implement and validate the authentic Pakistani Open-To-Sky (OTS) ventilation court.
We will test:
1. Adding vent opening for GF Powder Room on Line C (line = 51.75, y = 22.5 to 24.5).
2. Adding vent opening for 1F Bed-4 Bath on Line C (line = 51.75, y = 22.5 to 24.5).
3. Defining the OTS open-air court in Bay BC (X in [46.875, 51.375], Y in [20.5, 26.375]).
4. Removing the validation hack in line 1007 of model.py.
5. Verifying that ALL 19 check groups in validate() PASS naturally!
"""
import copy
import sys
sys.path.insert(0, '.')
from shapely.geometry import Polygon, box as sbox, Point
from shapely.ops import unary_union
import scripts.daata_hamlet.model as m

# Let's see what happens if we add the vents and test check 14
model = m.build()

# Check current check 14
wet_rooms_gf = [r for r in model.rooms if r.floor == "GF" and r.kind == "wet"]
for wr in wet_rooms_gf:
    print(f"GF {wr.name}: bounds={wr.poly.bounds}")
    has_vent = False
    for o in model.openings:
        if o.floor == "GF" and o.kind == "vent":
            if wr.poly.buffer(0.6).intersects(m.R(*o.rect(0.5))):
                has_vent = True
                print(f"  -> has vent: {o.name} line={o.line} ({o.a}, {o.b})")
    if not has_vent:
        print(f"  -> NO VENT FOUND!")

# Now add vent on Line C for GF Powder
v_powder = m.Opening("GF", "y", 51.75, 22.5, 24.5, 6.5, 8.0, "vent", "V-POWDER")
model.openings.append(v_powder)

# Re-check GF Powder
p_room = [r for r in model.rooms if r.floor == "GF" and r.name == "POWDER"][0]
print("After adding V-POWDER, intersects:", p_room.poly.buffer(0.6).intersects(m.R(*v_powder.rect(0.5))))

# Now add vent on Line C for 1F Bed-4 Bath
v_b4 = m.Opening("1F", "y", 51.75, 22.5, 24.5, 6.5, 8.0, "vent", "V-B4")
model.openings.append(v_b4)
b4_room = [r for r in model.rooms if r.floor == "1F" and r.name == "BATH" and r.poly.bounds[0] > 50][0]
print("After adding V-B4, intersects:", b4_room.poly.buffer(0.6).intersects(m.R(*v_b4.rect(0.5))))
