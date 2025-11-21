import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// Настройки
export default defineConfig({
  plugins: [react()],
  appType: 'spa',
  server: {
    allowedHosts: ['maxos_frontend'],
    proxy: {
      '/api': {
        target: 'http://localhost:8005',
        changeOrigin: true,
        rewrite: path => path.replace(/^\/api/, ''),
      },
    },
  },
})

