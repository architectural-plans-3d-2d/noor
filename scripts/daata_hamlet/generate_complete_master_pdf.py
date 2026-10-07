"""
DAATA HAMLET RESIDENCE - Complete Architectural Master Drawing Package PDF Generator
Compiles the complete architectural portfolio into a single, comprehensive, publication-grade PDF:
- Page 1: Sheet S-001 - Title Cover & Project Schedule (with 3D hero render & drawing index)
- Page 2: Sheet A-101 - Ground Floor Architectural Floor Plan
- Page 3: Sheet A-102 - First Floor Architectural Floor Plan
- Page 4: Sheet A-103 - Second Floor Architectural Floor Plan
- Page 5: Sheet A-104 - Roof & Mumty Architectural Plan
- Page 6: Sheet S-101 - Structural Column Grid & Continuity Layout
- Page 7: Sheet A-201A - South Front Elevation (With Boundary Wall in Background)
- Page 8: Sheet A-201B - South Front Elevation (Pure Architecture / Without Boundary Wall)
- Page 9: Sheet A-301 - 3D Architectural Perspectives & Photorealistic Cycles Renders

Formatted to international A3 Landscape (420 x 297 mm) standard architectural presentation layout.
"""
from __future__ import annotations
import base64
import pathlib
from playwright.sync_api import sync_playwright

WORKSPACE = pathlib.Path(__file__).parent.parent.parent.resolve()
ARTIFACT_DIR = pathlib.Path(r"C:\Users\adees\.gemini\antigravity\brain\754b2257-dc8d-4e91-8a73-3c0efba21f41")

def get_b64_image(path: pathlib.Path) -> str:
    ext = path.suffix.lower()
    mime = "image/png" if ext == ".png" else "image/svg+xml"
    data = base64.b64encode(path.read_bytes()).decode("ascii")
    return f"data:{mime};base64,{data}"

