"""A3 drawing set (PDF) - true scale 1/8"=1'-0" plan & elevation, 1/4"=1'-0" section."""
import datetime, math
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from matplotlib.patches import Rectangle
from model import *
from draw_plan import draw_ground_floor, door_geom
from draw_elev import draw_south_elevation, draw_stair_section
import checks

W_IN, H_IN = 16.535, 11.693
DATE = '05 OCT 2026'

def frame(fig, title, no, scale):
    ax = fig.add_axes([0, 0, 1, 1]); ax.set_xlim(0, W_IN); ax.set_ylim(0, H_IN); ax.axis('off')
    ax.add_patch(Rectangle((.3, .3), W_IN - .6, H_IN - .6, fill=False, lw=1.4))
    ax.add_patch(Rectangle((.4, .4), W_IN - .8, H_IN - .8, fill=False, lw=.4))
    x0 = W_IN - 3.55
    ax.add_patch(Rectangle((x0, .4), 3.15, H_IN - .8, fill=False, lw=.8))
    y = H_IN - .9
    ax.text(x0 + .15, y, 'DAATA HAMLET', fontsize=15, weight='bold'); y -= .3
    ax.text(x0 + .15, y, 'RESIDENCE', fontsize=15, weight='bold'); y -= .3
    ax.text(x0 + .15, y, 'Contemporary 3-storey villa  |  Pakistan', fontsize=7, color='#555'); y -= .45
    rows = [('PLOT', '3,129.1 sq ft  (290.7 m2)'), ('', '13.9 marla @225 / 11.5 @272.25'),
            ('STAGE', 'GROUND FLOOR - DESIGN v2'), ('UNITS', 'Feet-inches; origin = peg P1'),
            ('LEVELS', 'Plot/lawn +/-0 (=road P1), FFL +0\'-6"'), ('FLOOR HT', '11\'-0" floor-to-floor')]
    for a, b in rows:
        ax.text(x0 + .15, y, a, fontsize=6.5, color='#666'); ax.text(x0 + 1.0, y, b, fontsize=6.5); y -= .22
    y -= .1
    ax.plot([x0, x0 + 3.15], [y, y], c='k', lw=.5); y -= .3
    return ax, x0, y

def notes_block(ax, x0, y, lines, fs=6.2):
    for ln in lines:
        ax.text(x0 + .15, y, ln, fontsize=fs, va='top', wrap=True); y -= .19 * (1 + ln.count('\n'))
    return y

def title_bottom(ax, x0, title, no, scale):
    ax.add_patch(Rectangle((x0, .4), 3.15, 1.55, fill=False, lw=.8))
    ax.text(x0 + .15, 1.68, 'SHEET TITLE', fontsize=5.5, color='#666')
    ax.text(x0 + .15, 1.42, title, fontsize=9, weight='bold', va='top')
    ax.text(x0 + .15, .85, 'SCALE', fontsize=5.5, color='#666'); ax.text(x0 + .15, .62, scale, fontsize=7.5)
    ax.text(x0 + 1.7, .85, 'SHEET NO.', fontsize=5.5, color='#666'); ax.text(x0 + 1.7, .55, no, fontsize=16, weight='bold', color='#c0392b')
    ax.text(x0 + .15, .45, f'DATE {DATE}', fontsize=5, color='#666')

GEN_NOTES = [
    'GENERAL NOTES',
    '1. All dimensions in feet-inches. Do not scale; follow',
    '   written dimensions. Survey pegs per C-101.',
    '2. External / structural walls 9", partitions 4.5".',
    '3. RCC columns 9"x18" (21 nos) - size, steel and',
    '   footing to be confirmed by structural engineer.',
    '4. Zero construction west of Line B (X=36\'-1 1/2").',
    '5. Front setback 3\'-0"; east service passage',
    '   2\'-9 1/2" at road widening to 3\'-7" at rear.',
    '6. Every bath, powder and kitchen vents directly',
    '   to open air (road side, porch, OTS or passage).',
    '7. Authority bylaws (setbacks, coverage) to be',
    '   verified before submission for approval.',
]

def sheet_plan(pdf):
    fig = plt.figure(figsize=(W_IN, H_IN))
    ax0, x0, y = frame(fig, '', '', '')
    y = notes_block(ax0, x0, y, GEN_NOTES)
    y -= .15
    y = notes_block(ax0, x0, y, [
        'LEGEND',
        '   solid black  = RCC column 9"x18"',
        '   dark grey    = wall (9" / 4.5")',
        '   blue triple  = window,  double = ventilator',
        '   dashed treads = stair above 4\'-0" cut plane',
        '   D# / W# / V# = door / window / vent tags',
        '      (see schedule sheet A-103)',
    ])
    title_bottom(ax0, x0, 'GROUND FLOOR PLAN\n(FURNISHED, DIMENSIONED)', 'A-101', '1/8" = 1\'-0"  (1:96)')
    # true scale axes: 100 ft wide x 78 ft high at 1/8" per ft
    ax = fig.add_axes([.45 / W_IN, .6 / H_IN, 12.5 / W_IN, 9.75 / H_IN])
    draw_ground_floor(ax)
    pdf.savefig(fig); plt.close(fig)

