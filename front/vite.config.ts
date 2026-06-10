import { fileURLToPath, URL } from 'node:url';

import { defineConfig } from 'vitest/config';
import vue from '@vitejs/plugin-vue';
import vueDevTools from 'vite-plugin-vue-devtools';
import svgLoader from 'vite-svg-loader';

// https://vite.dev/config/
export default defineConfig({
  base: '/',
  plugins: [
    vue(),
    vueDevTools(),
    svgLoader({
      svgoConfig: {
        multipass: true
      }
    })
  ],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url))
    },
  },
  test: {
    environment: 'jsdom',
    coverage: {
      exclude: [
        '**/*.svg',
        '**/assets/icons/**',
        '**/*.d.ts',
        '**/index.ts',
        '**/*.config.{js,ts}',
        'assets/**',
        'public/**',
        'dist/**',
      ]
    }
  },
  css: {
    preprocessorOptions: {
      scss: {
        additionalData: `@use "@/assets/styles/mixins" as *;`,
        api: 'modern-compiler',
      }
    }
  },
  server: {
    host: "0.0.0.0",
    port: 5173,
    allowedHosts: true
  },
  preview: {
    host: "0.0.0.0",
    port: 5173,
    allowedHosts: true
  },
})