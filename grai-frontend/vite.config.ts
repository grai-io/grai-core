import react from "@vitejs/plugin-react"
import { defineConfig } from "vite"
import EnvironmentPlugin from "vite-plugin-environment"
import viteTsconfigPaths from "vite-tsconfig-paths"

const hash = Math.floor(Math.random() * 90000) + 10000

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [
    react(),
    viteTsconfigPaths(),
    EnvironmentPlugin({
      REACT_APP_SERVER_URL: "http://localhost:8000",
      REACT_APP_POSTHOG_API_KEY: null,
      REACT_APP_ALGOLIA_APP_ID: null,
    }),
  ],
  build: {
    outDir: "build",
    rollupOptions: {
      output: {
        entryFileNames: `[name]_` + hash + `.js`,
        chunkFileNames: `[name]_` + hash + `.js`,
        assetFileNames: `[name]_` + hash + `.[ext]`,
      },
    },
  },
  server: {
    port: 3000,
    open: true,
  },
})
