interface IBaseEntity {
    "section_id"?: Number,
    "name"?: String,
    "preview_text"?: String,
    "content_type"?: String,
    "date_creation"?: String,
    "active"?: Boolean,
    "id"?: Number,
    "content_text"?: String,
    "date_publiction"?: String,
    "images"?: [],
    "embedVideos"?: [],
    "nativeVideos"?: [],
    "reactions"?: {
        "likes"?: {
            "mine"?: boolean,
            "count"?: number,
        },
        "views"?: string,
    },
    "videos"?: [],
    "tags"?: [],
    "documents"?: {
        link: string,
        name: string,
    }
}

interface IBaseIndirectData {
    "ID"?: String,
    "PREVIEW_PICTURE"?: string,
    "DETAIL_PICTURE"?: string,
    "IBLOCK_ID"?: String,
    "NAME"?: String,
    "CREATED_BY"?: String,
    "BP_PUBLISHED"?: String,
    "DATE_CREATE"?: String,
    "ACTIVE_FROM_X"?: String,
    "ACTIVE_FROM"?: String,
}

interface IActualNewsIndirectData extends IBaseIndirectData {
    "PROPERTY_1066"?: String[],
    "PROPERTY_1116"?: String[],
    "PROPERTY_284"?: String[],
    "PROPERTY_285"?: String[],
    "PROPERTY_289"?: String[],
    "PROPERTY_290"?: String[],
    "PROPERTY_291"?:
    {
        "TYPE"?: String,
        "TEXT"?: String,
    }[],
    "PROPERTY_292"?: String[],
    "PROPERTY_293"?: String[],
    "PROPERTY_294"?: String[],
    "PROPERTY_295"?: String[],
    "PROPERTY_296"?: String[],
}

interface ICareIndirectData extends IBaseIndirectData {
    "PROPERTY_342"?: String[],
    "PROPERTY_343"?: String[],
    "PROPERTY_344"?: String[],
    "PROPERTY_435"?: String[],
    "PROPERTY_347"?: String[],
    "PROPERTY_348"?:
    {
        "TYPE"?: String,
        "TEXT"?: String
    }[],
    "PROPERTY_349"?: String[],
}

interface IAfishaItemIndirectData extends IBaseIndirectData {
    "PROPERTY_375"?: String[],
    "PROPERTY_438"?: String[],
    "PROPERTY_372"?: String[],
    "PROPERTY_373"?: String[],
    "PROPERTY_374"?:
    {
        "TYPE"?: String,
        "TEXT"?: String
    }[]
    "PROPERTY_376"?: String[],
    "PROPERTY_5004"?: String[]
}

interface ICorpEventsIndirectData extends IBaseIndirectData {
    "PROPERTY_1066"?: String[],
    "PROPERTY_411"?: String[],
    "PROPERTY_284"?: String[],
    "PROPERTY_285"?: String[],
    "PROPERTY_289"?: String[],
    "PROPERTY_290"?: String[],
    "PROPERTY_291"?:
    {
        "TYPE"?: String,
        "TEXT"?: String
    }[],
    "PROPERTY_292"?: String[],
    "PROPERTY_293"?: String[],
    "PROPERTY_294"?: String[],
    "PROPERTY_295"?: String[],
    "PROPERTY_296"?: String[],
}

interface ICorpLifeIndirectData extends IBaseIndirectData {
    "PROPERTY_666": String[],
    "PROPERTY_405": String[],
    "PROPERTY_406": String[],
    "PROPERTY_407": String[],
    "PROPERTY_409": String[],
    "PROPERTY_408": String[],
}

export interface IActualNews extends IBaseEntity {
    "indirect_data"?: IActualNewsIndirectData
}

export interface ICareSlide extends IBaseEntity {
    "indirect_data"?: ICareIndirectData
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