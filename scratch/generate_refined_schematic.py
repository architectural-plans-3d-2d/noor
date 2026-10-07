"""
Generate and save a visual concept layout of the adjusted Master Plan
"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches

fig, ax = plt.subplots(figsize=(14, 12))
ax.set_xlim(-5, 95)
ax.set_ylim(-5, 65)
ax.set_aspect('equal')
ax.grid(True, linestyle=':', alpha=0.6)

# Site boundary
pts = [(0.0, 0.0), (10.49, 10.01), (24.59, 26.13), (41.19, 36.84), (67.70, 50.70), (84.84, 57.67), (88.81, 62.16), (87.92, 0.0)]
site_poly = patches.Polygon(pts, fill=False, edgecolor='#0f172a', lw=2.5, linestyle='--')
ax.add_patch(site_poly)

# Grid lines B, C, C', D, E
for gl, gx in [('B', 36.5), ('C', 51.75), ("C'", 57.0), ('D', 69.0), ('E', 84.75)]:
    ax.axvline(gx, color='#94a3b8', linestyle='-.', lw=1)
    ax.text(gx, -3, f"GRID {gl}", ha='center', va='center', fontweight='bold', fontsize=10)

# 1. MAIN LAWN (West of Line B)
lawn_pts = [(0.0, 0.0), (10.49, 10.01), (24.59, 26.13), (36.125, 33.58), (36.125, 0.0)]
ax.add_patch(patches.Polygon(lawn_pts, facecolor='#dcfce7', edgecolor='#15803d', lw=2))
ax.text(18.0, 12.0, "MAIN LAWN\n~590 SQ.FT OPEN GARDEN\n(STRICTLY WEST OF LINE B)", ha='center', va='center', fontweight='bold', fontsize=11, color='#166534')

# 2. BED ROOM-2 (GF, SW corner)
ax.add_patch(patches.Rectangle((36.875, 3.75), 14.5, 16.0, facecolor='#fef3c7', edgecolor='#b45309', lw=2))
ax.text(44.125, 11.75, "BED ROOM-2\n14'-6\" x 16'-0\"\n(Sliding glass doors to Lawn)", ha='center', va='center', fontweight='bold', fontsize=10)

# 3. BED-2 BATH & DRESS
ax.add_patch(patches.Rectangle((52.125, 3.75), 4.5, 16.0, facecolor='#e0f2fe', edgecolor='#0369a1', lw=1.5))
ax.text(54.375, 11.75, "BATH & DRESS\n4'-6\" x 16'-0\"", ha='center', va='center', fontsize=9, rotation=90)

# 4. CAR PORCH
ax.add_patch(patches.Rectangle((57.375, 0.0), 11.25, 20.5, facecolor='#f1f5f9', edgecolor='#334155', lw=2))
ax.text(63.0, 10.25, "CAR PORCH\n11'-3\" x 20'-6\"\n(Executive Parking)", ha='center', va='center', fontweight='bold', fontsize=11)

# 5. DRAWING ROOM (SE corner)
ax.add_patch(patches.Rectangle((69.375, 3.75), 15.0, 16.0, facecolor='#fef3c7', edgecolor='#b45309', lw=2))
ax.text(76.875, 11.75, "DRAWING ROOM\n15'-0\" x 16'-0\"\n(Formal South Windows)", ha='center', va='center', fontweight='bold', fontsize=10)

# 6. ENTRANCE FROM CAR PORCH
ax.add_patch(patches.Rectangle((56.625, 20.5), 6.0, 4.5, facecolor='#ecfdf5', edgecolor='#059669', lw=2))
ax.text(59.625, 22.75, "ENTRANCE\nFOYER\n6'x4'-6\"", ha='center', va='center', fontweight='bold', fontsize=8, color='#065f46')
ax.plot([56.625, 62.625], [20.5, 20.5], color='#dc2626', lw=6, label='6ft Main Entrance Door')

# 7. POWDER ROOM (on porch wall)
ax.add_patch(patches.Rectangle((62.625, 20.5), 6.0, 4.5, facecolor='#ffedd5', edgecolor='#c2410c', lw=2))
ax.text(65.625, 22.75, "POWDER ROOM\n6'-0\" x 4'-6\"\n(Vent to Porch)", ha='center', va='center', fontweight='bold', fontsize=8, color='#9a3412')
ax.plot([63.5, 66.5], [20.5, 20.5], color='#0284c7', lw=4, label='Exterior Vent to Porch')

# 8. STAIRCASE CORE (directly adjacent to Foyer/Powder)
ax.add_patch(patches.Rectangle((57.375, 25.0), 11.25, 7.5, facecolor='#faf5ff', edgecolor='#7e22ce', lw=2))
ax.text(63.0, 28.75, "STAIRCASE CORE\n11'-3\" x 7'-6\"\n(Central U-Stair to 1F)", ha='center', va='center', fontweight='bold', fontsize=9, color='#6b21a8')

# 9. KITCHEN (Bay B-C, North, strictly east of Line B)
kit_pts = [(36.875, 24.0), (51.375, 24.0), (51.375, 38.0), (41.19, 34.0), (36.875, 31.0)]
ax.add_patch(patches.Polygon(kit_pts, facecolor='#fef3c7', edgecolor='#b45309', lw=2))
ax.text(44.0, 29.0, "KITCHEN\n14'-6\" x 11'-6\" (152 sft)\n(Strictly East of Line B)", ha='center', va='center', fontweight='bold', fontsize=9)

# 10. MASTER BEDROOM (Bay D-E, North of Drawing)
ax.add_patch(patches.Rectangle((69.375, 20.5), 15.0, 16.0, facecolor='#fef3c7', edgecolor='#b45309', lw=2))
ax.text(76.875, 28.5, "MASTER BEDROOM\n15'-0\" x 16'-0\"", ha='center', va='center', fontweight='bold', fontsize=10)

# 11. MASTER DRESS & BATH (NE Angled Wing)
mbath_pts = [(69.375, 36.5), (84.375, 36.5), (84.375, 54.5), (69.375, 48.0)]
ax.add_patch(patches.Polygon(mbath_pts, facecolor='#e0f2fe', edgecolor='#0369a1', lw=2))
ax.text(76.875, 44.0, "LUXURY MASTER\nDRESS & 5-FIXTURE BATH\n(224 SQ.FT)", ha='center', va='center', fontweight='bold', fontsize=9)

# 12. FAMILY LOUNGE + DINING
lounge_pts = [(51.375, 24.0), (57.375, 24.0), (57.375, 32.5), (69.375, 32.5), (69.375, 48.0), (51.375, 38.0)]
ax.add_patch(patches.Polygon(lounge_pts, facecolor='#f8fafc', edgecolor='#475569', lw=2))
ax.text(60.0, 38.0, "FAMILY LOUNGE\n+ DINING HALL\n(280+ SQ.FT)", ha='center', va='center', fontweight='bold', fontsize=11, color='#1e293b')

# 13. EAST PERIMETER PASSAGE
ax.plot([85.125, 85.125], [0, 56], color='#0284c7', lw=2, linestyle=':')
ax.text(86.5, 25.0, "2'-1\" PASSAGE", rotation=90, ha='center', va='center', fontsize=8, color='#0284c7')

ax.legend(loc='upper left', fontsize=10)
ax.set_title("DAATA HAMLET RESIDENCE — REFINED MASTER GROUND FLOOR LAYOUT\n(Zero Encroachment West of Line B | Clear Entrance from Car Porch | Integrated Stairs & Powder)", fontsize=13, fontweight='bold', pad=15)

plt.tight_layout()
plt.savefig("scratch/refined_master_gf_layout.png", dpi=150)
print("Saved scratch/refined_master_gf_layout.png")
