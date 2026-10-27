// Exportain Shorts — realistic 3D layer (three.js, physically based lighting, rendered by SwiftShader in headless
// Chromium). A scene opts in from board.json with  "gl": {"world": "ship", "cam": "orbit", ...}  and draws its SVG
// on a transparent background (overlay text/cards only). Worlds: ship, port, globe, warehouse, docs, fabric, farm.
// Every world takes options so each Short can look different (time of day, palette, camera move, props).
import * as THREE from './three/three.module.js';
import { RoomEnvironment } from './three/RoomEnvironment.js';

const W = 1080, H = 1920;
const BRAND = ['#005A1E', '#2E8B2E', '#5CBF14', '#F2B705', '#0E8C88', '#0B3B5C', '#b5452f', '#2c5aa0', '#d9822b'];
let renderer, pmrem, envTex, canvas;
const worlds = {};          // cache per scene id
const rnd = s => { let x = Math.sin(s * 9301 + 49297) * 233280; return x - Math.floor(x); };
const lerp = (a, b, t) => a + (b - a) * t, cl = (v, a = 0, b = 1) => Math.max(a, Math.min(b, v));
const ease = x => x < .5 ? 4 * x * x * x : 1 - Math.pow(-2 * x + 2, 3) / 2;

function init() {
  canvas = document.createElement('canvas');
  canvas.id = 'gl'; canvas.width = W; canvas.height = H;
  Object.assign(canvas.style, { position: 'absolute', inset: '0', width: '100%', height: '100%', zIndex: '0', display: 'none' });
  const st = document.getElementById('st'); st.insertBefore(canvas, st.firstChild);
  renderer = new THREE.WebGLRenderer({ canvas, antialias: true, preserveDrawingBuffer: true, powerPreference: 'high-performance' });
  renderer.setPixelRatio(1); renderer.setSize(W, H, false);
  renderer.toneMapping = THREE.ACESFilmicToneMapping; renderer.toneMappingExposure = 1.05;
  renderer.outputColorSpace = THREE.SRGBColorSpace;
  renderer.shadowMap.enabled = true; renderer.shadowMap.type = THREE.PCFSoftShadowMap;
  pmrem = new THREE.PMREMGenerator(renderer);
  envTex = pmrem.fromScene(new RoomEnvironment(), 0.04).texture;
}

