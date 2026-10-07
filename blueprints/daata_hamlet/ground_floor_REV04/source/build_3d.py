"""Blender (bpy) 3D model of the ground floor + 360 orbit render.
Usage: python3 build_3d.py [preview|video|blend]"""
import sys, math
import bpy, bmesh
import mapbox_earcut as earcut
import numpy as np
from shapely.geometry import box, Polygon, LineString
from shapely.ops import unary_union
sys.path.insert(0, '/home/claude/dh')
from model import *

MODE = sys.argv[1] if len(sys.argv) > 1 else 'preview'
FT = 0.3048
PL = 1.5                          # FFL above road
CX, CY = 60.0, 30.0               # scene centre (ft)

bpy.ops.wm.read_factory_settings(use_empty=True)
scene = bpy.context.scene

# ------------------------------------------------------------- materials
def mat(name, rgb, rough=0.6, metal=0.0, alpha=1.0, emit=None, transmission=0.0):
    m = bpy.data.materials.new(name); m.use_nodes = True
    b = m.node_tree.nodes['Principled BSDF']
    b.inputs['Base Color'].default_value = (*rgb, 1)
    b.inputs['Roughness'].default_value = rough
    b.inputs['Metallic'].default_value = metal
    if transmission:
        b.inputs['Transmission Weight'].default_value = transmission
        b.inputs['IOR'].default_value = 1.45
    if alpha < 1:
        b.inputs['Alpha'].default_value = alpha
    return m

def srgb(h):
    h = h.lstrip('#'); c = [int(h[i:i+2], 16) / 255 for i in (0, 2, 4)]
    return tuple(((x + 0.055) / 1.055) ** 2.4 if x > 0.04045 else x / 12.92 for x in c)

M = {
    'wall': mat('wall', srgb('#f4f1ea'), 0.85),
    'wallcut': mat('wallcut', srgb('#3b3b3b'), 0.9),
    'stone': mat('stone', srgb('#d9c7a6'), 0.9),
    'plinth': mat('plinth', srgb('#a8a29e'), 0.9),
    'wood': mat('wood', srgb('#b98a5a'), 0.5),
    'tile': mat('tile', srgb('#e7e5e4'), 0.35),
    'wet': mat('wet', srgb('#cbd5e1'), 0.3),
    'paver': mat('paver', srgb('#9ca3af'), 0.8),
    'grass': mat('grass', srgb('#6fa95b'), 0.95),
    'ground': mat('ground', srgb('#d6d3d1'), 0.95),
    'road': mat('road', srgb('#4b5563'), 0.9),
    'glass': mat('glass', srgb('#9cc7e6'), 0.05, transmission=0.85),
    'frame': mat('frame', srgb('#2d2d2d'), 0.4, 0.6),
    'door': mat('door', srgb('#7a4a24'), 0.45),
    'fabric': mat('fabric', srgb('#64748b'), 0.9),
    'bed': mat('bed', srgb('#f5f5f4'), 0.9),
    'counter': mat('counter', srgb('#1f2937'), 0.25),
    'cabinet': mat('cabinet', srgb('#e2d6c2'), 0.5),
    'porcelain': mat('porcelain', srgb('#ffffff'), 0.15),
    'stair': mat('stair', srgb('#efe9df'), 0.35),
    'column': mat('column', srgb('#e5e7eb'), 0.7),
    'car': mat('car', srgb('#111827'), 0.25, 0.7),
    'ots': mat('ots', srgb('#bde0fe'), 0.6),
    'leaf': mat('leaf', srgb('#3f7d3a'), 0.9),
    'trunk': mat('trunk', srgb('#6b4f3a'), 0.9),
    'boundary': mat('boundary', srgb('#e7e2d6'), 0.9),
    'gate': mat('gate', srgb('#3b3028'), 0.45, 0.6),
    'text': mat('text', srgb('#1f2937'), 0.6),
    'red': mat('red', srgb('#c0392b'), 0.6),
}

def P(x, y): return ((x - CX) * FT, (y - CY) * FT)

