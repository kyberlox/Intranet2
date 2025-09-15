export interface IActivitiesList {
    id: number,
    need_valid: boolean,
    name: string,
    coast: number
}

export interface IActivityToSend {
    activities: { value?: number, name: string, id: number }[],
    likes_left: number
}