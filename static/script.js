"use strict";

const LABELS = {
  list_of_plugins: "List of plugins",
  useragent: "User-Agent",
  list_of_fonts: "Detected fonts",
  canvas: "Canvas hash",
  language: "Language",
  resolution: "Screen resolution",
  color_depth: "Colour depth",
  accept_headers: "HTTP Accept",
  timezone: "Time zone",
  webgl_renderer: "WebGL renderer",
  platform: "Platform",
  webgl_vendor: "WebGL vendor",
  content_encoding: "Accept-Encoding",
  accept_lang: "Accept-Language",
  adblock: "Ad blocker detected",
  donottrack: "Do Not Track",
  local_storage: "Local storage",
  session_storage: "Session storage",
  cookie: "Cookies enabled",
};

function displayValue(value) {
  if (Array.isArray(value)) return value.length ? value.join(", ") : "—";
  if (value === "" || value === null || value === undefined) return "—";
  return String(value);
}

function renderTable(fingerprint, analysis) {
  const body = document.querySelector("#results-table tbody");
  body.replaceChildren();

  for (const key of analysis.order) {
    const row = document.createElement("tr");
    const cells = [
      LABELS[key] || key,
      displayValue(fingerprint[key]),
      analysis.entropy[key].toFixed(6),
      analysis.information_gain[key].toFixed(6),
    ];

    for (const value of cells) {
      const cell = document.createElement("td");
      cell.textContent = value;
      row.appendChild(cell);
    }
    body.appendChild(row);
  }

  document.getElementById("sample-count").textContent = analysis.sample_count;
  document.getElementById("results").hidden = false;
}

async function collectAndStore() {
  const button = document.getElementById("collect-button");
  const status = document.getElementById("status");
  button.disabled = true;
  status.textContent = "Collecting local browser attributes…";

  try {
    const headersResponse = await fetch("/api/headers", { cache: "no-store" });
    if (!headersResponse.ok) throw new Error("Could not read request headers.");
    const headers = await headersResponse.json();
    const fingerprint = collectFingerprint(headers);

    const response = await fetch("/api/fingerprints", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(fingerprint),
    });
    if (!response.ok) throw new Error("Could not store the fingerprint.");

    const result = await response.json();
    renderTable(fingerprint, result);
    status.textContent = `Sample ${result.id} stored in the local database.`;
  } catch (error) {
    status.textContent = error instanceof Error ? error.message : "Unexpected error.";
  } finally {
    button.disabled = false;
  }
}

document.getElementById("collect-button").addEventListener("click", collectAndStore);
