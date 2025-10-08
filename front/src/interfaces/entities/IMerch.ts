import type { IBaseIndirectData, IBaseEntity, IBXFileType } from "./IBase"

export interface IMerchData extends IBaseIndirectData {
    images: IBXFileType[]
    price: number
}
export interface IMerchItemData extends IBaseIndirectData {
    sizes_left:{
    s?:number
    m?:number
    l?:number
    xl?:number
    xxl?:number
    no_size?:number
}
    images: IBXFileType[]
    category?: string
    price?: number
}


export interface IMerch extends IBaseEntity {
    indirect_data?: IMerchData
}

export interface IMerchItem extends IBaseEntity{
    indirect_data?: IMerchItemData
}