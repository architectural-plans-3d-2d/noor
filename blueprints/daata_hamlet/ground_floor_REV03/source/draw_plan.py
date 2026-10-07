"""Ground floor plan drawing (matplotlib) - used for preview and the PDF sheet."""
import math
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon as MPoly, Arc, Circle, Rectangle
from shapely.geometry import box, LineString, Polygon
from model import *

INK = '#1b1b1b'; RED = '#c0392b'; GRID = '#9aa5b1'; BLUE = '#2b6cb0'; GREEN = '#2f855a'
FILL = {'wood': '#f6efe3', 'tile': '#f3f4f6', 'paver': '#eceae4', 'open': '#e6f2fb'}

def polys(g):
    return getattr(g, 'geoms', [g])

def draw_poly(ax, g, **kw):
    from matplotlib.path import Path
    from matplotlib.patches import PathPatch
    import numpy as np
    for p in polys(g):
        if p.is_empty: continue
        verts, codes = [], []
        for ring in [p.exterior] + list(p.interiors):
            c = list(ring.coords)
            verts += c; codes += [Path.MOVETO] + [Path.LINETO] * (len(c) - 2) + [Path.CLOSEPOLY]
        ax.add_patch(PathPatch(Path(np.array(verts), codes), **kw))

def opening_rect(o):
    return seg_rect(o['p0'], o['p1'], o['t'])

def door_geom(d):
    """returns hinge, leaf tip, length, arc angles and swing sector (empty for sliding doors)"""
    (x0, y0), (x1, y1) = d['p0'], d['p1']
    L = math.hypot(x1 - x0, y1 - y0)
    ux, uy = (x1 - x0) / L, (y1 - y0) / L
    nx, ny = -uy * d['side'], ux * d['side']
    hx, hy = x0 + nx * d['t'] / 2, y0 + ny * d['t'] / 2
    if d.get('kind', 'swing') in ('pocket', 'slide'):
        return (hx, hy), (hx, hy), L, 0, 0, Polygon()
    tip = (hx + nx * L, hy + ny * L)
    a0 = math.degrees(math.atan2(uy, ux)); a1 = math.degrees(math.atan2(ny, nx))
    pts = [(hx, hy)]
    da = ((a1 - a0 + 540) % 360) - 180
    for k in range(21):
        a = math.radians(a0 + da * k / 20)
        pts.append((hx + L * math.cos(a), hy + L * math.sin(a)))
    return (hx, hy), tip, L, min(a0, a0 + da), max(a0, a0 + da), Polygon(pts)

def dim_h(ax, x0, x1, y, txt=None, off=0, fs=5.5, c=INK):
    ax.plot([x0, x1], [y, y], c=c, lw=0.4)
    for x in (x0, x1):
        ax.plot([x - .35, x + .35], [y - .35, y + .35], c=c, lw=0.6)
        ax.plot([x, x], [y - .6, y + .6], c=c, lw=0.3)
    ax.text((x0 + x1) / 2, y + .35 + off, txt or fmt(x1 - x0), ha='center', va='bottom', fontsize=fs, color=c)

def dim_al(ax, a, b, off, txt=None, fs=4.6, c=INK):
    (x0, y0), (x1, y1) = a, b
    L = math.hypot(x1 - x0, y1 - y0); ux, uy = (x1 - x0) / L, (y1 - y0) / L; nx, ny = -uy, ux
    A = (x0 + nx * off, y0 + ny * off); B = (x1 + nx * off, y1 + ny * off)
    ax.plot([A[0], B[0]], [A[1], B[1]], c=c, lw=.4, zorder=7)
    for (px, py), (qx, qy) in ((a, A), (b, B)):
        ax.plot([px, qx + nx * .3 * (1 if off > 0 else -1)], [py, qy + ny * .3 * (1 if off > 0 else -1)], c=c, lw=.3, zorder=7)
        ax.plot([qx - .3 * (ux + nx), qx + .3 * (ux + nx)], [qy - .3 * (uy + ny), qy + .3 * (uy + ny)], c=c, lw=.6, zorder=7)
    ang = math.degrees(math.atan2(uy, ux))
    ax.text((A[0] + B[0]) / 2 + nx * .45 * (1 if off > 0 else -1), (A[1] + B[1]) / 2 + ny * .45 * (1 if off > 0 else -1), txt or fmt(L),
            rotation=ang, ha='center', va='center', fontsize=fs, color=c, zorder=7, bbox=dict(boxstyle='square,pad=0.05', fc='white', ec='none'))

