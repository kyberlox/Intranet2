export const extractYears = (objects) => {
    const years = [];
    objects.map((e) => {
        if (e.date_creation) {
            years.push(e.date_creation)
        }
    })
    const uniqueYears = [...new Set(years.map(date => date.split('-')[0]))];
    return uniqueYears.sort((a, b) => b - a);
}