<template>
<div v-if="isLogin"
     :class="{ 'dark-mode': isDarkMode }">
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
        <PageScrollArrow />
    </main>
</div>
<div v-else>
    <AuthPage />
</div>
<Toast :position="'bottom-right'" />
<YandexMetrika v-if="userId"
               :uid="userId" />
</template>

<script lang="ts">
import { defineComponent, computed, watch, onMounted } from "vue";
import { RouterView, useRoute } from "vue-router";
import Toast from 'primevue/toast';
import LayoutHeader from "./components/layout/LayoutHeader.vue";
import Sidebar from "./components/layout/RightSidebar.vue";
import Breadcrumbs from "./components/layout/Breadcrumbs.vue";
import AuthPage from "./views/user/AuthPage.vue";
import YandexMetrika from "./components/tools/common/YandexMetrika.vue";
import { useUserData } from "./stores/userData";
import { prefetchSection } from "./composables/usePrefetchSection";
import PageScrollArrow from "./components/layout/PageScrollArrow.vue";
import { useStyleModeStore } from "./stores/styleMode";

export default defineComponent({
    name: "app-layout",
    components: {
        LayoutHeader,
        Sidebar,
        RouterView,
        AuthPage,
        Breadcrumbs,
        Toast,
        PageScrollArrow,
        YandexMetrika
    },
    setup() {
        const route = useRoute();
        const userData = useUserData();
        const isLogin = computed(() => userData.getIsLogin);

        // предзагрузка данных в стор
        watch([route, isLogin], () => {
            if (isLogin.value) {
                prefetchSection('score');
                prefetchSection('calendar');
                const factoryGuidRoutes = ['factories', 'factoryReports', 'factoryTours', 'factoryTour'];
                const blogsRoutes = ['blogs', 'blogOf', 'certainBlog', 'adminElementInnerEdit'];

                if (blogsRoutes.includes(String(route.name)) || (route.name == 'adminElementInnerEdit' && route.params.id == '15')) {
                    prefetchSection('blogs')
                } else if (factoryGuidRoutes.includes(String(route.name))) {
                    prefetchSection('factoryGuid')
                }
            }
        }, { immediate: true, deep: true })

        onMounted(() => {
            userData.initKeyFromStorage();
            if (userData.getAuthKey) {
                prefetchSection('user');
            }
        })

        return {
            isLogin,
            userId: computed(() => useUserData().getMyId),
            isDarkMode: computed(() => useStyleModeStore().getDarkMode)
        }
    }
})
</script>
