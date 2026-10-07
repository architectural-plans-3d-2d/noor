---
name: openscad-parametric-cad
description: Parametric CAD modeling skill using OpenSCAD and mathematical constructive solid geometry (CSG). Generates code-driven structural framing, joinery, and precise dimensioned architectural assemblies with export to STL, 3MF, and DXF.
---

# OpenSCAD Parametric CAD Skill

## Purpose
Enables writing programmatic, fully-parameterized 3D models where all dimensions (wall thicknesses, spans, column grids, window mullions) are variables.

## Guidelines
- Always define top-level configuration variables with units in millimeters or meters:
  ```scad
  $fn = 60; // Smooth curve resolution
  unit_scale = 1000; // mm

  plot_width = 30 * unit_scale;
  plot_depth = 60 * unit_scale;
  floor_height = 3.2 * unit_scale;
  wall_thickness = 0.23 * unit_scale;
  ```
- Use modules for repeated architectural elements (`column()`, `window_opening()`, `door_frame()`, `stair_flight()`).
- Avoid zero-thickness faces in difference operations by adding epsilon (`eps = 0.01`) overlaps.
- Include 2D cross-sections via `projection(cut = true)` for architectural floor plan generation.
