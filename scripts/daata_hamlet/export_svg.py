"""
DAATA HAMLET RESIDENCE - High-Precision Architectural SVG Drawing Generator
Produces presentation-grade architectural sheets:
1. Ground Floor Architectural Plan (Sheet A-101)
2. First Floor Architectural Plan (Sheet A-102)
3. Second Floor Architectural Plan (Sheet A-103)
4. Roof & Mumty Plan (Sheet A-104)
5. Structural Column & Grid Layout Plan (Sheet S-101)
6. Front South Elevation (Sheet A-201)
"""
from __future__ import annotations
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from shapely.geometry import Polygon, box as sbox, Point, MultiPolygon
from scripts.daata_hamlet.model import (
    build, PLOT, SITE_POINTS, SURVEY_SEGMENTS, GX, GY, COLUMN_SPEC,
    LEVEL, FLOOR_H, WALL_H, MUMTY_TOP, PARAPET_H, ROAD_Z, GRADE_Z,
    STAIR_X0, MID_X, LANE_S, LANE_N, TREAD, RISER, fi, column_rect,
    XB_O, XB_I, XC_W, XC_E, XD_W, XD_E, XE_I, XE_O, split_col, beam_segments
)

OUT_DIR = Path("blueprints/daata_hamlet")
OUT_DIR.mkdir(parents=True, exist_ok=True)


