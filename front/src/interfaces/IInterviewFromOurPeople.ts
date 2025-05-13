export interface IInterviewFromOurPeople {
    id: number,
    title: string,
    fullImage?: string,
    image?: string,
    reactions: {
        views: number,
        likes: { count: number, mine: boolean },
    },
    innerText?: string,
}