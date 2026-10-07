"""
Architectural 3D Mesh & Geometry Pipeline
Utilizes trimesh and numpy for programmatic 3D geometry manipulation,
volume/area calculation, and format conversion.
"""

import trimesh
import numpy as np
import sys
from pathlib import Path

def create_parametric_box_slab(width: float, depth: float, thickness: float, position=(0, 0, 0)):
    """Create a rectangular architectural slab or wall."""
    box = trimesh.creation.box(extents=[width, thickness, depth])
    box.apply_translation([position[0], position[1] + thickness / 2.0, position[2]])
    return box

def analyze_model(mesh_path: str):
    """Load and print architectural metrics of a 3D model."""
    mesh = trimesh.load(mesh_path)
    print("=" * 50)
    print(f"Model: {mesh_path}")
    print(f"Is Watertight / Solid: {mesh.is_watertight}")
    print(f"Bounding Box Extents: {mesh.extents} (meters)")
    print(f"Footprint / Plan Area: ~{mesh.extents[0] * mesh.extents[2]:.2f} sq.m")
    print(f"Total Enclosed Volume: {mesh.volume:.2f} cu.m" if mesh.is_watertight else "Volume: Non-manifold")
    print(f"Vertex Count: {len(mesh.vertices)}, Face Count: {len(mesh.faces)}")
    print("=" * 50)
    return mesh

if __name__ == "__main__":
    if len(sys.argv) > 1:
        analyze_model(sys.argv[1])
    else:
        # Create a sample architectural pavilion test mesh and export
        print("[*] Generating sample architectural massing model...")
        ground = create_parametric_box_slab(16.0, 12.0, 0.4, (0, 0, 0))
        upper = create_parametric_box_slab(12.0, 8.0, 3.2, (2, 3.6, 0))
        roof = create_parametric_box_slab(14.0, 10.0, 0.3, (2, 6.8, 0))
        
        scene = trimesh.Scene([ground, upper, roof])
        out_file = Path("sample_massing.obj")
        scene.export(str(out_file))
        print(f"[+] Sample architectural model exported to: {out_file.resolve()}")
