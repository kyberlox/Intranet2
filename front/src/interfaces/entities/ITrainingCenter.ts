export interface IConductedTrainings {
    name?: string,
    section_id?: number,
    active?: boolean,
    content_text?: string,
    indirect_data?: {
        author?: string,
        reviews?: {
            text: string,
            stars: string,
            reviewer: string
        }[],
        event_date?: string,
        participants?:
        {
            fio?: string,
            image?: string | null,
            work_position?: string
        }[],
    },
    id: number,
    preview_text?: string | null,
    content_type?: string,
    date_creation: string | null,
    preview_file_url: string | null
}
