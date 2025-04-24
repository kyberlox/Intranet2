export interface WorkersOfTheYear {
    [year: number]: {
        id: number;
        name: string;
        position: string;
        department: string;
        photo: string;
        description?: string;
    }[];
}

export interface IWorkersResults {
    "ID"?: string,
    "IBLOCK_ID"?: string,
    "NAME"?: string,
    "IBLOCK_SECTION_ID"?: null,
    "CREATED_BY"?: string,
    "BP_PUBLISHED"?: string,
    "CODE"?: null,
    "PROPERTY_1035"?: {
        [key: string]: string
    },
    "PROPERTY_1036"?: {
        [key: string]: string
    },
    "PROPERTY_1037"?: {
        [key: string]: string
    },
    "PROPERTY_1113"?: {
        [key: string]: string
    },
    "PROPERTY_1039"?: {
        [key: string]: string
    },
    [key: string]: any
}