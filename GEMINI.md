# Architectural & 3D Visualization Rules

- When the user provides architectural briefs, floor plans, dimensions, or 3D requests:
  1. Parse all dimensions, grid spacing, wall thicknesses, and room programs.
  2. Maintain structural alignment (columns, load-bearing walls, vertical service cores).
  3. Output clean, interactive 3D WebGL visualizations using Three.js or photorealistic render setups using the Blender 5.1 Cycles pipeline.
  4. Use the skills configured in `.agents/skills/`:
     - `architectural-3d-modeler`
     - `transformable-furniture-modeler`
     - `threejs-viewer-and-rendering`
     - `blender-archviz-automation`
     - `comfyui-archviz-controlnet`
     - `openscad-parametric-cad`
