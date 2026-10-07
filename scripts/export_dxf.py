"""
DXF Exporter for STRATAVOX Lamella Cut Sheet
Generates industry-standard AutoCAD DXF (R12/2000 format) vector files
for laser cutting, waterjet, and CNC routing.
"""

from pathlib import Path
import math

def write_dxf(filename="blueprints/stratavox_lamella.dxf"):
    Path(filename).parent.mkdir(parents=True, exist_ok=True)
    
    # 860mm total length, 90mm height (scaled profile), 45mm corner radius
    # 3 pivot holes: (45, 45), (430, 45), (815, 45) with radius 3.0mm (diam 6.0mm)
    
    with open(filename, "w", encoding="ascii") as f:
        # Header
        f.write("0\nSECTION\n2\nHEADER\n0\nENDSEC\n")
        
        # Tables section (Layers)
        f.write("0\nSECTION\n2\nTABLES\n0\nTABLE\n2\nLAYER\n")
        f.write("0\nLAYER\n2\nCUT\n70\n0\n62\n1\n6\nCONTINUOUS\n0\nENDTAB\n0\nENDSEC\n")
        
        # Entities section
        f.write("0\nSECTION\n2\nENTITIES\n")
        
        def write_circle(cx, cy, r, layer="CUT"):
            f.write(f"0\nCIRCLE\n8\n{layer}\n10\n{cx:.3f}\n20\n{cy:.3f}\n30\n0.0\n40\n{r:.3f}\n")
            
        def write_line(x1, y1, x2, y2, layer="CUT"):
            f.write(f"0\nLINE\n8\n{layer}\n10\n{x1:.3f}\n20\n{y1:.3f}\n30\n0.0\n11\n{x2:.3f}\n21\n{y2:.3f}\n31\n0.0\n")
            
        # Top and Bottom straight edges
        write_line(45.0, 90.0, 815.0, 90.0)
        write_line(45.0, 0.0, 815.0, 0.0)
        
        # Left and Right semi-circles (approximated via arc segments)
        for i in range(16):
            a1 = math.pi / 2 + (i / 16.0) * math.pi
            a2 = math.pi / 2 + ((i + 1) / 16.0) * math.pi
            write_line(45.0 + 45.0 * math.cos(a1), 45.0 + 45.0 * math.sin(a1),
                       45.0 + 45.0 * math.cos(a2), 45.0 + 45.0 * math.sin(a2))
            
            a3 = -math.pi / 2 + (i / 16.0) * math.pi
            a4 = -math.pi / 2 + ((i + 1) / 16.0) * math.pi
            write_line(815.0 + 45.0 * math.cos(a3), 45.0 + 45.0 * math.sin(a3),
                       815.0 + 45.0 * math.cos(a4), 45.0 + 45.0 * math.sin(a4))
            
        # Pivot Holes (6.0mm diameter for bronze bushings)
        write_circle(45.0, 45.0, 3.0)
        write_circle(430.0, 45.0, 3.0)
        write_circle(815.0, 45.0, 3.0)
        
        # Wiring Channels (Slots)
        write_line(90.0, 42.0, 375.0, 42.0)
        write_line(90.0, 48.0, 375.0, 48.0)
        write_line(90.0, 42.0, 90.0, 48.0)
        write_line(375.0, 42.0, 375.0, 48.0)
        
        write_line(485.0, 42.0, 770.0, 42.0)
        write_line(485.0, 48.0, 770.0, 48.0)
        write_line(485.0, 42.0, 485.0, 48.0)
        write_line(770.0, 42.0, 770.0, 48.0)
        
        # Kerf Hinge Flexure Slits (Zone 1 and Zone 2)
        for kx in [260, 280, 300, 320, 600, 620, 640, 660]:
            write_line(kx, 6.0, kx, 35.0, layer="KERF")
            write_line(kx, 55.0, kx, 84.0, layer="KERF")
            
        for kx in [270, 290, 310, 610, 630, 650]:
            write_line(kx, 12.0, kx, 78.0, layer="KERF")
            
        f.write("0\nENDSEC\n0\nEOF\n")
        
    print(f"[+] Exported DXF: {Path(filename).resolve()}")

if __name__ == "__main__":
    write_dxf()
