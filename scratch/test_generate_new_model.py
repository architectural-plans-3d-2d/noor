import sys
from pathlib import Path
sys.path.insert(0, str(Path.cwd()))

import math
import re
from shapely.geometry import Polygon, box as sbox, Point, LineString
from shapely.ops import unary_union

print("Testing geometry generation...")
