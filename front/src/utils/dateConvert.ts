export const dateConvert = (dateString: string, convertType: 'toStringType' | 'toDateType') => {
    if (convertType == 'toDateType') {
        const [datePart, timePart] = dateString.trim().split(/[T\s]/);
        const [day, month, year] = datePart.replaceAll('-', '.').split('.');
        const dateIsReversed = day.length == 4;
        const time = parseTimePart(timePart);
        const date = new Date(
            Number(dateIsReversed ? day : year),
            Number(month) - 1,
            Number(dateIsReversed ? year : day),
            time.hours,
            time.minutes,
            time.seconds
        );

        return date;
    }
    else if (convertType == 'toStringType') {
        const date = new Date(dateString);
        const day = String(date.getDate()).padStart(2, '0');
        const month = String(date.getMonth() + 1).padStart(2, '0');
        const year = date.getFullYear();

        return `${day}.${month}.${year}`;
    }
    else return ''
}

const parseTimePart = (timePart?: string) => {
    if (!timePart) {
        return { hours: 11, minutes: 35, seconds: 26 };
    }

    const [hours = '0', minutes = '0', seconds = '0'] = timePart.replace('Z', '').split(/[+-]/)[0].split(':');

    return {
        hours: Number(hours),
        minutes: Number(minutes),
        seconds: Number(seconds)
    };
}

export const getMonth = (date: string) => {
    return date.split('.')[1];
}

export const formatDateNoTime = (date: string) => {
    if (!date) return;
    return date.length ? date.split(' ')[0] : date;
}

export const addZeroToMonth = (month: string) => {
    return Number(month) < 9 ? `0${month}` : month
}

export const removeYear = (date: string) => {
    return date.split('.')[0] + '.' + date.split('.')[1];
}
