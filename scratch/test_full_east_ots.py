import sys
import copy
from pathlib import Path

# Read existing model.py
path = Path("scripts/daata_hamlet/model.py")
text = path.read_text(encoding="utf-8")

# Let's inspect furniture in model.py:
# lines 370-371:
# circ("GF", 53.5, 22.0, 0.75) # Powder WC
# rect("GF", 55.5, 23.6, 58.85, 25.6) # Powder vanity counter
# In the new layout, Powder is at X in [62.125, 68.625], Y in [20.5, 26.5]:
# WC at (67.0, 22.0), Vanity at (63.0, 24.5, 67.5, 26.0)

# Let's replace furniture:
text = text.replace(
'''    circ("GF", 53.5, 22.0, 0.75)                               # Powder WC
    rect("GF", 55.5, 23.6, 58.85, 25.6)                       # Powder vanity counter''',
'''    circ("GF", 67.0, 22.0, 0.75)                               # Powder WC
    rect("GF", 63.0, 24.5, 67.5, 26.0)                       # Powder vanity counter'''
)

# Replace 1F middle bath fixtures:
# lines 365-367:
# rect(fl, 55.8, 20.8, 58.8, 23.8) # shower 3x3
# circ(fl, 53.5, 21.8, 0.75) # WC
# rect(fl, 53.0, 24.0, 55.5, 25.5) # basin
text = text.replace(
'''        if fl != "GF":
            rect(fl, 55.8, 20.8, 58.8, 23.8)                  # shower 3x3
            circ(fl, 53.5, 21.8, 0.75)                        # WC
            rect(fl, 53.0, 24.0, 55.5, 25.5)                  # basin''',
'''        if fl != "GF":
            rect(fl, 65.0, 20.8, 68.0, 23.8)                  # shower 3x3
            circ(fl, 63.5, 21.8, 0.75)                        # WC
            rect(fl, 63.0, 24.5, 66.0, 26.0)                  # basin'''
)

# Wardrobes in dresses:
# lines 341-344:
# if fl != "GF": rect(fl, 59.5, 25.5, 64.5, 27.5) # Middle dress
# if fl != "2F": rect(fl, 42.5, 25.5, 47.5, 27.5) # West dress
text = text.replace(
'''        if fl != "GF":
            rect(fl, 59.5, 25.5, 64.5, 27.5)                  # Middle dress''',
'''        if fl != "GF":
            rect(fl, 52.5, 24.5, 56.5, 26.5)                  # Middle dress'''
)

# Now GF Partitions:
# lines 448-459:
old_gf_partitions = '''    for r in [
        (73.125, 20.5, 73.5, 27.5),
        (78.5, 20.5, 78.875, 27.5),
        (41.75, 26.75, 42.125, 33.0),
        (46.5, 20.5, 46.875, 26.375),
        (46.5, 26.375, XC_W, 26.75),
        (59.125, 20.5, 59.5, 26.5),
        (52.125, 26.125, 59.5, 26.5),
        (STAIR_X0, 31.75, MID_X, 32.125)
    ]:'''

new_gf_partitions = '''    for r in [
        (73.125, 20.5, 73.5, 27.5),
        (78.5, 20.5, 78.875, 27.5),
        (41.75, 26.75, 42.125, 33.0),
        (56.75, 20.5, 57.125, 26.5),
        (61.75, 20.5, 62.125, 26.5),
        (56.75, 26.125, XD_W, 26.5),
        (STAIR_X0, 31.75, MID_X, 32.125)
    ]:'''

text = text.replace(old_gf_partitions, new_gf_partitions)

