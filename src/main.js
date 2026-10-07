import * as THREE from 'three';
import { OrbitControls } from 'three/examples/jsm/controls/OrbitControls.js';
import { GLTFLoader } from 'three/examples/jsm/loaders/GLTFLoader.js';

// Setup Canvas and Renderer
const canvas = document.getElementById('webgl-canvas');
const renderer = new THREE.WebGLRenderer({
  canvas,
  antialias: true,
  powerPreference: 'high-performance'
});
renderer.setSize(window.innerWidth, window.innerHeight);
renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
renderer.shadowMap.enabled = true;
renderer.shadowMap.type = THREE.PCFSoftShadowMap;
renderer.toneMapping = THREE.ACESFilmicToneMapping;
renderer.toneMappingExposure = 1.15;
renderer.localClippingEnabled = true;

// Scene setup
const scene = new THREE.Scene();
const skyColorDay = new THREE.Color(0xdceaf5);
const skyColorNight = new THREE.Color(0x0c1017);
scene.background = skyColorDay.clone();
scene.fog = new THREE.FogExp2(0xdceaf5, 0.008);

// Camera
const camera = new THREE.PerspectiveCamera(40, window.innerWidth / window.innerHeight, 0.1, 200);
// Center of the residence in meters is around (14, 4.5, -6)
const modelCenter = new THREE.Vector3(14, 4.5, -6);
camera.position.set(7.5, 3.2, 16);

// Orbit Controls
const controls = new OrbitControls(camera, renderer.domElement);
controls.enableDamping = true;
controls.dampingFactor = 0.05;
controls.target.copy(modelCenter);
controls.maxPolarAngle = Math.PI / 2 + 0.02; // prevent going below ground
controls.minDistance = 5;
controls.maxDistance = 90;

// Lighting Setup
const hemiLight = new THREE.HemisphereLight(0xffffff, 0x9fbcd1, 0.65);
scene.add(hemiLight);

const sunLight = new THREE.DirectionalLight(0xfffaed, 2.2);
sunLight.position.set(-18, 28, 22);
sunLight.castShadow = true;
sunLight.shadow.mapSize.width = 2048;
sunLight.shadow.mapSize.height = 2048;
sunLight.shadow.camera.near = 1;
sunLight.shadow.camera.far = 80;
sunLight.shadow.camera.left = -25;
sunLight.shadow.camera.right = 25;
sunLight.shadow.camera.top = 25;
sunLight.shadow.camera.bottom = -25;
sunLight.shadow.bias = -0.0003;
scene.add(sunLight);

// Interior & Exterior Accent Warm Lights (for Night Mode)
const accentLights = [];
const lightDefs = [
  { name: 'PorchLight', pos: [8.5, 3.2, -2.5], color: 0xffb74d, intensity: 25 },
  { name: 'DrawingRoomGlow', pos: [14.0, 2.8, -3.5], color: 0xffca28, intensity: 45 },
  { name: 'LoungeGlow', pos: [18.0, 3.0, -8.0], color: 0xffb74d, intensity: 35 },
  { name: '1FLoungeGlow', pos: [18.0, 6.2, -7.5], color: 0xffca28, intensity: 35 },
  { name: '2FPergolaGlow', pos: [14.0, 9.5, -7.5], color: 0xffb74d, intensity: 30 },
];

lightDefs.forEach(ld => {
  const pl = new THREE.PointLight(ld.color, 0, 14, 1.5);
  pl.position.set(...ld.pos);
  scene.add(pl);
  accentLights.push({ light: pl, targetIntensity: ld.intensity });
});

// Clipping Plane for Floor Cutaways
const cutPlane = new THREE.Plane(new THREE.Vector3(0, -1, 0), 100); // normal points down, cuts above
renderer.clippingPlanes = [cutPlane];

// GLTF Model Loading
let residenceModel = null;
const allMaterials = new Map();
const columnMeshes = [];
let columnsHighlighted = false;
let isNightMode = false;
let isWireframe = false;

const loader = new GLTFLoader();
const modelUrl = './models/daata_hamlet.glb';

