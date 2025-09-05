import type { IBaseIndirectData, IBaseEntity, IBXFileType } from "./IBase"

export interface IPostCardData extends IBaseIndirectData {
    preview_file_url: string
}

export interface IPostCard extends IBaseEntity {
    indirect_data?: IPostCardData
    images: IBXFileType[]
}
