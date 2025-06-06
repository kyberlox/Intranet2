export interface ICalendarEntity {
    "id": string,
    "month": string,
    "date": string,
    "past": boolean,
    "name": string,
    "calendar_id": string,
    "report": {
        "ELEMENT_ID": string,
        "NAME": string,
        "URL": string
    } | false,
    "preview": boolean,
    "color": string,
    "private_event": string,
    "attendee_status": string | null,
    "entryId": string | null
}

export interface ICalendar {
    [key: string]: ICalendarEntity[];
}

export interface ICalendarMini {
    [key: string]: string[];
}