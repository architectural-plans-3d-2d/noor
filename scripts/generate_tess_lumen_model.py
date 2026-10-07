"""
TESS-LUMEN 3D Parametric Model Generator
Generates watertight 3D models of the magneto-textile origami element in:
  - Mode A: Flat Acoustic Wall Sconce (tess_lumen_flat)
  - Mode B: Self-Standing Spatial Screen / Desk Lamp (tess_lumen_screen)
  - Mode C: 3D Faceted Origami Pendant Chandelier (tess_lumen_pendant)
"""

import trimesh
import numpy as np
import math
from pathlib import Path

def create_triangular_facet(base=0.3, height=0.3, thickness=0.003):
    """Create a 3mm thick triangular timber facet."""
    # Triangular prism vertices
    v = np.array([
        [-base/2, 0, 0],
        [base/2, 0, 0],
        [0, height, 0],
        [-base/2, 0, thickness],
        [base/2, 0, thickness],
        [0, height, thickness]
    ])
    f = np.array([
        # Bottom & Top
        [0, 2, 1],
        [3, 4, 5],
        # Sides
        [0, 1, 4], [0, 4, 3],
        [1, 2, 5], [1, 5, 4],
        [2, 0, 3], [2, 3, 5]
    ])
    mesh = trimesh.Trimesh(vertices=v, faces=f)
    return mesh

def build_flat_wall_panel():
    """Build the flat acoustic wall panel mode (1.2m x 0.6m)."""
    meshes = []
    # Base canvas sheet
    canvas = trimesh.creation.box(extents=[1.2, 0.6, 0.001])
    canvas.visual.vertex_colors = [235, 230, 220, 255] # Natural unbleached cotton
    meshes.append(canvas)
    
    # 2x4 grid of alternating triangular facets
    rows, cols = 2, 4
    dx, dy = 0.28, 0.28
    for r in range(rows):
        for c in range(cols):
            tri1 = create_triangular_facet(base=0.28, height=0.28, thickness=0.003)
            tri1.apply_translation([(c - 1.5) * 0.29, (r - 0.5) * 0.29 - 0.07, 0.002])
            tri1.visual.vertex_colors = [220, 185, 140, 255] # Birch wood
            meshes.append(tri1)
            
            tri2 = create_triangular_facet(base=0.28, height=0.28, thickness=0.003)
            tri2.apply_transform(trimesh.transformations.rotation_matrix(math.pi, [0, 0, 1]))
            tri2.apply_translation([(c - 1.5) * 0.29, (r - 0.5) * 0.29 + 0.07, 0.002])
            tri2.visual.vertex_colors = [75, 78, 85, 255] # Felt accent
            meshes.append(tri2)
            
    # Rear linear LED wash channels
    led_top = trimesh.creation.box(extents=[1.15, 0.015, 0.006])
    led_top.apply_translation([0, 0.28, -0.005])
    led_top.visual.vertex_colors = [255, 245, 210, 255]
    meshes.append(led_top)
    
    led_bot = trimesh.creation.box(extents=[1.15, 0.015, 0.006])
    led_bot.apply_translation([0, -0.28, -0.005])
    led_bot.visual.vertex_colors = [255, 245, 210, 255]
    meshes.append(led_bot)
    
    return trimesh.Scene(meshes)

def build_standing_screen():
    """Build the self-standing zig-zag spatial acoustic screen."""
    meshes = []
    num_folds = 6
    fold_width = 0.22
    fold_height = 0.55
    angle = math.radians(35) # Zigzag angle
    
    for i in range(num_folds):
        x_base = (i - num_folds / 2) * (fold_width * math.cos(angle))
        z_offset = (fold_width * math.sin(angle)) if (i % 2 == 1) else 0
        rot_y = angle if (i % 2 == 0) else -angle
        
        leaf = trimesh.creation.box(extents=[fold_width, fold_height, 0.004])
        leaf.apply_transform(trimesh.transformations.rotation_matrix(rot_y, [0, 1, 0]))
        leaf.apply_translation([x_base, fold_height / 2, z_offset])
        leaf.visual.vertex_colors = [220, 185, 140, 255] if (i % 2 == 0) else [75, 78, 85, 255]
        meshes.append(leaf)
        
        # Vertical crevice LED line inside each valley fold
        if i % 2 == 1:
            crevice_led = trimesh.creation.cylinder(radius=0.006, height=fold_height * 0.9, sections=16)
            crevice_led.apply_translation([x_base, fold_height / 2, z_offset - 0.01])
            crevice_led.visual.vertex_colors = [255, 245, 210, 255]
            meshes.append(crevice_led)
            
    return trimesh.Scene(meshes)

