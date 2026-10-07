"""
DAATA HAMLET RESIDENCE - Master Luxury Architectural Front Elevation Generator
Accurately implements the Master Scheme across the South (Front) Facade:
1. MAIN LAWN (X=0.00' to 36.125', ~500 SQ.FT OPEN GARDEN):
   Lush manicured lawn, travertine stepping stones, architectural landscaping, open to sky.
2. BEDROOM 2 (X=36.125' to 51.375', GROUND FLOOR):
   Travertine-clad modern facade with expansive sliding glass garden doors (8'x7') opening directly onto the Main Lawn.
3. BED-2 BATH & DRESS (X=51.375' to 56.625'):
   Architectural stone wall section with vertical reveal grooves.
4. CENTRAL CAR PORCH (X=56.625' to 68.625', 11'-3" x 20'-6"):
   Covered luxury carport with cantilevered bronze canopy fascia, warm LED recessed soffit lighting,
   paved travertine driveway, luxury executive vehicle, and grand 6'-0" Double Walnut Main Entrance Door.
5. FIRST FLOOR OPEN FRONT SUN TERRACE / BALCONY (X=56.625' to 68.625', OVER PORCH):
   Directly above Car Porch, featuring 12mm frameless tempered glass balustrade and sliding glass lounge doors.
6. CENTRAL STAIRCASE MUMTY TOWER (X=56.625' to 69.375', Z=32'-6" to +42'-0"):
   Rises centrally above the stair core with vertical ribbon glass, floating bronze canopy, and screened water tank.
7. DRAWING ROOM (X=68.625' to 84.375', GROUND FLOOR):
   Grand formal picture window (9'-0" x 6'-6") with chandelier illumination, sheer drapery, and warm stucco facade.
8. FIRST FLOOR BEDROOM 3 (MASTER SUITE) & SECOND FLOOR BEDROOM 6 (X=68.625' to 84.375'):
   Stacked luxury bedroom suites with graphite aluminum framed windows.
9. SECOND FLOOR WEST SUN TERRACE (X=36.125' to 51.375'):
   Open-to-sky sun deck with frameless glass railing, outdoor loungers, and planter foliage.
10. EAST PERIMETER PASSAGEWAY (X=84.375' to 87.21'):
    Distinct 2'-1" clear reveal with slim stone fin and flush slatted bronze security gate.
11. DUAL SHEETS:
    - Sheet A-201A: WITH boundary wall visible in background.
    - Sheet A-201B: WITHOUT boundary wall (pure architecture).
"""
from __future__ import annotations
import pathlib
import sys
from playwright.sync_api import sync_playwright

WORKSPACE = pathlib.Path(__file__).parent.parent.parent.resolve()
sys.path.insert(0, str(WORKSPACE))
BLUEPRINTS_DIR = WORKSPACE / "blueprints" / "daata_hamlet"
BRAIN_DIR = pathlib.Path(r"C:\Users\adees\.gemini\antigravity\brain\754b2257-dc8d-4e91-8a73-3c0efba21f41")

from scripts.daata_hamlet.model import (
    XB_O, XB_I, XC_W, XC_E, XC_P_W, XC_P_E, XD_W, XD_E, XE_I, XE_O,
    STAIR_X0, STAIR_X1, GX, GY, MUMTY_TOP, fi
)


