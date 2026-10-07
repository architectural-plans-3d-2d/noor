import sys
from pathlib import Path

# Add repository root
sys.path.insert(0, str(Path.cwd()))
import scripts.daata_hamlet.model as orig_m

text = Path("scripts/daata_hamlet/model.py").read_text(encoding="utf-8")

# Let's inspect changes:
# 1. GF:
# Remove (73.125, 20.5, 73.5, 27.5) from partitions
text = text.replace(
'''    for r in [
        (73.125, 20.5, 73.5, 27.5),
        (78.5, 20.5, 78.875, 27.5),
        (41.75, 26.75, 42.125, 33.0),
        (56.75, 20.5, 57.125, 26.5),
        (61.75, 20.5, 62.125, 26.5),
        (56.75, 26.125, XD_W, 26.5),
        (STAIR_X0, 31.75, MID_X, 32.125)
    ]:''',
'''    for r in [
        (78.5, 20.5, 78.875, 27.5),
        (41.75, 26.75, 42.125, 33.0),
        (56.75, 20.5, 57.125, 26.5),
        (61.75, 20.5, 62.125, 26.5),
        (56.75, 26.125, XD_W, 26.5),
        (STAIR_X0, 31.75, MID_X, 32.125)
    ]:'''
)

# GF Openings:
# Bed-1 door at Y=20.125: widen to 3'-6" at X in [70.0, 73.5]
# Bed-1 bath door: on wall X=78.6875, Y in [22.0, 25.0]
# Bed-2 door at Y=20.125: widen to 3'-6" at X in [43.5, 47.0]
text = text.replace(
'''    op(g, "x", 20.125, 45.0, 48.0, 0.0, 7.0, "door", "D2", "b", -1)
    op(g, "x", 26.5, 42.0, 44.5, 0.0, 7.0, "door", "D2", "a", 1)
    op(g, "y", 41.9375, 28.5, 31.0, 0.0, 7.0, "door", "D3", "a", 1)
    op(g, "x", 20.125, 63.5, 66.0, 0.0, 7.0, "door", "D3", "a", 1)
    op(g, "x", 20.125, 53.0, 56.5, 0.0, 7.0, "door", "D1", "a", 1)
    op(g, "y", 51.75, 21.0, 26.5, 0.0, 8.5, "arch", "GRAND ARCH")
    op(g, "y", 51.75, 28.5, 32.5, 0.0, 8.5, "arch", "ARCH")
    op(g, "y", 69.0, 37.5, 41.0, 0.0, 7.0, "door", "D1", "b", 1)
    op(g, "x", 46.5, 74.0, 77.0, 0.0, 7.0, "door", "D2", "a", 1)
    op(g, "x", 20.125, 69.75, 72.75, 0.0, 7.0, "door", "D2", "a", -1)
    op(g, "x", 20.125, 74.75, 77.25, 0.0, 7.0, "door", "D3", "b", 1)
    op(g, "y", 78.6875, 22.0, 24.5, 0.0, 7.0, "door", "D3", "b", 1)''',
'''    op(g, "x", 20.125, 43.5, 47.0, 0.0, 7.0, "door", "D2", "b", -1)
    op(g, "x", 26.5, 42.0, 44.5, 0.0, 7.0, "door", "D2", "a", 1)
    op(g, "y", 41.9375, 28.5, 31.0, 0.0, 7.0, "door", "D3", "a", 1)
    op(g, "x", 20.125, 63.5, 66.0, 0.0, 7.0, "door", "D3", "a", 1)
    op(g, "x", 20.125, 53.0, 56.5, 0.0, 7.0, "door", "D1", "a", 1)
    op(g, "y", 51.75, 21.0, 26.5, 0.0, 8.5, "arch", "GRAND ARCH")
    op(g, "y", 51.75, 28.5, 32.5, 0.0, 8.5, "arch", "ARCH")
    op(g, "y", 69.0, 37.5, 41.0, 0.0, 7.0, "door", "D1", "b", 1)
    op(g, "x", 46.5, 74.0, 77.0, 0.0, 7.0, "door", "D2", "a", 1)
    op(g, "x", 20.125, 70.0, 73.5, 0.0, 7.0, "door", "D2", "a", -1)
    op(g, "y", 78.6875, 22.5, 25.5, 0.0, 7.0, "door", "D3", "b", 1)'''
)

