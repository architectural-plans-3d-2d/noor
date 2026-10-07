"""Two A3 PDF sets:
  1) DH-GF-REV03_Drawings.pdf  - dimensioned plan, column/wall layout, south elevation + section
  2) DH-GF-REV03_Details.pdf   - door/window schedule with type elevations, stair & entrance details,
                                  OTS detail, room + column schedules
"""
import math
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from matplotlib.patches import Rectangle, Polygon as MPoly, Circle
from model import *
from draw_plan import draw_ground_floor, door_geom, draw_poly, dim_h, dim_v, dim_al
from draw_elev import draw_south_elevation, draw_stair_section, R_
from draw_interiors import elev_looking_south, elev_looking_east
from checks import side_space

INK = '#1b1b1b'; RED = '#c0392b'; BLUE = '#2b6cb0'
W_IN, H_IN = 16.535, 11.693
DATE = '05 OCT 2026'
REV = 'REV-04'
VER = STAIR_VERSION
VNAME = {'L': 'L-TYPE STAIR (OPTION 1)', 'U': 'COMPACT U-STAIR (OPTION 2)'}[VER]

# ------------------------------------------------------------------ sheet furniture
def frame(fig):
    ax = fig.add_axes([0, 0, 1, 1]); ax.set_xlim(0, W_IN); ax.set_ylim(0, H_IN); ax.axis('off')
    ax.add_patch(Rectangle((.3, .3), W_IN - .6, H_IN - .6, fill=False, lw=1.4))
    ax.add_patch(Rectangle((.4, .4), W_IN - .8, H_IN - .8, fill=False, lw=.4))
    x0 = W_IN - 3.55
    ax.add_patch(Rectangle((x0, .4), 3.15, H_IN - .8, fill=False, lw=.8))
    y = H_IN - .9
    ax.text(x0 + .15, y, 'DAATA HAMLET', fontsize=15, weight='bold'); y -= .3
    ax.text(x0 + .15, y, 'RESIDENCE', fontsize=15, weight='bold'); y -= .3
    ax.text(x0 + .15, y, 'Ground floor  |  Pakistan', fontsize=7, color='#555'); y -= .45
    rows = [('PLOT', '3,129.1 sq ft (290.7 m2)'), ('MARLA', '13.9 @ 225 sf  |  11.5 @ 272.25 sf'),
            ('LEVELS', 'Datum +/-0 = road at P1 (highest)'), ('', 'Plot & lawn +/-0, GF FFL +0\'-6"'),
            ('FLOOR HT', '11\'-0" floor to floor, 10\'-6" clear'), ('UNITS', 'Feet-inches; origin = peg P1'),
            ('REVISION', f'{REV}   {DATE}'), ('OPTION', VNAME)]
    for a, b in rows:
        ax.text(x0 + .15, y, a, fontsize=6.3, color='#666'); ax.text(x0 + 1.0, y, b, fontsize=6.3); y -= .22
    y -= .1
    ax.plot([x0, x0 + 3.15], [y, y], c='k', lw=.5); y -= .3
    return ax, x0, y

def notes(ax, x0, y, lines, fs=6.1):
    for ln in lines:
        bold = ln.isupper() and not ln.startswith(' ')
        ax.text(x0 + .15, y, ln, fontsize=fs, va='top', weight='bold' if bold else 'normal'); y -= .185
    return y

def title_block(ax, x0, title, no, scale):
    ax.add_patch(Rectangle((x0, .4), 3.15, 1.55, fill=False, lw=.8))
    ax.text(x0 + .15, 1.68, 'SHEET TITLE', fontsize=5.5, color='#666')
    ax.text(x0 + .15, 1.42, title, fontsize=9, weight='bold', va='top')
    ax.text(x0 + .15, .85, 'SCALE', fontsize=5.5, color='#666'); ax.text(x0 + .15, .62, scale, fontsize=7, va='center')
    ax.text(x0 + 1.95, .85, 'SHEET NO.', fontsize=5.5, color='#666'); ax.text(x0 + 1.95, .55, no, fontsize=16, weight='bold', color=RED)

def table(ax, x, y, cols, widths, rows, fs=6.2, rh=.2):
    tx = x
    for c, w in zip(cols, widths):
        ax.add_patch(Rectangle((tx, y - rh), w, rh, fc='#1f2937', ec='white', lw=.3))
        ax.text(tx + .05, y - rh / 2, c, fontsize=fs, color='white', va='center', weight='bold'); tx += w
    y -= rh
    for i, r in enumerate(rows):
        tx = x
        bold = str(r[0]).startswith('TOTAL')
        for v, w in zip(r, widths):
            ax.add_patch(Rectangle((tx, y - rh), w, rh, fc='#f3f4f6' if i % 2 else 'white', ec='#d1d5db', lw=.3))
            ax.text(tx + .05, y - rh / 2, str(v), fontsize=fs, va='center', weight='bold' if bold else 'normal'); tx += w
        y -= rh
    return y

def clip_all(ax):
    for t in ax.texts + ax.lines + ax.patches:
        t.set_clip_on(True); t.set_clip_path(ax.patch)

def scaled_axes(fig, x_in, y_in, xlim, ylim, ft_per_in):
    w = (xlim[1] - xlim[0]) / ft_per_in; h = (ylim[1] - ylim[0]) / ft_per_in
    ax = fig.add_axes([x_in / W_IN, y_in / H_IN, w / W_IN, h / H_IN])
    ax.set_xlim(*xlim); ax.set_ylim(*ylim); ax.set_aspect('equal'); ax.axis('off')
    return ax

