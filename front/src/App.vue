<template>
    <div v-if="isLogin">
        <LayoutHeader />
        <main>
            <div class="container-fluid"
                 :class="{ 'container-fluid--nopadding': !isLogin }">
                <div class="row main-layout"
                     :class="{ 'row--nomargin': !isLogin }">
                    <div class="main-content flex-grow">
                        <Breadcrumbs />
                        <RouterView />
                    </div>
                    <div v-if="isLogin"
                         class="main-sidebar flex-shrink d-print-none">
                        <Sidebar />
                    </div>
                </div>
            </div>
        </main>
    </div>
    <div v-else>
        <AuthPage />
    </div>
    <Toast :position="'bottom-right'" />
</template>

<script lang="ts">
import { defineComponent, computed, watch, onMounted } from "vue";
import { RouterView, useRoute } from "vue-router";

import Toast from 'primevue/toast';
import LayoutHeader from "./components/layout/LayoutHeader.vue";
import Sidebar from "./components/layout/RightSidebar.vue";
import Breadcrumbs from "./components/layout/Breadcrumbs.vue";
import AuthPage from "./views/user/AuthPage.vue";

import { useUserData } from "./stores/userData";
import { prefetchSection } from "./composables/usePrefetchSection";

export default defineComponent({
    name: "app-layout",
    components: {
        LayoutHeader,
        Sidebar,
        RouterView,
        AuthPage,
        Breadcrumbs,
        Toast,
    },
    setup() {
        const route = useRoute();
        const userData = useUserData();
        const isLogin = computed(() => userData.getIsLogin);

        // предзагрузка данных в стор
        watch([route, isLogin], () => {
            if (isLogin.value) {
                const factoryGuidRoutes = ['factories', 'factoryReports', 'factoryTours', 'factoryTour'];
                const blogsRoutes = ['blogs', 'blogOf', 'certainBlog', 'adminElementInnerEdit'];
                prefetchSection('calendar');

                if (blogsRoutes.includes(String(route.name))) {
                    prefetchSection('blogs')
                } else if (factoryGuidRoutes.includes(String(route.name))) {
                    prefetchSection('factoryGuid')
                }
            }
        }, { immediate: true, deep: true })

        onMounted(() => {
            userData.initKeyFromStorage();
            prefetchSection('user');
        })

        return {
            isLogin,
        }
    }
})
</script>

<style lang="scss">
@use "./assets/styles/mixins/mixins.scss" as *;
</style>
