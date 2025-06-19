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
    reactions?: {
        likes?: {
            mine?: boolean,
            count?: number,
        },
        views?: string,
    },
    tags?: string[],
    documents?: {
        link: string,
        name: string,
    },

    reportages?: boolean,
    tours?: boolean,
    videoHref?: string[]

    images?: string[],
    documentation?: string[],
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

interface ISafetyTechnicsData extends IBaseIndirectData {
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

export interface IBlogData extends IBaseIndirectData {
    PROPERTY_453?: string,
    PROPERTY_451?: string,
    PROPERTY_1022?: string,
    TITLE?: string,
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

export interface IFactoryData extends IBaseIndirectData {
    PREVIEW_PICTURE?: string,
    hrefTitle?: string,
    reportages?: boolean,
    reportsHref?: string,
    tours?: boolean,
    toursHref?: string,
    factoryId?: number,
    videoHref?: string[],
    href?: string,
    tourId?: string,
}

export interface IOpenVacancyData extends IBaseIndirectData {
    PROPERTY_5094: string[]
}

export interface IBlogAuthors {
    id: number,
    authorId: number,
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

export interface IFactorySlides extends IBaseEntity {
    indirect_data?: IFactoryData
}

export interface IOpenVacancy extends IBaseEntity {
    indirect_data?: IOpenVacancyData
}

export interface IBlogArticle extends IBaseEntity {
    indirect_data?: IBlogArticleData
}

// Общий индирект
export interface IUnionEntities extends IBaseEntity {
    indirect_data?: IActualNewsIndirectData |
    ICareIndirectData |
    ISafetyTechnicsData |
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
    IFactoryData |
    IOpenVacancyData
}

// ЮНИОН внутреннего индиректа
export type IUnionEntitiesData =
    IActualNewsIndirectData |
    ICareIndirectData |
    ISafetyTechnicsData |
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
    IFactoryData |
    IOpenVacancyData