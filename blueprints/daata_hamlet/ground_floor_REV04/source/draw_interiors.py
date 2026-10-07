"""True-orientation interior elevations of the entrance / stair / guest lobby.
B-B: standing in the foyer, LOOKING SOUTH at the entrance (west on the RIGHT, as you actually see it).
C-C: standing in the foyer, LOOKING EAST into the guest lobby (north on the LEFT)."""
import math
from matplotlib.patches import Rectangle, Polygon as MPoly
from model import *

INK = '#1b1b1b'

def R_(ax, x0, y0, x1, y1, **kw):
    ax.add_patch(Rectangle((min(x0, x1), y0), abs(x1 - x0), y1 - y0, **kw))

def _vd(ax, x, a, b, txt, side=1):
    ax.plot([x, x], [a, b], c=INK, lw=.35)
    for y in (a, b): ax.plot([x - .2, x + .2], [y - .2, y + .2], c=INK, lw=.5)
    ax.text(x + .25 * side, (a + b) / 2, txt, rotation=90, ha='left' if side > 0 else 'right', va='center', fontsize=4.2)

def _hd(ax, a, b, y, txt):
    ax.plot([a, b], [y, y], c=INK, lw=.35)
    for x in (a, b): ax.plot([x - .2, x + .2], [y - .2, y + .2], c=INK, lw=.5)
    ax.text((a + b) / 2, y + .15, txt, ha='center', fontsize=4.2)

def flight_profile(stations, base_h):
    """stepped profile + waist soffit; stations = list of (s0, s1, top_h) along the run (ascending)."""
    top = []
    for s0, s1, h in stations:
        top += [(s0, h - RISER / 12), (s0, h), (s1, h)]
    s_first, s_last = stations[0][0], stations[-1][1]
    h_first, h_last = stations[0][2] - RISER / 12, stations[-1][2]
    # waist slab underside parallel to the pitch line, 0.75' below the nosings
    soffit = [(s_last, h_last - 0.75), (s_first, h_first - 0.75)]
    return top + soffit

