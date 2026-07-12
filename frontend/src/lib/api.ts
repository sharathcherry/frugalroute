// API base URL helper.
// - Local dev: VITE_API_URL is empty → calls are same-origin ("/api/…") and
//   Vite's dev proxy forwards them to the backend.
// - Production (frontend on its own Railway domain): set VITE_API_URL to the
//   backend service's public URL, e.g. https://frugalroute-api.up.railway.app
const BASE = (import.meta.env.VITE_API_URL ?? "").replace(/\/$/, "");

export function api(path: string): string {
  return `${BASE}${path}`;
}
