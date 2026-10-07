import sys
from pathlib import Path
from shapely.geometry import Polygon, box as sbox, Point
from shapely.ops import unary_union

sys.path.insert(0, str(Path.cwd()))
import scripts.daata_hamlet.model as orig_m

text = Path("scripts/daata_hamlet/model.py").read_text(encoding="utf-8")

# Let's inspect each point:
# Point 1: 1F Utility Balcony shape = Dirty Kitchen below
# In model.py:
# dirty_k = de_block.intersection(FP_IN).intersection(sbox(XD_E, 46.875, XE_I, 60.0))
# util_balc should be exactly dirty_k:
text = text.replace(
'''    util_balc = de_block.intersection(sbox(XD_W, 46.875, XE_O, 60.0))
    room(f, "UTILITY BALCONY", util_balc, "ext", (77.0, 51.0))''',
'''    util_balc = de_block.intersection(FP_IN).intersection(sbox(XD_E, 46.875, XE_I, 60.0))
    room(f, "UTILITY BALCONY", util_balc, "ext", (77.0, 50.5))'''
)

# Point 2: Remove extra wardrobe boxes and console boxes blocking stairs
# In furnish(m):
# Remove rect("GF", 66.25, 28.5, XD_W, 34.0) (TV console blocking stair)
# Remove rect("1F", 66.25, 28.5, XD_W, 34.0) (TV console blocking stair)
# Remove all extra "WARDROBE" boxes
text = text.replace(
'''        # Wardrobes in master suites:
        rect(fl, 74.5, 25.5, 78.5, 27.5, "WARDROBE")         # East dress
        if fl != "GF":
            rect(fl, 52.5, 17.5, 56.5, 19.5, "WARDROBE")     # Middle bed wardrobe
        if fl != "2F":
            rect(fl, 43.0, 25.5, 47.0, 27.5, "WARDROBE")     # West dress''',
'''        # (Clean architectural furniture layout - redundant wardrobe boxes removed)'''
)

text = text.replace(
'''            rect("GF", 42.5, 27.25, 45.0, 29.0, "WARDROBE")   # Dress wardrobe
            rect("GF", 42.5, 30.25, 45.0, 32.0, "WARDROBE")   # Dress wardrobe
            rect("GF", 38.0, 20.6, 42.0, 21.6, "CONSOLE")     # Foyer console''',
'''            pass'''
)

# Fix lounge sofa coordinates on GF so it doesn't overlap powder room:
text = text.replace(
'''    rect("GF", 60.5, 24.5, 67.5, 27.5); rect("GF", 60.5, 27.5, 63.5, 31.5)       # Lounge sofas
    rect("GF", 66.25, 28.5, XD_W, 34.0)                                          # TV console''',
'''    rect("GF", 56.0, 28.5, 64.0, 31.5); rect("GF", 56.0, 31.5, 59.0, 35.0)       # Lounge sofas'''
)

# Remove TV console on 1F blocking stairs:
text = text.replace(
'''    rect("1F", 55.5, 29.0, 64.0, 32.0); rect("1F", 55.5, 32.0, 58.5, 36.0)
    rect("1F", 60.0, 37.0, 68.0, 40.5)
    rect("1F", 66.25, 28.5, XD_W, 34.0)''',
'''    rect("1F", 55.5, 29.0, 64.0, 32.0); rect("1F", 55.5, 32.0, 58.5, 36.0)
    rect("1F", 60.0, 37.0, 68.0, 40.5)'''
)

# Point 3: Correct "PRIVATE FOYER" text that is overextended
# Change "PRIVATE FOYER" to "FOYER"
text = text.replace('room(f, "PRIVATE FOYER", R(XC_E, 20.5, 56.75, 27.5), "circ", (54.5, 24.0), False)',
                    'room(f, "FOYER", R(XC_E, 20.5, 56.75, 27.5), "circ", (54.5, 24.0), False)')