class SVGCanvas:
    """Architectural sheet canvas with title block, scales, and layers."""
    def __init__(self, width_px=1600, height_px=1150, title="FLOOR PLAN", sheet_no="A-101",
                 scale_text='SCALE: 1/8" = 1\'-0"', north_arrow=True):
        self.w = width_px
        self.h = height_px
        self.title = title
        self.sheet_no = sheet_no
        self.scale_text = scale_text
        self.north = north_arrow
        self.elements = []
        self.defs = []
        self.scale = 13.5  # px per foot
        self.ox = 180      # canvas origin x
        self.oy = 960      # canvas origin y (invert y for CAD)

    def wx(self, x: float) -> float:
        return self.ox + x * self.scale

    def wy(self, y: float) -> float:
        return self.oy - y * self.scale

    def rect(self, x0, y0, x1, y1, fill="none", stroke="#000", stroke_w=1, rx=0, dash="", cls=""):
        x = min(self.wx(x0), self.wx(x1))
        y = min(self.wy(y0), self.wy(y1))
        w = abs(self.wx(x1) - self.wx(x0))
        h = abs(self.wy(y1) - self.wy(y0))
        dash_attr = f' stroke-dasharray="{dash}"' if dash else ""
        self.elements.append(
            f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" '
            f'fill="{fill}" stroke="{stroke}" stroke-width="{stroke_w}" rx="{rx}"{dash_attr} class="{cls}"/>'
        )

    def polygon(self, pts, fill="none", stroke="#000", stroke_w=1, cls="", dash=""):
        svg_pts = " ".join(f"{self.wx(x):.1f},{self.wy(y):.1f}" for x, y in pts)
        dash_attr = f' stroke-dasharray="{dash}"' if dash else ""
        self.elements.append(
            f'<polygon points="{svg_pts}" fill="{fill}" stroke="{stroke}" stroke-width="{stroke_w}"{dash_attr} class="{cls}"/>'
        )

    def line(self, x0, y0, x1, y1, stroke="#000", stroke_w=1, dash="", cls=""):
        dash_attr = f' stroke-dasharray="{dash}"' if dash else ""
        self.elements.append(
            f'<line x1="{self.wx(x0):.1f}" y1="{self.wy(y0):.1f}" '
            f'x2="{self.wx(x1):.1f}" y2="{self.wy(y1):.1f}" '
            f'stroke="{stroke}" stroke-width="{stroke_w}"{dash_attr} class="{cls}"/>'
        )

    def circle(self, cx, cy, r_ft, fill="none", stroke="#000", stroke_w=1, cls=""):
        self.elements.append(
            f'<circle cx="{self.wx(cx):.1f}" cy="{self.wy(cy):.1f}" r="{r_ft * self.scale:.1f}" '
            f'fill="{fill}" stroke="{stroke}" stroke-width="{stroke_w}" class="{cls}"/>'
        )

    def _escape(self, s: str) -> str:
        return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

    def text(self, x, y, txt, size=12, fill="#000", anchor="middle", weight="normal", font="Arial, sans-serif", rot=0):
        transform = f' transform="rotate({rot} {self.wx(x):.1f} {self.wy(y):.1f})"' if rot else ""
        escaped_txt = self._escape(txt)
        self.elements.append(
            f'<text x="{self.wx(x):.1f}" y="{self.wy(y):.1f}" font-size="{size}" font-family="{font}" '
            f'font-weight="{weight}" text-anchor="{anchor}" fill="{fill}"{transform}>{escaped_txt}</text>'
        )

    def canvas_text(self, px, py, txt, size=12, fill="#000", anchor="start", weight="normal", font="Arial, sans-serif"):
        escaped_txt = self._escape(txt)
        self.elements.append(
            f'<text x="{px}" y="{py}" font-size="{size}" font-family="{font}" '
            f'font-weight="{weight}" text-anchor="{anchor}" fill="{fill}">{escaped_txt}</text>'
        )

    def canvas_line(self, x0, y0, x1, y1, stroke="#000", stroke_w=1, dash=""):
        dash_attr = f' stroke-dasharray="{dash}"' if dash else ""
        self.elements.append(f'<line x1="{x0}" y1="{y0}" x2="{x1}" y2="{y1}" stroke="{stroke}" stroke-width="{stroke_w}"{dash_attr}/>')

    def dim_h(self, x0, x1, y, offset_ft=2.5, txt=None):
        yd = y + offset_ft
        self.line(x0, yd, x1, yd, stroke="#2c3e50", stroke_w=1)
        self.line(x0, y, x0, yd + (0.5 if offset_ft >= 0 else -0.5), stroke="#7f8c8d", stroke_w=0.75)
        self.line(x1, y, x1, yd + (0.5 if offset_ft >= 0 else -0.5), stroke="#7f8c8d", stroke_w=0.75)
        t = 0.35
        self.line(x0 - t, yd - t, x0 + t, yd + t, stroke="#2c3e50", stroke_w=1.5)
        self.line(x1 - t, yd - t, x1 + t, yd + t, stroke="#2c3e50", stroke_w=1.5)
        label = txt if txt is not None else fi(abs(x1 - x0))
        self.text((x0 + x1) / 2, yd + 0.45, label, size=10, fill="#2c3e50", weight="bold")

    def dim_v(self, y0, y1, x, offset_ft=2.5, txt=None):
        xd = x + offset_ft
        self.line(xd, y0, xd, y1, stroke="#2c3e50", stroke_w=1)
        self.line(x, y0, xd + (0.5 if offset_ft >= 0 else -0.5), y0, stroke="#7f8c8d", stroke_w=0.75)
        self.line(x, y1, xd + (0.5 if offset_ft >= 0 else -0.5), y1, stroke="#7f8c8d", stroke_w=0.75)
        t = 0.35
        self.line(xd - t, y0 - t, xd + t, y0 + t, stroke="#2c3e50", stroke_w=1.5)
        self.line(xd - t, y1 - t, xd + t, y1 + t, stroke="#2c3e50", stroke_w=1.5)
        label = txt if txt is not None else fi(abs(y1 - y0))
        self.text(xd + (0.8 if offset_ft >= 0 else -0.8), (y0 + y1) / 2, label, size=10, fill="#2c3e50", weight="bold", rot=-90)

    def draw_door_swing(self, o):
        w = o.b - o.a
        if o.kind == "double":
            leaf = w / 2
            r = leaf * self.scale
            if o.orient == "x":
                self.line(o.a, o.line, o.a, o.line + o.swing * leaf, stroke="#8b4513", stroke_w=1.2)
                self.line(o.b, o.line, o.b, o.line + o.swing * leaf, stroke="#8b4513", stroke_w=1.2)
                sweep1 = 1 if o.swing > 0 else 0
                path1 = f'M {self.wx(o.a + leaf):.1f} {self.wy(o.line):.1f} A {r:.1f} {r:.1f} 0 0 {sweep1} {self.wx(o.a):.1f} {self.wy(o.line + o.swing * leaf):.1f}'
                sweep2 = 0 if o.swing > 0 else 1
                path2 = f'M {self.wx(o.b - leaf):.1f} {self.wy(o.line):.1f} A {r:.1f} {r:.1f} 0 0 {sweep2} {self.wx(o.b):.1f} {self.wy(o.line + o.swing * leaf):.1f}'
                self.elements.append(f'<path d="{path1}" fill="none" stroke="#b08d57" stroke-width="0.8" stroke-dasharray="2,2"/>')
                self.elements.append(f'<path d="{path2}" fill="none" stroke="#b08d57" stroke-width="0.8" stroke-dasharray="2,2"/>')
            else:
                self.line(o.line, o.a, o.line + o.swing * leaf, o.a, stroke="#8b4513", stroke_w=1.2)
                self.line(o.line, o.b, o.line + o.swing * leaf, o.b, stroke="#8b4513", stroke_w=1.2)
                sweep1 = 0 if o.swing > 0 else 1
                path1 = f'M {self.wx(o.line):.1f} {self.wy(o.a + leaf):.1f} A {r:.1f} {r:.1f} 0 0 {sweep1} {self.wx(o.line + o.swing * leaf):.1f} {self.wy(o.a):.1f}'
                sweep2 = 1 if o.swing > 0 else 0
                path2 = f'M {self.wx(o.line):.1f} {self.wy(o.b - leaf):.1f} A {r:.1f} {r:.1f} 0 0 {sweep2} {self.wx(o.line + o.swing * leaf):.1f} {self.wy(o.b):.1f}'
                self.elements.append(f'<path d="{path1}" fill="none" stroke="#b08d57" stroke-width="0.8" stroke-dasharray="2,2"/>')
                self.elements.append(f'<path d="{path2}" fill="none" stroke="#b08d57" stroke-width="0.8" stroke-dasharray="2,2"/>')
            return

        hx, hy = (o.a, o.line) if o.hinge == "a" else (o.b, o.line)
        if o.orient == "x":
            swing_dir = o.swing
            self.line(hx, hy, hx, hy + swing_dir * w, stroke="#8b4513", stroke_w=1.2)
            cx, cy = self.wx(hx), self.wy(hy)
            r = w * self.scale
            x_closed = self.wx(o.b if o.hinge == "a" else o.a)
            y_closed = self.wy(o.line)
            x_open = self.wx(hx)
            y_open = self.wy(hy + swing_dir * w)
            sweep = 1 if ((swing_dir > 0 and o.hinge == "a") or (swing_dir < 0 and o.hinge == "b")) else 0
            path = f'M {x_closed:.1f} {y_closed:.1f} A {r:.1f} {r:.1f} 0 0 {sweep} {x_open:.1f} {y_open:.1f}'
            self.elements.append(f'<path d="{path}" fill="none" stroke="#b08d57" stroke-width="0.8" stroke-dasharray="2,2"/>')
        else:
            swing_dir = o.swing
            self.line(hx, hy, hx + swing_dir * w, hy, stroke="#8b4513", stroke_w=1.2)
            cx, cy = self.wx(hx), self.wy(hy)
            r = w * self.scale
            x_closed = self.wx(o.line)
            y_closed = self.wy(o.b if o.hinge == "a" else o.a)
            x_open = self.wx(hx + swing_dir * w)
            y_open = self.wy(hy)
            sweep = 1 if ((swing_dir > 0 and o.hinge == "b") or (swing_dir < 0 and o.hinge == "a")) else 0
            path = f'M {x_closed:.1f} {y_closed:.1f} A {r:.1f} {r:.1f} 0 0 {sweep} {x_open:.1f} {y_open:.1f}'
            self.elements.append(f'<path d="{path}" fill="none" stroke="#b08d57" stroke-width="0.8" stroke-dasharray="2,2"/>')


    def draw_window_symbol(self, o):
        if o.orient == "x":
            self.line(o.a, o.line - 0.25, o.b, o.line - 0.25, stroke="#3498db", stroke_w=1.2)
            self.line(o.a, o.line + 0.25, o.b, o.line + 0.25, stroke="#3498db", stroke_w=1.2)
            self.line(o.a, o.line, o.b, o.line, stroke="#2980b9", stroke_w=0.8)
            self.line(o.a, o.line - 0.375, o.a, o.line + 0.375, stroke="#2c3e50", stroke_w=1.2)
            self.line(o.b, o.line - 0.375, o.b, o.line + 0.375, stroke="#2c3e50", stroke_w=1.2)
        else:
            self.line(o.line - 0.25, o.a, o.line - 0.25, o.b, stroke="#3498db", stroke_w=1.2)
            self.line(o.line + 0.25, o.a, o.line + 0.25, o.b, stroke="#3498db", stroke_w=1.2)
            self.line(o.line, o.a, o.line, o.b, stroke="#2980b9", stroke_w=0.8)
            self.line(o.line - 0.375, o.a, o.line + 0.375, o.a, stroke="#2c3e50", stroke_w=1.2)
            self.line(o.line - 0.375, o.b, o.line + 0.375, o.b, stroke="#2c3e50", stroke_w=1.2)

    def draw_vent_symbol(self, o):
        """Draw bathroom ventilator symbol (double line + 'V' label)."""
        if o.orient == "x":
            self.line(o.a, o.line - 0.25, o.b, o.line - 0.25, stroke="#e67e22", stroke_w=1.2)
            self.line(o.a, o.line + 0.25, o.b, o.line + 0.25, stroke="#e67e22", stroke_w=1.2)
            self.text((o.a + o.b) / 2, o.line - 0.5, "V", size=8, weight="bold", fill="#e67e22")
        else:
            self.line(o.line - 0.25, o.a, o.line - 0.25, o.b, stroke="#e67e22", stroke_w=1.2)
            self.line(o.line + 0.25, o.a, o.line + 0.25, o.b, stroke="#e67e22", stroke_w=1.2)
            self.text(o.line + 0.6, (o.a + o.b) / 2 - 0.3, "V", size=8, weight="bold", fill="#e67e22")

    def draw_angled_opening(self, ao):
        """Draw opening on an angled chamfer wall (door/window)."""
        x0, y0 = ao.p0
        x1, y1 = ao.p1
        dx, dy = x1 - x0, y1 - y0
        L = math.hypot(dx, dy)
        if L <= 0:
            return
        nx, ny = -dy / L, dx / L
        # Mask wall
        self.line(x0, y0, x1, y1, stroke="#ffffff", stroke_w=6)
        if ao.kind in ("window", "slide"):
            # Double window lines
            t = 0.25
            self.line(x0 + nx * t, y0 + ny * t, x1 + nx * t, y1 + ny * t, stroke="#3498db", stroke_w=1.2)
            self.line(x0 - nx * t, y0 - ny * t, x1 - nx * t, y1 - ny * t, stroke="#3498db", stroke_w=1.2)
            self.line(x0, y0, x1, y1, stroke="#2980b9", stroke_w=0.8)
        elif ao.kind in ("door", "double"):
            # Angled double door
            self.line(x0, y0, x0 - nx * (L / 2), y0 - ny * (L / 2), stroke="#8b4513", stroke_w=1.4)
            self.line(x1, y1, x1 - nx * (L / 2), y1 - ny * (L / 2), stroke="#8b4513", stroke_w=1.4)

    def draw_title_block(self):
        self.canvas_line(20, 20, self.w - 20, 20, stroke="#1a252f", stroke_w=2)
        self.canvas_line(self.w - 20, 20, self.w - 20, self.h - 20, stroke="#1a252f", stroke_w=2)
        self.canvas_line(self.w - 20, self.h - 20, 20, self.h - 20, stroke="#1a252f", stroke_w=2)
        self.canvas_line(20, self.h - 20, 20, 20, stroke="#1a252f", stroke_w=2)
        self.canvas_line(30, 30, self.w - 30, 30, stroke="#7f8c8d", stroke_w=0.75)
        self.canvas_line(self.w - 30, 30, self.w - 30, self.h - 30, stroke="#7f8c8d", stroke_w=0.75)
        self.canvas_line(self.w - 30, self.h - 30, 30, self.h - 30, stroke="#7f8c8d", stroke_w=0.75)
        self.canvas_line(30, self.h - 30, 30, 30, stroke="#7f8c8d", stroke_w=0.75)

        tb_w, tb_h = 520, 90
        tb_x = self.w - 30 - tb_w
        tb_y = self.h - 30 - tb_h
        self.elements.append(f'<rect x="{tb_x}" y="{tb_y}" width="{tb_w}" height="{tb_h}" fill="#ffffff" stroke="#1a252f" stroke-width="1.5"/>')
        self.canvas_line(tb_x, tb_y + 30, tb_x + tb_w, tb_y + 30, stroke="#bdc3c7", stroke_w=1)
        self.canvas_line(tb_x, tb_y + 60, tb_x + tb_w, tb_y + 60, stroke="#bdc3c7", stroke_w=1)
        self.canvas_line(tb_x + 370, tb_y + 30, tb_x + 370, tb_y + tb_h, stroke="#bdc3c7", stroke_w=1)

        self.canvas_text(tb_x + 14, tb_y + 20, "DAATA HAMLET RESIDENCE", size=14, weight="bold", fill="#2c3e50")
        self.canvas_text(tb_x + 385, tb_y + 20, "PLOT: 3,129.1 SQ.FT.", size=10, fill="#7f8c8d")
        self.canvas_text(tb_x + 14, tb_y + 48, f"DRAWING: {self.title}", size=11, weight="bold", fill="#16a085")
        self.canvas_text(tb_x + 385, tb_y + 48, f"SHEET: {self.sheet_no}", size=12, weight="bold", fill="#c0392b")
        self.canvas_text(tb_x + 14, tb_y + 78, f"{self.scale_text}  |  STATUS: APPROVED FOR CAD", size=9.5, fill="#7f8c8d")
        self.canvas_text(tb_x + 385, tb_y + 78, "UNITS: FEET-INCHES", size=10, fill="#2c3e50", weight="bold")

        if self.north:
            nx = self.w - 85
            ny = 90
            self.elements.append(
                f'<g transform="translate({nx},{ny})">'
                f'<circle cx="0" cy="0" r="26" fill="#ffffff" stroke="#2c3e50" stroke-width="1.5"/>'
                f'<polygon points="0,-22 7,16 0,10" fill="#2c3e50"/>'
                f'<polygon points="0,-22 -7,16 0,10" fill="#bdc3c7"/>'
                f'<text x="0" y="-26" font-size="12" font-family="Arial" font-weight="bold" text-anchor="middle" fill="#2c3e50">N</text>'
                f'</g>'
            )

    def to_svg(self) -> str:
        self.draw_title_block()
        defs_block = "\n".join(self.defs)
        content = "\n".join(self.elements)
        return (
            f'<?xml version="1.0" encoding="UTF-8"?>\n'
            f'<svg xmlns="http://www.w3.org/2000/svg" width="{self.w}" height="{self.h}" viewBox="0 0 {self.w} {self.h}">\n'
            f'<defs>\n'
            f'  <style>\n'
            f'    text {{ user-select: none; }}\n'
            f'    .grid-line {{ stroke: #bdc3c7; stroke-width: 0.8; stroke-dasharray: 4,4; }}\n'
            f'    .col-rcc {{ fill: #2c3e50; stroke: #1a252f; stroke-width: 1; }}\n'
            f'    .wall-brick {{ fill: #ecf0f1; stroke: #2c3e50; stroke-width: 1.5; }}\n'
            f'    .part-wall {{ fill: #f8f9fa; stroke: #7f8c8d; stroke-width: 1.2; }}\n'
            f'  </style>\n'
            f'  <pattern id="shaftHatch" width="8" height="8" patternUnits="userSpaceOnUse">\n'
            f'    <line x1="0" y1="0" x2="8" y2="8" stroke="#7f8c8d" stroke-width="1"/>\n'
            f'    <line x1="8" y1="0" x2="0" y2="8" stroke="#7f8c8d" stroke-width="1"/>\n'
            f'  </pattern>\n'
            f'  <pattern id="passageHatch" width="12" height="12" patternUnits="userSpaceOnUse">\n'
            f'    <line x1="0" y1="12" x2="12" y2="0" stroke="#bdc3c7" stroke-width="0.75"/>\n'
            f'  </pattern>\n'
            f'  {defs_block}\n'
            f'</defs>\n'
            f'<rect width="{self.w}" height="{self.h}" fill="#fcfdfd"/>\n'
            f'{content}\n'
            f'</svg>'
        )

    def save(self, filepath: Path):
        filepath.write_text(self.to_svg(), encoding="utf-8")
        print(f"[+] Exported architectural sheet: {filepath}")