def sheet_elev(pdf):
    fig = plt.figure(figsize=(W_IN, H_IN))
    ax0, x0, y = frame(fig, '', '', '')
    y = notes_block(ax0, x0, y, [
        'FACADE & SITE NOTES (ROAD SIDE)',
        '1. Road falls 6\'-0" from P1 to P0. Plot and lawn',
        '   are filled level with the road at P1 (+/-0), so',
        '   nothing sits below the road. GF FFL +0\'-6".',
        '2. Stone retaining wall along the front (0 to',
        '   6\'-0") with a 3\'-6" MS railing on top.',
        '3. Car porch: one ramp (approx. 1:4.6, grooved',
        '   concrete) from the gate (-4\'-3 1/2") to a',
        '   wheel-stop at -0\'-9", then 2 full-width risers',
        '   of 7 1/2" to a 2\'-6" landing at the main door.',
        '4. 4\'-0" main door centred under flight-2;',
        '   drawing guest door D9 off the same landing.',
        '5. Pedestrian gate 3\'-6" at the east end of the',
        '   lawn: 4 steps up, stone path to side door D5.',
        '6. W1 & W3 centred, sill 2\'-6", 1\'-6" chajja.',
        '',
        'STAIR (SECTION A-A)',
        '1. L-type stair, 3\'-6" wide, 19 risers of 6.95".',
        '2. Flight-1: 13 risers climbs to the landing',
        '   at +7\'-6 1/2" (sits on the powder room).',
        '3. Flight-2: 6 risers climbs the last 3\'-5 1/2"',
        '   to the first floor (+11\'-0").',
        '4. Powder clear height under landing 7\'-1 1/2"',
        '   -> standard 6\'-9" door fits.',
    ])
    title_bottom(ax0, x0, 'SOUTH ELEVATION (GF)\n+ STAIR SECTION A-A', 'A-102', 'ELEV 1/8"=1\'-0"\nSECTION 1/4"=1\'-0"')
    ax = fig.add_axes([.45 / W_IN, 6.3 / H_IN, 12.75 / W_IN, (12.5 + 20) / 8 / H_IN])
    draw_south_elevation(ax)
    ax2 = fig.add_axes([3.5 / W_IN, .6 / H_IN, 24 / 4 / W_IN, (11 + 7) / 4 / H_IN])
    draw_stair_section(ax2)
    pdf.savefig(fig); plt.close(fig)

def table(ax, x, y, cols, widths, rows, fs=6.3, rh=.205, head_fc='#1f2937'):
    tx = x
    for c, w in zip(cols, widths):
        ax.add_patch(Rectangle((tx, y - rh), w, rh, fc=head_fc, ec='white', lw=.3))
        ax.text(tx + .05, y - rh / 2, c, fontsize=fs, color='white', va='center', weight='bold'); tx += w
    y -= rh
    for i, r in enumerate(rows):
        tx = x
        fc = '#f3f4f6' if i % 2 else 'white'
        bold = r and str(r[0]).startswith('TOTAL')
        for v, w in zip(r, widths):
            ax.add_patch(Rectangle((tx, y - rh), w, rh, fc=fc, ec='#d1d5db', lw=.3))
            col = '#047857' if v == 'PASS' else ('#b91c1c' if v == 'FAIL' else 'black')
            ax.text(tx + .05, y - rh / 2, str(v), fontsize=fs, va='center', color=col, weight='bold' if bold or v in ('PASS', 'FAIL') else 'normal'); tx += w
        y -= rh
    return y

