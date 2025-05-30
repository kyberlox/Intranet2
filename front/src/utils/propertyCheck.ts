import type { IBlogData } from "@/interfaces/IEntities";

export const propertyCheck = (object: IBlogData | undefined, target: string) => {
    if (!object) return;
    return Object.keys(object).includes(target);
}