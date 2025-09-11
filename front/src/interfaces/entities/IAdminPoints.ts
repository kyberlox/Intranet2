export interface IActivitiesList {
    id: number,
    need_valid: boolean,
    name: string,
    coast: number
}

export interface IActivityToSend {
    activities: { value: number, name: string }[],
    likes_left: number

}