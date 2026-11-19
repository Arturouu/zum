/// <reference types="vite/client" />

interface ImportMetaEnv {
  /** "false" para usar el backend real en vez del mock de services/route.ts */
  readonly VITE_USAR_MOCK?: string
}

interface ImportMeta {
  readonly env: ImportMetaEnv
}