GEN = ['GENERAL NOTES',
       '1. Dimensions in feet-inches; follow written',
       '   dimensions, do not scale the drawing.',
       '2. Walls: 9" external & structural, 4.5" partitions.',
       '   No wall thicker than 9".',
       f'3. RCC columns 9" x 18" ({len(COLUMNS)} nos), always',
       '   inside the 9" wall line. Sizes, steel & footings',
       '   by structural engineer.',
       '4. No construction west of Line B (X=36\'-1 1/2").',
       '5. Front setback 3\'-0". East service passage',
       '   2\'-9 1/2" at road, 3\'-7" at rear.',
       '6. All baths & kitchens vent directly to',
       '   open air (road side, porch, OTS or passage).',
       '7. Doors: main 6\'-0" double, rooms 3\'-6",',
       '   dressings 2\'-6" sliding, baths 2\'-0". Swing',
       '   leaves hinge on the corner side.',
       '8. Setbacks & coverage to be verified against the',
       '   approving authority bylaws before submission.']

# ------------------------------------------------------------------ DRAWINGS SET
def a101(pdf):
    fig = plt.figure(figsize=(W_IN, H_IN)); ax0, x0, y = frame(fig)
    y = notes(ax0, x0, y, GEN); y -= .15
    notes(ax0, x0, y, ['LEGEND',
                       '   black = RCC column 9"x18",  grey = wall',
                       '   blue triple line = window, double = vent',
                       '   dashed treads = stair above 4\'-0" cut',
                       '   D / W / V / SL = door, window, vent, slider',
                       '   (sizes on details sheet D-101)'])
    title_block(ax0, x0, 'GROUND FLOOR PLAN\n(DIMENSIONED, FURNISHED)', 'A-101', '1/8" = 1\'-0"  (1:96)')
    ax = fig.add_axes([.45 / W_IN, .6 / H_IN, 12.5 / W_IN, 9.75 / H_IN]); draw_ground_floor(ax)
    pdf.savefig(fig); plt.close(fig)

def draw_structure(ax):
    ax.set_aspect('equal'); ax.axis('off')
    ax.add_patch(MPoly(list(PLOT.exterior.coords), closed=True, fc='none', ec=RED, lw=1.0))
    draw_poly(ax, WALLS, fc='#d1d5db', ec='#6b7280', lw=.3, zorder=2)
    for k, x in GRID_X.items():
        ax.plot([x, x], [-3.5, 61.5], c='#9aa5b1', lw=.35, ls=(0, (10, 3, 2, 3)), zorder=1)
        ax.add_patch(Circle((x, 63.4), 1.1, fc='white', ec=INK, lw=.5, zorder=6)); ax.text(x, 63.4, k, ha='center', va='center', fontsize=6, zorder=7)
    for k, yv in GRID_Y.items():
        ax.plot([33, 91], [yv, yv], c='#9aa5b1', lw=.35, ls=(0, (10, 3, 2, 3)), zorder=1)
        ax.add_patch(Circle((93.0, yv), 1.1, fc='white', ec=INK, lw=.5, zorder=6)); ax.text(93.0, yv, k, ha='center', va='center', fontsize=6, zorder=7)
    xs = sorted(GRID_X.values()); ys = sorted(GRID_Y.values())
    for a, b in zip(xs, xs[1:]): dim_h(ax, a, b, 60.0, fs=4.6)
    dim_h(ax, xs[0], xs[-1], 61.6, txt=f'{fmt(xs[-1]-xs[0])} C/C', fs=4.6)
    for a, b in zip(ys, ys[1:]): dim_v(ax, a, b, 90.0, fs=4.6)
    for i, (k, c) in enumerate(COLUMNS.items(), 1):
        draw_poly(ax, c, fc='black', ec='black', lw=.2, zorder=5)
        cx, cy = c.centroid.x, c.centroid.y
        ax.text(cx + .9, cy + .9, f'C{i} ({k})', fontsize=4.2, color=RED, weight='bold', zorder=7)
    ax.text(36, -6.5, f'{len(COLUMNS)} RCC COLUMNS 9"x18", LONG SIDE ALONG THE WALL - NONE PROJECTS BEYOND THE 9" WALL FACE', fontsize=6)
    ax.set_xlim(30, 96); ax.set_ylim(-8, 66)

def a102(pdf):
    fig = plt.figure(figsize=(W_IN, H_IN)); ax0, x0, y = frame(fig)
    notes(ax0, x0, y, ['STRUCTURE NOTES',
                       '1. Grid lines are wall centre lines; columns',
                       '   stand ONLY on grid intersections (plus the',
                       '   P4 bend of the boundary).',
                       '2. Every building corner and every junction',
                       '   of 9" structural walls has a column;',
                       '   4.5" partitions carry no columns.',
                       '3. Max beam span about 16\'-0" (D-E bay 15\'-9").',
                       '4. Columns 9" x 18" sit fully inside the 9"',
                       '   walls - nothing projects into rooms/facade.',
                       '5. Columns continue to roof (3 storeys).',
                       '6. Footings, reinforcement, beam depths and',
                       '   slabs by structural engineer.',
                       '7. Plot is filled up to 6\'-0" on the east:',
                       '   footings to bear on natural ground, not',
                       '   on fill; retaining wall designed by engineer.'])
    title_block(ax0, x0, 'COLUMN & WALL\nLAYOUT', 'A-102', '1/8" = 1\'-0"  (1:96)')
    ax = scaled_axes(fig, 1.6, .6, (30, 96), (-8, 66), 8)
    draw_structure(ax)
    pdf.savefig(fig); plt.close(fig)