def extrude(geom, z0, z1, name, m):
    """extrude a shapely (multi)polygon between z0..z1 (ft, road datum)"""
    objs = []
    for poly in getattr(geom, 'geoms', [geom]):
        if poly.is_empty or poly.area < 1e-4: continue
        poly = poly.buffer(0)
        if poly.geom_type != 'Polygon':
            objs += extrude(poly, z0, z1, name, m); continue
        rings = [list(poly.exterior.coords)[:-1]] + [list(r.coords)[:-1] for r in poly.interiors]
        verts2 = [P(x, y) for r in rings for x, y in r]
        ends = np.cumsum([len(r) for r in rings]).astype(np.uint32)
        tris = earcut.triangulate_float64(np.array(verts2, dtype=np.float64).reshape(-1, 2), ends).reshape(-1, 3)
        n = len(verts2)
        bm = bmesh.new()
        vb = [bm.verts.new((x, y, z0 * FT)) for x, y in verts2]
        vt = [bm.verts.new((x, y, z1 * FT)) for x, y in verts2]
        for a, b, c in tris:
            try:
                bm.faces.new((vt[a], vt[b], vt[c]))
                bm.faces.new((vb[c], vb[b], vb[a]))
            except ValueError: pass
        s = 0
        for r in rings:
            k = len(r)
            for i in range(k):
                i0, i1 = s + i, s + (i + 1) % k
                try: bm.faces.new((vb[i0], vb[i1], vt[i1], vt[i0]))
                except ValueError: pass
            s += k
        bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
        me = bpy.data.meshes.new(name); bm.to_mesh(me); bm.free()
        ob = bpy.data.objects.new(name, me); ob.data.materials.append(m)
        scene.collection.objects.link(ob); objs.append(ob)
    return objs

def cube(x0, y0, x1, y1, z0, z1, name, m):
    return extrude(box(x0, y0, x1, y1), z0, z1, name, m)

FL = FFL                 # floor level (-0'-9")
CL = FFL + CEIL           # ceiling level (wall top in cut-away)

# ------------------------------------------------------------- site (road falls 6'-0" west -> east)
def sloped_quad(x0, y0, x1, y1, dz, name, m, n=24):
    """thin slab whose top follows road_z(x) + dz"""
    bm = bmesh.new()
    xs = np.linspace(x0, x1, n + 1)
    top = [[bm.verts.new((*P(x, y), (road_z(x) + dz) * FT)) for x in xs] for y in (y0, y1)]
    bot = [[bm.verts.new((*P(x, y), (road_z(x) + dz - 0.5) * FT)) for x in xs] for y in (y0, y1)]
    for i in range(n):
        bm.faces.new((top[0][i], top[0][i + 1], top[1][i + 1], top[1][i]))
        bm.faces.new((bot[0][i], bot[1][i], bot[1][i + 1], bot[0][i + 1]))
    me = bpy.data.meshes.new(name); bm.to_mesh(me); bm.free()
    ob = bpy.data.objects.new(name, me); ob.data.materials.append(m); scene.collection.objects.link(ob)
sloped_quad(-60, -18, 160, -0.02, 0.0, 'road', M['road'])
sloped_quad(-60, -40, 160, -18, 0.15, 'ground_s', M['ground'])
sloped_quad(-60, 0.0, 160, 110, -0.25, 'ground_n', M['ground'])   # neighbours, under the fill
# filled plot (level +/-0), its edge is the stone retaining wall; porch ramp carved out
fill = PLOT - RAMP - PORCH_TREAD - box(PED_GATE[0], -1, PED_GATE[1], 0.375 + 3 * 10 / 12) - box(-1, -1, 100, FRONT_T) - box(GATE_POCKET_X[0], -1, GATE_POCKET_X[1], 1.25)
extrude(fill, -7.0, PLOT_Z, 'fill', M['stone'])
lawn = PLOT & box(-5, -5, LINE_B, 80)
extrude(lawn, PLOT_Z, PLOT_Z + 0.25, 'lawn', M['grass'])
for st in STONES:
    extrude(st, PLOT_Z, PLOT_Z + 0.3, 'stone', M['plinth'])