# GF Openings:
# lines 472-494
old_gf_openings = '''    op(g, "y", 36.5, 22.0, 26.5, 0.0, 8.0, "double", "MAIN ENTRANCE", "a", 1)
    op(g, "y", 36.5, 28.75, 30.25, 6.5, 8.0, "vent", "V")
    op(g, "y", 51.75, 23.0, 25.0, 6.5, 8.0, "vent", "V"); op(g, "y", 46.6875, 22.0, 25.0, 2.0, 8.0, "window", "W-COURT")
    op(g, "y", 84.75, 22.5, 24.5, 6.5, 8.0, "vent", "V")
    op(g, "y", 84.75, 29.5, 34.5, 1.0, 10.25, "window", "STAIR-GL")
    op(g, "y", 84.75, 38.0, 43.5, 3.5, 7.0, "window", "KW")
    op(g, "y", 84.75, 48.0, 51.0, 0.0, 7.0, "door", "D-COURT", "a", 1)
    op(g, "y", 84.75, 51.5, 53.5, 6.5, 8.0, "vent", "V")
    op(g, "y", 51.75, 35.0, 38.25, 0.0, 8.0, "slide", "SL")
    op(g, "x", 42.125, 60.25, 67.25, 3.0, 8.0, "window", "W3")

    op(g, "x", 20.125, 45.0, 48.0, 0.0, 7.0, "door", "D2", "b", -1)
    op(g, "x", 26.5, 42.0, 44.5, 0.0, 7.0, "door", "D2", "a", 1)
    op(g, "y", 41.9375, 28.5, 31.0, 0.0, 7.0, "door", "D3", "a", 1)
    op(g, "x", 20.125, 54.0, 56.5, 0.0, 7.0, "door", "D3", "a", 1)
    op(g, "x", 20.125, 61.5, 65.0, 0.0, 7.0, "door", "D1", "a", 1)
    op(g, "y", 51.75, 28.5, 32.5, 0.0, 8.0, "arch", "ARCH")'''

new_gf_openings = '''    op(g, "y", 36.5, 22.0, 26.5, 0.0, 8.0, "double", "MAIN ENTRANCE", "a", 1)
    op(g, "y", 36.5, 28.75, 30.25, 6.5, 8.0, "vent", "V")
    op(g, "y", 61.9375, 22.5, 24.5, 6.5, 8.0, "vent", "V")
    op(g, "x", 26.3125, 57.5, 61.0, 2.5, 7.5, "window", "W-COURT")
    op(g, "y", 84.75, 22.5, 24.5, 6.5, 8.0, "vent", "V")
    op(g, "y", 84.75, 29.5, 34.5, 1.0, 10.25, "window", "STAIR-GL")
    op(g, "y", 84.75, 38.0, 43.5, 3.5, 7.0, "window", "KW")
    op(g, "y", 84.75, 48.0, 51.0, 0.0, 7.0, "door", "D-COURT", "a", 1)
    op(g, "y", 84.75, 51.5, 53.5, 6.5, 8.0, "vent", "V")
    op(g, "y", 51.75, 35.0, 38.25, 0.0, 8.0, "slide", "SL")
    op(g, "x", 42.125, 60.25, 67.25, 3.0, 8.0, "window", "W3")

    op(g, "x", 20.125, 45.0, 48.0, 0.0, 7.0, "door", "D2", "b", -1)
    op(g, "x", 26.5, 42.0, 44.5, 0.0, 7.0, "door", "D2", "a", 1)
    op(g, "y", 41.9375, 28.5, 31.0, 0.0, 7.0, "door", "D3", "a", 1)
    op(g, "x", 20.125, 63.5, 66.0, 0.0, 7.0, "door", "D3", "a", 1)
    op(g, "x", 20.125, 53.0, 56.5, 0.0, 7.0, "door", "D1", "a", 1)
    op(g, "y", 51.75, 21.0, 26.5, 0.0, 8.5, "arch", "GRAND ARCH")
    op(g, "y", 51.75, 28.5, 32.5, 0.0, 8.5, "arch", "ARCH")'''

text = text.replace(old_gf_openings, new_gf_openings)