# --------------------------------------------------------------------------
# DRAWING HELPERS
# --------------------------------------------------------------------------
def draw_structural_grid(canvas: SVGCanvas):
    for letter, x in GX.items():
        canvas.line(x, -5, x, 65, stroke="#bdc3c7", stroke_w=0.8, dash="5,5")
        by = -3.2
        canvas.circle(x, by, 1.25, fill="#ffffff", stroke="#2c3e50", stroke_w=1.2)
        canvas.text(x, by - 0.35, letter, size=11, weight="bold", fill="#2c3e50")
        ny = 67.5
        canvas.circle(x, ny, 1.35, fill="#ffffff", stroke="#2c3e50", stroke_w=1.2)
        canvas.text(x, ny - 0.4, letter, size=11, weight="bold", fill="#2c3e50")

    for num, y in GY.items():
        canvas.line(10, y, 92, y, stroke="#bdc3c7", stroke_w=0.8, dash="5,5")
        bx = 94.5
        canvas.circle(bx, y, 1.35, fill="#ffffff", stroke="#2c3e50", stroke_w=1.2)
        canvas.text(bx, y - 0.4, num, size=11, weight="bold", fill="#2c3e50")


def draw_columns_layer(canvas: SVGCanvas, m, floor_tag="GF"):
    for name, rect in m.columns.items():
        x0, y0, x1, y1 = rect
        canvas.rect(x0, y0, x1, y1, fill="#34495e", stroke="#1a252f", stroke_w=1.2, cls="col-rcc")
        canvas.line(x0, y0, x1, y1, stroke="#ecf0f1", stroke_w=0.5)
        canvas.line(x0, y1, x1, y0, stroke="#ecf0f1", stroke_w=0.5)


