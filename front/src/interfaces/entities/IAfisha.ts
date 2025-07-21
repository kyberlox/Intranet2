import type { IBaseIndirectData, IBaseEntity } from "./IBase"

export interface IAfishaItemIndirectData extends IBaseIndirectData {
    PROPERTY_375?: string[],
    PROPERTY_438?: string[],
    PROPERTY_372?: string[],
    PROPERTY_373?: string[],
    PROPERTY_374?:
    {
        TYPE?: string,
        TEXT?: string
    }[],
    PROPERTY_376?: string[],
    PROPERTY_5004?: string[]
}

export interface IAfishaItem extends IBaseEntity {
    indirect_data?: IAfishaItemIndirectData
}