def a103(pdf):
    fig = plt.figure(figsize=(W_IN, H_IN)); ax0, x0, y = frame(fig)
    notes(ax0, x0, y, ['FACADE & SITE',
                       '1. Road falls 6\'-0" from P1 to P0. Plot & lawn',
                       '   level with the road at P1; nothing below road.',
                       '2. Stone retaining wall along the front, 0 to',
                       '   6\'-0", with a 3\'-6" MS railing on the plot edge.',
                       '3. Car porch: ramp ~1:4.3 (grooved concrete)',
                       '   from the gate to a wheel-stop, 2 risers of',
                       '   7 1/2", then a 3\'-6" landing at FFL.',
                       '4. Main door 6\'-0" double, centred on the porch,',
                       '   between matching sidelights W9 / W10.',
                       '   Drawing room keeps its own guest door D9 off',
                       '   the landing; from inside, the closed guest',
                       '   lobby (door D8) leads to drawing & washroom.',
                       '5. W1 & W3: 7\'-0" x 4\'-6", centred on rooms,',
                       '   sill 2\'-6", 1\'-6" RCC chajja over.',
                       '6. V1: 2\'-0" x 1\'-0" frosted vent at +6\'-0".',
                       '',
                       f'STAIR (SECTION A-A) - {VNAME}',
                       '1. 3\'-6" wide, 19 risers of 6.95", treads 10".',
                       '2. Flight-1: 13 risers to landing +7\'-6 1/2"',
                       '   (landing sits over the foyer, beside the lobby).',
                       '3. Flight-2: 6 risers, 3\'-5 1/2" to first floor,',
                       '   ' + ('running west over the foyer.' if VER == 'L' else 'returning north beside flight-1.'),
                       '4. Clear height under landing 7\'-1 1/2".'])
    title_block(ax0, x0, 'SOUTH ELEVATION\n+ SECTION A-A', 'A-103', 'ELEV 1/8"=1\'-0"\nSECTION 1/4"=1\'-0"')
    ax = scaled_axes(fig, .45, 6.6, (-4, 98), (-10.5, FFL - PLOT_Z + FF_TO_FF + 6), 8)
    draw_south_elevation(ax)
    ax2 = scaled_axes(fig, 3.5, .7, (16, 40), (-3, FF_TO_FF + 4), 4)
    draw_stair_section(ax2)
    pdf.savefig(fig); plt.close(fig)

# ------------------------------------------------------------------ DETAILS SET
def door_elev(ax, x, y, w, h, tag, kind='door', sill=0.0, label=None):
    """door/window type elevation at (x,y) in feet units of the axes"""
    if kind == 'door':
        R_(ax, x, y, x + w, y + h, fc='#e9dcc9', ec=INK, lw=.9)
        R_(ax, x + .15, y, x + w - .15, y + h - .15, fc='#c8a27a', ec=INK, lw=.5)
        ax.plot([x + w - .45, x + w - .25], [y + 3.3, y + 3.3], c=INK, lw=1.2)
    else:
        R_(ax, x, y + sill, x + w, y + h, fc='#cfe3f3', ec=INK, lw=.9)
        n = max(1, round(w / 2.4))
        for i in range(1, n): ax.plot([x + w * i / n] * 2, [y + sill, y + h], c=INK, lw=.5)
        ax.plot([x, x + w + 0], [y, y], c='#9ca3af', lw=.5, ls='--')
        if sill > 0:
            ax.plot([x + w + .3] * 2, [y, y + sill], c=INK, lw=.35); ax.text(x + w + .45, y + sill / 2, f'SILL {fmt(sill)}', fontsize=3.8, va='center')
    ax.plot([x, x + w], [y - .55, y - .55], c=INK, lw=.35)
    ax.text(x + w / 2, y - .5, fmt(w), ha='center', va='bottom', fontsize=4.2)
    ax.plot([x - .4] * 2, [y + sill, y + h], c=INK, lw=.35)
    ax.text(x - .5, y + (sill + h) / 2, fmt(h - sill), rotation=90, ha='right', va='center', fontsize=4.2)
    ax.text(x + w / 2, y + h + .5, tag, ha='center', fontsize=5.5, weight='bold')
    if label: ax.text(x + w / 2, y - 1.7, label, ha='center', va='top', fontsize=3.8, color='#374151')

