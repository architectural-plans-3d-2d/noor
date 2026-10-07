"""
Test implementation of the Swapped Layout for Daata Hamlet:
- Bay BC: Drawing Room (front, 14.5' x 18.0' = 261 sq.ft >= 260 sq.ft) with ensuite Powder Room on Line B (direct exterior window).
          Main Entrance Foyer on Line B with straight 6' arch into Lounge.
- Bay CD: Family Lounge & Dining (front/center, 16.5' x 21.0' = 346 sq.ft).
          Bed Room-2 (rear/center, 16.5' x 14.5' = 239 sq.ft >= 14.5' x 16') facing quiet North Garden.
          Ensuite Bath on Line C (North garden exterior wall, direct exterior window).
- Bay DE: Bed Room-1 (front east, 15.0' x 16.0' = 240 sq.ft) with ensuite Bath on Line E (East Passage).
          Stair, Kitchen, Dirty Kitchen.
"""
import math
import re
from shapely.geometry import Polygon, box as sbox, Point, LineString
from shapely.ops import unary_union
import sys
sys.path.insert(0, '.')

import scripts.daata_hamlet.model as orig

# Test if we can configure this in Model
print("Script template ready.")
