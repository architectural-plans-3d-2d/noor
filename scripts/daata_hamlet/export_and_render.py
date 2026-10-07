"""
DAATA HAMLET RESIDENCE - High-Precision 3D Geometry Builder, GLTF Exporter, & Cycles Photoreal Renderer
Automates Blender 5.1 to:
1. Procedurally assemble 3D architectural geometry from scripts/daata_hamlet/model.py
2. Build professional PBR architectural materials (smooth stucco, dark bronze canopy fascias,
   warm teak pergolas/louvers, architectural glass, concrete columns, travertine cladding, lush lawn)
3. Export high-performance models/daata_hamlet.obj and models/daata_hamlet.glb
4. Render 4K/FHD photorealistic canopy-style elevation perspective with Cycles (AgX tone mapping, Nishita sky)
"""
from __future__ import annotations
import bpy
import bmesh
import math
import sys
from pathlib import Path

# Add project root to sys.path so Blender can import scripts.daata_hamlet.model
PROJ_ROOT = Path(__file__).resolve().parents[2]
if str(PROJ_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJ_ROOT))

from shapely.geometry import Polygon, MultiPolygon
from scripts.daata_hamlet.model import (
    build, PLOT, SITE_POINTS, LEVEL, FLOOR_H, WALL_H, MUMTY_TOP,
    GX, GY, COLUMN_SPEC, column_rect
)

FT2M = 0.3048  # Exact architectural unit conversion feet -> meters

OBJ_OUT = PROJ_ROOT / "models" / "daata_hamlet.obj"
GLB_OUT = PROJ_ROOT / "models" / "daata_hamlet.glb"
RENDER_OUT = PROJ_ROOT / "renders" / "daata_hamlet_canopy_cycles.png"
OBJ_OUT.parent.mkdir(parents=True, exist_ok=True)
RENDER_OUT.parent.mkdir(parents=True, exist_ok=True)


def reset_blender_scene():
    """Clear all default objects, meshes, materials, and lights."""
    bpy.ops.wm.read_factory_settings(use_empty=True)
    # Ensure active scene
    scene = bpy.context.scene
    return scene


def create_pbr_material(name: str, color_rgba: tuple, roughness: float, metalness: float = 0.0,
                        transmission: float = 0.0, ior: float = 1.45, alpha: float = 1.0) -> bpy.types.Material:
    mat = bpy.data.materials.new(name=name)
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    nodes.clear()

    output = nodes.new(type="ShaderNodeOutputMaterial")
    output.location = (400, 0)
    bsdf = nodes.new(type="ShaderNodeBsdfPrincipled")
    bsdf.location = (0, 0)

    # Base Color
    bsdf.inputs["Base Color"].default_value = color_rgba
    bsdf.inputs["Roughness"].default_value = roughness
    bsdf.inputs["Metallic"].default_value = metalness

    # Transmission / Glass
    if transmission > 0.0:
        if "Transmission Weight" in bsdf.inputs:
            bsdf.inputs["Transmission Weight"].default_value = transmission
        elif "Transmission" in bsdf.inputs:
            bsdf.inputs["Transmission"].default_value = transmission
        bsdf.inputs["IOR"].default_value = ior
        if "Alpha" in bsdf.inputs:
            bsdf.inputs["Alpha"].default_value = alpha
        mat.blend_method = "BLEND"
        mat.shadow_method = "HASHED" if hasattr(mat, "shadow_method") else "NONE"

    links.new(bsdf.outputs["BSDF"], output.inputs["Surface"])
    return mat