# GF Rooms:
# lines 500-514
old_gf_rooms = '''    powder_gf = R(XC_E, 20.5, 59.125, 26.5)
    room(g, "POWDER", powder_gf, "wet", (55.6, 23.5))
    lounge_gf = R(XC_E, 20.5, XD_W, 41.75).intersection(FP_IN).difference(R(XC_E, 20.5, 59.5, 26.5))
    room(g, "LOUNGE + DINING", lounge_gf, "hab", (62.0, 32.0))

    room(g, "BED ROOM-2", R(XB_I, 3.75, XC_W, 19.75), "hab")
    bath_gf = bc_block.intersection(FP_IN).intersection(sbox(XB_I, 26.75, 41.75, 33.0))
    room(g, "BATH", bath_gf, "wet", (39.5, 29.5))
    room(g, "DRESS", R(42.125, 26.75, 45.0, 33.0), "serv", (43.5, 29.5), False)
    ots_gf = sbox(46.875, 20.5, XC_W, 26.375)
    room(g, "LIGHT COURT (OTS)", ots_gf, "ext", (49.1, 23.5))
    foyer_gal = bc_block.intersection(FP_IN).intersection(sbox(45.375, 26.75, XC_W, 33.0))
    foyer_main = bc_block.intersection(FP_IN).intersection(sbox(XB_I, 20.5, 46.5, 26.375))
    foyer_gf = unary_union([foyer_main, foyer_gal])
    room(g, "ENTRANCE FOYER", foyer_gf, "circ", (39.5, 23.5), False)'''

new_gf_rooms = '''    powder_gf = R(62.125, 20.5, XD_W, 26.5)
    room(g, "POWDER", powder_gf, "wet", (65.4, 23.5))
    ots_gf = sbox(57.125, 20.5, 61.75, 26.5)
    room(g, "LIGHT COURT (OTS)", ots_gf, "ext", (59.4, 23.5))
    lounge_gf = R(XC_E, 20.5, XD_W, 41.75).intersection(FP_IN).difference(R(56.75, 20.5, XD_W, 26.5))
    room(g, "LOUNGE + DINING", lounge_gf, "hab", (62.0, 34.0))

    room(g, "BED ROOM-2", R(XB_I, 3.75, XC_W, 19.75), "hab")
    bath_gf = bc_block.intersection(FP_IN).intersection(sbox(XB_I, 26.75, 41.75, 33.0))
    room(g, "BATH", bath_gf, "wet", (39.5, 29.5))
    room(g, "DRESS", R(42.125, 26.75, 45.0, 33.0), "serv", (43.5, 29.5), False)
    foyer_gf = bc_block.intersection(FP_IN).intersection(sbox(XB_I, 20.5, XC_W, 33.0)).difference(sbox(XB_I, 26.375, 45.375, 33.0))
    room(g, "ENTRANCE FOYER", foyer_gf, "circ", (44.0, 23.5), False)'''

text = text.replace(old_gf_rooms, new_gf_rooms)

# 1F Partitions:
# lines 545-555
old_1f_partitions = '''    for r in [
        (73.125, 20.5, 73.5, 27.5),
        (78.5, 20.5, 78.875, 27.5),
        (42.125, 20.5, 42.5, 27.5),
        (46.5, 20.5, 46.875, 26.375),
        (46.5, 26.375, XC_W, 26.75),
        (59.125, 20.5, 59.5, 26.5),
        (52.125, 26.125, 59.5, 26.5),
        (64.5, 20.5, 64.875, 27.5),
        (STAIR_X0, 31.75, MID_X, 32.125)
    ]:'''

new_1f_partitions = '''    for r in [
        (73.125, 20.5, 73.5, 27.5),
        (78.5, 20.5, 78.875, 27.5),
        (42.125, 20.5, 42.5, 27.5),
        (47.5, 20.5, 47.875, 27.5),
        (56.75, 20.5, 57.125, 26.5),
        (61.75, 20.5, 62.125, 26.5),
        (56.75, 26.125, XD_W, 26.5),
        (STAIR_X0, 31.75, MID_X, 32.125)
    ]:'''

