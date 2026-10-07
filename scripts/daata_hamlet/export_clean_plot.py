"""
DAATA HAMLET RESIDENCE — Clean Site Survey & Plot Layout Exporter
Generates a pristine, presentation-grade plot sheet without internal building walls or furniture.
Contains:
1. Exact boundary polygon (P0, P1, P2, P3, P4, P5, P6, P7) with all segment dimensions
2. Survey points table with exact (X, Y) coordinates
3. Public access road frontage (87'-11")
4. Structural grid lines (A, B, C, C', D, E and 1, 2, 3, 4, 5, 6, 7)
5. Strict Line B Lawn demarcation (588.9 sq.ft reserved green space)
6. Buildable architectural envelope (49'-0" frontage x 49'-0" depth)
7. North arrow, graphic scale, area schedule, and professional title block
"""
from __future__ import annotations
import math
from pathlib import Path
import ezdxf
from ezdxf import colors
from playwright.sync_api import sync_playwright

WORKSPACE = Path(__file__).resolve().parents[2]
OUT_DIR = WORKSPACE / "blueprints" / "daata_hamlet"
OUT_DIR.mkdir(parents=True, exist_ok=True)
ARTIFACT_DIR = Path(r"C:\Users\adees\.gemini\antigravity\brain\754b2257-dc8d-4e91-8a73-3c0efba21f41")

SITE_POINTS = [
    ("P1", 0.0000, 0.0000), ("P2", 10.4884, 10.0122), ("P3", 24.5949, 26.1267),
    ("P4", 41.1897, 36.8354), ("P5", 67.6992, 50.7010), ("P6", 84.8373, 57.6678),
    ("P7", 88.8145, 62.1602), ("P0", 87.9167, 0.0000),
]
SURVEY_SEGMENTS = [
    ("P1", "P2", "14'-6\""), ("P2", "P3", "21'-5\""), ("P3", "P4", "19'-9\""),
    ("P4", "P5", "29'-11\""), ("P5", "P6", "18'-6\""), ("P6", "P7", "6'-0\""),
    ("P7", "P0", "62'-2\""), ("P0", "P1", "87'-11\"")
]

GX = {"A": 18.0, "B": 36.5, "C": 51.75, "C'": 57.0, "D": 69.0, "E": 84.75}
GY = {"1": 3.375, "2": 20.125, "3": 28.5, "4": 36.5, "5": 42.125, "6": 48.0, "7": 55.5}

XB_W = 36.125
XE_W = 84.375
XE_O = 85.125


