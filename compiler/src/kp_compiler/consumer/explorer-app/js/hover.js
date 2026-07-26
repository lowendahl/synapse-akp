/* ── OKF Pack Explorer — Hover & Highlight ──────────────────
   Node hover highlighting, tooltip positioning, highlight
   clear on background click.
   Depends on: constants.js, graph-config.js
   <200 LoC                                                    */

var highlightNodes = new Set();
var highlightLinks = new Set();
var hoverNode = null;

function tooltipMoveHandler(e) {
  var tt = document.getElementById("tooltip");
  tt.style.left = (e.clientX + 14) + "px";
  tt.style.top = (e.clientY - 10) + "px";
}

function onNodeHover(node, graph) {
  var tooltip = document.getElementById("tooltip");

  if (node) {
    hoverNode = node;
    highlightNodes.clear();
    highlightLinks.clear();
    highlightNodes.add(node);

    var data = graph.graphData();
    data.links.forEach(function(l) {
      var s = typeof l.source === "object" ? l.source : { id: l.source };
      var t = typeof l.target === "object" ? l.target : { id: l.target };
      if (s.id === node.id || t.id === node.id) {
        highlightLinks.add(l);
        highlightNodes.add(s.id === node.id ? t : s);
      }
    });

    tooltip.querySelector(".tt-title").textContent = node.title;
    tooltip.querySelector(".tt-type").textContent =
      node.type + " \u00B7 " + node.domain;
    tooltip.classList.add("visible");
    document.addEventListener("mousemove", tooltipMoveHandler);
  } else {
    hoverNode = null;
    highlightNodes.clear();
    highlightLinks.clear();
    tooltip.classList.remove("visible");
    document.removeEventListener("mousemove", tooltipMoveHandler);
  }

  refreshHighlight(graph);
}

function highlightFromDrawer(node, graph) {
  highlightNodes.clear();
  highlightLinks.clear();
  highlightNodes.add(node);

  var data = graph.graphData();
  data.links.forEach(function(l) {
    var s = typeof l.source === "object" ? l.source : null;
    var t = typeof l.target === "object" ? l.target : null;
    if (s && t && (s.id === node.id || t.id === node.id)) {
      highlightLinks.add(l);
      highlightNodes.add(s.id === node.id ? t : s);
    }
  });

  refreshHighlight(graph);
}

function clearHighlight(graph) {
  highlightNodes.clear();
  highlightLinks.clear();
  hoverNode = null;
  graph.nodeColor(function(n) { return getNodeColor(n, null, highlightNodes); })
       .linkWidth(1.2)
       .linkDirectionalParticles(0);
  if (!showCrossPackAlways && _updateVisibility) _updateVisibility();
}

function refreshHighlight(graph) {
  graph.nodeColor(function(n) { return getNodeColor(n, hoverNode, highlightNodes); })
       .linkWidth(function(l) { return highlightLinks.has(l) ? 2.5 : 0.8; })
       .linkDirectionalParticles(function(l) {
         return highlightLinks.has(l) ? 3 : 0;
       });
  if (!showCrossPackAlways && _updateVisibility) _updateVisibility();
}