def draw_site_boundary(canvas: SVGCanvas):
    pts = [(x, y) for _, x, y in SITE_POINTS]
    canvas.polygon(pts, fill="none", stroke="#e74c3c", stroke_w=2.0)
    for name, x, y in SITE_POINTS:
        canvas.circle(x, y, 0.5, fill="#e74c3c", stroke="#ffffff", stroke_w=1)
        canvas.text(x + (1.5 if x < 50 else -1.5), y + (1.5 if y < 40 else -1.5),
                    name, size=10, weight="bold", fill="#c0392b")

    for p_a, p_b, dim_txt in SURVEY_SEGMENTS:
        pt_a = [(x, y) for n, x, y in SITE_POINTS if n == p_a][0]
        pt_b = [(x, y) for n, x, y in SITE_POINTS if n == p_b][0]
        mx, my = (pt_a[0] + pt_b[0]) / 2, (pt_a[1] + pt_b[1]) / 2
        dx, dy = pt_b[0] - pt_a[0], pt_b[1] - pt_a[1]
        length = math.hypot(dx, dy)
        if length > 0:
            nx, ny = -dy / length, dx / length
            canvas.text(mx + nx * 2.2, my + ny * 2.2 - 0.3, dim_txt, size=9, weight="bold", fill="#c0392b")


