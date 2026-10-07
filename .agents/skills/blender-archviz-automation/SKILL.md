---
name: blender-archviz-automation
description: Automates Blender 5.1 via Python scripts for headless and interactive 3D modeling, material node generation, Cycles photorealistic rendering, camera composition, and GLTF/OBJ exports.
---

# Blender ArchViz Automation Skill

## Executable Location
- Blender 5.1 is installed at: `C:\Program Files\Blender Foundation\Blender 5.1\blender.exe`
- Runner script: `python scripts/blender_runner.py <script_to_run.py> [args]`
- Direct headless execution:
  `& "C:\Program Files\Blender Foundation\Blender 5.1\blender.exe" -b -P <script.py>`

## Key Automation Capabilities

### 1. Headless Scene Creation & Modeling
Python scripts executed via Blender's `bpy` module can:
- Clear default cube/light/camera.
- Generate parametric geometry via `bmesh` or `bpy.ops.mesh.primitive_*_add`.
- Apply Boolean modifiers (`DIFFERENCE`, `UNION`) for window and door cutouts.
- Set up modifiers: `BEVEL` (for realistic micro-rounded architectural edges), `SOLIDIFY` (for wall thickness), `ARRAY` (for structural columns / pergolas).

### 2. Architectural Camera Setup
- **Focal Length:** 24mm - 35mm for interior rooms; 50mm - 85mm for exterior elevations to prevent wide-angle distortion.
- **Two-Point Perspective (Vertical Shift):** Set camera `rotation_euler.x = 90°` and adjust `shift_y` to maintain perfectly straight vertical building lines (standard architectural photography technique).
- **Depth of Field:** Subtle aperture `f/5.6` or `f/8` focused on the building facade.

### 3. Lighting & Sun Position
- **Nishita Sky Texture:** Realistic physical atmosphere model with controllable sun elevation, sun rotation, turbidity, and ozone.
- **Cycles Engine Configuration:**
  - Device: GPU (`OPTIX` or `CUDA`) with CPU fallback.
  - Samples: 128 - 256 with OpenImageDenoise enabled.
  - Color Management: View Transform `AgX` or `Filmic`, Look `Medium High Contrast`.

### 4. PBR Shader Graphs
- Principled BSDF v2 node trees with procedural noise for subtle wall imperfections, roughness variation, and glass transmission.
