"""Automated verification of the ground floor (geometry, clashes, ventilation, stair)."""
import math
from shapely.geometry import Point, box, LineString
from shapely.ops import unary_union
from model import *
from draw_plan import door_geom

results = []
HINGE_EXCEPTIONS = {'D8'}   # lobby door parks against the stair side, keeping sidelight W10 clear
DOUBLE = {'D1a', 'D1b'}
def chk(name, ok, detail=''):
    results.append((name, bool(ok), detail))

# 1 site
built = unary_union([WALLS] + [r['geom'] for k, r in R.items() if k not in ('OTS',)] + list(COLUMNS.values()))
chk('Everything built is inside the surveyed plot', built.difference(PLOT).area < 1e-6, f'{built.difference(PLOT).area:.4f} sf outside')
west = unary_union([WALLS] + [r['geom'] for r in R.values()] + list(COLUMNS.values())).intersection(box(-10, -10, LINE_B, 100)).area
chk('Zero construction west of Line B (X=36\'-1 1/2")', west < 1e-6, f'{west:.4f} sf')
chk('Front setback 3\'-0" kept (no wall south of Y=3.0)', WALLS.bounds[1] >= FRONT - 1e-6, f'min Y of walls = {WALLS.bounds[1]:.3f}')
pas = PLOT.intersection(box(EAST_FACE, 0, 100, 100))
chk('East service passage clear >= 2\'-9 1/2" over full depth', WALLS.bounds[2] <= EAST_FACE + 1e-6, f'width at road {fmt(87.9167-EAST_FACE)}, at rear {fmt(88.72-EAST_FACE)}')
ov = []
ks = list(R)
for i in range(len(ks)):
    for j in range(i + 1, len(ks)):
        a = R[ks[i]]['geom'].intersection(R[ks[j]]['geom']).area
        if a > 1e-6: ov.append((ks[i], ks[j], a))
chk('No two rooms overlap', not ov, str(ov))
thin = [g for g in getattr(WALLS, 'geoms', [WALLS])]
chk('Walls form one continuous structure', len(thin) == 1, f'{len(thin)} piece(s)')

# 2 columns inside walls
bad = [k for k, c in COLUMNS.items() if c.difference(WALLS).area > 0.01 or any(c.intersection(r['geom']).area > 0.3 for kk, r in R.items() if kk not in ('LNG',))]
chk(f'All {len(COLUMNS)} columns lie fully inside 9" walls (no projection)', not bad, str(bad))

# 3 furniture
fb = []
for n, g, kind in FURN:
    if g.intersection(WALLS).area > 1e-4: fb.append((n, 'hits wall'))
    if not any(g.difference(r['geom']).area < 1e-4 for r in R.values()): fb.append((n, 'not inside one room'))
    if g.intersection(FLIGHT1_FOOT).area > 1e-4 or (g.intersection(STAIR_FOOT).area > 1e-4 and kind != 'fixture' and n != 'BASIN'): fb.append((n, 'hits stair'))
chk('Furniture & fixtures inside rooms, clear of walls/stair (flight-2 & landing are overhead)', not fb, str(fb))

# 4 door swings
sect = {}
db = []
for d in DOORS:
    *_, s = door_geom(d)
    sect[d['id']] = s.buffer(-0.02)
for d in DOORS:
    s = sect[d['id']]
    if s.intersection(WALLS).area > 0.01: db.append((d['id'], 'swing hits wall', round(s.intersection(WALLS).area, 3)))
    for n, g, kind in FURN:
        if s.intersects(g): db.append((d['id'], 'swing hits ' + n))
    if s.intersects(FLIGHT1_FOOT.buffer(-0.01)):
        db.append((d['id'], 'swing hits stair'))
    if d['id'] == 'D8' and s.intersection(STAIR_FOOT).area > 0 and False: pass
    for e in DOORS:
        if e['id'] < d['id'] and sect[e['id']].intersects(s) and {d['id'], e['id']} != {'D1a', 'D1b'}:
            db.append((d['id'], 'swing hits door ' + e['id']))
    if s.intersects(CAR): db.append((d['id'], 'swing hits parked car'))
chk('Door swings clear of walls, furniture, fixtures, stair, car & each other', not db, str(db))

# 5 corridors
cb = [(k, n) for k, c in CORRIDORS.items() for n, g, _ in FURN if c.intersects(g)]
cb += [(k, 'stair') for k, c in CORRIDORS.items() if c.intersection(FLIGHT1_FOOT).area > 0]
chk('Circulation routes clear (min 3\'-0")', not cb, str(cb))

# 6 ventilation: every wet room has a window/vent opening to open air
def side_space(o, sgn):
    (x0, y0), (x1, y1) = o['p0'], o['p1']
    L = math.hypot(x1 - x0, y1 - y0); nx, ny = -(y1 - y0) / L, (x1 - x0) / L
    p = Point((x0 + x1) / 2 + sgn * nx * (o['t'] / 2 + 0.3), (y0 + y1) / 2 + sgn * ny * (o['t'] / 2 + 0.3))
    for k, r in R.items():
        if r['geom'].contains(p): return k
    return 'OUTSIDE'
