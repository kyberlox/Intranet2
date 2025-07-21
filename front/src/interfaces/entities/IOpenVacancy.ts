import type { IBaseIndirectData, IBaseEntity } from "./IBase"

export interface IOpenVacancyData extends IBaseIndirectData {
    PROPERTY_5094: string[]
}

export interface IOpenVacancy extends IBaseEntity {
    indirect_data?: IOpenVacancyData
}