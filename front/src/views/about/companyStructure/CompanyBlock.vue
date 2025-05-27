<template>
    <div class="company-block"
         :class="{ 'company-block--root': level === 0 }">
        <div class="company-block__header">
            <h3 v-if="level === 0"
                class="company-block__title company-block__title--root">
                {{ department.name }}
            </h3>
            <h4 v-else
                class="company-block__title">
                {{ department.name }}
            </h4>
        </div>

        <div class="company-block__users"
             v-if="department.users && department.users.length">
            <div class="user-card"
                 v-for="worker in department.users"
                 :key="worker.user_id">
                <div class="user-card__name">{{ worker.user_fio }}</div>
                <div class="user-card__position">{{ worker.user_position }}</div>
            </div>
        </div>

        <!-- Рекурсивно отображаем детей в горизонтальном ряду -->
        <div v-if="department.children && department.children.length"
             class="company-block__children">
            <CompanyBlock v-for="child in department.children"
                          :key="child.id"
                          :department="child"
                          :level="level + 1" />
        </div>
    </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue';

export default defineComponent({
    props: {
        department: Object,
        level: Number
    },
    setup() {
        return {}
    }
})
</script>
<style lang="scss">
.company-block {
    background: #ffffff;
    border-radius: 4px;
    border: 1px solid #e5e7eb;
    padding: 12px;
    transition: border-color 0.2s ease;
    min-width: 200px;
    flex: 1;

    &:hover {
        border-color: #d1d5db;
    }

    &--root {
        background: #f9fafb;
        border-color: #374151;
        margin-bottom: 16px;

        .company-block__title--root {
            color: #111827;
        }

        .user-card {
            background: #f3f4f6;
            border-color: #d1d5db;

            &__name {
                color: #111827;
                font-weight: 500;
            }

            &__position {
                color: #6b7280;
            }
        }
    }
}

.company-block__header {
    margin-bottom: 8px;
    text-align: center;
}

.company-block__title {
    margin: 0;
    font-weight: 500;
    color: #374151;
    text-align: center;
    font-size: 14px;

    &--root {
        font-size: 18px;
        font-weight: 600;
        margin-bottom: 4px;
    }
}

.company-block__users {
    display: flex;
    flex-direction: column;
    gap: 6px;
    margin-bottom: 12px;
}

.user-card {
    background: #f9fafb;
    border: 1px solid #e5e7eb;
    border-radius: 3px;
    padding: 8px;
    text-align: center;

    &:hover {
        background: #f3f4f6;
    }

    &__name {
        font-size: 13px;
        font-weight: 500;
        color: #374151;
        margin-bottom: 2px;
    }

    &__position {
        font-size: 11px;
        color: #6b7280;
    }
}

.company-block__children {
    display: flex;
    flex-wrap: wrap;
    gap: 12px;
    margin-top: 12px;

    .company-block {
        border-color: #d1d5db;
        margin-bottom: 0;

        &:not(.company-block--root) {
            min-width: 180px;
            max-width: 250px;
        }
    }
}

@media (max-width: 768px) {
    .company-block {
        padding: 10px;
        min-width: 150px;

        &__title {
            font-size: 13px;

            &--root {
                font-size: 16px;
            }
        }
    }

    .company-block__children {
        gap: 8px;

        .company-block {
            min-width: 140px;
            max-width: 180px;
        }
    }

    .user-card {
        padding: 6px;

        &__name {
            font-size: 12px;
        }

        &__position {
            font-size: 10px;
        }
    }
}

@media (max-width: 480px) {
    .company-block__children {
        flex-direction: column;

        .company-block {
            min-width: auto;
            max-width: none;
        }
    }
}
</style>
