import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  base: '/',
  build: {
    outDir: 'dist',
    assetsDir: 'assets',
    rollupOptions: {
      output: {
        manualChunks: {
          vendor: ['react', 'react-dom'],
          firebase: ['firebase/app', 'firebase/auth', 'firebase/firestore', 'firebase/storage'],
          maps: ['@react-google-maps/api'],
          utils: ['axios', 'i18next', 'react-i18next']
        }
      }
    }
  },
  server: {
    port: 5173,
    strictPort: true,
    host: true
  },
  resolve: {
    alias: {
      '@': '/src'
    }
  }
})