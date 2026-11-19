import vue from '@vitejs/plugin-vue'
import { defineConfig } from 'vite'

// https://vite.dev/config/
export default defineConfig({
  plugins: [vue()],
  server: {
    // El backend (FastAPI) corre en el puerto 8000
    proxy: {
      '/api': 'http://localhost:8000',
    },
  },
  build: {
    // MapLibre ocupa ~1 MB y solo se descarga al entrar a /mapa (ruta con carga diferida)
    chunkSizeWarningLimit: 1200,
  },
})