text = text.replace(old_1f_partitions, new_1f_partitions)

# 1F Openings:
# lines 570
text = text.replace('op(f, "y", 51.75, 23.0, 25.0, 6.5, 8.0, "vent", "V")',
                    'op(f, "y", 61.9375, 22.5, 24.5, 6.5, 8.0, "vent", "V")')

# 1F Doors for Bed-4:
# old:
# op(f, "x", 20.125, 60.75, 63.25, 0.0, 7.0, "door", "D3", "a", 1)
# op(f, "x", 20.125, 65.25, 68.25, 0.0, 7.0, "door", "D2", "b", -1)
# op(f, "y", 59.3125, 22.0, 24.5, 0.0, 7.0, "door", "D3", "b", -1)
# op(f, "x", 27.875, 65.25, 68.25, 0.0, 7.0, "door", "D2", "b", 1)
old_1f_doors = '''    op(f, "x", 20.125, 60.75, 63.25, 0.0, 7.0, "door", "D3", "a", 1)
    op(f, "x", 20.125, 65.25, 68.25, 0.0, 7.0, "door", "D2", "b", -1)
    op(f, "y", 59.3125, 22.0, 24.5, 0.0, 7.0, "door", "D3", "b", -1)
    op(f, "x", 27.875, 65.25, 68.25, 0.0, 7.0, "door", "D2", "b", 1)'''

new_1f_doors = '''    op(f, "x", 20.125, 53.0, 56.0, 0.0, 7.0, "door", "D2", "a", 1)
    op(f, "x", 26.3125, 63.5, 66.0, 0.0, 7.0, "door", "D3", "b", 1)
    op(f, "x", 27.875, 53.0, 56.0, 0.0, 7.0, "door", "D2", "b", 1)'''

text = text.replace(old_1f_doors, new_1f_doors)

# 1F Rooms:
# lines 598-608
old_1f_rooms = '''    room(f, "BED ROOM-4", R(XC_E, 3.75, XD_W, 19.75), "hab")
    b4_bath = R(XC_E, 20.5, 59.125, 26.5)
    room(f, "BATH", b4_bath, "wet", (56.0, 23.5))
    room(f, "DRESS", R(59.5, 20.5, 64.5, 27.5), "serv")
    room(f, "LOBBY", R(64.875, 20.5, XD_W, 27.5), "circ", show_dims=False)
    room(f, "BED ROOM-5", R(XB_I, 3.75, XC_W, 19.75), "hab")
    room(f, "BATH", R(XB_I, 20.5, 42.125, 27.5), "wet")
    room(f, "DRESS", R(42.5, 20.5, 46.5, 27.5), "serv", (44.5, 23.5))
    ots_1f = sbox(46.875, 20.5, XC_W, 26.375)
    room(f, "LIGHT COURT (OTS)", ots_1f, "ext", (49.1, 23.5))
    room(f, "LOBBY", R(46.875, 26.375, XC_W, 27.5), "circ", show_dims=False)'''

new_1f_rooms = '''    room(f, "BED ROOM-4", R(XC_E, 3.75, XD_W, 19.75), "hab")
    b4_bath = R(62.125, 20.5, XD_W, 26.5)
    room(f, "BATH", b4_bath, "wet", (65.4, 23.5))
    ots_1f = sbox(57.125, 20.5, 61.75, 26.5)
    room(f, "LIGHT COURT (OTS)", ots_1f, "ext", (59.4, 23.5))
    room(f, "DRESS", R(XC_E, 20.5, 56.75, 27.5), "serv", (54.5, 23.5))
    room(f, "LOBBY", R(56.75, 26.5, XD_W, 27.5), "circ", show_dims=False)
    room(f, "BED ROOM-5", R(XB_I, 3.75, XC_W, 19.75), "hab")
    room(f, "BATH", R(XB_I, 20.5, 42.125, 27.5), "wet")
    room(f, "DRESS", R(42.5, 20.5, 47.5, 27.5), "serv", (45.0, 23.5))
    room(f, "LOBBY", R(47.5, 20.5, XC_W, 27.5), "circ", show_dims=False)'''

