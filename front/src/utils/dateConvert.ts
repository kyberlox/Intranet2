export const dateConvert = (dateString: string, convertType: 'toStringType' | 'toDateType') => {
    if (convertType == 'toDateType') {
        const [day, month, year] = dateString.split('.');

        const date = new Date(Number(year), Number(month) - 1, Number(day), 11, 35, 26);

        return date.toString();
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