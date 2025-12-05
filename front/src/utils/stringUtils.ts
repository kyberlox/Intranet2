export const textAreaRowsToContent = (str: string): number => {
    return str.split("\n").length;
}

export const makeSlashToBr = (str: string): string => {
    return str.replace('\n', '<br/>');
}