rest = (PLOT - lawn - FOOTPRINT - R['PORCH']['geom'])
extrude(rest, PLOT_Z, PLOT_Z + 0.1, 'yard', M['paver'])
# car ramp (sloped solid) to the wheel-stop, tread, entrance landing
bm = bmesh.new()
x0r, x1r = PORCH_X
pts = []
for (x, y) in ((x0r, 0), (x1r, 0), (x1r, RAMP_END_Y), (x0r, RAMP_END_Y)):
    pts.append((bm.verts.new((*P(x, y), ramp_z(y) * FT)), bm.verts.new((*P(x, y), -7 * FT))))
bm.faces.new([p[0] for p in pts]); bm.faces.new([p[1] for p in pts][::-1])
for i in range(4):
    a_, b_ = pts[i], pts[(i + 1) % 4]
    bm.faces.new((a_[1], b_[1], b_[0], a_[0]))
me = bpy.data.meshes.new('ramp'); bm.to_mesh(me); bm.free()
ob = bpy.data.objects.new('ramp', me); ob.data.materials.append(M['paver']); scene.collection.objects.link(ob)
extrude(PLATFORM, -7.0, FFL, 'entrance_landing', M['plinth'])
extrude(PORCH_TREAD, -7.0, RAMP_TOP_Z + PORCH_RISER, 'porch_tread', M['stair'])
# boundary walls (inside the plot line) on the sides/back, 7'-0" above the plot
bw = PLOT - PLOT.buffer(-0.375, join_style=2)
bw = bw - box(-1, -1, 100, 0.375)
bw = bw - FOOTPRINT.buffer(0.01)
extrude(bw, PLOT_Z, PLOT_Z + 7.0, 'boundary', M['boundary'])
# front: stone retaining wall (sloping foot follows the road) + 9" solid wall 4'-0" above the plot + coping
def xprism(outer, holes, y0, y1, name, m):
    """polygon in the X-Z plane (feet, absolute z) with optional holes, extruded across Y y0..y1"""
    rings = [outer] + holes
    flat = [p for r in rings for p in r]
    ends = np.cumsum([len(r) for r in rings]).astype(np.uint32)
    tris = earcut.triangulate_float64(np.array(flat, dtype=np.float64), ends).reshape(-1, 3)
    bm = bmesh.new()
    va = [bm.verts.new((*P(x, y0), z * FT)) for x, z in flat]
    vb = [bm.verts.new((*P(x, y1), z * FT)) for x, z in flat]
    for i, j, k in tris:
        try: bm.faces.new((va[i], va[j], va[k])); bm.faces.new((vb[k], vb[j], vb[i]))
        except ValueError: pass
    s0 = 0
    for r in rings:
        n = len(r)
        for i in range(n):
            a_, b_ = s0 + i, s0 + (i + 1) % n
            try: bm.faces.new((va[a_], va[b_], vb[b_], vb[a_]))
            except ValueError: pass
        s0 += n
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    me = bpy.data.meshes.new(name); bm.to_mesh(me); bm.free()
    ob = bpy.data.objects.new(name, me); ob.data.materials.append(m); scene.collection.objects.link(ob)
    return ob

def front_wall(x0, x1, y0, y1, name, top=PLOT_Z + FRONT_WALL_H):
    xs = list(np.arange(x0, x1, 1.0)) + [x1]
    retaining = [(x, road_z(x) - 0.4) for x in xs] + [(x1, PLOT_Z), (x0, PLOT_Z)]
    xprism(retaining, [], y0, y1, name + '_retaining', M['stone'])
    xprism([(x0, PLOT_Z), (x1, PLOT_Z), (x1, top), (x0, top)], [], y0, y1, name + '_wall', M['boundary'])
    xprism([(x0 - .04, top), (x1 + .04, top), (x1 + .04, top + .25), (x0 - .04, top + .25)], [], y0 - .08, y1 + .08, name + '_coping', M['plinth'])

