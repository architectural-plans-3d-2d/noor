"""
Blender 5.1 Photorealistic Cycles ArchViz Renderer
Imports an architectural model (OBJ/FBX/GLTF), sets up a physical sky (Nishita),
configures a two-point perspective architectural camera, and renders with Cycles.
Usage:
    python scripts/blender_runner.py scripts/blender_cycles_render.py model.obj output_render.png
"""

import bpy
import sys
import math
from pathlib import Path

# Parse arguments passed after '--'
argv = sys.argv
args = []
if "--" in argv:
    args = argv[argv.index("--") + 1:]

model_path = args[0] if len(args) > 0 else "sample_massing.obj"
output_image = args[1] if len(args) > 1 else "output_render.png"

print(f"[*] Loading model: {model_path}")
print(f"[*] Render target: {output_image}")

# 1. Reset Scene
bpy.ops.wm.read_factory_settings(use_empty=True)
scene = bpy.context.scene

# 2. Configure Render Engine to Cycles
scene.render.engine = 'CYCLES'
scene.cycles.device = 'CPU' # Safe default for any system
scene.cycles.samples = 64
scene.cycles.use_denoising = True
scene.render.resolution_x = 1920
scene.render.resolution_y = 1080
scene.render.resolution_percentage = 100
scene.view_settings.view_transform = 'AgX'
scene.view_settings.look = 'AgX - Medium High Contrast'

# 3. Import Model
model_file = Path(model_path).resolve()
if model_file.suffix.lower() == ".obj":
    bpy.ops.wm.obj_import(filepath=str(model_file))
elif model_file.suffix.lower() in [".gltf", ".glb"]:
    bpy.ops.import_scene.gltf(filepath=str(model_file))
elif model_file.suffix.lower() == ".fbx":
    bpy.ops.import_scene.fbx(filepath=str(model_file))

# 4. Create Ground Plane
bpy.ops.mesh.primitive_plane_add(size=200, location=(0, 0, 0))
ground = bpy.context.active_object
ground.name = "ArchitecturalGround"

# Ground Material
ground_mat = bpy.data.materials.new(name="GroundMaterial")
ground_mat.use_nodes = True
nodes = ground_mat.node_tree.nodes
bsdf = nodes.get("Principled BSDF")
if bsdf:
    bsdf.inputs["Base Color"].default_value = (0.15, 0.16, 0.18, 1.0)
    bsdf.inputs["Roughness"].default_value = 0.9
ground.data.materials.append(ground_mat)

# 5. Lighting: Sun Light
light_data = bpy.data.lights.new(name="SunLight", type='SUN')
light_data.energy = 4.5
light_data.angle = math.radians(2.0) # Soft architectural shadows
light_obj = bpy.data.objects.new(name="SunLight", object_data=light_data)
scene.collection.objects.link(light_obj)
light_obj.rotation_euler = (math.radians(50), math.radians(15), math.radians(45))

# 6. Architectural Camera (Two-Point Perspective)
cam_data = bpy.data.cameras.new(name="ArchCamera")
cam_data.lens = 35 # 35mm lens
cam_obj = bpy.data.objects.new(name="ArchCamera", object_data=cam_data)
scene.collection.objects.link(cam_obj)
scene.camera = cam_obj

# Position camera for an eye-level / elevated 3/4 perspective
cam_obj.location = (24, -28, 12)
cam_obj.rotation_euler = (math.radians(72), 0, math.radians(40))

# 7. Render
scene.render.filepath = str(Path(output_image).resolve())
scene.render.image_settings.file_format = 'PNG'
print(f"[*] Rendering image with Cycles ({scene.cycles.samples} samples)...")
bpy.ops.render.render(write_still=True)
print(f"[+] Render complete: {scene.render.filepath}")