# Point 4 & 5: On 2F, move Bedroom-7's bath to the LEFT (West) instead of the right!
# And keep the north wall on 2F as barrier to Rear Terrace.
# On 2F:
# Bed-7 Bath is at X in [52.125, 57.5], Y in [20.5, 26.5] (West side!)
# High-level vent on west wall X = 51.75 into outdoor Side Terrace!
# OTS on 2F is at X in [57.5, 62.125], Y in [20.5, 26.5]
# East side X in [62.125, XD_W] is STAIR LOBBY!
# 2F partitions:
old_2f_part = '''    for r in [
        (78.5, 20.5, 78.875, 27.5),
        (56.75, 20.5, 57.125, 26.5),
        (61.75, 20.5, 62.125, 26.5),
        (56.75, 26.125, XD_W, 26.5),
        (79.0, 36.375, 79.375, 46.125),
        (79.375, 41.5, XE_I, 41.875),
        (STAIR_X0, 31.75, MID_X, 32.125)
    ]:'''

new_2f_part = '''    for r in [
        (78.5, 20.5, 78.875, 27.5),
        (57.125, 20.5, 57.5, 26.5),
        (61.75, 20.5, 62.125, 26.5),
        (XC_E, 27.5, XD_W, 28.25),
        (79.0, 36.375, 79.375, 46.125),
        (79.375, 41.5, XE_I, 41.875),
        (STAIR_X0, 31.75, MID_X, 32.125)
    ]:'''

text = text.replace(old_2f_part, new_2f_part)

# 2F Openings:
# Bed-7 Bath vent on Line C (X = 51.75) venting west to Side Terrace:
# Bed-7 Bath door from bedroom at Y = 20.125, X in [53.5, 56.5]
# Bed-7 door to Stair Lobby on east at Y = 20.125, X in [63.5, 67.0]
# Arch on Line D connecting Stair Lobby to Stairs at X = 69.0, Y in [21.0, 26.5]
# Door to Rear Terrace on north wall at Y = 27.875, X in [63.5, 66.5]
old_2f_ops = '''    op(s, "x", 3.375, 56.375, 64.375, 0.0, 8.0, "slide", "SL")
    op(s, "x", 3.375, 73.375, 80.375, 0.0, 8.0, "slide", "SL")
    op(s, "y", 51.75, 6.0, 11.0, 2.0, 8.0, "window", "W2")
    op(s, "y", 51.75, 13.5, 16.5, 0.0, 7.0, "door", "D1", "a", -1)
    op(s, "y", 61.9375, 22.5, 24.5, 6.5, 8.0, "vent", "V")
    op(s, "y", 84.75, 22.5, 24.5, 6.5, 8.0, "vent", "V")
    op(s, "y", 84.75, 29.5, 34.5, 1.0, 10.25, "window", "STAIR-GL")
    op(s, "y", 84.75, 37.5, 40.5, 3.5, 7.0, "window", "LW-E")
    op(s, "y", 84.75, 43.0, 45.5, 6.5, 8.0, "vent", "V")
    op(s, "x", 46.5, 71.0, 77.0, 3.0, 7.0, "window", "LW-N")

    op(s, "x", 20.125, 53.0, 56.5, 0.0, 7.0, "door", "D2", "a", 1)
    op(s, "x", 20.125, 63.5, 66.0, 0.0, 7.0, "door", "D3", "a", 1)
    op(s, "x", 27.875, 53.0, 56.5, 0.0, 7.0, "door", "D1", "b", 1)
    op(s, "y", 69.0, 21.0, 26.5, 0.0, 7.0, "arch", "ARCH")
    op(s, "x", 20.125, 70.0, 73.5, 0.0, 7.0, "door", "D2", "a", -1)
    op(s, "y", 78.6875, 22.5, 25.5, 0.0, 7.0, "door", "D3", "b", 1)'''

