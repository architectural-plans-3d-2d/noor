"""South (road) elevation of GF + stair section."""
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Polygon as MPoly
from model import *

INK = '#1b1b1b'
PL = FFL - PLOT_Z              # plinth: FFL above plot (0'-6")
TOP = PL + FF_TO_FF           # top of GF roof slab (road datum)

def R_(ax, x0, y0, x1, y1, **kw):
    ax.add_patch(Rectangle((x0, y0), x1 - x0, y1 - y0, **kw))

def window(ax, x0, x1, sill, head, kind='window'):
    y0, y1 = PL + sill, PL + head
    R_(ax, x0, y0, x1, y1, fc='#cfe3f3', ec=INK, lw=.8, zorder=4)
    fr = .25
    R_(ax, x0 + fr, y0 + fr, x1 - fr, y1 - fr, fc='#a9cbe6', ec=INK, lw=.4, zorder=4)
    if kind == 'window':
        n = max(2, round((x1 - x0) / 2.4))
        for i in range(1, n):
            x = x0 + (x1 - x0) * i / n
            ax.plot([x, x], [y0, y1], c=INK, lw=.5, zorder=5)
        ax.plot([x0, x1], [y1 - 1.6, y1 - 1.6], c=INK, lw=.4, zorder=5)    # fanlight transom
        # chajja (sunshade) 1'-6" projection shown as band
        R_(ax, x0 - .75, y1 + .25, x1 + .75, y1 + .6, fc='#9ca3af', ec=INK, lw=.5, zorder=4)
        # glass reflections
        for i in range(n):
            xa = x0 + (x1 - x0) * i / n + .4
            ax.plot([xa, xa + .9], [y0 + .6, y0 + 1.9], c='white', lw=.6, alpha=.8, zorder=5)
    else:
        for k in range(1, 4):
            ax.plot([x0 + fr, x1 - fr], [y0 + (y1 - y0) * k / 4] * 2, c=INK, lw=.4, zorder=5)

