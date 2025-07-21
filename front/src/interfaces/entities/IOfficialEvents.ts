import type { IBaseIndirectData, IBaseEntity } from "./IBase"

interface IOfficialEventsData extends IBaseIndirectData {
    PROPERTY_665?: string[],
    PROPERTY_403?: string[],
    PROPERTY_398?: string[],
    PROPERTY_399?: string[],
    PROPERTY_400?: string[],
    PROPERTY_401?: string[],
    PROPERTY_402?: string[],
    date_creation?: string
}

export interface IOfficialEvents extends IBaseEntity {
    indirect_data?: IOfficialEventsData
}