new_2f_ops = '''    op(s, "x", 3.375, 56.375, 64.375, 0.0, 8.0, "slide", "SL")
    op(s, "x", 3.375, 73.375, 80.375, 0.0, 8.0, "slide", "SL")
    op(s, "y", 51.75, 6.0, 11.0, 2.0, 8.0, "window", "W2")
    op(s, "y", 51.75, 13.5, 16.5, 0.0, 7.0, "door", "D1", "a", -1)
    op(s, "y", 51.75, 22.5, 24.5, 6.5, 8.0, "vent", "V")
    op(s, "y", 84.75, 22.5, 24.5, 6.5, 8.0, "vent", "V")
    op(s, "y", 84.75, 29.5, 34.5, 1.0, 10.25, "window", "STAIR-GL")
    op(s, "y", 84.75, 37.5, 40.5, 3.5, 7.0, "window", "LW-E")
    op(s, "y", 84.75, 43.0, 45.5, 6.5, 8.0, "vent", "V")
    op(s, "x", 46.5, 71.0, 77.0, 3.0, 7.0, "window", "LW-N")

    op(s, "x", 20.125, 53.5, 56.5, 0.0, 7.0, "door", "D3", "a", 1)
    op(s, "x", 20.125, 63.5, 67.0, 0.0, 7.0, "door", "D2", "a", 1)
    op(s, "x", 27.875, 63.5, 66.5, 0.0, 7.0, "door", "D-TERR", "b", 1)
    op(s, "y", 69.0, 21.0, 26.5, 0.0, 7.0, "arch", "ARCH")
    op(s, "x", 20.125, 70.0, 73.5, 0.0, 7.0, "door", "D2", "a", -1)
    op(s, "y", 78.6875, 22.5, 25.5, 0.0, 7.0, "door", "D3", "b", 1)'''

text = text.replace(old_2f_ops, new_2f_ops)

# 2F Rooms:
old_2f_rms = '''    room(s, "BED ROOM-7", R(XC_E, 3.75, XD_W, 19.75), "hab")
    b7_bath = R(62.125, 20.5, XD_W, 26.5)
    room(s, "BATH", b7_bath, "wet", (65.4, 23.5))
    ots_2f = sbox(57.125, 20.5, 61.75, 26.5)
    room(s, "LIGHT COURT (OTS)", ots_2f, "ext", (59.4, 23.5))
    room(s, "PRIVATE FOYER", R(XC_E, 20.5, 56.75, 27.5), "circ", (54.5, 24.0), False)'''

new_2f_rms = '''    room(s, "BED ROOM-7", R(XC_E, 3.75, XD_W, 19.75), "hab")
    b7_bath = R(XC_E, 20.5, 57.125, 26.5)
    room(s, "BATH", b7_bath, "wet", (54.5, 23.5))
    ots_2f = sbox(57.5, 20.5, 61.75, 26.5)
    room(s, "LIGHT COURT (OTS)", ots_2f, "ext", (59.6, 23.5))
    room(s, "STAIR LOBBY", R(62.125, 20.5, XD_W, 27.5), "circ", (65.4, 24.0), False)'''

text = text.replace(old_2f_rms, new_2f_rms)

# 2F furniture:
text = text.replace(
'''            rect(fl, 65.0, 20.8, 68.0, 23.8)                  # shower 3x3
            circ(fl, 63.5, 21.8, 0.75)                        # WC
            rect(fl, 63.0, 24.5, 66.0, 26.0)                  # basin''',
'''            if fl == "1F":
                rect(fl, 65.0, 20.8, 68.0, 23.8)                  # shower 3x3
                circ(fl, 63.5, 21.8, 0.75)                        # WC
                rect(fl, 63.0, 24.5, 66.0, 26.0)                  # basin
            elif fl == "2F":
                rect(fl, 52.5, 20.8, 55.5, 23.8)                  # shower 3x3
                circ(fl, 56.0, 21.8, 0.75)                        # WC
                rect(fl, 53.0, 24.5, 56.0, 26.0)                  # basin'''
)

# Also check 1F partition (remove redundant wall between lounge and ots):
# (56.75, 26.125, XD_W, 26.5) -> on 1F, only enclose Bath-4: (61.75, 26.125, XD_W, 26.5)
text = text.replace(
'''    for r in [
        (78.5, 20.5, 78.875, 27.5),
        (42.125, 20.5, 42.5, 27.5),
        (56.75, 20.5, 57.125, 26.5),
        (61.75, 20.5, 62.125, 26.5),
        (56.75, 26.125, XD_W, 26.5),
        (STAIR_X0, 31.75, MID_X, 32.125)
    ]:''',
'''    for r in [
        (78.5, 20.5, 78.875, 27.5),
        (42.125, 20.5, 42.5, 27.5),
        (56.75, 20.5, 57.125, 26.5),
        (61.75, 20.5, 62.125, 26.5),
        (61.75, 26.125, XD_W, 26.5),
        (STAIR_X0, 31.75, MID_X, 32.125)
    ]:'''
)

Path("scratch/test_revision_6.py").write_text(text, encoding="utf-8")
print("Wrote scratch/test_revision_6.py successfully.")