// ---------------------------------------------------------------- textures (canvas, no downloads)
function canvasTex(w, h, draw, repeat) {
  const c = document.createElement('canvas'); c.width = w; c.height = h; const g = c.getContext('2d'); draw(g, w, h);
  const t = new THREE.CanvasTexture(c); t.colorSpace = THREE.SRGBColorSpace; t.anisotropy = 4;
  if (repeat) { t.wrapS = t.wrapT = THREE.RepeatWrapping; t.repeat.set(...repeat); }
  return t;
}
function containerTex(col, label, seed) {
  return canvasTex(512, 256, (g, w, h) => {
    g.fillStyle = col; g.fillRect(0, 0, w, h);
    for (let x = 0; x < w; x += 16) {                       // corrugation
      const gr = g.createLinearGradient(x, 0, x + 16, 0);
      gr.addColorStop(0, 'rgba(0,0,0,.28)'); gr.addColorStop(.35, 'rgba(255,255,255,.12)'); gr.addColorStop(.7, 'rgba(0,0,0,.05)'); gr.addColorStop(1, 'rgba(0,0,0,.3)');
      g.fillStyle = gr; g.fillRect(x, 0, 16, h);
    }
    g.fillStyle = 'rgba(0,0,0,.35)'; g.fillRect(0, 0, w, 10); g.fillRect(0, h - 12, w, 12);
    for (let i = 0; i < 40; i++) { g.fillStyle = `rgba(60,30,10,${rnd(seed + i) * .12})`; g.fillRect(rnd(seed * 3 + i) * w, rnd(seed * 7 + i) * h, 30 * rnd(i + seed), 4 + 20 * rnd(i * 2 + seed)); }
    if (label) { g.font = '800 54px Poppins, Inter, sans-serif'; g.fillStyle = 'rgba(255,255,255,.92)'; g.fillText(label, 26, 88); }
    g.font = '600 22px Inter, sans-serif'; g.fillStyle = 'rgba(255,255,255,.7)'; g.fillText('EXPU ' + (100000 + Math.floor(rnd(seed) * 899999)) + ' 4', 26, h - 30);
  });
}
function paperTex(title, lines, accent = '#005A1E', stamp = '') {
  return canvasTex(512, 720, (g, w, h) => {
    g.fillStyle = '#fbfaf6'; g.fillRect(0, 0, w, h);
    g.fillStyle = accent; g.fillRect(0, 0, w, 70);
    g.font = '800 34px Poppins, Inter, sans-serif'; g.fillStyle = '#fff'; g.fillText(title, 28, 48);
    for (let i = 0; i < lines; i++) { g.fillStyle = i % 4 === 0 ? '#9aa6ae' : '#cfd6da'; g.fillRect(34, 110 + i * 38, (i % 3 === 2 ? 260 : 420) - (i * 37 % 90), 12); }
    if (stamp) { g.save(); g.translate(360, 600); g.rotate(-.25); g.strokeStyle = 'rgba(46,139,46,.85)'; g.lineWidth = 8; g.strokeRect(-110, -44, 220, 88);
      g.font = '800 40px Poppins, Inter, sans-serif'; g.fillStyle = 'rgba(46,139,46,.85)'; g.textAlign = 'center'; g.fillText(stamp, 0, 14); g.restore(); }
  });
}
function skyTex(top, mid, bottom) {
  return canvasTex(16, 512, (g, w, h) => { const gr = g.createLinearGradient(0, 0, 0, h); gr.addColorStop(0, top); gr.addColorStop(.55, mid); gr.addColorStop(1, bottom); g.fillStyle = gr; g.fillRect(0, 0, w, h); });
}
const TIME = {   // lighting presets: rotate them between Shorts
  day:    { sky: ['#4f8fd0', '#9cc6e8', '#eaf2f7'], sun: '#fff4e0', si: 3.2, amb: .55, fog: '#bcd6ea', exp: 1.05, pos: [30, 40, 20] },
  golden: { sky: ['#2b4c7e', '#f0a35e', '#ffd9a0'], sun: '#ffc47a', si: 3.6, amb: .45, fog: '#f2c08c', exp: 1.0, pos: [-40, 14, 30] },
  dusk:   { sky: ['#0d1b33', '#3c4f7d', '#e07b5f'], sun: '#ff9a6b', si: 2.4, amb: .35, fog: '#4b5a80', exp: 1.15, pos: [-30, 8, -40] },
  studio: { sky: ['#0b3b5c', '#0e5a6e', '#0e8c88'], sun: '#ffffff', si: 2.6, amb: .7, fog: '#0e5a6e', exp: 1.1, pos: [10, 30, 25] },
};
function baseScene(o) {
  const L = TIME[o.time || 'day'];
  const s = new THREE.Scene(); s.environment = envTex; s.background = skyTex(...L.sky);
  s.fog = new THREE.Fog(L.fog, o.fogNear || 40, o.fogFar || 160);
  const sun = new THREE.DirectionalLight(L.sun, L.si); sun.position.set(...L.pos); sun.castShadow = true;
  sun.shadow.mapSize.set(2048, 2048); Object.assign(sun.shadow.camera, { left: -40, right: 40, top: 40, bottom: -40, near: 1, far: 200 }); sun.shadow.bias = -0.0004;
  s.add(sun, new THREE.HemisphereLight('#dbeeff', '#3b3024', L.amb));
  const cam = new THREE.PerspectiveCamera(o.fov || 38, W / H, 0.1, 600);
  return { s, cam, sun, exp: L.exp };
}
const std = (c, r = .55, m = .2) => new THREE.MeshStandardMaterial({ color: c, roughness: r, metalness: m });
function box(w, h, d, mat, x = 0, y = 0, z = 0, parent) { const m = new THREE.Mesh(new THREE.BoxGeometry(w, h, d), mat); m.position.set(x, y, z); m.castShadow = m.receiveShadow = true; parent && parent.add(m); return m; }

