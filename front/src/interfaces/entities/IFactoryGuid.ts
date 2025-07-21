import type { IBaseIndirectData, IBaseEntity } from "./IBase"

interface IExperienceData extends IBaseIndirectData {
    enterprise: string,
    enterpriseId: string,
    industry: string,
    industryId: string,
    sectorId: string,
    sector: string
}

interface IFactoryGuidData extends IBaseIndirectData {
    tours?: IFactoryDataTours[],
    reports?: IFactoryDataReports[]
}


export interface IFactoryDataTours {
    id?: string;
    name?: string;
    active?: boolean;
    '3D_files_path'?: string;
    photo_file_url?: string;
}

export interface IFactoryDataReports {
    id?: string,
    date?: string,
    link?: string,
    name?: string,
    active?: boolean,
    photo_file_url?: string
}

export interface IExperience extends IBaseEntity {
    indirect_data?: IExperienceData
}

export interface IFactoryGuidSlides extends IBaseEntity {
    indirect_data?: IFactoryGuidData
}