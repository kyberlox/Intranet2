import type { IUserList } from "@/components/tools/common/SearchList.vue";
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
    values?: string[] | { name: string, vision_name?: string, id?: string | number, value?: string }[];
    value?: number | string | IReportage[] | IUserList[] | number[];
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

export interface IRoots{
    PeerAdmin:boolean,
    EditorAdmin:boolean,
    VisionAdmin:boolean,
    GPT_gen_access: boolean,
    PeerModer: boolean,
    EditorModer: number[], 
    peerCurator: boolean[]
}