def d101(pdf):
    fig = plt.figure(figsize=(W_IN, H_IN)); ax0, x0, y = frame(fig)
    notes(ax0, x0, y, ['DOOR & WINDOW NOTES',
                       '1. Door heights 7\'-0". Frames 2"x5" seasoned wood.',
                       '2. Main door D1: 6\'-0" double teak (2 x 3\'-0"),',
                       '   centred on the porch, opens out to the landing.',
                       '3. Room doors 3\'-6" solid-core flush; baths',
                       '   2\'-0" WPC (water-proof).',
                       '4. Pocket sliding doors in 9" walls: D4 (dress),',
                       '   D9 & D10 (drawing room, 3\'-6"), D12 (store).',
                       '   D14 (Bed-1 dressing) on a top track. All',
                       '   wardrobes have sliding shutters.',
                       '5. Lawn door D5 opens INWARD into the passage.',
                       '6. Swing leaves hinge on the corner side and',
                       '   park flat against the adjoining wall.',
                       '7. Windows: aluminium, 5mm tinted glass, MS',
                       '   safety grill inside. Vents: frosted louvres.',
                       '8. W9 is a fixed glazed sidelight to the door.',
                       '9. Sill / head heights are above the GF FFL.'])
    title_block(ax0, x0, 'DOOR & WINDOW\nSCHEDULE + TYPES', 'D-101', '1/8" = 1\'-0" (TYPES)')
    ax = fig.add_axes([0, 0, 1, 1], facecolor='none'); ax.set_xlim(0, W_IN); ax.set_ylim(0, H_IN); ax.axis('off')
    # schedules
    ax.text(.6, H_IN - .7, 'DOOR SCHEDULE', fontsize=10, weight='bold')
    rows = []
    nm = lambda k: R[k]['name'].split(' (')[0].title().replace('Family Lounge + Dining', 'Lounge') if k in R else ('Lawn' if k == 'OUTSIDE' else k)
    for d in DOORS:
        if d['id'] == 'D1b': continue
        a = side_space(d, d['side']); b = side_space(d, -d['side'])
        w = math.dist(d['p0'], d['p1'])
        if d['id'] == 'D1a':
            rows.append(['D1', 'DT-0  6\'-0" DOUBLE', '6\'-0" x 7\'-0"', 'Car porch landing <-> Foyer', 'both leaves out to landing']); continue
        if d['kind'] == 'pocket':
            typ = 'DT-2P 2\'-6" POCKET'; how = 'slides into wall'
        elif d['kind'] == 'slide':
            typ = 'DT-2S 2\'-6" SLIDING'; how = 'slides on room face'
        else:
            typ = {3.5: 'DT-1  3\'-6"', 2.0: 'DT-3  2\'-0"'}[round(w, 2)]
        fr = 'Car porch landing' if b == 'PORCH' else nm(b)
        to = 'Car porch landing' if a == 'PORCH' else nm(a)
        if d['kind'] == 'swing': how = 'into ' + to
        else: fr, to = nm(side_space(d, +1)), nm(side_space(d, -1))
        rows.append([d['id'], typ, f"{fmt(w)} x {fmt(d['h'])}", f'{fr} -> {to}' if d['kind'] == 'swing' else f'{to} <-> {fr}', how])
    yy = table(ax, .6, H_IN - .85, ['TAG', 'TYPE', 'SIZE W x H', 'FROM -> TO', 'LEAF OPENS'], [.45, .9, 1.05, 2.1, 1.35], rows, fs=5.8, rh=.19)
    ax.text(.6, yy - .35, 'WINDOW & VENTILATOR SCHEDULE', fontsize=10, weight='bold')
    wrows = []
    for w in WINDOWS:
        L = math.dist(w['p0'], w['p1'])
        a, b = side_space(w, +1), side_space(w, -1)
        inside = a if a in R and R[a]['kind'] != 'open' else b
        out = b if inside == a else a
        wrows.append([w['id'], f"{fmt(L)} x {fmt(w['head']-w['sill'])}", fmt(w['sill']), fmt(w['head']), nm(inside),
                      {'OUTSIDE': 'open air', 'PORCH': 'car porch', 'OTS': 'OTS'}.get(out, out), w['kind']])
    table(ax, .6, yy - .5, ['TAG', 'SIZE W x H', 'SILL', 'HEAD', 'ROOM', 'OPENS TO', 'TYPE'], [.45, 1.15, .6, .6, 1.25, .75, .6], wrows, fs=5.8, rh=.19)
    # type elevations at 1/4" = 1'-0"
    axt = scaled_axes(fig, 6.9, .7, (0, 46), (-32, 46), 8)
    axt.text(0, 44.0, 'DOOR TYPES', fontsize=9, weight='bold')
    door_elev(axt, 1.5, 33.0, 6.0, 7.0, 'DT-0', label='D1 MAIN\n2 x 3\'-0"')
    axt.plot([4.5, 4.5], [33.0, 40.0], c=INK, lw=.6)
    ids = lambda f_: ' '.join(d['id'] for d in DOORS if d['id'] not in ('D1a', 'D1b') and f_(d))
    door_elev(axt, 11.0, 33.0, 3.5, 7.0, 'DT-1', label=ids(lambda d: d['kind'] == 'swing' and abs(math.dist(d['p0'], d['p1']) - 3.5) < .01))
    door_elev(axt, 19.0, 33.0, 2.5, 7.0, 'DT-2P/2S', label=ids(lambda d: d['kind'] != 'swing') + '\nSLIDING')
    axt.annotate('', xy=(22.5, 37.0), xytext=(20.0, 37.0), arrowprops=dict(arrowstyle='->', lw=.6))
    door_elev(axt, 27.0, 33.0, 2.0, 7.0, 'DT-3', label=ids(lambda d: d['kind'] == 'swing' and abs(math.dist(d['p0'], d['p1']) - 2.0) < .01))
    axt.text(0, 26.0, 'WINDOW & VENT TYPES (HEIGHTS FROM FFL)', fontsize=9, weight='bold')
    seen = {}
    xcur, ycur = 2.0, 14.0
    for w in WINDOWS:
        L = round(math.dist(w['p0'], w['p1']), 3); key = (L, w['sill'], w['head'], w['kind'])
        seen.setdefault(key, []).append(w['id'])
    for (L, sill, head, kind), tags in seen.items():
        if xcur + L > 44.0:
            xcur, ycur = 2.0, ycur - 14.0
        door_elev(axt, xcur, ycur, L, head, '/'.join(tags), kind='window', sill=sill, label=kind)
        xcur += L + 5.5
    pdf.savefig(fig); plt.close(fig)