g0, g1 = PED_GATE
front_wall(0.0, g0, 0.0, FRONT_T, 'front_w')
front_wall(g1, PORCH_X[0] - 0.75, 0.0, FRONT_T, 'front_m')
front_wall(GATE_POCKET_X[1], 87.9167, 0.0, FRONT_T, 'front_e')
# gate pocket: two skins with the 3" track cavity between, one coping over both
front_wall(GATE_POCKET_X[0], GATE_POCKET_X[1], 0.0, GATE_Y[0], 'pocket_outer')
front_wall(GATE_POCKET_X[0], GATE_POCKET_X[1], GATE_Y[1], GATE_Y[1] + 0.5, 'pocket_inner')
xprism([(GATE_POCKET_X[0], PLOT_Z + FRONT_WALL_H), (GATE_POCKET_X[1], PLOT_Z + FRONT_WALL_H),
        (GATE_POCKET_X[1], PLOT_Z + FRONT_WALL_H + .25), (GATE_POCKET_X[0], PLOT_Z + FRONT_WALL_H + .25)], [], -.08, 1.33, 'pocket_coping', M['plinth'])
# gate pillar on the west jamb
xprism([(PORCH_X[0] - 0.75, road_z(PORCH_X[0]) - 0.4), (PORCH_X[0], road_z(PORCH_X[0]) - 0.4),
        (PORCH_X[0], PLOT_Z + FRONT_WALL_H + 0.5), (PORCH_X[0] - 0.75, PLOT_Z + FRONT_WALL_H + 0.5)], [], -0.1, 1.0, 'gate_pillar', M['stone'])
# sliding car gate (closed): horizontal-slat panel, track at the ramp foot -> wall top
def slat_panel(x0, x1, z0, z1, name, y0, y1):
    holes, z = [], z0 + 1.0
    while z + 0.12 < z1 - 0.45:
        holes.append([(x0 + 0.35, z), (x0 + 0.35, z + 0.09), (x1 - 0.35, z + 0.09), (x1 - 0.35, z)])
        z += 0.42
    return xprism([(x0, z0), (x1, z0), (x1, z1), (x0, z1)], holes, y0, y1, name, M['gate'])
slat_panel(GATE_X[0], GATE_X[1], GATE_BOTTOM_Z, PLOT_Z + FRONT_WALL_H, 'GATE', GATE_Y[0] + .06, GATE_Y[1] - .06)
# pedestrian gate (closed) in the lawn wall, road -> wall top
slat_panel(g0 + .05, g1 - .05, road_z(sum(PED_GATE) / 2) + .05, PLOT_Z + FRONT_WALL_H, 'PED_GATE', 0.16, 0.28)
# pedestrian gate: 4 steps up from the road into the lawn (carved into the fill), open gate leaf
extrude(box(g0, -0.01, g1, 0.375 + 3 * 10 / 12), road_z(33.0) - 0.05, road_z(33.0), 'ped_base', M['plinth'])
for poly, z in PED_STEPS:
    extrude(poly, -7.0, z, 'ped_step', M['stair'])

# ------------------------------------------------------------- building
extrude(FOOTPRINT - R['PORCH']['geom'] - R['OTS']['geom'], PLOT_Z, FL, 'plinth', M['plinth'])
# walls & columns flanking the porch go down to the ramp
extrude(WALLS & box(56.0, 0, 70.0, 20.6), -7.0, FL, 'porch_wall_base', M['plinth'])
extrude(R['OTS']['geom'], PLOT_Z, PLOT_Z + 0.6, 'ots', M['grass'])
for k, r in R.items():
    if k in ('PORCH', 'OTS'): continue
    m = M['wood'] if r['finish'] == 'wood' else (M['wet'] if r['kind'] == 'wet' else M['tile'])
    extrude(r['geom'], FL - 0.02, FL + 0.02, 'floor_' + k, m)

