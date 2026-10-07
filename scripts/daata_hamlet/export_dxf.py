"""
DAATA HAMLET RESIDENCE - High-Precision Architectural DXF Exporter
Generates AutoCAD-compatible R2018 DXF files with industry-standard AIA layering:
- 0_BOUNDARY (Plot limits, boundary survey points)
- A_WALLS (Exterior and interior 9" / 4.5" masonry walls, VS-1 shaft)
- S_COLUMNS (Continuous 9"x18", 12"x18" structural RCC columns with solid hatch)
- S_BEAMS (RCC tie beams connecting columns along structural grid lines)
- A_DOORS (Door openings, leaves, and swing arcs)
- A_WINDOWS (Window frames and glazing centerlines)
- A_STAIRS (Flight steps, treads, risers, mid-landing, up arrows)
- A_ROOM_LABELS (Room program, dimensions, and floor areas)
- S_GRID_LINES (Column grid lines)
- S_GRID_BUBBLES (Numbered/lettered grid bubbles)
- A_DIMENSIONS (Exterior chain dimensions, overall spans, setbacks)
- A_CANOPY (Cantilevered concrete canopy, terraces, pergolas)
- A_ELEVATION_OUTLINE (Facade canopy silhouette, wall boundaries)
- A_ELEVATION_GLASS (Window frames and architectural glazing)
- A_LEVELS (Finished floor levels and elevation markers)
- G_TITLEBLOCK (Sheet titles and metadata)
"""
from __future__ import annotations
import math
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

import ezdxf
from ezdxf import colors
from shapely.geometry import Polygon, MultiPolygon
from scripts.daata_hamlet.model import (
    build, PLOT, SITE_POINTS, SURVEY_SEGMENTS, GX, GY, COLUMN_SPEC,
    LEVEL, FLOOR_H, WALL_H, MUMTY_TOP, PARAPET_H, ROAD_Z, GRADE_Z,
    STAIR_X0, STAIR_X1, MID_X, LANE_S, LANE_N, TREAD, RISER, fi, column_rect,
    XB_O, XB_I, XC_W, XC_E, XD_W, XD_E, XE_I, XE_O, beam_segments, split_col
)

OUT_DIR = Path("blueprints/daata_hamlet")
OUT_DIR.mkdir(parents=True, exist_ok=True)

LAYER_DEFS = {
    "0_BOUNDARY": {"color": colors.RED, "linetype": "Continuous"},
    "A_WALLS": {"color": colors.WHITE, "linetype": "Continuous"},
    "S_COLUMNS": {"color": colors.CYAN, "linetype": "Continuous"},
    "S_COLUMNS_HATCH": {"color": colors.BLUE, "linetype": "Continuous"},
    "S_BEAMS": {"color": colors.YELLOW, "linetype": "DASHED"},
    "A_DOORS": {"color": colors.YELLOW, "linetype": "Continuous"},
    "A_WINDOWS": {"color": colors.GREEN, "linetype": "Continuous"},
    "A_STAIRS": {"color": colors.GRAY, "linetype": "Continuous"},
    "A_ROOM_LABELS": {"color": colors.WHITE, "linetype": "Continuous"},
    "S_GRID_LINES": {"color": colors.MAGENTA, "linetype": "Continuous"},
    "S_GRID_BUBBLES": {"color": colors.MAGENTA, "linetype": "Continuous"},
    "A_DIMENSIONS": {"color": colors.RED, "linetype": "Continuous"},
    "A_CANOPY": {"color": colors.CYAN, "linetype": "Continuous"},
    "A_PERGOLA": {"color": colors.RED, "linetype": "Continuous"},
    "A_ELEVATION_OUTLINE": {"color": colors.WHITE, "linetype": "Continuous"},
    "A_ELEVATION_GLASS": {"color": colors.CYAN, "linetype": "Continuous"},
    "A_ELEVATION_FIN": {"color": colors.YELLOW, "linetype": "Continuous"},
    "A_LEVELS": {"color": colors.MAGENTA, "linetype": "Continuous"},
    "G_TITLEBLOCK": {"color": colors.WHITE, "linetype": "Continuous"},
}


def create_dxf_doc():
    doc = ezdxf.new("R2018")
    doc.header["$INSUNITS"] = 2  # 2 = Feet
    doc.header["$MEASUREMENT"] = 0  # English
    msp = doc.modelspace()
    for name, attrs in LAYER_DEFS.items():
        doc.layers.add(name, color=attrs["color"], linetype=attrs["linetype"])
    return doc, msp


def draw_poly_pts(msp, pts, layer: str):
    msp.add_lwpolyline([(x, y) for x, y in pts], format="xy", close=True, dxfattribs={"layer": layer})


def draw_shapely_polygon(msp, poly: Polygon, layer: str, x_offset=0.0, y_offset=0.0):
    if poly is None or poly.is_empty:
        return
    if isinstance(poly, MultiPolygon):
        for p in poly.geoms:
            draw_shapely_polygon(msp, p, layer, x_offset, y_offset)
        return
    pts = [(x + x_offset, y + y_offset) for x, y in poly.exterior.coords]
    msp.add_lwpolyline([(x, y) for x, y in pts], format="xy", close=True, dxfattribs={"layer": layer})
    for hole in poly.interiors:
        hpts = [(x + x_offset, y + y_offset) for x, y in hole.coords]
        msp.add_lwpolyline([(x, y) for x, y in hpts], format="xy", close=True, dxfattribs={"layer": layer})


