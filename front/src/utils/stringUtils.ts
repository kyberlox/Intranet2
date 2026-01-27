export const textAreaRowsToContent = (str: string): number => {
    return str.split("\n").length;
}

export const makeSlashToBr = (str: string): string => {
    return str.replace('\n', '<br/>');
}

export const createUniqueArr = (firstArr: string[], secArr: string[]) => {
   return new Set(firstArr.concat(secArr).filter((e)=>Boolean(e) !== false))
}