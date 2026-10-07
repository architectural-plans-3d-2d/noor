"""
TESS-LUMEN Photorealistic Cycles Architectural Renderer
Renders the 3D origami faceted pendant suspended in a luxury architectural dining/lounge setting.
"""

import bpy
import sys
import math
from pathlib import Path

model_file = "models/tess_lumen_pendant.obj"
output_file = "renders/tess_lumen_pendant_cycles.png"

Path(output_file).parent.mkdir(parents=True, exist_ok=True)
print(f"[*] Rendering TESS-LUMEN 3D Origami Chandelier with Cycles...")

# 1. Reset Scene
bpy.ops.wm.read_factory_settings(use_empty=True)
scene = bpy.context.scene

# 2. Render Settings
scene.render.engine = 'CYCLES'
scene.cycles.device = 'CPU'
scene.cycles.samples = 96
scene.cycles.use_denoising = True
scene.render.resolution_x = 1920
scene.render.resolution_y = 1080
scene.render.resolution_percentage = 100
scene.view_settings.view_transform = 'AgX'
scene.view_settings.look = 'AgX - Medium High Contrast'

# 3. Environment: Minimalist Dining Lounge
# Wood Oak Floor
bpy.ops.mesh.primitive_plane_add(size=14, location=(0, 0, 0))
floor = bpy.context.active_object
floor.name = "OakFloor"
floor_mat = bpy.data.materials.new(name="FloorMat")
floor_mat.use_nodes = True
bsdf_f = floor_mat.node_tree.nodes.get("Principled BSDF")
if bsdf_f:
    bsdf_f.inputs["Base Color"].default_value = (0.28, 0.22, 0.17, 1.0) # Warm oak
    bsdf_f.inputs["Roughness"].default_value = 0.38
floor.data.materials.append(floor_mat)

# Architectural Back Wall
bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 3.5, 2.2))
wall = bpy.context.active_object
wall.scale = (12, 0.2, 4.4)
wall_mat = bpy.data.materials.new(name="WallMat")
wall_mat.use_nodes = True
bsdf_w = wall_mat.node_tree.nodes.get("Principled BSDF")
if bsdf_w:
    bsdf_w.inputs["Base Color"].default_value = (0.07, 0.08, 0.10, 1.0) # Architectural dark slate
    bsdf_w.inputs["Roughness"].default_value = 0.95
wall.data.materials.append(wall_mat)

# Minimalist Round Dining Table Under Lamp
bpy.ops.mesh.primitive_cylinder_add(radius=0.75, depth=0.04, location=(0, 0, 0.74))
table_top = bpy.context.active_object
table_top.name = "TableTop"
table_mat = bpy.data.materials.new(name="TableMat")
table_mat.use_nodes = True
bsdf_t = table_mat.node_tree.nodes.get("Principled BSDF")
if bsdf_t:
    bsdf_t.inputs["Base Color"].default_value = (0.16, 0.17, 0.19, 1.0) # Matte black timber
    bsdf_t.inputs["Roughness"].default_value = 0.4
table_top.data.materials.append(table_mat)

# Table Leg Pedestal
bpy.ops.mesh.primitive_cylinder_add(radius=0.12, depth=0.72, location=(0, 0, 0.36))
table_leg = bpy.context.active_object
table_leg.data.materials.append(table_mat)

# 4. Import TESS-LUMEN 3D Model
model_path = Path(model_file).resolve()
bpy.ops.wm.obj_import(filepath=str(model_path))

# Elevate pendant so it hangs gracefully 85cm above table (Z = 1.62m)
imported_objects = [o for o in scene.objects if o not in [floor, wall, table_top, table_leg]]
pendant_parent = bpy.data.objects.new("TESS_LUMEN_Pendant", None)
scene.collection.objects.link(pendant_parent)
pendant_parent.location = (0, 0, 1.62)

for obj in imported_objects:
    obj.parent = pendant_parent

# Assign PBR Shaders
birch_mat = bpy.data.materials.new(name="CraftBirch")
birch_mat.use_nodes = True
bsdf_b = birch_mat.node_tree.nodes.get("Principled BSDF")
if bsdf_b:
    bsdf_b.inputs["Base Color"].default_value = (0.82, 0.68, 0.52, 1.0) # Blonde birch wood
    bsdf_b.inputs["Roughness"].default_value = 0.48

brass_mat = bpy.data.materials.new(name="BrassAccents")
brass_mat.use_nodes = True
bsdf_br = brass_mat.node_tree.nodes.get("Principled BSDF")
if bsdf_br:
    bsdf_br.inputs["Base Color"].default_value = (0.95, 0.76, 0.38, 1.0)
    bsdf_br.inputs["Metallic"].default_value = 0.95
    bsdf_br.inputs["Roughness"].default_value = 0.22

# 5. Lighting: Warm Internal Core Light
core_light = bpy.data.lights.new(name="OrigamiCoreLight", type='POINT')
core_light.energy = 220
core_light.color = (1.0, 0.82, 0.62) # 2700K warm incandescent
core_light.shadow_soft_size = 0.05 # Sharp, crystalline geometric facet shadows!
core_obj = bpy.data.objects.new(name="OrigamiCoreLight", object_data=core_light)
scene.collection.objects.link(core_obj)
core_obj.location = (0, 0, 1.62)

# Soft Cool Ambient Fill
sun = bpy.data.lights.new(name="WindowAmbient", type='SUN')
sun.energy = 0.8
sun.color = (0.8, 0.9, 1.0)
sun.angle = math.radians(12.0)
sun_obj = bpy.data.objects.new(name="WindowAmbient", object_data=sun)
scene.collection.objects.link(sun_obj)
sun_obj.rotation_euler = (math.radians(50), math.radians(15), math.radians(-40))

# 6. Architectural Camera (Eye-Level 35mm Prime)
cam_data = bpy.data.cameras.new(name="ArchCamera")
cam_data.lens = 35
cam_obj = bpy.data.objects.new(name="ArchCamera", object_data=cam_data)
scene.collection.objects.link(cam_obj)
scene.camera = cam_obj

cam_obj.location = (1.8, -2.4, 1.45) # 1.45m eye level
cam_obj.rotation_euler = (math.radians(78), 0, math.radians(36))

# 7. Render
scene.render.filepath = str(Path(output_file).resolve())
scene.render.image_settings.file_format = 'PNG'
print(f"[*] Rendering image with Cycles ({scene.cycles.samples} samples)...")
bpy.ops.render.render(write_still=True)
print(f"[+] Render complete: {scene.render.filepath}")
