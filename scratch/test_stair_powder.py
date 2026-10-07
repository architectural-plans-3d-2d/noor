"""
Test Staircase and Powder Room geometry in the central core
Core zone: X in [56.625, 68.625] (or up to C at 51.375), Y in [20.5, 30.0]
"""

# Let's test two flight directions for the stairs:
# Configuration 1:
# Entrance passage: X in [56.625, 62.0]
# Stairs & Powder: X in [62.0, 68.625] (width = 6'-7.5", clear 6'-3")
# In X in [62.0, 68.625]:
# What if the stair is an L-shape or U-shape or dog-leg?
# Floor height to 1F = 11.0 ft (132 inches).
# 18 risers x 7.33" = 132", or 20 risers x 6.6" = 132".

# Configuration 2:
# What if the stairs run East-West across X in [56.625, 68.625], but:
# Flight 1 starts at Y = 25.0 and goes East, and landing is above Powder?
# Where would you enter?
# What if you enter at Y = 20.5 through a Foyer, and the stairs are at Y in [23.5, 30.5]?
# But can the powder room be at Y in [20.5, 23.5]?
# YES! A powder room at Y in [20.5, 24.5] is on the exterior wall of the porch!

print("Testing Configuration 2 in detail...")
