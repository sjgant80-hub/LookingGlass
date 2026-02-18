// LookingGlass 3D Cube - Three.js visualization
// Requires: three.js r160+ and OrbitControls via importmap
import * as THREE from 'three';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';

const ACCENT = 0x00cccc;
const ACCENT_HI = 0x00ffff;
const GRID_COL = 0x1a1a2e;
const NODE_REST = 0x00cccc;
const NODE_HOT = 0x00ffff;
const BG = 0x0a0a0f;

let scene, camera, renderer, controls, raycaster, mouse;
let nodeMeshes = [];          // {mesh, slug, xyz, label}
let activeSlug = null;
let hoveredNode = null;
let labelDiv = null;
let cubeGroup;

// Pull PAGES from the router (already on window via router.js)
function getPages() { return window.__LG_PAGES || {}; }

// ── init ──────────────────────────────────────────────
export function init(canvas) {
  scene = new THREE.Scene();
  scene.fog = new THREE.FogExp2(BG, 0.12);

  camera = new THREE.PerspectiveCamera(50, canvas.clientWidth / canvas.clientHeight, 0.1, 100);
  camera.position.set(5, 4, 5);

  renderer = new THREE.WebGLRenderer({ canvas, antialias: true, alpha: true });
  renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
  renderer.setSize(canvas.clientWidth, canvas.clientHeight);
  renderer.setClearColor(BG, 1);

  controls = new OrbitControls(camera, canvas);
  controls.enableDamping = true;
  controls.dampingFactor = 0.08;
  controls.enablePan = false;
  controls.minDistance = 3;
  controls.maxDistance = 12;
  controls.autoRotate = true;
  controls.autoRotateSpeed = 0.4;

  raycaster = new THREE.Raycaster();
  raycaster.params.Points = { threshold: 0.3 };
  mouse = new THREE.Vector2(-9, -9);

  cubeGroup = new THREE.Group();
  scene.add(cubeGroup);

  buildWireframe();
  buildContourPlanes();
  buildNodes();
  buildEdgeGlow();
  addLights();
  createLabel();

  canvas.addEventListener('mousemove', onMouseMove);
  canvas.addEventListener('click', onClick);
  canvas.addEventListener('touchstart', onTouch, { passive: false });

  animate();
}

// ── wireframe cube shell ──────────────────────────────
function buildWireframe() {
  // outer 3x3x3 bounding wireframe
  const geo = new THREE.BoxGeometry(2, 2, 2);
  const edges = new THREE.EdgesGeometry(geo);
  const mat = new THREE.LineBasicMaterial({ color: ACCENT, opacity: 0.25, transparent: true });
  const wire = new THREE.LineSegments(edges, mat);
  cubeGroup.add(wire);

  // inner grid lines along each axis
  const lineMat = new THREE.LineBasicMaterial({ color: GRID_COL, opacity: 0.4, transparent: true });
  for (let axis = 0; axis < 3; axis++) {
    for (let i = 0; i <= 2; i++) {
      for (let j = 0; j <= 2; j++) {
        const pts = [];
        for (let k = 0; k <= 2; k++) {
          const v = [0, 0, 0];
          if (axis === 0) { v[0] = k - 1; v[1] = i - 1; v[2] = j - 1; }
          if (axis === 1) { v[0] = i - 1; v[1] = k - 1; v[2] = j - 1; }
          if (axis === 2) { v[0] = i - 1; v[1] = j - 1; v[2] = k - 1; }
          pts.push(new THREE.Vector3(v[0], v[1], v[2]));
        }
        const g = new THREE.BufferGeometry().setFromPoints(pts);
        cubeGroup.add(new THREE.Line(g, lineMat));
      }
    }
  }
}

// ── contour planes on each z-layer ───────────────────
function buildContourPlanes() {
  const layers = [0, 1, 2, 3]; // z=0,1,2 + the extra z=3 for Iran/Hormuz
  layers.forEach(z => {
    const zPos = z - 1; // center at origin: z=0→-1, z=1→0, z=2→1, z=3→2
    const geo = new THREE.PlaneGeometry(2, 2, 8, 8);
    const mat = new THREE.MeshBasicMaterial({
      color: ACCENT,
      wireframe: true,
      opacity: z === 3 ? 0.06 : 0.04,
      transparent: true,
      side: THREE.DoubleSide
    });
    const plane = new THREE.Mesh(geo, mat);
    plane.rotation.x = -Math.PI / 2;
    plane.position.y = zPos;
    cubeGroup.add(plane);
  });
}

