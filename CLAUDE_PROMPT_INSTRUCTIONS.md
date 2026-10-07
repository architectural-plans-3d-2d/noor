# ARCHITECTURAL DESIGN BRIEF & INSTRUCTION PROMPT FOR CLAUDE
## Project: DAATA HAMLET RESIDENCE (Luxury 3-Storey Contemporary Villa)
## Location / Context: Residential Custom Architecture (Pakistan)

---

### PROMPT TO COPY-PASTE TO CLAUDE:

```markdown
You are an expert residential architect and computational CAD engineer specializing in contemporary luxury homes in Pakistan. 
Your task is to design/refine the architectural floor plans, 3D model, and construction drawings for the **Daata Hamlet Residence**, an irregular plot contemporary villa.

Below are the exact survey coordinates, structural grid, zoning constraints, and spatial room program established for this project. Adhere strictly to these parameters without deviation.

---

### 1. SITE SURVEY & PLOT BOUNDARY DATA

- **Total Plot Area:** 3,129.1 sq.ft (approx. 12.8 Marla / 290.7 sq.m)
- **Frontage:** 87'-11" along the South Public Access Road (P0 to P1)
- **East Boundary Depth:** 62'-2" (P7 to P0)
- **Finished Floor Level (FFL):** Baseline Ground Floor = +0.00m (+1'-6" above road level)
- **Clear Floor Height:** 11'-0" floor-to-floor (10'-6" clear ceiling)

#### Exact Survey Peg Coordinates (in Feet, origin at South-West P1):
| Peg | X (ft) | Y (ft) | Boundary Segment | Segment Length | Description |
|:---:|:---:|:---:|:---:|:---:|:---|
| **P1** | 0.0000 | 0.0000 | P1 → P2 | 14'-6" (14.50') | South-West front corner (origin) |
| **P2** | 10.4884 | 10.0122 | P2 → P3 | 21'-5" (21.43') | West angled boundary peg |
| **P3** | 24.5949 | 26.1267 | P3 → P4 | 19'-9" (19.78') | West boundary transition peg |
| **P4** | 41.1897 | 36.8354 | P4 → P5 | 29'-11" (29.89') | North-West boundary corner peg |
| **P5** | 67.6992 | 50.7010 | P5 → P6 | 18'-6" (18.52') | Northern boundary intermediate peg |
| **P6** | 84.8373 | 57.6678 | P6 → P7 | 6'-0" (6.00') | North-East transition peg |
| **P7** | 88.8145 | 62.1602 | P7 → P0 | 62'-2" (62.16') | North-East apex corner |
| **P0** | 87.9167 | 0.0000 | P0 → P1 | 87'-11" (87.92') | South-East front road corner |

---

### 2. STRICT ZONING, SETBACKS & PLANNING CONSTRAINTS

1. **Line B Strict Lawn Demarcation (X = 36.125 ft):**
   - **ZERO building footprint or structure is permitted west of Line B (X < 36.125 ft).**
   - The entire front-west triangle ($588.9\text{ sq.ft}$) is strictly reserved for the **Main Lawn** (open-sky landscaped garden).
2. **Buildable Footprint Envelope:**
   - Frontage: $49\text{'-}0\text{"}$ clear ($X \in [36.125, 85.125]$).
   - South setback: $3\text{'-}0\text{"}$ from road for facade alignment.
3. **East Perimeter Passage:**
   - A continuous service passage of **$2\text{'-}9\frac{1}{2}\text{"}$ clear width** ($X \in [85.125, 87.917]$) along the entire East boundary for drainage, natural ventilation, and MEP maintenance.
4. **Natural Ventilation Standards (Pakistani Residential Norms):**
   - Every bathroom, powder room, and kitchen must have direct natural exterior ventilation. Trapped fumes or internal unvented shafts are strictly prohibited.

---

### 3. STRUCTURAL COLUMN GRID SYSTEM

The residence is structured on a rigorous orthogonal RCC column grid:
- **X-Grid Lines (East-West):**
  - Grid A: $X = 18.00\text{ ft}$ (Lawn center reference)
  - Grid B: $X = 36.50\text{ ft}$ (West building line)
  - Grid C: $X = 51.75\text{ ft}$ (Bed-2 / Dressing demising line)
  - Grid C': $X = 57.00\text{ ft}$ (Dressing / Car Porch line)
  - Grid D: $X = 69.00\text{ ft}$ (Car Porch / Drawing Room demising line)
  - Grid E: $X = 84.75\text{ ft}$ (East structural wall line)
- **Y-Grid Lines (North-South):**
  - Grid 1: $Y = 3.38\text{ ft}$ (Front structural wall)
  - Grid 2: $Y = 20.13\text{ ft}$ (Back of Car Porch / Bed 2 wall)
  - Grid 3: $Y = 28.50\text{ ft}$ (Stairs / Drawing bath boundary)
  - Grid 4: $Y = 36.50\text{ ft}$ (Kitchen north wall / Bed-1)
  - Grid 5: $Y = 42.13\text{ ft}$ (Lounge / Bed-1 north boundary)
  - Grid 6: $Y = 48.00\text{ ft}$ (Rear suite intermediate line)
  - Grid 7: $Y = 55.50\text{ ft}$ (Rear structural line)
- **Columns:** 22 continuous RCC columns ($9\text{"} \times 18\text{"}$ and $12\text{"} \times 18\text{"}$) continuous from Ground Floor to Roof.

---

### 4. GROUND FLOOR ARCHITECTURAL PROGRAM & LAYOUT

Design the Ground Floor plan matching the following spatial organization:

#### A. West Wing (Bay B to C):
1. **Bed Room-2 (Front South-West):**
   - Dimensions: $14\text{'-}6\text{"} \times 16\text{'-}0\text{"}$ ($X \in [36.5, 51.0], Y \in [3.75, 19.75]$).
   - Features: South window to front; bed on West wall; 8'-0" sliding glass door opening directly onto the Main Lawn; private door to en-suite Dress for Bed 2.
2. **Passage Way 4 Feet Wide:**
   - Dimensions: $14\text{'-}6\text{"} \times 4\text{'-}0\text{"}$ ($Y \in [20.5, 24.5]$).
   - Connects Bed Room-2, Lounge, and Kitchen without cutting through bedrooms.
3. **Main Kitchen:**
   - Dimensions: $14\text{'-}6\text{"} \times 11\text{'-}7\text{"}$ ($Y \in [24.5, 36.84]$).
   - Closed horizontally on the North at survey peg P4 ($Y = 36.84\text{ ft}$).
   - West window facing side yard; central prep island; direct access from 4-ft passage.
4. **Dirty Kitchen (Wet Preparation / Scullery):**
   - Dimensions: $8\text{'-}7\text{"} \times 4\text{'-}6\text{"}$ triangular pantry ($19.2\text{ sq.ft}$).
   - Extends north from horizontal line at P4 up to Grid Line C along the boundary. Direct access from Main Kitchen.

#### B. Central Dividing Strip (Bay C to C'):
1. **Bath for Bed 2 (South half):**
   - Dimensions: $4\text{'-}6\text{"} \times 7\text{'-}9\text{"}$ ($Y \in [3.75, 11.5]$).
   - High-level privacy ventilator venting to front facade.
2. **Dress for Bed 2 (North half):**
   - Dimensions: $4\text{'-}6\text{"} \times 7\text{'-}6\text{"}$ ($Y \in [12.25, 19.75]$).
   - En-suite walk-in wardrobe for Bed Room-2.

#### C. Arrival & Staircase Zone (Bay C' to D):
1. **Car Porch / Veranda:**
   - Dimensions: $11\text{'-}3\text{"} \times 20\text{'-}6\text{"}$ ($X \in [57.0, 68.625], Y \in [0.0, 20.5]$).
   - Accommodates executive SUV; features a wide **6'-0" main entrance double door** into the Foyer.
2. **Compact Dog-Leg Staircase:**
   - Total Core Width: Compacted to **$6\text{'-}0\text{"}$** ($X \in [62.625, 68.625]$), ensuring an **$11\text{'-}3\text{"}$ wide clear walkway** into the Lounge.
   - **Mid-Landing:** $6\text{'-}0\text{"} \times 4\text{'-}0\text{"}$ at elevation **$+7\text{'-}0\text{"}$** ($Y \in [20.5, 24.5]$).
   - **Flight 1 (West Flight, 3'-0" wide):** 11 risers @ $7.64\text{"}$ ascending South from Lounge ($Y = 33.0$) to Mid-Landing ($Y = 24.5$) at $+7\text{'-}0\text{"}$. Steps 1-5 solid, break line at step 5, steps 6-10 dashed overhead.
   - **Flight 2 (East Flight, 3'-0" wide):** 5 risers @ $7.64\text{"}$ ("3 feet or so") ascending North from Mid-Landing ($Y = 24.5$) to First Floor level at $+10\text{'-}6\text{"}$ / $+11\text{'-}0\text{"}$.
3. **Powder Room for Lounge (Integrated Under Stairs):**
   - Dimensions: $6\text{'-}0\text{"} \times 4\text{'-}0\text{"}$ situated directly beneath the Mid-Landing.
   - **Ceiling:** Topped at $+7\text{'-}0\text{"}$ clear ceiling height by the mid-landing slab.
   - **Door Access:** Door (`D-POWDER`) on West wall ($X = 62.625, Y \in [21.0, 24.0]$) opens directly into the **Entrance Foyer** (zero stair step interference).
   - **Ventilation:** Exterior ventilator (`V-POWDER`) on South wall ($Y = 20.875$) vents directly into the open-air Car Porch.
   - **Fixtures:** Fitted with WC commode and vanity wash basin.

#### D. Formal & Master Suite Wing (Bay D to E):
1. **Formal Drawing Room (Front South-East):**
   - Dimensions: $15\text{'-}0\text{"} \times 16\text{'-}0\text{"}$ ($X \in [69.375, 84.75], Y \in [3.75, 19.75]$).
   - South and East windows; private entrance from Car Porch; private door to attached bath.
2. **Dress for Drawing:**
   - Dimensions: $7\text{'-}1\frac{1}{2}\text{"} \times 7\text{'-}0\text{"}$ ($Y \in [20.5, 27.5]$).
3. **Bath for Drawing:**
   - Dimensions: $7\text{'-}1\frac{1}{2}\text{"} \times 7\text{'-}0\text{"}$ ($Y \in [20.5, 27.5]$).
   - Ventilator on East wall venting directly into the East perimeter passage.
4. **Bed-1 (Ground Floor Guest / Junior Suite):**
   - Dimensions: $15\text{'-}0\text{"} \times 14\text{'-}3\text{"}$ ($Y \in [28.25, 42.5]$).
   - Entered off the Lounge; morning window on East passage.
5. **Dressing for Bed-1:**
   - Dimensions: $7\text{'-}1\frac{1}{2}\text{"} \times 8\text{'-}0\frac{1}{2}\text{"}$ (avg 12'-0").
6. **Washroom for Bed-1:**
   - Dimensions: $7\text{'-}1\frac{1}{2}\text{"} \times 11\text{'-}3\text{"}$ (avg 13'-0") in the corner of survey pegs P5 and P6 with window and vent to East passage.

#### E. Central Living & Daylighting:
1. **Family TV Lounge:**
   - Dimensions: $16\text{'-}6\text{"} \times 23\text{'-}6\text{"}$ ($387.8\text{ sq.ft}$).
   - Expansive living and dining core with generous circulation.
2. **Open Area for Lighting (OTS):**
   - Trapezoidal light well along boundary P4–P5 north of Lounge ($45.0\text{ sq.ft}$) bringing natural daylight into Lounge and Kitchen.

---

### 5. UPPER FLOORS PROGRAM

- **First Floor:**
  - Front Sun Terrace above Car Porch.
  - Bed Room-4 (SW, above Bed-2) with attached Bath & Dress.
  - Bed Room-3 (SE, above Drawing Room) with attached Bath & Dress.
  - Bed Room-5 (Mid East, above Bed-1) with Master Bath & Dress.
  - Upper Family Lounge overlooking OTS light court.
  - Rear Utility Balcony matching the footprint of the Dirty Kitchen below.
- **Second Floor:**
  - Front Sun Terrace ($X \in [36.5, 69.0]$).
  - Bed Room-6 (West) and Bed Room-7 (East).
  - Rear Sun Terrace ($Y > 36.5$).
- **Roof & Mumty:**
  - Stair mumty enclosure; overhead water storage tank slab at $+42\text{'-}0\text{"}$.

---

### 6. DELIVERABLE EXPECTATIONS

Please output:
1. Complete dimensioned architectural floor plan for the Ground Floor.
2. Room-by-room area schedule table (Net sq.ft and dimensions).
3. Verification that all doors, swings, and furniture do not obstruct any circulation paths.
4. Confirmation that all plumbing fixtures (WCs, baths, kitchens) have direct exterior ventilation.
```

---

### Accompanying Graphic & CAD Deliverables

The clean plot drawings corresponding to this brief have been generated and synced:
- **High-Resolution Site Survey Image:** [`clean_plot_site_survey.png`](file:///C:/Users/adees/Documents/antigravity/magical-hubble/blueprints/daata_hamlet/clean_plot_site_survey.png)
- **Vector Architectural SVG Blueprint:** [`clean_plot_site_survey.svg`](file:///C:/Users/adees/Documents/antigravity/magical-hubble/blueprints/daata_hamlet/clean_plot_site_survey.svg)
- **AutoCAD DXF Drawing:** [`clean_plot_site_survey.dxf`](file:///C:/Users/adees/Documents/antigravity/magical-hubble/blueprints/daata_hamlet/clean_plot_site_survey.dxf)
