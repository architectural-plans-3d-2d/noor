"""
DAATA HAMLET RESIDENCE - GROUND FLOOR (REV-03)
Single source of truth. Units: decimal feet. Origin = survey peg P1 (SW road corner).
+X = East, +Y = North.  Walls: 9" (0.75') external / structural, 4.5" (0.375') partitions.
FFL GF = 0'-0" (+1'-6" above road).  Floor-to-floor = 11'-0".  Slab 6".
"""
import math
from shapely.geometry import Polygon, box, LineString, Point
from shapely.ops import unary_union

# ---------------------------------------------------------------- survey
PEGS = [('P1', 0.0, 0.0), ('P2', 10.4884, 10.0122), ('P3', 24.5949, 26.1267),
        ('P4', 41.1897, 36.8354), ('P5', 67.6992, 50.7010), ('P6', 84.8373, 57.6678),
        ('P7', 88.8145, 62.1602), ('P0', 87.9167, 0.0)]
PLOT = Polygon([(x, y) for _, x, y in PEGS])
INNER9 = PLOT.buffer(-0.75, join_style=2)      # inner face of 9" walls built on boundary

def north_y(x):
    """Y of the north boundary at a given X (P3..P6)."""
    pts = [(x_, y_) for _, x_, y_ in PEGS[2:6]]
    for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
        if x0 <= x <= x1:
            return y0 + (x - x0) * (y1 - y0) / (x1 - x0)
    raise ValueError(x)

# ---------------------------------------------------------------- planning lines
LINE_B = 36.125          # outer face of west wall (zero encroachment line)
FRONT = 3.0              # outer face of front wall (3'-0" setback)
EAST_FACE = 85.125       # outer face of east wall  -> 2'-9 1/2" passage at road
FF_TO_FF = 11.0
SLAB = 0.5
CEIL = FF_TO_FF - SLAB   # 10'-6" clear

GRID_X = {'B': 36.5, 'C': 51.0, "C'": 57.0, 'D': 69.0, 'E': 84.75}
GRID_Y = {'1': 3.375, '2': 20.125, '3': 28.5, '4': 33.1875, '5': 44.0625}

FOOTPRINT = (box(LINE_B, FRONT, EAST_FACE, 80) & PLOT)

# ---------------------------------------------------------------- levels (datum +/-0 = road at P1 = levelled plot)
ROAD_FALL = 6.0                                   # road falls 6'-0" from P1 (X=0) to P0 (X=87'-11")
def road_z(x): return -ROAD_FALL * x / 87.9167
PLOT_Z = 0.0                                      # plot (incl. lawn) filled level with the road at P1 - never below road
FFL = PLOT_Z + 0.5                                # GF finished floor +0'-6" (reduced plinth, per client)
# car porch: one ramp from the gate, then 2 full-width risers to a 2'-6" entrance landing (no other steps)
PORCH_X = (57.375, 68.625)
RAMP_END_Y = 15.25                                # top of ramp (wheel-stop line)
TREAD_Y = (15.25, 16.25)                          # one 1'-0" full-width tread
LANDING_Y = 16.25                                 # landing 3'-6" deep (Y 16.25 - 19.75) at FFL
PORCH_RISER = 7.5 / 12
GATE_Z = road_z(sum(PORCH_X) / 2)                 # -4'-3 1/2" at gate centre
RAMP_TOP_Z = FFL - 2 * PORCH_RISER                # -0'-9"
RAMP_SLOPE = (RAMP_TOP_Z - GATE_Z) / RAMP_END_Y   # ~1:4.3
PLATFORM = box(57.375, LANDING_Y, 68.625, 19.75)  # entrance landing
PORCH_TREAD = box(57.375, TREAD_Y[0], 68.625, TREAD_Y[1])
RAMP = box(57.375, 0.0, 68.625, RAMP_END_Y)
def ramp_z(y): return GATE_Z + min(max(y, 0), RAMP_END_Y) * RAMP_SLOPE
ENTRY_STEPS = [(PORCH_TREAD, RAMP_TOP_Z + PORCH_RISER)]
# pedestrian gate in the lawn front near the house; 4 steps up inside the gate, stone path to side door D5
PED_GATE = (31.25, 34.75)                         # 3'-6" gate
PED_RISERS = 4
PED_RISER = (PLOT_Z - road_z(sum(PED_GATE) / 2)) / PED_RISERS
PED_STEPS = [(box(31.25, 0.375 + k * 10 / 12, 34.75, 0.375 + (k + 1) * 10 / 12), road_z(33.0) + (k + 1) * PED_RISER) for k in range(PED_RISERS - 1)]
# stepping stones (no paved path) from the pedestrian gate steps to side door D5
STONES = [box(32.25, y, 33.75, y + 1.0) for y in (3.4, 5.4, 7.4, 9.4, 11.4, 13.4, 15.4, 17.4, 19.4)] + \
         [box(34.25, 21.6, 35.75, 23.1)]

