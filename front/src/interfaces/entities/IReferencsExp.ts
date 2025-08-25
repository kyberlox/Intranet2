interface ISector {
    sectorTitle: string;
    sectorId: string,
    sectorDocs?: {
        article_id?: number,
        b24_id?: string,
        file_url?: string,
        id?: string,
        is_archive?: boolean,
        is_preview?: boolean,
        original_name?: string,
        stored_name?: string,
        type?: string
    }[],
    sectorImgs?: string[],
}

interface IFactoryInExpData {
    sectors: ISector[];
    factoryName: string;
    factoryId: string;
}

export interface IFormattedData {
    [factoryKey: string]: IFactoryInExpData;
}