export interface IBlog {
    id: number;
    title: string;
    description: string;
    image: string;
    href: string;
    profileHref: string;
}

export interface IBlogArticle {
    title: string;
    description: string;
    image: string;
    href: string;
    articles: Array<{
        id: number;
        title: string;
        date: string;
        description?: string;
        reactions: {
            views: number;
            likes: {
                count: number;
                mine: boolean;
            }
        }
    }>;
}