import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// Настройки
export default defineConfig({
  plugins: [react()],
  appType: 'spa',
  server: {
    proxy: {
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true,
        rewrite: path => path.replace(/^\/api/, ''),
      },
    },
  },
})
