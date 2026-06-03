import type { IBaseIndirectData, IBaseEntity } from "./IBase"

export interface IBlogData extends IBaseIndirectData {
    author_uuid: number,
    company: number,
    TITLE?: string,
    photo_file_url: string,
    link: string,
    youtube_link: string,
    author: string
    users: {
        id: number,
        fio: string,
        TITLE: string,
        position: string,
        photo_file_url: string
    }
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
    authorTitle?: string
    isCompany?: boolean
}

export interface IBlog extends IBaseEntity {
    indirect_data?: IBlogData
}

export interface IBlogArticle extends IBaseEntity {
    indirect_data?: IBlogArticleData
}

export interface ISortItems {
    user_fio: string,
    user_id: number,
    user_photo: string,
    sort: number
}