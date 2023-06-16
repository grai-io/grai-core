import react from "@vitejs/plugin-react";
import { defineConfig } from "vite";
import EnvironmentPlugin from "vite-plugin-environment";
import viteTsconfigPaths from "vite-tsconfig-paths";

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [
    react(),
    viteTsconfigPaths(),
    EnvironmentPlugin({
      VITE_SERVER_URL: "http://localhost:8000",
      VITE_POSTHOG_API_KEY: null,
      VITE_ALGOLIA_APP_ID: null,
    }),
  ],
  build: {
    outDir: "build",
  },
  server: {
    port: 3000,
    open: true,
  },
});
