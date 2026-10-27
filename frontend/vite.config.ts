import { defineConfig } from 'vite';

export default defineConfig({
  root: '..',
  server: {
    port: 5173,
    host: '0.0.0.0'
  },
  build: {
    outDir: 'frontend/dist',
    rollupOptions: {
      input: ['../index.html', '../restaurant.html']
    }
  }
});
