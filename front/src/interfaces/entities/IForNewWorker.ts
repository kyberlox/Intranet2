import type { IBaseIndirectData, IBaseEntity } from "./IBase"

export interface IForNewWorkerData extends IBaseIndirectData {
    sort?: string
}

export interface IForNewWorker extends IBaseEntity {
    indirect_data?: IForNewWorkerData
}
