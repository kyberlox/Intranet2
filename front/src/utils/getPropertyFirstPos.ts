interface IGetPropertyObjectData {
    PROPERTY_347?: string[],
    PROPERTY_348?: {
        TEXT?: string
    }[];
    PROPERTY_374?: {
        TEXT?: string
    }[];
    PROPERTY_375?: string[],
    PROPERTY_1222?: string[],
    PROPERTY_5094?: string[],
}

interface IGetPropertyObject {
    indirect_data?: IGetPropertyObjectData
}

export const getProperty = (object: IGetPropertyObject, field: keyof IGetPropertyObjectData) => {
    if (!object.indirect_data) return;

    const indirectData = object.indirect_data;

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
