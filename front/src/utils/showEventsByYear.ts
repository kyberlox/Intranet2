import type { IBaseEntity } from "@/interfaces/IEntities";

export const showEventsByYear = (allEvents: IBaseEntity[], year: string) => {
    const visibleEvents: IBaseEntity[] = [];
    allEvents.forEach((e) => {
        if (e.date_creation && (String(new Date(e.date_creation).getFullYear()) == year) ) {
            visibleEvents.push(e);
        }
    })

    return visibleEvents
}