# GF Rooms:
# Merge Dress and Lobby for Bed-1
text = text.replace(
'''    room(g, "BED ROOM-1", R(XD_E, 3.75, XE_I, 19.75), "hab")
    room(g, "BATH", R(78.875, 20.5, XE_I, 27.5), "wet")
    room(g, "DRESS", R(73.5, 20.5, 78.5, 27.5), "serv")
    room(g, "LOBBY", R(XD_E, 20.5, 73.125, 27.5), "circ", show_dims=False)''',
'''    room(g, "BED ROOM-1", R(XD_E, 3.75, XE_I, 19.75), "hab")
    room(g, "BATH", R(78.875, 20.5, XE_I, 27.5), "wet")
    room(g, "DRESS & FOYER", R(XD_E, 20.5, 78.5, 27.5), "circ", (74.0, 24.0))'''
)

# 2. 1F:
# Remove (73.125, 20.5, 73.5, 27.5) and (47.5, 20.5, 47.875, 27.5)
text = text.replace(
'''    for r in [
        (73.125, 20.5, 73.5, 27.5),
        (78.5, 20.5, 78.875, 27.5),
        (42.125, 20.5, 42.5, 27.5),
        (47.5, 20.5, 47.875, 27.5),
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
        (56.75, 26.125, XD_W, 26.5),
        (STAIR_X0, 31.75, MID_X, 32.125)
    ]:'''
)

# 1F Openings:
old_1f_ops = '''    op(f, "x", 20.125, 43.75, 46.25, 0.0, 7.0, "door", "D3", "a", 1)
    op(f, "x", 20.125, 48.125, 51.125, 0.0, 7.0, "door", "D2", "b", -1)
    op(f, "y", 42.3125, 22.0, 24.5, 0.0, 7.0, "door", "D3", "b", -1)
    op(f, "x", 27.875, 48.125, 51.125, 0.0, 7.0, "door", "D2", "b", 1)
    op(f, "x", 20.125, 53.0, 56.0, 0.0, 7.0, "door", "D2", "a", 1)
    op(f, "x", 26.3125, 63.5, 66.0, 0.0, 7.0, "door", "D3", "b", 1)
    op(f, "x", 27.875, 53.0, 56.0, 0.0, 7.0, "door", "D2", "b", 1)
    op(f, "x", 20.125, 69.75, 72.75, 0.0, 7.0, "door", "D2", "a", -1)
    op(f, "x", 20.125, 74.75, 77.25, 0.0, 7.0, "door", "D3", "b", 1)
    op(f, "y", 78.6875, 22.0, 24.5, 0.0, 7.0, "door", "D3", "b", 1)
    op(f, "y", 69.0, 21.0, 26.5, 0.0, 7.0, "arch", "ARCH")'''

new_1f_ops = '''    op(f, "y", 42.3125, 22.5, 25.5, 0.0, 7.0, "door", "D3", "b", -1)
    op(f, "x", 20.125, 44.0, 47.5, 0.0, 7.0, "door", "D2", "b", -1)
    op(f, "x", 27.875, 44.0, 47.5, 0.0, 7.0, "door", "D2", "b", 1)
    op(f, "x", 20.125, 53.0, 56.5, 0.0, 7.0, "door", "D2", "a", 1)
    op(f, "x", 20.125, 63.5, 66.0, 0.0, 7.0, "door", "D3", "a", 1)
    op(f, "x", 27.875, 53.0, 56.5, 0.0, 7.0, "door", "D2", "b", 1)
    op(f, "x", 20.125, 70.0, 73.5, 0.0, 7.0, "door", "D2", "a", -1)
    op(f, "y", 78.6875, 22.5, 25.5, 0.0, 7.0, "door", "D3", "b", 1)
    op(f, "y", 69.0, 21.0, 26.5, 0.0, 7.0, "arch", "ARCH")'''

