"""
DAATA HAMLET RESIDENCE - Pure Drawings-Only Architectural PDF Generator
Creates a professional, clean, drawings-only architectural drawing set.
Contains strictly the architectural drawings and blueprints:
  Page 1: Ground Floor Architectural Plan (Sheet A-101)
  Page 2: First Floor Architectural Plan (Sheet A-102)
  Page 3: Second Floor Architectural Plan (Sheet A-103)
  Page 4: Roof & Mumty Architectural Plan (Sheet A-104)
  Page 5: Structural Column Grid & Continuity Plan (Sheet S-101)
  Page 6: South Front Elevation — With Boundary Wall (Sheet A-201A)
  Page 7: South Front Elevation — Pure Architecture (Sheet A-201B)

Zero cover sheets, zero specification tables, zero AI text/jargon, zero clutter.
Each page is 100% dedicated to the drawing sheet itself.
"""
from __future__ import annotations
import base64
import pathlib
import shutil
from playwright.sync_api import sync_playwright
import pymupdf

WORKSPACE = pathlib.Path(__file__).parent.parent.parent.resolve()
BLUEPRINTS_DIR = WORKSPACE / "blueprints" / "daata_hamlet"
ARTIFACT_DIR = pathlib.Path(r"C:\Users\adees\.gemini\antigravity\brain\754b2257-dc8d-4e91-8a73-3c0efba21f41")

def get_b64(path: pathlib.Path) -> str:
    ext = path.suffix.lower()
    mime = "image/png" if ext == ".png" else "image/svg+xml"
    return f"data:{mime};base64," + base64.b64encode(path.read_bytes()).decode("ascii")

def generate_pdf():
    # File targets
    out_pdf = BLUEPRINTS_DIR / "daata_hamlet_drawings_only.pdf"
    artifact_pdf = ARTIFACT_DIR / "daata_hamlet_drawings_only.pdf"

    # Make sure S-001 in 05_column_grid_layout.svg is S-101 if needed
    col_svg_path = BLUEPRINTS_DIR / "05_column_grid_layout.svg"
    col_content = col_svg_path.read_text(encoding="utf-8")
    if "SHEET: S-001" in col_content:
        col_content = col_content.replace("SHEET: S-001", "SHEET: S-101")
        col_svg_path.write_text(col_content, encoding="utf-8")
        print("[+] Updated Sheet number in 05_column_grid_layout.svg to S-101.")

    sheets = [
        ("Ground Floor Architectural Plan", BLUEPRINTS_DIR / "01_ground_floor_plan.svg"),
        ("First Floor Architectural Plan", BLUEPRINTS_DIR / "02_first_floor_plan.svg"),
        ("Second Floor Architectural Plan", BLUEPRINTS_DIR / "03_second_floor_plan.svg"),
        ("Roof & Mumty Architectural Plan", BLUEPRINTS_DIR / "04_roof_mumty_plan.svg"),
        ("Structural Column & Grid Layout", BLUEPRINTS_DIR / "05_column_grid_layout.svg"),
        ("South Front Elevation (With Boundary Wall)", BLUEPRINTS_DIR / "daata_hamlet_elevation_with_boundary_wall.png"),
        ("South Front Elevation (Pure Architecture)", BLUEPRINTS_DIR / "daata_hamlet_elevation_without_boundary_wall.png"),
    ]

    html_parts = []
    html_parts.append("""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>DAATA HAMLET RESIDENCE — Architectural Drawings</title>
  <style>
    @page {
      size: 420mm 297mm; /* Standard A3 Landscape */
      margin: 0;
    }
    * {
      margin: 0;
      padding: 0;
      box-sizing: border-box;
    }
    body {
      background: #ffffff;
      -webkit-print-color-adjust: exact;
      print-color-adjust: exact;
    }
    .sheet-page {
      width: 420mm;
      height: 297mm;
      page-break-after: always;
      page-break-inside: avoid;
      display: flex;
      justify-content: center;
      align-items: center;
      background: #ffffff;
      padding: 5mm;
      overflow: hidden;
    }
    .sheet-page:last-child {
      page-break-after: avoid;
    }
    .sheet-page img {
      max-width: 100%;
      max-height: 100%;
      width: auto;
      height: auto;
      object-fit: contain;
      display: block;
    }
  </style>
</head>
<body>
""")

    for title, path in sheets:
        uri = get_b64(path)
        html_parts.append(f'  <div class="sheet-page">\n    <img src="{uri}" alt="{title}">\n  </div>\n')

    html_parts.append("</body>\n</html>")

    html_content = "".join(html_parts)
    temp_html = WORKSPACE / "temp_drawings_print.html"
    temp_html.write_text(html_content, encoding="utf-8")

    print("[+] Rendering PDF via Playwright...")
    with sync_playwright() as pw:
        browser = pw.chromium.launch()
        page = browser.new_page()
        page.goto(temp_html.resolve().as_uri(), wait_until="networkidle")
        page.pdf(
            path=str(out_pdf),
            format="A3",
            landscape=True,
            print_background=True,
            prefer_css_page_size=True,
            margin={"top": "0", "right": "0", "bottom": "0", "left": "0"}
        )
        browser.close()

    temp_html.unlink(missing_ok=True)
    print(f"[+] Successfully wrote {out_pdf}")

    # Copy to artifacts directory
    ARTIFACT_DIR.mkdir(parents=True, exist_ok=True)
    shutil.copy2(out_pdf, artifact_pdf)
    print(f"[+] Copied to artifact: {artifact_pdf}")

    # Validate with pymupdf
    doc = pymupdf.open(str(out_pdf))
    print(f"[+] PDF Validation: Total Pages = {len(doc)}")
    for i, p in enumerate(doc):
        print(f"    Page {i+1}: size = {p.rect.width:.1f} x {p.rect.height:.1f} pt")
        # Save thumbnail of each page to inspect
        pix = p.get_pixmap(dpi=100)
        thumb_path = WORKSPACE / f"preview_page_{i+1}.png"
        pix.save(str(thumb_path))

    doc.close()
    print("[+] Completed drawings-only PDF generation and thumbnail export.")

if __name__ == "__main__":
    generate_pdf()
