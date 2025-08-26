import type { IBXFileType } from "./IBase";

export interface IAdminListItem {
    name?: string;
    disabled?: string;
    data_type?: string;
    field?: string;
    values?: string[];
    value?: string;
}

export interface IFileToUpload {
    name: string;
    size: number;
    url: string;
    file: File;
}

export interface newFileData {
    documentation?: IBXFileType[],
    images?: IBXFileType[] | string[],
    videos_embed?: string[],
    videos_native?: string[]
}