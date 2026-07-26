/* ── OKF Pack Explorer — Constants & Color Maps ─────────────
   Type colors, pack colors, shared lookup helpers.
   <200 LoC                                                    */

var TYPE_COLORS = {
  "KPI":                  "#e74c3c",
  "Metric":               "#e67e22",
  "Metric Collection":    "#d35400",
  "Process":              "#2ecc71",
  "Framework":            "#3498db",
  "Doctrine":             "#9b59b6",
  "Operating Model":      "#1abc9c",
  "Role":                 "#f39c12",
  "Program":              "#e91e63",
  "Priority":             "#ff5722",
  "Strategy":             "#ff9800",
  "Stage":                "#00bcd4",
  "Methodology":          "#009688",
  "Evidence Map":         "#8bc34a",
  "Evidence Source":      "#4caf50",
  "Risk Signal":          "#f44336",
  "Risk":                 "#ef5350",
  "Pipeline Object":      "#ab47bc",
  "Planning Artifact":    "#5c6bc0",
  "Governance":           "#26a69a",
  "Outcome Framework":    "#42a5f5",
  "Measurement Concept":  "#66bb6a",
  "Organization":         "#78909c",
  "GTM Motion":           "#ec407a",
  "Taxonomy":             "#78909c"
};

var DEFAULT_COLOR = "#78909c";

var PACK_COLORS = {
  "kp-csu":  "#4da6ff",
  "kp-mcem": "#fd8ea1"
};

function getTypeColor(type) {
  return TYPE_COLORS[type] || DEFAULT_COLOR;
}

function escapeHtml(str) {
  if (!str) return "";
  var d = document.createElement("div");
  d.textContent = str;
  return d.innerHTML;
}

// Cross-pack toggle state (shared across modules)
var showCrossPackAlways = false;
var _updateVisibility = null;
