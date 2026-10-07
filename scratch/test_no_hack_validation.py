"""
Test script to run the full validation suite with:
1. GF Powder vent on Line C added.
2. 1F Bed-4 Bath vent on Line C added.
3. The hack in check 14 (lines 1007-1008 of model.py) REMOVED completely!
"""
import sys
sys.path.insert(0, '.')
import scripts.daata_hamlet.model as m

# Let's monkeypatch build() to add the vents, and monkeypatch validate() to remove the hack
orig_build = m.build
def new_build():
    model = orig_build()
    # Add vent for GF Powder
    model.openings.append(m.Opening("GF", "y", 51.75, 22.5, 24.5, 6.5, 8.0, "vent", "V-POWDER"))
    # Add vent for 1F Bed-4 Bath
    model.openings.append(m.Opening("1F", "y", 51.75, 22.5, 24.5, 6.5, 8.0, "vent", "V-B4"))
    return model

m.build = new_build

# Test validation with hack removed:
model = m.build()

# Check 14 without hack:
res14 = []
for fl in m.FLOORS:
    wet_rooms = [r for r in model.rooms if r.floor == fl and r.kind == "wet"]
    for wr in wet_rooms:
        has_vent = False
        for o in model.openings:
            if o.floor == fl and o.kind == "vent":
                if wr.poly.buffer(0.6).intersects(m.R(*o.rect(0.5))):
                    has_vent = True
                    break
        res14.append((has_vent, f"{fl} {wr.name} (bounds={wr.poly.bounds}): direct exterior ventilation"))

print("Check 14 results (WITHOUT ANY HACK):")
for ok, msg in res14:
    print(("  PASS  " if ok else "  FAIL  ") + msg)

all_ok = all(ok for ok, _ in res14)
print("\nAll wet rooms naturally pass exterior ventilation check:", all_ok)

# Run full validate()
res_full = m.validate(model, verbose=False)
print("Total checks passed in full model:", sum(o for o, _ in res_full), "/", len(res_full))
