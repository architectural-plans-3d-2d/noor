"""
Test script to explore room rearrangement in model.py.
Goal:
1. Drawing Room in Bay BC (front west, adjacent to Car Porch) with ensuite Powder Room on Line B (direct exterior window).
2. Family Lounge + Dining in Bay CD (front/center) with south daylight windows and direct foyer archway.
3. Bed Room-2 in Bay CD (rear/center) facing quiet North Garden with ensuite bath on North garden wall (direct exterior window).
4. Bed Room-1 in Bay DE (front east) with ensuite bath on Line E (direct exterior window).
5. All 9 bathrooms across all 3 floors have direct exterior windows.
6. Verify all 19 validation check groups pass.
"""
import math
import re
from shapely.geometry import Polygon, box as sbox, Point, LineString
from shapely.ops import unary_union
import sys
sys.path.insert(0, '.')

import scripts.daata_hamlet.model as m_orig

print("Base model imported successfully.")
