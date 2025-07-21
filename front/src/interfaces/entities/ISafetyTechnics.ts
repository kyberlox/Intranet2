export interface ISafetyTechnicsVertSlide {
    content?: {
        id?: number,
        name?: string,
        image?: string,
        images?: string[],
        videos?: string[],
        content_text?: string,
        subtitle?: string,
        header?: string,
        description?: string,
        routeTo?: string
        preview_file_url?: string,
    }[],
    evacuationContent?: {
        images?: string[],
    },
    sideInfo?: string,
}

export interface ISafetyTechnicsSlide {
    content?: {
        id?: number,
        videos?: string[],
        content_text?: string,
        images?: string[]
        preview_file_url?: string,

    },
    evacuationContent?: {
        images?: string[],
    },
    sideInfo?: string,
}