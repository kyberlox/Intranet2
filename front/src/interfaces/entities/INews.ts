import type { IBaseIndirectData, IBaseEntity } from "./IBase"

export interface IActualNewsIndirectData extends IBaseIndirectData {
    author?: string[]
}

interface ICorpNewsData extends IBaseIndirectData {
    PROPERTY_1127?: string[],
    PROPERTY_1128?: string[]
}

export interface IActualNews extends IBaseEntity {
    indirect_data?: IActualNewsIndirectData
}

export interface ICorpEventsItem extends IBaseEntity {
    indirect_data?: IActualNewsIndirectData
}

export interface ICorpNews extends IBaseEntity {
    indirect_data?: ICorpNewsData
}