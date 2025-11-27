import type { IBaseIndirectData, IBaseEntity } from "./IBase"

export interface IContestIndirectData extends IBaseIndirectData {
            author: string,
            caregory: null | string,
            created_by: string,
            nomination: string,
            representative_id: number,
            representative_text: null | string
}

export interface IContest extends IBaseEntity {
    indirect_data: IContestIndirectData
}