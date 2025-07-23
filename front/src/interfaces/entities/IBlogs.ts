import type { IBaseIndirectData, IBaseEntity } from "./IBase"

export interface IBlogData extends IBaseIndirectData {
    author_uuid: number,
    company: number,
    TITLE?: string,
    photo_file_url: string,
    link: string,
}

export interface IBlogArticleData extends IBaseIndirectData {
    youtube_link?: string
}

export interface IBlogAuthors {
    authorId?: number,
    title?: string,
    authorAvatar?: string,
    link?: string,
    telegramQr?: string
}

export interface IBlog extends IBaseEntity {
    indirect_data?: IBlogData
}

export interface IBlogArticle extends IBaseEntity {
    indirect_data?: IBlogArticleData
}