def setup_all_materials() -> dict[str, bpy.types.Material]:
    mats = {}
    # 1. Exterior Plaster / Stucco (White minimalist modern)
    mats["plaster"] = create_pbr_material("Mat_Plaster", (0.93, 0.92, 0.90, 1.0), roughness=0.85, metalness=0.02)
    # 2. Signature Canopy Fascia & Dark Charcoal Trim
    mats["charcoal"] = create_pbr_material("Mat_Canopy_Bronze", (0.12, 0.12, 0.14, 1.0), roughness=0.25, metalness=0.85)
    # 3. Architectural Concrete (Slabs, Beams, Columns)
    mats["concrete"] = create_pbr_material("Mat_Concrete", (0.76, 0.75, 0.73, 1.0), roughness=0.75, metalness=0.04)
    mats["column"] = mats["concrete"]
    mats["beam"] = mats["concrete"]
    # 4. Warm Teak Louvers & Pergola Timber
    mats["timber"] = create_pbr_material("Mat_Teak_Wood", (0.55, 0.34, 0.18, 1.0), roughness=0.48, metalness=0.0)
    # 5. Walnut Entry Doors
    mats["timber_door"] = create_pbr_material("Mat_Walnut_Door", (0.32, 0.19, 0.11, 1.0), roughness=0.40, metalness=0.0)
    # 6. Architectural Double-Glazed Glass (Balustrades & Curtain Walls)
    mats["glass"] = create_pbr_material("Mat_Arch_Glass", (0.85, 0.93, 0.96, 1.0), roughness=0.05, metalness=0.0,
                                        transmission=0.92, ior=1.52, alpha=0.3)
    # 7. Dark Graphite Window Frames & Mullions
    mats["metal"] = create_pbr_material("Mat_Aluminum_Dark", (0.18, 0.19, 0.20, 1.0), roughness=0.30, metalness=0.85)
    # 8. Feature Stone Cladding (Drawing Room Front Volume)
    mats["stone"] = create_pbr_material("Mat_Travertine_Stone", (0.78, 0.73, 0.67, 1.0), roughness=0.88, metalness=0.02)
    # 9. Landscape Lawn Grass
    mats["grass"] = create_pbr_material("Mat_Lawn_Grass", (0.20, 0.42, 0.14, 1.0), roughness=0.90, metalness=0.0)
    # 10. Porch / Patio Travertine Paving
    mats["paving"] = create_pbr_material("Mat_Stone_Paving", (0.83, 0.81, 0.77, 1.0), roughness=0.65, metalness=0.05)
    # 11. Public Access Road Asphalt
    mats["asphalt"] = create_pbr_material("Mat_Road_Asphalt", (0.14, 0.14, 0.15, 1.0), roughness=0.92, metalness=0.0)
    # 12. Interior Honed Marble Floors
    mats["stone_floor"] = create_pbr_material("Mat_Interior_Floor", (0.88, 0.87, 0.84, 1.0), roughness=0.35, metalness=0.05)
    mats["floor"] = mats["stone_floor"]
    # 13. Black Granite Kitchen Countertops
    mats["counter"] = create_pbr_material("Mat_Black_Granite", (0.08, 0.08, 0.09, 1.0), roughness=0.18, metalness=0.10)
    # 14. Stainless / Fiberglass Overhead Tank
    mats["tank"] = create_pbr_material("Mat_Water_Tank", (0.92, 0.93, 0.95, 1.0), roughness=0.25, metalness=0.55)
    mats["duct"] = mats["metal"]
    return mats


