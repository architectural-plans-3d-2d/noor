"""
Visualize and test Central Layout Options:
Entrance from Car Porch, Stairs, and Powder Room
"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches

# Car porch: X in [56.625, 68.625], Y in [0, 20.5]
# Let's test two main options:

# OPTION 1: 
# Entrance Door from Car Porch is on the WEST side: X in [56.625, 62.0], Y = 20.5.
# Width = 5'-4.5". Grand 5'-0" Double Door (or 4' + 1.5' sidelight).
# Clear Entrance Hall: X in [51.375, 62.0], Y in [20.5, 28.5].
# Stairs & Powder on the EAST side: X in [62.0, 68.625], Y in [20.5, 28.5].
# Powder Room: under landing at X in [62.0, 68.625], Y in [20.5, 24.5].
# Stairs: Flight 1 starts at Y = 28.5, goes south to landing at Y = 24.5 (rises to +7'-0").
# Flight 2 turns at landing and goes north from Y = 24.5 to 28.5 (rises to +11'-0").

# OPTION 2:
# What if the entrance is in the CENTER or EAST?
# What if Stairs run East-West, but shifted north to Y in [24.5, 32.0]?
# Entrance Foyer: Y in [20.5, 24.5], X in [56.625, 68.625].
# Main Door: 6'-0" wide double door centered at X in [60.0, 66.0], Y = 20.5.
# When you enter at Y = 20.5, you step into a 4'-0" deep by 12'-0" wide Foyer Vestibule.
# Then at Y = 24.5, the stairs and powder are located!
# But where would powder ventilate?

# Let's plot both options and compare!
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 10))

for ax in (ax1, ax2):
    ax.set_xlim(30, 90)
    ax.set_ylim(0, 50)
    ax.set_aspect('equal')
    ax.grid(True, linestyle='--', alpha=0.5)

# OPTION 1 PLOT
ax1.set_title("OPTION 1: West Entrance Door + East Stairs & Powder", fontsize=12, fontweight='bold')
# Car Porch
ax1.add_patch(patches.Rectangle((56.625, 0), 12.0, 20.5, fill=True, facecolor='#e2e8f0', edgecolor='black', lw=2))
ax1.text(62.6, 10, "CAR PORCH\n11'-3\" x 20'-6\"", ha='center', va='center')
# Bed 2
ax1.add_patch(patches.Rectangle((36.125, 3.75), 15.25, 16.0, fill=True, facecolor='#fef08a', edgecolor='black', lw=2))
ax1.text(43.75, 11.75, "BED ROOM-2", ha='center', va='center')
# Bed 2 Bath
ax1.add_patch(patches.Rectangle((51.375, 3.75), 5.25, 16.0, fill=True, facecolor='#bfdbfe', edgecolor='black', lw=1.5))
ax1.text(54.0, 11.75, "BATH-2", ha='center', va='center', rotation=90)
# Drawing Room
ax1.add_patch(patches.Rectangle((68.625, 3.75), 15.75, 16.0, fill=True, facecolor='#fef08a', edgecolor='black', lw=2))
ax1.text(76.5, 11.75, "DRAWING ROOM", ha='center', va='center')

# Option 1 Entrance: X in [56.625, 62.0], Y = 20.5
ax1.add_patch(patches.Rectangle((56.625, 20.5), 5.375, 8.0, fill=True, facecolor='#bbf7d0', edgecolor='green', lw=2))
ax1.text(59.3, 24.5, "ENTRANCE\nPASSAGE\n(5'-4\" wide)", ha='center', va='center', fontsize=9, fontweight='bold')
# Main Door
ax1.plot([56.875, 61.875], [20.5, 20.5], color='red', lw=4, label='Main Door (5ft)')
# Stairs at X in [62.0, 68.625], Y in [20.5, 28.5]
ax1.add_patch(patches.Rectangle((62.0, 20.5), 6.625, 4.0, fill=True, facecolor='#fed7aa', edgecolor='orange', lw=2))
ax1.text(65.3, 22.5, "POWDER ROOM\n(under landing)\n6'-4\" x 4'-0\"", ha='center', va='center', fontsize=8, fontweight='bold')
ax1.add_patch(patches.Rectangle((62.0, 24.5), 6.625, 4.0, fill=True, facecolor='#fed7aa', edgecolor='purple', lw=2))
ax1.text(65.3, 26.5, "STAIR FLIGHTS\n(rises to 1F)", ha='center', va='center', fontsize=8)


# OPTION 2 PLOT
ax2.set_title("OPTION 2: Foyer at Porch Wall + Stair/Powder Shifted", fontsize=12, fontweight='bold')
# Car Porch
ax2.add_patch(patches.Rectangle((56.625, 0), 12.0, 20.5, fill=True, facecolor='#e2e8f0', edgecolor='black', lw=2))
ax2.text(62.6, 10, "CAR PORCH\n11'-3\" x 20'-6\"", ha='center', va='center')
# Bed 2
ax2.add_patch(patches.Rectangle((36.125, 3.75), 15.25, 16.0, fill=True, facecolor='#fef08a', edgecolor='black', lw=2))
ax2.text(43.75, 11.75, "BED ROOM-2", ha='center', va='center')
# Bed 2 Bath
ax2.add_patch(patches.Rectangle((51.375, 3.75), 5.25, 16.0, fill=True, facecolor='#bfdbfe', edgecolor='black', lw=1.5))
ax2.text(54.0, 11.75, "BATH-2", ha='center', va='center', rotation=90)
# Drawing Room
ax2.add_patch(patches.Rectangle((68.625, 3.75), 15.75, 16.0, fill=True, facecolor='#fef08a', edgecolor='black', lw=2))
ax2.text(76.5, 11.75, "DRAWING ROOM", ha='center', va='center')

# Foyer
ax2.add_patch(patches.Rectangle((56.625, 20.5), 12.0, 5.0, fill=True, facecolor='#bbf7d0', edgecolor='green', lw=2))
ax2.text(62.6, 23.0, "GRAND ENTRANCE FOYER\n11'-3\" x 5'-0\"", ha='center', va='center', fontsize=9, fontweight='bold')
# Main Door 6ft
ax2.plot([59.625, 65.625], [20.5, 20.5], color='red', lw=4, label='Main Door (6ft)')

plt.tight_layout()
plt.savefig("scratch/central_options.png", dpi=150)
print("Saved scratch/central_options.png")
