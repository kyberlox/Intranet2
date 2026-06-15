type calendarType = 'dayAndMonth' | 'monthAndYear' | 'month' | 'fullNoYear' | 'full';

const addZeroBeforeDigit = (num: number | string) => {
    return Number(num) < 9 ? '0' + String(num) : String(num)
}

export const calendarTypeFormat = (type: calendarType, newDate: Date) => {
    const day = newDate.getDate();
    const month = newDate.getMonth() + 1;
    const year = newDate.getFullYear();
    const time = newDate.getHours() + ':' + addZeroBeforeDigit(newDate.getMinutes());

    switch (type) {
        case 'dayAndMonth':
            return `${addZeroBeforeDigit(day)}.${addZeroBeforeDigit(month)}`;
        case 'monthAndYear':
            return `${addZeroBeforeDigit(month)}.${year}`;
        case 'month': {
            const formatMonth = newDate.toLocaleString('ru', { 'month': 'long' })
            return formatMonth.charAt(0).toUpperCase() + formatMonth.slice(1);
        }
        case 'fullNoYear':
            return `${addZeroBeforeDigit(day)}.${addZeroBeforeDigit(month)}.${year}`
        case 'full':
            return `${addZeroBeforeDigit(day)}.${addZeroBeforeDigit(month)}.${year} ${time ?? '00:00'}`
        default:
            break;
    }
}