def draw_stair_plan(canvas: SVGCanvas, floor_code="GF"):
    # Compact U-Turn Dog-Leg Staircase: Width 6'-0" (X in [62.625, 68.625])
    # Mid-Landing sits directly atop Powder Room: Y in [20.5, 24.5] at +7'-0"

    # 1. Mid-Landing Slab at +7'-0" (Capping Powder Room)
    canvas.rect(STAIR_X0, 20.5, 68.625, 24.5, fill="#f4f6f7", stroke="#2c3e50", stroke_w=1.2)
    canvas.text((STAIR_X0 + 68.625) / 2, 23.8, "MID-LANDING (+7'-0\")", size=7.5, weight="bold", fill="#2c3e50")
    if floor_code == "GF":
        canvas.text((STAIR_X0 + 68.625) / 2, 22.8, "POWDER ROOM UNDER", size=7.0, weight="bold", fill="#16a085")
        canvas.text((STAIR_X0 + 68.625) / 2, 21.9, '6\'-0" \u00d7 4\'-0" (+7\' CLG)', size=6.0, fill="#7f8c8d")
        # Draw WC Commode symbol under landing (in lower-west zone)
        canvas.rect(63.6, 20.6, 65.0, 21.1, fill="#ffffff", stroke="#7f8c8d", stroke_w=0.8)
        canvas.circle(64.3, 21.45, 0.35, fill="#ffffff", stroke="#7f8c8d", stroke_w=0.8)
        # Vanity basin symbol under landing (in lower-east zone)
        canvas.rect(66.5, 20.6, 67.8, 21.1, fill="#ffffff", stroke="#7f8c8d", stroke_w=0.8)
        canvas.circle(67.15, 20.85, 0.25, fill="#ffffff", stroke="#7f8c8d", stroke_w=0.8)

    # 2. Central Handrail Divider
    canvas.line(65.50, 24.5, 65.50, 33.0, stroke="#2c3e50", stroke_w=1.2)
    canvas.line(65.75, 24.5, 65.75, 33.0, stroke="#2c3e50", stroke_w=1.2)

    # 3. Outer Stringers
    canvas.line(STAIR_X0, 24.5, STAIR_X0, 33.0, stroke="#2c3e50", stroke_w=1.2)
    canvas.line(68.625, 24.5, 68.625, 29.0, stroke="#2c3e50", stroke_w=1.2)

    # 4. Flight 1 (West Flight: X in [62.625, 65.50]):
    # Starts at Y = 33.0 in Lounge, rises SOUTH to Mid-Landing at Y = 24.5 (11 risers @ 7.64" to +7'-0")
    # 10 treads @ 0.85 ft
    tread_len = (33.0 - 24.5) / 10.0  # 0.85 ft
    for i in range(10):
        ty = 33.0 - i * tread_len
        is_overhead = (floor_code == "GF" and i >= 5)  # Steps 6-10 are above eye level (> 4.2 ft)
        dash = "3,3" if is_overhead else ""
        stroke_col = "#7f8c8d" if is_overhead else "#2c3e50"
        canvas.line(STAIR_X0, ty, 65.50, ty, stroke=stroke_col, stroke_w=1, dash=dash)
        if not is_overhead and i < 5:
            canvas.text((STAIR_X0 + 65.50) / 2, ty - tread_len / 2 - 0.3, str(i + 1), size=7.0, fill="#7f8c8d")

    # Diagonal Break Line on West Flight at step 5 (~Y = 28.75) on GF
    if floor_code == "GF":
        by = 33.0 - 5 * tread_len
        canvas.line(STAIR_X0 - 0.2, by + 0.4, 65.50 + 0.2, by - 0.4, stroke="#c0392b", stroke_w=1.5)
        canvas.line(STAIR_X0 - 0.2, by + 0.6, 65.50 + 0.2, by - 0.2, stroke="#c0392b", stroke_w=1.5)

    # Flight 1 UP Arrow (pointing South toward Landing)
    arr_x1 = (STAIR_X0 + 65.50) / 2
    canvas.line(arr_x1, 32.5, arr_x1, 29.5, stroke="#e67e22", stroke_w=1.5)
    canvas.circle(arr_x1, 32.5, 0.25, fill="#e67e22", stroke="#e67e22")
    canvas.polygon([(arr_x1, 29.0), (arr_x1 - 0.35, 29.7), (arr_x1 + 0.35, 29.7)], fill="#e67e22")
    canvas.text(arr_x1 - 1.1, 31.0, "UP (TO +7')", size=7.5, weight="bold", fill="#e67e22", rot=90)

    # 5. Flight 2 (East Flight: X in [65.75, 68.625]):
    # Starts at Mid-Landing at Y = 24.5 (+7'-0"), rises NORTH to 1F level (+10'-6" / +11'-0")
    # 5 treads @ 0.9 ft from Y = 24.5 to 29.0
    f2_tread = (29.0 - 24.5) / 5.0  # 0.9 ft
    for j in range(5):
        ty = 24.5 + (j + 1) * f2_tread
        dash = "3,3" if floor_code == "GF" else ""  # Overhead flight on GF
        stroke_col = "#7f8c8d" if floor_code == "GF" else "#2c3e50"
        canvas.line(65.75, ty, 68.625, ty, stroke=stroke_col, stroke_w=1, dash=dash)
        if floor_code != "GF":
            canvas.text((65.75 + 68.625) / 2, ty - f2_tread / 2 - 0.3, str(j + 12), size=7.0, fill="#7f8c8d")

    # Flight 2 UP Arrow (pointing North toward 1F)
    arr_x2 = (65.75 + 68.625) / 2
    canvas.line(arr_x2, 25.0, arr_x2, 28.0, stroke="#27ae60", stroke_w=1.2, dash="2,2" if floor_code == "GF" else "")
    canvas.circle(arr_x2, 25.0, 0.25, fill="#27ae60", stroke="#27ae60")
    canvas.polygon([(arr_x2, 28.5), (arr_x2 - 0.35, 27.8), (arr_x2 + 0.35, 27.8)], fill="#27ae60")
    canvas.text(arr_x2 + 1.1, 26.5, "UP TO 1F", size=7.5, weight="bold", fill="#27ae60", rot=-90)

    # Closing north header line for Flight 2
    canvas.line(65.75, 29.0, 68.625, 29.0, stroke="#2c3e50", stroke_w=1.2)