def draw_boundary(msp, x_offset=0.0, y_offset=0.0):
    pts = [(x + x_offset, y + y_offset) for (_, x, y) in SITE_POINTS]
    draw_poly_pts(msp, pts, "0_BOUNDARY")
    for lbl, x, y in SITE_POINTS:
        px, py = x + x_offset, y + y_offset
        msp.add_circle((px, py), 0.5, dxfattribs={"layer": "0_BOUNDARY"})
        msp.add_text(lbl, height=0.8, dxfattribs={"layer": "0_BOUNDARY"}).set_placement(
            (px + 0.8, py + 0.8), align=ezdxf.enums.TextEntityAlignment.BOTTOM_LEFT
        )
    for p_a, p_b, dim_txt in SURVEY_SEGMENTS:
        pt_a = [(x, y) for n, x, y in SITE_POINTS if n == p_a][0]
        pt_b = [(x, y) for n, x, y in SITE_POINTS if n == p_b][0]
        mx = (pt_a[0] + pt_b[0]) / 2 + x_offset
        my = (pt_a[1] + pt_b[1]) / 2 + y_offset
        msp.add_text(f"{p_a}-{p_b}: {dim_txt}", height=0.7, dxfattribs={"layer": "0_BOUNDARY"}).set_placement(
            (mx, my), align=ezdxf.enums.TextEntityAlignment.MIDDLE_CENTER
        )


def draw_grid(msp, x_offset=0.0, y_offset=0.0):
    y_min, y_max = -4.0 + y_offset, 65.0 + y_offset
    for tag, x in GX.items():
        gx = x + x_offset
        msp.add_line((gx, y_min), (gx, y_max), dxfattribs={"layer": "S_GRID_LINES"})
        r = 1.2
        msp.add_circle((gx, y_min - r - 0.5), r, dxfattribs={"layer": "S_GRID_BUBBLES"})
        msp.add_text(tag, height=1.0, dxfattribs={"layer": "S_GRID_BUBBLES"}).set_placement(
            (gx, y_min - r - 0.5), align=ezdxf.enums.TextEntityAlignment.MIDDLE_CENTER
        )
        msp.add_circle((gx, y_max + r + 0.5), r, dxfattribs={"layer": "S_GRID_BUBBLES"})
        msp.add_text(tag, height=1.0, dxfattribs={"layer": "S_GRID_BUBBLES"}).set_placement(
            (gx, y_max + r + 0.5), align=ezdxf.enums.TextEntityAlignment.MIDDLE_CENTER
        )

    x_min, x_max = -5.0 + x_offset, 93.0 + x_offset
    for tag, y in GY.items():
        gy = y + y_offset
        msp.add_line((x_min, gy), (x_max, gy), dxfattribs={"layer": "S_GRID_LINES"})
        r = 1.2
        msp.add_circle((x_min - r - 0.5, gy), r, dxfattribs={"layer": "S_GRID_BUBBLES"})
        msp.add_text(tag, height=1.0, dxfattribs={"layer": "S_GRID_BUBBLES"}).set_placement(
            (x_min - r - 0.5, gy), align=ezdxf.enums.TextEntityAlignment.MIDDLE_CENTER
        )
        msp.add_circle((x_max + r + 0.5, gy), r, dxfattribs={"layer": "S_GRID_BUBBLES"})
        msp.add_text(tag, height=1.0, dxfattribs={"layer": "S_GRID_BUBBLES"}).set_placement(
            (x_max + r + 0.5, gy), align=ezdxf.enums.TextEntityAlignment.MIDDLE_CENTER
        )


def draw_columns(msp, floor_code: str, m, x_offset=0.0, y_offset=0.0):
    mumty_cols = {"D4", "E4", "D6", "E6"}
    for name, rect in m.columns.items():
        if floor_code == "RF" and name not in mumty_cols:
            continue
        x0, y0, x1, y1 = rect
        x0 += x_offset
        y0 += y_offset
        x1 += x_offset
        y1 += y_offset
        pts = [(x0, y0), (x1, y0), (x1, y1), (x0, y1)]
        draw_poly_pts(msp, pts, "S_COLUMNS")
        hatch = msp.add_hatch(color=colors.BLUE, dxfattribs={"layer": "S_COLUMNS_HATCH"})
        hatch.set_pattern_fill("SOLID")
        hatch.paths.add_polyline_path(pts, is_closed=True)
        cx = (x0 + x1) / 2
        cy = (y0 + y1) / 2
        msp.add_text(name, height=0.55, dxfattribs={"layer": "S_COLUMNS"}).set_placement(
            (cx, cy), align=ezdxf.enums.TextEntityAlignment.MIDDLE_CENTER
        )