def sheet_schedules(pdf):
    fig = plt.figure(figsize=(W_IN, H_IN))
    ax0, x0, y0 = frame(fig, '', '', '')
    notes_block(ax0, x0, y0, [
        'WHAT CHANGED vs. THE OLD BRIEF',
        '- Stair re-planned as an L: landing sits on the',
        '  powder (half in the lounge), 13R + 6R = 11\'-0".',
        '  Old brief had 16 risers (only 10\'-2").',
        '- Kitchen kept fully inside the plot (old one',
        '  crossed the boundary by ~7 sq ft).',
        '- Dirty kitchen fills the P4 corner (59 sq ft).',
        '- Bed-1 rebalanced to 15\'x15\'; dressing and',
        '  washroom run right up to the north boundary',
        '  - no leftover strip along the hypotenuse.',
        '- Main door centred under flight-2. Porch is one',
        '  ramp + 2 risers (plinth reduced to 6" so that',
        '  plot & lawn stay at/above road level).',
        '- Pedestrian gate + stone path in the lawn.',
        '- Bed-2 suite is dress-through: bed -> dress',
        '  (5\'-3"x8\'-7 1/2") -> bath (5\'-3"x7\'-0").',
        '- U-shaped kitchen: 4\'-1" work aisle (an island',
        '  would have left only 1\'-6").',
        '- Lawn is 652 sq ft (old brief said 588.9).',
    ])
    title_bottom(ax0, x0, 'SCHEDULES +\nDESIGN VERIFICATION', 'A-103', 'N.T.S.')
    ax = fig.add_axes([0, 0, 1, 1], facecolor='none'); ax.set_xlim(0, W_IN); ax.set_ylim(0, H_IN); ax.axis('off')
    # area schedule
    ax.text(.6, H_IN - .7, 'ROOM AREA SCHEDULE - GROUND FLOOR', fontsize=10, weight='bold')
    rows = []
    order = ['DRAW', 'BED2', 'BATH2', 'DRS2', 'LNG', 'KIT', 'DKIT', 'PASS', 'PWD', 'DRSD', 'BATHD', 'BED1', 'DRS1', 'WR1', 'PORCH', 'OTS']
    vent = {}
    for k in order:
        r = R[k]; g = r['geom']; bx = g.bounds
        rect = len(g.exterior.coords) == 5 and k != 'PWD'
        size = f"{fmt(bx[2]-bx[0])} x {fmt(bx[3]-bx[1])}" if rect else 'irregular (fits boundary)'
        if k == 'PORCH': size = f"{fmt(bx[2]-bx[0])} x {fmt(19.75-0)}"
        rows.append([r['name'], size, f"{g.area:.1f}"])
    encl = sum(R[k]['geom'].area for k in order if R[k]['kind'] != 'open')
    rows.append(['TOTAL NET ENCLOSED (carpet)', '', f'{encl:.1f}'])
    covered = FOOTPRINT.area - R['OTS']['geom'].area
    rows.append(['TOTAL COVERED GF (incl. walls, porch)', '', f'{covered:.1f}'])
    rows.append(['GROUND COVERAGE of plot', '', f'{covered/PLOT.area*100:.1f} %'])
    rows.append(['MAIN LAWN (open)', '', f"{(PLOT & box(-5,-5,LINE_B,80)).area:.1f}"])
    y = table(ax, .6, H_IN - .85, ['SPACE', 'CLEAR SIZE', 'NET SQ.FT'], [2.3, 1.75, .75], rows)
    # door schedule
    ax.text(.6, y - .35, 'DOOR SCHEDULE', fontsize=10, weight='bold')
    drows = []
    seen = set()
    from checks import side_space
    for d in DOORS:
        i = d['id'].rstrip('ab')
        if i in seen: continue
        seen.add(i)
        w = math.dist(d['p0'], d['p1']) * (2 if d['id'] == 'D1a' else 1)
        a, b = side_space(d, d['side']), side_space(d, -d['side'])
        nm = lambda k: R[k]['name'].split(' (')[0].title() if k in R else 'Lawn'
        kind = 'Double, teak' if i == 'D1' else ('Flush, external' if i in ('D5', 'D9') else 'Flush')
        drows.append([i, f"{fmt(w)} x {fmt(d['h'])}", f"{nm(b)} -> {nm(a)}", kind])
    y = table(ax, .6, y - .5, ['TAG', 'SIZE (W x H)', 'CONNECTS (swings into 2nd)', 'TYPE'], [.45, 1.25, 2.35, .95], drows)
    # window schedule
    X2 = 6.0
    ax.text(X2, H_IN - .7, 'WINDOW & VENTILATOR SCHEDULE', fontsize=10, weight='bold')
    wrows = []
    for w in WINDOWS:
        L = math.dist(w['p0'], w['p1'])
        a, b = side_space(w, +1), side_space(w, -1)
        inside = a if a in R and R[a]['kind'] != 'open' else b
        out = b if inside == a else a
        wrows.append([w['id'], f"{fmt(L)} x {fmt(w['head']-w['sill'])}", fmt(w['sill']), R[inside]['name'].split(' (')[0].title(),
                      {'OUTSIDE': 'open air', 'PORCH': 'car porch', 'OTS': 'OTS'}.get(out, out), w['kind']])
    y2 = table(ax, X2, H_IN - .85, ['TAG', 'SIZE', 'SILL', 'ROOM', 'OPENS TO', 'TYPE'], [.45, 1.15, .6, 1.2, .8, .65], wrows)
    # verification
    ax.text(X2, y2 - .35, f'AUTOMATED DESIGN CHECKS  ({checks.ok}/{len(checks.results)} PASS)', fontsize=10, weight='bold')
    vrows = [[('PASS' if o else 'FAIL'), n[:62], d[:44]] for n, o, d in checks.results]
    table(ax, X2, y2 - .5, ['', 'CHECK', 'RESULT'], [.45, 3.45, 2.95], vrows, fs=5.3, rh=.178)
    pdf.savefig(fig); plt.close(fig)

if __name__ == '__main__':
    with PdfPages('out/daata_hamlet_GF_v2_drawings.pdf') as pdf:
        sheet_plan(pdf); sheet_elev(pdf); sheet_schedules(pdf)
        d = pdf.infodict(); d['Title'] = 'Daata Hamlet Residence - Ground Floor v2'; d['Author'] = 'Claude for Maaez'
    print('ok')
