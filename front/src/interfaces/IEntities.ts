interface IBaseEntity {
    section_id?: number,
    name?: string,
    preview_text?: string,
    content_type?: string,
    date_creation?: string,
    active?: boolean,
    id?: number,
    content_text?: string,
    date_publiction?: string,
    images?: string[],
    embedVideos?: string[],
    nativeVideos?: string[],
    reactions?: {
        likes?: {
            mine?: boolean,
            count?: number,
        },
        views?: string,
    },
    videos?: string[],
    tags?: string[],
    documents?: {
        link: string,
        name: string,
    },
    image?: string,
}

interface IBaseIndirectData {
    ID?: string,
    PREVIEW_PICTURE?: string,
    DETAIL_PICTURE?: string,
    IBLOCK_ID?: string,
    NAME?: string,
    CREATED_BY?: string,
    BP_PUBLISHED?: string,
    DATE_CREATE?: string,
    ACTIVE_FROM_X?: string,
    ACTIVE_FROM?: string,
    videos?: string[]
}

interface IActualNewsIndirectData extends IBaseIndirectData {
    PROPERTY_1066?: string[],
    PROPERTY_1116?: string[],
    PROPERTY_284?: string[],
    PROPERTY_285?: string[],
    PROPERTY_289?: string[],
    PROPERTY_290?: string[],
    PROPERTY_291?:
    {
        TYPE?: string,
        TEXT?: string,
    }[],
    PROPERTY_292?: string[],
    PROPERTY_293?: string[],
    PROPERTY_294?: string[],
    PROPERTY_295?: string[],
    PROPERTY_296?: string[],
}

interface ICareIndirectData extends IBaseIndirectData {
    PROPERTY_342?: string[],
    PROPERTY_343?: string[],
    PROPERTY_344?: string[],
    PROPERTY_435?: string[],
    PROPERTY_347?: string[],
    PROPERTY_348?:
    {
        TYPE?: string,
        TEXT?: string
    }[],
    PROPERTY_349?: string[],
}

interface IAfishaItemIndirectData extends IBaseIndirectData {
    PROPERTY_375?: string[],
    PROPERTY_438?: string[],
    PROPERTY_372?: string[],
    PROPERTY_373?: string[],
    PROPERTY_374?:
    {
        TYPE?: string,
        TEXT?: string
    }[]
    PROPERTY_376?: string[],
    PROPERTY_5004?: string[]
}

interface ICorpEventsIndirectData extends IBaseIndirectData {
    PROPERTY_1066?: string[],
    PROPERTY_411?: string[],
    PROPERTY_284?: string[],
    PROPERTY_285?: string[],
    PROPERTY_289?: string[],
    PROPERTY_290?: string[],
    PROPERTY_291?:
    {
        TYPE?: string,
        TEXT?: string
    }[],
    PROPERTY_292?: string[],
    PROPERTY_293?: string[],
    PROPERTY_294?: string[],
    PROPERTY_295?: string[],
    PROPERTY_296?: string[],
}

interface ICorpLifeIndirectData extends IBaseIndirectData {
    PROPERTY_666: string[],
    PROPERTY_405: string[],
    PROPERTY_406: string[],
    PROPERTY_407: string[],
    PROPERTY_409: string[],
    PROPERTY_408: string[],
}

interface ISafetyTechnicsData extends IBaseIndirectData {
    PROPERTY_342: string[],
    PROPERTY_343: string[],
    PROPERTY_344: string[],
    PROPERTY_435: string[],
    PROPERTY_347: string[],
    PROPERTY_348:
    {
        TYPE: string,
        TEXT: string
    }[],
    PROPERTY_349: string[],
}

export interface IBlogData extends IBaseIndirectData {
    PROPERTY_453?: string,
    PROPERTY_451?: string,
}

export interface IBlogAuthors {
    id: number,
    authorid: number,
    title: string,
}

export interface IActualNews extends IBaseEntity {
    indirect_data?: IActualNewsIndirectData
}

export interface ICareSlide extends IBaseEntity {
    indirect_data?: ICareIndirectData
}

export interface ISafetyTechnicsSlide extends IBaseEntity {
    indirect_data?: ISafetyTechnicsData
}

export interface IAfishaItem extends IBaseEntity {
    indirect_data?: IAfishaItemIndirectData
}

export interface ICorpEventsItem extends IBaseEntity {
    indirect_data?: ICorpEventsIndirectData
}

export interface ICorpLife extends IBaseEntity {
    indirect_data?: ICorpLifeIndirectData
}

export interface IBlog extends IBaseEntity {
    indirect_data?: IBlogData
}






