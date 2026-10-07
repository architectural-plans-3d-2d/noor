"""
Generates the architectural presentation blueprint SVG for the Transformable Box Stool.
Includes all 5 sections:
  01 Basic Idea
  02 Configurations (Stool, Storage, Desk)
  03 Fabrication Steps (1 to 4)
  04 Mechanism & Joinery (Detail A, Detail B, Detail C)
  05 Key Dimensions (Stool, Storage, Desk orthographic views)
"""

import os

def generate_svg():
    os.makedirs("blueprints", exist_ok=True)
    svg_path = "blueprints/transformable_box_presentation_sheet.svg"

    svg_content = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1920 1080" width="1920" height="1080" style="background:#F9F8F6; font-family:'Segoe UI', -apple-system, sans-serif;">
  <defs>
    <style>
      .title {{ font-size: 42px; font-weight: 300; letter-spacing: 6px; fill: #2C2A29; }}
      .subtitle {{ font-size: 16px; font-weight: 400; letter-spacing: 4px; fill: #8C827A; }}
      .sec-tag {{ font-size: 13px; font-weight: 700; fill: #FFFFFF; }}
      .sec-title {{ font-size: 16px; font-weight: 700; letter-spacing: 2px; fill: #2C2A29; }}
      .body-txt {{ font-size: 12px; font-weight: 400; fill: #5A544F; line-height: 1.5; }}
      .dim-txt {{ font-size: 12px; font-weight: 600; fill: #333333; }}
      .plywood {{ fill: #E8D7C1; stroke: #8F765A; stroke-width: 1.5; }}
      .plywood-dark {{ fill: #D9C3A7; stroke: #7B6349; stroke-width: 1.5; }}
      .plywood-light {{ fill: #F3E7D7; stroke: #A89074; stroke-width: 1.5; }}
      .hardware {{ fill: #C8D1D9; stroke: #4A5568; stroke-width: 1.2; }}
      .dim-line {{ stroke: #666666; stroke-width: 1.0; stroke-dasharray: none; }}
      .dim-tick {{ stroke: #333333; stroke-width: 1.5; }}
      .circ-num {{ fill: #8F765A; }}
      .grid-line {{ stroke: #E2DDD5; stroke-width: 0.8; stroke-dasharray: 4,4; }}
    </style>
    <marker id="arrow" viewBox="0 0 10 10" refX="5" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 1.5 L 10 5 L 0 8.5 z" fill="#8F765A"/>
    </marker>
  </defs>

  <!-- BACKGROUND CARD -->
  <rect x="30" y="30" width="1860" height="1020" rx="16" fill="#FFFFFF" stroke="#E2DDD5" stroke-width="1.5"/>

  <!-- HEADER -->
  <g transform="translate(60, 80)">
    <text x="0" y="0" class="title">TRANSFORMABLE BOX</text>
    <text x="0" y="28" class="subtitle">STOOL &nbsp;|&nbsp; STORAGE &nbsp;|&nbsp; STUDY DESK</text>
  </g>

  <!-- 01 BASIC IDEA -->
  <g transform="translate(60, 150)">
    <rect x="0" y="0" width="28" height="24" rx="4" fill="#8F765A"/>
    <text x="6" y="17" class="sec-tag">01</text>
    <text x="38" y="17" class="sec-title">BASIC IDEA</text>
    
    <foreignObject x="0" y="32" width="380" height="70">
      <p xmlns="http://www.w3.org/1999/xhtml" class="body-txt" style="margin:0;">
        Two identical box stools are connected with a continuous piano hinge on the top surface. The stools fold and stack 180° into a vertical storage cabinet. A fold-down panel transforms the upper cabinet into a rigid study desk.
      </p>
    </foreignObject>

    <!-- Basic Idea Diagrams: Stool -> Storage -> Desk -->
    <g transform="translate(0, 110)">
      <!-- Box 1 & 2 side by side -->
      <polygon points="10,40 50,20 130,20 90,40" class="plywood-light"/>
      <polygon points="10,40 90,40 90,90 10,90" class="plywood"/>
      <polygon points="90,40 130,20 130,70 90,90" class="plywood-dark"/>

      <polygon points="90,40 130,20 210,20 170,40" class="plywood-light"/>
      <polygon points="90,40 170,40 170,90 90,90" class="plywood"/>
      <polygon points="170,40 210,20 210,70 170,90" class="plywood-dark"/>
      <!-- Top hinge -->
      <line x1="88" y1="40" x2="128" y2="20" stroke="#4A5568" stroke-width="3"/>
      <text x="18" y="112" class="body-txt" style="font-weight:600;">TWO IDENTICAL STOOLS</text>

      <!-- Arrow -->
      <line x1="225" y1="55" x2="255" y2="55" stroke="#8F765A" stroke-width="2" marker-end="url(#arrow)"/>

      <!-- Stacked Storage -->
      <g transform="translate(270, -20)">
        <polygon points="10,30 45,15 105,15 70,30" class="plywood-light"/>
        <polygon points="10,30 70,30 70,120 10,120" class="plywood"/>
        <polygon points="70,30 105,15 105,105 70,120" class="plywood-dark"/>
        <!-- Seam line -->
        <line x1="10" y1="75" x2="70" y2="75" stroke="#7B6349" stroke-width="1.5"/>
        <line x1="70" y1="75" x2="105" y2="60" stroke="#7B6349" stroke-width="1.5"/>
        <!-- Cutout Handle -->
        <rect x="78" y="42" width="16" height="5" rx="2.5" fill="#FFFFFF" stroke="#7B6349" stroke-width="1" transform="rotate(-20 78 42)"/>
        <text x="0" y="142" class="body-txt" style="font-weight:600;">FOLD &amp; STACK INTO STORAGE</text>
      </g>
    </g>
  </g>

  <!-- 02 CONFIGURATIONS -->
  <g transform="translate(560, 150)">
    <rect x="0" y="0" width="28" height="24" rx="4" fill="#8F765A"/>
    <text x="6" y="17" class="sec-tag">02</text>
    <text x="38" y="17" class="sec-title">CONFIGURATIONS</text>

    <!-- Config 1: Stool with human silhouette -->
    <g transform="translate(20, 40)">
      <circle cx="10" cy="10" r="10" class="circ-num"/>
      <text x="6" y="14" fill="#FFF" font-size="11" font-weight="700">1</text>
      <text x="28" y="12" class="sec-title" style="font-size:13px;">STOOL</text>
      <text x="28" y="27" class="body-txt">Two box stools placed side by side.</text>

      <!-- Isometric Bench with Silhouette -->
      <g transform="translate(0, 50)">
        <polygon points="10,40 50,20 180,20 140,40" class="plywood-light"/>
        <polygon points="10,40 140,40 140,85 10,85" class="plywood"/>
        <polygon points="140,40 180,20 180,65 140,85" class="plywood-dark"/>
        <line x1="75" y1="40" x2="115" y2="20" stroke="#7B6349" stroke-width="1.5"/>
        <!-- Human sitting outline silhouette -->
        <path d="M 120 -15 C 120 -25 130 -30 135 -30 C 140 -30 150 -25 150 -15 C 150 -5 140 0 135 0 C 130 0 120 -5 120 -15 Z M 130 0 L 140 35 L 115 35 L 110 70 L 100 70 L 105 35 L 125 0 Z" fill="#D2C8BF" opacity="0.6"/>
      </g>
    </g>

    <!-- Config 2: Storage Cabinet -->
    <g transform="translate(280, 40)">
      <circle cx="10" cy="10" r="10" class="circ-num"/>
      <text x="6" y="14" fill="#FFF" font-size="11" font-weight="700">2</text>
      <text x="28" y="12" class="sec-title" style="font-size:13px;">STORAGE</text>
      <text x="28" y="27" class="body-txt">Boxes folded and stacked to form a vertical cabinet.</text>

      <g transform="translate(30, 40)">
        <polygon points="10,25 45,10 100,10 65,25" class="plywood-light"/>
        <polygon points="10,25 65,25 65,135 10,135" class="plywood"/>
        <polygon points="65,25 100,10 100,120 65,135" class="plywood-dark"/>
        <line x1="10" y1="80" x2="65" y2="80" stroke="#7B6349" stroke-width="1.5"/>
        <line x1="65" y1="80" x2="100" y2="65" stroke="#7B6349" stroke-width="1.5"/>
        <!-- Handle on side -->
        <rect x="76" y="38" width="16" height="5" rx="2.5" fill="#FFFFFF" stroke="#7B6349" stroke-width="1" transform="rotate(-20 76 38)"/>
      </g>
    </g>

    <!-- Config 3: Study Desk -->
    <g transform="translate(520, 40)">
      <circle cx="10" cy="10" r="10" class="circ-num"/>
      <text x="6" y="14" fill="#FFF" font-size="11" font-weight="700">3</text>
      <text x="28" y="12" class="sec-title" style="font-size:13px;">STUDY DESK</text>
      <text x="28" y="27" class="body-txt">Fold down the panel to create a compact desk.</text>

      <g transform="translate(30, 40)">
        <!-- Vertical back frame -->
        <polygon points="20,25 50,10 95,10 65,25" class="plywood-light"/>
        <polygon points="20,25 65,25 65,135 20,135" class="plywood"/>
        <polygon points="65,25 95,10 95,120 65,135" class="plywood-dark"/>
        <!-- Shelves inside -->
        <line x1="25" y1="50" x2="60" y2="50" stroke="#7B6349" stroke-width="2"/>
        <line x1="25" y1="105" x2="60" y2="105" stroke="#7B6349" stroke-width="2"/>
        <!-- Cantilevered fold-down desk leaf -->
        <polygon points="-25,75 25,60 65,60 15,75" class="plywood-light"/>
        <polygon points="-25,75 15,75 15,80 -25,80" class="plywood"/>
        <!-- Folding stay bracket -->
        <line x1="-5" y1="78" x2="25" y2="95" stroke="#4A5568" stroke-width="2"/>
        <circle cx="10" cy="86" r="2" fill="#4A5568"/>
      </g>
    </g>
  </g>

  <!-- DIVIDER LINE -->
  <line x1="60" y1="410" x2="1860" y2="410" stroke="#E2DDD5" stroke-width="1.2"/>

  <!-- 03 FABRICATION STEPS -->
  <g transform="translate(60, 440)">
    <rect x="0" y="0" width="28" height="24" rx="4" fill="#8F765A"/>
    <text x="6" y="17" class="sec-tag">03</text>
    <text x="38" y="17" class="sec-title">FABRICATION STEPS</text>

    <!-- Step 1 -->
    <g transform="translate(10, 40)">
      <polygon points="10,25 35,10 75,10 50,25" class="plywood-light"/>
      <polygon points="10,25 50,25 50,65 10,65" class="plywood"/>
      <polygon points="50,25 75,10 75,50 50,65" class="plywood-dark"/>
      <circle cx="15" cy="85" r="9" class="circ-num"/>
      <text x="12" y="89" fill="#FFF" font-size="10" font-weight="700">1</text>
      <text x="30" y="86" class="body-txt" style="font-weight:600;">FABRICATE TWO</text>
      <text x="30" y="98" class="body-txt" style="font-weight:600;">IDENTICAL BOXES</text>
    </g>
    <line x1="150" y1="70" x2="175" y2="70" stroke="#8F765A" stroke-width="1.5" marker-end="url(#arrow)"/>

    <!-- Step 2 -->
    <g transform="translate(190, 40)">
      <polygon points="10,25 35,10 115,10 90,25" class="plywood-light"/>
      <polygon points="10,25 90,25 90,65 10,65" class="plywood"/>
      <polygon points="90,25 115,10 115,50 90,65" class="plywood-dark"/>
      <!-- Hinge -->
      <line x1="50" y1="25" x2="75" y2="10" stroke="#4A5568" stroke-width="3"/>
      <circle cx="15" cy="85" r="9" class="circ-num"/>
      <text x="12" y="89" fill="#FFF" font-size="10" font-weight="700">2</text>
      <text x="30" y="86" class="body-txt" style="font-weight:600;">CONNECT WITH HINGE</text>
      <text x="30" y="98" class="body-txt" style="font-weight:600;">ON TOP SURFACE</text>
    </g>
    <line x1="340" y1="70" x2="365" y2="70" stroke="#8F765A" stroke-width="1.5" marker-end="url(#arrow)"/>

    <!-- Step 3 -->
    <g transform="translate(380, 20)">
      <polygon points="10,25 35,10 75,10 50,25" class="plywood-light"/>
      <polygon points="10,25 50,25 50,105 10,105" class="plywood"/>
      <polygon points="50,25 75,10 75,90 50,105" class="plywood-dark"/>
      <line x1="10" y1="65" x2="50" y2="65" stroke="#7B6349" stroke-width="1.5"/>
      <circle cx="15" cy="125" r="9" class="circ-num"/>
      <text x="12" y="129" fill="#FFF" font-size="10" font-weight="700">3</text>
      <text x="30" y="126" class="body-txt" style="font-weight:600;">FOLD AND LOCK IN</text>
      <text x="30" y="138" class="body-txt" style="font-weight:600;">VERTICAL POSITION</text>
    </g>
    <line x1="520" y1="70" x2="545" y2="70" stroke="#8F765A" stroke-width="1.5" marker-end="url(#arrow)"/>

    <!-- Step 4 -->
    <g transform="translate(560, 20)">
      <polygon points="10,25 35,10 75,10 50,25" class="plywood-light"/>
      <polygon points="10,25 50,25 50,105 10,105" class="plywood"/>
      <polygon points="50,25 75,10 75,90 50,105" class="plywood-dark"/>
      <!-- Fold down flap -->
      <polygon points="-25,65 15,52 50,52 10,65" class="plywood-light"/>
      <polygon points="-25,65 10,65 10,69 -25,69" class="plywood"/>
      <line x1="-5" y1="68" x2="15" y2="82" stroke="#4A5568" stroke-width="1.5"/>
      <circle cx="15" cy="125" r="9" class="circ-num"/>
      <text x="12" y="129" fill="#FFF" font-size="10" font-weight="700">4</text>
      <text x="30" y="126" class="body-txt" style="font-weight:600;">INSTALL FOLD DOWN</text>
      <text x="30" y="138" class="body-txt" style="font-weight:600;">DESK PANEL &amp; SUPPORT</text>
    </g>
  </g>

  <!-- 04 MECHANISM & JOINERY DETAILS -->
  <g transform="translate(1300, 440)">
    <rect x="0" y="0" width="28" height="24" rx="4" fill="#8F765A"/>
    <text x="6" y="17" class="sec-tag">04</text>
    <text x="38" y="17" class="sec-title">MECHANISM &amp; JOINERY</text>

    <!-- Detail A: Top Hinge -->
    <g transform="translate(20, 40)">
      <circle cx="60" cy="60" r="55" fill="#F4EFEA" stroke="#8F765A" stroke-width="1.5"/>
      <!-- Piano Hinge Zoom -->
      <polygon points="30,70 60,45 100,45 70,70" class="plywood-light"/>
      <polygon points="30,70 70,70 70,85 30,85" class="plywood"/>
      <line x1="50" y1="58" x2="90" y2="33" stroke="#2B6CB0" stroke-width="5" stroke-linecap="round"/>
      <circle cx="65" cy="46" r="3" fill="#FFFFFF"/>
      <circle cx="75" cy="38" r="3" fill="#FFFFFF"/>
      
      <circle cx="0" cy="130" r="9" class="circ-num"/>
      <text x="-4" y="134" fill="#FFF" font-size="10" font-weight="700">A</text>
      <text x="15" y="131" class="sec-title" style="font-size:12px;">TOP HINGE</text>
      <text x="15" y="145" class="body-txt" style="font-size:11px;">Continuous stainless piano</text>
      <text x="15" y="157" class="body-txt" style="font-size:11px;">hinge spans 450mm seam.</text>
    </g>

    <!-- Detail B: Fold Down Desk Panel -->
    <g transform="translate(200, 40)">
      <circle cx="60" cy="60" r="55" fill="#F4EFEA" stroke="#8F765A" stroke-width="1.5"/>
      <!-- Desk flap & stay bracket Zoom -->
      <polygon points="15,65 65,50 105,50 55,65" class="plywood-light"/>
      <line x1="45" y1="62" x2="75" y2="85" stroke="#4A5568" stroke-width="3"/>
      <line x1="75" y1="85" x2="90" y2="92" stroke="#4A5568" stroke-width="3"/>
      <circle cx="75" cy="85" r="3" fill="#D69E2E"/>
      
      <circle cx="0" cy="130" r="9" class="circ-num"/>
      <text x="-4" y="134" fill="#FFF" font-size="10" font-weight="700">B</text>
      <text x="15" y="131" class="sec-title" style="font-size:12px;">FOLD DOWN PANEL</text>
      <text x="15" y="145" class="body-txt" style="font-size:11px;">Heavy-duty triangulated</text>
      <text x="15" y="157" class="body-txt" style="font-size:11px;">locking folding stay bracket.</text>
    </g>

    <!-- Detail C: Vertical Lock -->
    <g transform="translate(380, 40)">
      <circle cx="60" cy="60" r="55" fill="#F4EFEA" stroke="#8F765A" stroke-width="1.5"/>
      <!-- Latch & Stop Zoom -->
      <rect x="35" y="35" width="20" height="30" class="plywood-dark"/>
      <rect x="55" y="42" width="25" height="15" rx="3" class="hardware"/>
      <circle cx="68" cy="49" r="2.5" fill="#2D3748"/>
      
      <circle cx="0" cy="130" r="9" class="circ-num"/>
      <text x="-4" y="134" fill="#FFF" font-size="10" font-weight="700">C</text>
      <text x="15" y="131" class="sec-title" style="font-size:12px;">VERTICAL LOCK</text>
      <text x="15" y="145" class="body-txt" style="font-size:11px;">Solid wood stop &amp; metal</text>
      <text x="15" y="157" class="body-txt" style="font-size:11px;">draw-latch secure stacked units.</text>
    </g>
  </g>

  <!-- DIVIDER LINE -->
  <line x1="60" y1="670" x2="1860" y2="670" stroke="#E2DDD5" stroke-width="1.2"/>

  <!-- 05 KEY DIMENSIONS & ARCHITECTURAL ORTHOGRAPHICS -->
  <g transform="translate(60, 700)">
    <rect x="0" y="0" width="28" height="24" rx="4" fill="#8F765A"/>
    <text x="6" y="17" class="sec-tag">05</text>
    <text x="38" y="17" class="sec-title">KEY DIMENSIONS &amp; ORTHOGRAPHIC PLANS</text>

    <!-- 1. Stool Orthographic -->
    <g transform="translate(60, 40)">
      <text x="0" y="0" class="sec-title" style="font-size:13px;">STOOL CONFIGURATION (TOP &amp; FRONT)</text>
      
      <!-- Stool Front Elevation -->
      <g transform="translate(0, 30)">
        <rect x="0" y="0" width="160" height="80" class="plywood"/>
        <rect x="160" y="0" width="160" height="80" class="plywood"/>
        <line x1="160" y1="0" x2="160" y2="80" stroke="#7B6349" stroke-width="2"/>
        <!-- Top Hinge line -->
        <rect x="154" y="-3" width="12" height="6" rx="2" class="hardware"/>
        
        <!-- Dimensions -->
        <line x1="0" y1="95" x2="320" y2="95" class="dim-line"/>
        <line x1="0" y1="90" x2="0" y2="100" class="dim-tick"/>
        <line x1="320" y1="90" x2="320" y2="100" class="dim-tick"/>
        <text x="125" y="112" class="dim-txt">900 mm</text>

        <line x1="-15" y1="0" x2="-15" y2="80" class="dim-line"/>
        <line x1="-20" y1="0" x2="-10" y2="0" class="dim-tick"/>
        <line x1="-20" y1="80" x2="-10" y2="80" class="dim-tick"/>
        <text x="-65" y="44" class="dim-txt">450 mm</text>
      </g>

      <!-- Stool Side View -->
      <g transform="translate(360, 30)">
        <rect x="0" y="0" width="80" height="80" class="plywood"/>
        <line x1="0" y1="95" x2="80" y2="95" class="dim-line"/>
        <line x1="0" y1="90" x2="0" y2="100" class="dim-tick"/>
        <line x1="80" y1="90" x2="80" y2="100" class="dim-tick"/>
        <text x="18" y="112" class="dim-txt">450 mm</text>
      </g>
    </g>

    <!-- 2. Storage Orthographic -->
    <g transform="translate(680, 40)">
      <text x="0" y="0" class="sec-title" style="font-size:13px;">STORAGE CONFIGURATION (FRONT &amp; SIDE)</text>
      
      <!-- Front View -->
      <g transform="translate(30, 30)">
        <rect x="0" y="0" width="80" height="80" class="plywood"/>
        <rect x="0" y="80" width="80" height="80" class="plywood"/>
        <line x1="0" y1="80" x2="80" y2="80" stroke="#7B6349" stroke-width="2"/>
        <!-- Side Latch -->
        <rect x="76" y="72" width="8" height="16" class="hardware"/>
        
        <!-- Dimensions -->
        <line x1="-15" y1="0" x2="-15" y2="160" class="dim-line"/>
        <line x1="-20" y1="0" x2="-10" y2="0" class="dim-tick"/>
        <line x1="-20" y1="160" x2="-10" y2="160" class="dim-tick"/>
        <text x="-65" y="85" class="dim-txt">900 mm</text>

        <line x1="0" y1="175" x2="80" y2="175" class="dim-line"/>
        <line x1="0" y1="170" x2="0" y2="180" class="dim-tick"/>
        <line x1="80" y1="170" x2="80" y2="180" class="dim-tick"/>
        <text x="18" y="192" class="dim-txt">450 mm</text>
      </g>

      <!-- Side View -->
      <g transform="translate(160, 30)">
        <rect x="0" y="0" width="80" height="160" class="plywood"/>
        <line x1="0" y1="80" x2="80" y2="80" stroke="#7B6349" stroke-width="1.5"/>
        <!-- Cutout Handle -->
        <rect x="28" y="45" width="24" height="7" rx="3.5" fill="#FFFFFF" stroke="#7B6349" stroke-width="1"/>
        <line x1="0" y1="175" x2="80" y2="175" class="dim-line"/>
        <text x="18" y="192" class="dim-txt">450 mm</text>
      </g>
    </g>

    <!-- 3. Desk Orthographic -->
    <g transform="translate(1180, 40)">
      <text x="0" y="0" class="sec-title" style="font-size:13px;">DESK CONFIGURATION (SIDE ELEVATION)</text>
      
      <g transform="translate(40, 30)">
        <!-- Stacked Cabinet carcass -->
        <rect x="0" y="0" width="80" height="160" class="plywood"/>
        <line x1="0" y1="80" x2="80" y2="80" stroke="#7B6349" stroke-width="1.5"/>
        <!-- Folded Desk Leaf -->
        <rect x="80" y="80" width="80" height="6" class="plywood-light"/>
        <!-- Folding Bracket stay -->
        <line x1="80" y1="120" x2="140" y2="86" stroke="#4A5568" stroke-width="2.5"/>
        
        <!-- Cantilever Dimension -->
        <line x1="80" y1="65" x2="160" y2="65" class="dim-line"/>
        <line x1="80" y1="60" x2="80" y2="70" class="dim-tick"/>
        <line x1="160" y1="60" x2="160" y2="70" class="dim-tick"/>
        <text x="98" y="55" class="dim-txt">450 mm</text>

        <!-- Height Dimension -->
        <line x1="-15" y1="0" x2="-15" y2="160" class="dim-line"/>
        <line x1="-20" y1="0" x2="-10" y2="0" class="dim-tick"/>
        <line x1="-20" y1="160" x2="-10" y2="160" class="dim-tick"/>
        <text x="-65" y="85" class="dim-txt">900 mm</text>
      </g>
    </g>
  </g>

  <!-- FOOTER -->
  <g transform="translate(60, 1030)">
    <text x="0" y="0" class="body-txt" style="font-size:11px; fill:#9E9790;">
      ENGINEERED SPECIFICATIONS: 18mm Baltic Birch Plywood (13-ply void-free) • 304 Stainless Steel Continuous Piano Hinge • Heavy-Duty Triangulated Locking Desk Stays • 2mm Swing Clearance
    </text>
  </g>
</svg>
"""

    with open(svg_path, "w", encoding="utf-8") as f:
        f.write(svg_content)
    print(f"[+] Successfully generated vector blueprint presentation sheet at {svg_path}")

if __name__ == "__main__":
    generate_svg()
