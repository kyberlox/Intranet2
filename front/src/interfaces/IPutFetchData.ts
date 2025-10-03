export interface IPointsForm {
    uuid_from: number,
    uuid_to: number,
    activities_id: number,
    description: string
} 

export interface INewActivityData{
    coast?: number | null
    name?:string
    need_valid?:boolean
    id?: number
    activity_id?: string
    uuid?: string | number 
}