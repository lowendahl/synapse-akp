/* ── OKF Pack Explorer — Nebula / Galaxy Boundaries ──────────
   Renders translucent glow clouds and star dust around each
   knowledge pack to create distinct "galaxy" regions.
   Depends on: constants.js (PACK_OFFSETS, PACK_COLORS)
   <200 LoC                                                    */

var packNebulae = [];

function parseHexRGB(hex) {
  return {
    r: parseInt(hex.slice(1, 3), 16),
    g: parseInt(hex.slice(3, 5), 16),
    b: parseInt(hex.slice(5, 7), 16)
  };
}

function createNebulaCanvas(rgb, resolution) {
  var canvas = document.createElement("canvas");
  canvas.width = resolution;
  canvas.height = resolution;
  var ctx = canvas.getContext("2d");
  var cx = resolution / 2;

  // Slightly off-center for organic feel
  var grad = ctx.createRadialGradient(
    cx * 0.95, cx * 1.05, 0, cx, cx, cx
  );
  grad.addColorStop(0,    "rgba(" + rgb.r + "," + rgb.g + "," + rgb.b + ",0.09)");
  grad.addColorStop(0.25, "rgba(" + rgb.r + "," + rgb.g + "," + rgb.b + ",0.055)");
  grad.addColorStop(0.55, "rgba(" + rgb.r + "," + rgb.g + "," + rgb.b + ",0.02)");
  grad.addColorStop(0.85, "rgba(" + rgb.r + "," + rgb.g + "," + rgb.b + ",0.006)");
  grad.addColorStop(1,    "rgba(" + rgb.r + "," + rgb.g + "," + rgb.b + ",0.0)");
  ctx.fillStyle = grad;
  ctx.fillRect(0, 0, resolution, resolution);
  return canvas;
}

function initNebulae(graph, packs) {
  if (!window.THREE) return;
  var scene = graph.scene();

  packs.forEach(function(packId) {
    var off = PACK_OFFSETS[packId] || { x: 0, z: 0 };
    var hex = PACK_COLORS[packId] || "#888888";
    var rgb = parseHexRGB(hex);
    var group = new THREE.Group();

    // ── Core nebula glow ──
    var canvas1 = createNebulaCanvas(rgb, 512);
    var tex1 = new THREE.CanvasTexture(canvas1);
    var mat1 = new THREE.SpriteMaterial({
      map: tex1, transparent: true, depthWrite: false,
      blending: THREE.AdditiveBlending
    });
    var core = new THREE.Sprite(mat1);
    core.position.set(off.x, 0, off.z);
    core.scale.set(500, 500, 1);
    group.add(core);

    // ── Secondary halo (offset, larger, fainter) ──
    var canvas2 = createNebulaCanvas(rgb, 256);
    var tex2 = new THREE.CanvasTexture(canvas2);
    var mat2 = new THREE.SpriteMaterial({
      map: tex2, transparent: true, depthWrite: false,
      blending: THREE.AdditiveBlending, opacity: 0.35
    });
    var halo = new THREE.Sprite(mat2);
    halo.position.set(off.x + 30, 20, off.z - 25);
    halo.scale.set(620, 620, 1);
    group.add(halo);

    // ── Star dust particles ──
    var dustCount = 300;
    var positions = new Float32Array(dustCount * 3);
    for (var i = 0; i < dustCount; i++) {
      var theta = Math.random() * Math.PI * 2;
      var phi = Math.acos(2 * Math.random() - 1);
      var r = 60 + Math.random() * 150;
      positions[i * 3]     = off.x + r * Math.sin(phi) * Math.cos(theta);
      positions[i * 3 + 1] = r * Math.sin(phi) * Math.sin(theta) * 0.5;
      positions[i * 3 + 2] = off.z + r * Math.cos(phi);
    }
    var dustGeom = new THREE.BufferGeometry();
    dustGeom.setAttribute("position", new THREE.BufferAttribute(positions, 3));
    var dustMat = new THREE.PointsMaterial({
      color: new THREE.Color(hex),
      size: 1.2, transparent: true, opacity: 0.18,
      blending: THREE.AdditiveBlending, depthWrite: false
    });
    group.add(new THREE.Points(dustGeom, dustMat));

    scene.add(group);
    packNebulae.push({ group: group, packId: packId });
  });
}

function updateNebulaeVisibility(activePacks) {
  packNebulae.forEach(function(n) {
    n.group.visible = activePacks.has(n.packId);
  });
}
