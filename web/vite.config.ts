import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

// The marketing site talks to the FastAPI backend from app/api/main.py.
// In dev everything under /api-proxy is forwarded so the browser never hits CORS.
export default defineConfig({
  plugins: [react()],
  server: {
    port: 5174,
    host: "0.0.0.0",
    proxy: {
      "/api-proxy": {
        target: process.env.VITE_API_TARGET || "http://localhost:8000",
        changeOrigin: true,
        ws: true,
        rewrite: (p) => p.replace(/^\/api-proxy/, ""),
      },
    },
  },
  build: {
    outDir: "dist",
    sourcemap: false,
  },
});
