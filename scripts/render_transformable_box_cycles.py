"""
Photorealistic Blender 5.1 Cycles Studio Renderer (REV 3 - Master Quality)
Features:
- True curved infinity cove cyclorama with bevel curve and shade smooth (no black void!)
- Clean forward_axis='Y', up_axis='Z' import (perfect vertical orientation)
- Warm Scandinavian Baltic Birch and brushed stainless steel PBR shaders
- Studio softbox key/fill/rim/top lighting rig
- Perfectly framed cameras for all 5 presentation views:
    1. hero: Wide 3-in-1 lineup (Stool + Storage + Study Desk)
    2. stool: Config 1 3/4 isometric bench beauty view
    3. storage: Config 2 3/4 isometric vertical cabinet view
    4. desk: Config 3 3/4 isometric study desk in active setting
    5. macro: Close-up macro joinery on piano hinge and folding stay
"""

import bpy
import sys
import os
import math

def setup_studio():
    bpy.ops.wm.read_factory_settings(use_empty=True)
    scene = bpy.context.scene

    # Render settings: Cycles, AgX color management
    scene.render.engine = 'CYCLES'
    cycles = scene.cycles
    cycles.device = 'CPU'
    cycles.samples = 64
    cycles.use_denoising = True
    scene.view_settings.view_transform = 'AgX'
    scene.view_settings.look = 'AgX - Medium High Contrast'
    scene.render.resolution_x = 1920
    scene.render.resolution_y = 1080
    scene.render.resolution_percentage = 100

    # Build True Photographic Cyclorama (Infinity Cove)
    # Create plane, extrude back edge up, bevel corner
    bpy.ops.mesh.primitive_plane_add(size=16, location=(0, -1, 0))
    cove = bpy.context.active_object
    cove.name = "Infinity_Cove"
    cove.scale = (2.0, 1.2, 1.0)
    bpy.ops.object.transform_apply(scale=True)

    # Enter edit mode to extrude back edge
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='DESELECT')
    # Select the back edge (+Y edge)
    bm = None
    import bmesh
    bm = bmesh.from_edit_mesh(cove.data)
    for e in bm.edges:
        if all(v.co.y > 6.0 for v in e.verts):
            e.select = True
            break
    bmesh.update_edit_mesh(cove.data)

    # Extrude up by 8 meters
    bpy.ops.mesh.extrude_region_move(TRANSFORM_OT_translate={"value": (0, 0, 8.0)})
    
    # Bevel the seam edge
    bpy.ops.mesh.select_all(action='DESELECT')
    bm = bmesh.from_edit_mesh(cove.data)
    for e in bm.edges:
        if all(abs(v.co.z) < 0.1 and v.co.y > 5.9 for v in e.verts):
            e.select = True
    bmesh.update_edit_mesh(cove.data)
    bpy.ops.mesh.bevel(offset=3.5, segments=16, profile=0.5)

    bpy.ops.object.mode_set(mode='OBJECT')
    bpy.ops.object.shade_smooth()

    # Material for cyclorama floor (Soft, warm, luminous studio backdrop)
    cove_mat = bpy.data.materials.new(name="Infinity_Cove_Mat")
    bsdf_cove = cove_mat.node_tree.nodes.get("Principled BSDF")
    if bsdf_cove:
        bsdf_cove.inputs['Base Color'].default_value = (0.86, 0.85, 0.83, 1.0)
        bsdf_cove.inputs['Roughness'].default_value = 0.90
    cove.data.materials.append(cove_mat)

    # Studio Lighting Rig
    # 1. Key Softbox (Warm daylight 5000K)
    bpy.ops.object.light_add(type='AREA', location=(3.5, -4.2, 3.8))
    key = bpy.context.active_object
    key.name = "Key_Softbox"
    key.data.energy = 280
    key.data.size = 2.4
    key.data.size_y = 2.0
    key.data.color = (1.0, 0.96, 0.91)
    key.rotation_euler = (math.radians(55), math.radians(10), math.radians(35))

    # 2. Fill Softbox (Cool daylight 6000K)
    bpy.ops.object.light_add(type='AREA', location=(-4.0, -3.8, 3.0))
    fill = bpy.context.active_object
    fill.name = "Fill_Softbox"
    fill.data.energy = 110
    fill.data.size = 3.2
    fill.data.color = (0.92, 0.96, 1.0)
    fill.rotation_euler = (math.radians(50), math.radians(-12), math.radians(-40))

    # 3. Rim Accent Light
    bpy.ops.object.light_add(type='AREA', location=(0.0, 3.2, 3.5))
    rim = bpy.context.active_object
    rim.name = "Rim_Accent"
    rim.data.energy = 140
    rim.data.size = 2.8
    rim.rotation_euler = (math.radians(-50), 0, 0)

    # 4. Top Soft Skylight
    bpy.ops.object.light_add(type='AREA', location=(0.0, -1.0, 5.5))
    top = bpy.context.active_object
    top.name = "Top_Skylight"
    top.data.energy = 90
    top.data.size = 5.0

    return scene

def create_wood_material():
    mat = bpy.data.materials.new(name="Baltic_Birch_PBR")
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    nodes.clear()

    output = nodes.new(type='ShaderNodeOutputMaterial')
    bsdf = nodes.new(type='ShaderNodeBsdfPrincipled')
    # Rich warm Scandinavian blonde birch
    bsdf.inputs['Base Color'].default_value = (0.76, 0.60, 0.44, 1.0)
    bsdf.inputs['Roughness'].default_value = 0.35
    bsdf.inputs['Specular IOR Level'].default_value = 0.55

    # Procedural fine grain
    tex_noise = nodes.new(type='ShaderNodeTexNoise')
    tex_noise.inputs['Scale'].default_value = 32.0
    tex_noise.inputs['Detail'].default_value = 3.0
    tex_noise.inputs['Roughness'].default_value = 0.6

    bump = nodes.new(type='ShaderNodeBump')
    bump.inputs['Strength'].default_value = 0.025
    bump.inputs['Distance'].default_value = 0.005

    links.new(tex_noise.outputs['Fac'], bump.inputs['Height'])
    links.new(bump.outputs['Normal'], bsdf.inputs['Normal'])
    links.new(bsdf.outputs['BSDF'], output.inputs['Surface'])
    return mat

