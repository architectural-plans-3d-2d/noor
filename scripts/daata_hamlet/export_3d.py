"""
DAATA HAMLET RESIDENCE - 3D Architectural Model Exporter
Converts parametric model solids (681 boxes, 24 prisms) into:
- models/daata_hamlet.obj (Wavefront OBJ with materials and groups)
- models/daata_hamlet.mtl (PBR material library)
- models/daata_hamlet.glb (Binary glTF for Three.js WebGL viewer and Blender Cycles)
"""
from __future__ import annotations
import math
import sys
import shutil
from pathlib import Path

PROJ_ROOT = Path(__file__).resolve().parents[2]
if str(PROJ_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJ_ROOT))

import numpy as np
import trimesh
from shapely.affinity import scale
from shapely.geometry import Polygon, MultiPolygon
from scripts.daata_hamlet.model import build

FT2M = 0.3048  # Architectural metric conversion (1 ft = 0.3048 m)

MATERIAL_SPECS = {
    "plaster": {
        "name": "Plaster_White_Stucco",
        "color": [238, 236, 230, 255],
        "roughness": 0.85,
        "metallic": 0.02,
    },
    "charcoal": {
        "name": "Canopy_Charcoal_Bronze",
        "color": [34, 36, 42, 255],
        "roughness": 0.25,
        "metallic": 0.85,
    },
    "concrete": {
        "name": "RCC_Concrete_Slabs",
        "color": [195, 193, 188, 255],
        "roughness": 0.75,
        "metallic": 0.04,
    },
    "column": {
        "name": "RCC_Columns_Concealed",
        "color": [205, 204, 200, 255],
        "roughness": 0.80,
        "metallic": 0.05,
    },
    "beam": {
        "name": "RCC_Tie_Beams",
        "color": [200, 198, 194, 255],
        "roughness": 0.80,
        "metallic": 0.05,
    },
    "timber": {
        "name": "Teak_Pergola_Louvers",
        "color": [165, 102, 54, 255],
        "roughness": 0.48,
        "metallic": 0.0,
    },
    "timber_door": {
        "name": "Walnut_Entry_Door",
        "color": [92, 55, 33, 255],
        "roughness": 0.40,
        "metallic": 0.0,
    },
    "glass": {
        "name": "Architectural_Glass",
        "color": [180, 220, 235, 120],  # Semi-transparent
        "roughness": 0.05,
        "metallic": 0.0,
    },
    "metal": {
        "name": "Aluminum_Graphite_Frames",
        "color": [48, 50, 54, 255],
        "roughness": 0.30,
        "metallic": 0.85,
    },
    "stone": {
        "name": "Travertine_Stone_Cladding",
        "color": [198, 186, 172, 255],
        "roughness": 0.88,
        "metallic": 0.02,
    },
    "grass": {
        "name": "Landscape_Lawn_Grass",
        "color": [75, 135, 45, 255],
        "roughness": 0.90,
        "metallic": 0.0,
    },
    "paving": {
        "name": "Exterior_Stone_Paving",
        "color": [212, 208, 198, 255],
        "roughness": 0.65,
        "metallic": 0.05,
    },
    "asphalt": {
        "name": "Public_Road_Asphalt",
        "color": [42, 42, 44, 255],
        "roughness": 0.92,
        "metallic": 0.0,
    },
    "stone_floor": {
        "name": "Interior_Marble_Flooring",
        "color": [225, 223, 218, 255],
        "roughness": 0.35,
        "metallic": 0.05,
    },
    "floor": {
        "name": "Interior_Flooring",
        "color": [215, 212, 205, 255],
        "roughness": 0.45,
        "metallic": 0.0,
    },
    "counter": {
        "name": "Black_Granite_Counters",
        "color": [24, 24, 26, 255],
        "roughness": 0.18,
        "metallic": 0.10,
    },
    "tank": {
        "name": "Overhead_Water_Tank",
        "color": [238, 240, 245, 255],
        "roughness": 0.25,
        "metallic": 0.55,
    },
    "duct": {
        "name": "MEP_Stainless_Ducts",
        "color": [170, 175, 180, 255],
        "roughness": 0.30,
        "metallic": 0.90,
    },
    "boundary": {
        "name": "Boundary_Wall_Site",
        "color": [215, 213, 208, 255],
        "roughness": 0.88,
        "metallic": 0.02,
    },
}


