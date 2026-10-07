---
name: transformable-furniture-modeler
description: Specialized 3D modeling and photorealistic rendering skill for transformable, multipurpose, and kinematic furniture (box stools, folding desks, Murphy beds, modular storage, convertible joinery).
---

# Transformable Furniture & Kinematic Joinery Skill

## 1. Architectural & Ergonomic Standards
When modeling transformable and modular furniture (such as dual box stools converting into storage cabinets and fold-out study desks/display ledges):

1. **Ergonomic Baseline Dimensions:**
   - **Stool / Bench Seat Height:** 450mm (1'-6"). Standard human ergonomic sitting height.
   - **Seat Depth & Width:** 450mm x 450mm (1'-6" x 1'-6") per modular box.
   - **Combined Bench Width:** 900mm (3'-0") for two adjacent units.
   - **Stacked Vertical Cabinet Height:** 900mm (3'-0") FFL to top surface.
   - **Study Desk / Writing Surface Height:** 720mm – 750mm (approx. 2'-5" to 2'-6") above floor level.
   - **Fold-Out Desk / Ledge Depth:** 300mm – 380mm (1'-0" to 1'-3") cantilevered depth; 450mm (1'-6") width.
   - **Cutout Handle / Handhole:** 120mm – 140mm wide x 35mm – 40mm high with 15mm – 20mm rounded end radiuses, centered horizontally on upper third of panel.

2. **Panel Thickness & Joinery Standards:**
   - **Primary Material:** 18mm (3/4") or 19mm Premium Baltic Birch Plywood (13-ply void-free cross-lamination) or solid hardwood.
   - **Joinery Types:** Box/finger joints (comb joints), rebated lap joints, or hidden dowel/biscuit joinery.
   - **Clearance & Gap Allowance:** Provide 2mm – 3mm expansion and swing clearance along all hinged edges to prevent binding during 180° rotation.

3. **Hardware & Kinematic Elements:**
   - **Continuous Piano Hinge:** Full-length stainless steel or brass continuous hinge (32mm open leaf width, 1.2mm thickness) across the 180° rotation seam.
   - **Folding Stay / Locking Bracket:** Triangulated steel folding lid-stay with positive sliding lock or spring-loaded detent to safely support dynamic cantilevered loads (minimum 25kg rating for writing desks).
   - **Fasteners:** Countersunk M4 stainless/brass wood screws flush with hinge leaves.

---

## 2. 3D Model Construction Standards
1. **Solid Manifold Panels:** Never use zero-thickness planes. Every wood sheet must have its true 18mm thickness modeled with top, bottom, and end-grain sides.
2. **Micro-Bevels for Specular Highlights:** Apply 1.0mm – 1.5mm edge fillets / bevel modifiers on all wood corners. Without bevels, CG furniture looks fake and razor-sharp; with bevels, it catches realistic specular rim highlights.
3. **Explicit Hardware Geometry:** Model the physical piano hinge barrel, individual knuckles, pin, leaves, and screws. Model the folding stay bracket arms and central rivet pin.
4. **Kinematic Hierarchy & Pivots:** Group the 3D model into logical kinematic parts with local pivot origins placed exactly on hinge centerline axes:
   - `Base_Stool_Box` (Stationary origin at 0,0,0)
   - `Hinged_Upper_Box` (Pivot origin on rear piano hinge axis, rotation $\theta = 0^\circ \to 180^\circ$)
   - `FoldOut_Desk_Flap` (Pivot origin on desk hinge axis, rotation $\phi = 0^\circ \to 90^\circ$)
   - `Folding_Stay_Arm_Upper` & `Folding_Stay_Arm_Lower` (Linked kinematic constraint)

---

## 3. PBR Materials & Shading Specifications
- **Baltic Birch Plywood (Faces):**
  - Base Color: Warm natural blonde pine/birch ($R=0.82, G=0.70, B=0.55$)
  - Roughness: 0.38 – 0.48 (satin architectural clear lacquer)
  - Subtle normal map / bump: 0.05 strength fine wood grain
- **Plywood Exposed Edges (End Grain):**
  - Alternating dark and light laminated ply stripes (0.75 strength contrast).
- **Metal Hardware (Piano Hinges & Folding Stays):**
  - Base Color: $0.85, 0.85, 0.88$ (Brushed Stainless Steel) or $0.95, 0.78, 0.42$ (Satin Architectural Brass)
  - Metallic: 0.95 – 1.00
  - Roughness: 0.22 – 0.28 (anisotropic brushed sheen)

---

## 4. Photorealistic Cycles Rendering Standards
1. **Lighting Rig (Studio Catalog Softbox):**
   - Key Light: Large softbox area light ($1.5\text{m} \times 1.2\text{m}$) at 45° azimuth, 55° elevation (Color 5000K, soft shadow falloff).
   - Fill Light: Large subtle area light ($2.0\text{m} \times 1.5\text{m}$) opposite side (Color 5600K, 30% key intensity).
   - Rim / Hair Light: Small intense overhead strip light behind object to separate wood contours from background.
2. **Floor / Background:**
   - Seamless studio cyclorama backdrop (curved infinity cove) or warm modern architectural interior room with hardwood/concrete floor and contact shadow catchers.
3. **Multi-State Presentation Views:**
   - **View 1 (Hero 3-in-1 Lineup):** All three states rendered side-by-side in one frame (State 1: Stools -> State 2: Cabinet -> State 3: Study Desk/Display).
   - **View 2 (State Detail Focus):** Close-up 3/4 isometric perspective of active mode with realistic props (laptop, notebook, plant, ceramic cup).
   - **View 3 (Joinery Macro):** Macro close-up (85mm lens, shallow depth of field) focusing on the continuous piano hinge and finger joints.
