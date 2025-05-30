export interface SubpageItem {
    name: string;
    href?: {
        name: string;
        params: {
            id: number;
        };
    };
}

export interface IBook {
    name: string;
    id?: string | number;
    href?: {
        name: string;
        params: {
            id: number;
        };
    };
    subpages: SubpageItem[];
}