text = text.replace(old_1f_rooms, new_1f_rooms)

# 2F Partitions:
# lines 637-639:
old_2f_partitions = '''        (59.125, 20.5, 59.5, 26.5),
        (52.125, 26.125, 59.5, 26.5),
        (64.5, 20.5, 64.875, 27.5),'''

new_2f_partitions = '''        (56.75, 20.5, 57.125, 26.5),
        (61.75, 20.5, 62.125, 26.5),
        (56.75, 26.125, XD_W, 26.5),'''

text = text.replace(old_2f_partitions, new_2f_partitions)

# 2F Openings:
# line 650:
text = text.replace('op(s, "y", 51.75, 23.0, 25.0, 6.5, 8.0, "vent", "V")',
                    'op(s, "y", 61.9375, 22.5, 24.5, 6.5, 8.0, "vent", "V")')

# 2F Doors:
# lines 657-660:
old_2f_doors = '''    op(s, "x", 20.125, 60.75, 63.25, 0.0, 7.0, "door", "D3", "a", 1)
    op(s, "x", 20.125, 65.25, 68.25, 0.0, 7.0, "door", "D2", "b", -1)
    op(s, "y", 59.3125, 22.0, 24.5, 0.0, 7.0, "door", "D3", "b", -1)
    op(s, "x", 27.875, 65.25, 68.25, 0.0, 7.0, "door", "D1", "b", 1)'''

new_2f_doors = '''    op(s, "x", 20.125, 53.0, 56.0, 0.0, 7.0, "door", "D2", "a", 1)
    op(s, "x", 26.3125, 63.5, 66.0, 0.0, 7.0, "door", "D3", "a", 1)
    op(s, "x", 27.875, 53.0, 56.0, 0.0, 7.0, "door", "D1", "b", 1)'''

text = text.replace(old_2f_doors, new_2f_doors)

# 2F Rooms:
# lines 675-679:
old_2f_rooms = '''    room(s, "BED ROOM-7", R(XC_E, 3.75, XD_W, 19.75), "hab")
    b7_bath = R(XC_E, 20.5, 59.125, 26.5)
    room(s, "BATH", b7_bath, "wet", (56.0, 23.5))
    room(s, "DRESS", R(59.5, 20.5, 64.5, 27.5), "serv")
    room(s, "LOBBY", R(64.875, 20.5, XD_W, 27.5), "circ", show_dims=False)'''

new_2f_rooms = '''    room(s, "BED ROOM-7", R(XC_E, 3.75, XD_W, 19.75), "hab")
    b7_bath = R(62.125, 20.5, XD_W, 26.5)
    room(s, "BATH", b7_bath, "wet", (65.4, 23.5))
    ots_2f = sbox(57.125, 20.5, 61.75, 26.5)
    room(s, "LIGHT COURT (OTS)", ots_2f, "ext", (59.4, 23.5))
    room(s, "DRESS", R(XC_E, 20.5, 56.75, 27.5), "serv", (54.5, 23.5))
    room(s, "LOBBY", R(56.75, 26.5, XD_W, 27.5), "circ", show_dims=False)'''

text = text.replace(old_2f_rooms, new_2f_rooms)

# Slabs ots_hole:
# line 756:
text = text.replace('ots_hole = sbox(46.875, 20.5, XC_W, 26.375)',
                    'ots_hole = sbox(57.125, 20.5, 61.75, 26.5)')

Path("scratch/test_model_full.py").write_text(text, encoding="utf-8")
print("Wrote scratch/test_model_full.py successfully.")
