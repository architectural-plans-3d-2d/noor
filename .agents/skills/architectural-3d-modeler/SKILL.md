---
name: architectural-3d-modeler
description: Core architectural 3D modeling skill. Translates 2D floor plans, spatial requirements, blueprints, and text prompts into 3D architectural geometry, building elements (walls, slabs, doors, windows, stairs, roofs), and IFC/glTF/OBJ models.
---

# Architectural 3D Modeling Skill

## Overview
This skill provides comprehensive rules, standards, and procedures for building dimensionally accurate, aesthetically refined 3D architectural models.

## Architectural Conventions & Standards
1. **Coordinate System & Units:**
   - Standard unit: Meters (or millimeters for interior millwork).
   - Origin `(0, 0, 0)`: Ground floor center or southwest building corner at Finished Floor Level (FFL = 0.00).
   - `+Y`: Elevation / Height (in Three.js) or `+Z`: Elevation (in Blender/CAD/IFC). Ensure axis transformation when exporting.
   - `+X` / `+Z` (or `+X` / `+Y`): Horizontal ground plane.

2. **Standard Architectural Dimensions:**
   - **Ceiling Heights:** Residential standard: 2.8m - 3.2m (9.5ft - 10.5ft). Commercial: 3.5m - 4.5m.
   - **Exterior Walls:** 200mm - 300mm (8" - 12") thickness including insulation and plaster.
   - **Interior Partition Walls:** 100mm - 150mm (4" - 6").
   - **Doors:**
     - Single leaf: 900mm width x 2100mm height (3'-0" x 7'-0").
     - Double leaf: 1800mm x 2100mm.
     - Bathroom/Storage: 750mm - 800mm x 2100mm.
   - **Windows:**
     - Sill height: 900mm (residential living/bedrooms), 1100mm (kitchen counters).
     - Head height: 2100mm (aligned with door headers).
     - Full-height glazing / sliding doors: 0mm sill, 2400mm+ head height.
   - **Stairs:**
     - Riser: 150mm - 180mm (6" - 7").
     - Tread / Going: 280mm - 300mm (11" - 12").
     - Width: 1000mm - 1200mm minimum.

3. **Layer / Element Hierarchy:**
   - `site`: Ground plane, terrain, landscaping, curbs, roadways.
   - `substructure`: Foundation, footings, grade beams.
   - `structure`: Columns, load-bearing walls, structural slabs, beams.
   - `enclosure`: Exterior facade walls, curtain walls, storefronts, roofing.
   - `interior`: Partition walls, doors, stairs, ceilings, millwork.
   - `ff_e`: Furniture, fixtures, lighting, sanitaryware.
   - `lighting`: Key sun light, ambient fill, internal downlights, accent lights.

## Modeling Workflow
1. **Deconstruct 2D Layout:** Extract room boundaries, wall centerlines, door/window openings, and circulation paths.
2. **Extrude Ground Slab & Structural Grid:** Establish baseline grid lines (e.g. C01 to C16) and structural columns.
3. **Build Walls & Openings:** Create solid wall segments with boolean or cut-out openings for fenestration.
4. **Insert Fenestration (Doors & Windows):** Add frame profiles, glazing sheets (with slight glass refraction/transmission), and hardware.
5. **Add Finishes & Trim:** Baseboards, window surrounds, roof parapets, and coping stones.
6. **Assign PBR Materials:**
   - Concrete / Plaster: Base color, roughness (0.7-0.9), subtle normal bump.
   - Glass: Transmission (0.95), roughness (0.05), IOR (1.52), subtle sky reflection.
   - Wood / Timber: Warm albedo, directional grain roughness (0.4-0.6).
   - Metals: Metallic (1.0), roughness (0.2-0.4) for anodized aluminum / bronze.
