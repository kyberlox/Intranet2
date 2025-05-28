export interface IBlog {
    "id"?: number,
    "active"?: boolean,
    "content_text"?: string,
    "date_publiction"?: string,
    "preview_text"?: string | null,
    "name"?: string,
    "indirect_data"?: {
        "ID"?: string,
        "IBLOCK_ID"?: string,
        "NAME"?: string,
        "TITLE"?: string,
        "CREATED_BY"?: string,
        "DETAIL_TEXT"?: string,
        "DETAIL_PICTURE"?: string,
        'PROPERTY_453'?: string,
        'PROPERTY_451'?: string,
        "DATE_CREATE"?: string,
    },
    "images"?: [],
    "embedVideos"?: [],
    "nativeVideos"?: [],
    "reactions"?: {
        "likes"?: {
            "mine"?: boolean,
            "count"?: number,
        },
        "views"?: string,
    },
    "videos"?: [],
    "tags"?: [],
    "documents"?: {
        link: string,
        name: string,
    }[],
}

export interface IBlogAuthors {
    id: string,
    authorId: string,
    title: string,
}