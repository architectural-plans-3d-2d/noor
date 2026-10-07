"""
Detailed spatial layout test for Central Core:
Entrance from Car Porch, Stairs, and Powder Room
"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches

# The core area is bounded by:
# South: Car Porch (Y = 20.5, X in [56.625, 68.625]) and Bed-2 Bath (X in [51.375, 56.625])
# East: Drawing Room (X = 68.625, Y in [3.75, 20.5]) and Bed-1/MBed (X = 68.625, Y >= 20.5)
# West: Line C (X = 51.375)
# North: Family Lounge (Y >= 28.5 or 30.0)

fig, axes = plt.subplots(1, 3, figsize=(24, 8))

for ax in axes:
    ax.set_xlim(48, 72)
    ax.set_ylim(15, 34)
    ax.set_aspect('equal')
    ax.grid(True, linestyle='--', alpha=0.5)

# Common elements:
for ax in axes:
    # Car porch
    ax.add_patch(patches.Rectangle((56.625, 15), 12.0, 5.5, facecolor='#e2e8f0', edgecolor='black', lw=2))
    ax.text(62.6, 17.5, "CAR PORCH\n(X=56.625 to 68.625)", ha='center', va='center', fontsize=9)
    # Bed-2 Bath
    ax.add_patch(patches.Rectangle((51.375, 15), 5.25, 5.5, facecolor='#bfdbfe', edgecolor='black', lw=1.5))
    ax.text(54.0, 17.5, "BATH-2", ha='center', va='center', fontsize=8, rotation=90)
    # Drawing Room
    ax.add_patch(patches.Rectangle((68.625, 15), 3.0, 5.5, facecolor='#fef08a', edgecolor='black', lw=2))
    ax.text(70.0, 17.5, "DRAWING", ha='center', va='center', fontsize=8, rotation=90)

# ==============================================================================
# OPTION A: ENTRANCE FOYER IN FRONT (Y=20.5 to 24.5) + STAIRS & POWDER BEHIND (Y=24.5 to 32.5)
# ==============================================================================
ax = axes[0]
ax.set_title("OPTION A: Foyer in Front (Y=20.5-24.5)\nStairs & Powder Shifted North", fontsize=11, fontweight='bold')

# Main Door at Y = 20.5 (Car porch wall)
ax.plot([59.625, 65.625], [20.5, 20.5], color='red', lw=5, label='6ft Main Door')
# Entrance Foyer: Y in [20.5, 24.5], X in [56.625, 68.625]
ax.add_patch(patches.Rectangle((56.625, 20.5), 12.0, 4.0, facecolor='#dcfce7', edgecolor='green', lw=2))
ax.text(62.6, 22.5, "ENTRANCE FOYER (11'-3\" x 4'-0\")\nClear entry from Car Porch", ha='center', va='center', fontsize=8, fontweight='bold')

# Door to Drawing at X = 68.625, Y in [21.0, 24.0]
ax.plot([68.625, 68.625], [21.0, 24.0], color='blue', lw=4, label='Door to Drawing')

# Powder Room: X in [62.625, 68.625], Y in [24.5, 29.5] (6'-0" x 5'-0")
# But how does it ventilate to exterior? 
ax.add_patch(patches.Rectangle((62.625, 24.5), 6.0, 5.0, facecolor='#fed7aa', edgecolor='orange', lw=2))
ax.text(65.6, 27.0, "POWDER ROOM\n6'-0\" x 5'-0\"\n(under mid-landing)", ha='center', va='center', fontsize=8)

# Stairs: U-turn stairs X in [56.625, 62.625], Y in [24.5, 32.5]
ax.add_patch(patches.Rectangle((56.625, 24.5), 6.0, 8.0, facecolor='#f3e8ff', edgecolor='purple', lw=2))
ax.text(59.6, 28.5, "STAIRS\n(rises to 1F)", ha='center', va='center', fontsize=8)


# ==============================================================================
# OPTION B: SIDE-BY-SIDE SPLIT AT PORCH WALL (Y=20.5)
# West half (X=56.625 to 62.25): 5'-7.5" wide unobstructed ENTRANCE FOYER
# East half (X=62.25 to 68.625): POWDER ROOM on porch wall + STAIRS
# ==============================================================================
ax = axes[1]
ax.set_title("OPTION B: Side-by-Side Split at Porch Wall\nWest Entrance (5'-6\") + East Powder & Stairs", fontsize=11, fontweight='bold')

# Main Door at Y = 20.5, X in [56.875, 62.0] (5'-1.5" wide grand double door)
ax.plot([56.875, 62.0], [20.5, 20.5], color='red', lw=5, label='Main Door')

# Entrance Passage / Foyer: X in [51.375, 62.25], Y in [20.5, 28.5]
ax.add_patch(patches.Rectangle((56.625, 20.5), 5.625, 8.0, facecolor='#dcfce7', edgecolor='green', lw=2))
ax.text(59.4, 24.5, "MAIN ENTRANCE\nPASSAGE & FOYER\n(5'-7\" wide)\n100% CLEAR TO LOUNGE", ha='center', va='center', fontsize=8, fontweight='bold')

# Powder Room: X in [62.25, 68.625], Y in [20.5, 25.0] (6'-4\" x 4'-6\")
ax.add_patch(patches.Rectangle((62.25, 20.5), 6.375, 4.5, facecolor='#fed7aa', edgecolor='orange', lw=2))
ax.text(65.4, 22.75, "POWDER ROOM\n6'-4\" x 4'-6\"\nVentilates directly\nto Car Porch wall!", ha='center', va='center', fontsize=8, fontweight='bold')
# Vent to porch
ax.plot([63.5, 66.5], [20.5, 20.5], color='cyan', lw=4, label='Exterior Vent to Porch')

# Stairs: L-turn or U-turn stairs
# Mid-landing at X in [62.25, 68.625], Y in [20.5, 25.0] OVER the powder room!
# Stairs rise from Lounge (Y = 30.5) down to landing, or start at Foyer (X=59) and rise east
ax.add_patch(patches.Rectangle((62.25, 25.0), 6.375, 5.5, facecolor='#f3e8ff', edgecolor='purple', lw=2))
ax.text(65.4, 27.75, "STAIR FLIGHTS\n(Connecting to 1F)", ha='center', va='center', fontsize=8)


# ==============================================================================
# OPTION C: ENTER THROUGH PORCH CENTER, STAIRS ALONG DRAWING WALL WITH POWDER UNDER
# ==============================================================================
ax = axes[2]
ax.set_title("OPTION C: Central Entry Door + L-Shape/Corner Stair", fontsize=11, fontweight='bold')

# Door in center of Porch wall: X in [59.0, 65.0]
ax.plot([59.0, 65.0], [20.5, 20.5], color='red', lw=5)
ax.add_patch(patches.Rectangle((56.625, 20.5), 12.0, 4.5, facecolor='#dcfce7', edgecolor='green', lw=2))
ax.text(62.6, 22.75, "GRAND VESTIBULE\n11'-3\" x 4'-6\"", ha='center', va='center', fontsize=8, fontweight='bold')

# Powder room on West side of vestibule (X in [51.375, 56.625], Y in [20.5, 25.5])
# Wait! X in [51.375, 56.625] is north of Bed-2 Bath!
ax.add_patch(patches.Rectangle((51.375, 20.5), 5.25, 5.0, facecolor='#fed7aa', edgecolor='orange', lw=2))
ax.text(54.0, 23.0, "POWDER\n5'-3\" x 5'-0\"", ha='center', va='center', fontsize=8)

# Stairs at Y in [25.0, 32.5], X in [57.375, 68.625]
ax.add_patch(patches.Rectangle((57.375, 25.0), 11.25, 7.5, facecolor='#f3e8ff', edgecolor='purple', lw=2))
ax.text(63.0, 28.75, "CENTRAL U-STAIR\n11'-3\" x 7'-6\"\nDirectly off Foyer", ha='center', va='center', fontsize=8)

plt.tight_layout()
plt.savefig("scratch/detailed_central_options.png", dpi=150)
print("Saved scratch/detailed_central_options.png")
