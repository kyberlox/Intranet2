import type { IBaseIndirectData, IBaseEntity } from "./IBase"

export interface IOpenVacancyData extends IBaseIndirectData {
    link: string
}

export interface IOpenVacancy extends IBaseEntity {
    indirect_data?: IOpenVacancyData
}