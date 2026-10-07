"""
DAATA HAMLET RESIDENCE - Blender 5.1 Cycles Photorealistic Elevation Renderer
Renders the complete canopy-style 3-storey residence from the South Access Road:
- Full 87'-11" frontage in frame: 2-Car Canopy Porch, Travertine Drawing Room,
  floating 1F terrace, 2F timber pergola, and signature charcoal bronze canopy fascias
- Physically-based PBR materials with AgX color management
- Multiple-Scattering physical atmosphere at 4:30 PM golden hour
- 2-point perspective camera aligned directly with the south facade
"""
from __future__ import annotations
import bpy
import math
import sys
from pathlib import Path

PROJ_ROOT = Path(__file__).resolve().parents[2]
OBJ_FILE = PROJ_ROOT / "models" / "daata_hamlet.obj"
RENDER_OUT = PROJ_ROOT / "renders" / "daata_hamlet_canopy_cycles.png"
ISO_OUT = PROJ_ROOT / "renders" / "daata_hamlet_canopy_aerial.png"
RENDER_OUT.parent.mkdir(parents=True, exist_ok=True)

print(f"[*] Starting Blender 5.1 Cycles photoreal render for DAATA HAMLET RESIDENCE...")

# 1. Reset scene
bpy.ops.wm.read_factory_settings(use_empty=True)
scene = bpy.context.scene

# 2. Render Settings
scene.render.engine = 'CYCLES'
scene.cycles.device = 'CPU'
scene.cycles.samples = 64
scene.cycles.use_denoising = True
scene.render.resolution_x = 1920
scene.render.resolution_y = 1080
scene.render.resolution_percentage = 100
scene.view_settings.view_transform = 'AgX'
scene.view_settings.look = 'AgX - Medium High Contrast'
scene.view_settings.exposure = -1.2

# 3. Import Wavefront OBJ
print("[*] Importing 3D architectural model geometry...")
try:
    bpy.ops.wm.obj_import(filepath=str(OBJ_FILE))
except Exception as e:
    bpy.ops.import_scene.obj(filepath=str(OBJ_FILE))

# 4. PBR Materials
def setup_node_material(mat_name, base_color, roughness, metallic=0.0, transmission=0.0, ior=1.45, alpha=1.0):
    mat = bpy.data.materials.get(mat_name)
    if not mat:
        mat = bpy.data.materials.new(name=mat_name)
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    nodes.clear()

    out_node = nodes.new(type="ShaderNodeOutputMaterial")
    out_node.location = (400, 0)
    bsdf = nodes.new(type="ShaderNodeBsdfPrincipled")
    bsdf.location = (0, 0)

    bsdf.inputs["Base Color"].default_value = base_color
    bsdf.inputs["Roughness"].default_value = roughness
    bsdf.inputs["Metallic"].default_value = metallic

    if transmission > 0.0:
        if "Transmission Weight" in bsdf.inputs:
            bsdf.inputs["Transmission Weight"].default_value = transmission
        elif "Transmission" in bsdf.inputs:
            bsdf.inputs["Transmission"].default_value = transmission
        bsdf.inputs["IOR"].default_value = ior
        if "Alpha" in bsdf.inputs:
            bsdf.inputs["Alpha"].default_value = alpha

    links.new(bsdf.outputs["BSDF"], out_node.inputs["Surface"])
    return mat

setup_node_material("Plaster_White_Stucco", (0.80, 0.79, 0.77, 1.0), roughness=0.85, metallic=0.02)
setup_node_material("Canopy_Charcoal_Bronze", (0.08, 0.08, 0.10, 1.0), roughness=0.22, metallic=0.88)
setup_node_material("RCC_Concrete_Slabs", (0.70, 0.69, 0.67, 1.0), roughness=0.75, metallic=0.04)
setup_node_material("RCC_Columns_Concealed", (0.74, 0.73, 0.71, 1.0), roughness=0.80, metallic=0.05)
setup_node_material("RCC_Tie_Beams", (0.72, 0.71, 0.69, 1.0), roughness=0.80, metallic=0.05)
setup_node_material("Teak_Pergola_Louvers", (0.52, 0.30, 0.15, 1.0), roughness=0.48, metallic=0.0)
setup_node_material("Walnut_Entry_Door", (0.30, 0.16, 0.09, 1.0), roughness=0.40, metallic=0.0)
setup_node_material("Architectural_Glass", (0.85, 0.92, 0.95, 1.0), roughness=0.04, metallic=0.0, transmission=0.95, ior=1.52, alpha=0.20)
setup_node_material("Aluminum_Graphite_Frames", (0.14, 0.15, 0.17, 1.0), roughness=0.28, metallic=0.85)
setup_node_material("Travertine_Stone_Cladding", (0.70, 0.64, 0.56, 1.0), roughness=0.88, metallic=0.02)
setup_node_material("Landscape_Lawn_Grass", (0.14, 0.32, 0.10, 1.0), roughness=0.90, metallic=0.0)
setup_node_material("Exterior_Stone_Paving", (0.78, 0.76, 0.72, 1.0), roughness=0.65, metallic=0.05)
setup_node_material("Public_Road_Asphalt", (0.14, 0.14, 0.15, 1.0), roughness=0.92, metallic=0.0)
setup_node_material("Interior_Marble_Flooring", (0.80, 0.79, 0.76, 1.0), roughness=0.35, metallic=0.05)
setup_node_material("Interior_Flooring", (0.74, 0.70, 0.64, 1.0), roughness=0.45, metallic=0.0)
setup_node_material("Black_Granite_Counters", (0.06, 0.06, 0.07, 1.0), roughness=0.18, metallic=0.10)
setup_node_material("Overhead_Water_Tank", (0.90, 0.91, 0.92, 1.0), roughness=0.25, metallic=0.55)
setup_node_material("MEP_Stainless_Ducts", (0.65, 0.67, 0.70, 1.0), roughness=0.30, metallic=0.90)

