"""AutoCAD DXF (R2018, units = feet) of the GF plan + south elevation outline."""
import math, ezdxf
from ezdxf.enums import TextEntityAlignment as TA
from model import *
from draw_plan import door_geom

doc = ezdxf.new('R2018', setup=True)
doc.header['$INSUNITS'] = 2          # feet
doc.header['$MEASUREMENT'] = 0
msp = doc.modelspace()
LAY = {'0_SITE_BOUNDARY': 1, 'L-LAWN': 3, 'S-GRID': 8, 'S-COLS': 7, 'A-WALL': 7, 'A-WALL-HATCH': 8,
       'A-DOOR': 4, 'A-GLAZ': 5, 'A-STAIR': 6, 'A-FURN': 9, 'A-FIXT': 140, 'A-ROOM-NAME': 2,
       'A-DIMS': 1, 'A-ELEV': 7, 'A-TEXT': 7}
for n, c in LAY.items():
    doc.layers.add(n, color=c)
doc.layers.get('S-GRID').dxf.linetype = 'CENTER'

def pl(g, layer, closed=True):
    for p in getattr(g, 'geoms', [g]):
        if p.is_empty: continue
        for ring in [p.exterior] + list(p.interiors):
            msp.add_lwpolyline(list(ring.coords), close=closed, dxfattribs={'layer': layer})

def txt(s, x, y, h=0.45, layer='A-TEXT', rot=0, align=TA.MIDDLE_CENTER):
    t = msp.add_text(s, height=h, rotation=rot, dxfattribs={'layer': layer, 'style': 'OpenSans'})
    t.set_placement((x, y), align=align)

# site
pl(PLOT, '0_SITE_BOUNDARY')
for n, x, y in PEGS:
    msp.add_circle((x, y), 0.4, dxfattribs={'layer': '0_SITE_BOUNDARY'})
    txt(n, x + 0.9, y + 0.9, 0.55, '0_SITE_BOUNDARY')
lawn = PLOT & box(-5, -5, LINE_B, 80)
pl(lawn, 'L-LAWN')
h = msp.add_hatch(color=3, dxfattribs={'layer': 'L-LAWN'}); h.set_pattern_fill('DOTS', scale=1.5)
h.paths.add_polyline_path(list(lawn.exterior.coords), is_closed=True)
txt(f'MAIN LAWN  {lawn.area:.0f} SQ.FT', 18, 6, 0.9, 'L-LAWN')
msp.add_line((LINE_B, -1.5), (LINE_B, north_y(LINE_B) + 1.5), dxfattribs={'layer': '0_SITE_BOUNDARY', 'linetype': 'DASHED'})
# grids
for k, x in GRID_X.items():
    msp.add_line((x, -4.5), (x, 63), dxfattribs={'layer': 'S-GRID'})
    for yy in (-6.0, 64.6):
        msp.add_circle((x, yy), 1.1, dxfattribs={'layer': 'S-GRID'}); txt(k, x, yy, 0.8, 'S-GRID')
for k, y in GRID_Y.items():
    msp.add_line((30, y), (93.5, y), dxfattribs={'layer': 'S-GRID'})
    msp.add_circle((95.2, y), 1.1, dxfattribs={'layer': 'S-GRID'}); txt(k, 95.2, y, 0.8, 'S-GRID')
# walls with openings removed
from shapely.ops import unary_union
cuts = unary_union([seg_rect(o['p0'], o['p1'], o['t']) for o in DOORS + WINDOWS])
W = WALLS - cuts
pl(W, 'A-WALL')
for p in getattr(W, 'geoms', [W]):
    hh = msp.add_hatch(color=8, dxfattribs={'layer': 'A-WALL-HATCH'})
    hh.paths.add_polyline_path(list(p.exterior.coords), is_closed=True, flags=1)
    for r in p.interiors: hh.paths.add_polyline_path(list(r.coords), is_closed=True, flags=0)
