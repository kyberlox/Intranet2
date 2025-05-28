import type { IWorkersResults } from "@/interfaces/IWorkersOfTheYear";

export const renameKey = (item: IWorkersResults, key: string) => {
    const originalKey = Object.keys(item)[0];

    const value = item[originalKey as keyof IWorkersResults];
    item[key] = value;
}