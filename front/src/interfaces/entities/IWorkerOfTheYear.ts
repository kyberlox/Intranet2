import type { IBaseIndirectData, IBaseEntity } from "./IBase"

export interface IWorkerOfTheYearData extends IBaseIndirectData {
    uuid: number,
    year: string,
    position: string,
    department: string,
    photo_file_url: string,
    award: string,
    location: string
}

export interface IWorkerOfTheYear extends IBaseEntity {
    indirect_data?: IWorkerOfTheYearData
}