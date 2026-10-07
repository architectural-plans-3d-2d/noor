---
name: threejs-viewer-and-rendering
description: Procedural WebGL and Three.js 3D visualization skill. Used to build interactive browser-based 3D architectural viewers, load glTF/GLB/OBJ models, set up PBR materials, shadows, camera controls, and render inline interactive artifacts.
---

# Three.js 3D Architectural Viewer & Rendering Skill

## Purpose
Enables creating standalone interactive 3D WebGL scenes using Three.js directly within the project or as interactive generative UI artifacts.

## Core Capabilities
1. **Interactive Camera & Navigation:**
   - `OrbitControls` with damping enabled for smooth panning, orbiting, and zooming.
   - Preset camera buttons: Isometric Front-Right, Top-Down Floor Plan, Street-Level Eye Perspective, Front Elevation.
   - Clipping plane support for sectional cutaways through building storeys.

2. **Architectural Lighting Rig:**
   - `DirectionalLight` (Sun): Casts soft shadows (`shadow.mapSize: 2048x2048`, bias tuning to eliminate shadow acne). Positioned at 45° azimuth and 50° elevation.
   - `HemisphereLight`: Sky light (soft warm white `0xffffff`) + ground bounce (subtle earthy warm gray `0x444444`).
   - `AmbientLight`: Low intensity fill (0.2) to prevent pitch-black shadows.
   - Optional interior point lights / spot lights with quadratic distance decay.

3. **PBR Materials (`MeshStandardMaterial` / `MeshPhysicalMaterial`):**
   - **Walls / Slabs:** Off-white matte plaster (`color: 0xf5f5f0, roughness: 0.85`).
   - **Glazing:** Transparent reflective glass (`color: 0x88ccff, transparent: true, opacity: 0.35, roughness: 0.1, transmission: 0.9`).
   - **Wood Floors / Timber Slatting:** Warm oak (`color: 0xc89d67, roughness: 0.45`).
   - **Mullions / Metal Trim:** Charcoal anodized aluminum (`color: 0x222222, metalness: 0.8, roughness: 0.25`).
   - **Grass / Landscape:** Natural muted green (`color: 0x6e8b5a, roughness: 0.95`).

4. **Model Formats Supported:**
   - Procedural Three.js Geometries (`BoxGeometry`, `ExtrudeGeometry` from SVG/2D shapes).
   - `.gltf` / `.glb` via `GLTFLoader`.
   - `.obj` / `.mtl` via `OBJLoader`.
