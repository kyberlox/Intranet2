import type { IBaseIndirectData, IBaseEntity } from "./IBase"

export interface IForNewWorkerData extends IBaseIndirectData {
    PROPERTY_479?: string[],
    PROPERTY_475?: string[],
    PROPERTY_476?: string[],
    PROPERTY_477?:
    {
        TYPE: string,
        TEXT: string
    }[],
    PROPERTY_478?: string[],
    PROPERTY_480?: string[]
}

export interface IForNewWorker extends IBaseEntity {
    indirect_data?: IForNewWorkerData
}
