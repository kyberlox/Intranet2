
export const showEventsByYear = (allEvents, year: string) => {
    const visibleEvents = [];
    allEvents.map((e) => {
        if (e.date_creation.includes(year)) {
            visibleEvents.push(e)
        }
    })

    return visibleEvents
}