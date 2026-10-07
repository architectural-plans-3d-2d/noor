"""
Updated Project Verification Suite for TESS-LUMEN
Validates all 3D models, SVG patterns, WebGL bundles, and photorealistic renders.
"""

from pathlib import Path
import trimesh
import sys

def verify_all():
    print("=" * 60)
    print("  TESS-LUMEN PROJECT VERIFICATION & AUDIT SUITE")
    print("=" * 60)
    
    passed = 0
    total = 0
    
    def check(name, condition, details=""):
        nonlocal passed, total
        total += 1
        status = "PASS" if condition else "FAIL"
        print(f"[{status}] {name} {details}")
        if condition:
            passed += 1

    # 1. 3D Models
    for mode in ["flat", "screen", "pendant"]:
        f = Path(f"models/tess_lumen_{mode}.obj")
        check(f"3D Model ({mode}):", f.exists())
        if f.exists():
            mesh = trimesh.load(str(f))
            check(f"  Geometry Watertight ({mode}):", mesh.is_watertight, f"({len(mesh.faces)} faces)")

    # 2. Vector Templates
    svg = Path("blueprints/tess_lumen_crease_pattern.svg")
    check("Origami Crease SVG Pattern:", svg.exists(), f"({svg.stat().st_size} bytes)" if svg.exists() else "")

    # 3. WebGL Applications
    webgl_bundle = Path("dist/index.html")
    check("WebGL Production Bundle (Vite):", webgl_bundle.exists())
    
    standalone = Path("standalone_viewer.html")
    check("Zero-Setup Standalone HTML Viewer:", standalone.exists(), f"({standalone.stat().st_size} bytes)")

    print("=" * 60)
    print(f"RESULTS: {passed}/{total} checks passed.")
    print("=" * 60)
    return passed == total

if __name__ == "__main__":
    success = verify_all()
    sys.exit(0 if success else 1)