# --------------------------------------------------------------------------
# EXPORT SHEETS
# --------------------------------------------------------------------------
def generate_floor_sheet(m, floor_code: str, sheet_title: str, sheet_no: str, filename: str):
    canvas = SVGCanvas(title=sheet_title, sheet_no=sheet_no)

    draw_site_boundary(canvas)
    draw_structural_grid(canvas)

    # Landscape & Passage Zones (GF)
    if floor_code == "GF":
        for name, zone in m.zones.items():
            if name in ("BUILDING", "BOUNDARY WALL") or zone.is_empty:
                continue
            color = "#eafaf1" if "LAWN" in name or "GREEN" in name else "#f8f9fa"
            stroke_col = "#27ae60" if "LAWN" in name or "GREEN" in name else "#bdc3c7"
            if "PASSAGE" in name:
                fill_pat = "url(#passageHatch)"
            else:
                fill_pat = color
            if isinstance(zone, Polygon):
                canvas.polygon(list(zone.exterior.coords), fill=fill_pat, stroke=stroke_col, stroke_w=1)
            elif isinstance(zone, MultiPolygon):
                for p in zone.geoms:
                    canvas.polygon(list(p.exterior.coords), fill=fill_pat, stroke=stroke_col, stroke_w=1)

        canvas.text(18.0, 14.0, "MAIN LAWN", size=15, weight="bold", fill="#27ae60")
        canvas.text(18.0, 11.8, "(~590 SQ.FT OPEN GARDEN)", size=9.5, weight="bold", fill="#27ae60")
        canvas.text(18.0, 9.8, "STRICTLY RESERVED GREEN SPACE", size=8.0, fill="#2ecc71")
        canvas.text(80.5, 52.0, "NE SERVICE COURT", size=9.0, weight="bold", fill="#2c3e50")
        canvas.text(86.2, 26.0, "2'-1\" EAST PASSAGE", size=8.5, weight="bold", fill="#2980b9", rot=-90)
        canvas.text(50.0, -12.0, "PUBLIC ACCESS ROAD (87'-11\" FRONTAGE)", size=12, weight="bold", fill="#7f8c8d")

    # Upper Floor Terraces / Balconies
    if floor_code == "1F":
        canvas.rect(57.375, 0.0, XD_W, 20.5, fill="#fdfefe", stroke="#95a5a6", stroke_w=1, dash="4,4")
    elif floor_code == "2F":
        canvas.rect(XB_I, 0.0, XD_W, 20.5, fill="#fdfefe", stroke="#95a5a6", stroke_w=1, dash="4,4")
        canvas.rect(XB_I, 36.5, XE_O, 57.0, fill="#fdfefe", stroke="#95a5a6", stroke_w=1, dash="4,4")

    # Structural Walls & Partitions
    walls = m.walls.get(floor_code, [])
    for w in walls:
        canvas.rect(w.x0, w.y0, w.x1, w.y1, fill="#ffffff", stroke="#2c3e50", stroke_w=1.5)

    # Chamfer walls
    for p in m.prisms:
        if p.floor == floor_code and p.layer == "walls":
            canvas.polygon(list(p.poly.exterior.coords), fill="#ffffff", stroke="#2c3e50", stroke_w=1.5)

    # Columns
    draw_columns_layer(canvas, m, floor_code)

    # Openings
    ops = [o for o in m.openings if o.floor == floor_code]
    for o in ops:
        or_rect = o.rect(0.4)
        canvas.rect(or_rect[0], or_rect[1], or_rect[2], or_rect[3], fill="#ffffff", stroke="#ffffff", stroke_w=1)
        if o.kind in ("door", "double"):
            canvas.draw_door_swing(o)
        elif o.kind in ("window", "slide"):
            canvas.draw_window_symbol(o)
        elif o.kind == "vent":
            canvas.draw_vent_symbol(o)

    # Angled Openings
    for ao in m.angled_openings:
        if ao.floor == floor_code:
            canvas.draw_angled_opening(ao)

    # Stairs
    draw_stair_plan(canvas, floor_code)

    # Furniture Symbols
    for ftype, params, flabel in m.furniture.get(floor_code, []):
        if ftype == "rect":
            x0, y0, x1, y1 = params
            fill_col = "none" if (floor_code == "GF" and y0 < 18 and x0 < 36) else "#fdfefe"
            canvas.rect(x0, y0, x1, y1, fill=fill_col, stroke="#bdc3c7", stroke_w=0.8)
            if flabel:
                canvas.text((x0 + x1) / 2, (y0 + y1) / 2 - 0.3, flabel, size=8, fill="#7f8c8d")
        elif ftype == "circle":
            cx, cy, r = params
            canvas.circle(cx, cy, r, fill="#fdfefe", stroke="#bdc3c7", stroke_w=0.8)
            if flabel:
                canvas.text(cx, cy - 0.3, flabel, size=8, fill="#7f8c8d")


    # Room Names & Dimensions
    rooms = [r for r in m.rooms if r.floor == floor_code]
    for r in rooms:
        if r.kind == "shaft" or r.name == "MAIN LAWN" or "STAIR" in r.name or "POWDER" in r.name:
            continue
        if r.name == "LOBBY" and (r.poly.bounds[2] - r.poly.bounds[0] < 4.5):
            continue
        if r.label_xy is not None:
            rx, ry = r.label_xy
        else:
            rx, ry = (r.poly.bounds[0] + r.poly.bounds[2]) / 2, (r.poly.bounds[1] + r.poly.bounds[3]) / 2

        if "LIGHT COURT" in r.name or "OPEN AREA FOR LIGHTING" in r.name:
            if isinstance(r.poly, Polygon):
                canvas.polygon(list(r.poly.exterior.coords), fill="#e8f8f5", stroke="#16a085", stroke_w=1.2, dash="3,3")
            else:
                x0, y0, x1, y1 = r.poly.bounds
                canvas.rect(x0, y0, x1, y1, fill="#e8f8f5", stroke="#16a085", stroke_w=1.2, dash="3,3")
            canvas.text(rx, ry + 0.8, "OPEN AREA FOR LIGHTING", size=8.5, weight="bold", fill="#16a085")
            canvas.text(rx, ry - 0.2, "(OTS / SKYLIGHT)", size=8.0, weight="bold", fill="#16a085")
            continue

        is_compact = ("FOYER" in r.name or "STORE" in r.name or "BATH" in r.name or "DRESS" in r.name)
        fsize_title = 8.0 if is_compact else 11.0
        fsize_dims = 7.0 if is_compact else 9.0
        dy_title = 0.4 if is_compact else 0.6
        dy_dims = -0.5 if is_compact else -0.8

        canvas.text(rx, ry + dy_title, r.name, size=fsize_title, weight="bold", fill="#2c3e50")
        if r.show_dims:
            w_ft = r.poly.bounds[2] - r.poly.bounds[0]
            d_ft = r.poly.bounds[3] - r.poly.bounds[1]
            dim_str = f"{fi(w_ft)}  \u00d7  {fi(d_ft)}"
            canvas.text(rx, ry + dy_dims, dim_str, size=fsize_dims, weight="bold", fill="#7f8c8d")

    # Architectural Dimensions
    canvas.dim_h(XB_O, XE_O, 3.0, offset_ft=-4.0, txt=f"MAIN FACADE: {fi(XE_O - XB_O)}")
    canvas.dim_h(XB_O, XC_W, 3.0, offset_ft=-2.2, txt=f"BED-2: {fi(XC_W - XB_O)}")
    canvas.dim_h(XC_W, 56.625, 3.0, offset_ft=-2.2, txt="BATH: 5'-3\"")
    canvas.dim_h(57.375, XD_W, 3.0, offset_ft=-2.2, txt="PORCH: 11'-3\"")
    canvas.dim_h(XD_E, XE_O, 3.0, offset_ft=-2.2, txt=f"DRAWING: {fi(XE_O - XD_E)}")
    if floor_code == "GF":
        canvas.dim_h(0.0, XB_O, 3.0, offset_ft=-2.2, txt="MAIN LAWN: 36'-1\"")
        canvas.dim_h(XE_O, 87.21, 3.0, offset_ft=-2.2, txt="PASSAGE: 2'-1\"")

    canvas.dim_v(3.75, 19.75, XE_O, offset_ft=4.0)
    canvas.dim_v(20.5, 27.5, XE_O, offset_ft=4.0)
    canvas.dim_v(28.25, 35.625, XE_O, offset_ft=4.0)
    canvas.dim_v(36.375, 45.0 if floor_code == "1F" else 51.25, XE_O, offset_ft=4.0)
    canvas.dim_v(3.0, 52.0, XE_O, offset_ft=7.5, txt=f"OVERALL BUILDING DEPTH: {fi(49.0)}")

    canvas.save(OUT_DIR / filename)