def draw_south_elevation(ax):
    ax.set_aspect('equal'); ax.axis('off')
    # ground / road (drawn relative to the plot level; labels give absolute levels, datum = road at P1)
    rr = lambda x: road_z(x) - PLOT_Z
    xs = [-3, 91]
    ax.plot(xs, [rr(x) for x in xs], c=INK, lw=1.4, zorder=3)
    ax.add_patch(MPoly([(-3, rr(-3)), (91, rr(91)), (91, rr(91) - 1.2), (-3, rr(-3) - 1.2)], fc='#e5e7eb', ec='none', zorder=1))
    for x in range(-3, 91, 2):
        ax.plot([x, x - 1], [rr(x), rr(x) - .8], c=INK, lw=.3, zorder=2)
    g0, g1 = PED_GATE
    # whole frontage: stone retaining wall (road -> plot) + 9" solid boundary wall 4'-0" above the plot, coping on top
    H = FRONT_WALL_H
    for a_, b_ in ((0.0, g0), (g1, 56.625), (68.625, 87.9167)):
        ax.add_patch(MPoly([(a_, rr(a_)), (b_, rr(b_)), (b_, 0), (a_, 0)], fc='#cfc6b4', ec=INK, lw=.7, zorder=6))
        ax.add_patch(MPoly([(a_, 0), (b_, 0), (b_, H), (a_, H)], fc='#ece6da', ec=INK, lw=.7, zorder=6, alpha=.96))
        ax.add_patch(MPoly([(a_ - .05, H), (b_ + .05, H), (b_ + .05, H + .25), (a_ - .05, H + .25)], fc='#a8a29e', ec=INK, lw=.5, zorder=6))
    # gate pillar (west jamb) and the 11'-3" sliding car gate, shown OPEN (parked in the wall pocket, dashed)
    ax.add_patch(MPoly([(56.625, rr(56.625)), (57.375, rr(57.375)), (57.375, H + .5), (56.625, H + .5)], fc='#cfc6b4', ec=INK, lw=.7, zorder=6))
    gz = GATE_BOTTOM_Z - PLOT_Z
    ax.add_patch(MPoly([(GATE_POCKET_X[0] + .3, gz), (GATE_POCKET_X[1] - .3, gz), (GATE_POCKET_X[1] - .3, H), (GATE_POCKET_X[0] + .3, H)],
                       fc='none', ec=INK, lw=.6, ls=(0, (4, 2)), zorder=7))
    ax.plot([57.375, 68.625], [gz, gz], c=INK, lw=.6, ls=(0, (4, 2)), zorder=7)
    ax.text((GATE_POCKET_X[0] + GATE_POCKET_X[1]) / 2, H - 1.2, f'SLIDING GATE 11\'-3" x {fmt(H - gz)} PARKED IN WALL POCKET', fontsize=3.6, ha='center', zorder=7)
    ax.annotate('', xy=(58.5, H - 1.0), xytext=(67.5, H - 1.0), arrowprops=dict(arrowstyle='->', lw=.6), zorder=7)
    ax.text(63.0, H - 0.7, 'CLOSES', fontsize=3.6, ha='center', zorder=7)
    # pedestrian gate (slatted, road -> wall top) with 4 steps up into the lawn behind it
    ax.add_patch(MPoly([(g0, rr(g0)), (g1, rr(g1)), (g1, H), (g0, H)], fc='#5b4a3d', ec=INK, lw=.8, zorder=6))
    zz = rr(g0) + 1.0
    while zz < H - .5:
        ax.plot([g0 + .35, g1 - .35], [zz, zz], c='#e7e2d6', lw=.6, zorder=7); zz += .42
    ax.text((g0 + g1) / 2, H + .6, 'PEDESTRIAN GATE 3\'-6"', fontsize=3.6, ha='center', zorder=7)
    ax.text(15.5, H + .6, 'STONE RETAINING WALL + 9" BOUNDARY WALL 4\'-0" ABOVE PLOT', ha='center', fontsize=4.0, color='#57534e', zorder=7)
    ax.text(83.0, rr(83) + .5, f'RETAINING {fmt(-rr(69))} TO {fmt(-rr(87.9))}', ha='center', fontsize=4.0, color='#57534e', zorder=6)
    for x in range(1, 31, 3):
        ax.add_patch(MPoly([(x, 0), (x + .8, 2.2 + (x % 5) * .25), (x + 1.6, 0)], closed=True, fc='#c6e7c9', ec='#2f855a', lw=.3, zorder=2))
    # plinth
    for a_, b_ in ((LINE_B, 57.375), (68.625, EAST_FACE)):
        R_(ax, a_, 0, b_, PL, fc='#d6d3cd', ec=INK, lw=.8, zorder=2)
    # facade blocks: bed-2 wing (stone), bath strip (plaster), porch void, drawing wing (stone)
    R_(ax, LINE_B, PL, 51.375, TOP - .5, fc='#efe7da', ec=INK, lw=1.0, zorder=2)
    R_(ax, 51.375, PL, 57.375, TOP - .5, fc='#f8f8f6', ec=INK, lw=1.0, zorder=2)
    R_(ax, 68.625, PL, EAST_FACE, TOP - .5, fc='#efe7da', ec=INK, lw=1.0, zorder=2)
    for (a_, b_) in ((LINE_B, 51.375), (68.625, EAST_FACE)):
        y = PL + 1.0
        while y < TOP - .6:
            ax.plot([a_, b_], [y, y], c='#cbbfa9', lw=.3, zorder=2.5); y += 1.0
    # porch: shadow void down to the road, single 1:5 ramp, 2'-0" landing, main door beyond
    ax.add_patch(MPoly([(57.375, rr(57.375)), (68.625, rr(68.625)), (68.625, TOP - 1.25), (57.375, TOP - 1.25)], fc='#4b5563', ec='none', zorder=2))
    rt = RAMP_TOP_Z - PLOT_Z
    ax.add_patch(MPoly([(57.375, rr(57.375)), (68.625, rr(68.625)), (68.625, rt), (57.375, rt)], fc='#9ca3af', ec=INK, lw=.4, zorder=2.2))
    for k in range(1, 8):
        z = rr(63) + (rt - rr(63)) * k / 8
        ax.plot([57.375, 68.625], [z, z], c='#b8bec7', lw=.3, zorder=2.3)
    R_(ax, 57.375, rt, 68.625, rt + PORCH_RISER, fc='#e5e7eb', ec=INK, lw=.4, zorder=2.3)
    R_(ax, 57.375, rt + PORCH_RISER, 68.625, PL, fc='#d1d5db', ec=INK, lw=.4, zorder=2.3)
    ax.text(62.75, (rr(63) + rt) / 2, f'RAMP 1:{1/RAMP_SLOPE:.1f} + 2 RISERS TO LANDING AT DOOR', fontsize=3.8, ha='center', va='center', zorder=3)
    R_(ax, 60.0, PL, 66.0, PL + 7.0, fc='#7a4a24', ec='#d1d5db', lw=.5, zorder=2.5)   # main door beyond (6'-0" double)
    ax.plot([63.0, 63.0], [PL, PL + 7.0], c='#d1d5db', lw=.5, zorder=2.6)
    R_(ax, 57.875, PL + 1.0, 59.375, PL + 7.0, fc='#a9cbe6', ec='#d1d5db', lw=.5, zorder=2.5)  # W9 beyond
    R_(ax, 66.625, PL + 1.0, 68.125, PL + 7.0, fc='#a9cbe6', ec='#d1d5db', lw=.5, zorder=2.5)  # W10 beyond
    R_(ax, 65.5, PL + 5.75, 68.25, PL + 6.75, fc='#9ca3af', ec='#d1d5db', lw=.4, zorder=2.5)  # powder vent beyond
    ax.text(62.75, PL + 8.0, 'MAIN DOOR 6\'-0" + W9 / W10 (BEYOND)', color='white', fontsize=4, ha='center', zorder=3)
    R_(ax, 56.625, PL, 57.375, TOP - .5, fc='#e5e7eb', ec=INK, lw=.8, zorder=3)     # column C'1
    R_(ax, 68.625, PL, 69.375, TOP - .5, fc='#e5e7eb', ec=INK, lw=.8, zorder=3)     # column D1
    R_(ax, 56.625, TOP - 1.25, 69.375, TOP - .5, fc='#e5e7eb', ec=INK, lw=.8, zorder=3)  # porch beam
    # GF roof slab band (projects 6" as drip band)
    R_(ax, LINE_B - .25, TOP - .5, EAST_FACE + .25, TOP, fc='#d1d5db', ec=INK, lw=1.0, zorder=3)
    # openings
    for w in WINDOWS:
        (x0, y0), (x1, y1) = w['p0'], w['p1']
        if abs(y0 - GRID_Y['1']) < 1e-6 and abs(y1 - y0) < 1e-6:
            window(ax, min(x0, x1), max(x0, x1), w['sill'], w['head'], w['kind'])
            ax.text((x0 + x1) / 2, PL + w['sill'] - .9, w['id'], ha='center', fontsize=5, color='#2b6cb0')
    # levels
    for lv, t in ((rr(EAST_FACE), f'ROAD AT EAST EDGE  {fmt(road_z(EAST_FACE))}'), (rr(0), 'PLOT / LAWN = ROAD AT P1  +/-0\'-0"'),
                  (PL, f'GF FFL  +{fmt(FFL)}'), (PL + CEIL, f'GF CEILING  +{fmt(FFL+CEIL)}'), (TOP, f'FF FFL  +{fmt(FFL+FF_TO_FF)}')):
        ax.plot([EAST_FACE + 1, EAST_FACE + 7], [lv, lv], c=INK, lw=.4)
        ax.add_patch(MPoly([(EAST_FACE + 1.6, lv), (EAST_FACE + 2.1, lv + .5), (EAST_FACE + 1.1, lv + .5)], fc=INK))
        ax.text(EAST_FACE + 2.5, lv + .2, t, fontsize=4.6)
    # window head/sill dims
    def vd(x, a, b, txt):
        ax.plot([x, x], [a, b], c=INK, lw=.35)
        for y in (a, b): ax.plot([x - .3, x + .3], [y - .3, y + .3], c=INK, lw=.5)
        ax.text(x - .3, (a + b) / 2, txt, rotation=90, ha='right', va='center', fontsize=4.3)
    vd(39.0, PL, PL + 2.5, 'SILL 2\'-6"'); vd(39.0, PL + 2.5, PL + 7.0, '4\'-6"'); vd(39.0, PL + 7.0, PL + 10.5, '3\'-6"')
    vd(37.3, 0, TOP, f'{fmt(TOP)}')
    vd(86.6, rr(86.6), 0, 'FILL')
    # horizontal dims along base
    def hd(a, b, y, txt=None):
        ax.plot([a, b], [y, y], c=INK, lw=.35)
        for x in (a, b): ax.plot([x - .3, x + .3], [y - .3, y + .3], c=INK, lw=.5)
        ax.text((a + b) / 2, y + .25, txt or fmt(b - a), ha='center', fontsize=4.3)
    Y0 = -7.6
    hd(LINE_B, 40.25, Y0); hd(40.25, 47.25, Y0); hd(47.25, 53.0, Y0); hd(53.0, 55.0, Y0)
    hd(55.0, 57.375, Y0); hd(57.375, 68.625, Y0); hd(68.625, 73.375, Y0); hd(73.375, 80.375, Y0); hd(80.375, EAST_FACE, Y0)
    hd(LINE_B, EAST_FACE, Y0 - 1.6, "BUILDING FRONTAGE 49'-0\"")
    # material notes
    notes = [(43.75, 'BED ROOM-2\nSTONE CLADDING'), (54.0, 'BATH\nPLASTER'), (76.9, 'DRAWING ROOM\nSTONE CLADDING')]
    for x, t in notes:
        ax.text(x, PL + 9.0, t, ha='center', fontsize=4.2, color='#57534e', zorder=6)
    ax.text(LINE_B, TOP + 3.5, 'SOUTH (ROAD-SIDE) ELEVATION - GROUND FLOOR', fontsize=11, weight='bold')
    ax.set_xlim(-4, 98); ax.set_ylim(-10.5, TOP + 6)

