"""
Complete test of Solution 1:
Rearranging Ground Floor and First Floor:
GF:
- Bay BC:
  - Drawing Room: X in [36.875, 51.375], Y in [3.75, 21.75] -> 14.5' x 18.0' = 261.0 sft (>= 260 sft).
  - Powder Room: X in [36.875, 42.0], Y in [21.75, 27.25] -> on Line B (X = 36.5), real vent opening to outside air.
  - Entrance Foyer: X in [42.375, 51.375], Y in [21.75, 27.25] & X in [36.875, 51.375], Y in [27.25, 33.0].
    Main Entrance double doors on Line B (X = 36.5, Y in [27.75, 32.25]).
    Grand 6' arch on Line C (X = 51.75, Y in [27.0, 33.0]) straight into Lounge.
- Bay CD:
  - Family Lounge & Dining: X in [52.125, 68.625], Y in [3.75, 26.5] -> 16.5' x 22.75' = 375.4 sft.
  - Bed Room-2: X in [52.125, 68.625], Y in [27.25, 41.75] -> 16.5' x 14.5' = 239.3 sft (>= 14.5' x 16').
  - Bed-2 Bath: on Line C (X = 51.75, Y in [34.0, 39.5]) -> exterior wall facing garden!
- Bay DE:
  - Bed Room-1: X in [69.375, 84.375], Y in [3.75, 19.75] -> 15.0' x 16.0' = 240 sft.
  - Bed-1 Bath: on Line E (X = 84.75).
"""
import sys
sys.path.insert(0, '.')
import scripts.daata_hamlet.model as m_mod

print("Testing geometry feasibility...")
