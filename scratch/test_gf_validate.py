import sys
sys.path.insert(0, ".")
import math
from shapely.geometry import box as sbox, Polygon, Point, LineString
from shapely.ops import unary_union
import scripts.daata_hamlet.model as dhm

def test_config():
    # Let's inspect the current walls in GF Bay BC:
    # In model.py:
    # (XB_I, 27.5, XC_W, 28.25) -> wall at Y=27.5 to 28.25
    # Partitions:
    # (42.125, 20.5, 42.5, 27.5)
    # (47.5, 20.5, 47.875, 27.5)
    print("Checking current walls and rooms in GF Bay BC...")

test_config()