def build_3d_faceted_pendant():
    """Build the 3D volumetric faceted origami pendant chandelier."""
    meshes = []
    # 12-sided faceted geodetic ring
    ring_facets = 12
    radius = 0.28
    height = 0.38
    
    for i in range(ring_facets):
        a = (2 * math.pi / ring_facets) * i
        mid_a = (2 * math.pi / ring_facets) * (i + 0.5)
        
        # Upper angled triangle
        tri_up = create_triangular_facet(base=0.15, height=height / 2, thickness=0.003)
        rot_z = trimesh.transformations.rotation_matrix(mid_a, [0, 1, 0])
        tilt_up = trimesh.transformations.rotation_matrix(math.radians(24), [1, 0, 0])
        
        tri_up.apply_transform(tilt_up)
        tri_up.apply_transform(rot_z)
        tri_up.apply_translation([radius * math.cos(mid_a), height * 0.25, radius * math.sin(mid_a)])
        tri_up.visual.vertex_colors = [220, 185, 140, 255]
        meshes.append(tri_up)
        
        # Lower inverted triangle
        tri_dn = create_triangular_facet(base=0.15, height=height / 2, thickness=0.003)
        rot_inv = trimesh.transformations.rotation_matrix(math.pi, [0, 0, 1])
        tilt_dn = trimesh.transformations.rotation_matrix(math.radians(-24), [1, 0, 0])
        
        tri_dn.apply_transform(rot_inv)
        tri_dn.apply_transform(tilt_dn)
        tri_dn.apply_transform(rot_z)
        tri_dn.apply_translation([radius * math.cos(mid_a), -height * 0.25, radius * math.sin(mid_a)])
        tri_dn.visual.vertex_colors = [75, 78, 85, 255]
        meshes.append(tri_dn)
        
    # Central warm optical diffuser bulb/core
    core = trimesh.creation.icosphere(radius=0.08, subdivisions=3)
    core.visual.vertex_colors = [255, 240, 200, 255]
    meshes.append(core)
    
    # Minimal brass suspension canopy
    cord = trimesh.creation.cylinder(radius=0.002, height=0.6, sections=12)
    cord.apply_translation([0, height / 2 + 0.3, 0])
    cord.visual.vertex_colors = [50, 50, 50, 255]
    meshes.append(cord)
    
    cap = trimesh.creation.cylinder(radius=0.04, height=0.02, sections=24)
    cap.apply_translation([0, height / 2 + 0.01, 0])
    cap.visual.vertex_colors = [218, 165, 32, 255] # Brass
    meshes.append(cap)
    
    return trimesh.Scene(meshes)

def export_all():
    out_dir = Path("models")
    out_dir.mkdir(exist_ok=True, parents=True)
    
    print("[*] Generating TESS-LUMEN Mode A (Flat Wall Sconce)...")
    flat = build_flat_wall_panel()
    flat.export(str(out_dir / "tess_lumen_flat.obj"))
    flat.export(str(out_dir / "tess_lumen_flat.glb"))
    
    print("[*] Generating TESS-LUMEN Mode B (Spatial Screen)...")
    screen = build_standing_screen()
    screen.export(str(out_dir / "tess_lumen_screen.obj"))
    screen.export(str(out_dir / "tess_lumen_screen.glb"))
    
    print("[*] Generating TESS-LUMEN Mode C (3D Faceted Pendant)...")
    pendant = build_3d_faceted_pendant()
    pendant.export(str(out_dir / "tess_lumen_pendant.obj"))
    pendant.export(str(out_dir / "tess_lumen_pendant.glb"))
    
    print("[+] All TESS-LUMEN 3D models exported successfully to models/")

if __name__ == "__main__":
    export_all()
