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

export interface IActivityStatistics{
    id: string,
}

export interface IPointsAdmin {
    admin_id: number
    admin_last_name: string
    admin_name: string
    admin_second_name: string
}
export interface IPointsModer {
    moder_id: number
    moder_last_name: string
    moder_name: string
    moder_second_name: string
}

export interface ICurator {
    activity_id?: number,
    activity_name?: string,
    moder_id?: string
    curator_id?: number 
    curator_name?: string 
    curator_last_name?: string
    curator_second_name?: string 
}

export interface IActivityToConfirm {
    coast: number
    date_time: string
    description: string
    id: number
    name: number
    need_valid: boolean
    uuid_from: number
    uuid_to: number
}