for k, c in COLUMNS.items():
    pl(c, 'S-COLS')
    hh = msp.add_hatch(color=7, dxfattribs={'layer': 'S-COLS'}); hh.paths.add_polyline_path(list(c.exterior.coords), is_closed=True)
# windows
for w in WINDOWS:
    (x0, y0), (x1, y1) = w['p0'], w['p1']
    L = math.hypot(x1 - x0, y1 - y0); nx, ny = -(y1 - y0) / L, (x1 - x0) / L
    for s in (-w['t'] / 2, -w['t'] / 6, w['t'] / 6, w['t'] / 2):
        msp.add_line((x0 + nx * s, y0 + ny * s), (x1 + nx * s, y1 + ny * s), dxfattribs={'layer': 'A-GLAZ'})
    txt(w['id'], (x0 + x1) / 2 + nx * 1.5, (y0 + y1) / 2 + ny * 1.5, 0.45, 'A-GLAZ')
# doors
for d in DOORS:
    (hx, hy), tip, L, a0, a1, _ = door_geom(d)
    msp.add_line((hx, hy), tip, dxfattribs={'layer': 'A-DOOR'})
    msp.add_arc((hx, hy), L, a0, a1, dxfattribs={'layer': 'A-DOOR'})
    if not d['id'].endswith('b'):
        (x0, y0), (x1, y1) = d['p0'], d['p1']
        txt(d['id'].rstrip('a'), (x0 + x1) / 2, (y0 + y1) / 2, 0.4, 'A-DOOR')
# stair
for poly, hgt, fl in STAIR_TREADS:
    pl(poly, 'A-STAIR')
msp.add_line((66.875, 33.4), (66.875, 25.2), dxfattribs={'layer': 'A-STAIR'})
txt('UP', 66.875, 33.9, 0.45, 'A-STAIR')
txt(f'LANDING +{fmt(LANDING_H)}', 66.875, 22.25, 0.32, 'A-STAIR')
# porch: single ramp + entrance landing; pedestrian gate + path
pl(PLATFORM, 'A-STAIR'); txt(f'ENTRANCE LANDING 2\'-6" @ FFL +{fmt(FFL)}', 62.75, 18.5, 0.35, 'A-STAIR')
pl(PORCH_TREAD, 'A-STAIR'); txt('2 RISERS @ 7 1/2" UP', 62.75, 16.75, 0.3, 'A-STAIR')
for poly, z in PED_STEPS: pl(poly, 'A-STAIR')
msp.add_line((58.4, 1.0), (58.4, 16.0), dxfattribs={'layer': 'A-STAIR'}); txt(f'RAMP 1:{1/RAMP_SLOPE:.1f} UP', 58.0, 8.5, 0.4, 'A-STAIR', rot=90)
pl(LAWN_PATH & PLOT, 'L-LAWN'); txt('STONE PATH', 33.0, 12.0, 0.35, 'L-LAWN', rot=90)
msp.add_line((PED_GATE[0], 0.19), (PED_GATE[1], 0.19), dxfattribs={'layer': 'A-DOOR', 'linetype': 'DASHED'})
txt('PEDESTRIAN GATE 3\'-6"', sum(PED_GATE) / 2, -1.2, 0.35, 'A-DOOR')
for x, y, t in ((0.0, -1.2, 'ROAD +/-0\'-0" (DATUM)'), (87.9167, -1.2, 'ROAD -6\'-0"'), (62.5, 0.6, f'GATE {fmt(GATE_Z)}')):
    txt(t, x, y, 0.4, 'A-DIMS')
txt('LAWN / PLOT LEVEL +/-0\'-0" (= ROAD AT P1)', 18, 3.5, 0.5, 'L-LAWN')
# furniture
for n, g, kind in FURN:
    pl(g, 'A-FURN' if kind == 'furniture' else 'A-FIXT')
