import base64
import pathlib

WORKSPACE = pathlib.Path(__file__).parent.parent.resolve()
GLB_PATH = WORKSPACE / "models" / "daata_hamlet.glb"
OUT_HTML = WORKSPACE / "standalone_viewer.html"
ARTIFACT_DIR = pathlib.Path(r"C:\Users\adees\.gemini\antigravity\brain\754b2257-dc8d-4e91-8a73-3c0efba21f41")
OUT_ARTIFACT = ARTIFACT_DIR / "standalone_viewer.html"

glb_bytes = GLB_PATH.read_bytes()
b64_glb = base64.b64encode(glb_bytes).decode('ascii')
data_uri = f"data:model/gltf-binary;base64,{b64_glb}"

html = f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>DAATA HAMLET RESIDENCE — 3D Canopy Architecture Explorer</title>
  <style>
    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
      background: #090d16;
      color: #e2e8f0;
      overflow: hidden;
      width: 100vw;
      height: 100vh;
    }}
    #webgl-canvas {{
      position: absolute;
      top: 0;
      left: 0;
      width: 100%;
      height: 100%;
      z-index: 1;
    }}
    .ui-layer {{
      position: absolute;
      top: 0;
      left: 0;
      width: 100%;
      height: 100%;
      z-index: 10;
      pointer-events: none;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      padding: 20px;
    }}
    .top-bar {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      background: rgba(15, 23, 42, 0.85);
      backdrop-filter: blur(12px);
      border: 1px solid rgba(255, 255, 255, 0.1);
      border-radius: 12px;
      padding: 12px 20px;
      pointer-events: auto;
      box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.5);
    }}
    .brand {{
      display: flex;
      align-items: center;
      gap: 12px;
    }}
    .brand-icon {{
      font-size: 24px;
      background: #1e293b;
      padding: 6px 10px;
      border-radius: 8px;
      border: 1px solid #334155;
    }}
    .brand-text h1 {{
      font-size: 16px;
      font-weight: 800;
      letter-spacing: 1px;
      color: #f8fafc;
    }}
    .brand-text p {{
      font-size: 11px;
      color: #f59e0b;
      font-weight: 600;
      letter-spacing: 0.5px;
    }}
    .btn-group {{
      display: flex;
      gap: 8px;
    }}
    button {{
      background: #1e293b;
      color: #cbd5e1;
      border: 1px solid #334155;
      padding: 8px 14px;
      border-radius: 8px;
      font-size: 12px;
      font-weight: 600;
      cursor: pointer;
      transition: all 0.2s ease;
      display: flex;
      align-items: center;
      gap: 6px;
    }}
    button:hover {{
      background: #334155;
      color: #ffffff;
      border-color: #64748b;
    }}
    button.active {{
      background: #2563eb;
      color: #ffffff;
      border-color: #3b82f6;
      box-shadow: 0 0 15px rgba(37, 99, 235, 0.5);
    }}
    .bottom-bar {{
      display: flex;
      justify-content: space-between;
      align-items: flex-end;
      gap: 20px;
      pointer-events: auto;
    }}
    .dock {{
      background: rgba(15, 23, 42, 0.85);
      backdrop-filter: blur(12px);
      border: 1px solid rgba(255, 255, 255, 0.1);
      border-radius: 12px;
      padding: 12px 18px;
      display: flex;
      gap: 8px;
      box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.5);
    }}
    .card {{
      background: rgba(15, 23, 42, 0.90);
      backdrop-filter: blur(14px);
      border: 1px solid rgba(255, 255, 255, 0.12);
      border-radius: 12px;
      padding: 16px 20px;
      width: 380px;
      box-shadow: 0 20px 35px -10px rgba(0, 0, 0, 0.7);
    }}
    .card-title {{
      font-size: 13px;
      font-weight: 800;
      letter-spacing: 1px;
      color: #38bdf8;
      margin-bottom: 10px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      border-bottom: 1px solid #334155;
      padding-bottom: 6px;
    }}
    .stat-row {{
      display: flex;
      justify-content: space-between;
      font-size: 11.5px;
      margin: 6px 0;
    }}
    .stat-label {{ color: #94a3b8; font-weight: 500; }}
    .stat-value {{ color: #f8fafc; font-weight: 700; }}
    .badge-pass {{
      background: rgba(34, 197, 94, 0.2);
      color: #4ade80;
      padding: 2px 6px;
      border-radius: 4px;
      font-size: 10px;
      font-weight: 700;
      border: 1px solid rgba(34, 197, 94, 0.4);
    }}
    #loading {{
      position: absolute;
      top: 50%;
      left: 50%;
      transform: translate(-50%, -50%);
      background: rgba(15, 23, 42, 0.95);
      border: 1px solid #334155;
      padding: 24px 36px;
      border-radius: 12px;
      text-align: center;
      z-index: 100;
      box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.8);
    }}
    .spinner {{
      border: 3px solid rgba(255, 255, 255, 0.1);
      border-top: 3px solid #38bdf8;
      border-radius: 50%;
      width: 32px;
      height: 32px;
      animation: spin 0.8s linear infinite;
      margin: 0 auto 12px auto;
    }}
    @keyframes spin {{ 0% {{ transform: rotate(0deg); }} 100% {{ transform: rotate(360deg); }} }}
  </style>
  <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
  <script src="https://cdn.jsdelivr.net/npm/three@0.128.0/examples/js/controls/OrbitControls.js"></script>
  <script src="https://cdn.jsdelivr.net/npm/three@0.128.0/examples/js/loaders/GLTFLoader.js"></script>
</head>
<body>
  <div id="loading">
    <div class="spinner"></div>
    <div style="font-size: 14px; font-weight: bold; color: #f8fafc;">INITIALIZING CANOPY ARCHITECTURE 3D SCENE</div>
    <div style="font-size: 11px; color: #94a3b8; margin-top: 4px;">Unpacking Base64 GLTF Model (225 KB)...</div>
  </div>

  <canvas id="webgl-canvas"></canvas>

  <div class="ui-layer">
    <div class="top-bar">
      <div class="brand">
        <div class="brand-icon">🏛️</div>
        <div class="brand-text">
          <h1>DAATA HAMLET RESIDENCE</h1>
          <p>CONTEMPORARY CANOPY RESIDENCE &bull; ARCHITECTURAL 3D STUDY</p>
        </div>
      </div>
      
      <div class="btn-group">
        <button id="cam-elevation" class="active">📐 Front Elevation</button>
        <button id="cam-street">🚗 Street View</button>
        <button id="cam-aerial">🚁 Aerial Perspective</button>
        <button id="cam-plan">📋 Floor Plan</button>
        <button id="btn-night">🌙 Evening Lighting</button>
        <button id="btn-wireframe">🕸️ Wireframe</button>
      </div>
    </div>

    <div class="bottom-bar">
      <div class="dock">
        <button class="floor-btn active" data-floor="all">🏢 Complete Residence</button>
        <button class="floor-btn" data-floor="gf">Ground Floor (Drawing, 2 Beds, Lounge, Kitchen)</button>
        <button class="floor-btn" data-floor="f1">First Floor (3 Beds, Lounge, Terrace)</button>
        <button class="floor-btn" data-floor="f2">Second Floor (2 Beds, Servant, Sun Terrace)</button>
        <button class="floor-btn" data-floor="rf">Roof & Mumty (Water Tank)</button>
      </div>

      <div class="card">
        <div class="card-title">
          <span>PROJECT SCHEDULE</span>
          <span class="badge-pass">BYLAW COMPLIANT</span>
        </div>
        <div class="stat-row">
          <span class="stat-label">Plot Frontage / Area</span>
          <span class="stat-value">87'-11" | 3,129.1 sq.ft (12.8 Marla)</span>
        </div>
        <div class="stat-row">
          <span class="stat-label">Total Covered Area</span>
          <span class="stat-value">5,586 sq.ft (GF: 2,125 | 1F: 2,033 | 2F: 1,282)</span>
        </div>
        <div class="stat-row">
          <span class="stat-label">Drawing Room (GF)</span>
          <span class="stat-value">18'-0" &times; 16'-0" (288 sq.ft &gt; 15'x16')</span>
        </div>
        <div class="stat-row">
          <span class="stat-label">Bedrooms</span>
          <span class="stat-value">7 Master Suites (All &ge; 15'-0" &times; 16'-0")</span>
        </div>
        <div class="stat-row">
          <span class="stat-label">Dirty Kitchen</span>
          <span class="stat-value">100 sq.ft in NE Diagonal Apex (P5-P6-P7)</span>
        </div>
        <div class="stat-row">
          <span class="stat-label">Structural Grid</span>
          <span class="stat-value">22 Continuous Parallel Flush Columns</span>
        </div>
      </div>
    </div>
  </div>

  <script>
    const EMBEDDED_GLB_DATA = "{data_uri}";

    // Renderer
    const canvas = document.getElementById('webgl-canvas');
    const renderer = new THREE.WebGLRenderer({{ canvas, antialias: true, powerPreference: 'high-performance' }});
    renderer.setSize(window.innerWidth, window.innerHeight);
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
    renderer.shadowMap.enabled = true;
    renderer.shadowMap.type = THREE.PCFSoftShadowMap;
    renderer.toneMapping = THREE.ACESFilmicToneMapping;
    renderer.toneMappingExposure = 1.1;

    // Scene
    const scene = new THREE.Scene();
    const skyDay = new THREE.Color(0xdde9f5);
    const skyNight = new THREE.Color(0x0a0f1d);
    scene.background = skyDay.clone();
    scene.fog = new THREE.FogExp2(0xdde9f5, 0.007);

    // Camera (Target centered on residence)
    const camera = new THREE.PerspectiveCamera(38, window.innerWidth / window.innerHeight, 0.2, 300);
    const target = new THREE.Vector3(13.5, 4.5, -6.5);

    // Controls
    const controls = new THREE.OrbitControls(camera, renderer.domElement);
    controls.enableDamping = true;
    controls.dampingFactor = 0.06;
    controls.target.copy(target);
    controls.maxPolarAngle = Math.PI / 2 + 0.01;

    // Lights
    const hemiLight = new THREE.HemisphereLight(0xffffff, 0xa0b8cf, 0.7);
    scene.add(hemiLight);

    const dirLight = new THREE.DirectionalLight(0xfff7e6, 2.4);
    dirLight.position.set(-20, 32, 24);
    dirLight.castShadow = true;
    dirLight.shadow.mapSize.width = 2048;
    dirLight.shadow.mapSize.height = 2048;
    dirLight.shadow.bias = -0.0004;
    scene.add(dirLight);

    // Ground Plane with Grid
    const groundGeo = new THREE.PlaneGeometry(120, 120);
    const groundMat = new THREE.MeshStandardMaterial({{ color: 0x1f2937, roughness: 0.9, metalness: 0.05 }});
    const ground = new THREE.Mesh(groundGeo, groundMat);
    ground.rotation.x = -Math.PI / 2;
    ground.position.set(13.5, -0.02, -6.5);
    ground.receiveShadow = true;
    scene.add(ground);

    const grid = new THREE.GridHelper(90, 45, 0x38bdf8, 0x334155);
    grid.position.set(13.5, 0.0, -6.5);
    scene.add(grid);

    // Night Accent Lights
    const accentLights = [];
    const lightLocs = [
      {{ pos: [8.5, 3.2, -2.5], color: 0xffb74d, power: 25 }},
      {{ pos: [14.0, 2.8, -3.5], color: 0xffca28, power: 45 }},
      {{ pos: [18.0, 3.0, -8.0], color: 0xffb74d, power: 35 }},
      {{ pos: [18.0, 6.2, -7.5], color: 0xffca28, power: 35 }},
      {{ pos: [14.0, 9.5, -7.5], color: 0xffb74d, power: 30 }}
    ];
    lightLocs.forEach(l => {{
      const p = new THREE.PointLight(l.color, 0, 15, 1.5);
      p.position.set(...l.pos);
      scene.add(p);
      accentLights.push({{ light: p, target: l.power }});
    }});

    // Clipping plane for floor cutaways
    const clipPlane = new THREE.Plane(new THREE.Vector3(0, -1, 0), 100);
    renderer.clippingPlanes = [clipPlane];

    // Camera Presets
    const presets = {{
      elevation: {{ pos: [13.5, 5.0, 34.0], target: [13.5, 5.0, -6.5] }},
      street:    {{ pos: [-2.0, 2.5, 18.0], target: [13.5, 4.0, -6.5] }},
      aerial:    {{ pos: [28.0, 22.0, 24.0], target: [13.5, 4.0, -6.5] }},
      plan:      {{ pos: [13.5, 38.0, -6.5], target: [13.5, 0.0, -6.5] }}
    }};

    function setCameraPreset(key) {{
      const p = presets[key];
      if (!p) return;
      camera.position.set(...p.pos);
      controls.target.set(...p.target);
      controls.update();
    }}

    setCameraPreset('elevation');

    // Model Loading from Base64 Data URI
    let residence = null;
    const allMaterials = [];
    const loader = new THREE.GLTFLoader();

    loader.load(
      EMBEDDED_GLB_DATA,
      (gltf) => {{
        residence = gltf.scene;
        residence.traverse((node) => {{
          if (node.isMesh) {{
            node.castShadow = true;
            node.receiveShadow = true;
            if (node.material) {{
              allMaterials.push(node.material);
              node.material.clippingPlanes = [clipPlane];
              node.material.clipShadows = true;
            }}
          }}
        }});
        scene.add(residence);
        document.getElementById('loading').style.display = 'none';
      }},
      undefined,
      (err) => {{
        console.error('Model load error:', err);
        document.getElementById('loading').innerHTML = '<div style="color:#ef4444;font-weight:bold;">Error loading embedded 3D model</div>';
      }}
    );

    // UI Buttons
    const camBtns = ['elevation', 'street', 'aerial', 'plan'];
    camBtns.forEach(key => {{
      const el = document.getElementById('cam-' + key);
      if (el) {{
        el.onclick = () => {{
          camBtns.forEach(k => {{
            const b = document.getElementById('cam-' + k);
            if (b) b.classList.remove('active');
          }});
          el.classList.add('active');
          setCameraPreset(key);
        }};
      }}
    }});

    let isNight = false;
    document.getElementById('btn-night').onclick = function() {{
      isNight = !isNight;
      this.classList.toggle('active', isNight);
      if (isNight) {{
        scene.background = skyNight;
        scene.fog.color = skyNight;
        hemiLight.intensity = 0.15;
        dirLight.intensity = 0.35;
        accentLights.forEach(a => a.light.intensity = a.target);
      }} else {{
        scene.background = skyDay;
        scene.fog.color = skyDay;
        hemiLight.intensity = 0.7;
        dirLight.intensity = 2.4;
        accentLights.forEach(a => a.light.intensity = 0);
      }}
    }};

    let isWire = false;
    document.getElementById('btn-wireframe').onclick = function() {{
      isWire = !isWire;
      this.classList.toggle('active', isWire);
      allMaterials.forEach(m => m.wireframe = isWire);
    }};

    // Floor Cutaways
    const floorHeights = {{
      all: 100,
      gf: 3.8,
      f1: 7.2,
      f2: 10.4,
      rf: 100
    }};

    document.querySelectorAll('.floor-btn').forEach(btn => {{
      btn.onclick = () => {{
        document.querySelectorAll('.floor-btn').forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        const f = btn.dataset.floor;
        clipPlane.constant = floorHeights[f] || 100;
      }};
    }});

    // Resize
    window.addEventListener('resize', () => {{
      camera.aspect = window.innerWidth / window.innerHeight;
      camera.updateProjectionMatrix();
      renderer.setSize(window.innerWidth, window.innerHeight);
    }});

    // Render Loop
    function animate() {{
      requestAnimationFrame(animate);
      controls.update();
      renderer.render(scene, camera);
    }}
    animate();
  </script>
</body>
</html>
'''

OUT_HTML.write_text(html, encoding="utf-8")
OUT_ARTIFACT.write_text(html, encoding="utf-8")
print(f"[+] Successfully generated 100% self-contained standalone viewer: {OUT_HTML}")
print(f"[+] Output artifact: {OUT_ARTIFACT}")