def draw_walls(msp, floor_code: str, m, x_offset=0.0, y_offset=0.0):
    for w in m.walls.get(floor_code, []):
        x0 = w.x0 + x_offset
        y0 = w.y0 + y_offset
        x1 = w.x1 + x_offset
        y1 = w.y1 + y_offset
        draw_poly_pts(msp, [(x0, y0), (x1, y0), (x1, y1), (x0, y1)], "A_WALLS")
    for p in m.prisms:
        if p.floor == floor_code:
            draw_shapely_polygon(msp, p.poly, "A_WALLS", x_offset, y_offset)


def draw_openings(msp, floor_code: str, m, x_offset=0.0, y_offset=0.0):
    ops = [o for o in m.openings if o.floor == floor_code]
    for o in ops:
        w = o.b - o.a
        if o.kind in ("door", "double"):
            hx, hy = (o.a, o.line) if o.hinge == "a" else (o.b, o.line)
            hx += x_offset
            hy += y_offset
            if o.orient == "x":
                swing_dir = o.swing
                leaf_x = hx
                leaf_y = hy + swing_dir * w
                msp.add_line((hx, hy), (leaf_x, leaf_y), dxfattribs={"layer": "A_DOORS"})
                start_ang = 0 if swing_dir > 0 else 270
                end_ang = 90 if swing_dir > 0 else 360
                msp.add_arc((hx, hy), radius=w, start_angle=start_ang, end_angle=end_ang, dxfattribs={"layer": "A_DOORS"})
            else:
                swing_dir = o.swing
                leaf_x = hx + swing_dir * w
                leaf_y = hy
                msp.add_line((hx, hy), (leaf_x, leaf_y), dxfattribs={"layer": "A_DOORS"})
                start_ang = 0 if swing_dir > 0 else 90
                end_ang = 90 if swing_dir > 0 else 180
                msp.add_arc((hx, hy), radius=w, start_angle=start_ang, end_angle=end_ang, dxfattribs={"layer": "A_DOORS"})
            msp.add_text(o.name, height=0.6, dxfattribs={"layer": "A_DOORS"}).set_placement(
                (hx + 0.5, hy + 0.5), align=ezdxf.enums.TextEntityAlignment.MIDDLE_CENTER
            )
        elif o.kind in ("window", "slide"):
            if o.orient == "x":
                x0 = o.a + x_offset
                x1 = o.b + x_offset
                y_c = o.line + y_offset
                msp.add_line((x0, y_c - 0.375), (x1, y_c - 0.375), dxfattribs={"layer": "A_WINDOWS"})
                msp.add_line((x0, y_c + 0.375), (x1, y_c + 0.375), dxfattribs={"layer": "A_WINDOWS"})
                msp.add_line((x0, y_c), (x1, y_c), dxfattribs={"layer": "A_WINDOWS"})
                msp.add_text(o.name, height=0.6, dxfattribs={"layer": "A_WINDOWS"}).set_placement(
                    ((x0 + x1) / 2, y_c + 0.7), align=ezdxf.enums.TextEntityAlignment.MIDDLE_CENTER
                )
            else:
                y0 = o.a + y_offset
                y1 = o.b + y_offset
                x_c = o.line + x_offset
                msp.add_line((x_c - 0.375, y0), (x_c - 0.375, y1), dxfattribs={"layer": "A_WINDOWS"})
                msp.add_line((x_c + 0.375, y0), (x_c + 0.375, y1), dxfattribs={"layer": "A_WINDOWS"})
                msp.add_line((x_c, y0), (x_c, y1), dxfattribs={"layer": "A_WINDOWS"})
                msp.add_text(o.name, height=0.6, dxfattribs={"layer": "A_WINDOWS"}).set_placement(
                    (x_c + 0.7, (y0 + y1) / 2), align=ezdxf.enums.TextEntityAlignment.MIDDLE_CENTER
                )
        elif o.kind == "vent":
            if o.orient == "x":
                x0 = o.a + x_offset
                x1 = o.b + x_offset
                y_c = o.line + y_offset
                msp.add_line((x0, y_c - 0.25), (x1, y_c - 0.25), dxfattribs={"layer": "A_WINDOWS"})
                msp.add_line((x0, y_c + 0.25), (x1, y_c + 0.25), dxfattribs={"layer": "A_WINDOWS"})
                msp.add_text("V", height=0.5, dxfattribs={"layer": "A_WINDOWS"}).set_placement(
                    ((x0 + x1) / 2, y_c - 0.6), align=ezdxf.enums.TextEntityAlignment.MIDDLE_CENTER
                )
            else:
                y0 = o.a + y_offset
                y1 = o.b + y_offset
                x_c = o.line + x_offset
                msp.add_line((x_c - 0.25, y0), (x_c - 0.25, y1), dxfattribs={"layer": "A_WINDOWS"})
                msp.add_line((x_c + 0.25, y0), (x_c + 0.25, y1), dxfattribs={"layer": "A_WINDOWS"})
                msp.add_text("V", height=0.5, dxfattribs={"layer": "A_WINDOWS"}).set_placement(
                    (x_c + 0.6, (y0 + y1) / 2), align=ezdxf.enums.TextEntityAlignment.MIDDLE_CENTER
                )

    for ao in m.angled_openings:
        if ao.floor == floor_code:
            p0 = (ao.p0[0] + x_offset, ao.p0[1] + y_offset)
            p1 = (ao.p1[0] + x_offset, ao.p1[1] + y_offset)
            msp.add_line(p0, p1, dxfattribs={"layer": "A_WINDOWS"})
            mid_x = (p0[0] + p1[0]) / 2
            mid_y = (p0[1] + p1[1]) / 2
            msp.add_text(ao.name, height=0.6, dxfattribs={"layer": "A_WINDOWS"}).set_placement(
                (mid_x, mid_y + 0.5), align=ezdxf.enums.TextEntityAlignment.MIDDLE_CENTER
            )