def porch_section(ax):
    """Section B-B through the car porch (looking east). Horizontal = Y (road on the left)."""
    ax.set_aspect('equal'); ax.axis('off')
    z = lambda v: v                      # absolute levels (datum = road at P1)
    gz = GATE_Z
    # road & retaining
    ax.plot([-6, 0], [gz, gz], c=INK, lw=1.2)
    for x in range(-6, 0): ax.plot([x, x - .7], [gz, gz - .6], c=INK, lw=.3)
    # ramp, tread, landing
    prof = [(0, gz), (RAMP_END_Y, RAMP_TOP_Z), (TREAD_Y[0], RAMP_TOP_Z + PORCH_RISER), (TREAD_Y[1], RAMP_TOP_Z + PORCH_RISER),
            (TREAD_Y[1], FFL), (19.75, FFL), (19.75, gz - 1.5), (0, gz - 1.5)]
    prof = [(0, gz), (RAMP_END_Y, RAMP_TOP_Z), (RAMP_END_Y, RAMP_TOP_Z + PORCH_RISER), (TREAD_Y[1], RAMP_TOP_Z + PORCH_RISER),
            (TREAD_Y[1], FFL), (19.75, FFL), (19.75, gz - 1.5), (0, gz - 1.5)]
    ax.add_patch(MPoly(prof, closed=True, fc='#e7e2d6', ec=INK, lw=.8))
    # lounge wall with door, slab over porch
    R_(ax, 19.75, FFL, 20.5, FFL + CEIL, fc='#3a3a3a', ec=INK)
    R_(ax, 19.75, FFL, 20.5, FFL + 7.0, fc='white', ec=INK, lw=.5)
    ax.text(20.9, FFL + 3.5, 'MAIN DOOR D1\n3\'-6" x 7\'-0"', fontsize=4, va='center')
    R_(ax, 0, FFL + CEIL, 20.5, FFL + CEIL + .5, fc='#d1d5db', ec=INK, lw=.6)
    R_(ax, 0, FFL + CEIL - .75, .75, FFL + CEIL, fc='#d1d5db', ec=INK, lw=.5)
    ax.text(10, FFL + CEIL + .9, 'RCC SLAB (FIRST-FLOOR TERRACE ABOVE)', fontsize=4.3, ha='center')
    # car outline on the ramp
    th = math.atan(RAMP_SLOPE); y0, y1 = CAR.bounds[1], CAR.bounds[3]
    def onramp(y, hgt): return (y - hgt * math.sin(th), ramp_z(y) + hgt * math.cos(th))
    car = [onramp(y0 + .5, .6), onramp(y1 - .2, .6), onramp(y1 - .2, 2.6), onramp(y1 - 3.5, 2.9), onramp(y1 - 5.0, 4.6),
           onramp(y0 + 3.5, 4.6), onramp(y0 + 1.5, 3.0), onramp(y0 + .2, 2.7), onramp(y0 + .2, .9)]
    ax.add_patch(MPoly(car, closed=True, fc='none', ec='#6b7280', lw=.6, ls='--'))
    ax.text(7.5, ramp_z(7.5) + 2.2, 'CAR MAX 15\'-0"', fontsize=4, color='#6b7280', ha='center', rotation=math.degrees(th))
    # dims
    def hd(a, b, yv, t):
        ax.plot([a, b], [yv, yv], c=INK, lw=.35)
        for x in (a, b): ax.plot([x - .2, x + .2], [yv - .2, yv + .2], c=INK, lw=.5)
        ax.text((a + b) / 2, yv + .15, t, ha='center', fontsize=4.3)
    hd(0, RAMP_END_Y, gz - 2.4, f'RAMP {fmt(RAMP_END_Y)} @ 1:{1/RAMP_SLOPE:.1f}')
    hd(TREAD_Y[0], TREAD_Y[1], gz - 2.4, '1\'-0"'); hd(LANDING_Y, 19.75, gz - 2.4, '3\'-6"')
    for yv, t in ((gz, f'GATE {fmt(gz)}'), (RAMP_TOP_Z, f'WHEEL-STOP {fmt(RAMP_TOP_Z)}'), (FFL, f'LANDING = FFL +{fmt(FFL)}')):
        ax.plot([-6, -1], [yv, yv], c=INK, lw=.3); ax.text(-6, yv + .15, t, fontsize=4.2)
    ax.text(16.6, RAMP_TOP_Z + .2, '2 RISERS\n7 1/2"', fontsize=3.8, ha='right')
    ax.text(-6, FFL + CEIL + 2.0, 'SECTION B-B : CAR PORCH RAMP & ENTRANCE', fontsize=9, weight='bold')
    ax.set_xlim(-7, 24); ax.set_ylim(gz - 3.5, FFL + CEIL + 3)