def build_and_export_3d():
    print("[*] Generating high-precision 3D architectural geometry...")
    m = build()

    # Bucket solids by material key
    buckets: dict[str, list[trimesh.Trimesh]] = {k: [] for k in MATERIAL_SPECS}

    for b in m.boxes:
        if b.layer == "boundary":
            mat_key = "boundary"
        else:
            mat_key = b.mat if b.mat in MATERIAL_SPECS else "concrete"
        dx = (b.x1 - b.x0) * FT2M
        dy = (b.y1 - b.y0) * FT2M
        dz = (b.z1 - b.z0) * FT2M
        cx = (b.x0 + b.x1) / 2 * FT2M
        cy = (b.y0 + b.y1) / 2 * FT2M
        cz = (b.z0 + b.z1) / 2 * FT2M
        box = trimesh.creation.box(extents=[dx, dy, dz])
        box.apply_translation([cx, cy, cz])
        buckets[mat_key].append(box)

    # 2. Prisms (slabs, angled party walls, dirty kitchen)
    for p in m.prisms:
        if p.layer == "boundary":
            mat_key = "boundary"
        else:
            mat_key = p.mat if p.mat in MATERIAL_SPECS else "concrete"
        h = (p.z1 - p.z0) * FT2M
        poly_scaled = scale(p.poly, xfact=FT2M, yfact=FT2M, origin=(0, 0))
        sub_polys = poly_scaled.geoms if isinstance(poly_scaled, MultiPolygon) else [poly_scaled]
        for sub in sub_polys:
            if not sub.is_empty and sub.area > 1e-5:
                prism = trimesh.creation.extrude_polygon(sub, height=h)
                prism.apply_translation([0, 0, p.z0 * FT2M])
                buckets[mat_key].append(prism)

    # 3. Assemble consolidated meshes per material
    scene = trimesh.Scene()
    combined_meshes = {}
    total_verts = 0
    total_faces = 0

    for mat_key, m_list in buckets.items():
        if not m_list:
            continue
        spec = MATERIAL_SPECS[mat_key]
        c_mesh = trimesh.util.concatenate(m_list)
        # Apply vertex colors
        color_rgba = np.array(spec["color"], dtype=np.uint8)
        c_mesh.visual.vertex_colors = np.tile(color_rgba, (len(c_mesh.vertices), 1))
        
        # PBR Material
        pbr = trimesh.visual.material.PBRMaterial(
            name=spec["name"],
            baseColorFactor=[c / 255.0 for c in spec["color"]],
            roughnessFactor=spec["roughness"],
            metallicFactor=spec["metallic"]
        )
        c_mesh.visual.material = pbr

        combined_meshes[spec["name"]] = c_mesh
        scene.add_geometry(c_mesh, node_name=spec["name"])
        total_verts += len(c_mesh.vertices)
        total_faces += len(c_mesh.faces)
        print(f"  + Architectural component [{spec['name']}]: {len(c_mesh.vertices)} verts, {len(c_mesh.faces)} faces")

    # 4. Export GLB (Binary glTF)
    glb_out = PROJ_ROOT / "models" / "daata_hamlet.glb"
    glb_data = scene.export(file_type="glb")
    glb_out.write_bytes(glb_data)
    print(f"[+] Exported glTF binary model: {glb_out} ({len(glb_data) / 1024:.1f} KB)")

    # 5. Export OBJ and MTL
    obj_out = PROJ_ROOT / "models" / "daata_hamlet.obj"
    mtl_out = PROJ_ROOT / "models" / "daata_hamlet.mtl"
    
    # Write custom multi-material OBJ file
    write_obj_and_mtl(combined_meshes, obj_out, mtl_out)
    print(f"[+] Exported Wavefront OBJ: {obj_out}")
    print(f"[+] Exported Material MTL: {mtl_out}")

    # 6. Copy GLB to public and dist folders for Three.js
    public_dir = PROJ_ROOT / "public" / "models"
    public_dir.mkdir(parents=True, exist_ok=True)
    shutil.copy2(glb_out, public_dir / "daata_hamlet.glb")
    
    dist_dir = PROJ_ROOT / "dist" / "models"
    dist_dir.mkdir(parents=True, exist_ok=True)
    shutil.copy2(glb_out, dist_dir / "daata_hamlet.glb")
    print(f"[+] Copied GLB model to web app directories: {public_dir} and {dist_dir}")

    # Summary
    extents = scene.bounds[1] - scene.bounds[0]
    print("=" * 60)
    print(f"3D ARCHITECTURAL MODEL METRICS:")
    print(f"  Total Vertices   : {total_verts:,}")
    print(f"  Total Faces      : {total_faces:,}")
    print(f"  Model Bounding X : {extents[0]:.2f} m ({extents[0] / FT2M:.1f} ft)")
    print(f"  Model Bounding Y : {extents[1]:.2f} m ({extents[1] / FT2M:.1f} ft)")
    print(f"  Model Bounding Z : {extents[2]:.2f} m ({extents[2] / FT2M:.1f} ft)")
    print("=" * 60)


def write_obj_and_mtl(mesh_dict: dict[str, trimesh.Trimesh], obj_path: Path, mtl_path: Path):
    """Writes standard Wavefront OBJ and companion MTL with named materials and objects."""
    # Write MTL
    mtl_lines = ["# DAATA HAMLET RESIDENCE PBR MATERIAL LIBRARY", ""]
    for mat_key, spec in MATERIAL_SPECS.items():
        name = spec["name"]
        r, g, b, a = [c / 255.0 for c in spec["color"]]
        mtl_lines.extend([
            f"newmtl {name}",
            f"Ka {r*0.2:.3f} {g*0.2:.3f} {b*0.2:.3f}",
            f"Kd {r:.3f} {g:.3f} {b:.3f}",
            f"Ks {spec['metallic']:.3f} {spec['metallic']:.3f} {spec['metallic']:.3f}",
            f"Ns {int((1.0 - spec['roughness']) * 100)}",
            f"d {a:.2f}",
            f"illum 2",
            ""
        ])
    mtl_path.write_text("\n".join(mtl_lines), encoding="utf-8")

    # Write OBJ
    obj_lines = [
        "# DAATA HAMLET RESIDENCE 3D ARCHITECTURAL MODEL",
        f"mtllib {mtl_path.name}",
        ""
    ]
    v_offset = 1
    for name, mesh in mesh_dict.items():
        obj_lines.append(f"o {name}")
        obj_lines.append(f"usemtl {name}")
        # Vertices
        for vx, vy, vz in mesh.vertices:
            obj_lines.append(f"v {vx:.5f} {vy:.5f} {vz:.5f}")
        # Faces
        for f in mesh.faces:
            obj_lines.append(f"f {f[0] + v_offset} {f[1] + v_offset} {f[2] + v_offset}")
        v_offset += len(mesh.vertices)
        obj_lines.append("")

    obj_path.write_text("\n".join(obj_lines), encoding="utf-8")


if __name__ == "__main__":
    build_and_export_3d()
