import type { IBaseIndirectData, IBaseEntity } from "./IBase"

interface IPartnerBonusData extends IBaseIndirectData {
    PROPERTY_341?: string[],
    PROPERTY_337?: string[],
    PROPERTY_338?: string[],
    PROPERTY_340?: string[],
    PROPERTY_439?: string[],
}

export interface IPartnerBonus extends IBaseEntity {
    indirect_data?: IPartnerBonusData
}