import { defineConfig } from 'vite';

export default defineConfig({
  base: './', // relative paths so it can be served from any directory or subpath
  server: {
    port: 5173,
    open: false
  }
});
