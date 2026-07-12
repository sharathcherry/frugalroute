// vite.spa.config.ts — Plain client-side SPA build for FastAPI to serve.
// This produces a standard dist/ folder with index.html + assets/.
// Usage: npx vite build --config vite.spa.config.ts
import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
import tailwindcss from "@tailwindcss/vite";
import { TanStackRouterVite } from "@tanstack/router-plugin/vite";
import path from "path";

export default defineConfig({
  plugins: [
    TanStackRouterVite({ routesDirectory: "./src/routes", generatedRouteTree: "./src/routeTree.gen.ts" }),
    react(),
    tailwindcss(),
  ],
  resolve: {
    alias: {
      "@": path.resolve(__dirname, "./src"),
    },
  },
  build: {
    outDir: "dist",
    emptyOutDir: true,
  },
  server: {
    proxy: {
      "/api": "http://localhost:8000",
    },
  },
});
