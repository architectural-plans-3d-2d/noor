# Project Architectural & 3D Engineering Standards

## 1. Unit & Coordinate Standards
- **Dimensional Units:** Meters (default for site, structural, and architectural plans).
- **Millimeters (mm):** Permitted for detailed joinery, door/window sections, and hardware.
- **Finished Floor Level (FFL):** Ground floor baseline is always defined at elevation `0.00m`.
- **Ceiling Clear Heights:** Minimum 3.0m for residential living/lounges; 2.8m for ancillary zones.

## 2. 3D Model Generation Guidelines
- **Watertight & Manifold Geometry:** Ensure all structural elements have proper volume and thickness (no zero-thickness single planes for walls/slabs).
- **PBR Material Consistency:** All materials must use standard physically based rendering parameters:
  - Concrete/Plaster: Roughness 0.85, Metalness 0.05
  - Architectural Glass: Transmission 0.85-0.95, IOR 1.50-1.52, Roughness 0.05-0.10
  - Timber/Wood: Roughness 0.45-0.60
  - Architectural Metals: Metalness 0.80-1.00, Roughness 0.20-0.35
- **Camera Standards:** Use two-point perspective for elevations and facade renders (maintain true vertical lines without keystone convergence).

## 3. Available Architectural Engines
- **Interactive WebGL:** Three.js pipeline (`npm run dev`, `npm run build`, `dist/`).
- **Photorealistic Offline Rendering:** Blender 5.1 Cycles (`scripts/blender_runner.py scripts/blender_cycles_render.py <model> <output.png>`).
- **Mesh Validation & Analysis:** Python `trimesh` (`scripts/mesh_pipeline.py <model>`).
