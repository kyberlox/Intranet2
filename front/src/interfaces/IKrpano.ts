interface EmbedpanoOptions {
    swf: string;
    xml: string;
    target: string;
    html5: string;
    mobilescale: number;
    passQueryParameters: boolean;
    [key: string]: unknown;
}

declare global {
    interface Window {
        embedpano: (options: EmbedpanoOptions) => void;
        removepano: (id: string) => void;
    }
}