def draw_stairs(msp, x_offset=0.0, y_offset=0.0):
    # Compact U-Turn Dog-Leg Staircase: Width 6'-0" (X in [62.625, 68.625])
    # Mid-Landing sits directly atop Powder Room: Y in [20.5, 24.5] at +7'-0"
    draw_poly_pts(msp, [
        (STAIR_X0 + x_offset, 20.5 + y_offset),
        (68.625 + x_offset, 20.5 + y_offset),
        (68.625 + x_offset, 24.5 + y_offset),
        (STAIR_X0 + x_offset, 24.5 + y_offset)
    ], "A_STAIRS")
    msp.add_text("MID-LANDING (+7'-0\")", height=0.7, dxfattribs={"layer": "A_STAIRS"}).set_placement(
        ((STAIR_X0 + 68.625) / 2 + x_offset, 23.3 + y_offset), align=ezdxf.enums.TextEntityAlignment.MIDDLE_CENTER
    )
    msp.add_text("POWDER ROOM UNDER (+7' CLG)", height=0.55, dxfattribs={"layer": "A_STAIRS"}).set_placement(
        ((STAIR_X0 + 68.625) / 2 + x_offset, 22.0 + y_offset), align=ezdxf.enums.TextEntityAlignment.MIDDLE_CENTER
    )

    # Central divider rail
    msp.add_line((65.50 + x_offset, 24.5 + y_offset), (65.50 + x_offset, 33.0 + y_offset), dxfattribs={"layer": "A_STAIRS"})
    msp.add_line((65.75 + x_offset, 24.5 + y_offset), (65.75 + x_offset, 33.0 + y_offset), dxfattribs={"layer": "A_STAIRS"})

    # Outer stringers
    msp.add_line((STAIR_X0 + x_offset, 24.5 + y_offset), (STAIR_X0 + x_offset, 33.0 + y_offset), dxfattribs={"layer": "A_STAIRS"})
    msp.add_line((68.625 + x_offset, 24.5 + y_offset), (68.625 + x_offset, 29.0 + y_offset), dxfattribs={"layer": "A_STAIRS"})
    msp.add_line((65.75 + x_offset, 29.0 + y_offset), (68.625 + x_offset, 29.0 + y_offset), dxfattribs={"layer": "A_STAIRS"})

    # Flight 1 (West flight: X in [62.625, 65.50]): Rises South from Lounge at Y = 33.0 to Mid-Landing at Y = 24.5
    tread_len = (33.0 - 24.5) / 10.0  # 0.85 ft
    for i in range(10):
        ty = 33.0 - i * tread_len + y_offset
        lt = "DASHED" if i >= 5 else "Continuous"
        msp.add_line((STAIR_X0 + x_offset, ty), (65.50 + x_offset, ty), dxfattribs={"layer": "A_STAIRS", "linetype": lt})
        if i < 5:
            msp.add_text(str(i + 1), height=0.5, dxfattribs={"layer": "A_STAIRS"}).set_placement(
                ((STAIR_X0 + 65.50) / 2 + x_offset, ty - tread_len / 2), align=ezdxf.enums.TextEntityAlignment.MIDDLE_CENTER
            )

    # Flight 1 UP Arrow
    arr_x1 = (STAIR_X0 + 65.50) / 2 + x_offset
    msp.add_line((arr_x1, 32.5 + y_offset), (arr_x1, 29.5 + y_offset), dxfattribs={"layer": "A_STAIRS"})
    msp.add_text("UP (TO +7')", height=0.6, dxfattribs={"layer": "A_STAIRS"}).set_placement(
        (arr_x1 - 0.8, 31.0 + y_offset), align=ezdxf.enums.TextEntityAlignment.MIDDLE_CENTER
    )

    # Flight 2 (East flight: X in [65.75, 68.625]): Rises North from Mid-Landing at Y = 24.5 to 1F level at Y = 29.0
    f2_tread = (29.0 - 24.5) / 5.0
    for j in range(5):
        ty = 24.5 + (j + 1) * f2_tread + y_offset
        msp.add_line((65.75 + x_offset, ty), (68.625 + x_offset, ty), dxfattribs={"layer": "A_STAIRS", "linetype": "DASHED"})

    # Flight 2 UP Arrow
    arr_x2 = (65.75 + 68.625) / 2 + x_offset
    msp.add_line((arr_x2, 25.0 + y_offset), (arr_x2, 28.0 + y_offset), dxfattribs={"layer": "A_STAIRS", "linetype": "DASHED"})
    msp.add_text("UP TO 1F", height=0.6, dxfattribs={"layer": "A_STAIRS"}).set_placement(
        (arr_x2 + 0.8, 26.5 + y_offset), align=ezdxf.enums.TextEntityAlignment.MIDDLE_CENTER
    )