class CleanPlotSVG:
    def __init__(self, w=1600, h=1150):
        self.w = w
        self.h = h
        self.scale = 13.5  # px per ft
        self.ox = 180
        self.oy = 960
        self.elements = []

    def wx(self, x: float) -> float:
        return self.ox + x * self.scale

    def wy(self, y: float) -> float:
        return self.oy - y * self.scale

    def line(self, x0, y0, x1, y1, stroke="#000", stroke_w=1, dash=""):
        d = f' stroke-dasharray="{dash}"' if dash else ""
        self.elements.append(f'<line x1="{self.wx(x0):.1f}" y1="{self.wy(y0):.1f}" x2="{self.wx(x1):.1f}" y2="{self.wy(y1):.1f}" stroke="{stroke}" stroke-width="{stroke_w}"{d}/>')

    def rect(self, x0, y0, x1, y1, fill="none", stroke="#000", stroke_w=1, dash=""):
        x = min(self.wx(x0), self.wx(x1))
        y = min(self.wy(y0), self.wy(y1))
        w = abs(self.wx(x1) - self.wx(x0))
        h = abs(self.wy(y1) - self.wy(y0))
        d = f' stroke-dasharray="{dash}"' if dash else ""
        self.elements.append(f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" fill="{fill}" stroke="{stroke}" stroke-width="{stroke_w}"{d}/>')

    def polygon(self, pts, fill="none", stroke="#000", stroke_w=1, dash=""):
        s = " ".join(f"{self.wx(x):.1f},{self.wy(y):.1f}" for x, y in pts)
        d = f' stroke-dasharray="{dash}"' if dash else ""
        self.elements.append(f'<polygon points="{s}" fill="{fill}" stroke="{stroke}" stroke-width="{stroke_w}"{d}/>')

    def circle(self, cx, cy, r_ft, fill="none", stroke="#000", stroke_w=1):
        self.elements.append(f'<circle cx="{self.wx(cx):.1f}" cy="{self.wy(cy):.1f}" r="{r_ft * self.scale:.1f}" fill="{fill}" stroke="{stroke}" stroke-width="{stroke_w}"/>')

    def text(self, x, y, txt, size=11, fill="#000", anchor="middle", weight="normal", rot=0):
        t = f' transform="rotate({rot} {self.wx(x):.1f} {self.wy(y):.1f})"' if rot else ""
        self.elements.append(f'<text x="{self.wx(x):.1f}" y="{self.wy(y):.1f}" font-size="{size}" font-family="Arial, sans-serif" font-weight="{weight}" text-anchor="{anchor}" fill="{fill}"{t}>{txt}</text>')

    def canvas_line(self, x0, y0, x1, y1, stroke="#000", stroke_w=1, dash=""):
        d = f' stroke-dasharray="{dash}"' if dash else ""
        self.elements.append(f'<line x1="{x0}" y1="{y0}" x2="{x1}" y2="{y1}" stroke="{stroke}" stroke-width="{stroke_w}"{d}/>')

    def canvas_text(self, px, py, txt, size=11, fill="#000", anchor="start", weight="normal"):
        self.elements.append(f'<text x="{px}" y="{py}" font-size="{size}" font-family="Arial, sans-serif" font-weight="{weight}" text-anchor="{anchor}" fill="{fill}">{txt}</text>')

    def dim_h(self, x0, x1, y, offset_ft=2.5, txt=None):
        yd = y + offset_ft
        self.line(x0, yd, x1, yd, stroke="#2c3e50", stroke_w=1)
        self.line(x0, y, x0, yd + (0.5 if offset_ft >= 0 else -0.5), stroke="#7f8c8d", stroke_w=0.75)
        self.line(x1, y, x1, yd + (0.5 if offset_ft >= 0 else -0.5), stroke="#7f8c8d", stroke_w=0.75)
        t = 0.35
        self.line(x0 - t, yd - t, x0 + t, yd + t, stroke="#2c3e50", stroke_w=1.5)
        self.line(x1 - t, yd - t, x1 + t, yd + t, stroke="#2c3e50", stroke_w=1.5)
        label = txt if txt is not None else f"{abs(x1 - x0):.1f}'"
        self.text((x0 + x1) / 2, yd + 0.45, label, size=9.5, fill="#2c3e50", weight="bold")

    def dim_v(self, y0, y1, x, offset_ft=2.5, txt=None):
        xd = x + offset_ft
        self.line(xd, y0, xd, y1, stroke="#2c3e50", stroke_w=1)
        self.line(x, y0, xd + (0.5 if offset_ft >= 0 else -0.5), y0, stroke="#7f8c8d", stroke_w=0.75)
        self.line(x, y1, xd + (0.5 if offset_ft >= 0 else -0.5), y1, stroke="#7f8c8d", stroke_w=0.75)
        t = 0.35
        self.line(xd - t, y0 - t, xd + t, y0 + t, stroke="#2c3e50", stroke_w=1.5)
        self.line(xd - t, y1 - t, xd + t, y1 + t, stroke="#2c3e50", stroke_w=1.5)
        label = txt if txt is not None else f"{abs(y1 - y0):.1f}'"
        self.text(xd + (0.8 if offset_ft >= 0 else -0.8), (y0 + y1) / 2, label, size=9.5, fill="#2c3e50", weight="bold", rot=-90)

    def draw_border_and_title(self):
        # Outer border
        self.canvas_line(20, 20, self.w - 20, 20, stroke="#1a252f", stroke_w=2)
        self.canvas_line(self.w - 20, 20, self.w - 20, self.h - 20, stroke="#1a252f", stroke_w=2)
        self.canvas_line(self.w - 20, self.h - 20, 20, self.h - 20, stroke="#1a252f", stroke_w=2)
        self.canvas_line(20, self.h - 20, 20, 20, stroke="#1a252f", stroke_w=2)
        self.canvas_line(30, 30, self.w - 30, 30, stroke="#7f8c8d", stroke_w=0.75)
        self.canvas_line(self.w - 30, 30, self.w - 30, self.h - 30, stroke="#7f8c8d", stroke_w=0.75)
        self.canvas_line(self.w - 30, self.h - 30, 30, self.h - 30, stroke="#7f8c8d", stroke_w=0.75)
        self.canvas_line(30, self.h - 30, 30, 30, stroke="#7f8c8d", stroke_w=0.75)

        # Title Block
        tb_w, tb_h = 520, 95
        tb_x = self.w - 30 - tb_w
        tb_y = self.h - 30 - tb_h
        self.elements.append(f'<rect x="{tb_x}" y="{tb_y}" width="{tb_w}" height="{tb_h}" fill="#ffffff" stroke="#1a252f" stroke-width="1.5"/>')
        self.canvas_line(tb_x, tb_y + 32, tb_x + tb_w, tb_y + 32, stroke="#bdc3c7", stroke_w=1)
        self.canvas_line(tb_x, tb_y + 64, tb_x + tb_w, tb_y + 64, stroke="#bdc3c7", stroke_w=1)
        self.canvas_line(tb_x + 360, tb_y + 32, tb_x + 360, tb_y + tb_h, stroke="#bdc3c7", stroke_w=1)

        self.canvas_text(tb_x + 14, tb_y + 22, "DAATA HAMLET RESIDENCE", size=15, weight="bold", fill="#2c3e50")
        self.canvas_text(tb_x + 375, tb_y + 22, "PLOT AREA: 3,129.1 SQ.FT.", size=10, fill="#7f8c8d", weight="bold")
        self.canvas_text(tb_x + 14, tb_y + 50, "SHEET: CLEAN SITE SURVEY & PLOT BOUNDARY", size=11, weight="bold", fill="#2980b9")
        self.canvas_text(tb_x + 375, tb_y + 50, "SHEET NO: C-101", size=12, weight="bold", fill="#c0392b")
        self.canvas_text(tb_x + 14, tb_y + 82, 'SCALE: 1/8" = 1\'-0"  |  FOR AI ARCHITECTURAL PROMPTING', size=9.5, fill="#7f8c8d")
        self.canvas_text(tb_x + 375, tb_y + 82, "UNITS: FEET-INCHES", size=10, fill="#2c3e50", weight="bold")

        # North Arrow
        nx, ny = self.w - 85, 95
        self.elements.append(
            f'<g transform="translate({nx},{ny})">'
            f'<circle cx="0" cy="0" r="28" fill="#ffffff" stroke="#2c3e50" stroke-width="1.5"/>'
            f'<polygon points="0,-24 8,18 0,11" fill="#2c3e50"/>'
            f'<polygon points="0,-24 -8,18 0,11" fill="#bdc3c7"/>'
            f'<text x="0" y="-28" font-size="13" font-family="Arial" font-weight="bold" text-anchor="middle" fill="#2c3e50">N</text>'
            f'</g>'
        )

    def to_svg(self) -> str:
        self.draw_border_and_title()
        return (
            f'<?xml version="1.0" encoding="UTF-8"?>\n'
            f'<svg xmlns="http://www.w3.org/2000/svg" width="{self.w}" height="{self.h}" viewBox="0 0 {self.w} {self.h}">\n'
            f'<defs>\n'
            f'  <style>\n'
            f'    text {{ user-select: none; }}\n'
            f'  </style>\n'
            f'  <pattern id="lawnPat" width="16" height="16" patternUnits="userSpaceOnUse">\n'
            f'    <circle cx="8" cy="8" r="1.5" fill="#27ae60" opacity="0.4"/>\n'
            f'  </pattern>\n'
            f'  <pattern id="buildPat" width="20" height="20" patternUnits="userSpaceOnUse">\n'
            f'    <line x1="0" y1="20" x2="20" y2="0" stroke="#bdc3c7" stroke-width="0.75" opacity="0.4"/>\n'
            f'  </pattern>\n'
            f'</defs>\n'
            f'<rect width="{self.w}" height="{self.h}" fill="#fcfdfd"/>\n'
            + "\n".join(self.elements)
            + "\n</svg>"
        )


def generate_clean_plot():
    canvas = CleanPlotSVG()

    # 1. Road Representation
    canvas.rect(0, -22, 92, -9, fill="#f2f4f4", stroke="#bdc3c7", stroke_w=1)
    canvas.line(0, -15.5, 92, -15.5, stroke="#e67e22", stroke_w=1, dash="8,8")
    canvas.text(46, -16.5, "PUBLIC ACCESS ROAD (87'-11\" FRONTAGE)", size=13, weight="bold", fill="#7f8c8d")

    # 2. Main Lawn Reserved Zone (strictly West of Line B)
    # Polygon bounded by P1, P2, P3, and intersection with Line B (X=36.125)
    lawn_pts = [(0.0, 0.0), (10.4884, 10.0122), (24.5949, 26.1267), (36.125, 33.5671), (36.125, 0.0)]
    canvas.polygon(lawn_pts, fill="#eafaf1", stroke="#27ae60", stroke_w=1.5)
    canvas.polygon(lawn_pts, fill="url(#lawnPat)", stroke="none")

    # 3. Buildable Footprint Envelope (East of Line B)
    # Bounded by Line B, survey boundary P4-P7, P7-P0, and front setback at Y=3.0
    build_pts = [
        (36.125, 3.0), (36.125, 33.5671), (41.1897, 36.8354), (67.6992, 50.7010),
        (84.8373, 57.6678), (88.8145, 62.1602), (87.9167, 3.0)
    ]
    canvas.polygon(build_pts, fill="#f8f9fa", stroke="#34495e", stroke_w=1.5, dash="5,5")
    canvas.polygon(build_pts, fill="url(#buildPat)", stroke="none")

    # 4. Strict Line B Demarcation
    canvas.line(XB_W, -8.5, XB_W, 40, stroke="#e74c3c", stroke_w=2.0, dash="6,4")
    canvas.text(XB_W, 42.0, "LINE B: STRICT LAWN DEMARCATION", size=10, weight="bold", fill="#c0392b")
    canvas.text(XB_W, 40.5, "(ZERO BUILDING ENCROACHMENT WEST OF THIS LINE)", size=8.5, fill="#c0392b")

    # 5. Structural Grid Lines
    for letter, x in GX.items():
        canvas.line(x, -1.8, x, 65, stroke="#bdc3c7", stroke_w=0.75, dash="4,4")
        canvas.circle(x, -1.2, 1.1, fill="#ffffff", stroke="#2c3e50", stroke_w=1)
        canvas.text(x, -1.5, letter, size=9.5, weight="bold", fill="#2c3e50")
        canvas.circle(x, 66.5, 1.1, fill="#ffffff", stroke="#2c3e50", stroke_w=1)
        canvas.text(x, 66.2, letter, size=9.5, weight="bold", fill="#2c3e50")

    for num, y in GY.items():
        canvas.line(5, y, 92, y, stroke="#bdc3c7", stroke_w=0.75, dash="4,4")
        canvas.circle(94.5, y, 1.1, fill="#ffffff", stroke="#2c3e50", stroke_w=1)
        canvas.text(94.5, y - 0.35, num, size=9.5, weight="bold", fill="#2c3e50")

    # 6. Site Boundary Polygon (Red Bold)
    site_coords = [(x, y) for _, x, y in SITE_POINTS]
    canvas.polygon(site_coords, fill="none", stroke="#c0392b", stroke_w=2.5)

    # 7. Survey Pegs & Coordinates
    for name, x, y in SITE_POINTS:
        canvas.circle(x, y, 0.6, fill="#c0392b", stroke="#ffffff", stroke_w=1.2)
        ox = 2.2 if x < 50 else -2.2
        oy = 2.0 if y < 40 else -2.0
        canvas.text(x + ox, y + oy + 0.6, f"{name}", size=11, weight="bold", fill="#c0392b")
        canvas.text(x + ox, y + oy - 0.6, f"({x:.1f}, {y:.1f})", size=8.5, fill="#7f8c8d")

    # 8. Boundary Segment Dimensions
    for p_a, p_b, dim_txt in SURVEY_SEGMENTS:
        if p_a == "P0" and p_b == "P1":
            continue  # Covered by dimension chain below
        pt_a = [(x, y) for n, x, y in SITE_POINTS if n == p_a][0]
        pt_b = [(x, y) for n, x, y in SITE_POINTS if n == p_b][0]
        mx, my = (pt_a[0] + pt_b[0]) / 2, (pt_a[1] + pt_b[1]) / 2
        dx, dy = pt_b[0] - pt_a[0], pt_b[1] - pt_a[1]
        length = math.hypot(dx, dy)
        if length > 0:
            nx, ny = -dy / length, dx / length
            canvas.text(mx + nx * 2.5, my + ny * 2.5 - 0.3, dim_txt, size=10, weight="bold", fill="#c0392b")

    # 9. Main Zone Callouts
    # Main Lawn
    canvas.text(22.0, 16.0, "MAIN LAWN", size=16, weight="bold", fill="#27ae60")
    canvas.text(22.0, 14.0, "~588.9 SQ.FT (1.8 MARLA)", size=10, weight="bold", fill="#27ae60")
    canvas.text(22.0, 12.2, "STRICTLY RESERVED GREEN SPACE", size=8.5, fill="#2ecc71")
    canvas.text(22.0, 10.5, "100% OPEN SKY GARDEN", size=8.0, fill="#7f8c8d")

    # Buildable Zone
    canvas.text(62.0, 34.0, "PRIMARY ARCHITECTURAL RESIDENCE ENVELOPE", size=13, weight="bold", fill="#2c3e50")
    canvas.text(62.0, 31.8, "MAIN FACADE FRONTAGE = 49'-0\" CLEAR", size=10, weight="bold", fill="#2980b9")
    canvas.text(62.0, 29.8, "OVERALL BUILDING DEPTH = 49'-0\" TO 57'-0\"", size=9.5, fill="#7f8c8d")
    canvas.text(62.0, 27.8, "FINISHED FLOOR LEVEL (FFL) = +0.00m (+1.50' ABOVE ROAD)", size=9.0, fill="#7f8c8d")

    # East Passage Setback
    canvas.text(86.5, 30.0, "2'-9½\" CLEAR EAST SERVICE PASSAGE", size=9, weight="bold", fill="#2980b9", rot=-90)

    # 10. Dimension Chains
    canvas.dim_h(0.0, 87.9167, 0.0, offset_ft=-7.2, txt="OVERALL PLOT FRONTAGE = 87'-11\"")
    canvas.dim_h(0.0, XB_W, 0.0, offset_ft=-4.0, txt="MAIN LAWN: 36'-1½\"")
    canvas.dim_h(XB_W, XE_O, 0.0, offset_ft=-4.0, txt="RESIDENCE FACADE: 49'-0\"")
    canvas.dim_h(XE_O, 87.9167, 0.0, offset_ft=-4.0, txt="PASSAGE: 2'-9½\"")

    canvas.dim_v(0.0, 62.1602, 90.0, offset_ft=2.0, txt="EAST BOUNDARY DEPTH: 62'-2\"")

    # 11. Survey Table on Sheet
    tbl_x, tbl_y = 60, 65
    canvas.elements.append(
        f'<g transform="translate({tbl_x},{tbl_y})">'
        f'<rect x="0" y="0" width="370" height="235" fill="#ffffff" stroke="#2c3e50" stroke-width="1.5"/>'
        f'<text x="14" y="24" font-size="12" font-family="Arial" font-weight="bold" fill="#2c3e50">SITE SURVEY COORDINATE TABLE</text>'
        f'<line x1="0" y1="34" x2="370" y2="34" stroke="#bdc3c7" stroke-width="1"/>'
        f'<text x="16" y="50" font-size="9.5" font-family="Arial" font-weight="bold" fill="#7f8c8d">PEG</text>'
        f'<text x="65" y="50" font-size="9.5" font-family="Arial" font-weight="bold" fill="#7f8c8d">X (FT)</text>'
        f'<text x="135" y="50" font-size="9.5" font-family="Arial" font-weight="bold" fill="#7f8c8d">Y (FT)</text>'
        f'<text x="205" y="50" font-size="9.5" font-family="Arial" font-weight="bold" fill="#7f8c8d">SEGMENT</text>'
        f'<text x="295" y="50" font-size="9.5" font-family="Arial" font-weight="bold" fill="#7f8c8d">LENGTH</text>'
        f'<line x1="0" y1="58" x2="370" y2="58" stroke="#bdc3c7" stroke-width="1"/>'
    )
    y_r = 75
    for i, (name, x, y) in enumerate(SITE_POINTS):
        seg_lbl = f"{name} \u2192 {SITE_POINTS[(i+1)%len(SITE_POINTS)][0]}"
        seg_len = SURVEY_SEGMENTS[i][2] if i < len(SURVEY_SEGMENTS) else ""
        canvas.elements.append(
            f'<text x="28" y="{y_r}" font-size="9.5" font-family="Arial" font-weight="bold" fill="#c0392b">{name}</text>'
            f'<text x="80" y="{y_r}" font-size="9.5" font-family="Arial" fill="#2c3e50">{x:7.2f}</text>'
            f'<text x="150" y="{y_r}" font-size="9.5" font-family="Arial" fill="#2c3e50">{y:7.2f}</text>'
            f'<text x="235" y="{y_r}" font-size="9.5" font-family="Arial" fill="#7f8c8d">{seg_lbl}</text>'
            f'<text x="320" y="{y_r}" font-size="9.5" font-family="Arial" font-weight="bold" fill="#2c3e50">{seg_len}</text>'
        )
        y_r += 17

    canvas.elements.append(
        f'<line x1="0" y1="210" x2="370" y2="210" stroke="#bdc3c7" stroke-width="1"/>'
        f'<text x="14" y="226" font-size="10" font-family="Arial" font-weight="bold" fill="#27ae60">TOTAL PLOT AREA = 3,129.1 SQ.FT. (12.8 MARLA)</text>'
        f'</g>'
    )

    # Save SVG
    svg_path = OUT_DIR / "clean_plot_site_survey.svg"
    svg_path.write_text(canvas.to_svg(), encoding="utf-8")
    print(f"[+] Wrote Clean Plot SVG: {svg_path}")

    # Generate DXF
    doc = ezdxf.new("R2018")
    doc.header["$INSUNITS"] = 2  # Feet
    msp = doc.modelspace()
    doc.layers.add("0_SITE_BOUNDARY", color=colors.RED)
    doc.layers.add("S_GRID_LINES", color=colors.MAGENTA)
    doc.layers.add("A_ZONES", color=colors.GREEN)
    doc.layers.add("A_DIMENSIONS", color=colors.YELLOW)
    doc.layers.add("A_TEXT", color=colors.WHITE)

    # Site Boundary in DXF
    pts = [(x, y) for _, x, y in SITE_POINTS]
    msp.add_lwpolyline(pts, format="xy", close=True, dxfattribs={"layer": "0_SITE_BOUNDARY"})
    for name, x, y in SITE_POINTS:
        msp.add_circle((x, y), 0.5, dxfattribs={"layer": "0_SITE_BOUNDARY"})
        msp.add_text(f"{name} ({x:.1f}, {y:.1f})", height=0.8, dxfattribs={"layer": "0_SITE_BOUNDARY"}).set_placement(
            (x + 1.0, y + 1.0)
        )

    # Grids in DXF
    for ltr, x in GX.items():
        msp.add_line((x, -3), (x, 65), dxfattribs={"layer": "S_GRID_LINES", "linetype": "DASHED"})
        msp.add_text(ltr, height=1.0, dxfattribs={"layer": "S_GRID_LINES"}).set_placement((x, -4.5))
    for num, y in GY.items():
        msp.add_line((5, y), (92, y), dxfattribs={"layer": "S_GRID_LINES", "linetype": "DASHED"})
        msp.add_text(num, height=1.0, dxfattribs={"layer": "S_GRID_LINES"}).set_placement((94.0, y))

    # Road & Line B
    msp.add_line((XB_W, -4), (XB_W, 40), dxfattribs={"layer": "0_SITE_BOUNDARY", "linetype": "DASHED"})
    msp.add_text("LINE B (LAWN BOUNDARY)", height=1.0, dxfattribs={"layer": "A_TEXT"}).set_placement((XB_W + 1.0, 35.0))

    dxf_path = OUT_DIR / "clean_plot_site_survey.dxf"
    doc.saveas(str(dxf_path))
    print(f"[+] Wrote Clean Plot DXF: {dxf_path}")

    # Render High-Resolution PNG via Playwright
    html_wrapper = f"""<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <style>
    body {{ margin: 0; background: #ffffff; display: flex; justify-content: center; align-items: center; }}
    svg {{ width: 1600px; height: 1150px; }}
  </style>
</head>
<body>
{canvas.to_svg()}
</body>
</html>"""
    temp_html = WORKSPACE / "temp_clean_plot.html"
    temp_html.write_text(html_wrapper, encoding="utf-8")
    png_path = OUT_DIR / "clean_plot_site_survey.png"

    with sync_playwright() as pw:
        browser = pw.chromium.launch()
        page = browser.new_page(viewport={"width": 1600, "height": 1150})
        page.goto(temp_html.resolve().as_uri(), wait_until="networkidle")
        page.screenshot(path=str(png_path))
        browser.close()
    temp_html.unlink(missing_ok=True)
    print(f"[+] Rendered Clean Plot PNG: {png_path}")

    # Copy all to Artifacts directory
    import shutil
    shutil.copy2(svg_path, ARTIFACT_DIR / "clean_plot_site_survey.svg")
    shutil.copy2(dxf_path, ARTIFACT_DIR / "clean_plot_site_survey.dxf")
    shutil.copy2(png_path, ARTIFACT_DIR / "clean_plot_site_survey.png")
    print(f"[+] Copied all clean plot deliverables to: {ARTIFACT_DIR}")


if __name__ == "__main__":
    generate_clean_plot()