def draw_stair_section(ax):
    """Section A-A along flight-1, LOOKING EAST: north on the left, south (entrance) on the right.
    Horizontal coordinate h = 56 - Y."""
    ax.set_aspect('equal'); ax.axis('off')
    m = lambda y: 56.0 - y
    ax.plot([m(38), m(18)], [0, 0], c=INK, lw=1.2)                       # GF FFL
    R_(ax, m(38), CEIL, m(29.32), FF_TO_FF, fc='#d1d5db', ec=INK, lw=.6)  # FF slab north of the stair void
    R_(ax, m(20.5), CEIL, m(18.0), FF_TO_FF, fc='#d1d5db', ec=INK, lw=.6) # FF slab / porch roof south of front wall
    # flight-1 profile (cut), waist slab underneath -> open below
    pts = [(m(F1_BOT_Y), 0)]
    for i in range(F1_RISERS - 1):
        y = F1_BOT_Y - i * TREAD
        h = (i + 1) * RISER / 12
        pts += [(m(y), h), (m(y - TREAD), h)]
    pts += [(m(24.0), LANDING_H), (m(LANDING.bounds[1]), LANDING_H), (m(LANDING.bounds[1]), LANDING_H - 5 / 12),
            (m(24.0), LANDING_H - 5 / 12), (m(F1_BOT_Y) - 0.0, -0.0)]
    pts[-1] = (m(F1_BOT_Y - .55), 0)
    # waist slab: underside line from foot to landing
    ax.add_patch(MPoly(pts, closed=True, fc='#e5e7eb', ec=INK, lw=.7, zorder=3))
    # flight-2 (behind the cut) dashed
    if STAIR_VERSION == 'L':
        for j in range(F2_RISERS):
            h = LANDING_H + (j + 1) * RISER / 12
            ax.plot([m(20.5), m(24.0)], [h, h], c='#6b7280', lw=.4, ls='--')
        ax.text(m(24.0) + .2, FF_TO_FF - .3, 'FLIGHT-2 RISES WEST\n(BEHIND THE CUT)', fontsize=3.8, color='#6b7280', va='top', ha='right')
    else:
        pf = [(m(24.0), LANDING_H)]
        for j in range(F2_RISERS - 1):
            h = LANDING_H + (j + 1) * RISER / 12
            pf += [(m(24.0 + j * TREAD), h), (m(24.0 + (j + 1) * TREAD), h)]
        pf += [(m(F2_END_Y), FF_TO_FF)]
        ax.plot([p[0] for p in pf], [p[1] for p in pf], c='#6b7280', lw=.6, ls='--')
        ax.text(m(28.5), FF_TO_FF + .3, 'FLIGHT-2 RETURNS NORTH (BEHIND THE CUT)', fontsize=3.8, color='#6b7280', ha='center')
    # guest lobby under the landing
    R_(ax, m(24.0), 0, m(20.5), LANDING_H - 5 / 12, fc='#eaf4fb', ec='none', zorder=0)
    ax.text(m(22.25), 3.3, 'GUEST LOBBY\nUNDER LANDING', ha='center', fontsize=4.6, weight='bold')
    ax.text(m(22.25), 1.4, 'to drawing D8\n& washroom D9', ha='center', fontsize=3.8, color='#374151')
    # front wall with sidelight W10 (cut)
    R_(ax, m(20.5), 0, m(19.75), CEIL, fc='#3a3a3a', ec=INK)
    R_(ax, m(20.5), 1.0, m(19.75), 7.0, fc='white', ec=INK, lw=.4)
    ax.text(m(19.75) + .2, 4.0, 'W10\nSIDE-\nLIGHT', fontsize=3.6, va='center')
    ax.text(m(18.6), 0.4, 'PORCH', fontsize=4, ha='center', color='#6b7280')
    # dims
    def vd(x, a, b, txt):
        ax.plot([x, x], [a, b], c=INK, lw=.35)
        for y in (a, b): ax.plot([x - .25, x + .25], [y - .25, y + .25], c=INK, lw=.5)
        ax.text(x - .25, (a + b) / 2, txt, rotation=90, ha='right', va='center', fontsize=4.3)
    vd(m(36.0), 0, LANDING_H, f'FLIGHT-1: 13R = {fmt(LANDING_H)}')
    vd(m(37.3), LANDING_H, FF_TO_FF, f'FLIGHT-2: 6R = {fmt(FF_TO_FF-LANDING_H)}')
    vd(m(24.6), 0, LANDING_H - 5/12, f'CLEAR {fmt(LANDING_H-5/12)}')
    ax.plot([m(F1_BOT_Y), m(20.5)], [-1.2, -1.2], c=INK, lw=.35)
    ax.text(m((F1_BOT_Y + 20.5) / 2), -1.0, f"12 TREADS @ 10\" = 10'-0\"   +   LANDING 3'-6\"", ha='center', fontsize=4.3)
    ax.text(m(31.0), CEIL - .35, 'FF SLAB STARTS NORTH\nOF Y=29\'-4" (HEADROOM)', fontsize=3.8, va='top', ha='center')
    ax.text(m(38), FF_TO_FF + 2.2, f'SECTION A-A : STAIR ({STAIR_VERSION}-TYPE) + GUEST LOBBY   -   LOOKING EAST', fontsize=8.5, weight='bold')
    ax.text(m(38), FF_TO_FF + 1.0, f'NORTH (LOUNGE) <-  ->  SOUTH (ENTRANCE)   |   19 RISERS @ {RISER:.2f}"  TREAD 10"  WIDTH 3\'-6"', fontsize=5)
    ax.set_xlim(16, 40); ax.set_ylim(-3, FF_TO_FF + 4)

if __name__ == '__main__':
    fig = plt.figure(figsize=(16.5, 11.7))
    a1 = fig.add_axes([0.02, 0.38, 0.96, 0.6]); draw_south_elevation(a1)
    a2 = fig.add_axes([0.25, 0.02, 0.5, 0.36]); draw_stair_section(a2)
    fig.savefig('preview_elev.png', dpi=150)
