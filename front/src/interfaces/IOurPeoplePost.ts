export interface OurPeoplePost {
    id: number,
    image: string,
    title: string,
    reactions: {
        views: number,
        likes: { count: number, likedByMe: number },
    },
    href: string,
}