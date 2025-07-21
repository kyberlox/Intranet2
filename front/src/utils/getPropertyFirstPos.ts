export const getProperty = (object, field) => {
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
