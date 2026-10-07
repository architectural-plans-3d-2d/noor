"""
TESS-LUMEN Mode A: Acoustic Wall Sconce Renderer
Renders the flat tessellated panel mounted on a Scandinavian living room wall
with ambient perimeter halo lighting and acoustic texture.
"""

import bpy
import sys
import math
from pathlib import Path

model_file = "models/tess_lumen_flat.obj"
output_file = "renders/tess_lumen_wall_cycles.png"

Path(output_file).parent.mkdir(parents=True, exist_ok=True)
print(f"[*] Rendering TESS-LUMEN Wall Sconce Mode with Cycles...")

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

# 3. Environment: Scandinavian Living Room
# Light Oak Floor
bpy.ops.mesh.primitive_plane_add(size=14, location=(0, 0, 0))
floor = bpy.context.active_object
floor.name = "Floor"
floor_mat = bpy.data.materials.new(name="FloorMat")
floor_mat.use_nodes = True
bsdf_f = floor_mat.node_tree.nodes.get("Principled BSDF")
if bsdf_f:
    bsdf_f.inputs["Base Color"].default_value = (0.55, 0.44, 0.33, 1.0) # Light blonde oak
    bsdf_f.inputs["Roughness"].default_value = 0.45
floor.data.materials.append(floor_mat)

# Gallery Plaster Wall
bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 2.0, 2.2))
wall = bpy.context.active_object
wall.scale = (12, 0.2, 4.4)
wall_mat = bpy.data.materials.new(name="PlasterWall")
wall_mat.use_nodes = True
bsdf_w = wall_mat.node_tree.nodes.get("Principled BSDF")
if bsdf_w:
    bsdf_w.inputs["Base Color"].default_value = (0.88, 0.87, 0.84, 1.0) # Off-white warm gallery plaster
    bsdf_w.inputs["Roughness"].default_value = 0.88
wall.data.materials.append(wall_mat)

# Low Credenza / Sideboard under the panel
bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 1.6, 0.35))
credenza = bpy.context.active_object
credenza.scale = (2.0, 0.45, 0.7)
credenza_mat = bpy.data.materials.new(name="CredenzaMat")
credenza_mat.use_nodes = True
bsdf_c = credenza_mat.node_tree.nodes.get("Principled BSDF")
if bsdf_c:
    bsdf_c.inputs["Base Color"].default_value = (0.15, 0.16, 0.18, 1.0) # Charcoal oak
    bsdf_c.inputs["Roughness"].default_value = 0.5
credenza.data.materials.append(credenza_mat)

# 4. Import TESS-LUMEN Flat Panel Model
model_path = Path(model_file).resolve()
bpy.ops.wm.obj_import(filepath=str(model_path))

# Mount panel vertically flat on wall at eye level (Z = 1.6m, Y = 1.88m)
imported_objects = [o for o in scene.objects if o not in [floor, wall, credenza]]
panel_parent = bpy.data.objects.new("TESS_LUMEN_WallPanel", None)
scene.collection.objects.link(panel_parent)
panel_parent.location = (0, 1.88, 1.6)
panel_parent.rotation_euler = (math.radians(-90), 0, 0) # Rotate to vertical wall orientation

for obj in imported_objects:
    obj.parent = panel_parent

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

# 5. Lighting: Perimeter Halo Wall Graze
halo_light = bpy.data.lights.new(name="HaloGraze", type='AREA')
halo_light.energy = 160
halo_light.size = 1.2
halo_light.size_y = 0.6
halo_light.color = (1.0, 0.88, 0.72) # 2700K warm halo
halo_obj = bpy.data.objects.new(name="HaloGraze", object_data=halo_light)
scene.collection.objects.link(halo_obj)
halo_obj.location = (0, 1.89, 1.6)
halo_obj.rotation_euler = (math.radians(90), 0, 0) # Face towards wall

# Daylight Window Fill
sun = bpy.data.lights.new(name="WindowSun", type='SUN')
sun.energy = 1.5
sun.color = (0.9, 0.95, 1.0)
sun_obj = bpy.data.objects.new(name="WindowSun", object_data=sun)
scene.collection.objects.link(sun_obj)
sun_obj.rotation_euler = (math.radians(45), math.radians(30), math.radians(-30))

# 6. Architectural Camera (Straight-On Elevation View with slight angle)
cam_data = bpy.data.cameras.new(name="WallCamera")
cam_data.lens = 42
cam_obj = bpy.data.objects.new(name="WallCamera", object_data=cam_data)
scene.collection.objects.link(cam_obj)
scene.camera = cam_obj
cam_obj.location = (0.6, -1.8, 1.5)
cam_obj.rotation_euler = (math.radians(88), 0, math.radians(16))

# 7. Render
scene.render.filepath = str(Path(output_file).resolve())
scene.render.image_settings.file_format = 'PNG'
print(f"[*] Rendering Wall Sconce mode with Cycles ({scene.cycles.samples} samples)...")
bpy.ops.render.render(write_still=True)
print(f"[+] Render complete: {scene.render.filepath}")
