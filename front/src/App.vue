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
                        <RouterView @showToast="(errorType: string, text: string) => showToast(errorType, text)" />
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
    <Toast position="bottom-right" />
</template>

<script lang="ts">
import { defineComponent, computed, watch, onMounted } from "vue";
import { RouterView, useRoute } from "vue-router";

import LayoutHeader from "./components/layout/LayoutHeader.vue";
import Sidebar from "./components/layout/RightSidebar.vue";
import Breadcrumbs from "./components/layout/Breadcrumbs.vue";
import AuthPage from "./views/user/AuthPage.vue";

import { useUserData } from "./stores/userData";
import { prefetchSection } from "./utils/prefetchSection";

import Toast from 'primevue/toast';
import { useToast } from 'primevue/usetoast';


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
        // предзагрузка данных в стор
        watch(route, () => {
            const factoryGuidRoutes = ['factories', 'factoryReports', 'factoryTours', 'factoryTour'];
            const blogsRoutes = ['blogs', 'blogOf', 'certainBlog'];
            prefetchSection('user');
            prefetchSection('calendar');

            if (blogsRoutes.includes(String(route.name))) {
                prefetchSection('blogs')
            } else if (factoryGuidRoutes.includes(String(route.name))) {
                prefetchSection('factoryGuid')
            }
        }, { immediate: true, deep: true })

        onMounted(() => {
            useUserData().initKeyFromStorage();
        })

        const toast = useToast();
        const showToast = (type: string, text: string) => {
            toast.add({ severity: type, summary: '', detail: text, life: 13000 });
        };

        return {
            isLogin: computed(() => useUserData().getIsLogin),
            showToast
        }
    }
})
</script>

<style lang="scss">
@use "./assets/styles/mixins/mixins.scss" as *;
</style>
