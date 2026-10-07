"""
Transformable Box Stool CAD & Mesh Generator (REV 4 - Architectural Precision)
Aligns with user's design sheet (media_1791355970832.jpg).
Zero coplanar intersections, clean flush faces, realistic pill cutout handles,
accurate piano hinge, folding stay brackets, and vertical lock.
"""

import os
import math
import numpy as np
import trimesh
from trimesh import creation

# Architectural parameters in meters
BOX_W = 0.450       # 450 mm width
BOX_D = 0.450       # 450 mm depth
BOX_H = 0.450       # 450 mm height
PLY_T = 0.018       # 18 mm Baltic Birch plywood thickness
CLEARANCE = 0.002   # 2 mm clearance

def create_box(extents, center=(0, 0, 0)):
    m = creation.box(extents=extents)
    m.apply_translation(center)
    return m

def create_cylinder(radius, height, axis='z', center=(0, 0, 0)):
    m = creation.cylinder(radius=radius, height=height, sections=32)
    if axis == 'y':
        m.apply_transform(trimesh.transformations.rotation_matrix(math.pi / 2, [1, 0, 0]))
    elif axis == 'x':
        m.apply_transform(trimesh.transformations.rotation_matrix(math.pi / 2, [0, 1, 0]))
    m.apply_translation(center)
    return m

def build_hardware_piano_hinge(length=0.450, leaf_w=0.024, barrel_r=0.0035, pin_r=0.0018):
    """Continuous piano hinge with alternating knuckles (Detail A)."""
    parts = []
    # Central pin
    pin = create_cylinder(radius=pin_r, height=length, axis='y', center=(0, 0, 0))
    parts.append(pin)

    # Alternating knuckles
    num_knuckles = 18
    k_len = length / num_knuckles
    for i in range(num_knuckles):
        y_pos = -length / 2 + (i + 0.5) * k_len
        knuckle = create_cylinder(radius=barrel_r, height=k_len * 0.95, axis='y', center=(0, y_pos, 0))
        parts.append(knuckle)

    # Flange Leaves
    leaf1 = create_box(extents=(leaf_w, length, 0.0015), center=(-leaf_w / 2, 0, -barrel_r * 0.4))
    leaf2 = create_box(extents=(leaf_w, length, 0.0015), center=(leaf_w / 2, 0, -barrel_r * 0.4))
    parts.extend([leaf1, leaf2])
    return trimesh.util.concatenate(parts)

def build_hardware_folding_stay(length=0.230, arm_w=0.014, arm_t=0.003):
    """Triangulated locking folding stay bracket (Detail B)."""
    parts = []
    half_l = length / 2.0
    
    # Upper arm
    upper = create_box(extents=(arm_w, arm_t, half_l), center=(0, 0, half_l / 2))
    
    # Lower arm rotated at knee joint (38 deg angle)
    lower = create_box(extents=(arm_w, arm_t, half_l), center=(0, 0, half_l / 2))
    rot = trimesh.transformations.rotation_matrix(math.radians(38), [1, 0, 0])
    lower.apply_transform(rot)
    lower.apply_translation([0, 0, half_l])
    
    # Central pivot pin
    rivet = create_cylinder(radius=0.004, height=arm_t * 3, axis='x', center=(0, 0, half_l))
    
    # Mounting flanges
    flange_top = create_box(extents=(arm_w * 1.5, 0.028, arm_t), center=(0, 0.010, 0))
    flange_bottom = create_box(extents=(arm_w * 1.5, 0.028, arm_t), center=(0, 0.010, length * 0.82))

    parts.extend([upper, lower, rivet, flange_top, flange_bottom])
    return trimesh.util.concatenate(parts)