function container(seed, label, palette) {
  const col = (palette || BRAND)[Math.floor(rnd(seed) * (palette || BRAND).length)];
  const side = new THREE.MeshStandardMaterial({ map: containerTex(col, label, seed), roughness: .5, metalness: .45 });
  const end = std(col, .55, .45), top = std(new THREE.Color(col).multiplyScalar(.85), .6, .4);
  const m = new THREE.Mesh(new THREE.BoxGeometry(2.44, 2.59, 6.06), [side, side, top, top, end, end]);
  m.castShadow = m.receiveShadow = true; return m;
}
function sea(s, o) {
  const g = new THREE.PlaneGeometry(600, 600, 160, 160);
  const m = new THREE.Mesh(g, new THREE.MeshPhysicalMaterial({ color: o.water || '#0b4f6c', roughness: .12, metalness: .05, clearcoat: 1, clearcoatRoughness: .1 }));
  m.rotation.x = -Math.PI / 2; m.receiveShadow = true; s.add(m);
  const base = g.attributes.position.array.slice();
  return t => { const p = g.attributes.position.array; for (let i = 0; i < p.length; i += 3) { const x = base[i], y = base[i + 1];
    p[i + 2] = Math.sin(x * .18 + t * 1.3) * .35 + Math.cos(y * .21 + t * .9) * .3 + Math.sin((x + y) * .5 + t * 2.1) * .08; }
    g.attributes.position.needsUpdate = true; g.computeVertexNormals(); };
}
function shipMesh(o, seed = 1) {
  const g = new THREE.Group();
  const hullShape = new THREE.Shape(); hullShape.moveTo(-6, 0); hullShape.lineTo(6, 0); hullShape.lineTo(5.2, -3.4); hullShape.lineTo(-5.2, -3.4); hullShape.lineTo(-6, 0);
  const hull = new THREE.Mesh(new THREE.ExtrudeGeometry(hullShape, { depth: 64, bevelEnabled: false }), [std(o.hull || '#1d2a33', .55, .35), std('#8f2c2c', .6, .3)]);
  hull.position.z = -32; hull.castShadow = hull.receiveShadow = true; g.add(hull);
  const bow = new THREE.Mesh(new THREE.ConeGeometry(6, 9, 4, 1), std(o.hull || '#1d2a33', .55, .35)); bow.rotation.x = Math.PI / 2; bow.rotation.y = Math.PI / 4; bow.scale.set(1, 1, .4); bow.position.set(0, -1.7, 36); g.add(bow);
  box(12.2, .3, 64, std('#c9ccc8', .7, .2), 0, 0, 0, g);
  const bridge = new THREE.Group(); g.add(bridge); bridge.position.set(0, 0, -26);
  box(10, 7, 5, std('#f1f1ee', .4, .1), 0, 3.5, 0, bridge);
  for (let r = 0; r < 4; r++) box(10.1, .5, 5.1, std('#24384b', .2, .6), 0, 1.6 + r * 1.5, 0, bridge);
  box(2, 3, 2, std('#b5452f', .5, .3), 0, 8.5, 1, bridge);
  const lbl = o.label || 'EXPORTAIN';
  for (let z = -20; z < 31; z += 6.3) for (let x = -2; x <= 2; x++) for (let y = 0; y < (o.stack || 4); y++) {
    if (rnd(seed + z * 7 + x * 13 + y) > .93) continue;
    const c = container(seed + z * 3 + x * 11 + y * 17, (rnd(z + x + y + seed) > .82) ? lbl : '', o.palette); c.position.set(x * 2.5, 1.45 + y * 2.62, z); g.add(c);
  }
  return g;
}

