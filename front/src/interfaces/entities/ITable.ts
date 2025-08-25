export interface ItableItem {
    id?: number,
    name?: string,
    author?: string,
    score?: string,
    stars__count?: string,
    reviewsCount?: string,
    date?: string,
    subsection?: string,
    content_text?: string,
    indirect_data?: {
        author?: string,
        subsection?: string,
        subsection_id?: string,
        event_date?: string,
        reviews?: {
            reviewer?: string
            text?: string,
            stars?: string,
        }[],
    },
    documentation?: {
        file_url?: string,
    }[],
    images?: {
        file_url?: string,
    }[],
    videos_native?: {
        article_id: number,
        b24_id: string,
        content_type: string,
        file_url: string,
        id: string,
        is_archive: boolean,
        is_preview: boolean,
        original_name: string,
        stored_name: string,
        type: string
    }[],
}