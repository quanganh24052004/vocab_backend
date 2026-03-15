import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  base: '/', // BẮT BUỘC phải là dấu gạch chéo này để chạy subdomain
})