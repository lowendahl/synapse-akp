/* ── OKF Pack Explorer — Main Init ──────────────────────────
   Bootstraps the 3D graph, wires up UI controls, keyboard.
   Depends on: constants.js, graph-config.js, hover.js, drawer.js
   Expects: ForceGraph3D (global), GRAPH_DATA (global)
   <200 LoC                                                    */

(function() {
  var graph;
  var activeTypes = new Set();
  var activePacks = new Set();
  var searchTerm = "";

  function updateVisibility() {
    graph
      .nodeVisibility(function(n) { return isNodeVisible(n, activePacks, activeTypes, searchTerm); })
      .linkVisibility(function(l) { return isLinkVisible(l, activePacks, activeTypes, searchTerm); })
      .nodeColor(function(n) { return getNodeColor(n, hoverNode, highlightNodes); });
  }
  _updateVisibility = updateVisibility;

  function init() {
    var data = GRAPH_DATA;

    // Discover packs and types
    var packSet = {};
    var typeSet = {};
    data.nodes.forEach(function(n) {
      packSet[n.pack] = true;
      typeSet[n.type] = true;
    });
    var packs = Object.keys(packSet).sort();
    var types = Object.keys(typeSet).sort();

    packs.forEach(function(p) { activePacks.add(p); });
    types.forEach(function(t) { activeTypes.add(t); });
    initPackOffsets(packs);

    // Stats
    document.getElementById("stat-nodes").textContent = data.nodes.length + " nodes";
    document.getElementById("stat-edges").textContent = data.links.length + " edges";
    document.getElementById("stat-packs").textContent = packs.length + " packs";

    // ── Pack Toggles ───────────────────────────────────────
    var togglesEl = document.getElementById("pack-toggles");
    packs.forEach(function(p) {
      var btn = document.createElement("button");
      btn.className = "pack-toggle active";
      btn.textContent = p.replace("kp-", "").toUpperCase();
      btn.style.borderColor = PACK_COLORS[p] || "#888";
      btn.addEventListener("click", function() {
        if (activePacks.has(p)) activePacks.delete(p); else activePacks.add(p);
        btn.classList.toggle("active");
        updateVisibility();
        updateNebulaeVisibility(activePacks);
      });
      togglesEl.appendChild(btn);
    });

    // ── Legend ──────────────────────────────────────────────
    var legendEl = document.getElementById("legend");
    types.forEach(function(t) {
      var item = document.createElement("div");
      item.className = "legend-item";
      var dot = document.createElement("span");
      dot.className = "legend-dot";
      dot.style.background = getTypeColor(t);
      item.appendChild(dot);
      item.appendChild(document.createTextNode(t));
      item.addEventListener("click", function() {
        if (activeTypes.has(t)) activeTypes.delete(t); else activeTypes.add(t);
        item.classList.toggle("dimmed");
        updateVisibility();
      });
      legendEl.appendChild(item);
    });

    // ── Search ─────────────────────────────────────────────
    document.getElementById("search-box").addEventListener("input", function(e) {
      searchTerm = e.target.value;
      updateVisibility();
    });

    // ── Cross-pack toggle ─────────────────────────────────
    document.getElementById("xpack-toggle").addEventListener("change", function(e) {
      showCrossPackAlways = e.target.checked;
      updateVisibility();
    });

    // ── Drawer controls ────────────────────────────────────
    document.getElementById("drawer-close").addEventListener("click", function() {
      closeDrawer();
      clearHighlight(graph);
    });
    document.getElementById("drawer-overlay").addEventListener("click", function() {
      closeDrawer();
      clearHighlight(graph);
    });

    // ── Build Graph ────────────────────────────────────────
    var container = document.getElementById("graph-container");
    graph = ForceGraph3D()(container)
      .graphData(data)
      .nodeVal(function(n) { return getNodeSize(n); })
      .nodeColor(function(n) { return getNodeColor(n, hoverNode, highlightNodes); })
      .nodeOpacity(0.92)
      .nodeResolution(16)
      .nodeLabel(function() { return ""; })
      .linkColor(function(l) { return getLinkColor(l, highlightLinks); })
      .linkOpacity(0.8)
      .linkWidth(function(l) { return highlightLinks.has(l) ? 2.5 : 1.2; })
      .linkDirectionalArrowLength(4)
      .linkDirectionalArrowRelPos(1)
      .linkDirectionalParticles(function(l) { return highlightLinks.has(l) ? 3 : 0; })
      .linkDirectionalParticleWidth(2)
      .linkDirectionalParticleColor(function() { return "rgba(177,31,75,0.8)"; })
      .linkVisibility(function(l) { return isLinkVisible(l, activePacks, activeTypes, searchTerm); })
      .nodeVisibility(function(n) { return isNodeVisible(n, activePacks, activeTypes, searchTerm); })
      .onNodeClick(function(n) {
        openDrawer(n, graph);
        highlightFromDrawer(n, graph);
      })
      .onNodeHover(function(n) { onNodeHover(n, graph); })
      .onBackgroundClick(function() { clearHighlight(graph); })
      .d3AlphaDecay(0.02)
      .d3VelocityDecay(0.3)
      .warmupTicks(120)
      .cooldownTicks(300)
      .backgroundColor("rgba(0,0,0,0)");

    configureForces(graph, data);

    // ── Galaxy nebulae ──────────────────────────────────────
    setTimeout(function() { initNebulae(graph, packs); }, 200);

    // ── Background color from theme ────────────────────────
    setTimeout(function() {
      var renderer = graph.renderer();
      if (renderer) {
        var isDark = document.documentElement.getAttribute("data-theme") === "dark";
        renderer.setClearColor(isDark ? 0x0a0a0a : 0xf7f4ef, 1);
      }
    }, 100);
  }

  // ── Keyboard shortcuts ─────────────────────────────────
  document.addEventListener("keydown", function(e) {
    if (e.key === "Escape") {
      closeDrawer();
      if (graph) clearHighlight(graph);
    }
    if (e.key === "/" && document.activeElement !== document.getElementById("search-box")) {
      e.preventDefault();
      document.getElementById("search-box").focus();
    }
  });

  init();
})();
