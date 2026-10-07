"""
Test script to implement the exterior-ventilated courtyard/breezeway in model.py.
We will test:
1. Powder Room has an authentic vent opening to outside air.
2. 1F Bed-4 Bath has an authentic vent opening to outside air.
3. Check 14 passes WITHOUT the hardcoded hack.
4. Check 18 passes (zero outdated interior shaft cuts).
5. All 121 checks pass.
"""
import sys
sys.path.insert(0, '.')
import scripts.daata_hamlet.model as m

# Let's see the current openings on GF
m_obj = m.build()
print("GF openings:")
for o in m_obj.openings:
    if o.floor == 'GF':
        print(f"  {o.name:15s} {o.kind:8s} orient={o.orient} line={o.line:7.3f} ({o.a:6.2f}, {o.b:6.2f}) sill={o.sill} head={o.head}")
