import sys
from pathlib import Path
sys.path.insert(0, str(Path.cwd()))

import math
import re
from dataclasses import dataclass, field
from shapely.geometry import Polygon, box as sbox, Point, LineString
from shapely.ops import unary_union

from scripts.daata_hamlet.model import (
    SITE_POINTS, SURVEY_SEGMENTS, PLOT, PLOT_INNER, BUILD, east_bx,
    ROAD_Z, GRADE_Z, FLOORS, LEVEL, FLOOR_H, SLAB_T, BEAM_D, WALL_H,
    MUMTY_TOP, PARAPET_H, T9, T45, fi
)

print("Building test full model script...")
