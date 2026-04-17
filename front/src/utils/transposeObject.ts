type NameValue<T, K extends keyof T> = {
    name: K
    value: (T[K] | null)[]
}

export function toNameValueFormat<T extends Record<string, unknown>>(
    data: T[]
): NameValue<T, keyof T>[] {
    const result: Partial<Record<keyof T, (T[keyof T] | null)[]>> = {}

    data.forEach((item) => {
        (Object.keys(item) as (keyof T)[]).forEach((key) => {
            if (!result[key]) {
                result[key] = []
            }
            result[key]!.push(item[key] ?? null)
        })
    })

    return (Object.keys(result) as (keyof T)[]).map((key) => ({
        name: key,
        value: result[key]!,
    }))
}

export function nameValueToRows<T extends Record<string, unknown>, K extends keyof T>(
    columns: NameValue<T, K>[]
): T[] {
    if (columns.length === 0) return []

    const rowCount = columns[0]?.value.length ?? 0

    return Array.from({ length: rowCount }, (_, i) => {
        const row = {} as T

        columns.forEach((col) => {
            row[col.name] = col.value[i] as T[K]
        })

        return row
    })
}