def triangulate_2d_polygon(poly: Polygon) -> tuple[list[tuple[float, float]], list[tuple[int, int, int]]]:
    """Triangulates a shapely 2D polygon with potential interior holes into vertices and triangle index tuples."""
    # Use ear clipping with bridge lines for holes
    # Convert polygon with holes into a single boundary with seam bridges
    ext_coords = list(poly.exterior.coords)[:-1]
    all_pts = list(ext_coords)

    # For each hole, bridge it into exterior
    for interior in poly.interiors:
        hole_coords = list(interior.coords)[:-1]
        # Find closest pair
        min_d = float('inf')
        best_i = 0
        best_j = 0
        for i, p1 in enumerate(all_pts):
            for j, p2 in enumerate(hole_coords):
                d = (p1[0] - p2[0])**2 + (p1[1] - p2[1])**2
                if d < min_d:
                    min_d = d
                    best_i = i
                    best_j = j
        # Bridge: insert hole_coords reordered starting from best_j, then back to best_i
        n_hole = len(hole_coords)
        reordered_hole = [hole_coords[(best_j + k) % n_hole] for k in range(n_hole)]
        # Bridge sequence: best_i -> reordered_hole -> best_j -> best_i
        bridge_pts = all_pts[:best_i + 1] + reordered_hole + [reordered_hole[0]] + all_pts[best_i:]
        all_pts = bridge_pts

    # Ear clipping on the consolidated boundary
    pts = list(all_pts)
    n = len(pts)
    if n < 3:
        return pts, []

    # Signed area
    area = 0.0
    for i in range(n):
        j = (i + 1) % n
        area += pts[i][0] * pts[j][1] - pts[j][0] * pts[i][1]

    indices = list(range(n))
    if area < 0:
        indices.reverse()

    def is_convex(i0, i1, i2):
        p0, p1, p2 = pts[i0], pts[i1], pts[i2]
        cross = (p1[0] - p0[0]) * (p2[1] - p0[1]) - (p1[1] - p0[1]) * (p2[0] - p0[0])
        return cross > 1e-9

    def in_triangle(p, a, b, c):
        def sign(p1, p2, p3):
            return (p1[0] - p3[0]) * (p2[1] - p3[1]) - (p2[0] - p3[0]) * (p1[1] - p3[1])
        d1 = sign(p, a, b)
        d2 = sign(p, b, c)
        d3 = sign(p, c, a)
        return not ((d1 < -1e-9 or d2 < -1e-9 or d3 < -1e-9) and (d1 > 1e-9 or d2 > 1e-9 or d3 > 1e-9))

    tris = []
    attempts = 0
    max_attempts = len(indices) * 3
    while len(indices) > 3 and attempts < max_attempts:
        ear_found = False
        k = len(indices)
        for i in range(k):
            prev_idx = indices[(i - 1) % k]
            curr_idx = indices[i]
            next_idx = indices[(i + 1) % k]
            if not is_convex(prev_idx, curr_idx, next_idx):
                continue
            pa, pb, pc = pts[prev_idx], pts[curr_idx], pts[next_idx]
            any_inside = False
            for j in range(k):
                if j in ((i - 1) % k, i, (i + 1) % k):
                    continue
                if in_triangle(pts[indices[j]], pa, pb, pc):
                    any_inside = True
                    break
            if not any_inside:
                tris.append((prev_idx, curr_idx, next_idx))
                indices.pop(i)
                ear_found = True
                break
        attempts += 1
        if not ear_found and len(indices) > 3:
            tris.append((indices[0], indices[1], indices[2]))
            indices.pop(1)

    if len(indices) == 3:
        tris.append((indices[0], indices[1], indices[2]))

    return pts, tris


