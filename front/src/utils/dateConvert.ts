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
}