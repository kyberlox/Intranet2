import type { IBaseIndirectData, IBaseEntity } from "./IBase"

interface ICorpLifeIndirectData extends IBaseIndirectData {
    PROPERTY_666?: string[],
    PROPERTY_405?: string[],
    PROPERTY_406?: string[],
    PROPERTY_407?: string[],
    PROPERTY_409?: string[],
    PROPERTY_408?: string[],
}

export interface ICorpLife extends IBaseEntity {
    indirect_data?: ICorpLifeIndirectData
}