def build_3d_geometry(scene, mats: dict[str, bpy.types.Material]):
    print("[*] Assembling 3D architectural solids from parametric model...")
    m = build()

    # We bucket geometry by material name to create clean, grouped architectural objects
    # This keeps vertex buffers clean and allows instant material management
    bm_buckets = {mat_name: bmesh.new() for mat_name in mats}

    # 1. Boxes
    for b in m.boxes:
        mat_key = b.mat if b.mat in mats else "concrete"
        bm = bm_buckets[mat_key]
        x0, y0, z0 = b.x0 * FT2M, b.y0 * FT2M, b.z0 * FT2M
        x1, y1, z1 = b.x1 * FT2M, b.y1 * FT2M, b.z1 * FT2M

        # 8 vertices
        v0 = bm.verts.new((x0, y0, z0))
        v1 = bm.verts.new((x1, y0, z0))
        v2 = bm.verts.new((x1, y1, z0))
        v3 = bm.verts.new((x0, y1, z0))
        v4 = bm.verts.new((x0, y0, z1))
        v5 = bm.verts.new((x1, y0, z1))
        v6 = bm.verts.new((x1, y1, z1))
        v7 = bm.verts.new((x0, y1, z1))

        # 6 faces (outward facing)
        bm.faces.new((v0, v3, v2, v1))  # bottom
        bm.faces.new((v4, v5, v6, v7))  # top
        bm.faces.new((v0, v1, v5, v4))  # south
        bm.faces.new((v2, v3, v7, v6))  # north
        bm.faces.new((v3, v0, v4, v7))  # west
        bm.faces.new((v1, v2, v6, v5))  # east

    # 2. Prisms (slabs with stair cutouts, wedge party walls, diagonal dirty kitchen)
    for p in m.prisms:
        mat_key = p.mat if p.mat in mats else "concrete"
        bm = bm_buckets[mat_key]
        z0, z1 = p.z0 * FT2M, p.z1 * FT2M

        # Exterior side walls
        ext_coords = list(p.poly.exterior.coords)[:-1]
        n_ext = len(ext_coords)
        v_ext_bot = [bm.verts.new((x * FT2M, y * FT2M, z0)) for x, y in ext_coords]
        v_ext_top = [bm.verts.new((x * FT2M, y * FT2M, z1)) for x, y in ext_coords]
        for i in range(n_ext):
            nxt = (i + 1) % n_ext
            bm.faces.new((v_ext_bot[i], v_ext_bot[nxt], v_ext_top[nxt], v_ext_top[i]))

        # Interior hole side walls
        for interior in p.poly.interiors:
            hole_coords = list(interior.coords)[:-1]
            n_hole = len(hole_coords)
            v_h_bot = [bm.verts.new((x * FT2M, y * FT2M, z0)) for x, y in hole_coords]
            v_h_top = [bm.verts.new((x * FT2M, y * FT2M, z1)) for x, y in hole_coords]
            for i in range(n_hole):
                nxt = (i + 1) % n_hole
                # Reverse face normal so it points into the hole
                bm.faces.new((v_h_bot[nxt], v_h_bot[i], v_h_top[i], v_h_top[nxt]))

        # Top and bottom faces using 2D triangulation
        pts_2d, tris_2d = triangulate_2d_polygon(p.poly)
        v_bot_all = [bm.verts.new((x * FT2M, y * FT2M, z0)) for x, y in pts_2d]
        v_top_all = [bm.verts.new((x * FT2M, y * FT2M, z1)) for x, y in pts_2d]
        for i0, i1, i2 in tris_2d:
            try:
                # Bottom face (pointing down)
                bm.faces.new((v_bot_all[i0], v_bot_all[i2], v_bot_all[i1]))
                # Top face (pointing up)
                bm.faces.new((v_top_all[i0], v_top_all[i1], v_top_all[i2]))
            except ValueError:
                # Handle any coincident/duplicate edges safely
                pass

    # 3. Create Blender Mesh Objects from BMesh buckets
    collection = scene.collection
    created_objects = []
    for mat_name, bm in bm_buckets.items():
        if len(bm.verts) == 0:
            bm.free()
            continue

        bmesh.ops.remove_doubles(bm, verts=bm.verts, dist=0.0005)
        # Recalculate normals
        bmesh.ops.recalc_face_normals(bm, faces=bm.faces)

        mesh_data = bpy.data.meshes.new(name=f"Mesh_{mat_name}")
        bm.to_mesh(mesh_data)
        bm.free()

        obj = bpy.data.objects.new(name=f"Arch_{mat_name}", object_data=mesh_data)
        obj.data.materials.append(mats[mat_name])
        collection.objects.link(obj)
        created_objects.append(obj)
        print(f"  + Created {obj.name}: {len(mesh_data.vertices)} vertices, {len(mesh_data.polygons)} faces")

    return created_objects


def export_models():
    print(f"[*] Exporting 3D models to {OBJ_OUT} and {GLB_OUT}...")
    # Select all arch objects
    bpy.ops.object.select_all(action='SELECT')

    # Export Wavefront OBJ
    try:
        bpy.ops.wm.obj_export(filepath=str(OBJ_OUT), export_selected_objects=True)
    except Exception:
        bpy.ops.export_scene.obj(filepath=str(OBJ_OUT), use_selection=True)
    print(f"[+] Exported OBJ: {OBJ_OUT}")

    # Export glTF/GLB (Binary)
    bpy.ops.export_scene.gltf(
        filepath=str(GLB_OUT),
        export_format='GLB',
        use_selection=True,
        export_materials='EXPORT',
        export_yup=True
    )
    print(f"[+] Exported GLB: {GLB_OUT}")


