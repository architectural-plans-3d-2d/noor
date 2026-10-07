import sys
sys.path.insert(0, ".")
from shapely.geometry import LineString, Point
from scripts.daata_hamlet.model import PLOT, SITE_POINTS

boundary = LineString([(x, y) for _, x, y in SITE_POINTS])

print("Y | Boundary X | Building X | Clear Distance")
print("-" * 45)
for y in range(0, 36, 2):
    # Find boundary x at this y
    h_line = LineString([(-10, y), (50, y)])
    inter = boundary.intersection(h_line)
    if not inter.is_empty:
        bx = inter.x if isinstance(inter, Point) else [p.x for p in inter.geoms][0]
        # Building x
        if y <= 18:
            # Porch is from 17.5 to 36.125
            bld_x = 17.5
            dist = bld_x - bx
            print(f"{y:2d} | {bx:10.2f} | {bld_x:10.2f} (porch) | {dist:6.2f} ft ({dist*12:4.0f} in)")
        else:
            # Building wall at Line B is 36.125
            bld_x = 36.125
            dist = bld_x - bx
            print(f"{y:2d} | {bx:10.2f} | {bld_x:10.2f} (wall)  | {dist:6.2f} ft ({dist*12:4.0f} in)")
