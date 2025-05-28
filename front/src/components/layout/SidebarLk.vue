<template>
    <div class="sidebar-lk"
         :class="{ 'sidebar-lk--visible': visibleSidebar }">
        <div class="sidebar-lk__header">
            <h5 class="sidebar-lk__header__title">Личный кабинет</h5>
            <button type="button"
                    class="btn-close"
                    @click="close"></button>
        </div>
        <div class="sidebar-lk__body">
            <div class="sidebar-lk__body__points">
                <RouterLink class="sidebar-lk__body__points__point"
                            v-for="point in points"
                            :key="point.id"
                            :to="routeHandle(point)">
                    {{ point.name }}
                </RouterLink>
            </div>
        </div>
    </div>
    <div v-if="visibleSidebar"
         class="sidebar-lk-backdrop"
         @click="close"></div>
</template>
<script lang="ts">
import { defineComponent } from 'vue'
import { useRouter } from 'vue-router'
import { points } from '@/assets/staticJsons/topRightMenuPoints'

export default defineComponent({
    props: {
        visibleSidebar: {
            type: Boolean,
            default: false,
        }
    },
    emits: ['closeSidebar'],
    setup(props, { emit }) {
        const router = useRouter();

        const routeHandle = (point: { id: number, name: string, href: string, params?: { id: number } }) => {
            if (point.href == 'logout') {
                return ({ name: 'auth' })
            }
            else {
                return ({ name: point.href, params: point.params })
            }
        }

        return {
            points,
            close: () => emit('closeSidebar'),
            routeHandle,
        }
    }
})
</script>