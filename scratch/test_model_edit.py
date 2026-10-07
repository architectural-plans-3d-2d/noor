import re
from pathlib import Path

path = Path("scripts/daata_hamlet/model.py")
text = path.read_text(encoding="utf-8")

# 1. Car porch labels
text = text.replace('rect("GF", 19.6, 1.0, 25.8, 16.5, "CAR"); rect("GF", 28.4, 1.0, 34.6, 16.5, "CAR")',
                    'rect("GF", 19.6, 1.0, 25.8, 16.5, ""); rect("GF", 28.4, 1.0, 34.6, 16.5, "")')

# 2. Partitions on GF
old_gf_part = """    for r in [
        (73.125, 20.5, 73.5, 27.5),
        (78.5, 20.5, 78.875, 27.5),
        (41.75, 26.75, 42.125, 33.0),
        (59.125, 20.5, 59.5, 26.5),
        (52.125, 26.125, 59.5, 26.5),
        (STAIR_X0, 31.75, MID_X, 32.125)
    ]:"""

new_gf_part = """    for r in [
        (73.125, 20.5, 73.5, 27.5),
        (78.5, 20.5, 78.875, 27.5),
        (41.75, 26.75, 42.125, 33.0),
        (46.5, 20.5, 46.875, 26.375),
        (46.5, 26.375, XC_W, 26.75),
        (59.125, 20.5, 59.5, 26.5),
        (52.125, 26.125, 59.5, 26.5),
        (STAIR_X0, 31.75, MID_X, 32.125)
    ]:"""

text = text.replace(old_gf_part, new_gf_part)

# 3. Partitions on 1F
old_1f_part = """        (42.125, 20.5, 42.5, 27.5),
        (47.5, 20.5, 47.875, 27.5),"""

new_1f_part = """        (42.125, 20.5, 42.5, 27.5),
        (46.5, 20.5, 46.875, 26.375),
        (46.5, 26.375, XC_W, 26.75),"""

text = text.replace(old_1f_part, new_1f_part)

# 4. 1F Bed-5 dress
text = text.replace('room(f, "DRESS", R(42.5, 20.5, 47.5, 27.5), "serv")',
                    'room(f, "DRESS", R(42.5, 20.5, 46.5, 27.5), "serv", (44.5, 23.5))')

# 5. GF Foyer
text = text.replace('foyer_main = bc_block.intersection(FP_IN).intersection(sbox(XB_I, 20.5, 46.875, 26.375))',
                    'foyer_main = bc_block.intersection(FP_IN).intersection(sbox(XB_I, 20.5, 46.5, 26.375))')

text = text.replace('room(g, "ENTRANCE FOYER", foyer_gf, "circ", (42.0, 23.5), False)',
                    'room(g, "ENTRANCE FOYER", foyer_gf, "circ", (39.5, 23.5), False)')

# Add W-COURT window
old_gf_vent = 'op(g, "y", 51.75, 23.0, 25.0, 6.5, 8.0, "vent", "V")'
new_gf_vent = 'op(g, "y", 51.75, 23.0, 25.0, 6.5, 8.0, "vent", "V"); op(g, "y", 46.6875, 22.0, 25.0, 2.0, 8.0, "window", "W-COURT")'
text = text.replace(old_gf_vent, new_gf_vent)

Path("scratch/test_model.py").write_text(text, encoding="utf-8")
print("Saved scratch/test_model.py")
