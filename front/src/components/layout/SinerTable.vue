<template>
<div class="siner-table__wrapper">
    <table class="siner-table">
        <thead>
            <tr>
                <th v-for="column in columns"
                    :key="column.key"
                    :class="{
                        sortable: column.sortable,
                        'sorted-asc':
                            column.sortable &&
                            sortKey === column.key &&
                            sortDirection === 'asc',
                        'sorted-desc':
                            column.sortable &&
                            sortKey === column.key &&
                            sortDirection === 'desc',
                    }"
                    @click="column.sortable && handleSort(column.key)">
                    {{ column.label }}
                    <span v-if="column.sortable"
                          class="sort-icon">
                        <span v-if="sortKey === column.key && sortDirection === 'asc'">↑</span>
                        <span v-else-if="sortKey === column.key && sortDirection === 'desc'">↓</span>
                        <span v-else>↕</span>
                    </span>
                </th>
            </tr>
        </thead>

        <tbody v-if="!loading">
            <tr v-for="(row, rowIndex) in sortedRows"
                :key="rowIndex"
                @click="handleRowClick(row, rowIndex)">
                <td v-for="column in columns"
                    :key="column.key">
                    <slot :name="`column-${column.key}`"
                          :value="getValue(row, column.key)"
                          :row="row"
                          :column="column"
                          :rowIndex="rowIndex">
                        <template v-if="column.formatter">
                            {{ column.formatter(getValue(row, column.key)) }}
                        </template>
                        <span v-else-if="column.component">
                            <component :is="column.component"
                                       v-bind="getComponentProps(column, getValue(row, column.key), row)
                                        " />
                        </span>
                        <template v-else>
                            {{ formatValue(getValue(row, column.key)) }}
                        </template>
                    </slot>
                </td>
            </tr>
            <tr v-if="sortedRows.length === 0">
                <td :colspan="columns.length"
                    class="siner-table__empty-cell">
                    {{ emptyMessage }}
                </td>
            </tr>
        </tbody>
    </table>
</div>
<div class="siner-table__loading">
    <Loader />
</div>
</template>

<script lang="ts">
import { defineComponent, type PropType, ref, computed } from 'vue'
import Loader from './Loader.vue'

export type ColumnDefinition<T = Record<string, unknown>> = {
    key: string
    label: string
    field?: keyof T | string
    formatter?: (value: unknown) => string
    component?: unknown
    componentProps?: Record<string, unknown> | ((value: unknown, row: T) => Record<string, unknown>)
    sortable?: boolean
    filterable?: boolean
    width?: string | number
    align?: 'left' | 'center' | 'right'
    class?: string
}

export type TableRow = Record<string, unknown>