loader.load(
  modelUrl,
  (gltf) => {
    residenceModel = gltf.scene;
    // Align model orientation:
    // In our exporter: X=width, Y=depth (North), Z=elevation (Up)
    // Three.js glTF loader converts Z-up to Y-up automatically
    scene.add(residenceModel);

    // Compute bounding box and center
    const bbox = new THREE.Box3().setFromObject(residenceModel);
    const center = new THREE.Vector3();
    bbox.getCenter(center);
    modelCenter.copy(center);
    controls.target.copy(modelCenter);

    // Enhance materials and collect column meshes
    residenceModel.traverse((node) => {
      if (node.isMesh) {
        node.castShadow = true;
        node.receiveShadow = true;

        const matName = node.name || (node.material && node.material.name) || '';

        // Clone material so we can manipulate properties safely
        if (node.material) {
          node.material = node.material.clone();
          allMaterials.set(node, node.material.clone());

          // Architectural Glass
          if (matName.includes('Glass') || node.material.name.includes('Glass')) {
            node.material.transparent = true;
            node.material.opacity = 0.35;
            node.material.roughness = 0.05;
            node.material.metalness = 0.1;
            node.material.color.setHex(0xa8d8ea);
            node.castShadow = false;
          }
          // Canopy Bronze / Charcoal Fascia
          else if (matName.includes('Canopy') || matName.includes('Charcoal')) {
            node.material.roughness = 0.25;
            node.material.metalness = 0.85;
            node.material.color.setHex(0x22242a);
          }
          // Teak Pergola & Louvers
          else if (matName.includes('Teak') || matName.includes('Timber')) {
            node.material.roughness = 0.50;
            node.material.metalness = 0.0;
            node.material.color.setHex(0x9d5e30);
          }
          // White Stucco Plaster
          else if (matName.includes('Plaster')) {
            node.material.roughness = 0.85;
            node.material.metalness = 0.02;
            node.material.color.setHex(0xeeebe5);
          }
          // Columns
          else if (matName.includes('Column')) {
            columnMeshes.push(node);
          }
          // Landscape Grass
          else if (matName.includes('Grass')) {
            node.material.roughness = 0.90;
            node.material.color.setHex(0x42762a);
          }
          // Travertine Stone
          else if (matName.includes('Travertine') || matName.includes('Stone')) {
            node.material.roughness = 0.80;
            node.material.color.setHex(0xc7b9a5);
          }
        }
      }
    });

    console.log('[+] Daata Hamlet Residence 3D model loaded successfully!');
    setCameraPreset('canopy');
  },
  (progress) => {
    const pct = progress.total ? Math.round((progress.loaded / progress.total) * 100) : 100;
    console.log(`[*] Loading 3D model: ${pct}%`);
  },
  (error) => {
    console.error('[!] Error loading 3D model:', error);
  }
);

// Camera Presets
const presets = {
  canopy: {
    pos: new THREE.Vector3(12.5, 3.5, 18.0),
    target: new THREE.Vector3(14.0, 4.0, -3.0),
    title: 'Canopy Elevation (South Facade & Floating Terraces)'
  },
  street: {
    pos: new THREE.Vector3(4.0, 2.5, 16.5),
    target: new THREE.Vector3(14.0, 3.5, -4.5),
    title: 'Street Approach (2-Car Canopy Porch & Wedge Lawn)'
  },
  aerial: {
    pos: new THREE.Vector3(28.0, 24.0, 20.0),
    target: new THREE.Vector3(14.0, 3.0, -8.0),
    title: '3/4 Aerial View (Trapezoid Boundary, Terraces & Mumty)'
  },
  plan: {
    pos: new THREE.Vector3(14.0, 38.0, -8.0),
    target: new THREE.Vector3(14.0, 0.0, -8.0),
    title: 'Top-Down Plan View (Architectural Zoning & Layout)'
  }
};

let currentCamPos = camera.position.clone();
let targetCamPos = camera.position.clone();
let currentLookAt = controls.target.clone();
let targetLookAt = controls.target.clone();
let isLerpingCam = false;

function setCameraPreset(key) {
  const p = presets[key];
  if (!p) return;
  targetCamPos.copy(p.pos);
  targetLookAt.copy(p.target);
  isLerpingCam = true;

  document.querySelectorAll('.camera-presets .btn').forEach(b => b.classList.remove('active'));
  const btn = document.getElementById(`view-${key}`);
  if (btn) btn.classList.add('active');
}

// Floor Cutaways
const floorHeights = {
  all: 100.0,  // no cut
  GF: 3.55,    // cuts above Ground Floor ceiling
  '1F': 6.70,   // cuts above First Floor ceiling
  '2F': 9.85,   // cuts above Second Floor ceiling
  RF: 14.50    // cuts at roof mumty top
};

const floorSummaries = {
  all: 'Full 3-Storey canopy residence with continuous parallel RCC columns, zero loopholes, and custom diagonal dirty kitchen.',
  GF: 'GROUND FLOOR: Drawing Room (18x16), 2 Master Suites (15x16), Lounge & Dining, Wide Kitchen + NE Diagonal Dirty Kitchen (100 sft), 2-Car Porch, Lawns.',
  '1F': 'FIRST FLOOR: 3 Master Suites (all >= 15x16), Family Lounge, Open Kitchen, Open Porch Terrace, Balconies.',
  '2F': 'SECOND FLOOR: 2 Master Suites (all >= 15x16), Servant Room with Bath, Laundry, Store, Timber Pergola Terrace, Front Canopy Terrace.',
  RF: 'ROOF & MUMTY: Continuous Stair Mumty Landing, 800-gal Overhead Water Tank, Expansive Roof Deck with 3-ft Parapets.'
};

