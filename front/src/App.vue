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
</template>

<script lang="ts">
import { defineComponent, computed, watch, ref, onMounted } from "vue";
import { RouterView, useRoute } from "vue-router";
import LayoutHeader from "./components/layout/LayoutHeader.vue";
import Sidebar from "./components/layout/RightSidebar.vue";
import AuthPage from "./views/user/AuthPage.vue";
import Breadcrumbs from "./components/layout/Breadcrumbs.vue";

import { useblogDataStore } from "./stores/blogData";
import { getBlogAuthorsToStore } from "./utils/getBlogAuthorsToStore";
import { useLoadingStore } from '@/stores/loadingStore'
import { useUserData } from "./stores/userData";
import { useViewsDataStore } from "./stores/viewsData";
export default defineComponent({
    name: "app-layout",
    components: {
        LayoutHeader,
        Sidebar,
        RouterView,
        AuthPage,
        Breadcrumbs
    },
    setup() {
        const blogData = useblogDataStore();
        const blogAuthors = computed(() => blogData.getAllAuthors)
        const currentYear = new Date().getFullYear();

        const route = useRoute();
        const allAuthors = ref([]);
        // предзагрузка блогов в стор
        watch(route, () => {
            if (route.fullPath.includes('blog') && !blogAuthors.value.length) {
                getBlogAuthorsToStore(allAuthors, blogData)
            }
        }, { immediate: true, deep: true })

        onMounted(() => {
            useUserData().initKeyFromStorage();
            fetch(`https://portal.emk.ru/rest/1/f5ij1aoyuw5f39nb/calendar.event.get.json?type=company_calendar&ownerId=0&from=${currentYear}-01-01&to=${currentYear}-12-31`)
                .then((resp) => resp.json())
                .then((data) => {
                    useViewsDataStore().setData(data.result, 'calendarData');
                });
        })

        return {
            isLogin: computed(() => useUserData().getIsLogin),
            isLoading: computed(() => useLoadingStore().getLoadingStatus)
        }
    }
})
</script>

<style lang="scss">
@use "./assets/styles/mixins/mixins.scss" as *;
</style>
