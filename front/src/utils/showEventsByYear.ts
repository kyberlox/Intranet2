import type { IOfficialEvents } from "@/interfaces/IEntities";

export const showEventsByYear = (allEvents: IOfficialEvents[], year: string) => {
    const visibleEvents: IOfficialEvents[] = [];
    allEvents.forEach((e) => {
        if (e.date_creation && String(new Date(e.date_creation).getFullYear()) == year) {
            visibleEvents.push(e);
        }
    })

    return visibleEvents
}