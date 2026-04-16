<template>
    <div class="siner-table__wrapper">
        <table class="siner-table">
            <thead>
                <tr>
                    <th v-for="column in columns" :key="column.key">
                        {{ column.label }}
                    </th>
                </tr>
            </thead>

            <tbody v-if="!loading">
                <tr v-for="(row, rowIndex) in rows" :key="rowIndex">
                    <td v-for="column in columns" :key="column.key">
                        <slot
                            :name="`column-${column.key}`"
                            :value="getValue(row, column.key)"
                            :row="row"
                            :column="column"
                            :rowIndex="rowIndex"
                        >
                            <template v-if="column.formatter">
                                {{ column.formatter(getValue(row, column.key)) }}
                            </template>
                            <span v-else-if="column.component">
                                <component
                                    :is="column.component"
                                    v-bind="getComponentProps(column, getValue(row, column.key), row)"
                                />
                            </span>
                            <template v-else>
                                {{ formatValue(getValue(row, column.key)) }}
                            </template>
                        </slot>
                    </td>
                </tr>
                <tr v-if="rows.length === 0">
                    <td :colspan="columns.length" class="siner-table__empty-cell">
                        {{ emptyMessage }}
                    </td>
                </tr>
            </tbody>
        </table>

        <div v-if="loading" class="siner-table__loading">
            {{ loadingMessage }}
        </div>
    </div>
</template>

<script lang="ts">
import { defineComponent, type PropType } from 'vue'

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
            default: () => []
        },
        columns: {
            type: Array as PropType<ColumnDefinition[]>,
            required: true,
            validator: (value: ColumnDefinition[]) => value.length > 0
        },
        emptyMessage: {
            type: String,
            default: 'Нет данных'
        },
        loading: {
            type: Boolean,
            default: false
        },
        loadingMessage: {
            type: String,
            default: 'Загрузка...'
        }
    },

    emits: ['row-click', 'cell-click', 'sort'],

    setup(props, { emit }) {
        const getValue = (row: TableRow, key: string): unknown => {
            const column = props.columns.find(col => col.key === key)
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

        const getComponentProps = (column: ColumnDefinition, value: unknown, row: TableRow): Record<string, unknown> => {
            if (typeof column.componentProps === 'function') {
                return column.componentProps(value, row)
            }
            return {
                value,
                row,
                ...(column.componentProps || {})
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
            if (typeof item === 'object' && item !== null && 'fio' in item && typeof item.fio === 'string') {
                return item.fio
            }
            return '[1 элемент]'
        }

        const handleRowClick = (row: TableRow, index: number) => {
            emit('row-click', { row, index })
        }

        const handleCellClick = (value: unknown, row: TableRow, column: ColumnDefinition, index: number) => {
            emit('cell-click', { value, row, column, index })
        }


        return {
            getValue,
            getComponentProps,
            formatValue,
            handleRowClick,
            handleCellClick
        }
    }
})
</script>