def draw_rooms(msp, floor_code: str, m, x_offset=0.0, y_offset=0.0):
    rooms = [r for r in m.rooms if r.floor == floor_code]
    for r in rooms:
        if r.kind == "shaft" or "STAIR" in r.name or "POWDER" in r.name:
            continue
        if r.label_xy is not None:
            rx, ry = r.label_xy
        else:
            rx = (r.poly.bounds[0] + r.poly.bounds[2]) / 2
            ry = (r.poly.bounds[1] + r.poly.bounds[3]) / 2
        cx = rx + x_offset
        cy = ry + y_offset
        msp.add_text(r.name, height=0.9, dxfattribs={"layer": "A_ROOM_LABELS"}).set_placement(
            (cx, cy + 0.6), align=ezdxf.enums.TextEntityAlignment.MIDDLE_CENTER
        )
        if r.show_dims:
            w_ft = r.poly.bounds[2] - r.poly.bounds[0]
            d_ft = r.poly.bounds[3] - r.poly.bounds[1]
            dim_str = f"{fi(w_ft)} x {fi(d_ft)}"
            msp.add_text(dim_str, height=0.75, dxfattribs={"layer": "A_ROOM_LABELS"}).set_placement(
                (cx, cy - 0.5), align=ezdxf.enums.TextEntityAlignment.MIDDLE_CENTER
            )
        msp.add_text(f"({int(r.poly.area)} sq.ft)", height=0.65, dxfattribs={"layer": "A_ROOM_LABELS"}).set_placement(
            (cx, cy - 1.4), align=ezdxf.enums.TextEntityAlignment.MIDDLE_CENTER
        )


def draw_dimensions(msp, x_offset=0.0, y_offset=0.0):
    p1 = (0.0 + x_offset, -6.0 + y_offset)
    p2 = (87.917 + x_offset, -6.0 + y_offset)
    msp.add_line(p1, p2, dxfattribs={"layer": "A_DIMENSIONS"})
    msp.add_line((p1[0], p1[1] - 0.8), (p1[0], p1[1] + 6.0), dxfattribs={"layer": "A_DIMENSIONS"})
    msp.add_line((p2[0], p2[1] - 0.8), (p2[0], p2[1] + 6.0), dxfattribs={"layer": "A_DIMENSIONS"})
    msp.add_text("OVERALL PLOT FRONTAGE = 87'-11\"", height=1.0, dxfattribs={"layer": "A_DIMENSIONS"}).set_placement(
        ((p1[0] + p2[0]) / 2, p1[1] - 1.5), align=ezdxf.enums.TextEntityAlignment.MIDDLE_CENTER
    )

    tags = ["A", "B", "C", "D", "E"]
    y_dim = -3.0 + y_offset
    for i in range(len(tags) - 1):
        x_a = GX[tags[i]] + x_offset
        x_b = GX[tags[i + 1]] + x_offset
        msp.add_line((x_a, y_dim), (x_b, y_dim), dxfattribs={"layer": "A_DIMENSIONS"})
        msp.add_line((x_a, y_dim - 0.5), (x_a, y_dim + 0.5), dxfattribs={"layer": "A_DIMENSIONS"})
        msp.add_line((x_b, y_dim - 0.5), (x_b, y_dim + 0.5), dxfattribs={"layer": "A_DIMENSIONS"})
        bay_w = fi(GX[tags[i + 1]] - GX[tags[i]])
        msp.add_text(bay_w, height=0.7, dxfattribs={"layer": "A_DIMENSIONS"}).set_placement(
            ((x_a + x_b) / 2, y_dim + 0.8), align=ezdxf.enums.TextEntityAlignment.MIDDLE_CENTER
        )