def generate_pdf():
    # Asset paths
    hero_render_path = WORKSPACE / "renders" / "daata_hamlet_canopy_cycles.png"
    aerial_render_path = WORKSPACE / "renders" / "daata_hamlet_canopy_aerial.png"
    elev_with_bw_path = WORKSPACE / "blueprints" / "daata_hamlet" / "daata_hamlet_elevation_with_boundary_wall.png"
    elev_without_bw_path = WORKSPACE / "blueprints" / "daata_hamlet" / "daata_hamlet_elevation_without_boundary_wall.png"

    gf_svg_path = WORKSPACE / "blueprints" / "daata_hamlet" / "01_ground_floor_plan.svg"
    f1_svg_path = WORKSPACE / "blueprints" / "daata_hamlet" / "02_first_floor_plan.svg"
    f2_svg_path = WORKSPACE / "blueprints" / "daata_hamlet" / "03_second_floor_plan.svg"
    rf_svg_path = WORKSPACE / "blueprints" / "daata_hamlet" / "04_roof_mumty_plan.svg"
    col_svg_path = WORKSPACE / "blueprints" / "daata_hamlet" / "05_column_grid_layout.svg"

    b64_hero = get_b64_image(hero_render_path)
    b64_aerial = get_b64_image(aerial_render_path)
    b64_elev_with_bw = get_b64_image(elev_with_bw_path)
    b64_elev_without_bw = get_b64_image(elev_without_bw_path)

    b64_gf = get_b64_image(gf_svg_path)
    b64_f1 = get_b64_image(f1_svg_path)
    b64_f2 = get_b64_image(f2_svg_path)
    b64_rf = get_b64_image(rf_svg_path)
    b64_col = get_b64_image(col_svg_path)

    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>DAATA HAMLET RESIDENCE — Complete Architectural Drawing Set</title>
  <style>
    @page {{
      size: 420mm 297mm; /* A3 Landscape */
      margin: 0;
    }}
    * {{
      box-sizing: border-box;
      margin: 0;
      padding: 0;
    }}
    body {{
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
      background: #0f172a;
      color: #1e293b;
      -webkit-print-color-adjust: exact;
      print-color-adjust: exact;
    }}
    .sheet {{
      width: 420mm;
      height: 297mm;
      position: relative;
      background: #ffffff;
      page-break-after: always;
      overflow: hidden;
      display: flex;
      flex-direction: column;
      padding: 12mm;
    }}
    .sheet-border {{
      position: absolute;
      top: 8mm;
      left: 8mm;
      right: 8mm;
      bottom: 8mm;
      border: 1.5pt solid #0f172a;
      pointer-events: none;
    }}
    .sheet-inner-border {{
      position: absolute;
      top: 9.5mm;
      left: 9.5mm;
      right: 9.5mm;
      bottom: 9.5mm;
      border: 0.5pt solid #94a3b8;
      pointer-events: none;
    }}

    /* Architectural Header */
    .arch-header {{
      display: flex;
      justify-content: space-between;
      align-items: flex-end;
      border-bottom: 2pt solid #0f172a;
      padding-bottom: 4mm;
      margin-bottom: 4mm;
    }}
    .proj-title h1 {{
      font-size: 18pt;
      font-weight: 800;
      letter-spacing: 1.5pt;
      color: #0f172a;
      text-transform: uppercase;
    }}
    .proj-title p {{
      font-size: 9pt;
      font-weight: 600;
      color: #64748b;
      letter-spacing: 0.5pt;
      margin-top: 1mm;
    }}
    .sheet-title-badge {{
      text-align: right;
    }}
    .sheet-title-badge h2 {{
      font-size: 14pt;
      font-weight: 800;
      color: #0369a1;
      letter-spacing: 0.8pt;
    }}
    .sheet-title-badge span {{
      font-size: 8.5pt;
      font-weight: 700;
      color: #64748b;
    }}

    /* Main Drawing Canvas Area */
    .drawing-stage {{
      flex: 1;
      display: flex;
      justify-content: center;
      align-items: center;
      position: relative;
      background: #f8fafc;
      border: 1pt solid #cbd5e1;
      overflow: hidden;
    }}
    .drawing-img {{
      max-width: 100%;
      max-height: 100%;
      object-fit: contain;
    }}

    /* Bottom Architectural Title Block */
    .arch-titleblock {{
      margin-top: 4mm;
      border-top: 1.5pt solid #0f172a;
      padding-top: 3mm;
      display: grid;
      grid-template-columns: 2fr 1.2fr 1.2fr 1fr 1.2fr;
      gap: 4mm;
      font-size: 7.5pt;
    }}
    .tb-cell {{
      display: flex;
      flex-direction: column;
      gap: 1mm;
      border-right: 0.5pt solid #cbd5e1;
      padding-right: 3mm;
    }}
    .tb-cell:last-child {{
      border-right: none;
      padding-right: 0;
    }}
    .tb-label {{
      font-weight: 700;
      color: #64748b;
      text-transform: uppercase;
      font-size: 6.5pt;
    }}
    .tb-val {{
      font-weight: 800;
      color: #0f172a;
    }}
    .tb-val.highlight {{
      color: #0284c7;
      font-size: 10pt;
    }}

    /* Page 1 Cover Sheet Specific */
    .cover-body {{
      flex: 1;
      display: grid;
      grid-template-columns: 1.25fr 1fr;
      gap: 8mm;
      padding-top: 4mm;
    }}
    .cover-render-box {{
      border: 1pt solid #cbd5e1;
      border-radius: 4pt;
      overflow: hidden;
      background: #0f172a;
      display: flex;
      flex-direction: column;
    }}
    .cover-render-img {{
      width: 100%;
      height: 100%;
      object-fit: cover;
    }}
    .cover-info-panel {{
      display: flex;
      flex-direction: column;
      justify-content: space-between;
    }}
    .meta-table {{
      width: 100%;
      border-collapse: collapse;
      font-size: 8.5pt;
      margin-top: 3mm;
    }}
    .meta-table th, .meta-table td {{
      padding: 2.5mm 3mm;
      border: 0.5pt solid #cbd5e1;
      text-align: left;
    }}
    .meta-table th {{
      background: #f1f5f9;
      color: #475569;
      font-weight: 700;
      width: 40%;
    }}
    .meta-table td {{
      font-weight: 700;
      color: #0f172a;
    }}
    .index-table {{
      width: 100%;
      border-collapse: collapse;
      font-size: 8pt;
      margin-top: 4mm;
    }}
    .index-table th, .index-table td {{
      padding: 2mm 3mm;
      border: 0.5pt solid #cbd5e1;
      text-align: left;
    }}
    .index-table th {{
      background: #0f172a;
      color: #ffffff;
      font-weight: 700;
    }}
    .index-table tr:nth-child(even) {{
      background: #f8fafc;
    }}

    /* Page 9 3D Studies Grid */
    .studies-grid {{
      flex: 1;
      display: grid;
      grid-template-columns: 1.2fr 1fr;
      gap: 6mm;
      height: 100%;
    }}
    .render-card {{
      background: #0f172a;
      border: 1pt solid #cbd5e1;
      display: flex;
      flex-direction: column;
      overflow: hidden;
      position: relative;
    }}
    .render-card img {{
      width: 100%;
      height: 88%;
      object-fit: cover;
    }}
    .render-card-caption {{
      padding: 3mm 4mm;
      background: #ffffff;
      border-top: 1pt solid #cbd5e1;
      font-size: 8pt;
      font-weight: 700;
      color: #0f172a;
      display: flex;
      justify-content: space-between;
    }}
  </style>
