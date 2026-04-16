import type { IBaseEntity, IBaseIndirectData } from "./IBase";

export interface ISinerTableData extends IBaseEntity{
    indirect_data: ISinerTableIndirectData
}

export interface ISinerTableIndirectData extends IBaseIndirectData{
    implementer:[{
        fio: string,
        photo_file_url:string
    }],
    integrator?:[{
        fio: string,
        photo_file_url:string
    }],
    status:"Закрыт"|"Запущен",
    sinerteam_number:string,
    date_status: string,
    note_status:string
    sinerteam_name:string,
}

export interface ISinerTableParsedData extends IBaseEntity{
    "indirect_data-integrator"?:[{
        fio: string,
        photo_file_url:string
    }],
    "indirect_data-implementer":[{
        fio: string,
        photo_file_url:string
    }],
    "indirect_data-status":"Закрыт"|"Запущен"
    "indirect_data-date_status":string,
    "indirect_data-note_status":string,
    "indirect_data-sinerteam_number":string,
    "indirect_data-sinerteam_name":string,
}

export interface ISinerTableTransposedData {
    name:string,
    value: unknown[]
}