def d102(pdf):
    fig = plt.figure(figsize=(W_IN, H_IN)); ax0, x0, y = frame(fig)
    notes(ax0, x0, y, ['STAIR & ENTRANCE NOTES',
                       '1. Stair: RCC waist slab 5", treads 10" + 1"',
                       '   nosing, risers 6.95", width 3\'-6".',
                       '2. Riser count: flight-1 = 13 (to landing',
                       '   +7\'-6 1/2"), flight-2 = 6 (to FF +11\'-0").',
                       '3. Under the landing (7\'-1 1/2" clear) is the foyer;',
                       '   door D8 (3\'-6") on grid D closes the guest',
                       '   lobby -> drawing room D10, washroom D11, store',
                       '   D12. Drawing guest door D9 off the porch.',
                       '4. Glass balustrade 3\'-0" high on open sides.',
                       '5. ' + ('Flight-2 runs west over the foyer; soffit' if VER == 'L' else 'Flight-2 returns north beside flight-1;'),
                       '   ' + ('7\'-1 1/2" rising to 10\'-6".' if VER == 'L' else 'the 7\'-0" wide half landing covers the foyer.'),
                       '   Main door head 7\'-0" clears the soffit.',
                       '6. Porch ramp: broom-finished grooved RCC,',
                       '   drain channel with grating across the gate.',
                       '7. Wheel-stop (6" kerb) at the top of the ramp;',
                       '   max car length 15\'-0".'])
    title_block(ax0, x0, 'STAIR & ENTRANCE\nDETAILS', 'D-102', 'PLAN & A-A 1/4"=1\'-0"\nB-B 3/16"=1\'-0"')
    # enlarged plan of the stair & entrance
    axp = scaled_axes(fig, .5, 4.9, (55.5, 71.0), (13.5, 37.5), 4)
    draw_ground_floor(axp, furniture=False, dims=False, title=False)
    axp.set_xlim(55.5, 71.0); axp.set_ylim(13.5, 37.5)
    for i, (poly, h, fl) in enumerate(STAIR_TREADS):
        c = poly.centroid
        if fl == 1: axp.text(c.x - 1.15, c.y, str(i + 1), fontsize=4.2, ha='center', va='center', color=RED, zorder=9)
        elif fl == 2: axp.text(c.x, c.y - 1.2, str(i + 1), fontsize=4.2, ha='center', va='center', color=RED, zorder=9)
    dim_h(axp, 65.125, 68.625, 35.2, fs=4.4); dim_v(axp, 24.0, 34.0, 70.6, txt='12 TREADS = 10\'-0"', fs=4.0)
    if VER == 'L': dim_h(axp, F2_END_X, 65.125, 25.0, txt='5 TREADS = 4\'-2"', fs=4.0)
    else:
        dim_v(axp, 24.0, F2_END_Y, 60.9, txt='5 TREADS 4\'-2"', fs=4.0); dim_h(axp, 61.625, 68.625, 25.0, txt='LANDING 7\'-0"', fs=4.0)
    dim_v(axp, 20.5, 24.0, 70.6, txt='3\'-6"', fs=4.0)
    dim_h(axp, 60.0, 66.0, 14.6, txt='D1 6\'-0"', fs=4.0)
    clip_all(axp)
    fig.text(.5 / W_IN, 10.95 / H_IN, f'ENLARGED PLAN : {VNAME}, LOBBY & ENTRANCE  (1/4"=1\'-0")', fontsize=8, weight='bold')
    # section A-A (stair) & B-B (porch)
    ax2 = scaled_axes(fig, 5.0, 6.3, (16, 40), (-3, FF_TO_FF + 4), 4)
    draw_stair_section(ax2)
    ax3 = scaled_axes(fig, 5.0, .6, (-7, 24), (GATE_Z - 3.5, FFL + CEIL + 3), 16 / 3)
    porch_section(ax3)
    pdf.savefig(fig); plt.close(fig)

def d102b(pdf):
    fig = plt.figure(figsize=(W_IN, H_IN)); ax0, x0, y = frame(fig)
    notes(ax0, x0, y, ['INTERIOR ELEVATIONS (TRUE VIEW)',
                       '1. B-B is what you see standing in the foyer',
                       '   facing the entrance (south): the drawing',
                       '   room & lobby are on your LEFT, the passage',
                       '   on your RIGHT.',
                       '2. C-C is the view from the foyer into the',
                       '   guest lobby (east): drawing room door on the',
                       '   right-hand wall, guest washroom ahead.',
                       '3. The foyer under the landing is 7\'-1 1/2" high;',
                       '   the closed guest lobby behind D8 is 10\'-6".',
                       '4. Doors: D1 6\'-0" (2 x 3\'-0"), D8 lobby 3\'-6",',
                       '   D10 drawing 3\'-6" pocket, D11 washroom 2\'-0",',
                       '   D12 store 2\'-6" pocket.'])
    title_block(ax0, x0, 'INTERIOR ELEVATIONS\nENTRANCE & LOBBY', 'D-102B', '1/4" = 1\'-0"')
    a1 = scaled_axes(fig, .5, 5.75, (80 - 76 - 1.5, 80 - 50 + 1.5), (-2.2, FF_TO_FF + 3.2), 4)
    elev_looking_south(a1)
    a2 = scaled_axes(fig, .5, .55, (60 - 35.5 - 1.0, 60 - 18.5 + 1.0), (-1.5, FF_TO_FF + 3.2), 4)
    elev_looking_east(a2)
    pdf.savefig(fig); plt.close(fig)

def d105(pdf):
    import matplotlib.image as mpimg, os
    shots = [('A_lounge_looking_south', 'FROM THE LOUNGE LOOKING SOUTH - stair, landing and the entrance beneath'),
             ('B_foyer_looking_east_into_lobby', 'FROM THE FOYER LOOKING EAST - lobby door D8 (open), drawing door & washroom beyond'),
             ('C_dining_looking_east_at_stair', 'FROM THE DINING AREA - stair profile and open space under the flights'),
             ('D_porch_looking_north_at_entrance', 'FROM THE CAR PORCH - 6\'-0" main door centred, sidelights W9 / W10')]
    fig = plt.figure(figsize=(W_IN, H_IN)); ax0, x0, y = frame(fig)
    notes(ax0, x0, y, ['3D VIEWS', f'{VNAME}',
                       'Rendered from the 3D model built from the',
                       'same dimensions as these drawings. Walls are',
                       'cut at ceiling height so the stair, landing',
                       'and the space beneath are fully visible.'])
    title_block(ax0, x0, '3D VIEWS\nSTAIR & ENTRANCE', 'D-105', 'N.T.S.')
    pos = [(.5, 5.85), (6.6, 5.85), (.5, .75), (6.6, .75)]
    for (nm_, cap), (px, py) in zip(shots, pos):
        fp = f'stills/{VER}_{nm_}.png'
        ax = fig.add_axes([px / W_IN, py / H_IN, 5.9 / W_IN, 3.32 / H_IN]); ax.axis('off')
        if os.path.exists(fp): ax.imshow(mpimg.imread(fp))
        fig.text(px / W_IN, (py + 3.42) / H_IN, cap, fontsize=6.3, weight='bold')
    pdf.savefig(fig); plt.close(fig)