export default defineComponent({
    name: 'SinerTable',

    props: {
        rows: {
            type: Array as PropType<TableRow[]>,
            required: true,
            default: () => [],
        },
        columns: {
            type: Array as PropType<ColumnDefinition[]>,
            required: true,
            validator: (value: ColumnDefinition[]) => value.length > 0,
        },
        emptyMessage: {
            type: String,
            default: 'Нет данных',
        },
        loading: {
            type: Boolean,
            default: false,
        },
        loadingMessage: {
            type: String,
            default: 'Загрузка...',
        },
    },
    components: {
        Loader
    },

    emits: ['row-click', 'cell-click', 'sort'],

    setup(props, { emit }) {
        const sortKey = ref<string | null>(null)
        const sortDirection = ref<'asc' | 'desc'>('asc')

        const getValue = (row: TableRow, key: string): unknown => {
            const column = props.columns.find((col) => col.key === key)
            const field = column?.field || key

            if (typeof field === 'string' && field.includes('.')) {
                //@ts-expect-error lorem
                return field.split('.').reduce((obj, path) => {
                    if (obj && typeof obj === 'object' && path in obj) {
                        return (obj as Record<string, unknown>)[path]
                    }
                    return undefined
                }, row)
            }

            return row[field as string]
        }

        const compareValues = (a: unknown, b: unknown, sortKey: string): number => {
            const column = props.columns.find((col) => col.key === sortKey)
            const valueA = getValue(a as TableRow, column?.key || '')
            const valueB = getValue(b as TableRow, column?.key || '')

            const getPrimitiveValue = (value: unknown): any => {
                if (value === null || value === undefined) return ''

                if (Array.isArray(value)) {
                    if (value.length === 0) return ''
                    const firstItem = value[0]
                    if (firstItem && typeof firstItem === 'object' && 'fio' in firstItem) {
                        return firstItem.fio || ''
                    }
                    return String(value[0] || '')
                }

                if (typeof value === 'object') {
                    if ('fio' in value && typeof value.fio === 'string') {
                        return value.fio
                    }
                    if ('name' in value && typeof value.name === 'string') {
                        return value.name
                    }
                    return JSON.stringify(value)
                }

                if (typeof value === 'string' && column?.key === 'date_status') {
                    return parseDateForComparison(value)
                }

                return value
            }

            let valA = getPrimitiveValue(valueA)
            let valB = getPrimitiveValue(valueB)

            valA = String(valA).toLowerCase()
            valB = String(valB).toLowerCase()

            if (valA < valB) return -1
            if (valA > valB) return 1
            return 0
        }

        const parseDateForComparison = (dateString: string): number => {
            try {
                const [datePart, timePart] = dateString.split(' ')
                const [day, month, year] = datePart.split('.')
                if (timePart) {
                    const [hours, minutes, seconds] = timePart.split(':')
                    return new Date(
                        Number(year),
                        Number(month) - 1,
                        Number(day),
                        Number(hours),
                        Number(minutes),
                        Number(seconds),
                    ).getTime()
                }
                return new Date(Number(year), Number(month) - 1, Number(day)).getTime()
            } catch {
                return 0
            }
        }

        const sortedRows = computed(() => {
            if (!sortKey.value || !props.rows.length) {
                return props.rows
            }

            const sorted = [...props.rows]
            sorted.sort((a, b) => {
                const comparison = compareValues(a, b, sortKey.value!)
                return sortDirection.value === 'asc' ? comparison : -comparison
            })

            return sorted
        })

        const handleSort = (key: string) => {
            if (sortKey.value === key) {
                sortDirection.value = sortDirection.value === 'asc' ? 'desc' : 'asc'
            } else {
                sortKey.value = key
                sortDirection.value = 'asc'
            }

            emit('sort', { sortKey: sortKey.value, sortDirection: sortDirection.value })
        }

        const getComponentProps = (
            column: ColumnDefinition,
            value: unknown,
            row: TableRow,
        ): Record<string, unknown> => {
            if (typeof column.componentProps === 'function') {
                return column.componentProps(value, row)
            }
            return {
                value,
                row,
                ...(column.componentProps || {}),
            }
        }

        const formatValue = (value: unknown): string => {
            if (value === null || value === undefined) return '—'
            if (typeof value === 'string') return value
            if (typeof value === 'number') return String(value)
            if (typeof value === 'boolean') return value ? 'Да' : 'Нет'
            if (value instanceof Date) return value.toLocaleDateString()
            if (Array.isArray(value)) {
                if (value.length === 0) return '—'
                if (value.length === 1) return formatSingleArrayItem(value[0])
                return `${value.length} элементов`
            }
            if (typeof value === 'object') {
                if ('fio' in value && typeof value.fio === 'string') {
                    return value.fio
                }
                return JSON.stringify(value)
            }
            return String(value)
        }

        const formatSingleArrayItem = (item: unknown): string => {
            if (
                typeof item === 'object' &&
                item !== null &&
                'fio' in item &&
                typeof item.fio === 'string'
            ) {
                return item.fio
            }
            return '[1 элемент]'
        }

        const handleRowClick = (row: TableRow, index: number) => {
            emit('row-click', { row, index })
        }

        const handleCellClick = (
            value: unknown,
            row: TableRow,
            column: ColumnDefinition,
            index: number,
        ) => {
            emit('cell-click', { value, row, column, index })
        }

        return {
            getValue,
            getComponentProps,
            formatValue,
            handleRowClick,
            handleCellClick,
            sortedRows,
            handleSort,
            sortKey,
            sortDirection,
        }
    },
})
</script>