# ---------------------------------------------------------------- spaces (clear interior)
OTS_IN = PLOT.buffer(-4.5, join_style=2)        # lounge inner face (OTS 3'-0" clear + 2 x 9" walls)
OTS_OUT = PLOT.buffer(-3.75, join_style=2)

R = {}
def room(key, name, geom, kind='room', finish='tile'):
    R[key] = dict(key=key, name=name, geom=geom, kind=kind, finish=finish)

room('BED2', 'BED ROOM-2', box(36.875, 3.75, 50.625, 19.75), finish='wood')
room('BATH2', 'BATH (BED-2)', box(51.375, 3.75, 56.625, 10.75), kind='wet')
room('DRS2', 'DRESS (BED-2)', box(51.375, 11.125, 56.625, 19.75))
room('PASS', 'PASSAGE 4\'-0" WIDE', box(36.875, 20.5, 51.375, 24.5), kind='circ')
room('KIT', 'KITCHEN', box(36.875, 24.875, 50.625, 33.0), kind='wet')
room('DKIT', 'DIRTY KITCHEN', box(36.875, 33.375, 50.625, 80) & INNER9, kind='wet')
room('LNG', 'FAMILY LOUNGE + DINING', (box(51.375, 20.5, 68.625, 80) & OTS_IN) - box(64.75, 20.5, 68.625, 24.375))
room('OTS', 'OTS (OPEN TO SKY)', (box(51.375, 20, 68.625, 80) & INNER9) - OTS_OUT, kind='open')
room('PWD', 'POWDER', unary_union([box(65.125, 20.5, 72.375, 24.0),
                                   box(69.375, 24.0, 72.375, 28.125)]), kind='wet')
room('DRSD', 'DRESS (DRAWING)', box(72.75, 20.5, 78.0, 28.125))
room('BATHD', 'BATH (DRAWING)', box(78.375, 20.5, 84.375, 28.125), kind='wet')
room('DRAW', 'DRAWING ROOM', box(69.375, 3.75, 84.375, 19.75), finish='wood')
room('BED1', 'BED-1', box(69.375, 28.875, 84.375, 43.875), finish='wood')
room('DRS1', 'DRESSING (BED-1)', box(69.375, 44.25, 76.5, 80) & INNER9)
room('WR1', 'WASHROOM (BED-1)', box(76.875, 44.25, 84.375, 80) & INNER9, kind='wet')
room('PORCH', 'CAR PORCH', box(57.375, 0.0, 68.625, 19.75), kind='open', finish='paver')

# ---------------------------------------------------------------- walls = footprint - spaces
SPACES = unary_union([r['geom'] for r in R.values()])
WALLS = FOOTPRINT - SPACES
# the porch & veranda are open to the road: cut the front strip in front of them
WALLS = WALLS - box(57.375, 0, 68.625, 19.75)
# keep only real wall pieces (drop slivers)
WALLS = unary_union([g for g in getattr(WALLS, 'geoms', [WALLS]) if g.area > 0.05])

# ---------------------------------------------------------------- stair (L-type, 19 risers)
N_RISERS = 19
RISER = FF_TO_FF * 12 / N_RISERS          # 6.947"
TREAD = 10 / 12                           # 10"
F1_RISERS, F2_RISERS = 13, 6              # landing at 13R = 7'-6.3"
LANDING_H = F1_RISERS * RISER / 12
STAIR_W = 3.5
F1_X = (65.125, 68.625)
LANDING = box(65.125, 20.5, 68.625, 24.0)
F1_TOP_Y = 24.0
F1_BOT_Y = F1_TOP_Y + (F1_RISERS - 1) * TREAD     # 34.0
F2_Y = (20.5, 24.0)
F2_END_X = 65.125 - (F2_RISERS - 1) * TREAD        # 60.958 -> arrive FF

