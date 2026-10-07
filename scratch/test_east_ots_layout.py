import sys
import copy
from pathlib import Path
from shapely.geometry import Polygon, box as sbox, Point
from shapely.ops import unary_union

sys.path.insert(0, str(Path.cwd()))
import scripts.daata_hamlet.model as orig_m

print("Reading model.py source...")
source = Path("scripts/daata_hamlet/model.py").read_text(encoding="utf-8")

# Let's see the current GF partitions:
# (46.5, 20.5, 46.875, 26.375) -> old OTS west
# (46.5, 26.375, XC_W, 26.75)  -> old OTS north
# (59.125, 20.5, 59.5, 26.5)   -> old powder east
# (52.125, 26.125, 59.5, 26.5) -> old powder north

# In the NEW layout:
# OTS is at X in [57.125, 61.75], Y in [20.5, 26.5]
# Powder is at X in [62.125, 68.625], Y in [20.5, 26.5]
# Walls needed:
# - West wall of OTS: (56.75, 20.5, 57.125, 26.5)
# - Dividing wall between OTS and Powder: (61.75, 20.5, 62.125, 26.5)
# - North wall of OTS and Powder: (56.75, 26.125, XD_W, 26.5)

print("Target geometry defined.")