// ── node spheres ─────────────────────────────────────
function buildNodes() {
  const pages = getPages();
  const sphereGeo = new THREE.SphereGeometry(0.08, 16, 16);

  Object.entries(pages).forEach(([slug, p]) => {
    const [x, y, z] = p.xyz.split(',').map(Number);
    const pos = new THREE.Vector3(x - 1, z - 1, y - 1); // map: x→x, z→y(up), y→z(depth)

    // glow sprite behind
    const spriteMat = new THREE.SpriteMaterial({
      map: makeGlowTexture(),
      color: ACCENT,
      transparent: true,
      opacity: 0.4,
      blending: THREE.AdditiveBlending
    });
    const sprite = new THREE.Sprite(spriteMat);
    sprite.scale.set(0.5, 0.5, 1);
    sprite.position.copy(pos);
    cubeGroup.add(sprite);

    // solid node
    const mat = new THREE.MeshStandardMaterial({
      color: NODE_REST,
      emissive: NODE_REST,
      emissiveIntensity: 0.6,
      metalness: 0.3,
      roughness: 0.5
    });
    const mesh = new THREE.Mesh(sphereGeo, mat);
    mesh.position.copy(pos);
    cubeGroup.add(mesh);

    nodeMeshes.push({ mesh, sprite, slug, xyz: p.xyz, name: p.n, pos });
  });
}

// ── edge glow beams connecting adjacent nodes ────────
function buildEdgeGlow() {
  const mat = new THREE.LineBasicMaterial({
    color: ACCENT,
    opacity: 0.12,
    transparent: true
  });
  const pages = getPages();
  const coords = Object.values(pages).map(p => p.xyz.split(',').map(Number));
  const done = new Set();

  coords.forEach(([ax, ay, az]) => {
    coords.forEach(([bx, by, bz]) => {
      const dist = Math.abs(ax - bx) + Math.abs(ay - by) + Math.abs(az - bz);
      if (dist !== 1) return;
      const key = [[ax, ay, az].join(), [bx, by, bz].join()].sort().join('|');
      if (done.has(key)) return;
      done.add(key);
      const pts = [
        new THREE.Vector3(ax - 1, az - 1, ay - 1),
        new THREE.Vector3(bx - 1, bz - 1, by - 1)
      ];
      const g = new THREE.BufferGeometry().setFromPoints(pts);
      cubeGroup.add(new THREE.Line(g, mat));
    });
  });
}

// ── glow texture (procedural) ────────────────────────
let glowTex = null;
function makeGlowTexture() {
  if (glowTex) return glowTex;
  const size = 64;
  const c = document.createElement('canvas');
  c.width = c.height = size;
  const ctx = c.getContext('2d');
  const grad = ctx.createRadialGradient(size / 2, size / 2, 0, size / 2, size / 2, size / 2);
  grad.addColorStop(0, 'rgba(0,204,204,1)');
  grad.addColorStop(0.3, 'rgba(0,204,204,0.4)');
  grad.addColorStop(1, 'rgba(0,204,204,0)');
  ctx.fillStyle = grad;
  ctx.fillRect(0, 0, size, size);
  glowTex = new THREE.CanvasTexture(c);
  return glowTex;
}

// ── lights ───────────────────────────────────────────
function addLights() {
  scene.add(new THREE.AmbientLight(0x334455, 1.2));
  const pt = new THREE.PointLight(ACCENT, 2, 20);
  pt.position.set(3, 4, 3);
  scene.add(pt);
  const pt2 = new THREE.PointLight(0x4466aa, 1.5, 15);
  pt2.position.set(-3, -2, -3);
  scene.add(pt2);
}

// ── hover label ──────────────────────────────────────
function createLabel() {
  labelDiv = document.createElement('div');
  labelDiv.className = 'cube-label';
  labelDiv.style.display = 'none';
  document.getElementById('cube-overlay').appendChild(labelDiv);
}

