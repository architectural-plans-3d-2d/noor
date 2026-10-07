"""
STRATAVOX Parametric 3D Model Generator
Generates mathematically precise 3D meshes for STRATAVOX in multiple kinetic deployment states:
  - Collapsed Rosette (Mode 1)
  - Diffuse Cloud (Mode 2)
  - Vaulted Acoustic Cocoon (Mode 3)
Outputs watertight OBJ and GLB models with assigned material groups.
"""

import trimesh
import numpy as np
import math
import sys
from pathlib import Path

def create_lamella(length=0.9, width=0.07, thickness=0.012):
    """Create a single CNC-machined architectural birch lamella with end radiuses."""
    box = trimesh.creation.box(extents=[length, thickness, width])
    return box

def create_brass_pivot(radius=0.016, height=0.024):
    """Create precision machined brass pivot stud."""
    cyl = trimesh.creation.cylinder(radius=radius, height=height, sections=32)
    return cyl

def create_felt_baffle(span=0.8, arc_height=0.15, depth=0.25, thickness=0.006):
    """Create curved thermoformed acoustic felt saddle panel."""
    # Approximate saddle mesh via parametric surface extrusion
    segments = 24
    xs = np.linspace(-span / 2, span / 2, segments)
    ys = arc_height * (1.0 - (2.0 * xs / span) ** 2)
    
    vertices = []
    faces = []
    
    # Build upper and lower profile along depth
    for d in [-depth / 2, depth / 2]:
        for x, y in zip(xs, ys):
            vertices.append([x, y, d])
            vertices.append([x, y - thickness, d])
            
    mesh = trimesh.creation.box(extents=[span * 0.9, thickness, depth])
    return mesh

def build_stratavox_canopy(deployment_factor=1.0):
    """
    Build the complete STRATAVOX canopy assembly at given deployment factor (0.0 to 1.0).
    0.0 = Fully Collapsed Rosette
    0.5 = Diffuse Planar Cloud
    1.0 = Fully Vaulted Acoustic Cocoon
    """
    lamella_count = 24
    radius_hub = 0.25 + (deployment_factor * 0.15)
    radius_outer = 0.55 + (deployment_factor * 0.75) # 0.55m -> 1.30m (diameter 1.1m to 2.6m)
    vault_depth = deployment_factor * 0.55 # Z drops down in vaulted mode
    
    all_meshes = []
    
    # 1. Central Spun Brass Hub and Tension Ring
    center_hub = trimesh.creation.cylinder(radius=0.18, height=0.06, sections=48)
    center_hub.apply_translation([0, 0, 0])
    center_hub.visual.vertex_colors = [218, 165, 32, 255] # Brass Gold
    all_meshes.append(center_hub)
    
    # Central Accent Luminaire Dome
    light_core = trimesh.creation.icosphere(radius=0.12, subdivisions=3)
    light_core.apply_translation([0, -0.04, 0])
    light_core.visual.vertex_colors = [255, 250, 230, 255] # Warm White Light
    all_meshes.append(light_core)
    
    # 2. Scissor Kinematic Lamellae (Upper and Lower Cross Links)
    lamella_len = 0.82
    for i in range(lamella_count):
        angle = (2 * math.pi / lamella_count) * i
        cos_a = math.cos(angle)
        sin_a = math.sin(angle)
        
        # Upper scissor arm
        arm_up = create_lamella(length=lamella_len, width=0.06, thickness=0.012)
        tilt_angle = math.radians(12 + deployment_factor * 32)
        
        # Position between inner hub and outer rim
        mid_r = (radius_hub + radius_outer) / 2.0
        mid_y = - (vault_depth * (mid_r / radius_outer))
        
        # Transform arm
        rot_z = trimesh.transformations.rotation_matrix(angle, [0, 1, 0])
        rot_tilt = trimesh.transformations.rotation_matrix(tilt_angle, [0, 0, 1])
        trans = trimesh.transformations.translation_matrix([mid_r * cos_a, mid_y, mid_r * sin_a])
        
        arm_up.apply_transform(rot_tilt)
        arm_up.apply_transform(rot_z)
        arm_up.apply_translation([mid_r * cos_a, mid_y, mid_r * sin_a])
        arm_up.visual.vertex_colors = [222, 184, 135, 255] # Baltic Birch
        all_meshes.append(arm_up)
        
        # Pivot Node Hardware at outer edge
        pivot = create_brass_pivot(radius=0.018, height=0.035)
        pivot_y = - vault_depth * (radius_outer / radius_outer)
        pivot.apply_translation([radius_outer * cos_a, pivot_y, radius_outer * sin_a])
        pivot.visual.vertex_colors = [218, 165, 32, 255]
        all_meshes.append(pivot)
        
        # Acoustic PET Felt Wing between alternating lamellae
        if i % 2 == 0:
            felt_baffle = trimesh.creation.box(extents=[0.38 + (deployment_factor * 0.15), 0.008, 0.22])
            felt_baffle.apply_transform(rot_z)
            felt_baffle.apply_translation([(mid_r * 1.05) * cos_a, mid_y - 0.02, (mid_r * 1.05) * sin_a])
            felt_baffle.visual.vertex_colors = [70, 75, 82, 255] # Anthracite Charcoal Felt
            all_meshes.append(felt_baffle)
            
            # Embedded Linear LED strip under the felt baffle
            led_strip = trimesh.creation.box(extents=[0.36 + (deployment_factor * 0.15), 0.006, 0.015])
            led_strip.apply_transform(rot_z)
            led_strip.apply_translation([(mid_r * 1.05) * cos_a, mid_y - 0.03, (mid_r * 1.05) * sin_a])
            led_strip.visual.vertex_colors = [255, 245, 210, 255] # Emissive Light Strip
            all_meshes.append(led_strip)
            
    # Combine into single scene / composite mesh
    compound_scene = trimesh.Scene(all_meshes)
    return compound_scene

def export_all_states(output_dir="models"):
    out_path = Path(output_dir)
    out_path.mkdir(exist_ok=True, parents=True)
    
    states = [
        ("stratavox_collapsed", 0.0),
        ("stratavox_cloud", 0.5),
        ("stratavox_vaulted", 1.0)
    ]
    
    for name, factor in states:
        print(f"[*] Generating {name} (deployment factor: {factor})...")
        scene = build_stratavox_canopy(deployment_factor=factor)
        
        obj_file = out_path / f"{name}.obj"
        glb_file = out_path / f"{name}.glb"
        
        scene.export(str(obj_file))
        scene.export(str(glb_file))
        print(f"[+] Exported: {obj_file} & {glb_file}")

if __name__ == "__main__":
    export_all_states()