function setFloorCutaway(floorKey) {
  const h = floorHeights[floorKey] ?? 100.0;
  cutPlane.constant = h;

  document.querySelectorAll('.preset-modes .mode-btn').forEach(b => b.classList.remove('active'));
  const activeBtn = document.querySelector(`.preset-modes .mode-btn[data-floor="${floorKey}"]`);
  if (activeBtn) activeBtn.classList.add('active');

  const stateHighlight = document.getElementById('state-name');
  if (stateHighlight) {
    stateHighlight.textContent = activeBtn ? activeBtn.textContent : floorKey;
  }

  const summary = document.getElementById('mode-summary');
  if (summary && floorSummaries[floorKey]) {
    summary.textContent = floorSummaries[floorKey];
  }
}

// Toggle Structural Columns (X-Ray Highlight)
function toggleColumnHighlight() {
  columnsHighlighted = !columnsHighlighted;
  const btn = document.getElementById('btn-columns');
  if (btn) {
    btn.classList.toggle('active', columnsHighlighted);
    btn.textContent = columnsHighlighted ? 'Hide Structure' : 'Structural Columns';
  }

  if (!residenceModel) return;

  residenceModel.traverse((node) => {
    if (node.isMesh && node.material) {
      const isCol = node.name.includes('Column') || (node.material.name && node.material.name.includes('Column'));
      if (columnsHighlighted) {
        if (isCol) {
          node.material.color.setHex(0x00f0ff);
          node.material.roughness = 0.2;
          node.material.emissive.setHex(0x004466);
        } else {
          node.material.transparent = true;
          node.material.opacity = 0.25;
        }
      } else {
        // Restore
        const orig = allMaterials.get(node);
        if (orig) {
          node.material.copy(orig);
          if (node.name.includes('Glass')) {
            node.material.transparent = true;
            node.material.opacity = 0.35;
          }
        }
      }
    }
  });
}

// Night Illumination Toggle
function toggleNightMode() {
  isNightMode = !isNightMode;
  const btn = document.getElementById('btn-night');
  if (btn) {
    btn.classList.toggle('active', isNightMode);
    btn.textContent = isNightMode ? '☀️ Day View' : '🌙 Night Illumination';
  }

  // Animate lights and background
  const targetSky = isNightMode ? skyColorNight : skyColorDay;
  scene.background.copy(targetSky);
  scene.fog.color.copy(targetSky);

  sunLight.intensity = isNightMode ? 0.35 : 2.2;
  sunLight.color.setHex(isNightMode ? 0x9fbcd1 : 0xfffaed);
  hemiLight.intensity = isNightMode ? 0.2 : 0.65;

  accentLights.forEach(({ light, targetIntensity }) => {
    light.intensity = isNightMode ? targetIntensity : 0;
  });
}

// Wireframe Toggle
function toggleWireframe() {
  isWireframe = !isWireframe;
  const btn = document.getElementById('btn-wireframe');
  if (btn) {
    btn.classList.toggle('active', isWireframe);
  }
  if (!residenceModel) return;
  residenceModel.traverse((node) => {
    if (node.isMesh && node.material) {
      node.material.wireframe = isWireframe;
    }
  });
}

// Reset View
function resetView() {
  setFloorCutaway('all');
  setCameraPreset('canopy');
  if (columnsHighlighted) toggleColumnHighlight();
  if (isWireframe) toggleWireframe();
}

// Event Listeners
document.getElementById('view-canopy')?.addEventListener('click', () => setCameraPreset('canopy'));
document.getElementById('view-street')?.addEventListener('click', () => setCameraPreset('street'));
document.getElementById('view-aerial')?.addEventListener('click', () => setCameraPreset('aerial'));
document.getElementById('view-plan')?.addEventListener('click', () => setCameraPreset('plan'));

document.getElementById('btn-night')?.addEventListener('click', toggleNightMode);
document.getElementById('btn-wireframe')?.addEventListener('click', toggleWireframe);
document.getElementById('btn-columns')?.addEventListener('click', toggleColumnHighlight);
document.getElementById('btn-reset')?.addEventListener('click', resetView);

document.querySelectorAll('.preset-modes .mode-btn').forEach(btn => {
  btn.addEventListener('click', () => {
    const floor = btn.getAttribute('data-floor');
    if (floor) setFloorCutaway(floor);
  });
});

window.addEventListener('resize', () => {
  camera.aspect = window.innerWidth / window.innerHeight;
  camera.updateProjectionMatrix();
  renderer.setSize(window.innerWidth, window.innerHeight);
  renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
});

// Animation Loop
const clock = new THREE.Clock();

function animate() {
  requestAnimationFrame(animate);

  // Smooth camera lerp
  if (isLerpingCam) {
    camera.position.lerp(targetCamPos, 0.06);
    controls.target.lerp(targetLookAt, 0.06);
    if (camera.position.distanceTo(targetCamPos) < 0.05 && controls.target.distanceTo(targetLookAt) < 0.05) {
      camera.position.copy(targetCamPos);
      controls.target.copy(targetLookAt);
      isLerpingCam = false;
    }
  }

  controls.update();
  renderer.render(scene, camera);
}

animate();