function updateLabel(node, canvasRect) {
  if (!node) { labelDiv.style.display = 'none'; return; }
  const v = node.pos.clone().project(camera);
  const x = (v.x * 0.5 + 0.5) * canvasRect.width;
  const y = (-v.y * 0.5 + 0.5) * canvasRect.height;
  labelDiv.textContent = node.name + ' [' + node.xyz + ']';
  labelDiv.style.display = 'block';
  labelDiv.style.left = x + 'px';
  labelDiv.style.top = (y - 30) + 'px';
}

// ── interaction ──────────────────────────────────────
function onMouseMove(e) {
  const rect = renderer.domElement.getBoundingClientRect();
  mouse.x = ((e.clientX - rect.left) / rect.width) * 2 - 1;
  mouse.y = -((e.clientY - rect.top) / rect.height) * 2 + 1;
  controls.autoRotate = true;
}

function onClick() {
  if (hoveredNode) {
    location.hash = '#' + hoveredNode.slug;
    const evt = new CustomEvent('cube-nav', { detail: hoveredNode.slug });
    window.dispatchEvent(evt);
  }
}

function onTouch(e) {
  if (e.touches.length !== 1) return;
  const rect = renderer.domElement.getBoundingClientRect();
  const t = e.touches[0];
  mouse.x = ((t.clientX - rect.left) / rect.width) * 2 - 1;
  mouse.y = -((t.clientY - rect.top) / rect.height) * 2 + 1;
  // raycast immediately for touch
  doRaycast();
  if (hoveredNode) {
    e.preventDefault();
    location.hash = '#' + hoveredNode.slug;
  }
}

function doRaycast() {
  raycaster.setFromCamera(mouse, camera);
  const meshes = nodeMeshes.map(n => n.mesh);
  const hits = raycaster.intersectObjects(meshes);
  const prev = hoveredNode;
  hoveredNode = null;

  if (hits.length > 0) {
    const hit = hits[0].object;
    hoveredNode = nodeMeshes.find(n => n.mesh === hit) || null;
  }

  // update highlight state
  if (prev && prev !== hoveredNode) {
    const isActive = prev.slug === activeSlug;
    prev.mesh.material.emissiveIntensity = isActive ? 1.0 : 0.6;
    prev.mesh.scale.setScalar(isActive ? 1.3 : 1);
    prev.sprite.material.opacity = isActive ? 0.7 : 0.4;
    renderer.domElement.style.cursor = 'default';
  }
  if (hoveredNode) {
    hoveredNode.mesh.material.emissiveIntensity = 1.2;
    hoveredNode.mesh.scale.setScalar(1.5);
    hoveredNode.sprite.material.opacity = 0.8;
    renderer.domElement.style.cursor = 'pointer';
    controls.autoRotate = false;
  }
}

// ── highlight active node ────────────────────────────
export function setActive(slug) {
  activeSlug = slug;
  nodeMeshes.forEach(n => {
    const isActive = n.slug === slug;
    n.mesh.material.color.setHex(isActive ? ACCENT_HI : NODE_REST);
    n.mesh.material.emissive.setHex(isActive ? ACCENT_HI : NODE_REST);
    n.mesh.material.emissiveIntensity = isActive ? 1.0 : 0.6;
    n.mesh.scale.setScalar(isActive ? 1.3 : 1);
    n.sprite.material.opacity = isActive ? 0.7 : 0.4;
    n.sprite.scale.setScalar(isActive ? 0.7 : 0.5);
  });
}

// ── resize ───────────────────────────────────────────
export function resize(w, h) {
  if (!renderer) return;
  camera.aspect = w / h;
  camera.updateProjectionMatrix();
  renderer.setSize(w, h);
}

// ── animate ──────────────────────────────────────────
function animate() {
  requestAnimationFrame(animate);
  controls.update();
  doRaycast();
  const rect = renderer.domElement.getBoundingClientRect();
  updateLabel(hoveredNode, rect);

  // subtle pulse on active node
  if (activeSlug) {
    const n = nodeMeshes.find(n => n.slug === activeSlug);
    if (n) {
      const t = performance.now() * 0.003;
      n.sprite.scale.setScalar(0.6 + Math.sin(t) * 0.1);
    }
  }

  renderer.render(scene, camera);
}

// ── cleanup ──────────────────────────────────────────
export function dispose() {
  if (renderer) {
    renderer.dispose();
    controls.dispose();
  }
}
