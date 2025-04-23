export interface IfeedPost {
    title: string;
    date: string;
    likes: {
        count: number;
        mine: boolean;
    };
    text: string;
    documents: {
        name: string;
        link: string;
    }[];
    images: string[];
    videos: string[];
    tags?: Array<string>;
}   