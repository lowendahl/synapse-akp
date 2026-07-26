/* ── OKF Pack Explorer — Markdown Renderer ──────────────────
   Lightweight markdown-to-HTML for the detail drawer.
   Handles: tables, bold, italic, code, links, lists.
   <200 LoC                                                    */

function renderMarkdown(text) {
  if (!text) return "";
  var lines = text.split("\n");
  var html = [];
  var inTable = false;
  var inList = false;
  var listType = null;

  for (var i = 0; i < lines.length; i++) {
    var line = lines[i];

    // ── Table rows ─────────────────────────────────────────
    if (/^\s*\|/.test(line) && line.trim().endsWith("|")) {
      // Skip separator rows like |---|---|
      if (/^\s*\|[\s\-:|]+\|\s*$/.test(line)) continue;
      if (!inTable) { inTable = true; html.push("<table>"); }
      var cells = line.split("|").filter(function(c, idx, arr) {
        return idx > 0 && idx < arr.length - 1;
      });
      var isHeader = i + 1 < lines.length && /^\s*\|[\s\-:|]+\|\s*$/.test(lines[i + 1]);
      var tag = isHeader ? "th" : "td";
      html.push("<tr>");
      cells.forEach(function(c) {
        html.push("<" + tag + ">" + renderInline(c.trim()) + "</" + tag + ">");
      });
      html.push("</tr>");
      continue;
    }
    if (inTable) { inTable = false; html.push("</table>"); }

    // ── List items ─────────────────────────────────────────
    var ulMatch = line.match(/^\s*[-*]\s+(.+)/);
    var olMatch = line.match(/^\s*\d+\.\s+(.+)/);
    if (ulMatch) {
      if (!inList || listType !== "ul") {
        if (inList) html.push("</" + listType + ">");
        html.push("<ul>"); inList = true; listType = "ul";
      }
      html.push("<li>" + renderInline(ulMatch[1]) + "</li>");
      continue;
    }
    if (olMatch) {
      if (!inList || listType !== "ol") {
        if (inList) html.push("</" + listType + ">");
        html.push("<ol>"); inList = true; listType = "ol";
      }
      html.push("<li>" + renderInline(olMatch[1]) + "</li>");
      continue;
    }
    if (inList) { inList = false; html.push("</" + listType + ">"); listType = null; }

    // ── Blank lines ────────────────────────────────────────
    if (line.trim() === "") continue;

    // ── Normal paragraph ───────────────────────────────────
    html.push("<p>" + renderInline(line) + "</p>");
  }

  if (inTable) html.push("</table>");
  if (inList) html.push("</" + listType + ">");
  return html.join("");
}

function renderInline(text) {
  if (!text) return "";
  // Escape HTML entities first
  text = text.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
  // Bold: **text**
  text = text.replace(/\*\*(.+?)\*\*/g, "<strong>$1</strong>");
  // Italic: *text* (but not inside bold markers)
  text = text.replace(/(?<!\*)\*(?!\*)(.+?)(?<!\*)\*(?!\*)/g, "<em>$1</em>");
  // Inline code: `text`
  text = text.replace(/`([^`]+)`/g, "<code>$1</code>");
  // Links: [text](url)
  text = text.replace(/\[([^\]]+)\]\(([^)]+)\)/g, '<a href="$2" title="$2">$1</a>');
  return text;
}