cuts = unary_union([seg_rect(o['p0'], o['p1'], o['t']) for o in DOORS + WINDOWS])
WALL_SOLID = WALLS - cuts
front_skin = box(LINE_B, FRONT, 51.375, FRONT + 0.75) | box(68.625, FRONT, EAST_FACE, FRONT + 0.75)
extrude(WALL_SOLID - front_skin - box(65.1, 23.99, 68.65, 24.39), FL, CL, 'walls', M['wall'])   # under-stair partition built separately (stops under flight-1)
extrude(WALL_SOLID & front_skin, FL, CL, 'walls_stone', M['stone'])
# cut-plane cap (dark top edge so the plan reads from above)
extrude(WALL_SOLID - box(65.1, 23.99, 68.65, 24.39), CL, CL + 0.05, 'wallcap', M['wallcut'])
for k, c in COLUMNS.items():
    extrude(c, CL, CL + 0.07, 'colcap', M['frame'])   # columns sit inside the walls; mark them on the cut top
for o in DOORS + WINDOWS:
    rect = seg_rect(o['p0'], o['p1'], o['t'] - 0.04) & WALLS.buffer(0.05)
    if o in WINDOWS:
        extrude(rect, FL, FL + o['sill'], 'sill_' + o['id'], M['wall'] if o['sill'] > 0 else M['frame'])
        extrude(rect, FL + o['head'], CL, 'head_' + o['id'], M['wall'])
        (x0, y0), (x1, y1) = o['p0'], o['p1']
        extrude(seg_rect(o['p0'], o['p1'], 0.06), FL + o['sill'], FL + o['head'], 'glass_' + o['id'], M['glass'])
        L = math.hypot(x1 - x0, y1 - y0)
        for t in np.linspace(0, 1, max(2, round(L / 2.4)) + 1):
            px, py = x0 + (x1 - x0) * t, y0 + (y1 - y0) * t
            extrude(Point_(px, py).buffer(0.09, cap_style=3) if False else box(px - .08, py - .08, px + .08, py + .08),
                    FL + o['sill'], FL + o['head'], 'mull', M['frame'])
    else:
        extrude(rect, FL + o['h'], CL, 'lintel_' + o['id'], M['wall'])
# door leaves, opened at 60 degrees
from draw_plan import door_geom
for d in DOORS:
    if d['kind'] != 'swing':
        if d['kind'] == 'slide':                       # pocket doors are shown open (inside the wall)
            extrude(slide_park(d), FL, FL + d['h'], 'slide_' + d['id'], M['door'])
        continue
    (hx, hy), tip, L, a0, a1, _ = door_geom(d)
    ang = math.radians(a0 if d['side'] * 1 else a0)
    # leaf in open position: take the swing arc mid-point direction (45 deg open)
    ex, ey = tip                                   # leaf fully open, parked against its wall
    ux_, uy_ = (ex - hx) / L, (ey - hy) / L
    leaf = LineString([(hx + ux_ * 0.05, hy + uy_ * 0.05), (ex, ey)]).buffer(0.08, cap_style=2)
    extrude(leaf, FL, FL + d['h'], 'leaf_' + d['id'], M['door'])

# ------------------------------------------------------------- stair: real flights with open soffit (space under is visible)
R_FT = RISER / 12
def prism(profile, c0, c1, axis, name, m):
    """profile = [(s, z)] in feet (z above FFL); axis 'y': s=Y, extruded X c0..c1;  axis 'x': s=X, extruded Y c0..c1"""
    pr = np.array(profile, dtype=np.float64)
    tris = earcut.triangulate_float64(pr, np.array([len(pr)], dtype=np.uint32)).reshape(-1, 3)
    def W(s_, z_, c_):
        x, y = (c_, s_) if axis == 'y' else (s_, c_)
        return (*P(x, y), (FL + z_) * FT)
    bm = bmesh.new()
    va = [bm.verts.new(W(s_, z_, c0)) for s_, z_ in profile]
    vb = [bm.verts.new(W(s_, z_, c1)) for s_, z_ in profile]
    for a, b, c in tris:
        try: bm.faces.new((va[a], va[b], va[c])); bm.faces.new((vb[c], vb[b], vb[a]))
        except ValueError: pass
    n = len(profile)
    for i in range(n):
        j = (i + 1) % n
        try: bm.faces.new((va[i], va[j], vb[j], vb[i]))
        except ValueError: pass
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    me = bpy.data.meshes.new(name); bm.to_mesh(me); bm.free()
    ob = bpy.data.objects.new(name, me); ob.data.materials.append(m); scene.collection.objects.link(ob)
    return ob

