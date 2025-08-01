import type { IBaseIndirectData, IBaseEntity } from "./IBase"

export interface ICareIndirectData extends IBaseIndirectData {
    organizer: string,
    phone_number: string,
    theme: string
}

export interface ICareSlide extends IBaseEntity {
    indirect_data?: ICareIndirectData
}