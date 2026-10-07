"""
Test full model with OTS court and all checks:
"""
import sys
sys.path.insert(0, '.')
from shapely.geometry import box as sbox
import scripts.daata_hamlet.model as m

# Let's inspect all checks with the update
model = m.build()

# Add the vents
model.openings.append(m.Opening("GF", "y", 51.75, 23.0, 25.0, 6.5, 8.0, "vent", "V"))
model.openings.append(m.Opening("1F", "y", 51.75, 23.0, 25.0, 6.5, 8.0, "vent", "V"))

# Add OTS court to rooms
ots_gf = sbox(46.875, 20.5, m.XC_W, 26.375)
model.rooms.append(m.Room("GF", "LIGHT COURT (OTS)", ots_gf, "ext", (49.1, 23.5)))

# Update foyer_gf in rooms
for i, r in enumerate(model.rooms):
    if r.floor == "GF" and r.name == "ENTRANCE FOYER":
        foyer_gal = m.bc_block.intersection(m.FP_IN).intersection(sbox(45.375, 26.75, m.XC_W, 33.0))
        foyer_main = m.bc_block.intersection(m.FP_IN).intersection(sbox(m.XB_I, 20.5, 46.875, 26.375))
        foyer_gf = m.unary_union([foyer_main, foyer_gal])
        model.rooms[i] = m.Room("GF", "ENTRANCE FOYER", foyer_gf, "circ", (44.5, 23.5), False)

# Run validation with hack removed
orig_validate = m.validate
res = []

# Test all checks
res = m.validate(model, verbose=True)
print("\nValidation passed:", sum(o for o, _ in res), "/", len(res))
