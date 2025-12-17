/// <reference types="vite/client" />
/// <reference types="vite-svg-loader" />

interface ImportMetaEnv {
    readonly VITE_API_URL: string;
    readonly VITE_TEST_MODE: string;
}

interface ImportMeta {
    readonly env: ImportMetaEnv;
}
declare const VITE_API_URL: string;
declare const VITE_TEST_MODE: string;

