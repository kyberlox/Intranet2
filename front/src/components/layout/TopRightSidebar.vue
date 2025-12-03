<template>
<div class="sidebar-lk"
     :class="{ 'sidebar-lk--visible': visibleSidebar }">
    <div class="sidebar-lk__header">
        <h5 class="sidebar-lk__header__title">Личный кабинет</h5>
        <div class="modal__overlay__close-button">
            <CloseIcon @click="close" />
        </div>
    </div>
    <div class="sidebar-lk__body">
        <div class="sidebar-lk__body__points">
            <RouterLink class="sidebar-lk__body__points__point"
                        v-for="(point, index) in points.filter((e) => needAdminLink ? e : e.href !== 'admin')"
                        :key="index"
                        :to="uniqueRoutesHandle(point.href, point, idForRoute, '')">
                {{ point.name }}
            </RouterLink>
            <div class="sidebar-lk__body__points__point"
                 @click="handleLogout">Выйти</div>
        </div>
    </div>
</div>
<div v-if="visibleSidebar"
     class="sidebar-lk-backdrop"
     @click="close"></div>
</template>
<script lang="ts">
import { computed, defineComponent, watch, type ComputedRef } from 'vue'
import { points } from '@/assets/static/navLinks'
import { useUserData } from '@/stores/userData'
import { useRoute } from 'vue-router'
import { uniqueRoutesHandle } from '@/router/uniqueRoutesHandle'
import CloseIcon from '@/assets/icons/layout/CloseIcon.svg?component'

export default defineComponent({
    components: {
        CloseIcon
    },
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
        const idForRoute: ComputedRef<number> = computed(() => useUserStore.getMyId);

        watch((route), (newVal) => {
            if (newVal) {
                emit('closeSidebar');
            }
        })

        const handleLogout = () => {
            useUserData().logOut();
        }

        return {
            points,
            idForRoute,
            needAdminLink: computed(() => useUserData().getNeedAdminLink),
            uniqueRoutesHandle,
            close: () => emit('closeSidebar'),
            handleLogout,
        }
    }
})
</script>