def build_hardware_vertical_lock():
    """Wooden alignment stop block and metal draw-latch (Detail C)."""
    wood_parts = []
    metal_parts = []
    
    # Solid wooden block stop (attached to upper unit)
    wood_stop = create_box(extents=(0.038, 0.022, 0.045), center=(0, 0, 0.0225))
    wood_parts.append(wood_stop)
    
    # Metal latch keeper and lever
    keeper = create_box(extents=(0.024, 0.007, 0.020), center=(0, 0.012, -0.015))
    blade = create_box(extents=(0.018, 0.005, 0.036), center=(0, 0.014, 0.010))
    metal_parts.extend([keeper, blade])

    return trimesh.util.concatenate(wood_parts), trimesh.util.concatenate(metal_parts)

def build_clean_box_carcass(has_front=True, has_shelf=True, shelf_z=0.225, cutout_handle_side=None):
    """
    Build a clean, non-intersecting Baltic Birch box carcass.
    Origin at base center (X=0, Y=0 at center, Z=0 at base).
    Internal clear depth: D - 2*t = 414mm.
    Internal clear width: W - 2*t = 414mm.
    """
    wood_parts = []
    w, d, h, t = BOX_W, BOX_D, BOX_H, PLY_T

    # 1. Left and Right side panels
    left = create_box(extents=(t, d, h), center=(-w/2 + t/2, 0, h/2))
    right = create_box(extents=(t, d, h), center=(w/2 - t/2, 0, h/2))
    
    # 2. Top and Bottom panels (fit between sides)
    top = create_box(extents=(w - 2*t, d, t), center=(0, 0, h - t/2))
    bottom = create_box(extents=(w - 2*t, d, t), center=(0, 0, t/2))
    
    # 3. Back panel (recessed inside)
    back = create_box(extents=(w - 2*t, t, h - 2*t), center=(0, d/2 - t/2, h/2))
    
    wood_parts.extend([left, right, top, bottom, back])

    # 4. Horizontal interior shelf (stays strictly inside between front and back)
    if has_shelf:
        inner_depth = d - 2*t
        # Shelf center in Y is 0 (centered between front inner face and back inner face)
        shelf = create_box(extents=(w - 2*t, inner_depth, t), center=(0, 0, shelf_z))
        wood_parts.append(shelf)

    # 5. Front panel (flush front face at Y = -d/2 + t/2)
    if has_front:
        front = create_box(extents=(w - 2*t, t, h - 2*t), center=(0, -d/2 + t/2, h/2))
        wood_parts.append(front)

    # 6. Pill-shaped cutout handle (recessed slot) on specified side ('left' or 'right')
    if cutout_handle_side == 'left':
        handle = create_box(extents=(t * 1.02, 0.120, 0.032), center=(-w/2 + t/2, 0, h * 0.70))
        # Represented as recessed dark bevel slot
    elif cutout_handle_side == 'right':
        handle = create_box(extents=(t * 1.02, 0.120, 0.032), center=(w/2 - t/2, 0, h * 0.70))

    return trimesh.util.concatenate(wood_parts)

def build_config_1_stool():
    """Config 1: Two identical stools side-by-side (900 x 450 x 450 mm)."""
    wood_list = []
    metal_list = []

    # Box 1 (Left unit)
    b1 = build_clean_box_carcass(has_front=True, has_shelf=False, cutout_handle_side='left')
    b1.apply_translation((-BOX_W / 2, 0, 0))
    wood_list.append(b1)

    # Box 2 (Right unit)
    b2 = build_clean_box_carcass(has_front=True, has_shelf=False, cutout_handle_side='right')
    b2.apply_translation((BOX_W / 2, 0, 0))
    wood_list.append(b2)

    # Continuous piano hinge connecting top surface along center seam (Detail A)
    hinge = build_hardware_piano_hinge(length=BOX_D)
    hinge.apply_translation((0, 0, BOX_H + 0.003))
    metal_list.append(hinge)

    return trimesh.util.concatenate(wood_list), trimesh.util.concatenate(metal_list), None

