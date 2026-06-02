import { fileURLToPath, URL } from 'node:url'
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

export default defineConfig({
  plugins: [vue()],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url))
    }
  },
  // LE BLOC À AJOUTER POUR SIMULER NGINX EN LOCAL :
  server: {
    proxy: {
      '/api': {
        target: 'http://127.0.0.1:5001', // Le port de ton backend Flask local
        changeOrigin: true
      }
    }
  }
})