def setup_cycles_camera_and_lighting(scene):
    print("[*] Setting up architectural Cycles camera & Nishita sky...")
    # 1. Render engine setup
    scene.render.engine = 'CYCLES'
    scene.cycles.device = 'CPU'
    scene.cycles.samples = 128
    scene.cycles.use_denoising = True
    scene.render.resolution_x = 2560
    scene.render.resolution_y = 1440
    scene.render.resolution_percentage = 100
    scene.view_settings.view_transform = 'AgX'
    scene.view_settings.look = 'AgX - Medium High Contrast'

    # 2. Camera Setup: 2-Point Perspective looking at the Canopy Entrance
    # House spans X ~ [5m, 27m], Y ~ [0m, 19m], Z ~ [0m, 12m]
    # Porch canopy is around X=8m, Y=2m
    # Main drawing room facade is X=13m to X=17m
    # Camera placed on opposite road side at eye level (Z=1.65m), looking up with tilt correction (shift_y)
    cam_data = bpy.data.cameras.new(name="ArchCamera")
    cam_data.lens = 28.0  # Architectural 28mm wide-angle
    cam_data.sensor_width = 36.0
    # Two-point perspective: camera level with horizon (pitch = 90 deg / horizontal), use shift_y for elevation
    cam_data.shift_y = 0.28  # Raises the framing without keystoning!

    cam_obj = bpy.data.objects.new(name="MainCanopyCamera", object_data=cam_data)
    # Position camera south-west on the road approach
    cam_obj.location = (6.0, -18.0, 1.65)
    # Target center of front facade: (15.0, 3.0, 4.5)
    dx = 15.0 - 6.0
    dy = 3.0 - (-18.0)
    yaw = math.atan2(dx, -dy)  # Horizontal yaw
    cam_obj.rotation_euler = (math.radians(90), 0.0, yaw)

    scene.collection.objects.link(cam_obj)
    scene.camera = cam_obj

    # 3. Environment & Nishita Physical Sky (Golden Hour 4:30 PM)
    world = bpy.data.worlds.new(name="ArchWorld")
    scene.world = world
    world.use_nodes = True
    wnodes = world.node_tree.nodes
    wlinks = world.node_tree.links
    wnodes.clear()

    w_out = wnodes.new(type="ShaderNodeOutputWorld")
    sky_node = wnodes.new(type="ShaderNodeTexSky")
    sky_node.sky_type = 'NISHITA'
    sky_node.sun_elevation = math.radians(24.0)  # Low warm afternoon sun
    sky_node.sun_rotation = math.radians(215.0)  # Sun coming from southwest, casting dramatic shadows under the canopies!
    sky_node.altitude = 15.0
    sky_node.air_density = 1.1
    sky_node.dust_density = 1.8
    sky_node.ozone_density = 1.0
    sky_node.sun_intensity = 1.0

    wlinks.new(sky_node.outputs["Color"], w_out.inputs["Surface"])

    # 4. Fill / Warm Bounce Sun Light
    sun_data = bpy.data.lights.new(name="SunBounce", type='SUN')
    sun_data.energy = 2.5
    sun_data.color = (1.0, 0.96, 0.90)
    sun_data.angle = math.radians(2.0)  # Soft architectural shadows
    sun_obj = bpy.data.objects.new(name="SunBounceObj", object_data=sun_data)
    sun_obj.rotation_euler = (math.radians(66), math.radians(12), math.radians(215))
    scene.collection.objects.link(sun_obj)

    # 5. Accent Interior Warm Lights (showing evening illumination through glass facade)
    accents = [
        ("GF_DrawingRoom_Glow", (14.0, 3.0, 2.5), 150.0, (1.0, 0.85, 0.65)),
        ("GF_Porch_Canopy_Glow", (8.0, 2.5, 3.2), 80.0, (1.0, 0.90, 0.75)),
        ("1F_Lounge_Glow", (18.0, 7.0, 5.8), 120.0, (1.0, 0.88, 0.70)),
        ("2F_Pergola_Glow", (14.0, 8.0, 8.8), 80.0, (1.0, 0.85, 0.65)),
    ]
    for name, loc, power, col in accents:
        pt_data = bpy.data.lights.new(name=name, type='POINT')
        pt_data.energy = power
        pt_data.color = col
        pt_data.shadow_soft_size = 0.4
        pt_obj = bpy.data.objects.new(name=name, object_data=pt_data)
        pt_obj.location = loc
        scene.collection.objects.link(pt_obj)


def render_cycles_still():
    print(f"[*] Rendering photorealistic image to {RENDER_OUT}...")
    bpy.context.scene.render.filepath = str(RENDER_OUT)
    bpy.ops.render.render(write_still=True)
    print(f"[+] Render complete: {RENDER_OUT}")


def main():
    scene = reset_blender_scene()
    mats = setup_all_materials()
    build_3d_geometry(scene, mats)
    export_models()
    setup_cycles_camera_and_lighting(scene)
    render_cycles_still()
    print("[*] All 3D architectural exports and photoreal renders completed successfully!")


if __name__ == "__main__":
    main()
