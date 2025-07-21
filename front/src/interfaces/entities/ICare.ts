import type { IBaseIndirectData, IBaseEntity } from "./IBase"

export interface ICareIndirectData extends IBaseIndirectData {
    PROPERTY_342?: string[],
    PROPERTY_343?: string[],
    PROPERTY_344?: string[],
    PROPERTY_435?: string[],
    PROPERTY_347?: string[],
    PROPERTY_348?:
    {
        TYPE?: string,
        TEXT?: string
    }[],
    PROPERTY_349?: string[],
}

export interface ICareSlide extends IBaseEntity {
    indirect_data?: ICareIndirectData
}