def dim_v(ax, y0, y1, x, txt=None, fs=5.5, c=INK):
    ax.plot([x, x], [y0, y1], c=c, lw=0.4)
    for y in (y0, y1):
        ax.plot([x - .35, x + .35], [y - .35, y + .35], c=c, lw=0.6)
        ax.plot([x - .6, x + .6], [y, y], c=c, lw=0.3)
    ax.text(x - .35, (y0 + y1) / 2, txt or fmt(y1 - y0), ha='right', va='center', rotation=90, fontsize=fs, color=c)

LABEL_POS = {'BED2': (43.75, 9.0), 'BATH2': (53.6, 8.0), 'DRS2': (53.0, 17.2), 'PASS': (43.5, 22.5),
             'KIT': (44.0, 26.0), 'DKIT': (45.5, 37.2), 'LNG': (61.6, 39.9), 'OTS': (61.0, 45.2),
             'PWD': (70.9, 24.4), 'DRSD': (75.4, 23.8), 'BATHD': (81.4, 23.9), 'DRAW': (77.0, 5.6),
             'BED1': (77.4, 39.0), 'DRS1': (72.9, 48.6), 'WR1': (80.8, 48.6), 'PORCH': (62.5, 6.0)}

def draw_ground_floor(ax, furniture=True, dims=True, title=True):
    ax.set_aspect('equal'); ax.axis('off')
    # plot / lawn
    ax.add_patch(MPoly(list(PLOT.exterior.coords), closed=True, fc='white', ec=RED, lw=1.1, ls='-', zorder=1))
    lawn = PLOT & box(-5, -5, LINE_B, 80)
    draw_poly(ax, lawn, fc='#e8f5e9', ec='none', zorder=1)
    draw_poly(ax, (PLOT & box(-5, -5, 100, 80)) - FOOTPRINT - lawn - R['PORCH']['geom'],
              fc='#f1f5f9', ec='none', zorder=1)
    ax.text(18, 6.5, 'MAIN LAWN', ha='center', fontsize=9, color=GREEN, weight='bold', zorder=5)
    ax.text(18, 4.9, f'{lawn.area:.0f} SQ.FT  -  OPEN TO SKY', ha='center', fontsize=5.5, color=GREEN, zorder=5)
    ax.plot([LINE_B, LINE_B], [-1.5, north_y(LINE_B) + 1.5], c=RED, lw=0.6, ls=(0, (6, 3)), zorder=2)
    ax.text(LINE_B - .4, -1.4, 'LINE B (X=36\'-1 1/2")', fontsize=4.5, color=RED, ha='right')
    # pegs
    for n, x, y in PEGS:
        ax.add_patch(Circle((x, y), .45, fc=RED, ec='white', lw=.5, zorder=6))
        ax.text(x + .6, y + .6, n, fontsize=5.5, color=RED, weight='bold', zorder=6)
    # grids
    for k, x in GRID_X.items():
        ax.plot([x, x], [-4.5, 63], c=GRID, lw=.35, ls=(0, (10, 3, 2, 3)), zorder=1.5)
        for yy in (-6.0, 64.6):
            ax.add_patch(Circle((x, yy), 1.1, fc='white', ec=INK, lw=.5, zorder=6))
            ax.text(x, yy, k, ha='center', va='center', fontsize=6, zorder=7)
    for k, y in GRID_Y.items():
        ax.plot([30 if y > 20 else 14, 93.5], [y, y], c=GRID, lw=.35, ls=(0, (10, 3, 2, 3)), zorder=1.5)
        ax.add_patch(Circle((95.2, y), 1.1, fc='white', ec=INK, lw=.5, zorder=6))
        ax.text(95.2, y, k, ha='center', va='center', fontsize=6, zorder=7)
    # room fills
    for k, r in R.items():
        fc = FILL['open'] if r['kind'] == 'open' and k == 'OTS' else FILL.get(r['finish'], '#f7f7f7')
        draw_poly(ax, r['geom'], fc=fc, ec='none', zorder=2)
    # porch: one ramp from the gate, 2 full-width risers, 2'-6" landing at the main door
    draw_poly(ax, PLATFORM, fc='#e7e2d6', ec=INK, lw=.6, zorder=2.6)
    draw_poly(ax, PORCH_TREAD, fc='white', ec=INK, lw=.6, zorder=2.6)
    ax.text(62.75, 17.4, f'ENTRANCE LANDING 3\'-6" DEEP  FFL +{fmt(FFL)}', fontsize=3.6, ha='center', va='center', zorder=7)
    ax.text(62.75, sum(TREAD_Y) / 2, f'2 RISERS @ 7 1/2"  UP', fontsize=3.2, ha='center', va='center', zorder=7)
    for yy in [i * 1.0 for i in range(1, 15)]:
        ax.plot([57.45, 58.0], [yy, yy], c='#9ca3af', lw=.3, zorder=2.7)
        ax.plot([68.05, 68.55], [yy, yy], c='#9ca3af', lw=.3, zorder=2.7)
    ax.annotate('', xy=(58.4, 15.0), xytext=(58.4, 1.0), arrowprops=dict(arrowstyle='->', lw=.6, color='#555'), zorder=7)
    ax.text(57.95, 8.5, f'RAMP 1:{1/RAMP_SLOPE:.1f} UP', fontsize=3.8, rotation=90, ha='center', va='center', color='#555', zorder=7)
    ax.annotate('', xy=(67.4, 15.0), xytext=(67.4, 1.0), arrowprops=dict(arrowstyle='->', lw=.6, color='#555'), zorder=7)
    ax.text(62.5, .45, f'GATE {fmt(GATE_Z)}', fontsize=3.4, color='#c0392b', ha='center', zorder=7)
    ax.text(62.5, 14.6, f'WHEEL-STOP  {fmt(RAMP_TOP_Z)}', fontsize=3.0, color='#c0392b', ha='center', zorder=7)
    # site levels
    for x, y, t in ((0.0, -1.0, 'ROAD +/-0\'-0" (DATUM)'), (87.9167, -1.0, 'ROAD -6\'-0"')):
        ax.text(x, y, t, fontsize=3.8, color='#c0392b', ha='center', va='top', zorder=7)
    ax.text(18, 3.5, f'LAWN / PLOT LEVEL +/-{fmt(PLOT_Z)} (= ROAD AT P1)', fontsize=4, color=GREEN, ha='center', zorder=7)
    # pedestrian gate + stone path to side door D5
    for st in STONES:
        draw_poly(ax, st, fc='#d6d3cd', ec='#78716c', lw=.4, zorder=2.5)
    for poly, z in PED_STEPS:
        draw_poly(ax, poly, fc='white', ec=INK, lw=.4, zorder=2.6)
    ax.text(33.0, 3.4, f'UP {PED_RISERS}R', fontsize=3.2, ha='center', zorder=7)
    ax.plot([PED_GATE[0], PED_GATE[1]], [0.19, 0.19], c='white', lw=2.2, zorder=6)
    ax.plot([PED_GATE[0], PED_GATE[1]], [0.19, 0.19], c=INK, lw=.5, ls=(0, (2, 1)), zorder=6.1)
    ax.text(PED_GATE[0] - .3, 1.0, 'PEDESTRIAN\nGATE 3\'-6"', fontsize=3.4, ha='right', va='center', color=INK, zorder=7)
    ax.text(31.6, 12.0, 'STEPPING STONES 1\'-6" x 1\'-0" @ 2\'-0"', fontsize=3.2, rotation=90, ha='center', va='center', color='#57534e', zorder=7)
    # car
    if furniture:
        draw_poly(ax, CAR, fc='none', ec='#8a8a8a', lw=.5, ls='--', zorder=3)
        ax.text(62.5, 11.0, 'CAR\nMAX 15\'-0" LONG', ha='center', fontsize=4.5, color='#8a8a8a', zorder=3)
    # walls & columns
    draw_poly(ax, WALLS, fc='#3a3a3a', ec=INK, lw=.4, zorder=4)
    for c in COLUMNS.values():
        draw_poly(ax, c, fc='black', ec='black', lw=.2, zorder=5)
    # openings: clear wall then draw symbols
    for o in WINDOWS + DOORS:
        draw_poly(ax, opening_rect(o), fc='white', ec='none', zorder=4.5)
    for w in WINDOWS:
        (x0, y0), (x1, y1) = w['p0'], w['p1']
        L = math.hypot(x1 - x0, y1 - y0); nx, ny = -(y1 - y0) / L, (x1 - x0) / L
        for s in (-w['t'] / 2, -w['t'] / 6, w['t'] / 6, w['t'] / 2):
            if w['kind'] == 'vent' and abs(s) < w['t'] / 3: continue
            ax.plot([x0 + nx * s, x1 + nx * s], [y0 + ny * s, y1 + ny * s], c=BLUE, lw=.5, zorder=5)
        mx, my = (x0 + x1) / 2, (y0 + y1) / 2
        tag = w['id']
        ax.text(mx + nx * 1.6 * (1 if w['id'] not in ('W7', 'W8', 'V2') else -1), my + ny * 1.6 * (1 if w['id'] not in ('W7', 'W8', 'V2') else -1),
                tag, fontsize=4.2, color=BLUE, ha='center', va='center', zorder=6)
    for d in DOORS:
        if d['kind'] in ('pocket', 'slide'):
            (x0, y0), (x1, y1) = d['p0'], d['p1']
            draw_poly(ax, seg_rect(d['p0'], d['p1'], 0.12), fc=INK, ec=INK, lw=.2, zorder=6)
            draw_poly(ax, slide_park(d), fc='none', ec=INK, lw=.4, ls='--', zorder=6)
            pk = slide_park(d).centroid; c = ((x0 + x1) / 2, (y0 + y1) / 2)
            ax.annotate('', xy=(pk.x, pk.y), xytext=c, arrowprops=dict(arrowstyle='->', lw=.5), zorder=7)
            ax.text(*_tagpos(d), d['id'], fontsize=4.2, color=INK, ha='center', va='center', zorder=6,
                    bbox=dict(boxstyle='round,pad=0.12', fc='white', ec='none'))
            continue
        (hx, hy), tip, L, a0, a1, sector = door_geom(d)
        ax.plot([hx, tip[0]], [hy, tip[1]], c=INK, lw=.7, zorder=6)
        ax.add_patch(Arc((hx, hy), 2 * L, 2 * L, theta1=a0, theta2=a1, color=INK, lw=.35, zorder=6))
        if not d['id'].endswith('b'):
            ax.text(*_tagpos(d), d['id'].rstrip('a'), fontsize=4.2, color=INK, ha='center', va='center', zorder=6,
                    bbox=dict(boxstyle='round,pad=0.12', fc='white', ec='none'))
    # stair
    for poly, h, fl in STAIR_TREADS:
        hidden = fl == 1 and poly.bounds[1] < 29.0   # beyond cut plane (4'-0") show dashed
        draw_poly(ax, poly, fc='white', ec=INK, lw=.35, ls='--' if hidden or fl == 2 else '-', zorder=5)
    # cut line
    ax.plot([65.125, 68.625], [29.2, 28.6], c=INK, lw=.6, zorder=6)
    ax.annotate('', xy=(66.875, 25.2), xytext=(66.875, 33.4),
                arrowprops=dict(arrowstyle='->', lw=.6, color=INK), zorder=7)
    ax.text(66.9, 33.55, 'UP', fontsize=4.5, ha='center', va='bottom', zorder=7)
    ax.text(66.875, 22.25, f'LANDING\n+{fmt(LANDING_H)}', fontsize=3.6, ha='center', va='center', zorder=7, color='#555')
    ax.text(63.0, 22.25, 'FLIGHT-2 OVER\n(6R UP TO +11\'-0")', fontsize=3.4, ha='center', va='center', zorder=7, color='#555')
    ax.text(64.6, 31.0, 'FLIGHT-1\n13R @ 6.95"\n10" TREAD', fontsize=3.4, ha='right', va='center', zorder=7, color='#555')
    # furniture
    if furniture:
        for name, g, kind in FURN:
            ec = '#6b7280' if kind == 'furniture' else '#4a5568'
            fc = 'none' if kind == 'furniture' else ('#e2e8f0' if kind == 'counter' else 'white')
            draw_poly(ax, g, fc=fc, ec=ec, lw=.35, zorder=5)
            if name == 'WARDROBE':
                x0_, y0_, x1_, y1_ = g.bounds
                edges = ([((x0_, y0_), (x0_, y1_)), ((x1_, y0_), (x1_, y1_))] if (y1_ - y0_) > (x1_ - x0_)
                         else [((x0_, y0_), (x1_, y0_)), ((x0_, y1_), (x1_, y1_))])
                fr = min(edges, key=lambda e: -LineString(e).distance(WALLS))
                (ax_, ay_), (bx_, by_) = fr
                mx_, my_ = (ax_ + bx_) / 2, (ay_ + by_) / 2
                ix, iy = (g.centroid.x - mx_), (g.centroid.y - my_); n_ = math.hypot(ix, iy); ix, iy = ix / n_, iy / n_
                for k_, off_ in enumerate((0.12, 0.27)):
                    if k_ == 0:
                        ax.plot([ax_ + ix * off_, mx_ + ix * off_ + (bx_ - ax_) * .05], [ay_ + iy * off_, my_ + iy * off_ + (by_ - ay_) * .05], c=INK, lw=.5, zorder=6)
                    else:
                        ax.plot([mx_ + ix * off_ - (bx_ - ax_) * .05, bx_ + ix * off_], [my_ + iy * off_ - (by_ - ay_) * .05, by_ + iy * off_], c=INK, lw=.5, zorder=6)
            if name not in ('SIDE', 'CHAIRS'):
                (x0, y0, x1, y1) = g.bounds
                ax.text((x0 + x1) / 2, (y0 + y1) / 2, name, fontsize=3.0, color='#6b7280', ha='center', va='center',
                        rotation=90 if (y1 - y0) > (x1 - x0) * 1.6 else 0, zorder=5)
    # room labels
    for k, r in R.items():
        x, y = LABEL_POS[k]
        g = r['geom']
        bx = g.bounds
        txt = r['name']
        if k in ('PORCH', 'OTS'):
            sub = f"{g.area:.0f} SQ.FT" if k != 'PORCH' else f'{fmt(bx[2]-bx[0])} CLEAR WIDTH'
        elif g.geom_type == 'Polygon' and len(g.exterior.coords) == 5 and k != 'PWD':
            sub = f"{fmt(bx[2]-bx[0])} x {fmt(bx[3]-bx[1])}  ({g.area:.0f} SF)"
        else:
            sub = f"{g.area:.0f} SQ.FT (NET)"
        ax.text(x, y, txt, fontsize=5.2 if g.area > 100 else 4.2, weight='bold', ha='center', va='center', zorder=8)
        ax.text(x, y - (1.0 if g.area > 100 else .8), sub, fontsize=4.0 if g.area > 100 else 3.4, ha='center', va='center', zorder=8, color='#374151')
    # dimensions
    if dims:
        xs = [LINE_B, 51.375, 52.125, 56.625, 57.375, 68.625, 69.375, 84.375, EAST_FACE]
        dim_h(ax, 36.875, 50.625, -2.6); dim_h(ax, 51.375, 56.625, -2.6); dim_h(ax, 57.375, 68.625, -2.6)
        dim_h(ax, 69.375, 84.375, -2.6); dim_h(ax, EAST_FACE, 87.9167, -2.6, fs=4.5)
        dim_h(ax, 0, LINE_B, -2.6, txt=f'LAWN {fmt(LINE_B)}')
        dim_h(ax, LINE_B, EAST_FACE, -4.2, txt=f'BUILDING FRONTAGE {fmt(EAST_FACE-LINE_B)}')
        dim_h(ax, 0, 87.9167, -8.4, txt="PLOT FRONTAGE 87'-11\" (P1-P0)")
        dim_v(ax, 0, FRONT, 90.5, fs=4.5); dim_v(ax, 3.75, 19.75, 90.5); dim_v(ax, 20.5, 28.125, 90.5)
        dim_v(ax, 28.875, 43.875, 90.5); dim_v(ax, 44.25, 56.67, 90.5)
        dim_v(ax, 3.75, 19.75, 29.5); dim_v(ax, 20.5, 24.5, 29.5, fs=4.5); dim_v(ax, 24.875, 33.0, 29.5, fs=4.5)
    if dims:
        # OTS measurements
        dim_al(ax, (52.125, 41.709), (68.015, 50.02), 1.7)
        dim_al(ax, (52.125, 38.323), (68.625, 46.953), -1.5)
        dim_v(ax, 38.323, 41.709, 51.0, fs=3.6)
        mid = (60.2, 0.5 * (38.323 + 41.709) + (60.2 - 52.125) * 0.523)
        th = math.atan(0.523); nx, ny = -math.sin(th), math.cos(th)
        p_in = (60.6 - nx * 1.5, mid[1] + .2 - ny * 1.5); p_out = (60.6 + nx * 1.5, mid[1] + .2 + ny * 1.5)
        ax.annotate('', xy=p_out, xytext=p_in, arrowprops=dict(arrowstyle='<->', lw=.5), zorder=7)
        ax.text(62.6, mid[1] + 1.15, '3\'-0" CLEAR', fontsize=3.6, rotation=math.degrees(th), ha='center', zorder=7)
    if title:
        ax.text(14, 57, 'GROUND FLOOR PLAN', fontsize=12, weight='bold')
        ax.text(14, 55.2, 'GF FFL +0\'-6" | PLOT & LAWN +/-0\'-0" = ROAD AT P1 (HIGHEST)  |  CLEAR CEILING 10\'-6"  |  FLOOR-TO-FLOOR 11\'-0"', fontsize=5.5)
    ax.set_xlim(-2, 98); ax.set_ylim(-11, 67)
    # north arrow
    ax.annotate('', xy=(8, 50), xytext=(8, 44), arrowprops=dict(arrowstyle='-|>', lw=1, color=INK))
    ax.text(8, 50.6, 'N', ha='center', fontsize=8, weight='bold')

def _tagpos(d):
    (x0, y0), (x1, y1) = d['p0'], d['p1']
    L = math.hypot(x1 - x0, y1 - y0); ux, uy = (x1 - x0) / L, (y1 - y0) / L
    nx, ny = -uy * d['side'], ux * d['side']
    if d['id'] == 'D1a':
        return (62.125, 21.4)
    return ((x0 + x1) / 2 - nx * 1.3, (y0 + y1) / 2 - ny * 1.3)

if __name__ == '__main__':
    fig = plt.figure(figsize=(16.5, 11.7))
    ax = fig.add_axes([0.02, 0.02, 0.96, 0.96])
    draw_ground_floor(ax)
    fig.savefig('preview_plan.png', dpi=170)