// ---------------------------------------------------------------- worlds
const W3 = {
  ship(o) {
    const B = baseScene({ fogNear: 90, fogFar: 420, ...o }); const wave = sea(B.s, o);
    const sh = shipMesh(o, o.seed || 3); sh.rotation.y = o.heading ?? -0.35; B.s.add(sh); const FB = 3.2;
    const tug = shipMesh({ ...o, stack: 0 }, 9); tug.scale.set(.18, .18, .18); tug.position.set(18, 0, 30); B.s.add(tug);
    return { ...B, update(lt, d, t) {
      wave(t); sh.position.y = FB + Math.sin(t * .9) * .18; sh.rotation.z = Math.sin(t * .7) * .012; sh.position.z = lt * (o.speed ?? .9);
      cam(B.cam, o.cam || 'orbit', lt, d, { r: 105, h: 26, look: [0, 6, sh.position.z], ...o });
    } };
  },
  port(o) {
    const B = baseScene({ fogNear: 90, fogFar: 380, ...o }); const wave = sea(B.s, { water: '#123f55', ...o });
    const quay = box(90, 3, 160, std('#8d9399', .9, .05), -45, 1.2, 0, B.s);
    for (let i = 0; i < 3; i++) {                                    // gantry cranes
      const c = new THREE.Group(); c.position.set(-8, 2.7, -40 + i * 34); B.s.add(c);
      const red = std(i % 2 ? '#d6451f' : '#f2b705', .5, .5);
      box(1.2, 34, 1.2, red, 0, 17, -6, c); box(1.2, 34, 1.2, red, 0, 17, 6, c); box(1.2, 34, 1.2, red, -16, 17, -6, c); box(1.2, 34, 1.2, red, -16, 17, 6, c);
      box(60, 2.2, 2.2, red, 6, 34, 0, c); box(4, 3, 5, std('#e8e8e8', .4, .2), 10 + i * 4, 31.5, 0, c);
      c.userData.trolley = c.children[c.children.length - 1];
    }
    for (let x = 0; x < 6; x++) for (let z = 0; z < 9; z++) for (let y = 0; y < 1 + Math.floor(rnd(x * 9 + z) * 4); y++) {   // yard stacks
      const k = container(x * 31 + z * 7 + y, rnd(x + z * 3 + y) > .9 ? (o.label || 'EXPORTAIN') : '', o.palette); k.position.set(-30 - x * 3, 2.7 + 1.3 + y * 2.62, -60 + z * 7); B.s.add(k);
    }
    const sh = shipMesh(o, 5); sh.position.set(14, 3.2, 0); B.s.add(sh);
    return { ...B, update(lt, d, t) {
      wave(t); sh.position.y = 3.2 + Math.sin(t * .8) * .12;
      B.s.children.forEach(c => { if (c.userData && c.userData.trolley) c.userData.trolley.position.x = 10 + Math.sin(t * .6 + c.position.z) * 14; });
      cam(B.cam, o.cam || 'crane', lt, d, { r: 90, h: 40, look: [-6, 8, 0], ...o });
    } };
  },
  globe(o) {
    const B = baseScene({ time: 'studio', fogFar: 400, ...o }); B.s.background = skyTex('#03121f', '#06263d', '#0b3b5c'); B.s.fog = null;
    const tex = canvasTex(1024, 512, (g, w, h) => {                 // ocean + lat/long grid + simplified land masses
      const gr = g.createLinearGradient(0, 0, 0, h); gr.addColorStop(0, '#0a4f73'); gr.addColorStop(.5, '#0d6d8f'); gr.addColorStop(1, '#0a4f73'); g.fillStyle = gr; g.fillRect(0, 0, w, h);
      g.strokeStyle = 'rgba(255,255,255,.08)'; g.lineWidth = 1; for (let x = 0; x < w; x += w / 24) { g.beginPath(); g.moveTo(x, 0); g.lineTo(x, h); g.stroke(); } for (let y = 0; y < h; y += h / 12) { g.beginPath(); g.moveTo(0, y); g.lineTo(w, y); g.stroke(); }
      const P = (lon, lat) => [(lon + 180) / 360 * w, (90 - lat) / 180 * h];
      const land = { // coarse outlines (lon,lat)
        na: [[-168, 66], [-140, 70], [-95, 72], [-60, 60], [-52, 47], [-80, 25], [-97, 18], [-105, 22], [-118, 33], [-125, 48], [-140, 60]],
        sa: [[-80, 10], [-60, 8], [-35, -7], [-40, -22], [-58, -38], [-70, -54], [-75, -40], [-80, -5]],
        eu: [[-10, 36], [0, 44], [-5, 48], [5, 58], [25, 70], [40, 66], [50, 46], [30, 40], [20, 36], [10, 44]],
        af: [[-17, 15], [-5, 36], [12, 37], [32, 31], [43, 12], [51, 11], [40, -15], [20, -35], [12, -18], [8, 4]],
        as: [[40, 66], [90, 76], [140, 72], [165, 62], [140, 45], [122, 30], [110, 20], [100, 8], [92, 22], [80, 8], [72, 22], [60, 25], [48, 30], [50, 46]],
        au: [[113, -22], [130, -12], [145, -14], [153, -28], [146, -39], [130, -32], [115, -34]],
      };
      g.fillStyle = '#2e8b4e'; for (const k in land) { g.beginPath(); land[k].forEach(([a, b], i) => { const [x, y] = P(a, b); i ? g.lineTo(x, y) : g.moveTo(x, y); }); g.closePath(); g.fill(); }
      g.fillStyle = '#5CBF14'; const [bx, by] = P(90.4, 23.7); g.beginPath(); g.arc(bx, by, 7, 0, 7); g.fill();
    });
    const earth = new THREE.Mesh(new THREE.SphereGeometry(10, 96, 64), new THREE.MeshStandardMaterial({ map: tex, roughness: .7, metalness: .05 }));
    B.s.add(earth);
    const atm = new THREE.Mesh(new THREE.SphereGeometry(10.6, 64, 48), new THREE.MeshBasicMaterial({ color: '#5cbfff', transparent: true, opacity: .12, side: THREE.BackSide })); B.s.add(atm);
    const v = (lon, lat, r = 10.05) => { const p = (90 - lat) * Math.PI / 180, q = (lon + 180) * Math.PI / 180; return new THREE.Vector3(-r * Math.sin(p) * Math.cos(q), r * Math.cos(p), r * Math.sin(p) * Math.sin(q)); };
    const BD = [90.4, 23.7], dests = o.routes || [[-74, 40.7], [13.4, 52.5], [-0.1, 51.5], [139.7, 35.7], [55.3, 25.2], [-79.4, 43.7]];
    const arcs = dests.map(([lo, la], i) => {
      const a = v(...BD), b = v(lo, la), mid = a.clone().add(b).multiplyScalar(.5).normalize().multiplyScalar(10 + a.distanceTo(b) * .45);
      const curve = new THREE.QuadraticBezierCurve3(a, mid, b);
      const geo = new THREE.TubeGeometry(curve, 80, .06, 8, false);
      const m = new THREE.Mesh(geo, new THREE.MeshBasicMaterial({ color: ['#F2B705', '#5CBF14', '#ffffff', '#0E8C88'][i % 4] }));
      geo.setDrawRange(0, 0); earth.add(m);
      const dot = new THREE.Mesh(new THREE.SphereGeometry(.22, 16, 12), new THREE.MeshBasicMaterial({ color: '#ffffff' })); dot.position.copy(b); earth.add(dot);
      return { geo, n: geo.index.count, i };
    });
    return { ...B, update(lt, d, t) {
      earth.rotation.y = -1.9 + lt * (o.spin ?? .12);
      arcs.forEach(a => a.geo.setDrawRange(0, Math.floor(a.n * cl((lt - .4 - a.i * .35) / 1.2))));
      const z = lerp(o.z0 ?? 34, o.z1 ?? 27, ease(cl(lt / d))); B.cam.position.set(Math.sin(lt * .1) * 2, 4 + Math.sin(lt * .3), z); B.cam.lookAt(0, o.lookY ?? -1.5, 0);
    } };
  },
  warehouse(o) {
    const B = baseScene({ time: o.time || 'studio', fogNear: 30, fogFar: 110, ...o }); B.s.background = skyTex('#20262b', '#2f373d', '#3b444b');
    box(120, .2, 120, std('#9aa1a6', .85, .05), 0, -.1, 0, B.s);
    const cardboard = std('#c9975b', .9, 0), tape = std('#e9d3a8', .6, 0), wood = std('#a8743a', .8, 0);
    for (let r = 0; r < 4; r++) for (let c = 0; c < 5; c++) {                               // pallets with cartons
      const g = new THREE.Group(); g.position.set(-16 + c * 8, 0, -20 + r * 9); B.s.add(g);
      box(4.8, .5, 4.8, wood, 0, .25, 0, g);
      for (let y = 0; y < 2 + (r + c) % 3; y++) for (let a = 0; a < 2; a++) for (let b = 0; b < 2; b++) { const k = box(2.3, 1.6, 2.3, cardboard, -1.2 + a * 2.4, 1.3 + y * 1.62, -1.2 + b * 2.4, g); box(.3, 1.62, 2.32, tape, -1.2 + a * 2.4, 1.3 + y * 1.62, -1.2 + b * 2.4, g); }
    }
    for (let i = 0; i < 6; i++) { const l = new THREE.PointLight('#fff1d6', 120, 40, 2); l.position.set(-20 + i * 8, 14, 0); B.s.add(l); }
    return { ...B, update(lt, d) { cam(B.cam, o.cam || 'dolly', lt, d, { r: 34, h: 9, look: [0, 3, 0], ...o }); } };
  },
  docs(o) {
    const B = baseScene({ time: 'studio', ...o }); B.s.background = skyTex('#0b3b5c', '#0e5a6e', '#0e8c88'); B.s.fog = null;
    const desk = box(40, 1, 26, std('#6b4a33', .6, .05), 0, -.5, 0, B.s);
    const names = o.papers || [['Commercial Invoice', '#005A1E', 'CHECKED'], ['Packing List', '#0B3B5C', ''], ['Bill of Lading', '#0E8C88', 'B/L'], ['Certificate of Origin', '#b5452f', 'APPROVED'], ['Export LC', '#F2B705', '']];
    const sheets = names.map(([tt, col, st], i) => {
      const m = new THREE.Mesh(new THREE.BoxGeometry(5, .04, 7), [std('#fff', .8), std('#fff', .8), new THREE.MeshStandardMaterial({ map: paperTex(tt, 14, col, st), roughness: .8 }), std('#eee', .8), std('#fff', .8), std('#fff', .8)]);
      m.castShadow = m.receiveShadow = true; B.s.add(m); return { m, i };
    });
    return { ...B, update(lt, d, t) {
      sheets.forEach(({ m, i }) => { const p = ease(cl((lt - .2 - i * .45) / .9)); const tx = -9 + i * 4.5, tz = (i % 2) * 2.5 - 1;
        m.position.set(lerp(tx + 12, tx, p), lerp(9, .2 + i * .05, p) + (p >= 1 ? Math.sin(t * 1.6 + i) * .05 : 0), lerp(tz - 8, tz, p)); m.rotation.set(lerp(-1.2, 0, p), lerp(.9, (i - 2) * .12, p), lerp(.6, 0, p)); });
      B.cam.position.set(Math.sin(lt * .15) * 3, 22 - lt * .25, 15 - lt * .2); B.cam.lookAt(0, 0, 0);
    } };
  },
  fabric(o) {   // garment factory floor: fabric rolls + folded garments + sewing tables
    const B = baseScene({ time: 'studio', fogNear: 25, fogFar: 90, ...o }); B.s.background = skyTex('#1b2a33', '#24414e', '#2f5563');
    box(120, .2, 120, std('#b9c0c4', .85, .05), 0, -.1, 0, B.s);
    const cols = o.palette || ['#0B3B5C', '#d9822b', '#2E8B2E', '#b5452f', '#e8e2d6', '#5CBF14', '#2c5aa0'];
    for (let i = 0; i < 18; i++) { const r = new THREE.Mesh(new THREE.CylinderGeometry(.7, .7, 4, 32), std(cols[i % cols.length], .85, 0)); r.rotation.z = Math.PI / 2; r.position.set(-10 + (i % 6) * 1.5, .7 + Math.floor(i / 6) * 1.35, -6 - Math.floor(i / 6) * .2); r.castShadow = true; B.s.add(r); }
    for (let t = 0; t < 4; t++) { const g = new THREE.Group(); g.position.set(4 + (t % 2) * 9, 0, -6 + Math.floor(t / 2) * 8); B.s.add(g);
      box(6, .3, 3, std('#dfe3e6', .5, .2), 0, 3, 0, g); box(.3, 3, .3, std('#555', .5, .5), -2.7, 1.5, -1.2, g); box(.3, 3, .3, std('#555', .5, .5), 2.7, 1.5, 1.2, g);
      for (let s = 0; s < 4; s++) box(2.2, .25, 1.6, std(cols[(t + s) % cols.length], .9, 0), -1.4 + (s % 2) * 2.8, 3.3 + Math.floor(s / 2) * .26, 0, g); }
    for (let i = 0; i < 5; i++) { const l = new THREE.PointLight('#fff6e8', 90, 35, 2); l.position.set(-12 + i * 7, 10, 0); B.s.add(l); }
    return { ...B, update(lt, d) { cam(B.cam, o.cam || 'dolly', lt, d, { r: 26, h: 8, look: [0, 2.5, -2], ...o }); } };
  },
  farm(o) {     // agro exports: field rows + crates of produce
    const B = baseScene({ time: o.time || 'golden', fogNear: 30, fogFar: 140, ...o });
    box(300, .2, 300, std('#6f8f3a', .95, 0), 0, -.1, 0, B.s);
    for (let r = 0; r < 18; r++) for (let c = 0; c < 26; c++) { const p = new THREE.Mesh(new THREE.SphereGeometry(.55 + rnd(r * 26 + c) * .25, 12, 8), std(rnd(r + c) > .5 ? '#3f9b2f' : '#2e7d32', .9, 0)); p.position.set(-26 + c * 2, .45, -40 + r * 2.2); p.castShadow = true; B.s.add(p); }
    const produce = o.produce || '#f2b705';
    for (let i = 0; i < 6; i++) { const g = new THREE.Group(); g.position.set(-5 + (i % 3) * 3.4, 0, 6 + Math.floor(i / 3) * 3); B.s.add(g); box(3, 1.4, 2.2, std('#b07a43', .85, 0), 0, .7, 0, g);
      for (let k = 0; k < 14; k++) { const f = new THREE.Mesh(new THREE.SphereGeometry(.38, 14, 10), std(produce, .55, 0)); f.position.set(-1.1 + (k % 5) * .55, 1.5 + Math.floor(k / 5) * .25, -.6 + (k % 3) * .55); g.add(f); } }
    return { ...B, update(lt, d) { cam(B.cam, o.cam || 'crane', lt, d, { r: 26, h: 10, look: [0, 1.5, 6], ...o }); } };
  },
};