STAIR_TREADS = []   # (polygon, top-of-tread height ft, flight)
for i in range(F1_RISERS - 1):          # 12 treads, i=0 is first (lowest) tread at north end
    y1 = F1_BOT_Y - i * TREAD
    STAIR_TREADS.append((box(F1_X[0], y1 - TREAD, F1_X[1], y1), (i + 1) * RISER / 12, 1))
STAIR_TREADS.append((LANDING, LANDING_H, 0))
for j in range(F2_RISERS - 1):          # 5 treads going west
    x1 = 65.125 - j * TREAD
    STAIR_TREADS.append((box(x1 - TREAD, F2_Y[0], x1, F2_Y[1]), (F1_RISERS + j + 1) * RISER / 12, 2))
STAIR_FOOT = unary_union([t[0] for t in STAIR_TREADS])
FLIGHT1_FOOT = unary_union([t[0] for t in STAIR_TREADS if t[2] == 1])   # the only part standing on the lounge floor

# ---------------------------------------------------------------- columns 9"x18"
def col(x, y, along='x', w=0.75, l=1.5):
    return box(x - l/2, y - w/2, x + l/2, y + w/2) if along == 'x' else box(x - w/2, y - l/2, x + w/2, y + l/2)

def _fit(poly, axis_vec):
    """slide a column along its long axis (<= 9") until it sits fully inside the walls"""
    from shapely import affinity
    best = None
    for k in range(0, 13):
        for sgn in (1, -1):
            d = k * 0.0625 * sgn
            q = affinity.translate(poly, axis_vec[0] * d, axis_vec[1] * d)
            out = q.difference(WALLS).area
            if best is None or out < best[0] - 1e-9 or (abs(out - best[0]) < 1e-9 and abs(d) < abs(best[1])):
                best = (out, d, q)
        if best[0] < 1e-6: break
    return best[2]

def gcol(x, y, along):
    return _fit(col(x, y, along), (1, 0) if along == 'x' else (0, 1))

def ocol(cx, cy, ux, uy):
    """9" x 18" column centred at (cx,cy), 18" along unit vector (ux,uy) - for slanted walls"""
    nx, ny = -uy, ux
    pts = [(cx + ux * .75 * a + nx * .375 * b, cy + uy * .75 * a + ny * .375 * b) for a, b in ((-1, -1), (1, -1), (1, 1), (-1, 1))]
    return _fit(Polygon(pts), (ux, uy))

def _seg_dir(x):
    pts = [(x_, y_) for _, x_, y_ in PEGS[2:6]]
    for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
        if x0 <= x <= x1:
            L_ = math.hypot(x1 - x0, y1 - y0); return (x1 - x0) / L_, (y1 - y0) / L_
def _on_offset(x, off):
    ring = PLOT.buffer(-off, join_style=2).exterior
    p = ring.intersection(LineString([(x, 25), (x, 70)]))
    p = max(getattr(p, 'geoms', [p]), key=lambda q: q.y)
    return p.x, p.y

# Structural grid: columns only at grid-line intersections (and the P4 bend), never off-grid.
GX, GY = GRID_X, GRID_Y
COLUMNS = {}
for r in ('1', '2'):
    for c in ('B', 'C', "C'", 'D', 'E'):
        along = 'y' if (r == '1' and c in ("C'", 'D')) else 'x'
        COLUMNS[f'{c}{r}'] = gcol(GX[c], GY[r], along)
for c in ('D', 'E'):
    COLUMNS[f'{c}3'] = gcol(GX[c], GY['3'], 'x')
    COLUMNS[f'{c}5'] = gcol(GX[c], GY['5'], 'y')
for c in ('B', 'C'):
    COLUMNS[f'{c}4'] = gcol(GX[c], GY['4'], 'y')
# grid lines meeting the north boundary wall (centre line 4.5" in from the boundary)
for c in ('C', "C'", 'D', 'E'):
    cx, cy = _on_offset(GX[c], 0.375); ux, uy = _seg_dir(GX[c])
    COLUMNS[f'{c}N'] = ocol(cx, cy, ux, uy)
