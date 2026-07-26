/* ── OKF Pack Explorer — Drawer Logic ───────────────────────
   Opens/closes the detail drawer, populates content with
   markdown-rendered sections and clickable relationships.
   Depends on: constants.js, markdown.js
   <200 LoC                                                    */

var selectedNode = null;

function openDrawer(node, graph) {
  selectedNode = node;
  document.getElementById("drawer-title").textContent = node.title;
  document.getElementById("drawer-meta").innerHTML =
    '<span class="meta-badge meta-type">' + escapeHtml(node.type) + '</span>' +
    '<span class="meta-badge meta-domain">' + escapeHtml(node.domain) + '</span>' +
    '<span class="meta-badge meta-pack">' + escapeHtml(node.pack) + '</span>';

  // Replace body to clear old listeners
  var body = document.getElementById("drawer-body");
  var newBody = body.cloneNode(false);
  body.parentNode.replaceChild(newBody, body);
  body = newBody;
  body.id = "drawer-body";

  var html = '<div class="drawer-section">' +
    '<div class="drawer-section-title">Qualified ID</div>' +
    '<div id="drawer-id">' + escapeHtml(node.id) + '</div></div>';

  if (node.description) {
    html += '<div class="drawer-section">' +
      '<div class="drawer-section-title">Description</div>' +
      '<div id="drawer-description">' + renderMarkdown(node.description) + '</div></div>';
  }

  if (node.aliases && node.aliases.length > 0) {
    html += '<div class="drawer-section">' +
      '<div class="drawer-section-title">Aliases (' + node.aliases.length + ')</div><div>';
    node.aliases.forEach(function(a) {
      html += '<span class="alias-tag">' + escapeHtml(a) + '</span>';
    });
    html += '</div></div>';
  }

  // ── Relationships ──────────────────────────────────────
  var data = graph.graphData();
  var outRels = data.links.filter(function(l) {
    return (typeof l.source === "object" ? l.source.id : l.source) === node.id;
  });
  var inRels = data.links.filter(function(l) {
    return (typeof l.target === "object" ? l.target.id : l.target) === node.id;
  });

  if (outRels.length + inRels.length > 0) {
    html += '<div class="drawer-section">' +
      '<div class="drawer-section-title">Relationships (' +
      (outRels.length + inRels.length) + ')</div>' +
      '<div id="rel-list"></div></div>';
  }

  // ── Content sections (markdown-rendered) ───────────────
  if (node.sections && node.sections.length > 0) {
    html += '<div class="drawer-section">' +
      '<div class="drawer-section-title">Content (' + node.sections.length + ')</div>';
    node.sections.forEach(function(s) {
      html += '<div class="section-card"><div class="section-heading">' +
        escapeHtml(s.heading || "\u2014") +
        '</div><div class="section-content">' +
        renderMarkdown(s.content) + '</div></div>';
    });
    html += '</div>';
  }

  body.innerHTML = html;

  // ── Attach relationship click handlers ─────────────────
  var relList = document.getElementById("rel-list");
  if (relList) {
    outRels.forEach(function(l) {
      var t = typeof l.target === "object" ? l.target : { id: l.target, title: l.target };
      appendRelItem(relList, "\u2192", l.predicate, t, graph);
    });
    inRels.forEach(function(l) {
      var s = typeof l.source === "object" ? l.source : { id: l.source, title: l.source };
      appendRelItem(relList, "\u2190", l.predicate, s, graph);
    });
  }

  document.getElementById("drawer").classList.add("open");
  document.getElementById("drawer-overlay").classList.add("open");
}

function appendRelItem(container, arrow, predicate, targetNode, graph) {
  var item = document.createElement("div");
  item.className = "rel-item";
  item.innerHTML =
    '<span class="rel-arrow">' + arrow + '</span>' +
    '<span class="rel-predicate">' + escapeHtml(predicate) + '</span>' +
    '<span class="rel-target">' + escapeHtml(targetNode.title || targetNode.id) + '</span>';
  item.addEventListener("click", function() {
    navigateToNode(targetNode.id, graph);
  });
  container.appendChild(item);
}

function navigateToNode(nodeId, graph) {
  var data = graph.graphData();
  var node = data.nodes.find(function(n) { return n.id === nodeId; });
  if (node) {
    openDrawer(node, graph);
    var dist = 200;
    graph.cameraPosition(
      { x: node.x + dist, y: node.y + dist * 0.5, z: node.z + dist },
      { x: node.x, y: node.y, z: node.z }, 1200
    );
  }
}

function closeDrawer() {
  document.getElementById("drawer").classList.remove("open");
  document.getElementById("drawer-overlay").classList.remove("open");
  selectedNode = null;
}