def elev_looking_south(ax):
    ax.set_aspect('equal'); ax.axis('off')
    m = lambda x: 80.0 - x               # west on the right
    x_w, x_e = 50.0, 76.0
    # floor, ceiling slab with stair void
    ax.plot([m(x_w), m(x_e)], [0, 0], c=INK, lw=1.2)
    void = (F2_END_X, 68.625) if STAIR_VERSION == 'L' else (61.625, 68.625)
    for a, b in ((x_w, void[0]), (void[1], x_e)):
        R_(ax, m(a), CEIL, m(b), FF_TO_FF, fc='#d1d5db', ec=INK, lw=.6)
    # back wall = inside face of the front wall (Y 20.5), with its openings
    R_(ax, m(x_w), 0, m(x_e), CEIL, fc='#f3f1ec', ec='none', zorder=0)
    def opening(x0, x1, z0, z1, fc, label=None):
        R_(ax, m(x0), z0, m(x1), z1, fc=fc, ec=INK, lw=.6, zorder=1)
        if label: ax.text(m((x0 + x1) / 2), z1 + .25, label, ha='center', fontsize=4.0, zorder=6)
    opening(57.875, 59.375, 1.0, 7.0, '#cfe3f3', 'W9')
    opening(66.625, 68.125, 1.0, 7.0, '#cfe3f3', 'W10')
    opening(60.0, 66.0, 0.0, 7.0, '#9ca3af', 'D1  MAIN DOOR 6\'-0" (2 LEAVES OPEN OUT)')
    for x in (60.0, 66.0):                                   # leaves open out -> seen edge-on in the porch
        R_(ax, m(x) - .08, 0, m(x) + .08, 7.0, fc='#7a4a24', ec=INK, lw=.3, zorder=2)
    ax.text(m(63.0), 2.0, 'CAR PORCH\n(BEYOND)', ha='center', fontsize=4.2, color='white', zorder=3)
    opening(69.875, 73.375, 0.0, 7.0, '#efe7da', 'D10 POCKET SLIDING 3\'-6"')
    ax.text(m(71.6), 3.0, 'DRAWING\nROOM', ha='center', fontsize=4.2, color='#57534e', zorder=3)
    # lobby east wall cut (X 74.25-74.625) with washroom door D11 (cut through the opening)
    R_(ax, m(74.25), 7.0, m(74.625), CEIL, fc='#3a3a3a', ec=INK, lw=.4, zorder=4)
    ax.text(m(75.3), 3.5, 'D11\nGUEST\nWASH-\nROOM', ha='center', fontsize=4.0, zorder=4)
    # grid-D wall cut: lobby door D8 (3'-6") closes the lobby; wall above the door head
    R_(ax, m(68.625), 7.0, m(69.375), CEIL, fc='#3a3a3a', ec=INK, lw=.4, zorder=4)
    ax.text(m(69.0), 7.6, 'D8', ha='center', fontsize=4.2, color='white', zorder=6)
    # stair: landing slab cut, flight-2
    lx0, lx1 = LANDING.bounds[0], LANDING.bounds[2]
    R_(ax, m(lx0), LANDING_H - 5 / 12, m(lx1), LANDING_H, fc='#bdb6aa', ec=INK, lw=.7, zorder=5)
    ax.plot([m(lx0), m(lx1)], [LANDING_H + 3.0, LANDING_H + 3.0], c='#2b6cb0', lw=.6, zorder=5)
    if STAIR_VERSION == 'L':
        st = [(m(65.125 - j * TREAD), m(65.125 - (j + 1) * TREAD), (F1_RISERS + j + 1) * RISER / 12) for j in range(F2_RISERS - 1)]
        st = [(a, b, h) for a, b, h in st]
        pts = flight_profile([(a, b, h) for a, b, h in st], 0)
        pts = [(m(65.125), LANDING_H - 5 / 12)] + pts[:-2] + [(m(F2_END_X), FF_TO_FF), (m(F2_END_X), FF_TO_FF - 0.75), (m(65.125), LANDING_H - 0.75)]
        ax.add_patch(MPoly(pts, closed=True, fc='#bdb6aa', ec=INK, lw=.7, zorder=5))
        ax.text(m(63.0), LANDING_H + 2.2, 'FLIGHT-2 (CUT) 6R UP WEST', ha='center', fontsize=4.2, zorder=6)
    else:
        ax.text(m(63.0), LANDING_H + 0.5, 'FLIGHT-2 RETURNS NORTH (BEHIND YOU)', ha='center', fontsize=4.0, zorder=6)
    ax.text(m(lx0 + 1.75 if STAIR_VERSION == 'L' else 65.0), LANDING_H + .25, f'LANDING +{fmt(LANDING_H)}', ha='center', fontsize=4.2, zorder=6)
    # labels
    ax.text(m(64.5), 8.2, 'FOYER (UNDER LANDING)', ha='center', fontsize=5, weight='bold', zorder=6)
    ax.text(m(71.5), 8.2, 'GUEST LOBBY', ha='center', fontsize=5, weight='bold', zorder=6)
    ax.text(m(54.0), 8.2, 'LOUNGE / PASSAGE ->', ha='center', fontsize=5, weight='bold', zorder=6)
    # dims
    _hd(ax, m(60.0), m(66.0), -1.0, '6\'-0" CENTRED ON PORCH')
    _hd(ax, m(57.875), m(59.375), -1.0, '1\'-6"'); _hd(ax, m(66.625), m(68.125), -1.0, '1\'-6"')
    _hd(ax, m(69.875), m(73.375), -1.0, '3\'-6"')
    _vd(ax, m(x_e) - .6, 0, 7.0, 'DOOR HEAD 7\'-0"', -1)
    _vd(ax, m(65.6), 0, LANDING_H - 5 / 12, f'CLEAR UNDER LANDING {fmt(LANDING_H - 5/12)}')
    _vd(ax, m(x_w) + .6, 0, CEIL, 'CEILING 10\'-6"')
    ax.text(m(x_w), FF_TO_FF + 2.4, f'INTERIOR ELEVATION B-B ({STAIR_VERSION}-STAIR) : FROM THE FOYER LOOKING SOUTH', fontsize=8.5, weight='bold', ha='right')
    ax.text(m(x_w), FF_TO_FF + 1.2, 'TRUE VIEW - EAST (DRAWING / LOBBY) ON YOUR LEFT, WEST (PASSAGE) ON YOUR RIGHT', fontsize=5, ha='right')
    ax.set_xlim(m(x_e) - 1.5, m(x_w) + 1.5); ax.set_ylim(-2.2, FF_TO_FF + 3.2)

