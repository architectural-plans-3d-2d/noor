"""
TESS-LUMEN Mode B: Self-Standing Spatial Screen & Reading Lamp Renderer
Renders the zigzag acoustic divider on an architectural workstation/desk
with warm crevice illumination and speech privacy zoning.
"""

import bpy
import sys
import math
from pathlib import Path

model_file = "models/tess_lumen_screen.obj"
output_file = "renders/tess_lumen_screen_cycles.png"

Path(output_file).parent.mkdir(parents=True, exist_ok=True)
print(f"[*] Rendering TESS-LUMEN Mode B (Spatial Screen) with Cycles...")

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

# 3. Environment: Minimalist Studio Desk
# Studio Floor
bpy.ops.mesh.primitive_plane_add(size=12, location=(0, 0, 0))
floor = bpy.context.active_object
floor.name = "Floor"
floor_mat = bpy.data.materials.new(name="FloorMat")
floor_mat.use_nodes = True
bsdf_f = floor_mat.node_tree.nodes.get("Principled BSDF")
if bsdf_f:
    bsdf_f.inputs["Base Color"].default_value = (0.16, 0.17, 0.19, 1.0)
    bsdf_f.inputs["Roughness"].default_value = 0.5
floor.data.materials.append(floor_mat)

# Studio Desk Surface
bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0.4, 0.72))
desk = bpy.context.active_object
desk.scale = (2.2, 0.9, 0.04)
desk.name = "DeskTop"
desk_mat = bpy.data.materials.new(name="DeskMat")
desk_mat.use_nodes = True
bsdf_d = desk_mat.node_tree.nodes.get("Principled BSDF")
if bsdf_d:
    bsdf_d.inputs["Base Color"].default_value = (0.75, 0.62, 0.48, 1.0) # Scandinavian blonde birch desk
    bsdf_d.inputs["Roughness"].default_value = 0.42
desk.data.materials.append(desk_mat)

# 4. Import TESS-LUMEN Screen Model
model_path = Path(model_file).resolve()
bpy.ops.wm.obj_import(filepath=str(model_path))

# Place on top of desk (Z = 0.74m)
imported_objects = [o for o in scene.objects if o not in [floor, desk]]
screen_parent = bpy.data.objects.new("TESS_LUMEN_Screen", None)
scene.collection.objects.link(screen_parent)
screen_parent.location = (0, 0.4, 0.74)

for obj in imported_objects:
    obj.parent = screen_parent

# Assign PBR Shaders
birch_mat = bpy.data.materials.new(name="CraftBirch")
birch_mat.use_nodes = True
bsdf_b = birch_mat.node_tree.nodes.get("Principled BSDF")
if bsdf_b:
    bsdf_b.inputs["Base Color"].default_value = (0.82, 0.68, 0.52, 1.0)
    bsdf_b.inputs["Roughness"].default_value = 0.48

felt_mat = bpy.data.materials.new(name="CharcoalFelt")
felt_mat.use_nodes = True
bsdf_ft = felt_mat.node_tree.nodes.get("Principled BSDF")
if bsdf_ft:
    bsdf_ft.inputs["Base Color"].default_value = (0.18, 0.20, 0.24, 1.0)
    bsdf_ft.inputs["Roughness"].default_value = 0.95

# 5. Lighting: Warm Crevice Task Light
crevice_light = bpy.data.lights.new(name="CreviceLight", type='POINT')
crevice_light.energy = 140
crevice_light.color = (1.0, 0.84, 0.65) # Warm task light
crevice_obj = bpy.data.objects.new(name="CreviceLight", object_data=crevice_light)
scene.collection.objects.link(crevice_obj)
crevice_obj.location = (0, 0.35, 1.0)

# Soft Desk Ambient Fill
sun = bpy.data.lights.new(name="WindowAmbient", type='SUN')
sun.energy = 1.2
sun.color = (0.85, 0.92, 1.0)
sun_obj = bpy.data.objects.new(name="WindowAmbient", object_data=sun)
scene.collection.objects.link(sun_obj)
sun_obj.rotation_euler = (math.radians(45), math.radians(25), math.radians(-30))

# 6. Architectural Camera (3/4 Desk Perspective)
cam_data = bpy.data.cameras.new(name="DeskCamera")
cam_data.lens = 45
cam_obj = bpy.data.objects.new(name="DeskCamera", object_data=cam_data)
scene.collection.objects.link(cam_obj)
scene.camera = cam_obj
cam_obj.location = (1.4, -1.2, 1.25)
cam_obj.rotation_euler = (math.radians(72), 0, math.radians(42))

# 7. Render
scene.render.filepath = str(Path(output_file).resolve())
scene.render.image_settings.file_format = 'PNG'
print(f"[*] Rendering Screen mode with Cycles ({scene.cycles.samples} samples)...")
bpy.ops.render.render(write_still=True)
print(f"[+] Render complete: {scene.render.filepath}")
