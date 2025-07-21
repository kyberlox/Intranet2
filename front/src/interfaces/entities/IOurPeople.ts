import type { IBaseIndirectData, IBaseEntity } from "./IBase"

interface IOurPeopleData extends IBaseIndirectData {
    user_uuids?: string[],
}

export interface IOurPeople extends IBaseEntity {
    indirect_data?: IOurPeopleData
}