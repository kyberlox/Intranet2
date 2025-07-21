import type { IBaseIndirectData, IBaseEntity } from "./IBase"

interface IVideoReportsData extends IBaseIndirectData {
    PROPERTY_1066?: string[]
    PROPERTY_1116?: string[]
    PROPERTY_284?: string[]
    PROPERTY_285?: string[]
    PROPERTY_289?: string[]
    PROPERTY_290?: string[]
    PROPERTY_291?:
    {
        TYPE?: string,
        TEXT?: string
    }[],
    PROPERTY_292?: string[],
    PROPERTY_293?: string[],
    PROPERTY_294?: string[],
    PROPERTY_295?: string[],
    PROPERTY_296?: string[],
    PROPERTY_664?: string[],
    PROPERTY_5044?: string[],
}

export interface IVideoReports extends IBaseEntity {
    indirect_data?: IVideoReportsData
}