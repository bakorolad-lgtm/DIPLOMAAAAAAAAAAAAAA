import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// Настройки
export default defineConfig({
  plugins: [react()],
  server: {
    proxy: {
      '/auth': 'http://localhost:8000',
      '/courses': 'http://localhost:8000',
      '/quiz': 'http://localhost:8000',
    },
  },
})
