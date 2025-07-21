
export interface IReaction {
    views: number,
    likes: {
        count: number,
        likedByMe: boolean
    }
}
interface IBaseEntity {
    id: number,
    section_id?: number,
    name?: string,
    preview_text?: string,
    content_type?: string,
    date_creation?: string,
    active?: boolean,
    content_text?: string,
    date_publiction?: string,
    reactions?: IReaction,
    tags?: string[],
    documents?: {
        link: string,
        name: string,
    },

    reportages?: boolean,
    tours?: boolean,
    videoHref?: string[]

    images?: string[],
    documentation?: {
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
    videos_native?: string[],
    videos_embed?: string[],
    videos?: string[],
    preview_file_url?: string
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
    PREVIEW_TEXT?: string,
    DETAIL_TEXT?: string,
    DETAIL_TEXT_TYPE?: string,
    PREVIEW_TEXT_TYPE?: string,
}

export interface IConductedTrainings {
    "name"?: string,
    "section_id"?: number,
    "active"?: boolean,
    "content_text"?: string,
    "indirect_data"?: {
        "author"?: string,
        "reviews"?: {
            text: string,
            stars: string,
            reviewer: string
        }[],
        "event_date"?: string,
        "participants"?:
        {
            "fio"?: string,
            "image"?: string | null,
            "work_position"?: string
        }[],
    },
    "id": number,
    "preview_text"?: string | null,
    "content_type": string,
    "date_creation": string | null,
    "preview_file_url": string | null
}

export interface IActualNewsIndirectData extends IBaseIndirectData {
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

export interface ICareIndirectData extends IBaseIndirectData {
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

export interface IWorkerOfTheYearData extends IBaseIndirectData {
    uuid: number,
    year: string,
    position: string,
    department: string,
    photo_file_url: string,
    award: string,
    location: string
}

export interface IAfishaItemIndirectData extends IBaseIndirectData {
    PROPERTY_375?: string[],
    PROPERTY_438?: string[],
    PROPERTY_372?: string[],
    PROPERTY_373?: string[],
    PROPERTY_374?:
    {
        TYPE?: string,
        TEXT?: string
    }[],
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
    PROPERTY_666?: string[],
    PROPERTY_405?: string[],
    PROPERTY_406?: string[],
    PROPERTY_407?: string[],
    PROPERTY_409?: string[],
    PROPERTY_408?: string[],
}


export interface IBlogData extends IBaseIndirectData {
    author_uuid: number,
    company: number,
    TITLE?: string,
    photo_file_url: string,
    link: string,
}

export interface IBlogArticleData extends IBaseIndirectData {
    PROPERTY_1222?: string[],
    PROPERTY_1239?: string[],
}

interface IOurPeopleData extends IBaseIndirectData {
    PROPERTY_1235?: string[],
    PROPERTY_1237?: string[],
}

interface IVideoInterviewData extends IBaseIndirectData {
    PROPERTY_1025?: string[],
    PROPERTY_1048?: string[],
    PROPERTY_1026?: string[],
    PROPERTY_1242?: string[],
    PROPERTY_1243?: string[],
    PROPERTY_5045?: string[],
}

interface ICorpNewsData extends IBaseIndirectData {
    PROPERTY_1127?: string[],
    PROPERTY_1128?: string[]
}

interface IOfficialEventsData extends IBaseIndirectData {
    PROPERTY_665?: string[],
    PROPERTY_403?: string[],
    PROPERTY_398?: string[],
    PROPERTY_399?: string[],
    PROPERTY_400?: string[],
    PROPERTY_401?: string[],
    PROPERTY_402?: string[],
}

interface IVideoReportsData extends IBaseIndirectData {
    PROPERTY_1066?: string[]
    PROPERTY_1116?: string[]
    PROPERTY_284?: string[]
    PROPERTY_285?: string[]
    PROPERTY_289?: string[]
    PROPERTY_290?: string[]
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
    PROPERTY_664?: string[],
    PROPERTY_5044?: string[],
}

interface IPartnerBonusData extends IBaseIndirectData {
    PROPERTY_341?: string[],
    PROPERTY_337?: string[],
    PROPERTY_338?: string[],
    PROPERTY_340?: string[],
    PROPERTY_439?: string[],
}

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

export interface IExperienceData extends IBaseIndirectData {
    enterprise: string,
    enterpriseId: string,
    industry: string,
    industryId: string,
    sectorId: string,
    sector: string
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

export interface IFactoryGuidData extends IBaseIndirectData {
    tours?: IFactoryDataTours[],
    reports?: IFactoryDataReports[]
}

export interface IOpenVacancyData extends IBaseIndirectData {
    PROPERTY_5094: string[]
}

export interface IBlogAuthors {
    authorId?: number,
    title?: string,
    authorAvatar?: string,
    link?: string,
    telegramQr?: string
}

export interface IActualNews extends IBaseEntity {
    indirect_data?: IActualNewsIndirectData
}

export interface ICareSlide extends IBaseEntity {
    indirect_data?: ICareIndirectData
}

export interface IExperience extends IBaseEntity {
    indirect_data?: IExperienceData
}

export interface ISafetyTechnicsVertSlide {
    content?: {
        id?: number,
        name?: string,
        image?: string,
        images?: string[],
        videos?: string[],
        content_text?: string,
        subtitle?: string,
        header?: string,
        description?: string,
        routeTo?: string
        preview_file_url?: string,
    }[],
    evacuationContent?: {
        images?: string[],
    },
    sideInfo?: string,
}

export interface ISafetyTechnicsSlide {
    content?: {
        id?: number,
        videos?: string[],
        content_text?: string,
        images?: string[]
        preview_file_url?: string,

    },
    evacuationContent?: {
        images?: string[],
    },
    sideInfo?: string,
}

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

export interface IDocument {
    id?: string,
    original_name?: string,
    stored_name?: string,
    content_type?: string,
    type?: string,
    article_id?: number,
    b24_id?: string,
    file_url?: string,
    is_archive?: boolean,
    is_preview?: boolean
}

export interface ItableItem {
    id?: number,
    name?: string,
    author?: string,
    score?: string,
    stars__count?: string,
    reviewsCount?: string,
    date?: string,
    subsection?: string,
    content_text?: string,
    indirect_data?: {
        author?: string,
        subsection?: string,
        subsection_id?: string,
        event_date?: string,
        reviews?: {
            reviewer?: string
            text?: string,
            stars?: string,
        }[],
    },
    documentation?: {
        file_url?: string,
    }[],
    images?: {
        file_url?: string,
    }[],
    videos_native?: {
        article_id: number,
        b24_id: string,
        content_type: string,
        file_url: string,
        id: string,
        is_archive: boolean,
        is_preview: boolean,
        original_name: string,
        stored_name: string,
        type: string
    }[],
}


export interface IFormattedData {
    [factoryKey: string]: IFactoryInExpData;
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

export interface IOurPeople extends IBaseEntity {
    indirect_data?: IOurPeopleData
}

export interface IVideoInterview extends IBaseEntity {
    indirect_data?: IVideoInterviewData
}

export interface IVideoReports extends IBaseEntity {
    indirect_data?: IVideoReportsData
}
export interface ICorpNews extends IBaseEntity {
    indirect_data?: ICorpNewsData
}

export interface IOfficialEvents extends IBaseEntity {
    indirect_data?: IOfficialEventsData
}

export interface IPartnerBonus extends IBaseEntity {
    indirect_data?: IPartnerBonusData
}

export interface IForNewWorker extends IBaseEntity {
    indirect_data?: IForNewWorkerData
}

export interface IFactoryGuidSlides extends IBaseEntity {
    indirect_data?: IFactoryGuidData
}

export interface IOpenVacancy extends IBaseEntity {
    indirect_data?: IOpenVacancyData
}

export interface IBlogArticle extends IBaseEntity {
    indirect_data?: IBlogArticleData
}

export interface IWorkerOfTheYear extends IBaseEntity {
    indirect_data?: IWorkerOfTheYearData
}

// Общий индирект
export interface IUnionEntities extends IBaseEntity {
    indirect_data?: IActualNewsIndirectData |
    ICareIndirectData |
    IAfishaItemIndirectData |
    ICorpEventsIndirectData |
    ICorpLifeIndirectData |
    IBlogData |
    IBlogArticleData |
    IOurPeopleData |
    IVideoInterviewData |
    IVideoReportsData |
    ICorpNewsData |
    IOfficialEventsData |
    IPartnerBonusData |
    IForNewWorkerData |
    IFactoryGuidData |
    IOpenVacancyData |
    ISafetyTechnicsSlide |
    IFactoryDataReports
}

// ЮНИОН внутреннего индиректа
export type IUnionEntitiesData =
    IActualNewsIndirectData |
    ICareIndirectData |
    IAfishaItemIndirectData |
    ICorpEventsIndirectData |
    ICorpLifeIndirectData |
    IBlogData |
    IBlogArticleData |
    IOurPeopleData |
    IVideoInterviewData |
    IVideoReportsData |
    ICorpNewsData |
    IOfficialEventsData |
    IPartnerBonusData |
    IForNewWorkerData |
    IFactoryGuidData |
    IOpenVacancyData |
    ISafetyTechnicsSlide |
    IFactoryDataReports