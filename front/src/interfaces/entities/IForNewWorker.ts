import type { IBaseIndirectData, IBaseEntity } from "./IBase"

export interface IForNewWorkerData extends IBaseIndirectData {
    sort?: string,
    module?: string
}

export interface IForNewWorker extends IBaseEntity {
    indirect_data?: IForNewWorkerData
}
