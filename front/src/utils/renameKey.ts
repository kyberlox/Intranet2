import type { IWorkerOfTheYear } from "@/interfaces/IEntities";

export const renameKey = <T extends IWorkerOfTheYear>(
    item: T,
    newKey: keyof T
) => {
    const originalKey = Object.keys(item)[0] as keyof T;

    const value = item[originalKey];
    item[newKey] = value;
}