def draw_floor_sheet(msp, m, floor_code: str, title: str, x_offset=0.0, y_offset=0.0):
    draw_boundary(msp, x_offset, y_offset)
    draw_grid(msp, x_offset, y_offset)
    draw_columns(msp, floor_code, m, x_offset, y_offset)
    draw_walls(msp, floor_code, m, x_offset, y_offset)
    draw_openings(msp, floor_code, m, x_offset, y_offset)
    draw_stairs(msp, x_offset, y_offset)
    draw_rooms(msp, floor_code, m, x_offset, y_offset)
    draw_dimensions(msp, x_offset, y_offset)


    if floor_code == "GF":
        for name, zone in m.zones.items():
            if name not in ("BUILDING", "BOUNDARY WALL"):
                draw_shapely_polygon(msp, zone, "A_CANOPY", x_offset, y_offset)
    elif floor_code == "1F":
        # Porch terrace (West)
        draw_poly_pts(msp, [
            (17.5 + x_offset, 0.0 + y_offset),
            (XB_I + x_offset, 0.0 + y_offset),
            (XB_I + x_offset, 18.0 + y_offset),
            (17.5 + x_offset, 18.0 + y_offset)
        ], "A_CANOPY")
        msp.add_text("OPEN TERRACE OVER PORCH", height=1.0, dxfattribs={"layer": "A_CANOPY"}).set_placement(
            (27.0 + x_offset, 9.0 + y_offset), align=ezdxf.enums.TextEntityAlignment.MIDDLE_CENTER
        )
        # Utility terrace over dirty kitchen (North East)
        draw_poly_pts(msp, [
            (XD_W + x_offset, 45.75 + y_offset),
            (XE_O + x_offset, 45.75 + y_offset),
            (XE_O + x_offset, 52.0 + y_offset),
            (XD_W + x_offset, 52.0 + y_offset)
        ], "A_CANOPY")
        msp.add_text("UTILITY TERRACE", height=1.0, dxfattribs={"layer": "A_CANOPY"}).set_placement(
            ((XD_W + XE_O) / 2 + x_offset, 48.875 + y_offset), align=ezdxf.enums.TextEntityAlignment.MIDDLE_CENTER
        )
    elif floor_code == "2F":
        # Front Sun Terrace (Open to sky)
        draw_poly_pts(msp, [
            (XB_I + x_offset, 0.0 + y_offset),
            (XC_W + x_offset, 0.0 + y_offset),
            (XC_W + x_offset, 20.5 + y_offset),
            (XB_I + x_offset, 20.5 + y_offset)
        ], "A_CANOPY")
        msp.add_text("FRONT SUN TERRACE (OPEN TO SKY)", height=1.0, dxfattribs={"layer": "A_CANOPY"}).set_placement(
            ((XB_I + XC_W) / 2 + x_offset, 10.25 + y_offset), align=ezdxf.enums.TextEntityAlignment.MIDDLE_CENTER
        )
        # Rear Terraces
        draw_poly_pts(msp, [
            (XB_O + x_offset, 20.5 + y_offset),
            (XC_W + x_offset, 20.5 + y_offset),
            (XC_W + x_offset, 33.75 + y_offset),
            (XB_O + x_offset, 33.75 + y_offset)
        ], "A_CANOPY")
        draw_poly_pts(msp, [
            (XC_W + x_offset, 28.25 + y_offset),
            (XD_W + x_offset, 28.25 + y_offset),
            (XD_W + x_offset, 42.5 + y_offset),
            (XC_W + x_offset, 42.5 + y_offset)
        ], "A_CANOPY")

    msp.add_text(title, height=2.0, dxfattribs={"layer": "G_TITLEBLOCK"}).set_placement(
        (44.0 + x_offset, -9.0 + y_offset), align=ezdxf.enums.TextEntityAlignment.MIDDLE_CENTER
    )
    msp.add_text("DAATA HAMLET RESIDENCE | CANOPY ARCHITECTURE", height=1.2, dxfattribs={"layer": "G_TITLEBLOCK"}).set_placement(
        (44.0 + x_offset, -11.0 + y_offset), align=ezdxf.enums.TextEntityAlignment.MIDDLE_CENTER
    )


