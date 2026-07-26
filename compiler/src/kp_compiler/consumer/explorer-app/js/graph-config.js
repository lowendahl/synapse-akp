/* ── OKF Pack Explorer — Graph Configuration ────────────────
   Force layout, node sizing, coloring, visibility filters.
   Depends on: constants.js (getTypeColor, PACK_COLORS)
   <200 LoC                                                    */

var PACK_OFFSETS = {};

function initPackOffsets(packs) {
  packs.forEach(function(p, i) {
    var angle = (i / packs.length) * Math.PI * 2;
    PACK_OFFSETS[p] = {
      x: Math.cos(angle) * 200,
      z: Math.sin(angle) * 200
    };
  });
}

function configureForces(graph, data) {
  // Pack-cluster separation force
  graph.d3Force("pack-cluster", function(alpha) {
    data.nodes.forEach(function(n) {
      var off = PACK_OFFSETS[n.pack] || { x: 0, z: 0 };
      n.vx += (off.x - (n.x || 0)) * alpha * 0.04;
      n.vz += (off.z - (n.z || 0)) * alpha * 0.04;
    });
  });

  // Gravity — pull orphan/distant nodes back toward pack center
  graph.d3Force("gravity", function(alpha) {
    data.nodes.forEach(function(n) {
      var off = PACK_OFFSETS[n.pack] || { x: 0, z: 0 };
      var dx = (n.x || 0) - off.x;
      var dy = (n.y || 0);
      var dz = (n.z || 0) - off.z;
      var dist = Math.sqrt(dx * dx + dy * dy + dz * dz);
      if (dist > 150) {
        var pull = alpha * 0.06 * (dist - 150) / dist;
        n.vx -= dx * pull;
        n.vy -= dy * pull;
        n.vz -= dz * pull;
      }
    });
  });

  graph.d3Force("charge").strength(-50);
  graph.d3Force("link").distance(function(l) {
    var s = typeof l.source === "object" ? l.source : null;
    var t = typeof l.target === "object" ? l.target : null;
    return (s && t && s.pack !== t.pack) ? 250 : 45;
  });
}

function getNodeSize(n) {
  var sc = (n.sections || []).length;
  var base = {
    "KPI": 6, "Metric": 5, "Framework": 7, "Methodology": 8,
    "Stage": 7, "Process": 4, "Evidence Map": 4, "Program": 5,
    "Priority": 6, "Strategy": 6
  };
  return (base[n.type] || 3) + Math.min(sc * 0.3, 3);
}

function getNodeColor(n, hoverNode, highlightNodes) {
  if (hoverNode === n) return "#ffffff";
  if (highlightNodes.size > 0 && !highlightNodes.has(n)) return "#333333";
  return getTypeColor(n.type);
}

function getLinkColor(l, highlightLinks) {
  if (highlightLinks.has(l)) return "rgba(253,142,161,1)";
  var sn = typeof l.source === "object" ? l.source : null;
  var tn = typeof l.target === "object" ? l.target : null;
  if (sn && tn && sn.pack !== tn.pack) return "rgba(253,142,161,0.18)";
  return "rgba(180,180,180,0.5)";
}

function isNodeVisible(n, activePacks, activeTypes, searchTerm) {
  if (!activePacks.has(n.pack)) return false;
  if (!activeTypes.has(n.type)) return false;
  if (searchTerm) {
    var t = searchTerm.toLowerCase();
    if (!n.title.toLowerCase().includes(t) &&
        !n.id.toLowerCase().includes(t) &&
        !(n.aliases || []).some(function(a) { return a.toLowerCase().includes(t); }))
      return false;
  }
  return true;
}

function isLinkVisible(l, activePacks, activeTypes, searchTerm) {
  var s = typeof l.source === "object" ? l.source : null;
  var t = typeof l.target === "object" ? l.target : null;
  if (!s || !t) return true;
  if (!isNodeVisible(s, activePacks, activeTypes, searchTerm) ||
      !isNodeVisible(t, activePacks, activeTypes, searchTerm)) return false;
  // Cross-pack toggle: hide unless always-on or currently highlighted
  if (s.pack !== t.pack && !showCrossPackAlways && !highlightLinks.has(l)) return false;
  return true;
}
