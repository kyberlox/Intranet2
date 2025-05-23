export interface Reaction {
    views: number;
    likes: {
        count: number;
        mine: boolean;
    };
}

export interface ImageWithHref {
    id: number;
    image: string;
    title?: string;
    href?: string;
    reactions?: Reaction;
    blockTitle?: string;
}

export interface BlockImage {
    id: number;
    title?: string;
    description?: string;
    image: string;
    href?: string;
    reactions?: Reaction;
    blockTitle?: string;
}

export interface SingleBlock {
    id: number;
    type: 'singleBlock';
    title: string;
    images: (string | ImageWithHref)[];
    href?: string;
    modifiers?: string[];
}

export interface FullRowBlock {
    id: number;
    type: 'fullRowBlock';
    title: string;
    href?: string;
    images: BlockImage[];
}

export interface MixedRowBlockContent {
    id?: number;
    type: 'singleBlock' | 'fullRowBlock';
    title: string;
    images: (string | ImageWithHref | BlockImage)[];
    href?: string;
    modifiers?: string[];
    blockTitle?: string;
}


export interface MixedRowBlock {
    id: number;
    type: 'mixedRowBlock';
    content: MixedRowBlockContent[];
}

export type MainPageBlock = SingleBlock | FullRowBlock | MixedRowBlock;

export type MainPageCards = MainPageBlock[];