def flight_prof(s_start, d, h0, n, to_floor=False):
    """n treads from s_start in direction d (+1/-1), first riser from h0; ends with riser up to h0+(n+1)R"""
    pts = [(s_start, h0)]
    for k in range(n):
        s0 = s_start + d * k * TREAD
        pts += [(s0, h0 + (k + 1) * R_FT), (s0 + d * TREAD, h0 + (k + 1) * R_FT)]
    s_end = s_start + d * n * TREAD
    pts += [(s_end, h0 + (n + 1) * R_FT)]
    zs = lambda s_: h0 + abs(s_ - s_start) / TREAD * R_FT - 0.42
    pts += [(s_end, zs(s_end))]
    if to_floor:
        pts += [(s_start + d * 0.42 * TREAD / R_FT, 0.0)]
    else:
        pts += [(s_start, h0 - 0.42)]
    return pts

# flight-1 (on the floor, rising south along the D wall)
prism(flight_prof(F1_BOT_Y, -1, 0.0, F1_RISERS - 1, to_floor=True), F1_X[0], F1_X[1], 'y', 'flight1', M['stair'])
# landing slab (5")
extrude(LANDING, FL + LANDING_H - 5 / 12, FL + LANDING_H, 'landing', M['stair'])
if STAIR_VERSION == 'L':
    prism(flight_prof(65.125, -1, LANDING_H, F2_RISERS - 1), F2_Y[0], F2_Y[1], 'x', 'flight2', M['stair'])
    rails = [('y', 65.1, (F1_BOT_Y, 0.0), (24.0, LANDING_H)), ('x', 24.02, (65.125, LANDING_H), (F2_END_X, FF_TO_FF))]
else:
    prism(flight_prof(24.0, +1, LANDING_H, F2_RISERS - 1), U_F2_X[0], U_F2_X[1], 'y', 'flight2', M['stair'])
    rails = [('y', 65.1, (F1_BOT_Y, 0.0), (24.0, LANDING_H)), ('y', 61.6, (24.0, LANDING_H), (F2_END_Y, FF_TO_FF)),
             ('x', 24.02, (61.625, LANDING_H), (61.625, LANDING_H))]
    rails = rails[:2]
# 3'-0" glass balustrades following the pitch
for ax_, c, (s0, z0), (s1, z1) in rails:
    prism([(s0, z0 + 0.1), (s1, z1 + 0.1), (s1, z1 + 3.0), (s0, z0 + 3.0)], c - 0.03, c + 0.03, ax_, 'balustrade', M['glass'])
# under-stair partition at the top of flight-1 (separates lounge under-stair from the lobby)
pass  # no under-stair partition (open to the lobby)

# ------------------------------------------------------------- furniture
HEIGHT = {'KING': (1.8, 'bed'), 'SIDE': (1.8, 'cabinet'), 'STUDY': (2.5, 'cabinet'), 'SHOWER': (0.25, 'porcelain'),
          'WC': (1.4, 'porcelain'), 'BASIN': (2.8, 'porcelain'), 'WARDROBE': (7.0, 'cabinet'), 'COUNTER': (3.0, 'counter'),
          'FRIDGE': (6.0, 'porcelain'), 'DINING': (2.5, 'wood'), 'CHAIRS': (1.5, 'fabric'), 'TV': (1.6, 'counter'),
          'SOFA': (2.6, 'fabric'), 'COFFEE': (1.3, 'wood'), 'ARMCHAIR': (2.6, 'fabric'), 'CENTRE': (1.3, 'wood')}