def generate_column_grid_sheet(m):
    canvas = SVGCanvas(title="STRUCTURAL COLUMN & GRID LAYOUT", sheet_no="S-101",
                       scale_text='SCALE: 1/8" = 1\'-0"')
    draw_site_boundary(canvas)
    draw_structural_grid(canvas)

    for name, rect in m.columns.items():
        x0, y0, x1, y1 = rect
        canvas.rect(x0, y0, x1, y1, fill="#c0392b", stroke="#78281f", stroke_w=1.5)
        canvas.line(x0, y0, x1, y1, stroke="#ffffff", stroke_w=0.6)
        canvas.line(x0, y1, x1, y0, stroke="#ffffff", stroke_w=0.6)
        cx = (x0 + x1) / 2
        cy = (y0 + y1) / 2
        canvas.text(cx, cy + 1.8, name, size=10, weight="bold", fill="#c0392b")

    # Tie beam lines
    for a, b in beam_segments():
        al, an = split_col(a)
        bl, bn = split_col(b)
        ax, ay = GX[al], GY[an]
        bx, by = GX[bl], GY[bn]
        canvas.line(ax, ay, bx, by, stroke="#e67e22", stroke_w=1.2, dash="3,3")

    gl = [("A", GX["A"]), ("B", GX["B"]), ("C", GX["C"]), ("D", GX["D"]), ("E", GX["E"])]
    for (l1, x1), (l2, x2) in zip(gl, gl[1:]):
        canvas.dim_h(x1, x2, 0.0, offset_ft=-4.0, txt=f"{l1}-{l2}: {fi(x2 - x1)}")

    gn = list(GY.items())
    for (n1, y1), (n2, y2) in zip(gn, gn[1:]):
        canvas.dim_v(y1, y2, 85.5, offset_ft=4.0, txt=f"{n1}-{n2}: {fi(y2 - y1)}")

    # Schedule box
    sched_x, sched_y = 60, 80
    canvas.elements.append(
        f'<g transform="translate({sched_x},{sched_y})">'
        f'<rect x="0" y="0" width="340" height="240" fill="#ffffff" stroke="#2c3e50" stroke-width="1.5"/>'
        f'<text x="14" y="24" font-size="12" font-family="Arial" font-weight="bold" fill="#2c3e50">RCC COLUMN SCHEDULE (24 COLUMNS)</text>'
        f'<line x1="0" y1="34" x2="340" y2="34" stroke="#bdc3c7" stroke-width="1"/>'
        f'<text x="14" y="52" font-size="10" font-family="Arial" fill="#7f8c8d">MARK</text>'
        f'<text x="70" y="52" font-size="10" font-family="Arial" fill="#7f8c8d">SIZE (INCHES)</text>'
        f'<text x="170" y="52" font-size="10" font-family="Arial" fill="#7f8c8d">REBAR (MAIN)</text>'
        f'<text x="260" y="52" font-size="10" font-family="Arial" fill="#7f8c8d">EXTENT</text>'
        f'<line x1="0" y1="60" x2="340" y2="60" stroke="#bdc3c7" stroke-width="1"/>'
        f'<text x="14" y="80" font-size="10" font-family="Arial" font-weight="bold" fill="#2c3e50">C1 (A1-A2)</text>'
        f'<text x="70" y="80" font-size="10" font-family="Arial" fill="#2c3e50">12" \u00d7 18"</text>'
        f'<text x="170" y="80" font-size="10" font-family="Arial" fill="#2c3e50">8 \u00d7 #6 (3/4")</text>'
        f'<text x="260" y="80" font-size="10" font-family="Arial" fill="#2c3e50">GF \u2192 ROOF</text>'
        f'<text x="14" y="104" font-size="10" font-family="Arial" font-weight="bold" fill="#2c3e50">C2 (B, C, D, E)</text>'
        f'<text x="70" y="104" font-size="10" font-family="Arial" fill="#2c3e50">9" \u00d7 18"</text>'
        f'<text x="170" y="104" font-size="10" font-family="Arial" fill="#2c3e50">6 \u00d7 #6 (3/4")</text>'
        f'<text x="260" y="104" font-size="10" font-family="Arial" fill="#2c3e50">GF \u2192 ROOF</text>'
        f'<text x="14" y="128" font-size="10" font-family="Arial" font-weight="bold" fill="#2c3e50">C3 (MUMTY)</text>'
        f'<text x="70" y="128" font-size="10" font-family="Arial" fill="#2c3e50">9" \u00d7 18"</text>'
        f'<text x="170" y="128" font-size="10" font-family="Arial" fill="#2c3e50">6 \u00d7 #6 (3/4")</text>'
        f'<text x="260" y="128" font-size="10" font-family="Arial" fill="#2c3e50">GF \u2192 MUMTY</text>'
        f'<text x="14" y="152" font-size="10" font-family="Arial" font-weight="bold" fill="#2c3e50">C4 (CHAMFER)</text>'
        f'<text x="70" y="152" font-size="10" font-family="Arial" fill="#2c3e50">9" \u00d7 18"</text>'
        f'<text x="170" y="152" font-size="10" font-family="Arial" fill="#2c3e50">6 \u00d7 #6 (3/4")</text>'
        f'<text x="260" y="152" font-size="10" font-family="Arial" fill="#2c3e50">GF \u2192 ROOF</text>'
        f'<line x1="0" y1="164" x2="340" y2="164" stroke="#bdc3c7" stroke-width="1"/>'
        f'<text x="14" y="182" font-size="9" font-family="Arial" fill="#7f8c8d">\u2022 All 24 columns are parallel to each other.</text>'
        f'<text x="14" y="198" font-size="9" font-family="Arial" fill="#7f8c8d">\u2022 Concealed inside 9" walls without protrusions.</text>'
        f'<text x="14" y="214" font-size="9" font-family="Arial" fill="#7f8c8d">\u2022 Concrete: Class A (3,000 psi cylinder strength).</text>'
        f'<text x="14" y="230" font-size="9" font-family="Arial" fill="#7f8c8d">\u2022 Steel: Deformed Grade 60 (fy = 60,000 psi).</text>'
        f'</g>'
    )

    canvas.save(OUT_DIR / "05_column_grid_layout.svg")


def export_all():
    print("[*] Generating complete architectural drawing package...")
    m = build()
    generate_floor_sheet(m, "GF", "GROUND FLOOR ARCHITECTURAL PLAN", "A-101", "01_ground_floor_plan.svg")
    generate_floor_sheet(m, "1F", "FIRST FLOOR ARCHITECTURAL PLAN", "A-102", "02_first_floor_plan.svg")
    generate_floor_sheet(m, "2F", "SECOND FLOOR ARCHITECTURAL PLAN", "A-103", "03_second_floor_plan.svg")
    generate_floor_sheet(m, "RF", "ROOF & MUMTY PLAN", "A-104", "04_roof_mumty_plan.svg")
    generate_column_grid_sheet(m)
    print("[+] All 5 plan SVG drawings exported successfully to blueprints/daata_hamlet/")


if __name__ == "__main__":
    export_all()
