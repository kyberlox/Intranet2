//V - развернутый T
export function flattenObjectList<T, V>(data: T[]): V[] {
    const result: V[] = [];
    data.forEach(element => {
        result.push(flattenObject(element as unknown as Record<string, string>) as V);
    });
    return result;
}

export function flattenObject(
    data: Record<string, string>,
    parentKey?:string,
    result: Record<string, string> = {}
): Record<string, string> {
    for (const [key, value] of Object.entries(data)) {
        if (typeof value === 'object' && value !== null && !Array.isArray(value)) {
            flattenObject(value,key,result);
        } else {
            result[parentKey?parentKey+"-"+key:key] = value;
        }
    }

    return result;
}