pl(CAR, 'A-FURN')
# room names
from draw_plan import LABEL_POS
for k, r in R.items():
    x, y = LABEL_POS[k]; g = r['geom']; bx = g.bounds
    txt(r['name'], x, y, 0.55 if g.area > 100 else 0.4, 'A-ROOM-NAME')
    sub = (f"{fmt(bx[2]-bx[0])} x {fmt(bx[3]-bx[1])}" if (len(g.exterior.coords) == 5 and k not in ('PWD',)) else f"{g.area:.0f} SQ.FT")
    txt(sub, x, y - 0.9, 0.35, 'A-ROOM-NAME')
# dimensions
dimstyle = 'EZ_FEET'
ds = doc.dimstyles.new(dimstyle); ds.dxf.dimtxt = 0.45; ds.dxf.dimasz = 0.35; ds.dxf.dimexe = 0.3; ds.dxf.dimexo = 0.3
ds.dxf.dimtsz = 0.3; ds.dxf.dimgap = 0.15
def dim(p1, p2, base, angle=0):
    d = msp.add_linear_dim(base=base, p1=p1, p2=p2, angle=angle, dimstyle=dimstyle,
                           text=fmt(math.dist(p1, p2) if angle == 0 and p1[1] == p2[1] else abs((p2[1]-p1[1]) if angle == 90 else (p2[0]-p1[0]))),
                           dxfattribs={'layer': 'A-DIMS'})
    d.render()
for a, b in ((0, LINE_B), (LINE_B, 50.625), (51.375, 56.625), (57.375, 68.625), (69.375, 84.375), (EAST_FACE, 87.9167)):
    dim((a, 0), (b, 0), (0, -2.6))
dim((LINE_B, 0), (EAST_FACE, 0), (0, -4.2)); dim((0, 0), (87.9167, 0), (0, -8.4))
for a, b in ((0, FRONT), (3.75, 19.75), (20.5, 28.125), (28.875, 43.875)):
    dim((87.9, a), (87.9, b), (90.5, 0), angle=90)
for a, b in ((3.75, 19.75), (20.5, 24.5), (24.875, 33.0)):
    dim((36.1, a), (36.1, b), (34.0, 0), angle=90)
txt('DAATA HAMLET RESIDENCE - GROUND FLOOR PLAN (v2)  |  UNITS: FEET  |  ORIGIN = PEG P1', 14, 57, 1.0, 'A-TEXT', align=TA.LEFT)

# ---- south elevation outline, placed below the plan (offset Y = -40)
OY = -40
PLH = 1.5; TOP = PLH + 11
def rect(x0, y0, x1, y1, layer='A-ELEV'):
    msp.add_lwpolyline([(x0, y0 + OY), (x1, y0 + OY), (x1, y1 + OY), (x0, y1 + OY)], close=True, dxfattribs={'layer': layer})
msp.add_line((-3, OY), (91, OY), dxfattribs={'layer': 'A-ELEV'})
rect(LINE_B, 0, EAST_FACE, PLH); rect(LINE_B, PLH, 52.125, TOP - .5); rect(52.125, PLH, 57.375, TOP - .5)
rect(68.625, PLH, EAST_FACE, TOP - .5); rect(56.625, PLH, 57.375, TOP - .5); rect(68.625, PLH, 69.375, TOP - .5)
rect(56.625, TOP - 1.25, 69.375, TOP - .5); rect(LINE_B - .25, TOP - .5, EAST_FACE + .25, TOP)
for w in WINDOWS:
    (x0, y0), (x1, y1) = w['p0'], w['p1']
    if abs(y0 - GRID_Y['1']) < 1e-6 and abs(y1 - y0) < 1e-6:
        rect(min(x0, x1), PLH + w['sill'], max(x0, x1), PLH + w['head'], 'A-GLAZ')
        if w['kind'] == 'window':
            rect(min(x0, x1) - .75, PLH + w['head'] + .25, max(x0, x1) + .75, PLH + w['head'] + .6)
txt('SOUTH (ROAD-SIDE) ELEVATION - GROUND FLOOR', LINE_B, TOP + 3 + OY, 1.0, 'A-TEXT', align=TA.LEFT)

doc.saveas('out/daata_hamlet_GF_v2.dxf')
print('saved', len(msp))
