interface ImportMetaEnv {
  readonly VITE_SERVER_URL: string
  readonly VITE_ALGOLIA_APP_ID: string
  readonly VITE_POSTHOG_API_KEY: string
}

interface ImportMeta {
  readonly env: ImportMetaEnv
}
