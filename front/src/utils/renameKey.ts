import type { IWorkersResults } from "@/interfaces/IWorkersOfTheYear";

export const renameKey = (item: IWorkersResults, key: string) => {
    const originalKey = Object.keys(item)[0];
    console.log(originalKey);

    const value = item[originalKey as keyof IWorkersResults];
    item[key] = value;
}