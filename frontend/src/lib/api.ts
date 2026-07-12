// API base URL helper.
// - Local dev: VITE_API_URL is empty → calls are same-origin ("/api/…") and
//   Vite's dev proxy forwards them to the backend.
// - Production: set VITE_API_URL to the backend's public URL.
//   e.g. https://frugalroute-production.up.railway.app
//   NOTE: must include https:// — if omitted we add it automatically.
function buildBase(): string {
  let raw = (import.meta.env.VITE_API_URL ?? "").replace(/\/$/, "");
  if (raw && !raw.startsWith("http://") && !raw.startsWith("https://")) {
    raw = "https://" + raw;
  }
  return raw;
}

const BASE = buildBase();

export function api(path: string): string {
  return `${BASE}${path}`;
}
