"""
Batch render all production Cycles views for Transformable Box Furniture.
"""

import subprocess
import sys
import os

VIEWS = [
    ("transformable_box_lineup", "box_hero_3in1_lineup", "hero"),
    ("transformable_box_stool", "box_config1_stool", "isometric"),
    ("transformable_box_storage", "box_config2_storage", "isometric"),
    ("transformable_box_desk", "box_config3_desk", "isometric"),
    ("transformable_box_desk", "box_joinery_macro", "macro"),
]

def main():
    print("[*] Starting production rendering of all 5 views in Blender 5.1 Cycles...")
    for model, out_name, view_type in VIEWS:
        print(f"\n==========================================")
        print(f"[*] Rendering {out_name} ({view_type})...")
        cmd = [
            sys.executable,
            "scripts/blender_runner.py",
            "scripts/render_transformable_box_cycles.py",
            model,
            out_name,
            view_type
        ]
        ret = subprocess.run(cmd)
        if ret.returncode != 0:
            print(f"[!] Error rendering {out_name}, aborting.")
            sys.exit(ret.returncode)
        print(f"[+] Completed {out_name}.")

    print("\n[+] All 5 production views rendered successfully!")

if __name__ == "__main__":
    main()