text = text.replace(old_1f_ops, new_1f_ops)

# 1F Rooms:
old_1f_rms = '''    room(f, "BED ROOM-3", R(XD_E, 3.75, XE_I, 19.75), "hab")
    room(f, "BATH", R(78.875, 20.5, XE_I, 27.5), "wet")
    room(f, "DRESS", R(73.5, 20.5, 78.5, 27.5), "serv")
    room(f, "LOBBY", R(XD_E, 20.5, 73.125, 27.5), "circ", show_dims=False)
    room(f, "BED ROOM-4", R(XC_E, 3.75, XD_W, 19.75), "hab")
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

new_1f_rms = '''    room(f, "BED ROOM-3", R(XD_E, 3.75, XE_I, 19.75), "hab")
    room(f, "BATH", R(78.875, 20.5, XE_I, 27.5), "wet")
    room(f, "DRESS & FOYER", R(XD_E, 20.5, 78.5, 27.5), "circ", (74.0, 24.0))
    room(f, "BED ROOM-4", R(XC_E, 3.75, XD_W, 19.75), "hab")
    b4_bath = R(62.125, 20.5, XD_W, 26.5)
    room(f, "BATH", b4_bath, "wet", (65.4, 23.5))
    ots_1f = sbox(57.125, 20.5, 61.75, 26.5)
    room(f, "LIGHT COURT (OTS)", ots_1f, "ext", (59.4, 23.5))
    room(f, "PRIVATE FOYER", R(XC_E, 20.5, 56.75, 27.5), "circ", (54.5, 24.0), False)
    room(f, "BED ROOM-5", R(XB_I, 3.75, XC_W, 19.75), "hab")
    room(f, "BATH", R(XB_I, 20.5, 42.125, 27.5), "wet")
    room(f, "DRESS & FOYER", R(42.5, 20.5, XC_W, 27.5), "circ", (47.0, 24.0))'''

text = text.replace(old_1f_rms, new_1f_rms)

# 3. 2F:
# Remove (73.125, 20.5, 73.5, 27.5) from 2F partitions
text = text.replace(
'''    for r in [
        (73.125, 20.5, 73.5, 27.5),
        (78.5, 20.5, 78.875, 27.5),
        (56.75, 20.5, 57.125, 26.5),
        (61.75, 20.5, 62.125, 26.5),
        (56.75, 26.125, XD_W, 26.5),
        (79.0, 36.375, 79.375, 46.125),
        (79.375, 41.5, XE_I, 41.875),
        (STAIR_X0, 31.75, MID_X, 32.125)
    ]:''',
'''    for r in [
        (78.5, 20.5, 78.875, 27.5),
        (56.75, 20.5, 57.125, 26.5),
        (61.75, 20.5, 62.125, 26.5),
        (56.75, 26.125, XD_W, 26.5),
        (79.0, 36.375, 79.375, 46.125),
        (79.375, 41.5, XE_I, 41.875),
        (STAIR_X0, 31.75, MID_X, 32.125)
    ]:'''
)

# 2F Openings:
old_2f_ops = '''    op(s, "x", 20.125, 53.0, 56.0, 0.0, 7.0, "door", "D2", "a", 1)
    op(s, "x", 26.3125, 63.5, 66.0, 0.0, 7.0, "door", "D3", "a", 1)
    op(s, "x", 27.875, 53.0, 56.0, 0.0, 7.0, "door", "D1", "b", 1)
    op(s, "y", 69.0, 21.0, 26.5, 0.0, 7.0, "arch", "ARCH")
    op(s, "x", 20.125, 69.75, 72.75, 0.0, 7.0, "door", "D2", "a", -1)
    op(s, "x", 20.125, 74.75, 77.25, 0.0, 7.0, "door", "D3", "b", 1)
    op(s, "y", 78.6875, 22.0, 24.5, 0.0, 7.0, "door", "D3", "b", 1)'''

new_2f_ops = '''    op(s, "x", 20.125, 53.0, 56.5, 0.0, 7.0, "door", "D2", "a", 1)
    op(s, "x", 20.125, 63.5, 66.0, 0.0, 7.0, "door", "D3", "a", 1)
    op(s, "x", 27.875, 53.0, 56.5, 0.0, 7.0, "door", "D1", "b", 1)
    op(s, "y", 69.0, 21.0, 26.5, 0.0, 7.0, "arch", "ARCH")
    op(s, "x", 20.125, 70.0, 73.5, 0.0, 7.0, "door", "D2", "a", -1)
    op(s, "y", 78.6875, 22.5, 25.5, 0.0, 7.0, "door", "D3", "b", 1)'''

text = text.replace(old_2f_ops, new_2f_ops)

# 2F Rooms:
old_2f_rms = '''    room(s, "BED ROOM-6", R(XD_E, 3.75, XE_I, 19.75), "hab")
    room(s, "BATH", R(78.875, 20.5, XE_I, 27.5), "wet")
    room(s, "DRESS", R(73.5, 20.5, 78.5, 27.5), "serv")
    room(s, "LOBBY", R(XD_E, 20.5, 73.125, 27.5), "circ", show_dims=False)
    room(s, "BED ROOM-7", R(XC_E, 3.75, XD_W, 19.75), "hab")
    b7_bath = R(62.125, 20.5, XD_W, 26.5)
    room(s, "BATH", b7_bath, "wet", (65.4, 23.5))
    ots_2f = sbox(57.125, 20.5, 61.75, 26.5)
    room(s, "LIGHT COURT (OTS)", ots_2f, "ext", (59.4, 23.5))
    room(s, "DRESS", R(XC_E, 20.5, 56.75, 27.5), "serv", (54.5, 23.5))
    room(s, "LOBBY", R(56.75, 26.5, XD_W, 27.5), "circ", show_dims=False)'''

new_2f_rms = '''    room(s, "BED ROOM-6", R(XD_E, 3.75, XE_I, 19.75), "hab")
    room(s, "BATH", R(78.875, 20.5, XE_I, 27.5), "wet")
    room(s, "DRESS & FOYER", R(XD_E, 20.5, 78.5, 27.5), "circ", (74.0, 24.0))
    room(s, "BED ROOM-7", R(XC_E, 3.75, XD_W, 19.75), "hab")
    b7_bath = R(62.125, 20.5, XD_W, 26.5)
    room(s, "BATH", b7_bath, "wet", (65.4, 23.5))
    ots_2f = sbox(57.125, 20.5, 61.75, 26.5)
    room(s, "LIGHT COURT (OTS)", ots_2f, "ext", (59.4, 23.5))
    room(s, "PRIVATE FOYER", R(XC_E, 20.5, 56.75, 27.5), "circ", (54.5, 24.0), False)'''

text = text.replace(old_2f_rms, new_2f_rms)

# Wardrobes in furnish:
# Update wardrobe rects in furnish to match the new open suites
text = text.replace(
'''        # Wardrobes in dresses:
        rect(fl, 73.5, 25.5, 78.5, 27.5)                      # East dress
        if fl != "GF":
            rect(fl, 52.5, 24.5, 56.5, 26.5)                  # Middle dress
        if fl != "2F":
            rect(fl, 42.5, 25.5, 47.5, 27.5)                  # West dress''',
'''        # Wardrobes in master suites:
        rect(fl, 74.5, 25.5, 78.5, 27.5, "WARDROBE")         # East dress
        if fl != "GF":
            rect(fl, 52.5, 17.5, 56.5, 19.5, "WARDROBE")     # Middle bed wardrobe
        if fl != "2F":
            rect(fl, 43.0, 25.5, 47.0, 27.5, "WARDROBE")     # West dress'''
)

Path("scratch/test_uncongested_model.py").write_text(text, encoding="utf-8")
print("Wrote scratch/test_uncongested_model.py successfully.")
