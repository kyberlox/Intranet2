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
                <!-- <RouterLink class="sidebar-lk__body__points__point"
                            v-for="(point, index) in points"
                            :key="index"
                            :to="routeHandle(point)">
                    {{ point.name }}
                </RouterLink> -->
            </div>
        </div>
    </div>
    <div v-if="visibleSidebar"
         class="sidebar-lk-backdrop"
         @click="close"></div>
</template>
<script lang="ts">
import { computed, defineComponent, watch } from 'vue'
import { points } from '@/assets/staticJsons/navLinks'
import { useUserData } from '@/stores/userData'
import { useRoute } from 'vue-router'

export default defineComponent({
    props: {
        visibleSidebar: {
            type: Boolean,
            default: false,
        }
    },
    emits: ['closeSidebar'],
    setup(props, { emit }) {
        const route = useRoute();

        const useUserStore = useUserData();
        const idForRoute = computed(() => useUserStore.getMyId);
        const routeHandle = (point) => {
            if (point.href == 'logout') {
                return ({ name: 'auth' })
            }
            else if (idForRoute.value) {
                return ({ name: point.href, params: { id: idForRoute.value } })
            }
        }

        watch((route), (newVal) => {
            if (newVal) {
                emit('closeSidebar');
            }
        })

        return {
            points,
            close: () => emit('closeSidebar'),
            routeHandle,
        }
    }
})
</script>