# grid C' meeting the lounge / OTS wall (mid-support of the 18'-7" slanted wall)
cx, cy = _on_offset(GX["C'"], 4.125); ux, uy = _seg_dir(GX["C'"])
COLUMNS["C'L"] = ocol(cx, cy, ux, uy)
# bend of the boundary at peg P4 (L-shaped corner column inside the 9" walls)
BWALL = PLOT - INNER9
COLUMNS['P4'] = BWALL & box(41.19 - 0.9, 36.84 - 0.9, 41.19 + 0.9, 36.84 + 0.9)

# ---------------------------------------------------------------- openings
# Each opening: centreline points p0->p1 on the wall, wall thickness t.
def seg_rect(p0, p1, t):
    (x0, y0), (x1, y1) = p0, p1
    L = math.hypot(x1 - x0, y1 - y0); nx, ny = -(y1 - y0) / L, (x1 - x0) / L
    h = t / 2 + 0.02
    return Polygon([(x0 + nx*h, y0 + ny*h), (x1 + nx*h, y1 + ny*h), (x1 - nx*h, y1 - ny*h), (x0 - nx*h, y0 - ny*h)])

def on_lounge_wall(x):
    """point on lounge north wall centreline at given X"""
    # wall centreline = offset 4.125 from boundary
    c = PLOT.buffer(-4.125, join_style=2).exterior
    l = LineString([(x, 30), (x, 60)])
    p = c.intersection(l)
    p = max(getattr(p, 'geoms', [p]), key=lambda q: q.y)
    return (p.x, p.y)

DOORS = []      # dict(id, p0 hinge, p1, t, side(+1 left of p0->p1 / -1 right), kind, h)
WINDOWS = []    # dict(id, p0, p1, t, sill, head, kind)

def door(i, hinge, end, t, side, kind='swing', h=7.0, park=+1):
    """swing: p0 = hinge, side = swing side.  pocket/slide: p0-p1 = opening, park = +1 slides beyond p1 / -1 beyond p0,
    side = face the surface panel runs on (slide)."""
    DOORS.append(dict(id=i, p0=hinge, p1=end, t=t, side=side, kind=kind, h=h, park=park))

def slide_park(d):
    """rectangle the sliding panel occupies when the door is open"""
    (x0, y0), (x1, y1) = d['p0'], d['p1']
    L = math.hypot(x1 - x0, y1 - y0); ux, uy = (x1 - x0) / L, (y1 - y0) / L
    a, b = ((x1, y1), (x1 + ux * L, y1 + uy * L)) if d['park'] > 0 else ((x0 - ux * L, y0 - uy * L), (x0, y0))
    if d['kind'] == 'pocket':
        return seg_rect(a, b, 0.2)
    nx, ny = -uy * d['side'], ux * d['side']
    off = d['t'] / 2 + 0.12
    return seg_rect((a[0] + nx * off, a[1] + ny * off), (b[0] + nx * off, b[1] + ny * off), 0.16)

def win(i, p0, p1, t, sill, head, kind='window'):
    WINDOWS.append(dict(id=i, p0=p0, p1=p1, t=t, sill=sill, head=head, kind=kind))

