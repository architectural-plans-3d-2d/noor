import sys
from pathlib import Path
sys.path.insert(0, str(Path.cwd()))
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from shapely.geometry import Polygon, box as sbox, Point, LineString
from shapely.ops import unary_union
from scripts.daata_hamlet.model import PLOT, SITE_POINTS, R

fig, ax = plt.subplots(figsize=(14, 11))

# Plot boundary
px, py = zip(*list(PLOT.exterior.coords))
ax.plot(px, py, 'r-', lw=2.5, label='Plot Boundary')
for p, x, y in SITE_POINTS:
    ax.plot(x, y, 'ro')
    ax.annotate(p, (x, y), textcoords="offset points", xytext=(5, 5), fontsize=10, fontweight='bold', color='darkred')

# Zones:
# 1. Main Lawn:
lawn = sbox(0, 0, 36.125, 20.0).intersection(PLOT)
lx, ly = zip(*list(lawn.exterior.coords))
ax.fill(lx, ly, color='#abebc6', alpha=0.6)
ax.text(18, 10, 'MAIN LAWN\n(Converted from old porch)\n~520 sq.ft', ha='center', va='center', fontweight='bold', color='#145a32')

# 2. Bed-2:
b2 = sbox(36.125, 0.0, 51.375, 16.0)
b2x, b2y = zip(*list(b2.exterior.coords))
ax.fill(b2x, b2y, color='#d4efdf', alpha=0.7, ec='black', lw=1.5)
ax.text(43.75, 8.0, 'BED ROOM-2\n15\'-3" x 16\'-0"\n244 sft\n(Lawn View)', ha='center', va='center', fontweight='bold')

# 3. Bed-2 Bath & Dress:
b2bd = sbox(51.375, 0.0, 56.625, 16.0)
bx, by = zip(*list(b2bd.exterior.coords))
ax.fill(bx, by, color='#e8f8f5', alpha=0.7, ec='black', lw=1.5)
ax.text(54.0, 8.0, 'BATH &\nDRESS\n5\'-3"x16\'-0"', ha='center', va='center', fontsize=9, fontweight='bold')

# 4. New Car Porch:
cp = sbox(56.625, 0.0, 68.625, 20.0)
cpx, cpy = zip(*list(cp.exterior.coords))
ax.fill(cpx, cpy, color='#eaeded', alpha=0.7, ec='black', lw=2)
ax.text(62.625, 10.0, 'NEW CAR PORCH\n12\'-0" x 20\'-0"\n(Central Arrival)', ha='center', va='center', fontweight='bold', color='#2c3e50')

# 5. Drawing Room (South-East):
dr = sbox(68.625, 0.0, 87.21, 16.0)
drx, dry = zip(*list(dr.exterior.coords))
ax.fill(drx, dry, color='#fef9e7', alpha=0.7, ec='black', lw=1.5)
ax.text(77.9, 8.0, 'DRAWING ROOM\n18\'-7" x 16\'-0"\n297 sft\n(Corner Suite)', ha='center', va='center', fontweight='bold')

# 6. Central Staircase & Powder:
st = sbox(56.625, 20.0, 68.625, 28.5)
stx, sty = zip(*list(st.exterior.coords))
ax.fill(stx, sty, color='#fcf3cf', alpha=0.7, ec='black', lw=1.5)
ax.text(62.625, 24.25, 'STAIRCASE CORE\n(Powder Room Under\n7\'-0" Landing)', ha='center', va='center', fontsize=9, fontweight='bold')

# 7. Entrance Foyer:
ef = sbox(36.125, 16.0, 56.625, 24.0)
efx, efy = zip(*list(ef.exterior.coords))
ax.fill(efx, efy, color='#ebf5fb', alpha=0.7, ec='black', lw=1.5)
ax.text(46.375, 20.0, 'ENTRANCE FOYER\n20\'-6" x 8\'-0"\n(Direct 6\' Porch Door)', ha='center', va='center', fontweight='bold', color='#1b4f72')

# 8. Kitchen on Angled Boundary:
kit = sbox(24.0, 20.0, 36.125, 34.0).intersection(PLOT)
kx, ky = zip(*list(kit.exterior.coords))
ax.fill(kx, ky, color='#fdebd0', alpha=0.7, ec='black', lw=1.5)
ax.text(30.0, 27.0, 'KITCHEN\n(Trapezoid on\nBoundary Wall)', ha='center', va='center', fontsize=9, fontweight='bold', color='#7e5109')

# 9. Lounge + Dining:
lounge = sbox(36.125, 24.0, 68.625, 45.0).intersection(PLOT.buffer(-2.0))
lx, ly = zip(*list(lounge.exterior.coords))
ax.fill(lx, ly, color='#e8daef', alpha=0.6, ec='black', lw=1.5)
ax.text(50.0, 34.0, 'FAMILY LOUNGE + DINING\n(Expands north to P4-P5\nwith 2\'-0" passage)', ha='center', va='center', fontweight='bold', color='#512e5f')

# 10. Rear Suite (Bed-1 / Master Suite):
r_bed = sbox(68.625, 16.0, 87.21, 36.0)
rbx, rby = zip(*list(r_bed.exterior.coords))
ax.fill(rbx, rby, color='#d1f2eb', alpha=0.7, ec='black', lw=1.5)
ax.text(77.9, 26.0, 'BED ROOM-1\n(Rear Master Suite)\n18\'-7" x 20\'-0"', ha='center', va='center', fontweight='bold', color='#0e6251')

# 11. Rear Suite Bath & Dress:
r_bd = sbox(68.625, 36.0, 88.0, 56.0).intersection(PLOT.buffer(-2.0))
rx, ry = zip(*list(r_bd.exterior.coords))
ax.fill(rx, ry, color='#a3e4d7', alpha=0.7, ec='black', lw=1.5)
ax.text(76.0, 44.0, 'MASTER BATH &\nDRESSING\n(Angled Slope Wing)', ha='center', va='center', fontweight='bold', color='#0b5345')

ax.set_aspect('equal')
ax.set_xlim(-5, 95)
ax.set_ylim(-5, 65)
ax.set_title('DAATA HAMLET RESIDENCE — Proposed Architectural Concept Scheme', fontsize=14, fontweight='bold')
ax.grid(True, linestyle=':', alpha=0.5)

plt.tight_layout()
plt.savefig('scratch/proposed_concept_layout.png', dpi=150)
print("Saved scratch/proposed_concept_layout.png successfully!")
