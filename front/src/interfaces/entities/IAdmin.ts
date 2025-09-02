import type { IBXFileType } from "./IBase";

export interface IReportage {
    id?: string;
    date?: string;
    link: string;
    name: string;
    active?: string;
    photo_file_url?: string;
}

export interface IAdminListItem {
    name?: string;
    disabled?: string;
    data_type?: string;
    field?: string;
    values?: string[];
    value?: string | IReportage[];
}

export interface IFileToUpload {
    name: string;
    size: number;
    url: string;
    file: File;
}

export interface INewFileData {
    documentation?: IBXFileType[],
    images?: IBXFileType[],
    videos_embed?: IBXFileType[],
    videos_native?: IBXFileType[]
}