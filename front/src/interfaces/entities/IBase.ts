
export interface IReaction {
    views: number,
    likes: {
        count: number,
        likedByMe: boolean
    }
}

export interface IBXFileType {
    article_id?: number,
    b24_id?: string,
    file_url?: string,
    id?: string,
    is_archive?: boolean,
    is_preview?: boolean,
    original_name?: string,
    stored_name?: string,
    type?: string
}

export interface IBaseEntity {
    id: number,
    section_id?: number,
    name?: string,
    preview_text?: string,
    content_type?: string,
    date_creation?: string,
    active?: boolean,
    content_text?: string,
    date_publiction?: string,
    reactions?: IReaction,
    tags?: string[],

    reportages?: boolean,
    tours?: boolean,
    videoHref?: string,

    images?: string[] | IBXFileType[],
    documentation?: IBXFileType[],
    videos_native?: IBXFileType[],
    videos_embed?: IBXFileType[],
    videos?: string[],
    preview_file_url?: string,
    photo_file_url?: string
}

export interface IBaseIndirectData {
    ID?: string,
    PREVIEW_PICTURE?: string,
    DETAIL_PICTURE?: string,
    IBLOCK_ID?: string,
    NAME?: string,
    CREATED_BY?: string,
    BP_PUBLISHED?: string,
    DATE_CREATE?: string,
    ACTIVE_FROM_X?: string,
    ACTIVE_FROM?: string,
    videos?: string[]
    PREVIEW_TEXT?: string,
    DETAIL_TEXT?: string,
    DETAIL_TEXT_TYPE?: string,
    PREVIEW_TEXT_TYPE?: string,
}

export interface IDocument {
    id?: string,
    original_name?: string,
    stored_name?: string,
    content_type?: string,
    type?: string,
    article_id?: number,
    b24_id?: string,
    file_url?: string,
    is_archive?: boolean,
    is_preview?: boolean
}