# Hide boundary wall for unobstructed elevation view
b_obj = bpy.data.objects.get("Boundary_Wall_Site") or bpy.data.objects.get("Arch_Boundary_Wall_Site")
if b_obj:
    b_obj.hide_render = True

# 5. Camera Setup: South Facade Canopy Perspective
print("[*] Setting up South elevation perspective camera...")
target_obj = bpy.data.objects.new("FocalTarget", None)
target_obj.location = (16.5, 5.0, 4.5)
scene.collection.objects.link(target_obj)

cam_data = bpy.data.cameras.new(name="SouthElevationCamera")
cam_data.lens = 24.0  # 24mm architectural wide prime
cam_data.sensor_width = 36.0
cam_data.shift_y = 0.08  # Balanced framing for 3-storey elevation

cam_obj = bpy.data.objects.new(name="SouthElevationCamObj", object_data=cam_data)
# Positioned centered across the South access road looking directly at the residence
cam_obj.location = (16.5, -30.0, 4.5)

track = cam_obj.constraints.new(type='TRACK_TO')
track.target = target_obj
track.track_axis = 'TRACK_NEGATIVE_Z'
track.up_axis = 'UP_Y'

scene.collection.objects.link(cam_obj)
scene.camera = cam_obj

# 6. Nishita Physical Sky & Afternoon Sunlight
print("[*] Setting up Nishita physical sky and golden hour lighting...")
world = bpy.data.worlds.new(name="ArchWorld")
scene.world = world
world.use_nodes = True
wnodes = world.node_tree.nodes
wlinks = world.node_tree.links
wnodes.clear()

w_out = wnodes.new(type="ShaderNodeOutputWorld")
sky_node = wnodes.new(type="ShaderNodeTexSky")
sky_node.sky_type = 'MULTIPLE_SCATTERING'
sky_node.sun_elevation = math.radians(28.0)  # 28 deg afternoon sun
sky_node.sun_rotation = math.radians(205.0)  # Sun coming from southwest, casting dramatic shadows under canopies
sky_node.altitude = 10.0
sky_node.air_density = 1.0
sky_node.aerosol_density = 1.4
sky_node.ozone_density = 1.0
sky_node.sun_intensity = 0.75

wlinks.new(sky_node.outputs["Color"], w_out.inputs["Surface"])

# 7. Interior Warm Evening Lights (3000K)
fixtures = [
    ("Porch_Downlight", (8.5, 2.8, 3.2), 40.0, (1.0, 0.88, 0.70)),
    ("Drawing_Room_Chandelier", (14.2, 3.2, 2.6), 60.0, (1.0, 0.86, 0.65)),
    ("Ground_Lounge_Cove", (18.5, 6.5, 2.8), 45.0, (1.0, 0.88, 0.70)),
    ("First_Floor_Lounge_Glow", (18.0, 7.0, 6.2), 50.0, (1.0, 0.88, 0.70)),
    ("First_Floor_Terrace_Sconce", (9.0, 3.0, 6.6), 30.0, (1.0, 0.90, 0.75)),
    ("Second_Floor_Pergola_Lights", (14.0, 7.5, 9.5), 35.0, (1.0, 0.85, 0.65)),
]
for name, loc, power, col in fixtures:
    light_data = bpy.data.lights.new(name=name, type='POINT')
    light_data.energy = power
    light_data.color = col
    light_data.shadow_soft_size = 0.5
    light_obj = bpy.data.objects.new(name=name, object_data=light_data)
    light_obj.location = loc
    scene.collection.objects.link(light_obj)

# 8. Render Frame 1: Full Front Elevation Perspective
print(f"[*] Rendering signature Canopy-Style South Elevation to: {RENDER_OUT}...")
scene.render.filepath = str(RENDER_OUT)
bpy.ops.render.render(write_still=True)
print(f"[+] Render written to: {RENDER_OUT}")

# 9. Render Frame 2: High 3/4 Aerial Perspective (Full Plot)
print(f"[*] Rendering high 3/4 aerial perspective to: {ISO_OUT}...")
if b_obj:
    b_obj.hide_render = False

cam_obj.location = (-6.0, -22.0, 16.0)
cam_data.lens = 26.0
cam_data.shift_y = 0.0
target_obj.location = (16.0, 6.0, 4.0)
scene.render.filepath = str(ISO_OUT)
bpy.ops.render.render(write_still=True)
print(f"[+] Aerial render written to: {ISO_OUT}")
print("[+] All renders completed successfully!")