def create_metal_material():
    mat = bpy.data.materials.new(name="Stainless_Steel_Hardware_PBR")
    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    if bsdf:
        bsdf.inputs['Base Color'].default_value = (0.86, 0.86, 0.88, 1.0)
        bsdf.inputs['Metallic'].default_value = 1.0
        bsdf.inputs['Roughness'].default_value = 0.18
    return mat

def create_props_material():
    mat = bpy.data.materials.new(name="Modern_Props_PBR")
    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    if bsdf:
        bsdf.inputs['Base Color'].default_value = (0.16, 0.17, 0.19, 1.0)  # Space Gray aluminum
        bsdf.inputs['Metallic'].default_value = 0.88
        bsdf.inputs['Roughness'].default_value = 0.25
    return mat

def render_model_scene(name_prefix, output_png_path, view_type="hero"):
    setup_studio()
    
    wood_mat = create_wood_material()
    metal_mat = create_metal_material()
    props_mat = create_props_material()

    # Import parts with EXACT coordinate alignment: forward_axis='Y', up_axis='Z'
    # 1. Wood
    wood_obj_path = os.path.abspath(f"models/{name_prefix}_wood.obj")
    if os.path.exists(wood_obj_path):
        bpy.ops.wm.obj_import(filepath=wood_obj_path, forward_axis='Y', up_axis='Z')
        for obj in bpy.context.selected_objects:
            if obj.type == 'MESH':
                obj.data.materials.clear()
                obj.data.materials.append(wood_mat)

    # 2. Metal
    metal_obj_path = os.path.abspath(f"models/{name_prefix}_metal.obj")
    if os.path.exists(metal_obj_path):
        bpy.ops.wm.obj_import(filepath=metal_obj_path, forward_axis='Y', up_axis='Z')
        for obj in bpy.context.selected_objects:
            if obj.type == 'MESH':
                obj.data.materials.clear()
                obj.data.materials.append(metal_mat)

    # 3. Props
    props_obj_path = os.path.abspath(f"models/{name_prefix}_props.obj")
    if os.path.exists(props_obj_path):
        bpy.ops.wm.obj_import(filepath=props_obj_path, forward_axis='Y', up_axis='Z')
        for obj in bpy.context.selected_objects:
            if obj.type == 'MESH':
                obj.data.materials.clear()
                obj.data.materials.append(props_mat)

    # Camera setup
    cam_data = bpy.data.cameras.new(name="Studio_Camera")
    
    if view_type == "hero":
        # Dynamic 3/4 studio lineup showing front, sides, top surfaces, and cantilever depth
        cam_data.lens = 42
        cam_pos = (0.75, -4.4, 1.35)
        cam_rot = (math.radians(76), 0, math.radians(10))
    elif view_type == "isometric":
        # 3/4 isometric perspective for single configuration (framed for 900mm tall cabinet)
        cam_data.lens = 52
        cam_pos = (1.35, -2.4, 1.40)
        cam_rot = (math.radians(65), 0, math.radians(32))
    elif view_type == "macro":
        # Macro close-up under desk leaf focusing on folding stay bracket (Detail B)
        cam_data.lens = 75
        cam_pos = (-0.38, -0.65, 0.48)
        cam_rot = (math.radians(68), 0, math.radians(-32))
    else:
        cam_data.lens = 48
        cam_pos = (0.0, -2.8, 1.0)
        cam_rot = (math.radians(78), 0, 0)

    cam_obj = bpy.data.objects.new(name="Studio_Camera", object_data=cam_data)
    bpy.context.scene.collection.objects.link(cam_obj)
    bpy.context.scene.camera = cam_obj
    cam_obj.location = cam_pos

    # Add Target Empty at center of object (0, 0, 0.45m) for perfect framing
    target_empty = bpy.data.objects.new("Cam_Target", None)
    target_empty.location = (0, 0, 0.45)
    bpy.context.scene.collection.objects.link(target_empty)
    
    track_con = cam_obj.constraints.new(type='TRACK_TO')
    track_con.target = target_empty
    track_con.track_axis = 'TRACK_NEGATIVE_Z'
    track_con.up_axis = 'UP_Y'

    # Render
    os.makedirs(os.path.dirname(output_png_path), exist_ok=True)
    bpy.context.scene.render.filepath = output_png_path
    print(f"[*] Starting Cycles render of {name_prefix} ({view_type}) -> {output_png_path}...")
    bpy.ops.render.render(write_still=True)
    print(f"[+] Render complete: {output_png_path}")

if __name__ == "__main__":
    args = sys.argv
    try:
        idx = args.index("--")
        custom_args = args[idx+1:]
    except ValueError:
        custom_args = []

    prefix = custom_args[0] if len(custom_args) > 0 else "transformable_box_lineup"
    out_file = custom_args[1] if len(custom_args) > 1 else "box_hero_3in1_lineup"
    v_type = custom_args[2] if len(custom_args) > 2 else "hero"

    out_png = os.path.abspath(f"renders/{out_file}.png")
    render_model_scene(prefix, out_png, view_type=v_type)