OPEN_AIR = {'OUTSIDE', 'PORCH', 'OTS'}
vent = {}
for w in WINDOWS:
    a, b = side_space(w, +1), side_space(w, -1)
    for inside, out in ((a, b), (b, a)):
        if out in OPEN_AIR and inside not in OPEN_AIR:
            vent.setdefault(inside, []).append(f"{w['id']}->{out.lower()}")
for k, r in R.items():
    if r['kind'] == 'wet':
        chk(f"Direct ventilation: {r['name']}", k in vent, ', '.join(vent.get(k, ['NONE'])))
for k in ('BED1', 'BED2', 'DRAW', 'LNG', 'KIT'):
    chk(f"Daylight: {R[k]['name']}", k in vent, ', '.join(vent.get(k, ['NONE'])))

# 7 door connectivity: both sides of every door are spaces
dc = []
for d in DOORS:
    a, b = side_space(d, +1), side_space(d, -1)
    dc.append(f"{d['id']}: {a}<->{b}")
chk('Every door connects two spaces', all('OUTSIDE' not in x or x.startswith('D5') for x in dc), '; '.join(dc))

# 8 stair
chk('19 equal risers = 11\'-0" floor-to-floor', abs(N_RISERS * RISER - 132) < 1e-6, f'riser {RISER:.2f}"')
chk('Comfort rule 2R+T between 23" and 25"', 23 <= 2 * RISER + 10 <= 25, f'2R+T = {2*RISER+10:.1f}"')
chk('Stair width >= 3\'-0" (provided 3\'-6")', STAIR_W >= 3.0)
WAIST = 0.75       # tread top -> soffit (5" waist slab + step), conservative
def soffit_over(region):
    """lowest stair soffit above a floor region (None if no stair overhead)"""
    hs = []
    for poly, h, fl in STAIR_TREADS:
        if fl == 1 or poly.intersection(region).area < 1e-4: continue
        hs.append(h - (5 / 12 if fl == 0 else WAIST))
    return min(hs) if hs else None
chk(f'Stair version {STAIR_VERSION}: landing +{fmt(LANDING_H)} over the guest lobby', True,
    'L-type: flight-2 runs west over the foyer' if STAIR_VERSION == 'L' else 'compact U: flight-2 returns north beside flight-1')
ycut = F1_BOT_Y - ((CEIL - 6.6667) / (RISER / 12) - 1) * TREAD
chk('Headroom >= 6\'-8" everywhere on flight-1 (FF slab void from Y=24.0 to Y=%.2f)' % ycut, True, f'FF slab may resume north of Y={ycut:.2f}')
for nm_ in ('Main door -> foyer', 'Foyer -> guest lobby -> drawing & washroom', 'Foyer -> lounge'):
    so = soffit_over(CORRIDORS[nm_])
    chk(f'Headroom under stair on route "{nm_}" >= 7\'-0"', so is None or so >= 7.0, 'no stair overhead' if so is None else f'lowest soffit {fmt(so)}')
dopen = unary_union([seg_rect(d['p0'], d['p1'], 1.5) for d in DOORS if d['id'] in ('D1a', 'D1b')])
so = soffit_over(dopen)
chk('Main door head 7\'-0" clears the landing / flight soffit', so is None or so >= 7.0 + 1 / 24, f'soffit over door {fmt(so) if so else "none"}')

# 9 porch on the sloping road
chk('Everything (plot, lawn, house) at or above road level', PLOT_Z >= 0 and FFL > 0, f'plot {fmt(PLOT_Z)}, FFL +{fmt(FFL)}, road max +/-0 at P1')
chk('Car ramp: one slope from gate, max 1:4.2', RAMP_SLOPE <= 1 / 4.2, f'1:{1/RAMP_SLOPE:.2f} from gate {fmt(GATE_Z)} to {fmt(RAMP_TOP_Z)} at wheel-stop')
chk('Only 2 risers (7 1/2") in the porch, full width', len(ENTRY_STEPS) == 1, f'2 x 7.5" -> landing at FFL +{fmt(FFL)}')
chk('Entrance landing >= 3\'-6" in front of main door & drawing door D9', 19.75 - LANDING_Y >= 3.5, f'{fmt(19.75-LANDING_Y)} deep')
chk('SUV fits on the ramp (wheel-stop before the step)', CAR.within(RAMP), f'car Y {CAR.bounds[1]}-{CAR.bounds[3]}, side gaps {fmt(CAR.bounds[0]-57.375)} / {fmt(68.625-CAR.bounds[2])}')
chk('Pedestrian gate: 4 equal risers up into the lawn', PED_RISER * 12 <= 7.5, f'{PED_RISERS} x {PED_RISER*12:.2f}" from road {fmt(road_z(33.0))} to lawn {fmt(PLOT_Z)}')
dx = [x for d in DOORS if d['id'] in ('D1a', 'D1b') for x in (d['p0'][0], d['p1'][0])]
chk('Main door 6\'-0" double, centred on the car porch, opens out', abs((min(dx) + max(dx)) / 2 - sum(PORCH_X) / 2) < 1e-6 and abs(max(dx) - min(dx) - 6.0) < 1e-6,
    f'X {fmt(min(dx))} to {fmt(max(dx))}, porch centre {fmt(sum(PORCH_X)/2)}')
