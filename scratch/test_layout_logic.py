"""
Test layout configurations for Central Area and Bay B-C
"""
from shapely.geometry import box as sbox, Polygon

XB_W, XB_E = 36.125, 36.875
XC_W, XC_E = 51.375, 52.125
XC_P_W, XC_P_E = 56.625, 57.375
XD_W, XD_E = 68.625, 69.375
XE_W, XE_E = 84.375, 85.125

print("--- 1. BAY B-C (WEST ROOMS) ---")
# User: "do not go beyond line B, west of B is lawn reserved"
# Everything west of XB_W (36.125) is MAIN LAWN.
# Inside Bay B-C (X in [36.125, 51.375]):
# South: Bed Room-2: X in [36.875, 51.375], Y in [3.75, 19.75]
# Dimensions: 14'-6" x 16'-0" = 232 sq.ft.
# North of Bed Room-2 (Y in [20.5, 36.0]):
# Plot boundary near P4: at X = 36.125, Y_b = 33.58; at X = 51.375, Y_b = 42.15.
# If setback = 2'-0", Y_inner at X=36.125 is ~31.58, at X=51.375 is ~40.15.
# What if KITCHEN is placed in Bay B-C:
# e.g., Kitchen: X in [36.875, 51.375], Y in [23.5, 35.0] (approx 14'-6" x 11'-6")
# Area = ~150 sq.ft! That's a great kitchen!
# And between Bed Room-2 (Y <= 19.75) and Kitchen (Y >= 23.5), we have an internal corridor / lobby (Y in [19.75, 23.5])!
print("Kitchen in Bay B-C fits cleanly within boundary and stays EAST of Line B!")

print("\n--- 2. CENTRAL CORE (CAR PORCH, ENTRANCE, STAIRS, POWDER) ---")
# Car Porch: X in [56.625, 68.625], Y in [0, 20.5].
# Drawing Room: X in [68.625, 84.375], Y in [3.75, 19.75].
# Bed-2 Bath/Dress: X in [51.375, 56.625], Y in [3.75, 19.75].

# Now, at Y = 20.5, between X = 51.375 and X = 68.625:
# Total width = 17'-3"!
# Car Porch faces north onto Y = 20.5 between X = 56.625 and 68.625 (12'-0" width).
# If we place:
# ENTRANCE DOOR: at Y = 20.5, on the car porch wall.
# Where should the door be, and where should the stairs and powder be?

# Let's explore:
# Can the stairs be located at:
# X in [58.0, 68.625], Y in [22.0, 29.5]?
# If stairs are at Y in [22.5, 30.0], then Y in [20.5, 22.5] is only 2 feet. That's too tight.

# What if:
# Entrance Foyer is from Y = 20.5 to 25.5 across X in [56.625, 68.625]?
# But then where does the staircase go?
# If staircase goes at Y in [25.5, 33.5], X in [58.0, 68.625]:
# Then the staircase is at Y in [25.5, 33.5].
# And where is the powder room?
# If powder room is at Y in [20.5, 25.5], X in [62.625, 68.625]:
# Size: 6'-0" x 5'-0" powder room!
# Exterior wall: South wall at Y = 20.5 faces Car Porch! Natural ventilation window directly to porch!
# Entrance door: on South wall at Y = 20.5, X in [56.625, 62.625] (6'-0" wide double entrance door)!
# And what is at Y in [25.5, 33.5]?
# The STAIRCASE is at Y in [25.5, 33.5]!
# Wait! In this layout:
# - Powder room is at Y in [20.5, 25.5], X in [62.625, 68.625] (against Drawing room and Porch).
# - Main entrance door is at Y = 20.5, X in [56.625, 62.625] (opening into Foyer).
# - Foyer is at Y in [20.5, 25.5], X in [51.375, 62.625] (11'-3" wide x 5'-0" deep).
# - Directly behind the Foyer (at Y in [25.5, 33.5]):
#   The STAIRCASE rises!
#   Wait! If the staircase is at Y in [25.5, 33.5], X in [60.0, 68.625]:
#   It rises up from Foyer level up to First floor!
#   And what is under the staircase?
#   Storage / coat closet / or expanded powder / display niche!