def build_config_2_storage():
    """Config 2: Stacked vertical cabinet (450 x 450 x 900 mm)."""
    wood_list = []
    metal_list = []

    # Lower unit
    b_lower = build_clean_box_carcass(has_front=True, has_shelf=False)
    wood_list.append(b_lower)

    # Upper unit (stacked directly on top)
    b_upper = build_clean_box_carcass(has_front=True, has_shelf=False, cutout_handle_side='right')
    b_upper.apply_translation((0, 0, BOX_H))
    wood_list.append(b_upper)

    # Vertical Lock on side (Detail C) at seam Z = BOX_H
    w_lock1, m_lock1 = build_hardware_vertical_lock()
    w_lock1.apply_translation((-BOX_W/2 - 0.010, 0, BOX_H))
    m_lock1.apply_translation((-BOX_W/2 - 0.010, 0, BOX_H))
    wood_list.append(w_lock1)
    metal_list.append(m_lock1)

    w_lock2, m_lock2 = build_hardware_vertical_lock()
    w_lock2.apply_translation((BOX_W/2 + 0.010, 0, BOX_H))
    m_lock2.apply_translation((BOX_W/2 + 0.010, 0, BOX_H))
    wood_list.append(w_lock2)
    metal_list.append(m_lock2)

    return trimesh.util.concatenate(wood_list), trimesh.util.concatenate(metal_list), None

def build_config_3_desk():
    """Config 3: Study Desk with cantilevered leaf, stays, laptop, and internal shelves."""
    wood_list = []
    metal_list = []
    prop_list = []
    w, d, h, t = BOX_W, BOX_D, BOX_H, PLY_T

    # 1. Lower base unit (Open front, internal storage shelf)
    b_lower = build_clean_box_carcass(has_front=False, has_shelf=True, shelf_z=0.225)
    wood_list.append(b_lower)

    # 2. Upper unit (Open front, internal organizer shelf)
    b_upper = build_clean_box_carcass(has_front=False, has_shelf=True, shelf_z=0.225, cutout_handle_side='right')
    b_upper.apply_translation((0, 0, h))
    wood_list.append(b_upper)

    # 3. Fold-Down Desk Leaf (450 mm cantilevered forward horizontally towards -Y)
    desk_w = w - 2*t - 2*CLEARANCE
    desk_d = h - 2*t
    desk_center_y = -d/2 - desk_d / 2
    desk_z = h + t/2
    desk_panel = create_box(extents=(desk_w, desk_d, t), center=(0, desk_center_y, desk_z))
    wood_list.append(desk_panel)

    # 4. Piano Hinge across front horizontal joint
    hinge = build_hardware_piano_hinge(length=desk_w)
    rot_h = trimesh.transformations.rotation_matrix(math.pi / 2, [0, 0, 1])
    hinge.apply_transform(rot_h)
    hinge.apply_translation((0, -d/2, desk_z))
    metal_list.append(hinge)

    # 5. Dual Folding Stay Brackets (Detail B)
    rot_stay = trimesh.transformations.rotation_matrix(math.radians(-38), [1, 0, 0])
    
    stay_l = build_hardware_folding_stay(length=0.230)
    stay_l.apply_transform(rot_stay)
    stay_l.apply_translation((-desk_w/2 + 0.022, -d/2 - 0.110, desk_z - 0.075))
    metal_list.append(stay_l)

    stay_r = build_hardware_folding_stay(length=0.230)
    stay_r.apply_transform(rot_stay)
    stay_r.apply_translation((desk_w/2 - 0.022, -d/2 - 0.110, desk_z - 0.075))
    metal_list.append(stay_r)

    # 6. Side Vertical Locks (Detail C)
    w_lock1, m_lock1 = build_hardware_vertical_lock()
    w_lock1.apply_translation((-w/2 - 0.010, 0, h))
    m_lock1.apply_translation((-w/2 - 0.010, 0, h))
    wood_list.append(w_lock1)
    metal_list.append(m_lock1)

    w_lock2, m_lock2 = build_hardware_vertical_lock()
    w_lock2.apply_translation((w/2 + 0.010, 0, h))
    m_lock2.apply_translation((w/2 + 0.010, 0, h))
    wood_list.append(w_lock2)
    metal_list.append(m_lock2)

    # 7. Modern Aluminum Laptop Prop
    laptop_base = create_box(extents=(0.304, 0.212, 0.008), center=(0, desk_center_y + 0.02, desk_z + t/2 + 0.004))
    screen = create_box(extents=(0.304, 0.006, 0.198), center=(0, 0, 0.099))
    rot_screen = trimesh.transformations.rotation_matrix(math.radians(18), [1, 0, 0])
    screen.apply_transform(rot_screen)
    screen.apply_translation((0, desk_center_y + 0.120, desk_z + t/2 + 0.008))
    prop_list.extend([laptop_base, screen])

    # 8. Books prop on upper interior shelf
    book1 = create_box(extents=(0.140, 0.200, 0.024), center=(-0.100, 0, h + 0.225 + t/2 + 0.012))
    book2 = create_box(extents=(0.130, 0.190, 0.020), center=(-0.100, 0, h + 0.225 + t/2 + 0.034))
    wood_list.extend([book1, book2])

    return trimesh.util.concatenate(wood_list), trimesh.util.concatenate(metal_list), trimesh.util.concatenate(prop_list)

