export interface IPointsForm {
    uuid_from: number
    uuid_to: number
    activities_id: number
    description: string
}

export interface INewActivityData {
    coast?: number | null
    name?: string
    need_valid?: boolean
    id?: number
    activity_id?: string
    uuid?: string | number
    is_auto?: boolean
    description?: string
}

export interface IPurchaseMerchData {
    art_id: number
    l?: number
    m?: number
    s?: number
    xl?: number
    xxl?: number
    no_size?: number
    user_points?: number
}