E, P = 0.75, 0.375
# Door widths: 3'-6" all rooms, 2'-6" dressing rooms, 2'-0" baths/powder. Hinges on the corner side.
# --- main entrance: 5'-0" double door (2 x 2'-6"), opens OUT onto the 3'-6" landing so neither leaf can cover the powder door
door('D1a', (59.625, 20.125), (62.125, 20.125), E, -1)                 # left leaf
door('D1b', (64.625, 20.125), (62.125, 20.125), E, +1)                 # right leaf
win('W9', (57.875, 20.125), (59.375, 20.125), E, 1.0, 7.0)             # glazed sidelight beside the main door
# --- Bed-2 suite
door('D2', (50.5, 20.125), (47.0, 20.125), E, +1)                      # passage -> bed2 (3'-6")
door('D4', (51.0, 11.75), (51.0, 14.25), E, -1, 'pocket', park=+1)    # bed2 -> dress2 (2'-6" pocket sliding)
door('D3', (51.5, 10.9375), (53.5, 10.9375), P, -1)                    # dress2 -> bath2 (2'-0")
win('SL1', (36.5, 4.75), (36.5, 12.75), E, 0.0, 7.0, 'sliding')       # 8'-0" sliding glass to lawn
win('W1', (40.25, 3.375), (47.25, 3.375), E, 2.5, 7.0)                 # south window bed2 (centred)
win('V1', (53.0, 3.375), (55.0, 3.375), E, 6.0, 7.0, 'vent')           # bath2 vent to front (centred)
# --- passage / kitchen
door('D5', (36.5, 20.75), (36.5, 24.25), E, -1)                        # lawn -> passage (3'-6", swings IN)
door('D6', (50.5, 24.6875), (47.0, 24.6875), P, -1)                    # passage -> kitchen (3'-6")
door('D7', (50.5, 33.1875), (47.0, 33.1875), P, -1)                    # kitchen -> dirty kitchen (3'-6")
win('W2', (36.5, 26.0), (36.5, 31.0), E, 3.5, 7.0)                     # kitchen west window over sink
win('V2', (51.0, 38.6), (51.0, 40.1), E, 5.0, 6.5, 'vent')           # dirty kitchen vent into OTS
# --- powder (2'-0")
door('D8', (64.9375, 20.75), (64.9375, 22.75), P, -1, h=6.75)          # lounge -> powder
win('V3', (65.5, 20.125), (68.25, 20.125), E, 5.75, 6.75, 'vent')      # powder vent into car porch
# --- drawing
door('D9', (69.0, 19.75), (69.0, 16.25), E, +1)                        # entrance landing -> drawing (3'-6")
door('D10', (73.25, 20.125), (75.75, 20.125), E, +1, 'pocket', park=-1)  # drawing -> dress (2'-6" pocket sliding)
door('D11', (78.1875, 20.75), (78.1875, 22.75), P, -1)                 # dress -> bath (2'-0")
win('W3', (73.375, 3.375), (80.375, 3.375), E, 2.5, 7.0)               # south window drawing
win('W4', (84.75, 8.5), (84.75, 13.5), E, 3.0, 7.0)                    # east window drawing
win('V4', (84.75, 23.0), (84.75, 25.0), E, 6.0, 7.0, 'vent')           # bath(drawing) vent
# --- Bed-1 suite
door('D12', (69.0, 43.5), (69.0, 40.0), E, -1)                         # lounge -> bed1 (3'-6")
door('D13', (69.625, 44.0625), (72.125, 44.0625), P, -1, 'slide', park=+1)  # bed1 -> dressing (2'-6" sliding, bed-1 face)
door('D14', (76.6875, 47.5), (76.6875, 49.5), P, +1)                   # dressing -> washroom (2'-0")
win('W5', (84.75, 32.5), (84.75, 38.0), E, 3.0, 7.0)                   # bed1 east window
win('W6', (84.75, 47.5), (84.75, 50.5), E, 5.0, 7.0, 'vent')           # washroom vent/window
# --- lounge glazing to OTS (on slanted wall)
win('W7', on_lounge_wall(54.0), on_lounge_wall(58.0), E, 3.0, 7.0)
win('W8', on_lounge_wall(61.0), on_lounge_wall(64.0), E, 3.0, 7.0)

# ---------------------------------------------------------------- fixtures & furniture
# (name, polygon, kind)  kind: fixture | furniture | counter
FURN = []
def f(name, x0, y0, x1, y1, kind='furniture'):
    FURN.append((name, box(x0, y0, x1, y1), kind))

