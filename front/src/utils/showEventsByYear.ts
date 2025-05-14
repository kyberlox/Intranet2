
export const showEventsByYear = (allEvents, year: string) => {
    console.log(allEvents);

    const visibleEvents = [];
    allEvents.map((e) => {
        if (e.date_creation.includes(year)) {
            visibleEvents.push(e)
        }
    })
    console.log(visibleEvents);

    return visibleEvents
}