def elev_looking_east(ax):
    ax.set_aspect('equal'); ax.axis('off')
    m = lambda y: 60.0 - y               # north on the left
    y_n, y_s = 35.5, 18.5
    cut_x = 64.5
    ax.plot([m(y_n), m(y_s)], [0, 0], c=INK, lw=1.2)
    R_(ax, m(y_n), CEIL, m(29.32), FF_TO_FF, fc='#d1d5db', ec=INK, lw=.6)
    R_(ax, m(20.5), CEIL, m(y_s), FF_TO_FF, fc='#d1d5db', ec=INK, lw=.6)
    # back plane: D wall face (X 68.625) north of the lobby, lobby end wall (X 74.25) through the gap
    R_(ax, m(y_n), 0, m(24.375), CEIL, fc='#f3f1ec', ec='none', zorder=0)
    R_(ax, m(24.0), 0, m(20.5), CEIL, fc='#e9e4da', ec='none', zorder=0)
    R_(ax, m(24.0), LANDING_H - 5 / 12, m(20.5), CEIL, fc='#f3f1ec', ec='none', zorder=0.5)
    # door D8 on grid D closes the lobby: frame 3'-6" x 7'-0", leaf parked open against the stair side
    R_(ax, m(24.0), 7.0, m(20.5), LANDING_H - 5 / 12, fc='#f3f1ec', ec=INK, lw=.4, zorder=0.6)
    ax.plot([m(24.0), m(24.0), m(20.5), m(20.5)], [0, 7.0, 7.0, 0], c=INK, lw=.9, zorder=2)
    ax.text(m(22.25), 7.25, 'D8 LOBBY DOOR 3\'-6" x 7\'-0"', ha='center', fontsize=3.8, zorder=6)
    ax.text(m(22.25), 6.0, 'GUEST LOBBY', ha='center', fontsize=5, weight='bold', zorder=6)
    R_(ax, m(22.75), 0, m(20.75), 7.0, fc='#cbd5e1', ec=INK, lw=.6, zorder=1)
    ax.text(m(21.75), 3.5, 'D11\nGUEST\nWASH-\nROOM\n2\'-0"', ha='center', va='center', fontsize=3.8, zorder=2)
    R_(ax, m(24.0) - .08, 0, m(24.0) + .08, 7.0, fc='#7a4a24', ec=INK, lw=.3, zorder=2)
    ax.text(m(23.6), .5, 'D12 STORE\n(SIDE)', fontsize=3.4, ha='left', zorder=3)
    ax.text(m(20.9), 1.0, 'D10 DRAWING\n(SIDE WALL)', fontsize=3.4, ha='center', zorder=3)
    # flight-1 seen from the side (beyond the cut) with open soffit
    st = [(m(F1_BOT_Y - i * TREAD), m(F1_BOT_Y - (i + 1) * TREAD), (i + 1) * RISER / 12) for i in range(F1_RISERS - 1)]
    pts = flight_profile(st, 0)
    pts = [(m(F1_BOT_Y), 0)] + pts[:-2] + [(m(24.0), LANDING_H), (m(24.0), LANDING_H - 5 / 12), (m(F1_BOT_Y - 0.6), 0)]
    ax.add_patch(MPoly(pts, closed=True, fc='#e5e7eb', ec=INK, lw=.7, zorder=3))
    ax.text(m(29.5), 1.0, 'UNDER-STAIR - OPEN\n(TO LOUNGE & FOYER)', ha='center', fontsize=3.8, zorder=4)
    # landing + flight-2 at the cut
    lb = LANDING.bounds
    if STAIR_VERSION == 'L':
        R_(ax, m(24.0), LANDING_H - 5 / 12, m(20.5), LANDING_H, fc='#e5e7eb', ec=INK, lw=.6, zorder=4)
        j = int((65.125 - cut_x) // TREAD); h = (F1_RISERS + j + 1) * RISER / 12
        R_(ax, m(24.0), h - 0.75, m(20.5), h, fc='#bdb6aa', ec=INK, lw=.7, zorder=5)
        ax.text(m(22.25), h + .25, 'FLIGHT-2 (CUT) RISING WEST', ha='center', fontsize=3.8, zorder=6)
    else:
        R_(ax, m(24.0), LANDING_H - 5 / 12, m(20.5), LANDING_H, fc='#bdb6aa', ec=INK, lw=.7, zorder=5)
        st2 = [(m(24.0 + j * TREAD), m(24.0 + (j + 1) * TREAD), (F1_RISERS + j + 1) * RISER / 12) for j in range(F2_RISERS - 1)]
        p2 = flight_profile(st2, 0)
        p2 = [(m(24.0), LANDING_H - 5 / 12)] + p2[:-2] + [(m(F2_END_Y), FF_TO_FF), (m(F2_END_Y), FF_TO_FF - .75), (m(24.0), LANDING_H - .75)]
        ax.add_patch(MPoly(p2, closed=True, fc='#bdb6aa', ec=INK, lw=.7, zorder=5))
        ax.text(m(26.2), FF_TO_FF + .3, 'FLIGHT-2 (CUT) RETURNS NORTH', ha='center', fontsize=3.8, zorder=6)
    # front wall cut with the main door
    R_(ax, m(20.5), 7.0, m(19.75), CEIL, fc='#3a3a3a', ec=INK, lw=.4, zorder=4)
    R_(ax, m(19.75), -.05, m(19.75) + .1, 7.0, fc='#7a4a24', ec='none', zorder=4)
    ax.text(m(19.1), 3.5, 'D1\nMAIN\nDOOR', ha='center', fontsize=4.0, zorder=4)
    _vd(ax, m(24.8), 0, LANDING_H - 5 / 12, f'CLEAR {fmt(LANDING_H - 5/12)}', -1)
    _vd(ax, m(y_n) + .6, 0, LANDING_H, f'LANDING +{fmt(LANDING_H)}')
    ax.text(m(y_n), FF_TO_FF + 2.4, f'INTERIOR ELEVATION C-C ({STAIR_VERSION}-STAIR) : FROM THE FOYER LOOKING EAST INTO THE GUEST LOBBY', fontsize=8.5, weight='bold')
    ax.text(m(y_n), FF_TO_FF + 1.2, 'NORTH (LOUNGE) ON YOUR LEFT, SOUTH (ENTRANCE) ON YOUR RIGHT', fontsize=5)
    ax.set_xlim(m(y_n) - 1.0, m(y_s) + 1.0); ax.set_ylim(-1.5, FF_TO_FF + 3.2)

if __name__ == '__main__':
    import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
    fig = plt.figure(figsize=(14, 10))
    a1 = fig.add_axes([0.03, 0.52, 0.94, 0.46]); elev_looking_south(a1)
    a2 = fig.add_axes([0.03, 0.02, 0.6, 0.46]); elev_looking_east(a2)
    fig.savefig(f'interiors_{STAIR_VERSION}.png', dpi=110)