# Bed-2
f('KING BED 6x6\'6"', 39.375, 13.25, 45.375, 19.75)
f('SIDE', 37.875, 18.25, 39.375, 19.75); f('SIDE', 45.375, 18.25, 46.875, 19.75)
f('STUDY', 36.875, 11.75, 38.875, 15.25)
# Bath-2
f('SHOWER', 51.375, 3.75, 56.625, 6.75, 'fixture')
f('WC', 54.375, 7.25, 56.625, 8.5, 'fixture')
f('BASIN', 55.125, 9.0, 56.625, 10.75, 'fixture')
# Dress-2
f('WARDROBE', 54.625, 11.125, 56.625, 19.75)
# Kitchen
f('COUNTER', 36.875, 24.875, 38.875, 31.0, 'counter')
f('COUNTER', 36.875, 31.0, 44.5, 33.0, 'counter')
f('COUNTER (U)', 38.875, 24.875, 46.5, 26.875, 'counter')
f('FRIDGE', 44.5, 31.0, 46.5, 33.0, 'fixture')
# Dirty kitchen
f('COUNTER + SINK', 40.75, 33.375, 46.5, 35.375, 'counter')
# Lounge
f('DINING 6-SEAT', 55.5, 25.0, 58.5, 30.5)
f('CHAIRS', 54.25, 25.5, 55.5, 30.0); f('CHAIRS', 58.5, 25.5, 59.75, 30.0)
f('TV UNIT', 52.125, 32.0, 53.5, 36.5)
f('SOFA 3-SEAT', 59.0, 31.5, 62.0, 38.0)
f('COFFEE TBL', 55.5, 33.0, 57.5, 36.5)
# Powder
f('WC', 70.25, 25.875, 71.5, 28.125, 'fixture')
f('BASIN', 70.875, 21.25, 72.375, 23.0, 'fixture')
# Drawing
f('SOFA 3-SEAT', 76.5, 16.75, 83.5, 19.75)
f('SOFA 2-SEAT', 81.375, 7.5, 84.375, 12.5)
f('ARMCHAIR', 73.0, 9.0, 75.75, 11.75); f('ARMCHAIR', 73.0, 12.5, 75.75, 15.25)
f('CENTRE TBL', 77.0, 10.0, 80.0, 14.0)
# Dress (drawing)
f('WARDROBE', 72.75, 26.125, 78.0, 28.125)
# Bath (drawing)
f('BASIN', 82.375, 20.5, 84.375, 22.0, 'fixture')
f('WC', 82.125, 22.75, 84.375, 24.0, 'fixture')
f('SHOWER', 78.375, 25.5, 84.375, 28.125, 'fixture')
# Bed-1
f('KING BED 6x6\'6"', 74.375, 28.875, 80.375, 35.375)
f('SIDE', 72.875, 28.875, 74.375, 30.375); f('SIDE', 80.375, 28.875, 81.875, 30.375)
f('TV UNIT', 75.0, 42.375, 81.0, 43.875)
# Dressing-1
f('WARDROBE', 69.375, 47.0, 71.375, 50.4)
f('WARDROBE', 72.875, 44.25, 76.5, 46.25)
# Washroom-1
f('BASIN', 79.5, 44.25, 82.0, 45.75, 'fixture')
f('WC', 82.125, 45.25, 84.375, 46.5, 'fixture')
f('SHOWER', 79.5, 50.5, 84.375, 53.5, 'fixture')
# Car
CAR = box(59.5, 0.125, 65.5, 15.125)   # car up to 15'-0" long x 6'-0" wide; wheel-stop at Y 15.125 #  # 6'-3" x 15'-9" (Fortuner class), wheel-stop 6" short of platform

# ---------------------------------------------------------------- circulation corridors that must stay clear (min 3'-0")
CORRIDORS = {
    'Main door -> lounge': box(59.7, 20.5, 64.6, 23.5),
    'Entrance landing 3\'-6" deep': box(57.4, 16.3, 68.6, 19.7),
    'Driver side walk-up on ramp': box(65.6, 7.5, 68.6, 15.2),
    'Passage to lounge': box(51.375, 20.5, 54.0, 24.5),
    'Lounge -> powder door': box(60.0, 21.0, 64.9, 23.5),
    'Foyer -> stair foot': box(62.0, 24.5, 65.0, 31.0),
    'Stair landing zone (3\' at foot)': box(65.125, 34.0, 68.625, 37.0),
    'Lounge -> Bed-1 door': box(62.5, 37.0, 68.625, 41.0),
    'Kitchen work aisle (4\'-1")': box(38.9, 26.9, 46.5, 30.95),
    'Dress -> bath (drawing)': box(75.5, 22.5, 78.0, 25.5),
    'Bed-1 -> dressing': box(69.5, 40.75, 72.75, 43.875),
}

def fmt(ft):
    """decimal ft -> 12'-6 1/2\" """
    neg = ft < 0; ft = abs(ft)
    tot = round(ft * 24) / 2      # half inches
    f_ = int(tot // 12); inch = tot - f_ * 12
    whole = int(inch); half = inch - whole > 0
    s = f"{f_}'-{whole}{' 1/2' if half else ''}\""
    return ('-' if neg else '') + s