for name, g, kind in FURN:
    key = name.split()[0]
    h, mk = HEIGHT.get(key, (2.0, 'cabinet'))
    if key == 'SOFA' or key == 'ARMCHAIR':
        extrude(g, FL, FL + 1.4, name, M[mk])
        extrude(g.buffer(-0.2), FL + 1.4, FL + 1.6, name, M['bed'])
    elif key == 'KING':
        extrude(g, FL, FL + 1.2, name, M['wood']); extrude(g.buffer(-0.15), FL + 1.2, FL + h, name, M['bed'])
    else:
        extrude(g, FL, FL + h, name, M[mk])
    if key == 'SHOWER':
        x0, y0, x1, y1 = g.bounds
# car parked on the 1:6 ramp (tilted about its mid-point)
x0, y0, x1, y1 = CAR.bounds
cy = (y0 + y1) / 2; cz = ramp_z(cy)
parts = []
parts += cube(x0 + .2, y0 + .3, x1 - .2, y1 - .3, cz + 1.0, cz + 3.4, 'car_body', M['car'])
parts += cube(x0 + .6, y0 + 3.0, x1 - .6, y1 - 4.0, cz + 3.4, cz + 5.6, 'car_cabin', M['glass'])
for (wx, wy) in ((x0 + .1, y0 + 2.5), (x1 - .9, y0 + 2.5), (x0 + .1, y1 - 3.5), (x1 - .9, y1 - 3.5)):
    parts += cube(wx, wy, wx + .8, wy + 2.2, cz, cz + 2.2, 'wheel', M['frame'])
th = math.atan(RAMP_SLOPE); py, pz = (cy - CY) * FT, cz * FT
for ob in parts:
    for v in ob.data.vertices:
        yy, zz = v.co.y - py, v.co.z - pz
        v.co.y = py + yy * math.cos(th) - zz * math.sin(th)
        v.co.z = pz + yy * math.sin(th) + zz * math.cos(th)

# trees in the lawn
for tx, ty, r in ((12, 6, 3.0), (22, 12, 3.6), (30, 6, 2.6), (27, 20, 2.4)):
    bpy.ops.mesh.primitive_cylinder_add(radius=0.35 * FT, depth=6 * FT, location=(*P(tx, ty), 3 * FT))
    bpy.context.object.data.materials.append(M['trunk'])
    bpy.ops.mesh.primitive_ico_sphere_add(radius=r * FT, subdivisions=2, location=(*P(tx, ty), (6 + r * .7) * FT))
    bpy.context.object.data.materials.append(M['leaf']); bpy.ops.object.shade_smooth()

# floor labels
def label(txt_, x, y, size=1.0):
    bpy.ops.object.text_add(location=(*P(x, y), (FL + 0.05) * FT))
    t = bpy.context.object; t.data.body = txt_; t.data.size = size * FT
    t.data.align_x = 'CENTER'; t.data.align_y = 'CENTER'; t.data.materials.append(M['text'])
from draw_plan import LABEL_POS
for k, r in R.items():
    if k in ('PORCH', 'OTS', 'PASS', 'STORE'): continue
    x, y = LABEL_POS[k]
    nm = r['name'].replace('FAMILY LOUNGE + DINING', 'LOUNGE').replace(' (BED-2)', '').replace(' (BED-1)', '').replace(' (DRAWING)', '')
    label(nm, x, y + (2.0 if k in ('BED2', 'DRAW') else 0), 1.1 if r['geom'].area > 100 else 0.6)

# ------------------------------------------------------------- light, world, camera
sun = bpy.data.lights.new('sun', 'SUN'); sun.energy = 3.2; sun.angle = math.radians(2.5)
so = bpy.data.objects.new('sun', sun); scene.collection.objects.link(so)
so.rotation_euler = (math.radians(48), 0, math.radians(-35))
world = bpy.data.worlds.new('w'); scene.world = world; world.use_nodes = True
bg = world.node_tree.nodes['Background']; bg.inputs['Color'].default_value = (*srgb('#dbe7f3'), 1); bg.inputs['Strength'].default_value = 0.9