def ots_section(ax):
    """Section C-C across the OTS, perpendicular to the north boundary (horizontal = distance from lounge)."""
    ax.set_aspect('equal'); ax.axis('off')
    # from left: lounge (3'), lounge wall 9", OTS 3'-0", boundary wall 9", neighbour
    x_lw = 3.0; x_ots = x_lw + .75; x_bw = x_ots + 3.0; x_nb = x_bw + .75
    top = FFL + 3 * FF_TO_FF + 3
    ax.plot([-1, x_nb + 2], [PLOT_Z, PLOT_Z], c=INK, lw=1.0)
    R_(ax, 0, PLOT_Z, x_lw, FFL, fc='#d6d3cd', ec=INK, lw=.5)
    ax.text(1.5, FFL + 1.0, 'LOUNGE\nFFL +0\'-6"', fontsize=4.3, ha='center')
    for k in range(3):
        base = FFL + k * FF_TO_FF
        R_(ax, x_lw, base, x_ots, base + 3.0, fc='#3a3a3a', ec=INK, lw=.4)
        R_(ax, x_lw, base + 3.0, x_ots, base + 7.0, fc='#cfe3f3', ec=INK, lw=.5)
        R_(ax, x_lw, base + 7.0, x_ots, base + FF_TO_FF, fc='#3a3a3a', ec=INK, lw=.4)
        R_(ax, -1, base + CEIL, x_lw, base + FF_TO_FF, fc='#d1d5db', ec=INK, lw=.4)
    R_(ax, x_bw, PLOT_Z, x_nb, top, fc='#3a3a3a', ec=INK, lw=.4)
    R_(ax, x_ots, PLOT_Z, x_bw, PLOT_Z + .5, fc='#c6e7c9', ec=INK, lw=.4)
    ax.text((x_ots + x_bw) / 2, PLOT_Z + .9, 'GRAVEL + PLANTS\nFLOOR DRAIN', fontsize=3.6, ha='center')
    ax.text((x_ots + x_bw) / 2, top - 2.0, 'OPEN TO SKY\n(ALL FLOORS)', fontsize=4.3, ha='center')
    ax.annotate('', xy=(x_bw, FFL + 8.5), xytext=(x_ots, FFL + 8.5), arrowprops=dict(arrowstyle='<->', lw=.5))
    ax.text((x_ots + x_bw) / 2, FFL + 8.8, '3\'-0"\nCLEAR', fontsize=4.3, ha='center')
    ax.text(x_lw + .375, FFL + 5.0, 'W7/W8', rotation=90, fontsize=3.8, ha='center', va='center')
    ax.text(x_nb + .2, top - 6, 'BOUNDARY\nWALL 9"', fontsize=4.0)
    ax.text(-1, top + 1.2, 'SECTION C-C : OTS (LIGHT WELL)', fontsize=9, weight='bold')
    ax.set_xlim(-1.5, x_nb + 4); ax.set_ylim(PLOT_Z - 1, top + 2.5)

def d103(pdf):
    fig = plt.figure(figsize=(W_IN, H_IN)); ax0, x0, y = frame(fig)
    o = R['OTS']['geom']
    notes(ax0, x0, y, ['OTS (OPEN-TO-SKY LIGHT WELL)',
                       f'1. Clear width 3\'-0" measured square to the',
                       '   north boundary, between the 9" lounge wall',
                       '   and the 9" boundary wall.',
                       f'2. Length on lounge side {fmt(math.dist((52.125, 38.323), (68.625, 46.953)))},',
                       f'   on boundary side {fmt(math.dist((52.125, 41.709), (68.015, 50.02)) + math.dist((68.015, 50.02), (68.625, 50.268)))}.',
                       f'3. End widths (N-S): {fmt(41.709-38.323)} at grid C,',
                       f'   {fmt(50.268-46.953)} at grid D. Area {o.area:.1f} sq ft.',
                       '4. Floor: 4" gravel over brick-on-edge with a',
                       '   4" floor drain; lounge glazing W7 & W8.',
                       '5. Dirty kitchen vent V2 opens into the OTS.',
                       '6. Kept open through every floor up to the roof.'])
    title_block(ax0, x0, 'OTS DETAIL\n(PLAN + SECTION)', 'D-103', 'PLAN 3/8"=1\'-0"\nSECTION 1/8"=1\'-0"')
    axp = scaled_axes(fig, .5, 1.4, (48.0, 72.0), (33.0, 54.0), 8 / 3)
    draw_ground_floor(axp, furniture=False, dims=False, title=False)
    axp.set_xlim(48.0, 72.0); axp.set_ylim(33.0, 54.0)
    dim_al(axp, (52.125, 41.709), (68.015, 50.02), 1.4, fs=6)
    dim_al(axp, (52.125, 38.323), (68.625, 46.953), -1.3, fs=6)
    dim_v(axp, 38.323, 41.709, 50.8, fs=5.5); dim_v(axp, 46.953, 50.268, 70.6, fs=5.5)
    th = math.atan(0.523); nx, ny = -math.sin(th), math.cos(th)
    for xm in (56.0, 64.0):
        ym = 38.323 + (xm - 52.125) * 0.523
        a = (xm + nx * .75, ym + ny * .75); b = (xm + nx * 3.75, ym + ny * 3.75)
        axp.annotate('', xy=b, xytext=a, arrowprops=dict(arrowstyle='<->', lw=.6), zorder=9)
        axp.text((a[0] + b[0]) / 2 + .9, (a[1] + b[1]) / 2 - .2, '3\'-0"', fontsize=6, rotation=math.degrees(th), zorder=9)
    for w in ('W7', 'W8'):
        ww = [x for x in WINDOWS if x['id'] == w][0]
        dim_al(axp, ww['p0'], ww['p1'], -2.6, txt=f'{w} {fmt(math.dist(ww["p0"], ww["p1"]))}', fs=5)
    clip_all(axp)
    fig.text(.5 / W_IN, 9.55 / H_IN, 'ENLARGED PLAN : OTS  (3/8"=1\'-0")', fontsize=9, weight='bold')
    ax2 = scaled_axes(fig, 10.2, 1.0, (-1.5, 13.5), (PLOT_Z - 1, FFL + 3 * FF_TO_FF + 5.5), 8)
    ots_section(ax2)
    pdf.savefig(fig); plt.close(fig)

