import { fileURLToPath, URL } from 'node:url';

import { defineConfig } from 'vite';
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

  css: {
    preprocessorOptions: {
      scss: {
        additionalData: `
        @use "@/assets/styles/mixins/_mixins.scss" as *;
        @use "@/assets/styles/main.scss";`,
        api: 'modern-compiler',
      }
    }
  },

  server: {
    host: "0.0.0.0",
    port: 5173,
    allowedHosts: ['http://intranet1-dmz.imp.int/', 'http://testrcube1-a66.imp.int/']
  },
  preview: {
    host: "0.0.0.0",
    port: 5173,
  },

})