cam = bpy.data.cameras.new('cam'); cam.lens = 28
co = bpy.data.objects.new('cam', cam); scene.collection.objects.link(co); scene.camera = co
target = bpy.data.objects.new('target', None); scene.collection.objects.link(target)
target.location = (*P(58, 24), 0 * FT)
tc = co.constraints.new('TRACK_TO'); tc.target = target; tc.track_axis = 'TRACK_NEGATIVE_Z'; tc.up_axis = 'UP_Y'

RADIUS, HEIGHT_C = 22.0, 14.0       # metres

def place(t):
    a = math.radians(-90) + 2 * math.pi * t          # start from the road (south)
    co.location = (target.location.x + RADIUS * math.cos(a), target.location.y + RADIUS * math.sin(a), HEIGHT_C)

scene.render.engine = 'CYCLES'
scene.cycles.device = 'CPU'
scene.cycles.samples = 12
scene.cycles.use_denoising = True
scene.cycles.max_bounces = 4
scene.render.film_transparent = False
scene.view_settings.view_transform = 'AgX'
scene.view_settings.look = 'AgX - Medium High Contrast'

if MODE == 'preview':
    scene.render.resolution_x, scene.render.resolution_y = 1280, 720
    for i, t in enumerate((0.0,)):
        place(t); scene.render.filepath = f'/home/claude/dh/r_prev_{i}.png'
        bpy.ops.render.render(write_still=True)
elif MODE == 'video':
    N = int(sys.argv[2]) if len(sys.argv) > 2 else 240
    s0, s1 = int(sys.argv[3]), int(sys.argv[4])
    scene.render.resolution_x, scene.render.resolution_y = 1280, 720
    for i in range(s0, min(s1, N)):
        place(i / N); scene.render.filepath = f'/home/claude/dh/frames/f_{i:04d}.png'
        bpy.ops.render.render(write_still=True)
elif MODE == 'stills':
    co.constraints.remove(tc)
    cam.lens = 16
    scene.cycles.samples = 32
    scene.render.resolution_x, scene.render.resolution_y = 1600, 900
    V = STAIR_VERSION
    shots = {
        'A_lounge_looking_south': ((62.0, 36.5, 5.3), (63.5, 20.0, 4.0)),
        'B_foyer_looking_east_into_lobby': ((59.0, 22.4, 5.0), (75.0, 22.0, 4.2)),
        'C_dining_looking_east_at_stair': ((53.5, 27.5, 4.8), (68.0, 25.5, 5.5)),
        'D_porch_looking_north_at_entrance': ((63.0, 5.0, 4.6), (63.0, 22.0, 5.0)),
    }
    import mathutils
    for nm_, (eye, look) in shots.items():
        e = mathutils.Vector((*P(eye[0], eye[1]), (FL + eye[2]) * FT)); l = mathutils.Vector((*P(look[0], look[1]), (FL + look[2]) * FT))
        co.location = e
        co.rotation_euler = (l - e).to_track_quat('-Z', 'Y').to_euler()
        scene.render.filepath = f'/home/claude/dh/stills/{V}_{nm_}.png'
        bpy.ops.render.render(write_still=True)
elif MODE == 'blend':
    place(0)
    # drop camera/light helpers and 3D text (labels are drawn by the web viewer)
    for ob in list(bpy.data.objects):
        if ob.type in ('FONT', 'CAMERA', 'EMPTY', 'LIGHT'):
            bpy.data.objects.remove(ob, do_unlink=True)
    bpy.ops.export_scene.gltf(filepath=f'/home/claude/dh/web/DH-GF-{STAIR_VERSION}.glb', export_format='GLB',
                              export_apply=True, export_draco_mesh_compression_enable=False)