def d104(pdf):
    fig = plt.figure(figsize=(W_IN, H_IN)); ax0, x0, y = frame(fig)
    notes(ax0, x0, y, ['FINISH KEY',
                       '  WOOD  = engineered wood / laminate',
                       '  TILE  = 24"x24" porcelain',
                       '  WET   = anti-skid ceramic + waterproofing',
                       '  PAVER = grooved RCC / exterior pavers',
                       '',
                       'CEILINGS',
                       '  10\'-6" clear unless noted. Powder west',
                       '  half 7\'-1 1/2" (under stair landing).'])
    title_block(ax0, x0, 'ROOM & COLUMN\nSCHEDULES', 'D-104', 'N.T.S.')
    ax = fig.add_axes([0, 0, 1, 1], facecolor='none'); ax.set_xlim(0, W_IN); ax.set_ylim(0, H_IN); ax.axis('off')
    ax.text(.6, H_IN - .7, 'ROOM SCHEDULE - GROUND FLOOR', fontsize=10, weight='bold')
    order = ['DRAW', 'BED2', 'DRS2', 'BATH2', 'LNG', 'KIT', 'DKIT', 'PASS', 'LOBBY', 'STORE', 'BATHD', 'BED1', 'DRS1', 'WR1', 'PORCH', 'OTS']
    fin = {'wood': 'WOOD', 'tile': 'TILE', 'paver': 'PAVER'}
    rows = []
    for k in order:
        r = R[k]; g = r['geom']; bx = g.bounds
        rect = len(g.exterior.coords) == 5
        size = f"{fmt(bx[2]-bx[0])} x {fmt(bx[3]-bx[1])}" if rect else 'irregular'
        f_ = 'WET' if r['kind'] == 'wet' else fin.get(r['finish'], 'TILE')
        if k == 'OTS': f_ = 'GRAVEL'
        rows.append([r['name'].replace('FAMILY LOUNGE + DINING', 'LOUNGE + DINING'), size, f"{g.area:.1f}", f_])
    encl = sum(R[k]['geom'].area for k in order if R[k]['kind'] != 'open')
    covered = FOOTPRINT.area - R['OTS']['geom'].area
    rows += [['TOTAL NET CARPET AREA', '', f'{encl:.1f}', ''], ['TOTAL COVERED AREA (WITH WALLS, PORCH)', '', f'{covered:.1f}', ''],
             ['GROUND COVERAGE', '', f'{covered/PLOT.area*100:.1f} %', ''], ['MAIN LAWN', '', f"{(PLOT & box(-5,-5,LINE_B,80)).area:.1f}", 'GRASS']]
    table(ax, .6, H_IN - .85, ['SPACE', 'CLEAR SIZE', 'SQ.FT', 'FLOOR'], [2.6, 1.6, .7, .7], rows, fs=6.0)
    ax.text(6.9, H_IN - .7, 'COLUMN SCHEDULE', fontsize=10, weight='bold')
    def grid_ref(x, y):
        gx = min(GRID_X.items(), key=lambda kv: abs(kv[1] - x)); gy = min(GRID_Y.items(), key=lambda kv: abs(kv[1] - y))
        rx = gx[0] if abs(gx[1] - x) < 1.0 else f'{gx[0]}{"+" if x > gx[1] else "-"}{fmt(abs(x-gx[1]))}'
        ry = gy[0] if abs(gy[1] - y) < 1.0 else 'boundary wall'
        return f'{rx} / {ry}'
    crow = []
    for i, (k, c) in enumerate(COLUMNS.items(), 1):
        bx = c.bounds; along = 'E-W' if (bx[2] - bx[0]) > (bx[3] - bx[1]) else 'N-S'
        crow.append([f'C{i}', grid_ref(c.centroid.x, c.centroid.y), '9" x 18"', along, f'({c.centroid.x:.2f}, {c.centroid.y:.2f})'])
    table(ax, 6.9, H_IN - .85, ['MARK', 'GRID / LOCATION', 'SIZE', '18" ALONG', 'CENTRE X,Y (FT)'], [.55, 1.75, .7, .7, 1.25], crow, fs=5.8, rh=.19)
    pdf.savefig(fig); plt.close(fig)

if __name__ == '__main__':
    import os; os.makedirs('out', exist_ok=True)
    with PdfPages(f'out/DH-GF-{REV}-{VER}_Drawings.pdf') as pdf:
        a101(pdf); a102(pdf); a103(pdf)
        d = pdf.infodict(); d['Title'] = f'Daata Hamlet Residence - Ground Floor Drawings {REV}'; d['Author'] = 'Daata Hamlet Residence'
    with PdfPages(f'out/DH-GF-{REV}-{VER}_Details.pdf') as pdf:
        d101(pdf); d102(pdf); d102b(pdf); d105(pdf); d103(pdf); d104(pdf)
        d = pdf.infodict(); d['Title'] = f'Daata Hamlet Residence - Ground Floor Details {REV}'; d['Author'] = 'Daata Hamlet Residence'
    print('ok')
