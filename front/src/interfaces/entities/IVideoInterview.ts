import type { IBaseIndirectData, IBaseEntity } from "./IBase"

interface IVideoInterviewData extends IBaseIndirectData {
    author?: string
}

export interface IVideoInterview extends IBaseEntity {
    indirect_data?: IVideoInterviewData
}
