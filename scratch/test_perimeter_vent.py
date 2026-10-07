"""
Test script for the perimeter-ventilated layout:
- GF Powder Room located in Bay BC on Line B (X = 36.875 to 42.0, Y = 20.5 to 25.0)
  with direct vent V on Line B (X = 36.5, Y = 21.5 to 24.0) opening to open air.
  Powder Anteroom/Vanity at X = 42.0 to 51.375, Y = 20.5 to 25.0 entered from Drawing Room
  via door D3 on Line C (or north wall).
- Main Entrance double doors on Line B at Y = 25.5 to 30.0.
  Grand Foyer Hallway running straight to Line C (X = 51.75, Y = 25.5 to 31.0) into Lounge.
- Bed-2 Bath at NW chamfer with window W-BATH.
- Lounge in Bay CD from Y = 20.5 to 41.75 is completely monolithic (no powder room protrusion).
- Check that all 121 checks pass!
"""
import sys
sys.path.insert(0, '.')
from scripts.daata_hamlet.model import *

print("Starting test...")