// camera moves: orbit | dolly | crane | push | flyby — vary per Short
function cam(c, kind, lt, d, o) {
  const p = ease(cl(lt / Math.max(d, .1))), [lx, ly, lz] = o.look;
  if (kind === 'orbit') { const a = (o.a0 ?? .6) + lt * (o.spinCam ?? .09); c.position.set(lx + Math.sin(a) * o.r, o.h + Math.sin(lt * .4), lz + Math.cos(a) * o.r); }
  else if (kind === 'dolly') c.position.set(lx + lerp(-o.r * .5, o.r * .4, p), o.h, lz + o.r * .9);
  else if (kind === 'crane') c.position.set(lx + o.r * .55, lerp(o.h * 1.6, o.h * .7, p), lz + o.r * .8);
  else if (kind === 'push') c.position.set(lx + o.r * .3, o.h, lz + lerp(o.r, o.r * .55, p));
  else c.position.set(lx + lerp(o.r, -o.r, p), o.h * .8, lz + o.r * .5);   // flyby
  c.lookAt(lx, ly, lz);
}

// ---------------------------------------------------------------- engine hook
let plan = null;
export function setPlan(p) { plan = p; }
const WHITE_LOGO = new URL('./logo_white_badge.png', import.meta.url).href;
let badgeSrc = null;
function badge(white) {
  const b = document.getElementById('badgeimg'); if (!b) return;
  if (badgeSrc === null) badgeSrc = b.getAttribute('src');
  const want = white ? WHITE_LOGO : badgeSrc; if (b.getAttribute('src') !== want) b.setAttribute('src', want);
}
export function frame(t) {
  if (!plan) return;
  const sc = plan.scenes.find(s => t >= s.start && t < s.end) || null;
  const gl = sc && sc.gl;
  badge(!!(sc && (sc.badge === 'white' || (gl && gl.badge !== 'dark'))) && t < plan.voice_duration);
  if (!gl || t >= plan.voice_duration) { if (canvas) canvas.style.display = 'none'; return; }
  if (!renderer) init();
  if (!worlds[sc.id]) worlds[sc.id] = W3[gl.world](gl);
  const w = worlds[sc.id]; renderer.toneMappingExposure = w.exp || 1.05;
  const lt = t - sc.start, d = sc.end - sc.start;
  w.update(lt, d, t); renderer.render(w.s, w.cam); canvas.style.display = 'block';
}
export const worldNames = Object.keys(W3);
