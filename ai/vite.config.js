import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// Deploy to GitHub Pages at seven-fortunas.github.io/dashboards/ai/
export default defineConfig({
  plugins: [react()],
  base: '/dashboards/ai/',
  build: {
    outDir: 'dist'
  }
})
