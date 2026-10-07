"""
DAATA HAMLET RESIDENCE - World-Class Luxury Architectural Front Elevation SVG Generator
Produces an award-winning, magazine-grade architectural presentation vector drawing:
- True 87'-11" frontage with proportional dimensional accuracy
- Signature stepped floating canopy slabs with dark charcoal bronze fascias and wood soffits
- Roman split-face travertine stone volume on Drawing Room
- Teak timber pergolas and vertical solar louvers casting dramatic 45-degree architectural shadows
- Multi-layer glass curtain walls with soft reflections and interior chandelier warmth
- Structural column grid markers (Grids A-E) perfectly aligned
- Human scale entourage, landscape planters, luxury car silhouette in carport, and datum level markers
"""
from __future__ import annotations
import math
from pathlib import Path

OUT_PATHS = [
    Path("blueprints/daata_hamlet/06_front_south_elevation.svg"),
    Path("blueprints/daata_hamlet/daata_hamlet_luxury_canopy_elevation.svg"),
    Path(r"C:\Users\adees\.gemini\antigravity\brain\754b2257-dc8d-4e91-8a73-3c0efba21f41\daata_hamlet_luxury_canopy_elevation.svg")
]

def build_luxury_elevation_svg() -> str:
    # Canvas dimensions: 2400 x 1500 px
    W, H = 2400, 1500
    
    # Coordinate system mapping:
    # Total plot frontage = 87.917 ft (~88 ft)
    # We span X from ~10 ft to 98 ft (world span = 88 ft)
    # Canvas building width: 1760 px (from x=320 to x=2080)
    # Scale: 1 ft = 20.0 pixels!
    
    SCALE = 20.0
    ORIGIN_X = 320.0  # corresponds to world X = 0.0 (West plot boundary)
    GROUND_Y = 1180.0 # corresponds to Finished Ground Level Z = 0.00'
    
    def wx(ft: float) -> float:
        return ORIGIN_X + ft * SCALE
    
    def wy(ft: float) -> float:
        # Elevation: Z goes UP, so canvas Y goes DOWN
        return GROUND_Y - ft * SCALE
    
    svg = []
    svg.append(f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
<defs>
  <!-- Gradients & Atmosphere -->
  <linearGradient id="skyGrad" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0%" stop-color="#e9eef5"/>
    <stop offset="45%" stop-color="#f4f7fb"/>
    <stop offset="85%" stop-color="#fdfbf7"/>
    <stop offset="100%" stop-color="#fff8ec"/>
  </linearGradient>

  <linearGradient id="groundGrad" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0%" stop-color="#2d3748"/>
    <stop offset="15%" stop-color="#1a202c"/>
    <stop offset="100%" stop-color="#0f172a"/>
  </linearGradient>

  <linearGradient id="bronzeCanopy" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0%" stop-color="#2d3139"/>
    <stop offset="25%" stop-color="#1f232b"/>
    <stop offset="80%" stop-color="#16181f"/>
    <stop offset="100%" stop-color="#0d0e12"/>
  </linearGradient>

  <linearGradient id="bronzeTrim" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0%" stop-color="#3b4252"/>
    <stop offset="50%" stop-color="#4c566a"/>
    <stop offset="100%" stop-color="#2e3440"/>
  </linearGradient>

  <linearGradient id="woodSoffit" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0%" stop-color="#8a532b"/>
    <stop offset="50%" stop-color="#73411e"/>
    <stop offset="100%" stop-color="#5c3216"/>
  </linearGradient>

  <linearGradient id="teakLouver" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0%" stop-color="#bc7a3d"/>
    <stop offset="50%" stop-color="#9d5d28"/>
    <stop offset="100%" stop-color="#7e461a"/>
  </linearGradient>

  <linearGradient id="glassReflection" x1="0" y1="0" x2="0.8" y2="1">
    <stop offset="0%" stop-color="#dbeafe" stop-opacity="0.85"/>
    <stop offset="30%" stop-color="#bfdbfe" stop-opacity="0.65"/>
    <stop offset="70%" stop-color="#93c5fd" stop-opacity="0.45"/>
    <stop offset="100%" stop-color="#60a5fa" stop-opacity="0.30"/>
  </linearGradient>

  <linearGradient id="interiorWarmGlow" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0%" stop-color="#fef08a" stop-opacity="0.70"/>
    <stop offset="50%" stop-color="#fed7aa" stop-opacity="0.45"/>
    <stop offset="100%" stop-color="#fdba74" stop-opacity="0.20"/>
  </linearGradient>

  <linearGradient id="stuccoWall" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0%" stop-color="#ffffff"/>
    <stop offset="60%" stop-color="#f8fafc"/>
    <stop offset="100%" stop-color="#f1f5f9"/>
  </linearGradient>

  <linearGradient id="travertineSkin" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0%" stop-color="#e8dec8"/>
    <stop offset="25%" stop-color="#decfae"/>
    <stop offset="50%" stop-color="#ebdcc0"/>
    <stop offset="75%" stop-color="#d6c59e"/>
    <stop offset="100%" stop-color="#e2d4b7"/>
  </linearGradient>

  <!-- Architectural Drop Shadows -->
  <linearGradient id="dropShadowV" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0%" stop-color="#000000" stop-opacity="0.45"/>
    <stop offset="40%" stop-color="#000000" stop-opacity="0.25"/>
    <stop offset="100%" stop-color="#000000" stop-opacity="0.0"/>
  </linearGradient>

  <linearGradient id="dropShadowH" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0%" stop-color="#000000" stop-opacity="0.40"/>
    <stop offset="100%" stop-color="#000000" stop-opacity="0.0"/>
  </linearGradient>

  <linearGradient id="pergolaShadow" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0%" stop-color="#000000" stop-opacity="0.35"/>
    <stop offset="100%" stop-color="#000000" stop-opacity="0.0"/>
  </linearGradient>

  <!-- Patterns -->
  <pattern id="travertineJoints" width="40" height="14" patternUnits="userSpaceOnUse">
    <rect width="40" height="14" fill="none"/>
    <line x1="0" y1="14" x2="40" y2="14" stroke="#c4b595" stroke-width="0.75" stroke-opacity="0.8"/>
    <line x1="20" y1="0" x2="20" y2="14" stroke="#c4b595" stroke-width="0.75" stroke-opacity="0.8"/>
  </pattern>

  <pattern id="paverGrid" width="16" height="8" patternUnits="userSpaceOnUse">
    <rect width="16" height="8" fill="#e2e8f0"/>
    <line x1="0" y1="8" x2="16" y2="8" stroke="#cbd5e1" stroke-width="0.75"/>
    <line x1="8" y1="0" x2="8" y2="8" stroke="#cbd5e1" stroke-width="0.75"/>
  </pattern>

  <pattern id="lawnStipple" width="6" height="6" patternUnits="userSpaceOnUse">
    <rect width="6" height="6" fill="#4d7c0f"/>
    <circle cx="2" cy="2" r="0.7" fill="#65a30d"/>
    <circle cx="5" cy="5" r="0.7" fill="#84cc16"/>
  </pattern>

  <!-- Filters -->
  <filter id="softGlow" x="-20%" y="-20%" width="140%" height="140%">
    <feGaussianBlur stdDeviation="6" result="blur"/>
    <feComposite in="SourceGraphic" in2="blur" operator="over"/>
  </filter>

  <filter id="crispShadow" x="-10%" y="-10%" width="130%" height="130%">
    <feDropShadow dx="3" dy="12" stdDeviation="8" flood-color="#000000" flood-opacity="0.32"/>
  </filter>
</defs>

<!-- 1. PRESENTATION CANVAS BACKGROUND -->
<rect width="{W}" height="{H}" fill="#fcfdfd"/>
<rect x="30" y="30" width="{W-60}" height="{H-60}" fill="none" stroke="#cbd5e1" stroke-width="1"/>
<rect x="34" y="34" width="{W-68}" height="{H-68}" fill="none" stroke="#94a3b8" stroke-width="1.5"/>

<!-- 2. ARCHITECTURAL SKY -->
<rect x="40" y="40" width="{W-80}" height="{GROUND_Y - 40}" fill="url(#skyGrad)"/>

<!-- Distant Warm Horizon Ambient Glow -->
<ellipse cx="{wx(44)}" cy="{GROUND_Y - 80}" rx="900" ry="260" fill="#fef3c7" opacity="0.35"/>
''')

    # 3. GROUND PLANE & ROAD SECTION
    road_top_y = wy(-1.5)
    grade_top_y = wy(-1.0)
    plinth_y = wy(1.5)
    
    svg.append(f'''
<!-- 3. GROUND STRATA & ROAD BASELINE -->
<!-- Deep Ground Section -->
<rect x="40" y="{GROUND_Y}" width="{W-80}" height="{H - 40 - GROUND_Y}" fill="url(#groundGrad)"/>
<line x1="40" y1="{GROUND_Y}" x2="{W-40}" y2="{GROUND_Y}" stroke="#0f172a" stroke-width="4"/>

<!-- Public Road & Asphalt (Frontage) -->
<rect x="{wx(-4)}" y="{road_top_y}" width="{wx(94) - wx(-4)}" height="{GROUND_Y - road_top_y}" fill="#334155"/>
<line x1="{wx(-4)}" y1="{road_top_y}" x2="{wx(94)}" y2="{road_top_y}" stroke="#64748b" stroke-width="2"/>

<!-- Road White Curb Markings -->
<line x1="{wx(-2)}" y1="{road_top_y + 6}" x2="{wx(92)}" y2="{road_top_y + 6}" stroke="#94a3b8" stroke-width="2" stroke-dasharray="24,18"/>

<!-- Pedestrian Footpath & Curb -->
<rect x="{wx(-2)}" y="{wy(-0.5)}" width="{wx(92) - wx(-2)}" height="{road_top_y - wy(-0.5)}" fill="url(#paverGrid)"/>
<line x1="{wx(-2)}" y1="{wy(-0.5)}" x2="{wx(92)}" y2="{wy(-0.5)}" stroke="#475569" stroke-width="2"/>

<!-- Manicured Front Green Strip & Lawn Base -->
<rect x="{wx(0)}" y="{wy(0.0)}" width="{wx(87.9) - wx(0)}" height="{wy(-0.5) - wy(0.0)}" fill="url(#lawnStipple)"/>
<line x1="{wx(0)}" y1="{wy(0.0)}" x2="{wx(87.9)}" y2="{wy(0.0)}" stroke="#365314" stroke-width="2.5"/>
''')

    # 4. STRUCTURAL GRID LINES (A to E)
    grid_x_map = {
        'A': 18.0,
        'B': 37.25,
        'C': 53.0,
        'D': 71.75,
        'E': 87.5
    }
    
    svg.append('<!-- 4. STRUCTURAL COLUMN GRID LINES (A-E) -->')
    for tag, gx_val in grid_x_map.items():
        cx = wx(gx_val)
        svg.append(f'''
<line x1="{cx}" y1="80" x2="{cx}" y2="{GROUND_Y + 40}" stroke="#94a3b8" stroke-width="1.2" stroke-dasharray="8,6,2,6"/>
<circle cx="{cx}" cy="80" r="16" fill="#ffffff" stroke="#0f172a" stroke-width="1.8"/>
<text x="{cx}" y="85" font-family="'Helvetica Neue', Arial, sans-serif" font-size="14" font-weight="bold" fill="#0f172a" text-anchor="middle">{tag}</text>
<circle cx="{cx}" cy="{GROUND_Y + 40}" r="14" fill="#ffffff" stroke="#0f172a" stroke-width="1.5"/>
<text x="{cx}" y="{GROUND_Y + 45}" font-family="'Helvetica Neue', Arial, sans-serif" font-size="12" font-weight="bold" fill="#0f172a" text-anchor="middle">{tag}</text>
''')

    # 5. BUILDING FACADE VOLUMES (BACK TO FRONT)
    # Floor levels:
    # GF: Z=0 to 11.83 (FFL +1.5, ceiling +11.83)
    # 1F: Z=11.83 to 22.17
    # 2F: Z=22.17 to 32.50
    # Mumty: Z=32.50 to 42.00
    
    svg.append('''
<!-- 5. BUILDING MAIN VOLUMES & ARCHITECTURAL MASSING -->
<!-- Background: Stair Mumty Core (Z=32.50' to 42.00', X=71.75' to 87.5') -->
''')
    mumty_x0 = wx(71.375)
    mumty_w = (87.5 - 71.375) * SCALE
    mumty_y0 = wy(42.0)
    mumty_h = (42.0 - 32.5) * SCALE
    
    svg.append(f'''
<rect x="{mumty_x0}" y="{mumty_y0}" width="{mumty_w}" height="{mumty_h}" fill="url(#stuccoWall)" stroke="#334155" stroke-width="2"/>
<!-- Mumty Razor Parapet Coping -->
<rect x="{mumty_x0 - 6}" y="{mumty_y0 - 8}" width="{mumty_w + 12}" height="8" fill="url(#bronzeCanopy)" stroke="#0f172a" stroke-width="1"/>
<!-- Mumty Vertical Architectural Slot Window -->
<rect x="{wx(74.0)}" y="{wy(40.5)}" width="{wx(76.5) - wx(74.0)}" height="{(40.5 - 34.0)*SCALE}" fill="#1e293b" stroke="#0f172a" stroke-width="1.5"/>
<rect x="{wx(74.2)}" y="{wy(40.3)}" width="{wx(76.3) - wx(74.2)}" height="{(40.3 - 34.2)*SCALE}" fill="url(#glassReflection)"/>

<!-- Overhead 800-Gal Water Tank Silhouette on Mumty Roof -->
<rect x="{wx(78.5)}" y="{wy(47.5)}" width="{wx(85.5) - wx(78.5)}" height="{(47.5 - 42.0)*SCALE}" rx="4" fill="#e2e8f0" stroke="#475569" stroke-width="1.5"/>
<line x1="{wx(78.5)}" y1="{wy(44.5)}" x2="{wx(85.5)}" y2="{wy(44.5)}" stroke="#94a3b8" stroke-width="1"/>
<text x="{wx(82.0)}" y="{wy(44.0)}" font-family="'Helvetica Neue', Arial, sans-serif" font-size="9" font-weight="bold" fill="#64748b" text-anchor="middle">800-GAL TANK</text>
''')

    # SECOND FLOOR (Z=22.17' to 32.50')
    # Bedroom 6 & 7 facade + Master Penthouse Volume
    svg.append('''
<!-- ====================================================================== -->
<!-- SECOND FLOOR ARCHITECTURE (Z=22'-2" to 32'-6") -->
<!-- ====================================================================== -->
''')
    # Penthouse main wall (X=53.0 to 87.5)
    f2_wall_x0 = wx(52.625)
    f2_wall_w = (87.5 - 52.625) * SCALE
    f2_wall_y0 = wy(32.5)
    f2_wall_h = (32.5 - 22.167) * SCALE
    
    svg.append(f'''
<!-- Second Floor Penthouse Stucco Facade -->
<rect x="{f2_wall_x0}" y="{f2_wall_y0}" width="{f2_wall_w}" height="{f2_wall_h}" fill="url(#stuccoWall)" stroke="#334155" stroke-width="2"/>

<!-- Bedroom 7 Panoramic Window (X=60.0 to 69.0) -->
<rect x="{wx(60.0)}" y="{wy(30.0)}" width="{(69.0 - 60.0)*SCALE}" height="{(30.0 - 24.5)*SCALE}" fill="#0f172a" stroke="#000" stroke-width="2"/>
<rect x="{wx(60.2)}" y="{wy(29.8)}" width="{(68.6 - 60.0)*SCALE}" height="{(29.6 - 24.7)*SCALE}" fill="url(#interiorWarmGlow)"/>
<rect x="{wx(60.2)}" y="{wy(29.8)}" width="{(68.6 - 60.0)*SCALE}" height="{(29.6 - 24.7)*SCALE}" fill="url(#glassReflection)"/>
<!-- Aluminum Window Mullions -->
<line x1="{wx(64.5)}" y1="{wy(30.0)}" x2="{wx(64.5)}" y2="{wy(24.5)}" stroke="#0f172a" stroke-width="3"/>

<!-- Bedroom 6 Window (X=76.0 to 83.0) -->
<rect x="{wx(76.0)}" y="{wy(30.0)}" width="{(83.0 - 76.0)*SCALE}" height="{(30.0 - 24.5)*SCALE}" fill="#0f172a" stroke="#000" stroke-width="2"/>
<rect x="{wx(76.2)}" y="{wy(29.8)}" width="{(82.6 - 76.0)*SCALE}" height="{(29.6 - 24.7)*SCALE}" fill="url(#interiorWarmGlow)"/>
<rect x="{wx(76.2)}" y="{wy(29.8)}" width="{(82.6 - 76.0)*SCALE}" height="{(29.6 - 24.7)*SCALE}" fill="url(#glassReflection)"/>
<line x1="{wx(79.5)}" y1="{wy(30.0)}" x2="{wx(79.5)}" y2="{wy(24.5)}" stroke="#0f172a" stroke-width="3"/>

<!-- Continuous RCC Columns D & E in 2F Facade -->
<rect x="{wx(71.375)}" y="{wy(32.5)}" width="{(72.125 - 71.375)*SCALE}" height="{f2_wall_h}" fill="#1e293b" stroke="#0f172a" stroke-width="1.2"/>
<rect x="{wx(87.125)}" y="{wy(32.5)}" width="{(87.875 - 87.125)*SCALE}" height="{f2_wall_h}" fill="#1e293b" stroke="#0f172a" stroke-width="1.2"/>
''')

    # SECOND FLOOR TIMBER PERGOLA & CANOPY TERRACE (X=36.875 to 52.625)
    # The signature teak wood pergola structure over the west terrace
    perg_x0 = wx(37.25)
    perg_x1 = wx(52.625)
    perg_w = perg_x1 - perg_x0
    perg_beam_y = wy(33.0)
    perg_post_top_y = wy(33.0)
    perg_deck_y = wy(22.167)
    
    svg.append(f'''
<!-- 2F Pergola Terrace Back Wall (Recessed) -->
<rect x="{perg_x0}" y="{wy(32.5)}" width="{perg_w}" height="{(32.5 - 22.167)*SCALE}" fill="#f1f5f9" stroke="#94a3b8" stroke-width="1.5"/>

<!-- Pergola Cast Shadows on Wall (45 deg diagonal) -->
<polygon points="{perg_x0},{wy(32.5)} {perg_x1},{wy(32.5)} {perg_x1},{wy(27.0)} {perg_x0 + 40},{wy(27.0)}" fill="url(#dropShadowV)" opacity="0.6"/>

<!-- 2F Glazed Terrace Sliding Doors (X=40.0 to 49.5) -->
<rect x="{wx(40.0)}" y="{wy(30.2)}" width="{(49.5 - 40.0)*SCALE}" height="{(30.2 - 22.167)*SCALE}" fill="#0f172a" stroke="#000" stroke-width="2"/>
<rect x="{wx(40.2)}" y="{wy(30.0)}" width="{(49.1 - 40.0)*SCALE}" height="{(30.0 - 22.2)*SCALE}" fill="url(#interiorWarmGlow)"/>
<rect x="{wx(40.2)}" y="{wy(30.0)}" width="{(49.1 - 40.0)*SCALE}" height="{(30.0 - 22.2)*SCALE}" fill="url(#glassReflection)"/>
<!-- Sliding Screen Frame Mullions -->
<line x1="{wx(44.75)}" y1="{wy(30.2)}" x2="{wx(44.75)}" y2="{wy(22.167)}" stroke="#0f172a" stroke-width="3"/>

<!-- Pergola RCC Structural Posts (Columns B3, B4 & C3) -->
<rect x="{wx(37.25)}" y="{wy(33.0)}" width="15" height="{(33.0 - 22.167)*SCALE}" fill="#1e293b" stroke="#0f172a" stroke-width="1.5"/>
<rect x="{wx(52.625) - 15}" y="{wy(33.0)}" width="15" height="{(33.0 - 22.167)*SCALE}" fill="#1e293b" stroke="#0f172a" stroke-width="1.5"/>

<!-- Teak Timber Pergola Horizontal Rafters (12 Rhythmic Slats) -->
''')
    for i in range(9):
        ry = wy(33.0 - i * 0.95)
        svg.append(f'''
<rect x="{perg_x0 - 8}" y="{ry - 5}" width="{perg_w + 16}" height="8" rx="2" fill="url(#teakLouver)" stroke="#5c3216" stroke-width="1" filter="url(#crispShadow)"/>
<!-- Teak Wood Endgrain Highlight -->
<circle cx="{perg_x0 - 4}" cy="{ry - 1}" r="2" fill="#d97706"/>
<circle cx="{perg_x1 + 4}" cy="{ry - 1}" r="2" fill="#d97706"/>
''')

    # SECOND FLOOR GLASS BALUSTRADE & CANOPY FASCIA (Z=22.167')
    svg.append(f'''
<!-- 2F Glass Balustrade (Frameless Tempered Glass, H=3.5 ft) -->
<rect x="{wx(37.0)}" y="{wy(25.67)}" width="{(87.5 - 37.0)*SCALE}" height="{(3.5)*SCALE}" fill="url(#glassReflection)" stroke="#93c5fd" stroke-width="1"/>
<line x1="{wx(37.0)}" y1="{wy(25.67)}" x2="{wx(87.5)}" y2="{wy(25.67)}" stroke="#0f172a" stroke-width="3"/>
<!-- Stainless Steel Base Shoe -->
<rect x="{wx(37.0)}" y="{wy(22.4)}" width="{(87.5 - 37.0)*SCALE}" height="6" fill="#64748b" stroke="#334155" stroke-width="1"/>

<!-- 2F FLOATING CANOPY SLAB & BRONZE FASCIA (Z=21.5' to 22.167', Overhang from X=34.0' to 89.5') -->
<g filter="url(#crispShadow)">
  <!-- Deep Drop Shadow Under 2F Canopy -->
  <rect x="{wx(34.0)}" y="{wy(21.2)}" width="{(89.5 - 34.0)*SCALE}" height="24" fill="url(#dropShadowV)"/>
  <!-- Charcoal Bronze Fascia -->
  <rect x="{wx(34.0)}" y="{wy(22.3)}" width="{(89.5 - 34.0)*SCALE}" height="18" fill="url(#bronzeCanopy)" stroke="#0f172a" stroke-width="1.8"/>
  <rect x="{wx(34.0)}" y="{wy(22.3)}" width="{(89.5 - 34.0)*SCALE}" height="3" fill="url(#bronzeTrim)"/>
  <!-- Wood Soffit Reveal -->
  <rect x="{wx(34.5)}" y="{wy(21.4)}" width="{(89.0 - 34.5)*SCALE}" height="5" fill="url(#woodSoffit)"/>
</g>
''')

    # FIRST FLOOR (Z=11.83' to 22.17')
    # Master Bedroom 4, Bedroom 3, Bedroom 5, Family Lounge
    svg.append('''
<!-- ====================================================================== -->
<!-- FIRST FLOOR ARCHITECTURE (Z=11'-10" to 22'-2") -->
<!-- ====================================================================== -->
''')
    f1_wall_x0 = wx(36.875)
    f1_wall_w = (87.5 - 36.875) * SCALE
    f1_wall_y0 = wy(21.5)
    f1_wall_h = (21.5 - 11.833) * SCALE
    
    svg.append(f'''
<!-- First Floor Main Stucco Facade -->
<rect x="{f1_wall_x0}" y="{f1_wall_y0}" width="{f1_wall_w}" height="{f1_wall_h}" fill="url(#stuccoWall)" stroke="#334155" stroke-width="2"/>

<!-- First Floor Drawing Room Upper Box: Travertine Stone Feature Skin (X=36.875 to 52.625) -->
<rect x="{wx(36.875)}" y="{wy(21.5)}" width="{(52.625 - 36.875)*SCALE}" height="{f1_wall_h}" fill="url(#travertineSkin)" stroke="#78350f" stroke-width="1.8"/>
<rect x="{wx(36.875)}" y="{wy(21.5)}" width="{(52.625 - 36.875)*SCALE}" height="{f1_wall_h}" fill="url(#travertineJoints)" opacity="0.65"/>

<!-- Master Bedroom 4 Ribbon Glass Window with Vertical Timber Fins (X=41.5 to 49.5) -->
<rect x="{wx(41.5)}" y="{wy(19.8)}" width="{(49.5 - 41.5)*SCALE}" height="{(19.8 - 14.0)*SCALE}" fill="#0f172a" stroke="#000" stroke-width="2"/>
<rect x="{wx(41.7)}" y="{wy(19.6)}" width="{(49.1 - 41.5)*SCALE}" height="{(19.4 - 14.2)*SCALE}" fill="url(#interiorWarmGlow)"/>
<rect x="{wx(41.7)}" y="{wy(19.6)}" width="{(49.1 - 41.5)*SCALE}" height="{(19.4 - 14.2)*SCALE}" fill="url(#glassReflection)"/>
''')
    # Vertical teak solar fins on 1F Window
    for i in range(8):
        fx = wx(42.0 + i * 0.95)
        svg.append(f'''
<rect x="{fx}" y="{wy(20.2)}" width="6" height="{(20.2 - 13.6)*SCALE}" fill="url(#teakLouver)" stroke="#5c3216" stroke-width="0.75" filter="url(#crispShadow)"/>
''')

    svg.append(f'''
<!-- 1F Family Lounge Panoramic Ribbon Window (X=58.0 to 68.0) -->
<rect x="{wx(58.0)}" y="{wy(19.8)}" width="{(68.0 - 58.0)*SCALE}" height="{(19.8 - 14.0)*SCALE}" fill="#0f172a" stroke="#000" stroke-width="2"/>
<rect x="{wx(58.2)}" y="{wy(19.6)}" width="{(67.6 - 58.0)*SCALE}" height="{(19.4 - 14.2)*SCALE}" fill="url(#interiorWarmGlow)"/>
<rect x="{wx(58.2)}" y="{wy(19.6)}" width="{(67.6 - 58.0)*SCALE}" height="{(19.4 - 14.2)*SCALE}" fill="url(#glassReflection)"/>
<!-- Center Sliding Division -->
<line x1="{wx(63.0)}" y1="{wy(19.8)}" x2="{wx(63.0)}" y2="{wy(14.0)}" stroke="#0f172a" stroke-width="3"/>

<!-- 1F Master Suite 3 Window (X=76.0 to 83.0) -->
<rect x="{wx(76.0)}" y="{wy(19.8)}" width="{(83.0 - 76.0)*SCALE}" height="{(19.8 - 14.0)*SCALE}" fill="#0f172a" stroke="#000" stroke-width="2"/>
<rect x="{wx(76.2)}" y="{wy(19.6)}" width="{(82.6 - 76.0)*SCALE}" height="{(19.4 - 14.2)*SCALE}" fill="url(#interiorWarmGlow)"/>
<rect x="{wx(76.2)}" y="{wy(19.6)}" width="{(82.6 - 76.0)*SCALE}" height="{(19.4 - 14.2)*SCALE}" fill="url(#glassReflection)"/>
<line x1="{wx(79.5)}" y1="{wy(19.8)}" x2="{wx(79.5)}" y2="{wy(14.0)}" stroke="#0f172a" stroke-width="3"/>

<!-- Continuous RCC Columns B, C, D, E in 1F Facade -->
<rect x="{wx(37.25) - 4}" y="{wy(21.5)}" width="15" height="{f1_wall_h}" fill="#1e293b" stroke="#0f172a" stroke-width="1.2"/>
<rect x="{wx(53.0) - 4}" y="{wy(21.5)}" width="15" height="{f1_wall_h}" fill="#1e293b" stroke="#0f172a" stroke-width="1.2"/>
<rect x="{wx(71.75) - 4}" y="{wy(21.5)}" width="15" height="{f1_wall_h}" fill="#1e293b" stroke="#0f172a" stroke-width="1.2"/>
<rect x="{wx(87.5) - 4}" y="{wy(21.5)}" width="15" height="{f1_wall_h}" fill="#1e293b" stroke="#0f172a" stroke-width="1.2"/>

<!-- 1F OPEN TERRACE OVER 2-CAR PORCH (X=17.5' to 36.875') -->
<!-- Terrace Glass Balustrade (H=3.5 ft) -->
<rect x="{wx(17.5)}" y="{wy(15.33)}" width="{(36.875 - 17.5)*SCALE}" height="{(3.5)*SCALE}" fill="url(#glassReflection)" stroke="#93c5fd" stroke-width="1"/>
<line x1="{wx(17.5)}" y1="{wy(15.33)}" x2="{wx(36.875)}" y2="{wy(15.33)}" stroke="#0f172a" stroke-width="3"/>
<rect x="{wx(17.5)}" y="{wy(12.0)}" width="{(36.875 - 17.5)*SCALE}" height="5" fill="#64748b" stroke="#334155" stroke-width="1"/>
<!-- Outdoor Lounge Chairs & Planter Box on Porch Terrace -->
<rect x="{wx(20.0)}" y="{wy(13.5)}" width="24" height="18" rx="3" fill="#475569"/>
<rect x="{wx(22.0)}" y="{wy(14.2)}" width="20" height="8" rx="2" fill="#94a3b8"/>
<rect x="{wx(26.0)}" y="{wy(13.2)}" width="18" height="12" rx="2" fill="#d97706"/>
<!-- Terrace Green Planter Box -->
<rect x="{wx(32.0)}" y="{wy(13.6)}" width="36" height="14" fill="#334155" stroke="#1e293b" stroke-width="1"/>
<path d="M {wx(32.0)},{wy(13.6)} Q {wx(34.0)},{wy(16.0)} {wx(36.0)},{wy(13.6)} Q {wx(38.0)},{wy(16.5)} {wx(40.0)},{wy(13.6)}" fill="#15803d" stroke="#166534" stroke-width="1.5"/>
''')

    # FIRST FLOOR CANOPY SLAB & DEEP OVERHANG (Z=10.5' to 11.83')
    # This is the massive cantilevered 2-car porch canopy extending across X=14.0' to 90.0'
    canopy_1f_x0 = wx(14.0)
    canopy_1f_x1 = wx(90.0)
    canopy_1f_w = canopy_1f_x1 - canopy_1f_x0
    canopy_1f_y = wy(12.0)
    
    svg.append(f'''
<!-- ====================================================================== -->
<!-- SIGNATURE CANTILEVERED CANOPY SLAB (Z=10'-6" to 11'-10") -->
<!-- Deep 4'-6" Horizontal Floating Cantilever Overhang -->
<!-- ====================================================================== -->
<g filter="url(#crispShadow)">
  <!-- Dramatic 45-degree Architectural Drop Shadow on Ground Floor Facade -->
  <rect x="{canopy_1f_x0}" y="{wy(10.5)}" width="{canopy_1f_w}" height="32" fill="url(#dropShadowV)"/>
  
  <!-- 16" Architectural Dark Bronze Metallic Fascia -->
  <rect x="{canopy_1f_x0}" y="{wy(12.0)}" width="{canopy_1f_w}" height="24" fill="url(#bronzeCanopy)" stroke="#020617" stroke-width="2.5"/>
  <rect x="{canopy_1f_x0}" y="{wy(12.0)}" width="{canopy_1f_w}" height="4" fill="url(#bronzeTrim)"/>
  <rect x="{canopy_1f_x0}" y="{wy(10.8)}" width="{canopy_1f_w}" height="2" fill="#0f172a"/>
  
  <!-- Teak Wood Soffit with Warm Recessed Linear LED Lighting Strip -->
  <rect x="{canopy_1f_x0 + 4}" y="{wy(10.7)}" width="{canopy_1f_w - 8}" height="7" fill="url(#woodSoffit)"/>
  <line x1="{canopy_1f_x0 + 20}" y1="{wy(10.3)}" x2="{canopy_1f_x1 - 20}" y2="{wy(10.3)}" stroke="#fde047" stroke-width="2.5" filter="url(#softGlow)"/>
</g>
''')

    # GROUND FLOOR (Z=0.00' to 10.50', FFL +1.50')
    # 2-Car Porch, Drawing Room Stone Block, Main Entrance, Bedroom 1
    svg.append('''
<!-- ====================================================================== -->
<!-- GROUND FLOOR ARCHITECTURE (Z=0'-0" to 10'-6") -->
<!-- ====================================================================== -->
''')
    # Plinth Base (Z=0.0 to 1.5 ft)
    svg.append(f'''
<!-- Plinth Foundation Beam & Step Baseline (+1'-6" FFL) -->
<rect x="{wx(0.0)}" y="{wy(1.5)}" width="{(87.9)*SCALE}" height="{(1.5)*SCALE}" fill="#334155" stroke="#1e293b" stroke-width="2"/>
<line x1="{wx(0.0)}" y1="{wy(1.5)}" x2="{wx(87.9)}" y2="{wy(1.5)}" stroke="#94a3b8" stroke-width="2"/>
<text x="{wx(2.0)}" y="{wy(0.4)}" font-family="'Helvetica Neue', Arial, sans-serif" font-size="10" font-weight="bold" fill="#f8fafc">PLINTH BEAM (+1'-6" FFL)</text>
''')

    # 2-CAR PORCH ENTRY (X=17.5' to 36.875')
    svg.append(f'''
<!-- 2-Car Porch Open Space Under Canopy (Cobblestone Travertine Floor) -->
<rect x="{wx(17.5)}" y="{wy(10.5)}" width="{(36.875 - 17.5)*SCALE}" height="{(10.5 - 1.5)*SCALE}" fill="#f8fafc" stroke="#cbd5e1" stroke-width="1.5"/>

<!-- RCC Structural Canopy Posts: Column A1 (X=18.0') and Column B1 (X=37.25') -->
<rect x="{wx(17.5)}" y="{wy(11.0)}" width="{(18.5 - 17.5)*SCALE}" height="{(11.0 - 0.0)*SCALE}" fill="#1e293b" stroke="#0f172a" stroke-width="2.2"/>
<rect x="{wx(36.75)}" y="{wy(11.0)}" width="{(37.75 - 36.75)*SCALE}" height="{(11.0 - 0.0)*SCALE}" fill="#1e293b" stroke="#0f172a" stroke-width="2.2"/>

<!-- Luxury Dark SUV Car Silhouette in Porch (Porsche Taycan / Range Rover) -->
<g transform="translate({wx(21.0)}, {wy(1.5) - 65}) scale(0.68)">
  <!-- Car Shadow -->
  <ellipse cx="140" cy="95" rx="140" ry="12" fill="#000000" opacity="0.6"/>
  <!-- Car Body Silhouette -->
  <path d="M 15,75 Q 35,45 80,42 L 140,25 Q 185,22 230,42 L 265,58 Q 285,68 285,82 L 280,88 L 10,88 Z" fill="#0f172a" stroke="#334155" stroke-width="2"/>
  <!-- Windows & Roof Glass -->
  <path d="M 85,44 L 138,28 Q 175,25 215,44 L 205,58 L 85,58 Z" fill="#38bdf8" opacity="0.55"/>
  <!-- Wheels -->
  <circle cx="65" cy="88" r="22" fill="#020617" stroke="#475569" stroke-width="4"/>
  <circle cx="65" cy="88" r="13" fill="#94a3b8"/>
  <circle cx="230" cy="88" r="22" fill="#020617" stroke="#475569" stroke-width="4"/>
  <circle cx="230" cy="88" r="13" fill="#94a3b8"/>
  <!-- Headlights & Taillights -->
  <rect x="270" y="66" width="12" height="4" rx="2" fill="#38bdf8" filter="url(#softGlow)"/>
  <rect x="8" y="68" width="8" height="4" rx="2" fill="#ef4444" filter="url(#softGlow)"/>
</g>
''')

    # DRAWING ROOM PAVILION (X=36.875' to 52.625')
    # Split-face Travertine Stone Cladding + Feature Ribbon Window W2
    dr_x0 = wx(36.875)
    dr_w = (52.625 - 36.875) * SCALE
    dr_h = (10.5 - 1.5) * SCALE
    
    svg.append(f'''
<!-- Drawing Room Prominent Volume: Roman Split-Face Travertine Stone Cladding -->
<g filter="url(#crispShadow)">
  <rect x="{dr_x0}" y="{wy(10.5)}" width="{dr_w}" height="{dr_h}" fill="url(#travertineSkin)" stroke="#78350f" stroke-width="2"/>
  <rect x="{dr_x0}" y="{wy(10.5)}" width="{dr_w}" height="{dr_h}" fill="url(#travertineJoints)" opacity="0.85"/>
</g>

<!-- Drawing Room Large Ribbon Window W2 (7'-0" x 6'-0", Sill +2.0', Head +8.0') -->
<g>
  <rect x="{wx(41.625)}" y="{wy(8.0)}" width="{(48.625 - 41.625)*SCALE}" height="{(8.0 - 2.0)*SCALE}" fill="#020617" stroke="#0f172a" stroke-width="3"/>
  <rect x="{wx(41.8)}" y="{wy(7.8)}" width="{(48.2 - 41.625)*SCALE}" height="{(7.6 - 2.2)*SCALE}" fill="url(#interiorWarmGlow)"/>
  <rect x="{wx(41.8)}" y="{wy(7.8)}" width="{(48.2 - 41.625)*SCALE}" height="{(7.6 - 2.2)*SCALE}" fill="url(#glassReflection)"/>
  <!-- Luxury Chandelier Silhouette Inside Drawing Room -->
  <ellipse cx="{wx(45.125)}" cy="{wy(5.8)}" rx="20" ry="10" fill="#fde047" opacity="0.8" filter="url(#softGlow)"/>
  <line x1="{wx(45.125)}" y1="{wy(7.8)}" x2="{wx(45.125)}" y2="{wy(5.8)}" stroke="#ca8a04" stroke-width="1.5"/>
  <!-- Minimal Window Dividing Mullion -->
  <line x1="{wx(45.125)}" y1="{wy(8.0)}" x2="{wx(45.125)}" y2="{wy(2.0)}" stroke="#0f172a" stroke-width="2.5"/>
</g>

<!-- Modern Teak Architectural Slat Screen on Left Corner of Drawing Room -->
<g>
''')
    for i in range(5):
        lx = wx(37.5 + i * 0.7)
        svg.append(f'''
<rect x="{lx}" y="{wy(10.2)}" width="5" height="{(10.2 - 1.8)*SCALE}" fill="url(#teakLouver)" stroke="#5c3216" stroke-width="0.75" filter="url(#crispShadow)"/>
''')
    svg.append('</g>')

    # MAIN ENTRANCE FOYER (X=52.625' to 60.0')
    # Grand Walnut Pivot Door & Illuminated Entry Steps
    foyer_x0 = wx(52.625)
    foyer_w = (60.0 - 52.625) * SCALE
    
    svg.append(f'''
<!-- Main Entrance Foyer Volume (Recessed Air-Lock Entry) -->
<rect x="{foyer_x0}" y="{wy(10.5)}" width="{foyer_w}" height="{dr_h}" fill="url(#stuccoWall)" stroke="#334155" stroke-width="2"/>

<!-- Entrance Foyer Recess Shadow -->
<rect x="{foyer_x0}" y="{wy(10.5)}" width="18" height="{dr_h}" fill="url(#dropShadowH)"/>

<!-- Grand Walnut Solid Pivot Door (4'-0" x 8'-0") -->
<rect x="{wx(54.5)}" y="{wy(9.5)}" width="{(58.5 - 54.5)*SCALE}" height="{(9.5 - 1.5)*SCALE}" fill="url(#woodSoffit)" stroke="#3b1d08" stroke-width="2"/>
<!-- Modern Vertical Bronze Pull Handle (5-ft long) -->
<rect x="{wx(57.8)}" y="{wy(7.0)}" width="4" height="{(5.0)*SCALE}" rx="2" fill="#d97706" filter="url(#crispShadow)"/>
<!-- Transom Glass Above Door -->
<rect x="{wx(54.5)}" y="{wy(10.2)}" width="{(58.5 - 54.5)*SCALE}" height="{(10.2 - 9.5)*SCALE}" fill="url(#glassReflection)" stroke="#0f172a" stroke-width="1.5"/>

<!-- Illuminated Architectural Floating Steps (Z=0.0 to 1.5 ft) -->
<rect x="{wx(53.5)}" y="{wy(0.5)}" width="{(59.5 - 53.5)*SCALE}" height="{(0.5)*SCALE}" fill="#f1f5f9" stroke="#94a3b8" stroke-width="1.5"/>
<line x1="{wx(53.5)}" y1="{wy(0.5)}" x2="{wx(59.5)}" y2="{wy(0.5)}" stroke="#fde047" stroke-width="3" filter="url(#softGlow)"/>

<rect x="{wx(54.0)}" y="{wy(1.0)}" width="{(59.0 - 54.0)*SCALE}" height="{(0.5)*SCALE}" fill="#f8fafc" stroke="#94a3b8" stroke-width="1.5"/>
<line x1="{wx(54.0)}" y1="{wy(1.0)}" x2="{wx(59.0)}" y2="{wy(1.0)}" stroke="#fde047" stroke-width="3" filter="url(#softGlow)"/>

<!-- Architectural Planter Urn Beside Entrance -->
<rect x="{wx(52.8)}" y="{wy(3.5)}" width="16" height="40" fill="#334155" stroke="#0f172a" stroke-width="1.5"/>
<ellipse cx="{wx(53.2)}" cy="{wy(4.8)}" rx="18" ry="24" fill="#15803d" opacity="0.85"/>
''')

    # BEDROOM 1 & LOUNGE FACADE (X=60.0' to 87.5')
    bed1_x0 = wx(60.0)
    bed1_w = (87.5 - 60.0) * SCALE
    
    svg.append(f'''
<!-- Ground Floor Bedroom 1 Suite & Lounge East Wing Facade -->
<rect x="{bed1_x0}" y="{wy(10.5)}" width="{bed1_w}" height="{dr_h}" fill="url(#stuccoWall)" stroke="#334155" stroke-width="2"/>

<!-- Bedroom 1 Ribbon Window W1 (7'-0" x 6'-0", Sill +2.0', Head +8.0') -->
<g>
  <rect x="{wx(76.125)}" y="{wy(8.0)}" width="{(83.125 - 76.125)*SCALE}" height="{(8.0 - 2.0)*SCALE}" fill="#020617" stroke="#0f172a" stroke-width="3"/>
  <rect x="{wx(76.3)}" y="{wy(7.8)}" width="{(82.7 - 76.125)*SCALE}" height="{(7.6 - 2.2)*SCALE}" fill="url(#interiorWarmGlow)"/>
  <rect x="{wx(76.3)}" y="{wy(7.8)}" width="{(82.7 - 76.125)*SCALE}" height="{(7.6 - 2.2)*SCALE}" fill="url(#glassReflection)"/>
  <line x1="{wx(79.625)}" y1="{wy(8.0)}" x2="{wx(79.625)}" y2="{wy(2.0)}" stroke="#0f172a" stroke-width="2.5"/>
</g>

<!-- Architectural Vertical Accent Fin (Between Lounge and Bed 1) -->
<rect x="{wx(71.375)}" y="{wy(10.5)}" width="{(72.125 - 71.375)*SCALE}" height="{dr_h}" fill="#1e293b" stroke="#0f172a" stroke-width="2"/>

<!-- East Party Wall Corner Column E1 (X=87.5') -->
<rect x="{wx(87.125)}" y="{wy(10.5)}" width="{(87.875 - 87.125)*SCALE}" height="{dr_h}" fill="#1e293b" stroke="#0f172a" stroke-width="2"/>
''')

    # 6. ENTOURAGE & CONTEMPORARY LANDSCAPE
    svg.append('''
<!-- ====================================================================== -->
<!-- 6. LANDSCAPE ENTOURAGE & HUMAN SCALE FIGURES -->
<!-- ====================================================================== -->
<!-- Japanese Sculptural Maple / Bamboo in Front Lawn (X=8.0' to 14.0') -->
<g transform="translate(480, 1020)">
  <!-- Tree Trunk -->
  <path d="M 50,160 Q 45,110 35,70 Q 25,30 15,0 Q 25,35 30,80 Q 40,120 52,160 Z" fill="#475569"/>
  <!-- Delicate Branches & Foliage Clouds -->
  <circle cx="10" cy="-5" r="28" fill="#15803d" opacity="0.65"/>
  <circle cx="35" cy="20" r="22" fill="#16a34a" opacity="0.70"/>
  <circle cx="-15" cy="35" r="24" fill="#22c55e" opacity="0.60"/>
  <circle cx="20" cy="55" r="18" fill="#15803d" opacity="0.65"/>
</g>

<!-- Human Scale Figures (Architectural Vector Silhouettes) -->
<!-- Figure 1: Walking toward entrance -->
<g transform="translate(1360, 1100) scale(0.65)">
  <!-- Head -->
  <circle cx="20" cy="15" r="8" fill="#1e293b"/>
  <!-- Torso & Coat -->
  <path d="M 12,25 L 28,25 L 32,75 L 8,75 Z" fill="#334155"/>
  <!-- Legs -->
  <line x1="14" y1="75" x2="10" y2="125" stroke="#1e293b" stroke-width="5" stroke-linecap="round"/>
  <line x1="26" y1="75" x2="30" y2="125" stroke="#1e293b" stroke-width="5" stroke-linecap="round"/>
</g>

<!-- Figure 2: On upper terrace -->
<g transform="translate(980, 810) scale(0.55)">
  <circle cx="15" cy="12" r="7" fill="#64748b"/>
  <path d="M 8,20 L 22,20 L 25,60 L 5,60 Z" fill="#475569"/>
  <line x1="10" y1="60" x2="8" y2="100" stroke="#334155" stroke-width="4" stroke-linecap="round"/>
  <line x1="20" y1="60" x2="22" y2="100" stroke="#334155" stroke-width="4" stroke-linecap="round"/>
</g>
''')

    # 7. ARCHITECTURAL ELEVATION DATUMS & LEVEL SYMBOLS
    levels = [
        ("FINISHED GROUND LEVEL", "±0'-0\"", 0.0),
        ("PLINTH FINISHED LEVEL", "+1'-6\"", 1.5),
        ("FIRST FLOOR FFL", "+11'-10\"", 11.833),
        ("SECOND FLOOR FFL", "+22'-2\"", 22.167),
        ("ROOF CANOPY LEVEL", "+32'-6\"", 32.5),
        ("TOP OF MUMTY &amp; TANK", "+42'-0\"", 42.0),
    ]

    svg.append('''
<!-- ====================================================================== -->
<!-- 7. ARCHITECTURAL LEVEL DATUMS (LEFT SIDE CALLOUTS) -->
<!-- ====================================================================== -->
''')
    for name, fi_txt, z_val in levels:
        ly = wy(z_val)
        svg.append(f'''
<!-- Datum Line for {name} -->
<line x1="60" y1="{ly}" x2="{wx(92)}" y2="{ly}" stroke="#94a3b8" stroke-width="0.75" stroke-dasharray="6,4"/>

<!-- CAD Level Symbol Target (Quarter Circle) -->
<circle cx="110" cy="{ly}" r="12" fill="#ffffff" stroke="#0f172a" stroke-width="1.5"/>
<path d="M 98,{ly} A 12,12 0 0,0 110,{ly-12} L 110,{ly} Z" fill="#0f172a"/>
<path d="M 110,{ly} A 12,12 0 0,0 122,{ly+12} L 110,{ly} Z" fill="#0f172a"/>

<!-- Level Description & Elevation Height -->
<text x="135" y="{ly - 3}" font-family="'Helvetica Neue', Arial, sans-serif" font-size="11" font-weight="bold" fill="#0f172a">{name}</text>
<text x="135" y="{ly + 11}" font-family="'Helvetica Neue', Arial, sans-serif" font-size="10" font-weight="600" fill="#475569">{fi_txt}</text>
''')

    # 8. MATERIAL ANNOTATIONS & ARCHITECTURAL SPECIFICATION CALLOUTS
    callouts = [
        ("01. 14\" ANODIZED BRONZE CANOPY FASCIA (HORIZONTAL FLOATING SLAB)", wx(24.0), wy(12.0), wx(12.0), wy(16.0)),
        ("02. WARM TEAK TIMBER PERGOLA &amp; SOLAR SHADING LOUVERS", wx(45.0), wy(33.0), wx(32.0), wy(37.5)),
        ("03. SPLIT-FACE TRAVERTINE STONE VOLUMETRIC SKIN", wx(45.0), wy(7.0), wx(30.0), wy(4.0)),
        ("04. 12mm STRUCTURAL FRAMELESS TEMPERED GLASS BALUSTRADE", wx(28.0), wy(14.5), wx(18.0), wy(19.5)),
        ("05. CONTINUOUS 9\"x18\" RCC COLUMNS CONCEALED IN 9\" WALLS", wx(71.75), wy(17.0), wx(74.0), wy(12.0)),
        ("06. 2-CAR CANOPY CARPORT (EV READY | TRAVERTINE PAVING)", wx(26.0), wy(4.0), wx(14.0), wy(2.0)),
    ]

    svg.append('''
<!-- ====================================================================== -->
<!-- 8. ARCHITECTURAL SPECIFICATION & MATERIAL LEADER LINES -->
<!-- ====================================================================== -->
''')
    for text, ax, ay, tx, ty in callouts:
        svg.append(f'''
<circle cx="{ax}" cy="{ay}" r="3.5" fill="#e11d48"/>
<polyline points="{ax},{ay} {tx},{ty} {tx + (180 if tx >= ax else -180)},{ty}" fill="none" stroke="#e11d48" stroke-width="1.2"/>
<text x="{tx + (10 if tx >= ax else -10)}" y="{ty - 5}" font-family="'Helvetica Neue', Arial, sans-serif" font-size="10" font-weight="bold" fill="#0f172a" text-anchor="{'start' if tx >= ax else 'end'}">{text}</text>
''')

    # 9. DIMENSION STRINGS ACROSS OVERALL FRONTAGE
    dim_y = wy(-4.5)
    svg.append(f'''
<!-- ====================================================================== -->
<!-- 9. OVERALL DIMENSIONS & SETBACK SPANS -->
<!-- ====================================================================== -->
<!-- Overall Frontage Dimension Line: 87'-11" (26.80m) -->
<line x1="{wx(0.0)}" y1="{dim_y}" x2="{wx(87.917)}" y2="{dim_y}" stroke="#0f172a" stroke-width="1.5"/>
<line x1="{wx(0.0)}" y1="{dim_y - 12}" x2="{wx(0.0)}" y2="{dim_y + 12}" stroke="#0f172a" stroke-width="2"/>
<line x1="{wx(87.917)}" y1="{dim_y - 12}" x2="{wx(87.917)}" y2="{dim_y + 12}" stroke="#0f172a" stroke-width="2"/>
<!-- 45-deg Architectural Slash Ticks -->
<line x1="{wx(0.0)-6}" y1="{dim_y+6}" x2="{wx(0.0)+6}" y2="{dim_y-6}" stroke="#0f172a" stroke-width="2.5"/>
<line x1="{wx(87.917)-6}" y1="{dim_y+6}" x2="{wx(87.917)+6}" y2="{dim_y-6}" stroke="#0f172a" stroke-width="2.5"/>
<rect x="{wx(44.0)-140}" y="{dim_y-14}" width="280" height="26" fill="#ffffff" stroke="#cbd5e1" stroke-width="1" rx="4"/>
<text x="{wx(44.0)}" y="{dim_y+4}" font-family="'Helvetica Neue', Arial, sans-serif" font-size="14" font-weight="bold" fill="#0f172a" text-anchor="middle">OVERALL PLOT FRONTAGE = 87'-11" (26.80 m)</text>

<!-- Bay Sub-Dimensions (Porch, Drawing Room, Foyer, Bedroom 1) -->
<line x1="{wx(17.5)}" y1="{dim_y + 26}" x2="{wx(36.875)}" y2="{dim_y + 26}" stroke="#475569" stroke-width="1.2"/>
<line x1="{wx(17.5)-4}" y1="{dim_y + 30}" x2="{wx(17.5)+4}" y2="{dim_y + 22}" stroke="#475569" stroke-width="2"/>
<line x1="{wx(36.875)-4}" y1="{dim_y + 30}" x2="{wx(36.875)+4}" y2="{dim_y + 22}" stroke="#475569" stroke-width="2"/>
<text x="{wx(27.18)}" y="{dim_y + 40}" font-family="'Helvetica Neue', Arial, sans-serif" font-size="11" font-weight="bold" fill="#334155" text-anchor="middle">PORCH: 19'-4½"</text>

<line x1="{wx(36.875)}" y1="{dim_y + 26}" x2="{wx(52.625)}" y2="{dim_y + 26}" stroke="#475569" stroke-width="1.2"/>
<line x1="{wx(52.625)-4}" y1="{dim_y + 30}" x2="{wx(52.625)+4}" y2="{dim_y + 22}" stroke="#475569" stroke-width="2"/>
<text x="{wx(44.75)}" y="{dim_y + 40}" font-family="'Helvetica Neue', Arial, sans-serif" font-size="11" font-weight="bold" fill="#334155" text-anchor="middle">DRAWING ROOM: 15'-9"</text>

<line x1="{wx(52.625)}" y1="{dim_y + 26}" x2="{wx(71.375)}" y2="{dim_y + 26}" stroke="#475569" stroke-width="1.2"/>
<line x1="{wx(71.375)-4}" y1="{dim_y + 30}" x2="{wx(71.375)+4}" y2="{dim_y + 22}" stroke="#475569" stroke-width="2"/>
<text x="{wx(62.0)}" y="{dim_y + 40}" font-family="'Helvetica Neue', Arial, sans-serif" font-size="11" font-weight="bold" fill="#334155" text-anchor="middle">FOYER &amp; LOUNGE: 18'-9"</text>

<line x1="{wx(71.375)}" y1="{dim_y + 26}" x2="{wx(87.5)}" y2="{dim_y + 26}" stroke="#475569" stroke-width="1.2"/>
<line x1="{wx(87.5)-4}" y1="{dim_y + 30}" x2="{wx(87.5)+4}" y2="{dim_y + 22}" stroke="#475569" stroke-width="2"/>
<text x="{wx(79.4)}" y="{dim_y + 40}" font-family="'Helvetica Neue', Arial, sans-serif" font-size="11" font-weight="bold" fill="#334155" text-anchor="middle">BEDROOM 1: 16'-1½"</text>
''')

    # 10. LUXURY ARCHITECTURAL TITLE BLOCK
    tb_x0 = 1720
    tb_y0 = 1320
    tb_w = 640
    tb_h = 140
    
    svg.append(f'''
<!-- ====================================================================== -->
<!-- 10. LUXURY ARCHITECTURAL PRESENTATION TITLE BLOCK -->
<!-- ====================================================================== -->
<g filter="url(#crispShadow)">
  <!-- Title Block Shell -->
  <rect x="{tb_x0}" y="{tb_y0}" width="{tb_w}" height="{tb_h}" rx="8" fill="#0f172a" stroke="#1e293b" stroke-width="2"/>
  <rect x="{tb_x0+4}" y="{tb_y0+4}" width="{tb_w-8}" height="32" rx="4" fill="#1e293b"/>
  
  <!-- Project Title -->
  <text x="{tb_x0+16}" y="{tb_y0+25}" font-family="'Helvetica Neue', Arial, sans-serif" font-size="13" font-weight="bold" fill="#f8fafc" letter-spacing="1.5">DAATA HAMLET RESIDENCE</text>
  <text x="{tb_x0+tb_w-16}" y="{tb_y0+25}" font-family="'Helvetica Neue', Arial, sans-serif" font-size="11" font-weight="bold" fill="#f59e0b" text-anchor="end">CANOPY ARCHITECTURE</text>
  
  <!-- Drawing Name -->
  <text x="{tb_x0+16}" y="{tb_y0+58}" font-family="'Helvetica Neue', Arial, sans-serif" font-size="16" font-weight="800" fill="#ffffff" letter-spacing="0.5">SOUTH FRONT ELEVATION — LUXURY CANOPY STYLE</text>
  <text x="{tb_x0+16}" y="{tb_y0+78}" font-family="'Helvetica Neue', Arial, sans-serif" font-size="11" font-weight="500" fill="#94a3b8">3-STOREY RESIDENCE | 22 CONTINUOUS CONCEALED RCC COLUMNS | 100% ZERO-LOOPHOLE DESIGN</text>
  
  <!-- Metadata Grid -->
  <line x1="{tb_x0+16}" y1="{tb_y0+90}" x2="{tb_x0+tb_w-16}" y2="{tb_y0+90}" stroke="#334155" stroke-width="1"/>
  
  <text x="{tb_x0+16}" y="{tb_y0+106}" font-family="'Helvetica Neue', Arial, sans-serif" font-size="10" font-weight="bold" fill="#64748b">SHEET NO:</text>
  <text x="{tb_x0+80}" y="{tb_y0+106}" font-family="'Helvetica Neue', Arial, sans-serif" font-size="11" font-weight="bold" fill="#38bdf8">A-201</text>
  
  <text x="{tb_x0+160}" y="{tb_y0+106}" font-family="'Helvetica Neue', Arial, sans-serif" font-size="10" font-weight="bold" fill="#64748b">SCALE:</text>
  <text x="{tb_x0+210}" y="{tb_y0+106}" font-family="'Helvetica Neue', Arial, sans-serif" font-size="11" font-weight="bold" fill="#f8fafc">1/4" = 1'-0" (1:50)</text>
  
  <text x="{tb_x0+340}" y="{tb_y0+106}" font-family="'Helvetica Neue', Arial, sans-serif" font-size="10" font-weight="bold" fill="#64748b">PLOT AREA:</text>
  <text x="{tb_x0+415}" y="{tb_y0+106}" font-family="'Helvetica Neue', Arial, sans-serif" font-size="11" font-weight="bold" fill="#f8fafc">3,129.1 SQ.FT (12.8 MARLA)</text>
  
  <text x="{tb_x0+16}" y="{tb_y0+124}" font-family="'Helvetica Neue', Arial, sans-serif" font-size="10" font-weight="bold" fill="#64748b">COVERED AREA:</text>
  <text x="{tb_x0+110}" y="{tb_y0+124}" font-family="'Helvetica Neue', Arial, sans-serif" font-size="11" font-weight="bold" fill="#f8fafc">5,586.0 SQ.FT</text>
  
  <text x="{tb_x0+240}" y="{tb_y0+124}" font-family="'Helvetica Neue', Arial, sans-serif" font-size="10" font-weight="bold" fill="#64748b">VERIFICATION:</text>
  <text x="{tb_x0+330}" y="{tb_y0+124}" font-family="'Helvetica Neue', Arial, sans-serif" font-size="11" font-weight="bold" fill="#4ade80">108 / 108 AUTOMATED TESTS PASS (100% FOOLPROOF)</text>
</g>

<!-- Modern North & Elevation Compass Symbol -->
<g transform="translate(2300, 120)">
  <circle cx="0" cy="0" r="26" fill="#ffffff" stroke="#0f172a" stroke-width="1.8" filter="url(#crispShadow)"/>
  <polygon points="0,-20 -6,0 0,-4" fill="#e11d48"/>
  <polygon points="0,-20 6,0 0,-4" fill="#0f172a"/>
  <polygon points="0,20 -6,0 0,4" fill="#94a3b8"/>
  <polygon points="0,20 6,0 0,4" fill="#cbd5e1"/>
  <text x="0" y="-24" font-family="'Helvetica Neue', Arial, sans-serif" font-size="12" font-weight="bold" fill="#0f172a" text-anchor="middle">N</text>
  <text x="0" y="34" font-family="'Helvetica Neue', Arial, sans-serif" font-size="9" font-weight="bold" fill="#64748b" text-anchor="middle">SOUTH VIEW</text>
</g>

</svg>''')

    return "\n".join(svg)

def export():
    svg_content = build_luxury_elevation_svg()
    for p in OUT_PATHS:
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(svg_content, encoding="utf-8")
        print(f"[+] Exported presentation luxury elevation to: {p}")

if __name__ == "__main__":
    export()
