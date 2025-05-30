import type { IOfficialEvents, ICorpEventsItem, ICorpLife, IActualNews } from "@/interfaces/IEntities";

export const extractYears = (objects: IOfficialEvents[] | ICorpEventsItem[] | ICorpLife[] | IActualNews[]) => {
    const years: string[] = [];
    objects.map((e) => {
        if (e.date_creation) {
            years.push(e.date_creation)
        }
    })

    const uniqueYears = [...new Set(years.map(date => date.split('-')[0]))];
    return uniqueYears.sort((a, b) => Number(b) - Number(a));
}