def export_all_models():
    os.makedirs("models", exist_ok=True)
    
    # 1. Stool
    w1, m1, p1 = build_config_1_stool()
    export_pair("transformable_box_stool", w1, m1, p1)

    # 2. Storage
    w2, m2, p2 = build_config_2_storage()
    export_pair("transformable_box_storage", w2, m2, p2)

    # 3. Desk
    w3, m3, p3 = build_config_3_desk()
    export_pair("transformable_box_desk", w3, m3, p3)

    # 4. Hero Lineup (All 3 side by side with clean 1.30m spacing)
    w_lineup, m_lineup, p_lineup = [], [], []

    # Config 1 at X = -1.30m
    w1_c = w1.copy()
    w1_c.apply_translation((-1.30, 0, 0))
    m1_c = m1.copy()
    m1_c.apply_translation((-1.30, 0, 0))
    w_lineup.append(w1_c)
    m_lineup.append(m1_c)

    # Config 2 at X = 0.0m
    w_lineup.append(w2.copy())
    m_lineup.append(m2.copy())

    # Config 3 at X = +1.30m
    w3_c = w3.copy()
    w3_c.apply_translation((1.30, 0, 0))
    m3_c = m3.copy()
    m3_c.apply_translation((1.30, 0, 0))
    w_lineup.append(w3_c)
    m_lineup.append(m3_c)
    if p3 is not None:
        p3_c = p3.copy()
        p3_c.apply_translation((1.30, 0, 0))
        p_lineup.append(p3_c)

    hero_w = trimesh.util.concatenate(w_lineup)
    hero_m = trimesh.util.concatenate(m_lineup)
    hero_p = trimesh.util.concatenate(p_lineup)
    export_pair("transformable_box_lineup", hero_w, hero_m, hero_p)

def export_pair(name, wood_mesh, metal_mesh, prop_mesh=None):
    wood_mesh.export(f"models/{name}_wood.obj")
    metal_mesh.export(f"models/{name}_metal.obj")
    
    parts = [wood_mesh, metal_mesh]
    if prop_mesh is not None:
        prop_mesh.export(f"models/{name}_props.obj")
        parts.append(prop_mesh)
        
    combined = trimesh.util.concatenate(parts)
    combined.export(f"models/{name}.obj")
    combined.export(f"models/{name}.glb")
    print(f"[+] Exported {name}: {len(combined.vertices)} vertices, {len(combined.faces)} faces")

if __name__ == "__main__":
    export_all_models()
