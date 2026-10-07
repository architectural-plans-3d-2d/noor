"""
STRATAVOX Reflected Ceiling Plan (RCP) Cycles Renderer
Renders a direct orthographic/elevated vertical view showing the
mesmerizing auxetic mandala geometry and brass/timber contrast.
"""

import bpy
import sys
import math
from pathlib import Path

# Parse arguments
model_file = "models/stratavox_vaulted.obj"
output_file = "renders/stratavox_rcp_cycles.png"

Path(output_file).parent.mkdir(parents=True, exist_ok=True)
print(f"[*] Rendering STRATAVOX RCP view with Cycles...")

# 1. Reset
bpy.ops.wm.read_factory_settings(use_empty=True)
scene = bpy.context.scene

# 2. Render Settings
scene.render.engine = 'CYCLES'
scene.cycles.device = 'CPU'
scene.cycles.samples = 96
scene.cycles.use_denoising = True
scene.render.resolution_x = 1440
scene.render.resolution_y = 1440 # Square format for architectural mandala presentation
scene.render.resolution_percentage = 100
scene.view_settings.view_transform = 'AgX'
scene.view_settings.look = 'AgX - Medium High Contrast'

# 3. Import Model
model_path = Path(model_file).resolve()
bpy.ops.wm.obj_import(filepath=str(model_path))

# 4. Materials
birch_mat = bpy.data.materials.new(name="FinnishBirch")
birch_mat.use_nodes = True
bsdf_b = birch_mat.node_tree.nodes.get("Principled BSDF")
if bsdf_b:
    bsdf_b.inputs["Base Color"].default_value = (0.78, 0.62, 0.44, 1.0)
    bsdf_b.inputs["Roughness"].default_value = 0.52

brass_mat = bpy.data.materials.new(name="ArchitecturalBrass")
brass_mat.use_nodes = True
bsdf_br = brass_mat.node_tree.nodes.get("Principled BSDF")
if bsdf_br:
    bsdf_br.inputs["Base Color"].default_value = (0.95, 0.76, 0.38, 1.0)
    bsdf_br.inputs["Metallic"].default_value = 0.98
    bsdf_br.inputs["Roughness"].default_value = 0.22

# 5. Lighting
# Under-canopy glow
light_data = bpy.data.lights.new(name="CenterGlow", type='POINT')
light_data.energy = 320
light_data.color = (1.0, 0.84, 0.65)
light_obj = bpy.data.objects.new(name="CenterGlow", object_data=light_data)
scene.collection.objects.link(light_obj)
light_obj.location = (0, 0, -0.3)

# Soft studio ring lights
for i in range(4):
    angle = (math.pi / 2) * i
    s_data = bpy.data.lights.new(name=f"StudioFill_{i}", type='AREA')
    s_data.energy = 80
    s_data.size = 2.0
    s_obj = bpy.data.objects.new(name=f"StudioFill_{i}", object_data=s_data)
    scene.collection.objects.link(s_obj)
    s_obj.location = (math.cos(angle) * 3.0, math.sin(angle) * 3.0, 2.5)

# 6. Orthographic/Top Camera Looking Straight Down
cam_data = bpy.data.cameras.new(name="TopCamera")
cam_data.type = 'PERSP'
cam_data.lens = 55
cam_obj = bpy.data.objects.new(name="TopCamera", object_data=cam_data)
scene.collection.objects.link(cam_obj)
scene.camera = cam_obj
cam_obj.location = (0, 0, 4.2)
cam_obj.rotation_euler = (0, 0, 0)

# 7. Render
scene.render.filepath = str(Path(output_file).resolve())
scene.render.image_settings.file_format = 'PNG'
print(f"[*] Rendering RCP view ({scene.cycles.samples} samples)...")
bpy.ops.render.render(write_still=True)
print(f"[+] Render complete: {scene.render.filepath}")
