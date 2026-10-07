"""
STRATAVOX Production Architectural Cycles Renderer
Sets up an architectural gallery context with PBR materials, warm circadian lighting,
and two-point perspective camera, rendering with Blender 5.1 Cycles.
"""

import bpy
import sys
import math
from pathlib import Path

# Parse arguments
argv = sys.argv
args = []
if "--" in argv:
    args = argv[argv.index("--") + 1:]

model_file = args[0] if len(args) > 0 else "models/stratavox_vaulted.obj"
output_file = args[1] if len(args) > 1 else "renders/stratavox_perspective_cycles.png"

Path(output_file).parent.mkdir(parents=True, exist_ok=True)
print(f"[*] Rendering STRATAVOX with Blender 5.1 Cycles...")
print(f"[*] Model: {model_file} -> Target: {output_file}")

# 1. Clear scene
bpy.ops.wm.read_factory_settings(use_empty=True)
scene = bpy.context.scene

# 2. Render Settings (Cycles GPU/CPU)
scene.render.engine = 'CYCLES'
scene.cycles.device = 'CPU'
scene.cycles.samples = 128
scene.cycles.use_denoising = True
scene.render.resolution_x = 1920
scene.render.resolution_y = 1080
scene.render.resolution_percentage = 100
scene.view_settings.view_transform = 'AgX'
scene.view_settings.look = 'AgX - Medium High Contrast'

# 3. Create Interior Architectural Room
# Polished Terrazzo/Concrete Floor
bpy.ops.mesh.primitive_plane_add(size=20, location=(0, 0, 0))
floor = bpy.context.active_object
floor.name = "ArchitecturalFloor"
floor_mat = bpy.data.materials.new(name="FloorMat")
floor_mat.use_nodes = True
nodes = floor_mat.node_tree.nodes
bsdf = nodes.get("Principled BSDF")
if bsdf:
    bsdf.inputs["Base Color"].default_value = (0.12, 0.13, 0.15, 1.0)
    bsdf.inputs["Roughness"].default_value = 0.22 # Polished sheen with soft reflections
    bsdf.inputs["Metallic"].default_value = 0.05
floor.data.materials.append(floor_mat)

# Gallery Concrete Feature Wall
bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 5, 2.5))
wall = bpy.context.active_object
wall.scale = (16, 0.3, 5)
wall.name = "BackWall"
wall_mat = bpy.data.materials.new(name="WallMat")
wall_mat.use_nodes = True
bsdf_w = wall_mat.node_tree.nodes.get("Principled BSDF")
if bsdf_w:
    bsdf_w.inputs["Base Color"].default_value = (0.08, 0.09, 0.11, 1.0)
    bsdf_w.inputs["Roughness"].default_value = 0.92
wall.data.materials.append(wall_mat)

# 4. Import STRATAVOX Canopy Model
model_path = Path(model_file).resolve()
bpy.ops.wm.obj_import(filepath=str(model_path))

# Elevate STRATAVOX to suspension height (Z = 2.4m)
imported_objects = [o for o in scene.objects if o not in [floor, wall]]
canopy_parent = bpy.data.objects.new("STRATAVOX_Canopy", None)
scene.collection.objects.link(canopy_parent)
canopy_parent.location = (0, 0, 2.4)

for obj in imported_objects:
    obj.parent = canopy_parent

# Assign PBR Shaders to Model Elements
birch_mat = bpy.data.materials.new(name="FinnishBirch")
birch_mat.use_nodes = True
bsdf_b = birch_mat.node_tree.nodes.get("Principled BSDF")
if bsdf_b:
    bsdf_b.inputs["Base Color"].default_value = (0.78, 0.62, 0.44, 1.0) # Warm blonde birch
    bsdf_b.inputs["Roughness"].default_value = 0.52

brass_mat = bpy.data.materials.new(name="ArchitecturalBrass")
brass_mat.use_nodes = True
bsdf_br = brass_mat.node_tree.nodes.get("Principled BSDF")
if bsdf_br:
    bsdf_br.inputs["Base Color"].default_value = (0.95, 0.76, 0.38, 1.0) # Satin brass
    bsdf_br.inputs["Metallic"].default_value = 0.98
    bsdf_br.inputs["Roughness"].default_value = 0.25

# 5. Lighting Setup
# Internal Warm Glow (2700K candlelight inside canopy)
light_data = bpy.data.lights.new(name="CanopyGlow", type='POINT')
light_data.energy = 280
light_data.color = (1.0, 0.82, 0.62)
light_data.shadow_soft_size = 0.25
light_obj = bpy.data.objects.new(name="CanopyGlow", object_data=light_data)
scene.collection.objects.link(light_obj)
light_obj.location = (0, 0, 2.25)

# Downlight spotlight onto floor (casting geometric auxetic shadows)
spot_data = bpy.data.lights.new(name="CanopySpot", type='SPOT')
spot_data.energy = 450
spot_data.color = (1.0, 0.92, 0.82)
spot_data.spot_size = math.radians(65)
spot_data.spot_blend = 0.3
spot_obj = bpy.data.objects.new(name="CanopySpot", object_data=spot_data)
scene.collection.objects.link(spot_obj)
spot_obj.location = (0, 0, 2.35)
spot_obj.rotation_euler = (0, 0, 0)

# Soft Cool Ambient Fill (Contrast)
sun_data = bpy.data.lights.new(name="SunAmbient", type='SUN')
sun_data.energy = 1.2
sun_data.color = (0.75, 0.85, 1.0)
sun_data.angle = math.radians(10.0)
sun_obj = bpy.data.objects.new(name="SunAmbient", object_data=sun_data)
scene.collection.objects.link(sun_obj)
sun_obj.rotation_euler = (math.radians(45), math.radians(20), math.radians(-35))

# 6. Architectural Camera (Eye-Level 3/4 Perspective)
cam_data = bpy.data.cameras.new(name="ArchCamera")
cam_data.lens = 38 # Architectural 38mm prime lens
cam_obj = bpy.data.objects.new(name="ArchCamera", object_data=cam_data)
scene.collection.objects.link(cam_obj)
scene.camera = cam_obj

cam_obj.location = (2.6, -3.4, 1.65) # Eye level 1.65m
cam_obj.rotation_euler = (math.radians(78), 0, math.radians(35))

# 7. Render Execution
scene.render.filepath = str(Path(output_file).resolve())
scene.render.image_settings.file_format = 'PNG'
print(f"[*] Rendering high-resolution 1080p image with Cycles (128 samples)...")
bpy.ops.render.render(write_still=True)
print(f"[+] Render complete: {scene.render.filepath}")
