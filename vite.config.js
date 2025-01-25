import { defineConfig } from 'vite';
import { resolve } from 'path';

export default defineConfig({
  server: {
    headers: {
      'Cross-Origin-Embedder-Policy': 'require-corp',
      'Cross-Origin-Opener-Policy': 'same-origin',
      'Cross-Origin-Resource-Policy': 'cross-origin'
    }
  },
  optimizeDeps: {
    exclude: ['onnxruntime-web']
  },
  build: {
    target: 'esnext',
    rollupOptions: {
      external: ['onnxruntime-web']
    }
  },
  resolve: {
    alias: {
      'onnxruntime-web': resolve(__dirname, 'node_modules/onnxruntime-web/dist/ort.bundle.min.mjs')
    }
  },
  assetsInclude: ['**/*.onnx', '**/*.wasm'],
  publicDir: 'public'
});
