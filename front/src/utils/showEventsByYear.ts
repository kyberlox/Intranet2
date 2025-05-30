import type { IOfficialEvents } from "@/interfaces/IEntities";

export const showEventsByYear = (allEvents: IOfficialEvents[], year: string) => {

    const visibleEvents: IOfficialEvents[] = [];
    allEvents.map((e) => {
        if (e.date_creation && Array.isArray(e.date_creation) && e.date_creation.includes(year)) {
            visibleEvents.push(e)
        }
    })

    return visibleEvents
}