def export_all():
    print("[*] Generating complete AutoCAD DXF architectural drawing package...")
    m = build()

    plans = [
        ("GF", "GROUND FLOOR ARCHITECTURAL PLAN", "01_ground_floor_plan.dxf"),
        ("1F", "FIRST FLOOR ARCHITECTURAL PLAN", "02_first_floor_plan.dxf"),
        ("2F", "SECOND FLOOR ARCHITECTURAL PLAN", "03_second_floor_plan.dxf"),
        ("RF", "ROOF & MUMTY PLAN", "04_roof_mumty_plan.dxf"),
    ]

    for fl, title, fname in plans:
        doc, msp = create_dxf_doc()
        draw_floor_sheet(msp, m, fl, title, 0.0, 0.0)
        out_path = OUT_DIR / fname
        doc.saveas(out_path)
        print(f"[+] Exported DXF: {out_path}")

    # Column Grid Structural Plan
    doc_g, msp_g = create_dxf_doc()
    draw_boundary(msp_g, 0.0, 0.0)
    draw_grid(msp_g, 0.0, 0.0)
    draw_columns(msp_g, "GF", m, 0.0, 0.0)

    # Tie Beams
    for a, b in beam_segments():
        al, an = split_col(a)
        bl, bn = split_col(b)
        ax, ay = GX[al], GY[an]
        bx, by = GX[bl], GY[bn]
        msp_g.add_line((ax, ay), (bx, by), dxfattribs={"layer": "S_BEAMS"})

    draw_dimensions(msp_g, 0.0, 0.0)
    msp_g.add_text("STRUCTURAL COLUMN GRID & FOUNDATION AXES", height=2.0, dxfattribs={"layer": "G_TITLEBLOCK"}).set_placement(
        (44.0, -9.0), align=ezdxf.enums.TextEntityAlignment.MIDDLE_CENTER
    )

    # Schedule notes in structural sheet
    sx, sy = -3.0, 48.0
    msp_g.add_text("RCC COLUMN SCHEDULE & SPECIFICATIONS", height=1.0, dxfattribs={"layer": "G_TITLEBLOCK"}).set_placement(
        (sx, sy), align=ezdxf.enums.TextEntityAlignment.BOTTOM_LEFT
    )
    notes = [
        "1. C1 (A1-A2): 12\"x18\" RCC Column, 8 x #6 (3/4\") Rebar, Extent: GF -> ROOF",
        "2. C2 (B, C, D, E): 9\"x18\" RCC Column, 6 x #6 (3/4\") Rebar, Extent: GF -> ROOF",
        "3. C3 (D4, E4, D6, E6): 9\"x18\" RCC Column, 6 x #6 (3/4\") Rebar, Extent: GF -> MUMTY (+42'-0\")",
        "4. C4 (B'5, C'7, D'8): 9\"x18\" Chamfer Terminal Columns, 6 x #6 Rebar, Extent: GF -> ROOF",
        "5. All 24 columns are strictly parallel along orthogonal grid axes and concealed in 9\" walls.",
        "6. Concrete: Class A (3,000 psi cylinder strength). Steel: Deformed Grade 60 (fy = 60,000 psi)."
    ]
    for idx, note in enumerate(notes):
        msp_g.add_text(note, height=0.6, dxfattribs={"layer": "G_TITLEBLOCK"}).set_placement(
            (sx, sy - 1.5 - idx * 1.2), align=ezdxf.enums.TextEntityAlignment.BOTTOM_LEFT
        )

    out_grid = OUT_DIR / "05_column_grid_structural.dxf"
    doc_g.saveas(out_grid)
    print(f"[+] Exported DXF: {out_grid}")

    # South Elevation
    doc_e, msp_e = create_dxf_doc()
    msp_e.add_line((-5.0, 0.0), (95.0, 0.0), dxfattribs={"layer": "A_LEVELS"})
    levels = [
        ("FINISHED GROUND LEVEL 0.00'", 0.0),
        ("PLINTH LEVEL +1'-6\"", 1.5),
        ("FIRST FLOOR FFL +11'-0\"", 11.0),
        ("SECOND FLOOR FFL +22'-0\"", 22.0),
        ("ROOF LEVEL +33'-0\"", 33.0),
        ("MUMTY TOP +42'-0\"", 42.0),
    ]
    for lbl, z in levels:
        msp_e.add_line((-5.0, z), (95.0, z), dxfattribs={"layer": "A_LEVELS"})
        msp_e.add_text(lbl, height=0.8, dxfattribs={"layer": "A_LEVELS"}).set_placement(
            (-6.0, z), align=ezdxf.enums.TextEntityAlignment.MIDDLE_RIGHT
        )

    # Ground Floor Building Facade (X from XB_O to XE_O)
    draw_poly_pts(msp_e, [(XB_O, 0.0), (XE_O, 0.0), (XE_O, 11.0), (XB_O, 11.0)], "A_ELEVATION_OUTLINE")
    # Ground Floor Windows & Openings:
    # 1. Bedroom 2 Sliding Door to Lawn (X in [39.5, 48.0], Z in [1.5, 8.5])
    draw_poly_pts(msp_e, [(39.5, 1.5), (48.0, 1.5), (48.0, 8.5), (39.5, 8.5)], "A_ELEVATION_GLASS")
    msp_e.add_text("SL-BED2 (GARDEN)", height=0.6, dxfattribs={"layer": "A_ROOM_LABELS"}).set_placement((43.75, 5.0), align=ezdxf.enums.TextEntityAlignment.MIDDLE_CENTER)
    # 2. Central Car Porch Opening & 6ft Main Entrance Door (X in [56.625, 68.625])
    draw_poly_pts(msp_e, [(56.625, 0.0), (56.625, 11.0), (68.625, 11.0), (68.625, 0.0)], "S_COLUMNS")
    draw_poly_pts(msp_e, [(56.625, 1.5), (62.625, 1.5), (62.625, 9.5), (56.625, 9.5)], "A_DOORS")
    msp_e.add_text("6FT MAIN ENTRY", height=0.6, dxfattribs={"layer": "A_ROOM_LABELS"}).set_placement((59.625, 5.5), align=ezdxf.enums.TextEntityAlignment.MIDDLE_CENTER)
    draw_poly_pts(msp_e, [(63.5, 6.5), (66.5, 6.5), (66.5, 8.0), (63.5, 8.0)], "A_ELEVATION_GLASS")
    msp_e.add_text("V-POWDER", height=0.5, dxfattribs={"layer": "A_ROOM_LABELS"}).set_placement((65.0, 7.25), align=ezdxf.enums.TextEntityAlignment.MIDDLE_CENTER)
    # 3. Formal Drawing Room Picture Window (X in [72.0, 81.0], Z in [2.0, 8.5])
    draw_poly_pts(msp_e, [(72.0, 2.0), (81.0, 2.0), (81.0, 8.5), (72.0, 8.5)], "A_ELEVATION_GLASS")
    msp_e.add_text("W-DRAWING (9'x6'-6\")", height=0.6, dxfattribs={"layer": "A_ROOM_LABELS"}).set_placement((76.5, 5.5), align=ezdxf.enums.TextEntityAlignment.MIDDLE_CENTER)

    # Porch Canopy Fascia (Z in [11.0, 11.75])
    draw_poly_pts(msp_e, [(55.5, 11.0), (69.5, 11.0), (69.5, 11.75), (55.5, 11.75)], "A_CANOPY")
    # 1F Balcony Glass Railing over Car Porch (X in [56.625, 68.625], Z in [11.0, 14.5])
    draw_poly_pts(msp_e, [(56.625, 11.0), (68.625, 11.0), (68.625, 14.5), (56.625, 14.5)], "A_ELEVATION_GLASS")
    msp_e.add_text("1F BALCONY GLASS RAILING", height=0.6, dxfattribs={"layer": "A_ROOM_LABELS"}).set_placement((62.625, 12.75), align=ezdxf.enums.TextEntityAlignment.MIDDLE_CENTER)

    # First Floor Facade & Windows (Z in [11.0, 22.0])
    draw_poly_pts(msp_e, [(XB_O, 11.0), (XE_O, 11.0), (XE_O, 22.0), (XB_O, 22.0)], "A_ELEVATION_OUTLINE")
    draw_poly_pts(msp_e, [(40.5, 14.0), (47.5, 14.0), (47.5, 19.5), (40.5, 19.5)], "A_ELEVATION_GLASS")
    msp_e.add_text("W-BED4", height=0.6, dxfattribs={"layer": "A_ROOM_LABELS"}).set_placement((44.0, 16.5), align=ezdxf.enums.TextEntityAlignment.MIDDLE_CENTER)
    draw_poly_pts(msp_e, [(72.5, 14.0), (80.5, 14.0), (80.5, 19.5), (72.5, 19.5)], "A_ELEVATION_GLASS")
    msp_e.add_text("W-BED3", height=0.6, dxfattribs={"layer": "A_ROOM_LABELS"}).set_placement((76.5, 16.5), align=ezdxf.enums.TextEntityAlignment.MIDDLE_CENTER)

    # Second Floor Sun Terrace & Railing (West side: X in [XB_I, XC_W])
    draw_poly_pts(msp_e, [(XB_I, 22.0), (XC_W, 22.0), (XC_W, 25.5), (XB_I, 25.5)], "A_ELEVATION_GLASS")
    msp_e.add_text("2F SUN TERRACE (OPEN TO SKY)", height=0.6, dxfattribs={"layer": "A_ROOM_LABELS"}).set_placement(((XB_I + XC_W) / 2, 23.75), align=ezdxf.enums.TextEntityAlignment.MIDDLE_CENTER)

    # Second Floor Penthouse Facade (X in [XC_W, XE_O], Z in [22.0, 33.0])
    draw_poly_pts(msp_e, [(XC_W, 22.0), (XE_O, 22.0), (XE_O, 33.0), (XC_W, 33.0)], "A_ELEVATION_OUTLINE")
    draw_poly_pts(msp_e, [(57.5, 25.0), (64.5, 25.0), (64.5, 30.0), (57.5, 30.0)], "A_ELEVATION_GLASS")
    draw_poly_pts(msp_e, [(73.0, 25.0), (80.0, 25.0), (80.0, 30.0), (73.0, 30.0)], "A_ELEVATION_GLASS")

    # Roof Floating Canopy (Z in [33.0, 34.0])
    draw_poly_pts(msp_e, [(50.0, 33.0), (86.0, 33.0), (86.0, 34.0), (50.0, 34.0)], "A_CANOPY")

    # Mumty Stair Tower (Central: X in [57.375, 68.625], Rising to +42'-0")
    draw_poly_pts(msp_e, [(STAIR_X0, 33.0), (STAIR_X1, 33.0), (STAIR_X1, 42.0), (STAIR_X0, 42.0)], "A_ELEVATION_OUTLINE")
    draw_poly_pts(msp_e, [(61.0, 34.5), (65.0, 34.5), (65.0, 40.5), (61.0, 40.5)], "A_ELEVATION_GLASS")
    draw_poly_pts(msp_e, [(STAIR_X0 - 1.0, 42.0), (STAIR_X1 + 1.0, 42.0), (STAIR_X1 + 1.0, 42.75), (STAIR_X0 - 1.0, 42.75)], "A_CANOPY")
    msp_e.add_text("MUMTY TOWER (+42'-0\")", height=0.7, dxfattribs={"layer": "A_ROOM_LABELS"}).set_placement(((STAIR_X0 + STAIR_X1) / 2, 41.0), align=ezdxf.enums.TextEntityAlignment.MIDDLE_CENTER)

    msp_e.add_text("FRONT (SOUTH) ELEVATION - CANOPY ARCHITECTURE", height=1.8,
                  dxfattribs={"layer": "G_TITLEBLOCK"}).set_placement((44.0, -5.0), align=ezdxf.enums.TextEntityAlignment.MIDDLE_CENTER)
    out_elev = OUT_DIR / "06_front_south_elevation.dxf"
    doc_e.saveas(out_elev)
    print(f"[+] Exported DXF: {out_elev}")

    # Master DXF
    doc_m, msp_m = create_dxf_doc()
    for idx, (fl, title, _) in enumerate(plans):
        draw_floor_sheet(msp_m, m, fl, title, idx * 130.0, 0.0)
    out_m = OUT_DIR / "daata_hamlet_master_project.dxf"
    doc_m.saveas(out_m)
    print(f"[+] Exported Master Project DXF: {out_m}")
    print("[+] All DXF files generated successfully!")


if __name__ == "__main__":
    export_all()