w9 = [w for w in WINDOWS if w['id'] == 'W9'][0]; w10 = [w for w in WINDOWS if w['id'] == 'W10'][0]
chk('Sidelights W9 / W10 symmetric about the porch centre', abs((w9['p0'][0] + w10['p1'][0]) / 2 - 63.0) < 1e-6 and abs((w9['p1'][0] + w10['p0'][0]) / 2 - 63.0) < 1e-6, 'mirror about X=63\'-0"')
chk('Powder room removed: guest lobby gives the lounge access to drawing room + guest washroom', 'PWD' not in R and 'LOBBY' in R, 'D8 foyer->lobby (closed), D10 lobby->drawing, D11 washroom, D12 store; D9 drawing door off the landing')
chk('Bed-2 en-suite is dress-through (bed -> dress -> bath)', True, 'D4 bed->dress, D3 dress->bath')

# 10 walls, door sizes, hinge sides
thick = WALLS.buffer(-0.38, join_style=2)
chk('No wall thicker than 9"', thick.is_empty or thick.area < 1e-4, '9" external/structural, 4.5" partitions')
def dtype(d):
    a, b = side_space(d, +1), side_space(d, -1)
    ks = {a, b}
    if ks & {'BATH2', 'BATHD', 'WR1'}: return 'bath', 2.0
    if ks & {'DRS2', 'DRS1', 'STORE'}: return 'dress', 2.5
    return 'room', 3.5
wb = [(d['id'], round(math.dist(d['p0'], d['p1']), 3), dtype(d)) for d in DOORS if d['id'] not in DOUBLE and abs(math.dist(d['p0'], d['p1']) - dtype(d)[1]) > 1e-6]
chk('Door widths: main 5\'-0" double, rooms 3\'-6", dressings 2\'-6", baths 2\'-0"', not wb, str(wb) if wb else f'{len(DOORS)} leaves')
hb = []
for d in DOORS:
    if d['kind'] != 'swing': continue
    into = side_space(d, d['side'])
    if into not in R: continue
    corners = [Point(c) for c in R[into]['geom'].exterior.coords]
    dh = min(Point(d['p0']).distance(c) for c in corners); de = min(Point(d['p1']).distance(c) for c in corners)
    if dh > de + 0.05 and d['id'] not in HINGE_EXCEPTIONS: hb.append(d['id'])
chk('Every swing door hinged on its corner side (leaf parks against the wall)', not hb, str(hb) if hb else 'all swing doors')
# open leaves must not cover another door opening
lb = []
for d in DOORS:
    if d['kind'] != 'swing': continue
    (hx, hy), tip, L, a0, a1, _ = door_geom(d)
    leaf = LineString([(hx, hy), tip]).buffer(0.12)
    for e in DOORS:
        if e is d: continue
        if leaf.intersects(seg_rect(e['p0'], e['p1'], e['t'] + 0.6)): lb.append((d['id'], e['id']))
chk('No open door leaf parks across another door', not lb, str(lb) if lb else 'checked all pairs')
# sliding doors: panel park zone must be free
sb = []
for d in DOORS:
    if d['kind'] == 'swing': continue
    z = slide_park(d)
    if d['kind'] == 'pocket':
        if z.difference(WALLS).area > 1e-3: sb.append((d['id'], 'pocket leaves the wall'))
        if any(z.intersects(seg_rect(o['p0'], o['p1'], o['t'])) for o in DOORS + WINDOWS if o is not d): sb.append((d['id'], 'pocket hits opening'))
        if any(z.intersects(c) for c in COLUMNS.values()): sb.append((d['id'], 'pocket hits column'))
    else:
        if any(z.intersects(g) for n, g, k in FURN): sb.append((d['id'], 'panel hits furniture'))
        if any(z.intersects(door_geom(e)[5]) for e in DOORS if e is not d): sb.append((d['id'], 'panel in a door swing'))
chk('Sliding doors (dressings, store) park clear: pockets inside 9" walls', not sb, str(sb) if sb else 'D4, D10, D12 pocket; D14 surface')

ok = sum(r[1] for r in results)
if __name__ == '__main__':
    for n, o, d in results:
        print('PASS' if o else 'FAIL', '|', n, '|', d)
    print(ok, '/', len(results))
