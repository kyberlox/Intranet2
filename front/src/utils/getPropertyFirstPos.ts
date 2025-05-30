// import type { IUnionEntitiesData } from "@/interfaces/IEntities";
import type { IUnionEntitiesData, IUnionEntities } from "@/interfaces/IEntities";

// type IndirectDataTypes = IForNewWorker; // добавьте другие типы по необходимости


export const getProperty = <T extends IUnionEntitiesData>(
    object: IUnionEntities,
    field: keyof T
) => {
    if (!object.indirect_data) return;

    const indirectData = object.indirect_data as T;

    if (indirectData && field in indirectData) {
        const value = indirectData[field];

        if (Array.isArray(value) && value[0]) {
            return value[0];
        }

        if (value && !Array.isArray(value)) {
            return value;
        }
    }
}
