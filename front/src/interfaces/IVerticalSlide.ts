export interface IVerticalSlide {
    header?: string,
    preview_file_url?: string,
    name?: string,
    user_fio?: string,
    position?: string,
    department?: string,
    routeTo?: string,
    id?: number,
    subtitle?: string,
    description?: string,
    indirect_data?: {
        organizer?: string,

        // для благотворительных
        PROPERTY_342?: string[],
        PROPERTY_343?: string[],
        PROPERTY_344?: string[],
        PROPERTY_435?: string[],
        PROPERTY_347?: string[],
        PROPERTY_348?:
        {
            TYPE?: string,
            TEXT?: string
        }[],
        PROPERTY_349?: string[],
    }
}