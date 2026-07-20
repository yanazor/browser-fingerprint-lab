"use strict";

function simpleHash(input) {
  // FNV-1a: compact, deterministic and sufficient for this local demo.
  // It is not intended for cryptographic use.
  let hash = 0x811c9dc5;
  for (let index = 0; index < input.length; index += 1) {
    hash ^= input.charCodeAt(index);
    hash = Math.imul(hash, 0x01000193);
  }
  return (hash >>> 0).toString(16).padStart(8, "0");
}

function getCanvasFingerprint() {
  const canvas = document.createElement("canvas");
  const context = canvas.getContext("2d");
  if (!context) return "unsupported";

  const text = "CANVAS_FINGERPRINT";
  context.textBaseline = "alphabetic";
  context.font = "14px Arial";
  context.fillStyle = "#f60";
  context.fillRect(125, 1, 62, 20);
  context.fillStyle = "#069";
  context.fillText(text, 2, 15);
  context.fillStyle = "rgba(102, 204, 0, 0.7)";
  context.fillText(text, 4, 17);

  return simpleHash(canvas.toDataURL());
}

function getWebGLInfo() {
  const canvas = document.createElement("canvas");
  const context = canvas.getContext("webgl");
  if (!context) return { vendor: "unsupported", renderer: "unsupported" };

  const extension = context.getExtension("WEBGL_debug_renderer_info");
  if (!extension) return { vendor: "masked", renderer: "masked" };

  return {
    vendor: context.getParameter(extension.UNMASKED_VENDOR_WEBGL) || "unknown",
    renderer: context.getParameter(extension.UNMASKED_RENDERER_WEBGL) || "unknown",
  };
}

function getInstalledFonts() {
  const candidates = [
    "Arial", "Calibri", "Cambria", "Consolas", "Courier New", "Georgia",
    "Helvetica", "Menlo", "Monaco", "Segoe UI", "Tahoma",
    "Times New Roman", "Trebuchet MS", "Verdana", "DejaVu Sans",
    "Liberation Sans", "Noto Sans",
  ];

  if (!document.fonts || !document.fonts.check) return [];
  return candidates.filter((font) => document.fonts.check(`12px "${font}"`));
}

function getPlugins() {
  return Array.from(navigator.plugins || [], (plugin) => plugin.name);
}

function storageAvailable(storageName) {
  try {
    return Boolean(window[storageName]);
  } catch (_error) {
    return false;
  }
}

function collectFingerprint(headers) {
  const webgl = getWebGLInfo();
  const timezoneName = Intl.DateTimeFormat().resolvedOptions().timeZone || "unknown";

  return {
    list_of_plugins: getPlugins(),
    useragent: navigator.userAgent,
    list_of_fonts: getInstalledFonts(),
    canvas: getCanvasFingerprint(),
    language: navigator.language || "",
    resolution: `${screen.width}x${screen.height}`,
    color_depth: screen.colorDepth,
    accept_headers: headers.accept || "",
    timezone: timezoneName,
    webgl_renderer: webgl.renderer,
    platform: navigator.platform || "",
    webgl_vendor: webgl.vendor,
    content_encoding: headers.accept_encoding || "",
    accept_lang: headers.accept_language || "",
    adblock: getComputedStyle(document.getElementById("adblock-bait")).display === "none",
    donottrack: navigator.doNotTrack || "",
    local_storage: storageAvailable("localStorage"),
    session_storage: storageAvailable("sessionStorage"),
    cookie: navigator.cookieEnabled,
  };
}
