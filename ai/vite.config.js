import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// Deploy to GitHub Pages at seven-fortunas.github.io/dashboards/
export default defineConfig({
  plugins: [react()],
  base: '/',
  build: {
    outDir: 'dist'
  }
})
