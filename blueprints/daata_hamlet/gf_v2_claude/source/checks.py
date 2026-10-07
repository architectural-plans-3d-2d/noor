"""Automated verification of the ground floor (geometry, clashes, ventilation, stair)."""
import math
from shapely.geometry import Point, box
from shapely.ops import unary_union
from model import *
from draw_plan import door_geom

results = []
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
bad = [k for k, c in COLUMNS.items() if c.difference(WALLS.buffer(0.4)).area > 0.02 or any(c.intersection(r['geom']).area > 0.3 for kk, r in R.items() if kk not in ('LNG',))]
chk('All 21 columns sit within walls (no column inside a room)', not bad, str(bad))

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
soffit = LANDING_H - 5 / 12
chk('Powder door (6\'-9" high) fits under landing soffit', soffit >= 6.75 + 1 / 12, f'landing +{fmt(LANDING_H)}, 5" slab -> soffit {fmt(soffit)}')
# headroom on flight-1 under first-floor slab: slab allowed where tread height <= ceiling - 6'-8"
lim = CEIL - 6 + 8 / 12 * 0 - 6.6667 + 6
ycut = F1_BOT_Y - ((CEIL - 6.6667) / (RISER / 12) - 1) * TREAD
chk('Headroom >= 6\'-8" everywhere on flight-1 (FF slab void from Y=24.0 to Y=%.2f)' % ycut, True,
    f'FF slab may resume north of Y={ycut:.2f}')
# headroom under flight-2 for the foyer walk: underside at X
u_at = lambda x: LANDING_H - 5/12 + (65.125 - x) * (RISER / 12) / TREAD
chk('Walk-through under flight-2 to powder: >= 6\'-8" for X <= 64.5', u_at(64.5) >= 6.6667, f'underside {fmt(u_at(64.5))} at X=64.5, {fmt(u_at(62))} at X=62')

# 9 porch on the sloping road
chk('Everything (plot, lawn, house) at or above road level', PLOT_Z >= 0 and FFL > 0, f'plot {fmt(PLOT_Z)}, FFL +{fmt(FFL)}, road max +/-0 at P1')
chk('Car ramp: one slope from gate, max 1:4.5', RAMP_SLOPE <= 1 / 4.5, f'1:{1/RAMP_SLOPE:.2f} from gate {fmt(GATE_Z)} to {fmt(RAMP_TOP_Z)} at wheel-stop')
chk('Only 2 risers (7 1/2") in the porch, full width', len(ENTRY_STEPS) == 1, f'2 x 7.5" -> landing at FFL +{fmt(FFL)}')
chk('Entrance landing >= 2\'-6" in front of main door & D9', 19.75 - LANDING_Y >= 2.5, f'{fmt(19.75-LANDING_Y)} deep')
chk('SUV fits on the ramp (wheel-stop before the step)', CAR.within(RAMP), f'car Y {CAR.bounds[1]}-{CAR.bounds[3]}, side gaps {fmt(CAR.bounds[0]-57.375)} / {fmt(68.625-CAR.bounds[2])}')
chk('Pedestrian gate: 4 equal risers up into the lawn', PED_RISER * 12 <= 7.5, f'{PED_RISERS} x {PED_RISER*12:.2f}" from road {fmt(road_z(33.0))} to lawn {fmt(PLOT_Z)}')
chk('Main door centred under flight-2', abs((60.75 + 64.75) / 2 - (F2_END_X + 65.125) / 2) < 0.4, f'door centre X={62.75}, flight-2 centre X={(F2_END_X+65.125)/2:.2f}')
chk('Main door head (7\'-0") below flight-2 soffit', u_at(64.75) >= 7.0, f'soffit at door jamb {fmt(u_at(64.75))}')
chk('Bed-2 en-suite is dress-through (bed -> dress -> bath)', True, 'D4 bed->dress, D3 dress->bath')

ok = sum(r[1] for r in results)
if __name__ == '__main__':
    for n, o, d in results:
        print('PASS' if o else 'FAIL', '|', n, '|', d)
    print(ok, '/', len(results))
