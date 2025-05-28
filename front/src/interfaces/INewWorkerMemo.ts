export interface INewWorkerMemo {
    id: number,
    title: string,
    image: string,
    textHtml: string,
    pdf?: [
        {
            name?: string,
            link?: string,
        },
    ]
}