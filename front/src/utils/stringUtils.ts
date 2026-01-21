export const textAreaRowsToContent = (str: string): number => {
    return str.split("\n").length;
}

export const makeSlashToBr = (str: string): string => {
    return str.replace('\n', '<br/>');
}

export const duplicateExist = (element: string, searchArray: Array<string>) => {
    return searchArray.includes(element) ? true : false
}