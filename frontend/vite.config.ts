import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import tailwindcss from '@tailwindcss/vite'

// https://vite.dev/config/
export default defineConfig({
  plugins: [react(), tailwindcss()],
  server: {
    host: true,
    allowedHosts: [
      '1817-108-91-116-214.ngrok-free.app',
      '1645-108-91-116-214.ngrok-free.app'
    ],
  },
})