</head>
<body>

  <!-- ====================================================================== -->
  <!-- PAGE 1: SHEET S-001 - COVER & PROJECT PORTFOLIO SCHEDULE -->
  <!-- ====================================================================== -->
  <div class="sheet">
    <div class="sheet-border"></div>
    <div class="sheet-inner-border"></div>

    <div class="arch-header">
      <div class="proj-title">
        <h1>DAATA HAMLET RESIDENCE</h1>
        <p>ARCHITECTURAL MASTER DRAWING SET &bull; 3-STOREY CONTEMPORARY CANOPY VILLA</p>
      </div>
      <div class="sheet-title-badge">
        <h2>COVER &bull; PROJECT SCHEDULE</h2>
        <span>SHEET S-001</span>
      </div>
    </div>

    <div class="cover-body">
      <div class="cover-render-box">
        <img class="cover-render-img" src="{b64_hero}" alt="Exterior 3D Elevation Render" />
      </div>

      <div class="cover-info-panel">
        <div>
          <h3 style="font-size: 11pt; font-weight: 800; color: #0f172a; border-bottom: 1.5pt solid #0f172a; padding-bottom: 2mm;">
            PROJECT SCHEDULE &amp; ARCHITECTURAL PARAMETERS
          </h3>
          <table class="meta-table">
            <tr><th>Client / Owner</th><td>Mr. Daata Hamlet</td></tr>
            <tr><th>Project Location</th><td>Sector B, Phase 1, Daata Hamlet</td></tr>
            <tr><th>Plot Frontage</th><td>87'-11" (26.80 m) Continuous Front Face</td></tr>
            <tr><th>Plot Geometry</th><td>Trapezoidal: 87'-11" Front, Depth 62'-2" to 44'-8"</td></tr>
            <tr><th>Total Plot Area</th><td>3,129.1 Sq.Ft (12.8 Marla / 290.7 Sq.M)</td></tr>
            <tr><th>Total Covered Area</th><td>5,586.0 Sq.Ft (Across 3 Floors + Mumty Core)</td></tr>
            <tr><th>Ground Floor Area</th><td>2,125.0 Sq.Ft (Drawing, 2 Beds, Lounge, 2 Kitchens)</td></tr>
            <tr><th>First Floor Area</th><td>2,033.0 Sq.Ft (3 Master Suites, Lounge, Terrace)</td></tr>
            <tr><th>Second Floor Area</th><td>1,282.0 Sq.Ft (2 Beds, Servant, Open Sun Terrace)</td></tr>
            <tr><th>Mumty &amp; Water Tank</th><td>146.0 Sq.Ft Landing (+42'-0" Height)</td></tr>
            <tr><th>Structural Grid</th><td>22 Continuous Parallel RCC Columns (Flush in 9" Walls)</td></tr>
            <tr><th>Ground Floor Living</th><td>Drawing Room (18'x16') &bull; Bedrooms (15'x16')</td></tr>
            <tr><th>Kitchen Strategy</th><td>Wide 15'x11' Main + 100 sft NE Apex Dirty Kitchen</td></tr>
          </table>

          <h3 style="font-size: 10pt; font-weight: 800; color: #0f172a; border-bottom: 1.5pt solid #0f172a; padding-bottom: 1.5mm; margin-top: 4mm;">
            MASTER DRAWING INDEX
          </h3>
          <table class="index-table">
            <tr><th style="width: 20%;">Sheet</th><th style="width: 50%;">Drawing Title</th><th>Scale</th><th>Status</th></tr>
            <tr><td><b>S-001</b></td><td>Cover &bull; Project Parameters &amp; Drawing Index</td><td>N.T.S.</td><td>Issued</td></tr>
            <tr><td><b>A-101</b></td><td>Ground Floor Architectural Plan</td><td>1/4" = 1'-0"</td><td>Issued</td></tr>
            <tr><td><b>A-102</b></td><td>First Floor Architectural Plan</td><td>1/4" = 1'-0"</td><td>Issued</td></tr>
            <tr><td><b>A-103</b></td><td>Second Floor Architectural Plan</td><td>1/4" = 1'-0"</td><td>Issued</td></tr>
            <tr><td><b>A-104</b></td><td>Roof &amp; Mumty Architectural Plan</td><td>1/4" = 1'-0"</td><td>Issued</td></tr>
            <tr><td><b>S-101</b></td><td>Structural Column Grid Layout (22 Continuous Columns)</td><td>1/4" = 1'-0"</td><td>Issued</td></tr>
            <tr><td><b>A-201A</b></td><td>South Front Elevation (With Boundary Wall in Background)</td><td>1/4" = 1'-0"</td><td>Issued</td></tr>
            <tr><td><b>A-201B</b></td><td>South Front Elevation (Pure Architecture / Open Setting)</td><td>1/4" = 1'-0"</td><td>Issued</td></tr>
            <tr><td><b>A-301</b></td><td>Photorealistic 3D Perspectives &amp; Visualizations</td><td>N.T.S.</td><td>Issued</td></tr>
          </table>
        </div>

        <div style="font-size: 7.5pt; color: #64748b; line-height: 1.4; border-top: 1pt solid #cbd5e1; padding-top: 2mm;">
          <b>Architectural Notes:</b> All structural elements satisfy building bylaws. Continuous parallel 9"x18" reinforced concrete columns are concealed flush within 9" brick masonry walls. Finished floor levels: Plinth +1'-6", 1F +11'-10", 2F +22'-2", Roof +32'-6", Top of Mumty Core +42'-0".
        </div>
      </div>
    </div>

    <div class="arch-titleblock">
      <div class="tb-cell">
        <span class="tb-label">Architectural Studio</span>
        <span class="tb-val">STUDIO DESIGN ASSOCIATES</span>
      </div>
      <div class="tb-cell">
        <span class="tb-label">Project &bull; Client</span>
        <span class="tb-val">DAATA HAMLET RESIDENCE</span>
      </div>
      <div class="tb-cell">
        <span class="tb-label">Date &bull; Revision</span>
        <span class="tb-val">OCTOBER 2026 &bull; REV 03</span>
      </div>
      <div class="tb-cell">
        <span class="tb-label">Scale</span>
        <span class="tb-val">AS NOTED</span>
      </div>
      <div class="tb-cell">
        <span class="tb-label">Drawing Sheet</span>
        <span class="tb-val highlight">S-001</span>
      </div>
    </div>
  </div>

  <!-- ====================================================================== -->
  <!-- PAGE 2: SHEET A-101 - GROUND FLOOR ARCHITECTURAL PLAN -->
  <!-- ====================================================================== -->
  <div class="sheet">
    <div class="sheet-border"></div>
    <div class="sheet-inner-border"></div>

    <div class="arch-header">
      <div class="proj-title">
        <h1>DAATA HAMLET RESIDENCE</h1>
        <p>GROUND FLOOR ARCHITECTURAL PLAN &bull; FFL +1'-6" &bull; COVERED AREA: 2,125 SQ.FT</p>
      </div>
      <div class="sheet-title-badge">
        <h2>GROUND FLOOR PLAN</h2>
        <span>SHEET A-101</span>
      </div>
    </div>

    <div class="drawing-stage">
      <img class="drawing-img" src="{b64_gf}" alt="Ground Floor Architectural Plan" />
    </div>

    <div class="arch-titleblock">
      <div class="tb-cell">
        <span class="tb-label">Accommodations</span>
        <span class="tb-val">Drawing Room (18'x16'), 2 Master Beds (15'x16'), Lounge (25'x16'), Main &amp; Dirty Kitchen, 2-Car Porch</span>
      </div>
      <div class="tb-cell">
        <span class="tb-label">Dirty Kitchen Feature</span>
        <span class="tb-val">Custom 100 sft Tucked in NE Diagonal Apex (P5-P6-P7)</span>
      </div>
      <div class="tb-cell">
        <span class="tb-label">Status</span>
        <span class="tb-val">ISSUED FOR TENDER</span>
      </div>
      <div class="tb-cell">
        <span class="tb-label">Scale</span>
        <span class="tb-val">1/4" = 1'-0" (1:50)</span>
      </div>
      <div class="tb-cell">
        <span class="tb-label">Drawing Sheet</span>
        <span class="tb-val highlight">A-101</span>
      </div>
    </div>
  </div>

  <!-- ====================================================================== -->
  <!-- PAGE 3: SHEET A-102 - FIRST FLOOR ARCHITECTURAL PLAN -->
  <!-- ====================================================================== -->
  <div class="sheet">
    <div class="sheet-border"></div>
    <div class="sheet-inner-border"></div>

    <div class="arch-header">
      <div class="proj-title">
        <h1>DAATA HAMLET RESIDENCE</h1>
        <p>FIRST FLOOR ARCHITECTURAL PLAN &bull; FFL +11'-10" &bull; COVERED AREA: 2,033 SQ.FT</p>
      </div>
      <div class="sheet-title-badge">
        <h2>FIRST FLOOR PLAN</h2>
        <span>SHEET A-102</span>
      </div>
    </div>

    <div class="drawing-stage">
      <img class="drawing-img" src="{b64_f1}" alt="First Floor Architectural Plan" />
    </div>

    <div class="arch-titleblock">
      <div class="tb-cell">
        <span class="tb-label">Accommodations</span>
        <span class="tb-val">3 Master Suites (Beds 3, 4, 5 &ge; 15'x16'), Family Lounge (25'x16'), Open Kitchen, Porch Canopy Terrace</span>
      </div>
      <div class="tb-cell">
        <span class="tb-label">Outdoor Terraces</span>
        <span class="tb-val">Front Porch Canopy Terrace (346.5 sft) + West Balcony</span>
      </div>
      <div class="tb-cell">
        <span class="tb-label">Status</span>
        <span class="tb-val">ISSUED FOR TENDER</span>
      </div>
      <div class="tb-cell">
        <span class="tb-label">Scale</span>
        <span class="tb-val">1/4" = 1'-0" (1:50)</span>
      </div>
      <div class="tb-cell">
        <span class="tb-label">Drawing Sheet</span>
        <span class="tb-val highlight">A-102</span>
      </div>
    </div>
  </div>

  <!-- ====================================================================== -->
  <!-- PAGE 4: SHEET A-103 - SECOND FLOOR ARCHITECTURAL PLAN -->
  <!-- ====================================================================== -->
  <div class="sheet">
    <div class="sheet-border"></div>
    <div class="sheet-inner-border"></div>

    <div class="arch-header">
      <div class="proj-title">
        <h1>DAATA HAMLET RESIDENCE</h1>
        <p>SECOND FLOOR ARCHITECTURAL PLAN &bull; FFL +22'-2" &bull; COVERED AREA: 1,282 SQ.FT</p>
      </div>
      <div class="sheet-title-badge">
        <h2>SECOND FLOOR PLAN</h2>
        <span>SHEET A-103</span>
      </div>
    </div>

    <div class="drawing-stage">
      <img class="drawing-img" src="{b64_f2}" alt="Second Floor Architectural Plan" />
    </div>

    <div class="arch-titleblock">
      <div class="tb-cell">
        <span class="tb-label">Accommodations</span>
        <span class="tb-val">2 Master Suites (Beds 6, 7), Servant Room &amp; Bath (10'x8'), Laundry &amp; Store, Open Sun Terrace</span>
      </div>
      <div class="tb-cell">
        <span class="tb-label">Terraces</span>
        <span class="tb-val">Open-to-Sky Front Sun Terrace (307.5 sft) with Glass Balustrade</span>
      </div>
      <div class="tb-cell">
        <span class="tb-label">Status</span>
        <span class="tb-val">ISSUED FOR TENDER</span>
      </div>
      <div class="tb-cell">
        <span class="tb-label">Scale</span>
        <span class="tb-val">1/4" = 1'-0" (1:50)</span>
      </div>
      <div class="tb-cell">
        <span class="tb-label">Drawing Sheet</span>
        <span class="tb-val highlight">A-103</span>
      </div>
    </div>
  </div>

  <!-- ====================================================================== -->
  <!-- PAGE 5: SHEET A-104 - ROOF & MUMTY PLAN -->
  <!-- ====================================================================== -->
  <div class="sheet">
    <div class="sheet-border"></div>
    <div class="sheet-inner-border"></div>

    <div class="arch-header">
      <div class="proj-title">
        <h1>DAATA HAMLET RESIDENCE</h1>
        <p>ROOF &amp; MUMTY ARCHITECTURAL PLAN &bull; CANOPY LEVEL +32'-6" &bull; TOP OF MUMTY +42'-0"</p>
      </div>
      <div class="sheet-title-badge">
        <h2>ROOF &amp; MUMTY PLAN</h2>
        <span>SHEET A-104</span>
      </div>
    </div>

    <div class="drawing-stage">
      <img class="drawing-img" src="{b64_rf}" alt="Roof and Mumty Plan" />
    </div>

    <div class="arch-titleblock">
      <div class="tb-cell">
        <span class="tb-label">Elements</span>
        <span class="tb-val">Stair Mumty Landing, 800-Gallon Water Tank Housing, Roof Terrace (1,850 sft Solar Zone)</span>
      </div>
      <div class="tb-cell">
        <span class="tb-label">Parapet &amp; Drainage</span>
        <span class="tb-val">3'-0" Solid Parapet Walls, 1:60 Waterproof Slope screed</span>
      </div>
      <div class="tb-cell">
        <span class="tb-label">Status</span>
        <span class="tb-val">ISSUED FOR TENDER</span>
      </div>
      <div class="tb-cell">
        <span class="tb-label">Scale</span>
        <span class="tb-val">1/4" = 1'-0" (1:50)</span>
      </div>
      <div class="tb-cell">
        <span class="tb-label">Drawing Sheet</span>
        <span class="tb-val highlight">A-104</span>
      </div>
    </div>
  </div>

  <!-- ====================================================================== -->
  <!-- PAGE 6: SHEET S-101 - STRUCTURAL COLUMN GRID LAYOUT -->
  <!-- ====================================================================== -->
  <div class="sheet">
    <div class="sheet-border"></div>
    <div class="sheet-inner-border"></div>

    <div class="arch-header">
      <div class="proj-title">
        <h1>DAATA HAMLET RESIDENCE</h1>
        <p>STRUCTURAL COLUMN GRID LAYOUT &bull; 22 CONTINUOUS PARALLEL RCC COLUMNS (GRIDS A-E &bull; 1-8)</p>
      </div>
      <div class="sheet-title-badge">
        <h2>COLUMN GRID LAYOUT</h2>
        <span>SHEET S-101</span>
      </div>
    </div>

    <div class="drawing-stage">
      <img class="drawing-img" src="{b64_col}" alt="Structural Column Grid Layout" />
    </div>

    <div class="arch-titleblock">
      <div class="tb-cell">
        <span class="tb-label">Structural System</span>
        <span class="tb-val">22 Continuous 9"x18" RCC Columns running Ground -> First -> Second -> Mumty</span>
      </div>
      <div class="tb-cell">
        <span class="tb-label">Concealment Details</span>
        <span class="tb-val">100% Flush Concealed inside 9" Masonry Walls (Zero Protrusion)</span>
      </div>
      <div class="tb-cell">
        <span class="tb-label">Status</span>
        <span class="tb-val">STRUCTURAL APPROVED</span>
      </div>
      <div class="tb-cell">
        <span class="tb-label">Scale</span>
        <span class="tb-val">1/4" = 1'-0" (1:50)</span>
      </div>
      <div class="tb-cell">
        <span class="tb-label">Drawing Sheet</span>
        <span class="tb-val highlight">S-101</span>
      </div>
    </div>
  </div>

  <!-- ====================================================================== -->
  <!-- PAGE 7: SHEET A-201A - SOUTH FRONT ELEVATION (WITH BOUNDARY WALL) -->
  <!-- ====================================================================== -->
  <div class="sheet">
    <div class="sheet-border"></div>
    <div class="sheet-inner-border"></div>

    <div class="arch-header">
      <div class="proj-title">
        <h1>DAATA HAMLET RESIDENCE</h1>
        <p>SOUTH FRONT ELEVATION &bull; WITH BOUNDARY WALL (BACKGROUND OF LAWN &amp; CAR PORCH ONLY)</p>
      </div>
      <div class="sheet-title-badge">
        <h2>FRONT ELEVATION &bull; WITH WALL</h2>
        <span>SHEET A-201A</span>
      </div>
    </div>

    <div class="drawing-stage">
      <img class="drawing-img" src="{b64_elev_with_bw}" alt="South Front Elevation With Boundary Wall" />
    </div>

    <div class="arch-titleblock">
      <div class="tb-cell">
        <span class="tb-label">Key Architecture</span>
        <span class="tb-val">Open 2F Sun Terrace, Rising Mumty Tower (+42'-0"), Separate Drawing (7'x6') &amp; Lounge/Bed Windows</span>
      </div>
      <div class="tb-cell">
        <span class="tb-label">Porch &amp; Balustrades</span>
        <span class="tb-val">2 Rear-Facing Cars in Porch, Dual 1F/2F 12mm Frameless Glass Railings</span>
      </div>
      <div class="tb-cell">
        <span class="tb-label">Status</span>
        <span class="tb-val">WORKING ELEVATION</span>
      </div>
      <div class="tb-cell">
        <span class="tb-label">Scale</span>
        <span class="tb-val">1/4" = 1'-0" (1:50)</span>
      </div>
      <div class="tb-cell">
        <span class="tb-label">Drawing Sheet</span>
        <span class="tb-val highlight">A-201A</span>
      </div>
    </div>
  </div>

  <!-- ====================================================================== -->
  <!-- PAGE 8: SHEET A-201B - SOUTH FRONT ELEVATION (PURE ARCHITECTURE) -->
  <!-- ====================================================================== -->
  <div class="sheet">
    <div class="sheet-border"></div>
    <div class="sheet-inner-border"></div>

    <div class="arch-header">
      <div class="proj-title">
        <h1>DAATA HAMLET RESIDENCE</h1>
        <p>SOUTH FRONT ELEVATION &bull; PURE ARCHITECTURAL CANOPY ELEVATION (WITHOUT BOUNDARY WALL)</p>
      </div>
      <div class="sheet-title-badge">
        <h2>FRONT ELEVATION &bull; OPEN</h2>
        <span>SHEET A-201B</span>
      </div>
    </div>

    <div class="drawing-stage">
      <img class="drawing-img" src="{b64_elev_without_bw}" alt="South Front Elevation Without Boundary Wall" />
    </div>

    <div class="arch-titleblock">
      <div class="tb-cell">
        <span class="tb-label">Elevation Features</span>
        <span class="tb-val">Unobstructed Floating Cantilevered Canopies, Stepped Silhouette, Travertine Cladding</span>
      </div>
      <div class="tb-cell">
        <span class="tb-label">Materials</span>
        <span class="tb-val">Charcoal Bronze Fascias, Natural Teak Soffits, 12mm Tempered Glass</span>
      </div>
      <div class="tb-cell">
        <span class="tb-label">Status</span>
        <span class="tb-val">PRESENTATION DRAWING</span>
      </div>
      <div class="tb-cell">
        <span class="tb-label">Scale</span>
        <span class="tb-val">1/4" = 1'-0" (1:50)</span>
      </div>
      <div class="tb-cell">
        <span class="tb-label">Drawing Sheet</span>
        <span class="tb-val highlight">A-201B</span>
      </div>
    </div>
  </div>

  <!-- ====================================================================== -->
  <!-- PAGE 9: SHEET A-301 - PHOTOREALISTIC 3D PERSPECTIVES -->
  <!-- ====================================================================== -->
  <div class="sheet">
    <div class="sheet-border"></div>
    <div class="sheet-inner-border"></div>

    <div class="arch-header">
      <div class="proj-title">
        <h1>DAATA HAMLET RESIDENCE</h1>
        <p>3D ARCHITECTURAL VISUALIZATIONS &bull; BLENDER 5.1 CYCLES PHOTOREALISTIC RENDERS</p>
      </div>
      <div class="sheet-title-badge">
        <h2>3D PERSPECTIVES</h2>
        <span>SHEET A-301</span>
      </div>
    </div>

    <div class="studies-grid">
      <div class="render-card">
        <img src="{b64_hero}" alt="Front South Perspective Render" />
        <div class="render-card-caption">
          <span>FIG 1: SIGNATURE CANOPY FRONT SOUTH ELEVATION PERSPECTIVE</span>
          <span style="color:#0284c7;">4:30 PM GOLDEN HOUR LIGHTING</span>
        </div>
      </div>

      <div class="render-card">
        <img src="{b64_aerial}" alt="Bird's Eye Aerial View" />
        <div class="render-card-caption">
          <span>FIG 2: BIRD'S EYE 3/4 AERIAL PERSPECTIVE</span>
          <span style="color:#0284c7;">SITE CONTAINMENT &bull; ROOF CANOPY &bull; NE APEX KITCHEN</span>
        </div>
      </div>
    </div>

    <div class="arch-titleblock">
      <div class="tb-cell">
        <span class="tb-label">Rendering Engine</span>
        <span class="tb-val">Cycles PBR Offline Raytracing (Nishita Atmospheric Physical Sun/Sky)</span>
      </div>
      <div class="tb-cell">
        <span class="tb-label">Interactive 3D Study</span>
        <span class="tb-val">Available via standalone_viewer.html (WebGL / Three.js)</span>
      </div>
      <div class="tb-cell">
        <span class="tb-label">Status</span>
        <span class="tb-val">PRESENTATION ISSUE</span>
      </div>
      <div class="tb-cell">
        <span class="tb-label">Scale</span>
        <span class="tb-val">N.T.S.</span>
      </div>
      <div class="tb-cell">
        <span class="tb-label">Drawing Sheet</span>
        <span class="tb-val highlight">A-301</span>
      </div>
    </div>
  </div>

</body>
</html>
"""

    temp_html = WORKSPACE / "temp_pdf_bundle.html"
    temp_html.write_text(html_content, encoding="utf-8")

    pdf_out_path = WORKSPACE / "blueprints" / "daata_hamlet" / "daata_hamlet_master_architectural_package.pdf"
    artifact_pdf_path = ARTIFACT_DIR / "daata_hamlet_master_architectural_package.pdf"

    print("[+] Rendering complete 9-page architectural master PDF bundle via Playwright...")
    with sync_playwright() as pw:
        browser = pw.chromium.launch()
        page = browser.new_page()
        page.goto(temp_html.resolve().as_uri(), wait_until="load")
        
        # Give 2.5s for all base64 images and vector SVGs to decode fully
        page.wait_for_timeout(2500)
        
        page.pdf(
            path=str(pdf_out_path),
            format="A3",
            landscape=True,
            print_background=True,
            prefer_css_page_size=True
        )
        page.pdf(
            path=str(artifact_pdf_path),
            format="A3",
            landscape=True,
            print_background=True,
            prefer_css_page_size=True
        )
        browser.close()

    if temp_html.exists():
        temp_html.unlink()

    print(f"[+] Master Architectural PDF generated successfully:")
    print(f"    - Workspace: {pdf_out_path} ({pdf_out_path.stat().st_size:,} bytes)")
    print(f"    - Artifact:  {artifact_pdf_path} ({artifact_pdf_path.stat().st_size:,} bytes)")

if __name__ == "__main__":
    generate_pdf()