def render_elevation_svg(with_boundary_wall: bool) -> str:
    W, H = 2400, 1500
    SCALE = 20.0
    ORIGIN_X = 320.0  # world X = 0.0 (West plot boundary)
    GROUND_Y = 1180.0 # world Z = 0.0 (Finished Ground Level)

    def wx(ft: float) -> float:
        return ORIGIN_X + ft * SCALE

    def wy(ft: float) -> float:
        return GROUND_Y - ft * SCALE

    sheet_title = "SOUTH FRONT ELEVATION — WITH BOUNDARY WALL (BACKGROUND)" if with_boundary_wall else "SOUTH FRONT ELEVATION — PURE ARCHITECTURE (WITHOUT BOUNDARY WALL)"
    sheet_no = "A-201A" if with_boundary_wall else "A-201B"
    version_badge = "WITH BOUNDARY WALL" if with_boundary_wall else "WITHOUT BOUNDARY WALL"

    svg = []
    svg.append(f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
<defs>
  <!-- Atmosphere Gradients -->
  <linearGradient id="skyGrad" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0%" stop-color="#e2ebf5"/>
    <stop offset="45%" stop-color="#edf4fa"/>
    <stop offset="85%" stop-color="#fdfbf7"/>
    <stop offset="100%" stop-color="#fff8ec"/>
  </linearGradient>

  <linearGradient id="groundGrad" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0%" stop-color="#2d3748"/>
    <stop offset="15%" stop-color="#1a202c"/>
    <stop offset="100%" stop-color="#0f172a"/>
  </linearGradient>

  <linearGradient id="lawnGrassGrad" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0%" stop-color="#4d7c0f"/>
    <stop offset="35%" stop-color="#3f6212"/>
    <stop offset="100%" stop-color="#1e3a0f"/>
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

  <linearGradient id="glassBalustrade" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0%" stop-color="#e0f2fe" stop-opacity="0.75"/>
    <stop offset="50%" stop-color="#bae6fd" stop-opacity="0.55"/>
    <stop offset="100%" stop-color="#7dd3fc" stop-opacity="0.35"/>
  </linearGradient>

  <linearGradient id="interiorWarmGlow" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0%" stop-color="#fef08a" stop-opacity="0.75"/>
    <stop offset="50%" stop-color="#fed7aa" stop-opacity="0.50"/>
    <stop offset="100%" stop-color="#fdba74" stop-opacity="0.25"/>
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

  <linearGradient id="dropShadowV" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0%" stop-color="#000000" stop-opacity="0.45"/>
    <stop offset="40%" stop-color="#000000" stop-opacity="0.25"/>
    <stop offset="100%" stop-color="#000000" stop-opacity="0.0"/>
  </linearGradient>

  <linearGradient id="wallSconceGlow" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0%" stop-color="#fef08a" stop-opacity="0.8"/>
    <stop offset="60%" stop-color="#fed7aa" stop-opacity="0.3"/>
    <stop offset="100%" stop-color="#f59e0b" stop-opacity="0.0"/>
  </linearGradient>

  <!-- Car Shaders -->
  <linearGradient id="suvBody" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0%" stop-color="#1e293b"/>
    <stop offset="20%" stop-color="#334155"/>
    <stop offset="50%" stop-color="#475569"/>
    <stop offset="80%" stop-color="#334155"/>
    <stop offset="100%" stop-color="#1e293b"/>
  </linearGradient>

  <linearGradient id="redLightbar" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0%" stop-color="#b91c1c"/>
    <stop offset="15%" stop-color="#ef4444"/>
    <stop offset="50%" stop-color="#f87171"/>
    <stop offset="85%" stop-color="#ef4444"/>
    <stop offset="100%" stop-color="#b91c1c"/>
  </linearGradient>

  <pattern id="travertineJoints" width="40" height="14" patternUnits="userSpaceOnUse">
    <rect width="40" height="14" fill="none"/>
    <line x1="0" y1="14" x2="40" y2="14" stroke="#c4b595" stroke-width="0.75" stroke-opacity="0.8"/>
    <line x1="20" y1="0" x2="20" y2="14" stroke="#c4b595" stroke-width="0.75" stroke-opacity="0.8"/>
  </pattern>

  <pattern id="boundaryWallGroove" width="40" height="18" patternUnits="userSpaceOnUse">
    <rect width="40" height="18" fill="#e2e8f0"/>
    <line x1="0" y1="18" x2="40" y2="18" stroke="#cbd5e1" stroke-width="1.2"/>
  </pattern>

  <pattern id="carportBackSlats" width="10" height="40" patternUnits="userSpaceOnUse">
    <rect width="10" height="40" fill="#1e293b"/>
    <rect x="2" width="6" height="40" fill="#2d3748"/>
  </pattern>

  <pattern id="passageGateSlats" width="8" height="40" patternUnits="userSpaceOnUse">
    <rect width="8" height="40" fill="#0f172a"/>
    <rect x="2" width="4" height="40" fill="#bc7a3d"/>
  </pattern>

  <!-- Shadow & Glow Filters -->
  <filter id="crispShadow" x="-10%" y="-10%" width="120%" height="130%">
    <feDropShadow dx="0" dy="4" stdDeviation="3" flood-color="#0f172a" flood-opacity="0.25"/>
  </filter>
  <filter id="softGlow" x="-30%" y="-30%" width="160%" height="160%">
    <feGaussianBlur stdDeviation="6" result="blur"/>
    <feComposite in="SourceGraphic" in2="blur" operator="over"/>
  </filter>
  <filter id="tailLightGlow" x="-20%" y="-20%" width="140%" height="140%">
    <feGaussianBlur stdDeviation="3" result="blur"/>
    <feComposite in="SourceGraphic" in2="blur" operator="over"/>
  </filter>
</defs>

<!-- 1. PRESENTATION SHEET BORDER -->
<rect x="20" y="20" width="{W-40}" height="{H-40}" fill="#ffffff" stroke="#0f172a" stroke-width="2.5"/>
<rect x="34" y="34" width="{W-68}" height="{H-68}" fill="none" stroke="#94a3b8" stroke-width="1.5"/>

<!-- 2. ARCHITECTURAL SKY -->
<rect x="40" y="40" width="{W-80}" height="{GROUND_Y - 40}" fill="url(#skyGrad)"/>
<ellipse cx="{wx(44)}" cy="{GROUND_Y - 120}" rx="950" ry="300" fill="#fef3c7" opacity="0.35"/>

<!-- 3. GROUND STRATA & ROAD BASELINE -->
<rect x="40" y="{GROUND_Y}" width="{W-80}" height="{H - 40 - GROUND_Y}" fill="url(#groundGrad)"/>
<rect x="40" y="{wy(-1.5)}" width="{W-80}" height="{GROUND_Y - wy(-1.5)}" fill="#1e293b"/>
<line x1="40" y1="{wy(-1.5)}" x2="{W-40}" y2="{wy(-1.5)}" stroke="#475569" stroke-width="2"/>
<line x1="60" y1="{wy(-2.5)}" x2="{W-60}" y2="{wy(-2.5)}" stroke="#e2e8f0" stroke-width="3" stroke-dasharray="35,30"/>
<rect x="{wx(-2.0)}" y="{wy(-0.4)}" width="{wx(90.0) - wx(-2.0)}" height="{wy(-1.5) - wy(-0.4)}" fill="#cbd5e1" stroke="#94a3b8" stroke-width="1"/>
<line x1="{wx(-2.0)}" y1="{wy(-0.4)}" x2="{wx(90.0)}" y2="{wy(-0.4)}" stroke="#64748b" stroke-width="2"/>

<!-- Finished Ground Berm -->
<rect x="{wx(0.0)}" y="{wy(0.0)}" width="{wx(87.917) - wx(0.0)}" height="{wy(-0.4) - wy(0.0)}" fill="#365314" stroke="#1e293b" stroke-width="1"/>
''')

    # BOUNDARY WALL (BACKGROUND ONLY)
    if with_boundary_wall:
        bw_top_y = wy(7.0)
        bw_h = 7.0 * SCALE
        svg.append(f'''
<!-- BOUNDARY WALL IN BACKGROUND (BEHIND MAIN LAWN & EAST PASSAGE) -->
<g id="west-boundary-wall-bg">
  <rect x="{wx(0.0)}" y="{bw_top_y}" width="{(XB_O - 0.0)*SCALE}" height="{bw_h}" fill="url(#boundaryWallGroove)" stroke="#94a3b8" stroke-width="1.5"/>
  <rect x="{wx(0.0)-2}" y="{bw_top_y - 6}" width="{(XB_O - 0.0)*SCALE + 4}" height="6" fill="#1e293b" stroke="#0f172a" stroke-width="1"/>
  <rect x="{wx(12.0)}" y="{wy(5.0)}" width="8" height="18" rx="2" fill="#0f172a"/>
  <polygon points="{wx(12.0)+4},{wy(5.0)} {wx(12.0)-16},{wy(7.0)} {wx(12.0)+24},{wy(7.0)}" fill="url(#wallSconceGlow)" opacity="0.7"/>
  <polygon points="{wx(12.0)+4},{wy(5.0)+18} {wx(12.0)-16},{wy(3.0)} {wx(12.0)+24},{wy(3.0)}" fill="url(#wallSconceGlow)" opacity="0.7"/>
  <rect x="{wx(24.0)}" y="{wy(5.0)}" width="8" height="18" rx="2" fill="#0f172a"/>
  <polygon points="{wx(24.0)+4},{wy(5.0)} {wx(24.0)-16},{wy(7.0)} {wx(24.0)+24},{wy(7.0)}" fill="url(#wallSconceGlow)" opacity="0.7"/>
  <polygon points="{wx(24.0)+4},{wy(5.0)+18} {wx(24.0)-16},{wy(3.0)} {wx(24.0)+24},{wy(3.0)}" fill="url(#wallSconceGlow)" opacity="0.7"/>
</g>

<g id="east-boundary-wall-bg">
  <rect x="{wx(87.21)}" y="{bw_top_y}" width="{(91.5 - 87.21)*SCALE}" height="{bw_h}" fill="url(#boundaryWallGroove)" stroke="#94a3b8" stroke-width="1.5"/>
  <rect x="{wx(87.21)-2}" y="{bw_top_y - 6}" width="{(91.5 - 87.21)*SCALE + 4}" height="6" fill="#1e293b" stroke="#0f172a" stroke-width="1"/>
  <rect x="{wx(89.0)}" y="{wy(5.0)}" width="8" height="18" rx="2" fill="#0f172a"/>
  <polygon points="{wx(89.0)+4},{wy(5.0)} {wx(89.0)-16},{wy(7.0)} {wx(89.0)+24},{wy(7.0)}" fill="url(#wallSconceGlow)" opacity="0.7"/>
</g>
''')

    # STRUCTURAL COLUMN GRID LINES (B, C, C', D, E)
    grid_x_map = {'B': GX['B'], 'C': GX['C'], "C'": GX["C'"], 'D': GX['D'], 'E': GX['E']}
    svg.append('<!-- 4. STRUCTURAL COLUMN GRID LINES (B, C, C\', D, E) -->')
    for tag, gx_val in grid_x_map.items():
        cx = wx(gx_val)
        svg.append(f'''
<line x1="{cx}" y1="80" x2="{cx}" y2="{GROUND_Y + 40}" stroke="#94a3b8" stroke-width="1.2" stroke-dasharray="8,6,2,6"/>
<circle cx="{cx}" cy="80" r="16" fill="#ffffff" stroke="#0f172a" stroke-width="1.8"/>
<text x="{cx}" y="85" font-family="'Helvetica Neue', Arial, sans-serif" font-size="14" font-weight="bold" fill="#0f172a" text-anchor="middle">{tag}</text>
<circle cx="{cx}" cy="{GROUND_Y + 40}" r="14" fill="#ffffff" stroke="#0f172a" stroke-width="1.5"/>
<text x="{cx}" y="{GROUND_Y + 45}" font-family="'Helvetica Neue', Arial, sans-serif" font-size="12" font-weight="bold" fill="#0f172a" text-anchor="middle">{tag}</text>
''')

    # 5. THIRD FLOOR CENTRAL STAIRCASE MUMTY CORE (Z=32'-6" to +42'-0")
    # Central Staircase core rises at X in [56.625, 69.375]
    mumty_x0 = wx(XC_P_W)
    mumty_w = (XD_E - XC_P_W) * SCALE
    mumty_y0 = wy(MUMTY_TOP)
    mumty_h = (MUMTY_TOP - 32.5) * SCALE

    svg.append(f'''
<!-- 5. CENTRAL STAIRCASE MUMTY TOWER (X=56'-7½" to 69'-4½", Z=32'-6" to +42'-0") -->
<g id="rising-stair-mumty-core" filter="url(#crispShadow)">
  <rect x="{mumty_x0}" y="{mumty_y0}" width="{mumty_w}" height="{mumty_h}" fill="url(#stuccoWall)" stroke="#334155" stroke-width="2"/>
  <line x1="{mumty_x0}" y1="{wy(35.5)}" x2="{mumty_x0 + mumty_w}" y2="{wy(35.5)}" stroke="#cbd5e1" stroke-width="1.5"/>
  <line x1="{mumty_x0}" y1="{wy(38.5)}" x2="{mumty_x0 + mumty_w}" y2="{wy(38.5)}" stroke="#cbd5e1" stroke-width="1.5"/>

  <!-- Vertical Architectural Ribbon Window on Central Mumty Facade -->
  <rect x="{wx(61.0)}" y="{wy(40.5)}" width="{(65.0 - 61.0)*SCALE}" height="{(40.5 - 34.0)*SCALE}" fill="#0f172a" stroke="#000" stroke-width="2"/>
  <rect x="{wx(61.2)}" y="{wy(40.3)}" width="{(64.6 - 61.0)*SCALE}" height="{(40.1 - 34.2)*SCALE}" fill="url(#interiorWarmGlow)"/>
  <rect x="{wx(61.2)}" y="{wy(40.3)}" width="{(64.6 - 61.0)*SCALE}" height="{(40.1 - 34.2)*SCALE}" fill="url(#glassReflection)"/>
  <line x1="{wx(63.0)}" y1="{wy(40.5)}" x2="{wx(63.0)}" y2="{wy(34.0)}" stroke="#0f172a" stroke-width="2"/>

  <!-- Floating Charcoal Bronze Mumty Roof Canopy Fascia (+42'-0") -->
  <rect x="{mumty_x0 - 8}" y="{mumty_y0 - 10}" width="{mumty_w + 16}" height="12" fill="url(#bronzeCanopy)" stroke="#020617" stroke-width="2"/>
  <rect x="{mumty_x0 - 8}" y="{mumty_y0 - 10}" width="{mumty_w + 16}" height="3" fill="url(#bronzeTrim)"/>
  <rect x="{mumty_x0 - 6}" y="{mumty_y0 + 2}" width="{mumty_w + 12}" height="3" fill="url(#woodSoffit)"/>
  <rect x="{mumty_x0}" y="{mumty_y0 + 2}" width="{mumty_w}" height="14" fill="url(#dropShadowV)"/>

  <!-- Screened 800-Gallon Water Tank Enclosure atop Mumty Roof -->
  <rect x="{wx(60.5)}" y="{wy(45.5)}" width="{(66.5 - 60.5)*SCALE}" height="{(45.5 - 42.0)*SCALE}" rx="3" fill="#e2e8f0" stroke="#64748b" stroke-width="1.5"/>
  <line x1="{wx(60.5)}" y1="{wy(43.8)}" x2="{wx(66.5)}" y2="{wy(43.8)}" stroke="#94a3b8" stroke-width="1"/>
  <text x="{wx(63.5)}" y="{wy(43.5)}" font-family="'Helvetica Neue', Arial, sans-serif" font-size="8.5" font-weight="bold" fill="#64748b" text-anchor="middle">800-GAL TANK ENCLOSURE</text>
</g>
''')

    # 6. SECOND FLOOR ARCHITECTURE (Z=22'-2" to 32'-6")
    # Penthouse block from Grid C (51.375) to Grid E (85.125)
    f2_wall_x0 = wx(XC_W)
    f2_wall_w = (XE_O - XC_W) * SCALE
    f2_wall_y0 = wy(32.5)
    f2_wall_h = (32.5 - 22.167) * SCALE

    svg.append(f'''
<!-- 6. SECOND FLOOR PENTHOUSE ROOMS (X=51'-4½" to 85'-1½", Z=22'-2" to 32'-6") -->
<rect x="{f2_wall_x0}" y="{f2_wall_y0}" width="{f2_wall_w}" height="{f2_wall_h}" fill="url(#stuccoWall)" stroke="#334155" stroke-width="2"/>

<!-- Bedroom 7 Sliding Door (X=57.5 to 64.5) -->
<rect x="{wx(57.5)}" y="{wy(30.0)}" width="{(64.5 - 57.5)*SCALE}" height="{(30.0 - 24.5)*SCALE}" fill="#0f172a" stroke="#000" stroke-width="2"/>
<rect x="{wx(57.7)}" y="{wy(29.8)}" width="{(64.1 - 57.5)*SCALE}" height="{(29.6 - 24.7)*SCALE}" fill="url(#interiorWarmGlow)"/>
<rect x="{wx(57.7)}" y="{wy(29.8)}" width="{(64.1 - 57.5)*SCALE}" height="{(29.6 - 24.7)*SCALE}" fill="url(#glassReflection)"/>
<line x1="{wx(61.0)}" y1="{wy(30.0)}" x2="{wx(61.0)}" y2="{wy(24.5)}" stroke="#0f172a" stroke-width="3"/>

<!-- Bedroom 6 Window / Sliding Door (X=73.0 to 80.0) -->
<rect x="{wx(73.0)}" y="{wy(30.0)}" width="{(80.0 - 73.0)*SCALE}" height="{(30.0 - 24.5)*SCALE}" fill="#0f172a" stroke="#000" stroke-width="2"/>
<rect x="{wx(73.2)}" y="{wy(29.8)}" width="{(79.6 - 73.0)*SCALE}" height="{(29.6 - 24.7)*SCALE}" fill="url(#interiorWarmGlow)"/>
<rect x="{wx(73.2)}" y="{wy(29.8)}" width="{(79.6 - 73.0)*SCALE}" height="{(29.6 - 24.7)*SCALE}" fill="url(#glassReflection)"/>
<line x1="{wx(76.5)}" y1="{wy(30.0)}" x2="{wx(76.5)}" y2="{wy(24.5)}" stroke="#0f172a" stroke-width="3"/>

<!-- Columns D & E in 2F Facade -->
<rect x="{wx(XD_W)}" y="{wy(32.5)}" width="{(XD_E - XD_W)*SCALE}" height="{f2_wall_h}" fill="#1e293b" stroke="#0f172a" stroke-width="1.2"/>
<rect x="{wx(XE_I)}" y="{wy(32.5)}" width="{(XE_O - XE_I)*SCALE}" height="{f2_wall_h}" fill="#1e293b" stroke="#0f172a" stroke-width="1.2"/>

<!-- 2F PENTHOUSE ROOF CANOPY SLAB -->
<g filter="url(#crispShadow)">
  <rect x="{wx(XC_W - 0.5)}" y="{wy(32.8)}" width="{(XE_O + 0.5 - (XC_W - 0.5))*SCALE}" height="18" fill="url(#bronzeCanopy)" stroke="#0f172a" stroke-width="2"/>
  <rect x="{wx(XC_W - 0.5)}" y="{wy(32.8)}" width="{(XE_O + 0.5 - (XC_W - 0.5))*SCALE}" height="4" fill="url(#bronzeTrim)"/>
  <rect x="{wx(XC_W)}" y="{wy(31.9)}" width="{(XE_O - XC_W)*SCALE}" height="5" fill="url(#woodSoffit)"/>
</g>
''')

    # 7. SECOND FLOOR OPEN-TO-SKY FRONT SUN TERRACE (X=36.125' to 51.375')
    terrace_x0 = wx(XB_O)
    terrace_x1 = wx(XC_W)
    terrace_w = terrace_x1 - terrace_x0
    terrace_deck_y = wy(22.167)

    svg.append(f'''
<!-- 7. SECOND FLOOR OPEN-TO-SKY WEST SUN TERRACE (X=36'-1½" to 51'-4½") -->
<g id="second-floor-open-terrace">
  <polygon points="{wx(40.5)},{terrace_deck_y} {wx(45.5)},{terrace_deck_y} {wx(46.5)},{terrace_deck_y - 12} {wx(43.5)},{terrace_deck_y - 6} {wx(40.5)},{terrace_deck_y - 6}" fill="#475569" stroke="#334155" stroke-width="1"/>
  <rect x="{wx(44.5)}" y="{terrace_deck_y - 14}" width="10" height="4" rx="2" fill="#f8fafc"/>
  <rect x="{wx(47.0)}" y="{terrace_deck_y - 10}" width="12" height="10" rx="2" fill="#d97706" stroke="#92400e" stroke-width="1"/>
  <rect x="{wx(37.5)}" y="{terrace_deck_y - 16}" width="28" height="16" rx="2" fill="#1e293b" stroke="#0f172a" stroke-width="1"/>
  <circle cx="{wx(38.0)}" cy="{terrace_deck_y - 18}" r="8" fill="#15803d" opacity="0.8"/>
  <circle cx="{wx(38.8)}" cy="{terrace_deck_y - 22}" r="10" fill="#22c55e" opacity="0.85"/>

  <!-- 2F Frameless Glass Balustrade -->
  <rect x="{terrace_x0}" y="{wy(25.67)}" width="{terrace_w}" height="{(3.5)*SCALE}" fill="url(#glassBalustrade)" stroke="#93c5fd" stroke-width="1.2"/>
  <line x1="{terrace_x0}" y1="{wy(25.67)}" x2="{terrace_x1}" y2="{wy(25.67)}" stroke="#0f172a" stroke-width="3"/>
  <rect x="{terrace_x0}" y="{wy(22.4)}" width="{terrace_w}" height="6" fill="#64748b" stroke="#334155" stroke-width="1"/>
</g>
''')

    # 8. FIRST FLOOR ARCHITECTURE (Z=11'-10" to 22'-2")
    f1_wall_x0 = wx(XB_O)
    f1_wall_w = (XE_O - XB_O) * SCALE
    f1_wall_y0 = wy(21.5)
    f1_wall_h = (21.5 - 11.833) * SCALE

    svg.append(f'''
<!-- 8. FIRST FLOOR ARCHITECTURE (Z=11'-10" to 22'-2") -->
<rect x="{f1_wall_x0}" y="{f1_wall_y0}" width="{f1_wall_w}" height="{f1_wall_h}" fill="url(#stuccoWall)" stroke="#334155" stroke-width="2"/>

<!-- 1F Bed-4 Feature Facade (Travertine) (X=36.125 to 51.375) -->
<rect x="{wx(XB_O)}" y="{wy(21.5)}" width="{(XC_W - XB_O)*SCALE}" height="{f1_wall_h}" fill="url(#travertineSkin)" stroke="#78350f" stroke-width="1.8"/>
<rect x="{wx(XB_O)}" y="{wy(21.5)}" width="{(XC_W - XB_O)*SCALE}" height="{f1_wall_h}" fill="url(#travertineJoints)" opacity="0.65"/>

<!-- Bed-4 Window with Vertical Louvers (X=40.5 to 47.5) -->
<rect x="{wx(40.5)}" y="{wy(19.8)}" width="{(47.5 - 40.5)*SCALE}" height="{(19.8 - 14.0)*SCALE}" fill="#0f172a" stroke="#000" stroke-width="2"/>
<rect x="{wx(40.7)}" y="{wy(19.6)}" width="{(47.1 - 40.5)*SCALE}" height="{(19.4 - 14.2)*SCALE}" fill="url(#interiorWarmGlow)"/>
<rect x="{wx(40.7)}" y="{wy(19.6)}" width="{(47.1 - 40.5)*SCALE}" height="{(19.4 - 14.2)*SCALE}" fill="url(#glassReflection)"/>
''')
    for i in range(8):
        fx = wx(41.0 + i * 0.85)
        svg.append(f'<rect x="{fx}" y="{wy(20.2)}" width="6" height="{(20.2 - 13.6)*SCALE}" fill="url(#teakLouver)" stroke="#5c3216" stroke-width="0.75" filter="url(#crispShadow)"/>\n')

    # 1F Central Open Sun Terrace / Balcony above Car Porch (X=56.625 to 68.625)
    porch_terrace_x0 = wx(XC_P_W)
    porch_terrace_w = (XD_W - XC_P_W) * SCALE
    svg.append(f'''
<!-- 1F OPEN FRONT SUN TERRACE / BALCONY OVER CAR PORCH (X=56'-7½" to 68'-7½") -->
<g id="first-floor-porch-terrace">
  <!-- Recessed Sliding Door Access from 1F Lounge / Hall -->
  <rect x="{wx(58.5)}" y="{wy(19.8)}" width="{(66.5 - 58.5)*SCALE}" height="{(19.8 - 12.0)*SCALE}" fill="#0f172a" stroke="#000" stroke-width="2"/>
  <rect x="{wx(58.7)}" y="{wy(19.6)}" width="{(66.1 - 58.5)*SCALE}" height="{(19.4 - 12.2)*SCALE}" fill="url(#interiorWarmGlow)"/>
  <rect x="{wx(58.7)}" y="{wy(19.6)}" width="{(66.1 - 58.5)*SCALE}" height="{(19.4 - 12.2)*SCALE}" fill="url(#glassReflection)"/>
  <line x1="{wx(62.5)}" y1="{wy(19.8)}" x2="{wx(62.5)}" y2="{wy(12.0)}" stroke="#0f172a" stroke-width="3"/>

  <!-- Terrace Outdoor Planters -->
  <rect x="{wx(57.2)}" y="{wy(13.6)}" width="24" height="14" rx="2" fill="#334155" stroke="#1e293b" stroke-width="1"/>
  <path d="M {wx(57.2)},{wy(13.6)} Q {wx(58.2)},{wy(15.5)} {wx(59.2)},{wy(13.6)}" fill="#15803d" stroke="#166534" stroke-width="1.5"/>

  <!-- 1F Frameless Glass Balustrade over Car Porch -->
  <rect x="{porch_terrace_x0}" y="{wy(15.33)}" width="{porch_terrace_w}" height="{(3.5)*SCALE}" fill="url(#glassBalustrade)" stroke="#93c5fd" stroke-width="1.2"/>
  <line x1="{porch_terrace_x0}" y1="{wy(15.33)}" x2="{porch_terrace_x0 + porch_terrace_w}" y2="{wy(15.33)}" stroke="#0f172a" stroke-width="3"/>
  <rect x="{porch_terrace_x0}" y="{wy(12.0)}" width="{porch_terrace_w}" height="6" fill="#64748b" stroke="#334155" stroke-width="1"/>
</g>

<!-- 1F Bedroom 3 (Master Suite) Window (X=72.5 to 80.5) -->
<rect x="{wx(72.5)}" y="{wy(19.8)}" width="{(80.5 - 72.5)*SCALE}" height="{(19.8 - 14.0)*SCALE}" fill="#0f172a" stroke="#000" stroke-width="2"/>
<rect x="{wx(72.7)}" y="{wy(19.6)}" width="{(80.1 - 72.5)*SCALE}" height="{(19.4 - 14.2)*SCALE}" fill="url(#interiorWarmGlow)"/>
<rect x="{wx(72.7)}" y="{wy(19.6)}" width="{(80.1 - 72.5)*SCALE}" height="{(19.4 - 14.2)*SCALE}" fill="url(#glassReflection)"/>
<line x1="{wx(76.5)}" y1="{wy(19.8)}" x2="{wx(76.5)}" y2="{wy(14.0)}" stroke="#0f172a" stroke-width="3"/>

<!-- Columns B, C, C', D, E in 1F Facade -->
<rect x="{wx(GX['B']) - 4}" y="{wy(21.5)}" width="15" height="{f1_wall_h}" fill="#1e293b" stroke="#0f172a" stroke-width="1.2"/>
<rect x="{wx(GX['C']) - 4}" y="{wy(21.5)}" width="15" height="{f1_wall_h}" fill="#1e293b" stroke="#0f172a" stroke-width="1.2"/>
<rect x="{wx(XC_P_W) - 4}" y="{wy(21.5)}" width="15" height="{f1_wall_h}" fill="#1e293b" stroke="#0f172a" stroke-width="1.2"/>
<rect x="{wx(GX['D']) - 4}" y="{wy(21.5)}" width="15" height="{f1_wall_h}" fill="#1e293b" stroke="#0f172a" stroke-width="1.2"/>
<rect x="{wx(GX['E']) - 4}" y="{wy(21.5)}" width="15" height="{f1_wall_h}" fill="#1e293b" stroke="#0f172a" stroke-width="1.2"/>

<!-- CANTILEVERED CANOPY SLAB OVER CENTRAL CAR PORCH (Z=+11'-0") -->
<g id="car-porch-canopy-fascia" filter="url(#crispShadow)">
  <rect x="{wx(55.5)}" y="{wy(10.5)}" width="{(70.0 - 55.5)*SCALE}" height="28" fill="url(#dropShadowV)"/>
  <rect x="{wx(55.5)}" y="{wy(11.8)}" width="{(70.0 - 55.5)*SCALE}" height="20" fill="url(#bronzeCanopy)" stroke="#020617" stroke-width="2.5"/>
  <rect x="{wx(55.5)}" y="{wy(11.8)}" width="{(70.0 - 55.5)*SCALE}" height="4" fill="url(#bronzeTrim)"/>
  <rect x="{wx(55.5)}" y="{wy(10.8)}" width="{(70.0 - 55.5)*SCALE}" height="2" fill="#0f172a"/>
  <rect x="{wx(56.0)}" y="{wy(10.7)}" width="{(69.0 - 56.0)*SCALE}" height="7" fill="url(#woodSoffit)"/>
  <line x1="{wx(57.5)}" y1="{wy(10.3)}" x2="{wx(68.0)}" y2="{wy(10.3)}" stroke="#fde047" stroke-width="2.5" filter="url(#softGlow)"/>
</g>
''')

    # 9. GROUND FLOOR ARCHITECTURE (Z=0'-0" to 10'-6")
    svg.append(f'''
<!-- 9. GROUND FLOOR ARCHITECTURE (Z=0'-0" to 10'-6") -->
<!-- Ground Plinth Beam (+1'-6" FFL) across Main Building (X=36.125 to 85.125) -->
<rect x="{wx(XB_O)}" y="{wy(1.5)}" width="{(XE_O - XB_O)*SCALE}" height="{(1.5)*SCALE}" fill="#334155" stroke="#1e293b" stroke-width="2"/>
<line x1="{wx(XB_O)}" y1="{wy(1.5)}" x2="{wx(XE_O)}" y2="{wy(1.5)}" stroke="#94a3b8" stroke-width="2"/>
<text x="{wx(XB_O) + 10}" y="{wy(0.4)}" font-family="'Helvetica Neue', Arial, sans-serif" font-size="9" font-weight="bold" fill="#f8fafc">PLINTH BEAM (+1'-6" FFL)</text>

<!-- ============================================================== -->
<!-- 9A. MAIN LAWN (~500 SQ.FT OPEN GARDEN FRONTAGE, X=0 to 36.125) -->
<!-- ============================================================== -->
<g id="main-lawn-garden">
  <!-- Lush Lawn Green Groundcover -->
  <rect x="{wx(0.0)}" y="{wy(1.5)}" width="{(XB_O - 0.0)*SCALE}" height="{1.5*SCALE}" fill="url(#lawnGrassGrad)" stroke="#1e3a0f" stroke-width="1.5"/>

  <!-- Travertine Garden Pathway Stepping Stones -->
  <polygon points="{wx(4.0)},{wy(0.2)} {wx(8.0)},{wy(0.2)} {wx(7.5)},{wy(0.8)} {wx(3.5)},{wy(0.8)}" fill="#f1f5f9" stroke="#cbd5e1" stroke-width="1"/>
  <polygon points="{wx(10.0)},{wy(0.3)} {wx(15.0)},{wy(0.3)} {wx(14.5)},{wy(0.9)} {wx(9.5)},{wy(0.9)}" fill="#f1f5f9" stroke="#cbd5e1" stroke-width="1"/>
  <polygon points="{wx(18.0)},{wy(0.4)} {wx(23.5)},{wy(0.4)} {wx(23.0)},{wy(1.0)} {wx(17.5)},{wy(1.0)}" fill="#f1f5f9" stroke="#cbd5e1" stroke-width="1"/>
  <polygon points="{wx(26.0)},{wy(0.5)} {wx(32.0)},{wy(0.5)} {wx(31.5)},{wy(1.1)} {wx(25.5)},{wy(1.1)}" fill="#f1f5f9" stroke="#cbd5e1" stroke-width="1"/>

  <!-- Modern Architectural Planter Box & Low Shrubbery -->
  <rect x="{wx(2.0)}" y="{wy(3.0)}" width="{(14.0)*SCALE}" height="{1.5*SCALE}" rx="2" fill="#334155" stroke="#1e293b" stroke-width="1.5"/>
  <rect x="{wx(2.5)}" y="{wy(3.2)}" width="{(13.5)*SCALE}" height="{0.3*SCALE}" fill="#64748b"/>
  <circle cx="{wx(4.5)}" cy="{wy(4.0)}" r="16" fill="#15803d" opacity="0.85"/>
  <circle cx="{wx(8.0)}" cy="{wy(4.5)}" r="20" fill="#22c55e" opacity="0.8"/>
  <circle cx="{wx(11.5)}" cy="{wy(4.2)}" r="18" fill="#16a34a" opacity="0.85"/>
  <circle cx="{wx(14.5)}" cy="{wy(3.8)}" r="15" fill="#4ade80" opacity="0.75"/>

  <!-- Feature Architectural Garden Birch / Tree -->
  <path d="M {wx(26.0)},{wy(1.5)} Q {wx(25.0)},{wy(6.0)} {wx(24.0)},{wy(11.0)} Q {wx(23.5)},{wy(14.5)} {wx(22.0)},{wy(17.0)}" fill="none" stroke="#292524" stroke-width="3" stroke-linecap="round"/>
  <path d="M {wx(24.5)},{wy(9.0)} Q {wx(26.5)},{wy(12.0)} {wx(28.5)},{wy(14.5)}" fill="none" stroke="#292524" stroke-width="2" stroke-linecap="round"/>
  <circle cx="{wx(22.0)}" cy="{wy(17.0)}" r="24" fill="#4d7c0f" opacity="0.6"/>
  <circle cx="{wx(24.5)}" cy="{wy(18.5)}" r="28" fill="#65a30d" opacity="0.7"/>
  <circle cx="{wx(28.5)}" cy="{wy(15.0)}" r="22" fill="#4d7c0f" opacity="0.65"/>

  <text x="{wx(18.0)}" y="{wy(2.2)}" font-family="'Helvetica Neue', Arial, sans-serif" font-size="11" font-weight="bold" fill="#f8fafc" text-anchor="middle">MAIN LAWN (~500 SQ.FT OPEN GARDEN)</text>
</g>

<!-- ============================================================== -->
<!-- 9B. BEDROOM 2 FAÇADE (X=36.125 to 51.375)                      -->
<!-- ============================================================== -->
<rect x="{wx(XB_O)}" y="{wy(10.5)}" width="{(XC_W - XB_O)*SCALE}" height="{(10.5 - 1.5)*SCALE}" fill="url(#travertineSkin)" stroke="#78350f" stroke-width="1.8"/>
<rect x="{wx(XB_O)}" y="{wy(10.5)}" width="{(XC_W - XB_O)*SCALE}" height="{(10.5 - 1.5)*SCALE}" fill="url(#travertineJoints)" opacity="0.65"/>

<!-- Expansive Bedroom 2 Sliding Glass Garden Door (X=39.5 to 48.0, 8.5' x 7') -->
<rect x="{wx(39.5) - 4}" y="{wy(8.5) - 4}" width="{(48.0 - 39.5)*SCALE + 8}" height="{(8.5 - 1.5)*SCALE + 8}" rx="2" fill="#0f172a" stroke="#020617" stroke-width="2.5"/>
<rect x="{wx(39.5)}" y="{wy(8.5)}" width="{(48.0 - 39.5)*SCALE}" height="{(8.5 - 1.5)*SCALE}" fill="url(#interiorWarmGlow)"/>
<rect x="{wx(39.5)}" y="{wy(8.5)}" width="{(48.0 - 39.5)*SCALE}" height="{(8.5 - 1.5)*SCALE}" fill="url(#glassReflection)"/>
<line x1="{wx(43.75)}" y1="{wy(8.5)}" x2="{wx(43.75)}" y2="{wy(1.5)}" stroke="#0f172a" stroke-width="3"/>
<rect x="{wx(39.5) - 6}" y="{wy(1.5)}" width="{(48.0 - 39.5)*SCALE + 12}" height="6" rx="1.5" fill="#decfae" stroke="#78350f" stroke-width="1"/>

<!-- ============================================================== -->
<!-- 9C. BED-2 BATH & DRESS FAÇADE (X=51.375 to 56.625)             -->
<!-- ============================================================== -->
<rect x="{wx(XC_W)}" y="{wy(10.5)}" width="{(XC_P_W - XC_W)*SCALE}" height="{(10.5 - 1.5)*SCALE}" fill="url(#travertineSkin)" stroke="#78350f" stroke-width="1.5"/>
<line x1="{wx(54.0)}" y1="{wy(10.5)}" x2="{wx(54.0)}" y2="{wy(1.5)}" stroke="#78350f" stroke-width="1.5" stroke-dasharray="8,4"/>

<!-- ============================================================== -->
<!-- 9D. CENTRAL CAR PORCH & MAIN ENTRANCE (X=56.625 to 68.625)     -->
<!-- ============================================================== -->
<!-- Structural Pilasters at Grid C' and D -->
<rect x="{wx(XC_P_W)}" y="{wy(10.5)}" width="15" height="{(10.5 - 1.5)*SCALE}" fill="#1e293b" stroke="#0f172a" stroke-width="2"/>
<rect x="{wx(XD_W) - 15}" y="{wy(10.5)}" width="15" height="{(10.5 - 1.5)*SCALE}" fill="#1e293b" stroke="#0f172a" stroke-width="2"/>

<!-- Driveway Pavers Ramp under Porch -->
<polygon points="{wx(55.5)},{wy(0.0)} {wx(69.5)},{wy(0.0)} {wx(68.625)},{wy(1.5)} {wx(56.625)},{wy(1.5)}" fill="#e2e8f0" stroke="#cbd5e1" stroke-width="1"/>

<!-- Rear Entrance Wall Backdrop (Y=20.5) -->
<rect x="{wx(XC_P_W) + 15}" y="{wy(10.5)}" width="{(XD_W - XC_P_W)*SCALE - 30}" height="{(10.5 - 1.5)*SCALE}" fill="url(#stuccoWall)" stroke="#334155" stroke-width="1"/>

<!-- GRAND 6'-0" DOUBLE WALNUT PIVOT ENTRANCE DOOR (X=59.5 to 65.5, Height 8.5') -->
<g id="grand-entrance-door">
  <rect x="{wx(59.5)}" y="{wy(10.0)}" width="{(65.5 - 59.5)*SCALE}" height="{(10.0 - 1.5)*SCALE}" fill="#0f172a" stroke="#000" stroke-width="2"/>
  <rect x="{wx(59.7)}" y="{wy(9.8)}" width="{(65.1 - 59.5)*SCALE}" height="{(9.6 - 1.5)*SCALE}" fill="url(#woodSoffit)"/>
  <line x1="{wx(62.5)}" y1="{wy(9.8)}" x2="{wx(62.5)}" y2="{wy(1.7)}" stroke="#451a03" stroke-width="2.5"/>
  <!-- Bronze Vertical Pull Handles -->
  <rect x="{wx(62.2)}" y="{wy(6.5)}" width="4" height="{(6.5 - 3.5)*SCALE}" rx="2" fill="#fbbf24" stroke="#d97706" stroke-width="1"/>
  <rect x="{wx(62.8)}" y="{wy(6.5)}" width="4" height="{(6.5 - 3.5)*SCALE}" rx="2" fill="#fbbf24" stroke="#d97706" stroke-width="1"/>
  <!-- Ambient Sconce / Porch Pendant Glow -->
  <circle cx="{wx(62.5)}" cy="{wy(10.2)}" r="10" fill="#fef08a" filter="url(#softGlow)"/>
</g>
''')

    # SINGLE LUXURY VEHICLE PARKED IN CENTRAL CAR PORCH (REAR VIEW)
    c_x = wx(62.6) # Porch center
    car_base_y = wy(1.5)

    svg.append(f'''
<!-- LUXURY EXECUTIVE SUV IN CENTRAL CAR PORCH (REAR VIEW) -->
<g id="luxury-suv-carporch" filter="url(#crispShadow)">
  <rect x="{c_x - 56}" y="{car_base_y - 28}" width="20" height="28" rx="4" fill="#0f172a"/>
  <rect x="{c_x + 36}" y="{car_base_y - 28}" width="20" height="28" rx="4" fill="#0f172a"/>
  <line x1="{c_x - 56}" y1="{car_base_y - 8}" x2="{c_x - 36}" y2="{car_base_y - 8}" stroke="#334155" stroke-width="2"/>
  <line x1="{c_x + 36}" y1="{car_base_y - 8}" x2="{c_x + 56}" y2="{car_base_y - 8}" stroke="#334155" stroke-width="2"/>
  <rect x="{c_x - 52}" y="{car_base_y - 24}" width="104" height="18" rx="3" fill="#0f172a"/>
  <rect x="{c_x - 48}" y="{car_base_y - 18}" width="16" height="8" rx="3" fill="#cbd5e1" stroke="#475569" stroke-width="1"/>
  <rect x="{c_x + 32}" y="{car_base_y - 18}" width="16" height="8" rx="3" fill="#cbd5e1" stroke="#475569" stroke-width="1"/>
  <path d="M {c_x - 60},{car_base_y - 20} Q {c_x - 62},{car_base_y - 52} {c_x - 56},{car_base_y - 62} L {c_x + 56},{car_base_y - 62} Q {c_x + 62},{car_base_y - 52} {c_x + 60},{car_base_y - 20} Z" fill="url(#suvBody)" stroke="#0f172a" stroke-width="1.5"/>
  <rect x="{c_x - 22}" y="{car_base_y - 45}" width="44" height="18" rx="2" fill="#0f172a"/>
  <rect x="{c_x - 20}" y="{car_base_y - 43}" width="40" height="14" rx="1.5" fill="#f8fafc" stroke="#94a3b8" stroke-width="0.75"/>
  <text x="{c_x}" y="{car_base_y - 32}" font-family="'Helvetica Neue', Arial, sans-serif" font-size="8" font-weight="900" fill="#0f172a" text-anchor="middle" letter-spacing="1">ISB - 777</text>
  <rect x="{c_x - 54}" y="{car_base_y - 64}" width="108" height="8" rx="3" fill="url(#redLightbar)" filter="url(#tailLightGlow)"/>
  <circle cx="{c_x - 48}" cy="{car_base_y - 60}" r="2.5" fill="#fef2f2"/>
  <circle cx="{c_x + 48}" cy="{car_base_y - 60}" r="2.5" fill="#fef2f2"/>
  <path d="M {c_x - 52},{car_base_y - 64} L {c_x - 40},{car_base_y - 104} L {c_x + 40},{car_base_y - 104} L {c_x + 52},{car_base_y - 64} Z" fill="#090d16" stroke="#0f172a" stroke-width="1.5"/>
  <polygon points="{c_x - 36},{car_base_y - 100} {c_x - 10},{car_base_y - 100} {c_x + 8},{car_base_y - 68} {c_x - 18},{car_base_y - 68}" fill="#38bdf8" opacity="0.35"/>
  <rect x="{c_x - 16}" y="{car_base_y - 103}" width="32" height="3" rx="1" fill="#ef4444"/>
  <rect x="{c_x - 43}" y="{car_base_y - 108}" width="86" height="6" rx="2" fill="#1e293b"/>
  <ellipse cx="{c_x - 58}" cy="{car_base_y - 74}" rx="7" ry="4" fill="#334155" stroke="#0f172a" stroke-width="1"/>
  <ellipse cx="{c_x + 58}" cy="{car_base_y - 74}" rx="7" ry="4" fill="#334155" stroke="#0f172a" stroke-width="1"/>
</g>
''')

    # ==============================================================
    # 9E. DRAWING ROOM FAÇADE (X=68.625 to 84.375)
    # ==============================================================
    dr_wall_x0 = wx(XD_W)
    dr_wall_w = (XE_O - XD_W) * SCALE
    win_dr_x0 = wx(72.0)
    win_dr_w = (81.0 - 72.0) * SCALE # 9' x 6'-6"
    win_dr_y0 = wy(8.5)
    win_dr_h = (8.5 - 2.0) * SCALE

    svg.append(f'''
<!-- 9E. DRAWING ROOM FAÇADE & GRAND PICTURE WINDOW (X=68'-7½" to 85'-1½") -->
<rect x="{dr_wall_x0}" y="{wy(10.5)}" width="{dr_wall_w}" height="{(10.5 - 1.5)*SCALE}" fill="url(#stuccoWall)" stroke="#334155" stroke-width="2"/>
<line x1="{dr_wall_x0}" y1="{wy(4.0)}" x2="{dr_wall_x0 + dr_wall_w}" y2="{wy(4.0)}" stroke="#cbd5e1" stroke-width="1.5"/>
<line x1="{dr_wall_x0}" y1="{wy(7.0)}" x2="{dr_wall_x0 + dr_wall_w}" y2="{wy(7.0)}" stroke="#cbd5e1" stroke-width="1.5"/>

<!-- Grand Drawing Room Window W2 (X=72.0 to 81.0, 9'x6'-6") -->
<rect x="{win_dr_x0 - 4}" y="{win_dr_y0 - 4}" width="{win_dr_w + 8}" height="{win_dr_h + 8}" rx="2" fill="#0f172a" stroke="#020617" stroke-width="2.5"/>
<rect x="{win_dr_x0}" y="{win_dr_y0}" width="{win_dr_w}" height="{win_dr_h}" fill="url(#interiorWarmGlow)"/>
<rect x="{win_dr_x0}" y="{win_dr_y0}" width="{win_dr_w}" height="{win_dr_h}" fill="url(#glassReflection)"/>

<!-- Chandelier Warm Ambient Glow -->
<circle cx="{win_dr_x0 + win_dr_w*0.5}" cy="{win_dr_y0 + 32}" r="16" fill="#fef08a" opacity="0.8" filter="url(#softGlow)"/>
<circle cx="{win_dr_x0 + win_dr_w*0.5}" cy="{win_dr_y0 + 32}" r="6" fill="#d97706"/>
<line x1="{win_dr_x0 + win_dr_w*0.5}" y1="{win_dr_y0}" x2="{win_dr_x0 + win_dr_w*0.5}" y2="{win_dr_y0 + 26}" stroke="#78350f" stroke-width="2"/>

<!-- Elegant Sheer Drapes & Mullions -->
<rect x="{win_dr_x0}" y="{win_dr_y0}" width="18" height="{win_dr_h}" fill="#fef3c7" opacity="0.5"/>
<rect x="{win_dr_x0 + win_dr_w - 18}" y="{win_dr_y0}" width="18" height="{win_dr_h}" fill="#fef3c7" opacity="0.5"/>
<line x1="{win_dr_x0 + win_dr_w * 0.5}" y1="{win_dr_y0}" x2="{win_dr_x0 + win_dr_w * 0.5}" y2="{win_dr_y0 + win_dr_h}" stroke="#0f172a" stroke-width="3"/>
<rect x="{win_dr_x0 - 6}" y="{win_dr_y0 + win_dr_h}" width="{win_dr_w + 12}" height="6" rx="1.5" fill="#cbd5e1" stroke="#64748b" stroke-width="1"/>

<!-- ============================================================== -->
<!-- 9F. EAST PASSAGE REVEAL & SECURITY GATE (X=85.125 to 87.21)    -->
<!-- ============================================================== -->
<g id="east-passage-reveal">
  <!-- Slim Stone Fin at Edge of Main Block -->
  <rect x="{wx(XE_O)}" y="{wy(10.5)}" width="{0.35*SCALE}" height="{(10.5 - 1.5)*SCALE}" fill="#334155" stroke="#0f172a" stroke-width="1.5"/>
  <!-- Recessed Slatted Bronze/Timber Security Gate (Height +6'-0") -->
  <rect x="{wx(XE_O) + 7}" y="{wy(6.0)}" width="{(87.21 - XE_O)*SCALE - 7}" height="{6.0*SCALE}" fill="url(#passageGateSlats)" stroke="#0f172a" stroke-width="1.2"/>
  <rect x="{wx(XE_O) + 5}" y="{wy(6.2)}" width="{(87.21 - XE_O)*SCALE - 3}" height="4" fill="#0f172a"/>
</g>
''')

    # HUMAN SCALE FIGURES
    svg.append(f'''
<!-- 10. HUMAN SCALE FIGURES -->
<g id="human-scale-figures" opacity="0.85">
  <circle cx="{wx(70.5)}" cy="{wy(6.0)}" r="5.5" fill="#0f172a"/>
  <path d="M {wx(70.5)},{wy(5.6)} L {wx(70.5)},{wy(2.8)} L {wx(69.8)},{wy(0.0)}" stroke="#0f172a" stroke-width="3.5" stroke-linecap="round"/>
  <line x1="{wx(70.5)}" y1="{wy(2.8)}" x2="{wx(71.2)}" y2="{wy(0.0)}" stroke="#0f172a" stroke-width="3.5" stroke-linecap="round"/>
  <circle cx="{wx(72.0)}" cy="{wy(5.6)}" r="5" fill="#334155"/>
  <path d="M {wx(72.0)},{wy(5.2)} L {wx(72.0)},{wy(2.6)} L {wx(71.4)},{wy(0.0)}" stroke="#334155" stroke-width="3" stroke-linecap="round"/>
  <line x1="{wx(72.0)}" y1="{wy(2.6)}" x2="{wx(72.6)}" y2="{wy(0.0)}" stroke="#334155" stroke-width="3" stroke-linecap="round"/>
</g>
''')

    # 11. ARCHITECTURAL LEVEL DATUMS
    levels = [
        ("FINISHED GROUND LEVEL", "±0'-0\"", 0.0),
        ("PLINTH FINISHED LEVEL", "+1'-6\"", 1.5),
        ("FIRST FLOOR FFL", "+11'-10\"", 11.833),
        ("SECOND FLOOR FFL", "+22'-2\"", 22.167),
        ("2F ROOF CANOPY LEVEL", "+32'-6\"", 32.5),
        ("TOP OF MUMTY CORE & TANK", "+42'-0\"", 42.0),
    ]

    svg.append('<!-- 11. ARCHITECTURAL LEVEL DATUMS -->\n')
    for name, fi_txt, z_val in levels:
        ly = wy(z_val)
        svg.append(f'''
<line x1="60" y1="{ly}" x2="{wx(92)}" y2="{ly}" stroke="#94a3b8" stroke-width="0.75" stroke-dasharray="6,4"/>
<circle cx="110" cy="{ly}" r="12" fill="#ffffff" stroke="#0f172a" stroke-width="1.5"/>
<path d="M 98,{ly} A 12,12 0 0,0 110,{ly-12} L 110,{ly} Z" fill="#0f172a"/>
<path d="M 110,{ly} A 12,12 0 0,0 122,{ly+12} L 110,{ly} Z" fill="#0f172a"/>
<text x="135" y="{ly - 3}" font-family="'Helvetica Neue', Arial, sans-serif" font-size="11" font-weight="bold" fill="#0f172a">{name}</text>
<text x="135" y="{ly + 11}" font-family="'Helvetica Neue', Arial, sans-serif" font-size="10" font-weight="600" fill="#475569">{fi_txt}</text>
''')

    # 12. MATERIAL SPECIFICATION CALLOUTS
    callouts = [
        ("01. CENTRAL STAIRCASE MUMTY TOWER & WATER TANK (+42'-0\") [GRID C'-D]", wx(63.0), wy(42.0), wx(50.0), wy(46.0)),
        ("02. SECOND FLOOR WEST SUN TERRACE WITH 12mm TEMPERED GLASS RAILING", wx(44.0), wy(25.6), wx(28.0), wy(29.0)),
        ("03. FIRST FLOOR OPEN FRONT SUN TERRACE / BALCONY OVER CAR PORCH", wx(62.5), wy(15.3), wx(52.0), wy(18.5)),
        ("04. 14\" ANODIZED CHARCOAL BRONZE PORCH CANOPY WITH WARM LED LIGHTING", wx(58.0), wy(11.8), wx(46.0), wy(14.0)),
        ("05. BEDROOM 2 SLIDING GLASS DOOR TO MAIN LAWN (8'-6\" x 7'-0\")", wx(44.0), wy(8.0), wx(35.0), wy(4.5)),
        ("06. CENTRAL CAR PORCH (11'-3\" x 20'-6\") WITH 6'-0\" DOUBLE MAIN ENTRANCE DOOR", wx(62.5), wy(3.5), wx(62.5), wy(0.5)),
        ("07. FORMAL DRAWING ROOM SOUTH PICTURE WINDOW W2 (9'-0\" x 6'-6\")", wx(76.5), wy(8.0), wx(76.5), wy(4.5)),
        ("08. MAIN LAWN FRONTAGE (~500 SQ.FT OPEN LANDSCAPED GARDEN)", wx(18.0), wy(1.5), wx(14.0), wy(-1.0)),
        ("09. EAST PERIMETER PASSAGE REVEAL (2'-1\" CLEAR) WITH SLATTED BRONZE GATE", wx(86.0), wy(5.0), wx(88.0), wy(1.5)),
    ]

    svg.append('<!-- 12. MATERIAL SPECIFICATION LEADER LINES -->\n')
    for text, ax, ay, tx, ty in callouts:
        svg.append(f'''
<circle cx="{ax}" cy="{ay}" r="3.5" fill="#e11d48"/>
<polyline points="{ax},{ay} {tx},{ty} {tx + (180 if tx >= ax else -180)},{ty}" fill="none" stroke="#e11d48" stroke-width="1.2"/>
<text x="{tx + (10 if tx >= ax else -10)}" y="{ty - 5}" font-family="'Helvetica Neue', Arial, sans-serif" font-size="10" font-weight="bold" fill="#0f172a" text-anchor="{'start' if tx >= ax else 'end'}">{text}</text>
''')

    # 13. OVERALL DIMENSIONS ACROSS 87'-11" FRONTAGE
    dim_y = wy(-4.5)
    svg.append(f'''
<!-- 13. OVERALL DIMENSIONS & SETBACK SPANS -->
<line x1="{wx(0.0)}" y1="{dim_y}" x2="{wx(87.917)}" y2="{dim_y}" stroke="#0f172a" stroke-width="1.5"/>
<line x1="{wx(0.0)}" y1="{dim_y - 12}" x2="{wx(0.0)}" y2="{dim_y + 12}" stroke="#0f172a" stroke-width="2"/>
<line x1="{wx(87.917)}" y1="{dim_y - 12}" x2="{wx(87.917)}" y2="{dim_y + 12}" stroke="#0f172a" stroke-width="2"/>
<line x1="{wx(0.0)-6}" y1="{dim_y+6}" x2="{wx(0.0)+6}" y2="{dim_y-6}" stroke="#0f172a" stroke-width="2.5"/>
<line x1="{wx(87.917)-6}" y1="{dim_y+6}" x2="{wx(87.917)+6}" y2="{dim_y-6}" stroke="#0f172a" stroke-width="2.5"/>
<rect x="{wx(44.0)-140}" y="{dim_y-14}" width="280" height="26" fill="#ffffff" stroke="#cbd5e1" stroke-width="1" rx="4"/>
<text x="{wx(44.0)}" y="{dim_y+4}" font-family="'Helvetica Neue', Arial, sans-serif" font-size="14" font-weight="bold" fill="#0f172a" text-anchor="middle">OVERALL PLOT FRONTAGE = 87'-11" (26.80 m)</text>

<!-- Bay Sub-Dimensions -->
<line x1="{wx(0.0)}" y1="{dim_y + 26}" x2="{wx(XB_O)}" y2="{dim_y + 26}" stroke="#475569" stroke-width="1.2"/>
<line x1="{wx(0.0)-4}" y1="{dim_y + 30}" x2="{wx(0.0)+4}" y2="{dim_y + 22}" stroke="#475569" stroke-width="2"/>
<line x1="{wx(XB_O)-4}" y1="{dim_y + 30}" x2="{wx(XB_O)+4}" y2="{dim_y + 22}" stroke="#475569" stroke-width="2"/>
<text x="{wx((0.0 + XB_O)/2)}" y="{dim_y + 40}" font-family="'Helvetica Neue', Arial, sans-serif" font-size="11" font-weight="bold" fill="#334155" text-anchor="middle">MAIN LAWN: 36'-1\u00bd"</text>

<line x1="{wx(XB_O)}" y1="{dim_y + 26}" x2="{wx(XC_W)}" y2="{dim_y + 26}" stroke="#475569" stroke-width="1.2"/>
<line x1="{wx(XC_W)-4}" y1="{dim_y + 30}" x2="{wx(XC_W)+4}" y2="{dim_y + 22}" stroke="#475569" stroke-width="2"/>
<text x="{wx((XB_O + XC_W)/2)}" y="{dim_y + 40}" font-family="'Helvetica Neue', Arial, sans-serif" font-size="11" font-weight="bold" fill="#334155" text-anchor="middle">BEDROOM 2: 15'-3"</text>

<line x1="{wx(XC_W)}" y1="{dim_y + 26}" x2="{wx(XC_P_W)}" y2="{dim_y + 26}" stroke="#475569" stroke-width="1.2"/>
<line x1="{wx(XC_P_W)-4}" y1="{dim_y + 30}" x2="{wx(XC_P_W)+4}" y2="{dim_y + 22}" stroke="#475569" stroke-width="2"/>
<text x="{wx((XC_W + XC_P_W)/2)}" y="{dim_y + 40}" font-family="'Helvetica Neue', Arial, sans-serif" font-size="10" font-weight="bold" fill="#334155" text-anchor="middle">BATH: 5'-3"</text>

<line x1="{wx(XC_P_W)}" y1="{dim_y + 26}" x2="{wx(XD_W)}" y2="{dim_y + 26}" stroke="#475569" stroke-width="1.2"/>
<line x1="{wx(XD_W)-4}" y1="{dim_y + 30}" x2="{wx(XD_W)+4}" y2="{dim_y + 22}" stroke="#475569" stroke-width="2"/>
<text x="{wx((XC_P_W + XD_W)/2)}" y="{dim_y + 40}" font-family="'Helvetica Neue', Arial, sans-serif" font-size="11" font-weight="bold" fill="#334155" text-anchor="middle">CAR PORCH: 12'-0"</text>

<line x1="{wx(XD_W)}" y1="{dim_y + 26}" x2="{wx(XE_O)}" y2="{dim_y + 26}" stroke="#475569" stroke-width="1.2"/>
<line x1="{wx(XE_O)-4}" y1="{dim_y + 30}" x2="{wx(XE_O)+4}" y2="{dim_y + 22}" stroke="#475569" stroke-width="2"/>
<text x="{wx((XD_W + XE_O)/2)}" y="{dim_y + 40}" font-family="'Helvetica Neue', Arial, sans-serif" font-size="11" font-weight="bold" fill="#334155" text-anchor="middle">DRAWING: 15'-9"</text>

<line x1="{wx(XE_O)}" y1="{dim_y + 26}" x2="{wx(87.21)}" y2="{dim_y + 26}" stroke="#475569" stroke-width="1.2"/>
<line x1="{wx(87.21)-4}" y1="{dim_y + 30}" x2="{wx(87.21)+4}" y2="{dim_y + 22}" stroke="#475569" stroke-width="2"/>
<text x="{wx((XE_O + 87.21)/2)}" y="{dim_y + 40}" font-family="'Helvetica Neue', Arial, sans-serif" font-size="10" font-weight="bold" fill="#334155" text-anchor="middle">PASSAGE: 2'-1"</text>
''')

    # 14. PRESENTATION TITLE BLOCK
    tb_x0, tb_y0 = 1720, 1320
    tb_w, tb_h = 640, 140
    svg.append(f'''
<!-- 14. PRESENTATION TITLE BLOCK -->
<g filter="url(#crispShadow)">
  <rect x="{tb_x0}" y="{tb_y0}" width="{tb_w}" height="{tb_h}" rx="8" fill="#0f172a" stroke="#1e293b" stroke-width="2"/>
  <rect x="{tb_x0+4}" y="{tb_y0+4}" width="{tb_w-8}" height="32" rx="4" fill="#1e293b"/>
  <text x="{tb_x0+16}" y="{tb_y0+25}" font-family="'Helvetica Neue', Arial, sans-serif" font-size="13" font-weight="bold" fill="#f8fafc" letter-spacing="1.5">RESIDENCE FOR MR. DAATA HAMLET</text>
  <text x="{tb_x0+tb_w-16}" y="{tb_y0+25}" font-family="'Helvetica Neue', Arial, sans-serif" font-size="11" font-weight="bold" fill="#f59e0b" text-anchor="end">{version_badge}</text>
  <text x="{tb_x0+16}" y="{tb_y0+58}" font-family="'Helvetica Neue', Arial, sans-serif" font-size="15" font-weight="800" fill="#ffffff" letter-spacing="0.5">{sheet_title}</text>
  <text x="{tb_x0+16}" y="{tb_y0+78}" font-family="'Helvetica Neue', Arial, sans-serif" font-size="11" font-weight="500" fill="#94a3b8">ARCHITECTURAL TENDER DRAWING | MASTER 3-STOREY CANOPY RESIDENCE | SCALE 1:50</text>
  <line x1="{tb_x0+16}" y1="{tb_y0+90}" x2="{tb_x0+tb_w-16}" y2="{tb_y0+90}" stroke="#334155" stroke-width="1"/>
  <text x="{tb_x0+16}" y="{tb_y0+106}" font-family="'Helvetica Neue', Arial, sans-serif" font-size="10" font-weight="bold" fill="#64748b">SHEET NO:</text>
  <text x="{tb_x0+80}" y="{tb_y0+106}" font-family="'Helvetica Neue', Arial, sans-serif" font-size="11" font-weight="bold" fill="#38bdf8">{sheet_no}</text>
  <text x="{tb_x0+160}" y="{tb_y0+106}" font-family="'Helvetica Neue', Arial, sans-serif" font-size="10" font-weight="bold" fill="#64748b">SCALE:</text>
  <text x="{tb_x0+210}" y="{tb_y0+106}" font-family="'Helvetica Neue', Arial, sans-serif" font-size="11" font-weight="bold" fill="#f8fafc">1/4" = 1'-0" (1:50)</text>
  <text x="{tb_x0+340}" y="{tb_y0+106}" font-family="'Helvetica Neue', Arial, sans-serif" font-size="10" font-weight="bold" fill="#64748b">PLOT AREA:</text>
  <text x="{tb_x0+415}" y="{tb_y0+106}" font-family="'Helvetica Neue', Arial, sans-serif" font-size="11" font-weight="bold" fill="#f8fafc">3,129.1 SQ.FT (12.8 MARLA)</text>
  <text x="{tb_x0+16}" y="{tb_y0+124}" font-family="'Helvetica Neue', Arial, sans-serif" font-size="10" font-weight="bold" fill="#64748b">PROJECT:</text>
  <text x="{tb_x0+75}" y="{tb_y0+124}" font-family="'Helvetica Neue', Arial, sans-serif" font-size="11" font-weight="bold" fill="#f8fafc">CANOPY VILLA (GF + 1F + 2F + MUMTY)</text>
  <text x="{tb_x0+330}" y="{tb_y0+124}" font-family="'Helvetica Neue', Arial, sans-serif" font-size="10" font-weight="bold" fill="#64748b">STATUS:</text>
  <text x="{tb_x0+385}" y="{tb_y0+124}" font-family="'Helvetica Neue', Arial, sans-serif" font-size="11" font-weight="bold" fill="#4ade80">ISSUED FOR CONSTRUCTION</text>
</g>

<!-- Compass North -->
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


def export_all():
    svg_with_bw = render_elevation_svg(with_boundary_wall=True)
    svg_without_bw = render_elevation_svg(with_boundary_wall=False)

    paths = {
        "with_bw_svg": BLUEPRINTS_DIR / "daata_hamlet_elevation_with_boundary_wall.svg",
        "without_bw_svg": BLUEPRINTS_DIR / "daata_hamlet_elevation_without_boundary_wall.svg",
        "default_svg": BLUEPRINTS_DIR / "06_front_south_elevation.svg",
        "default_luxury_svg": BLUEPRINTS_DIR / "daata_hamlet_luxury_canopy_elevation.svg",

        "artifact_with_bw_svg": BRAIN_DIR / "daata_hamlet_elevation_with_boundary_wall.svg",
        "artifact_without_bw_svg": BRAIN_DIR / "daata_hamlet_elevation_without_boundary_wall.svg",
        "artifact_default_svg": BRAIN_DIR / "06_front_south_elevation.svg",
        "artifact_default_luxury_svg": BRAIN_DIR / "daata_hamlet_luxury_canopy_elevation.svg",

        "with_bw_png": BLUEPRINTS_DIR / "daata_hamlet_elevation_with_boundary_wall.png",
        "without_bw_png": BLUEPRINTS_DIR / "daata_hamlet_elevation_without_boundary_wall.png",
        "artifact_with_bw_png": BRAIN_DIR / "daata_hamlet_elevation_with_boundary_wall.png",
        "artifact_without_bw_png": BRAIN_DIR / "daata_hamlet_elevation_without_boundary_wall.png",
        "artifact_default_png": BRAIN_DIR / "06_front_south_elevation.png",
        "artifact_default_luxury_png": BRAIN_DIR / "daata_hamlet_luxury_canopy_elevation.png",
    }

    # Save SVGs
    paths["with_bw_svg"].parent.mkdir(parents=True, exist_ok=True)
    paths["with_bw_svg"].write_text(svg_with_bw, encoding="utf-8")
    paths["artifact_with_bw_svg"].write_text(svg_with_bw, encoding="utf-8")
    paths["default_svg"].write_text(svg_with_bw, encoding="utf-8")
    paths["artifact_default_svg"].write_text(svg_with_bw, encoding="utf-8")
    paths["default_luxury_svg"].write_text(svg_with_bw, encoding="utf-8")
    paths["artifact_default_luxury_svg"].write_text(svg_with_bw, encoding="utf-8")

    paths["without_bw_svg"].write_text(svg_without_bw, encoding="utf-8")
    paths["artifact_without_bw_svg"].write_text(svg_without_bw, encoding="utf-8")

    print("[+] Saved all updated SVG elevation files successfully.")

    # Render PNGs via Playwright
    with sync_playwright() as pw:
        browser = pw.chromium.launch()
        page = browser.new_page(viewport={"width": 2400, "height": 1500})

        temp_html_1 = WORKSPACE / "temp_with_bw.html"
        temp_html_1.write_text(f'<!DOCTYPE html><html><body style="margin:0;padding:0;overflow:hidden;background:#fff;">{svg_with_bw}</body></html>', encoding="utf-8")
        page.goto(temp_html_1.resolve().as_uri(), wait_until="load")
        page.screenshot(path=str(paths["with_bw_png"]), timeout=8000)
        page.screenshot(path=str(paths["artifact_with_bw_png"]), timeout=8000)
        page.screenshot(path=str(paths["artifact_default_png"]), timeout=8000)
        page.screenshot(path=str(paths["artifact_default_luxury_png"]), timeout=8000)
        temp_html_1.unlink()
        print("[+] Rendered WITH BOUNDARY WALL elevation PNG.")

        temp_html_2 = WORKSPACE / "temp_without_bw.html"
        temp_html_2.write_text(f'<!DOCTYPE html><html><body style="margin:0;padding:0;overflow:hidden;background:#fff;">{svg_without_bw}</body></html>', encoding="utf-8")
        page.goto(temp_html_2.resolve().as_uri(), wait_until="load")
        page.screenshot(path=str(paths["without_bw_png"]), timeout=8000)
        page.screenshot(path=str(paths["artifact_without_bw_png"]), timeout=8000)
        temp_html_2.unlink()
        print("[+] Rendered WITHOUT BOUNDARY WALL elevation PNG.")

        browser.close()

    print("[+] All updated dual elevations generated and snapshotted with 0 errors!")


if __name__ == "__main__":
    export_all()
