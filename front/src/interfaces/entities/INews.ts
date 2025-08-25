import type { IBaseIndirectData, IBaseEntity } from "./IBase"

export interface INewsIndirectData extends IBaseIndirectData {
    author?: string[]
}

export interface INews extends IBaseEntity {
    indirect_data?: INewsIndirectData
}