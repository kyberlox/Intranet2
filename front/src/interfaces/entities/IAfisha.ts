import type { IBaseIndirectData, IBaseEntity } from "./IBase"

export interface IAfishaItemIndirectData extends IBaseIndirectData {
    data_from: string,
    date_to: string,
}

export interface IAfishaItem extends IBaseEntity {
    indirect_data?: IAfishaItemIndirectData
}
