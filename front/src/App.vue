<template>
<div v-if="route.name !== 'vcard'"
     :class="{ 'dark-mode': isDarkMode }">
    <SnowFlakes v-if="[12, 1, 2].includes(new Date().getMonth() + 1)" />
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
            <PageScrollArrow />
        </main>
    </div>
    <div v-else>
        <AuthPage />
    </div>
</div>
<VCard v-else />
<Toast :position="'bottom-right'" />
<YandexMetrika v-if="userId"
               :uid="userId" />
</template>

<script lang="ts">
import { defineComponent, computed, watch, onMounted } from "vue";
import { RouterView, useRoute } from "vue-router";
import Toast from 'primevue/toast';
import LayoutHeader from "./components/layout/header/LayoutHeader.vue";
import Sidebar from "./components/layout/sidebars/RightSidebar.vue";
import Breadcrumbs from "./components/layout/Breadcrumbs.vue";
import AuthPage from "./views/user/AuthPage.vue";
import YandexMetrika from "./components/tools/common/YandexMetrika.vue";
import { useUserData } from "./stores/userData";
import { prefetchSection } from "./composables/usePrefetchSection";
import PageScrollArrow from "./components/layout/PageScrollArrow.vue";
import { useStyleModeStore } from "./stores/styleMode";
import SnowFlakes from "./components/layout/SnowFlakes.vue";
import VCard from "./views/vcard/VCard.vue";
import router from "./router";

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
        YandexMetrika,
        SnowFlakes,
        VCard
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
                const refferer = localStorage.getItem('from');
                if (refferer) {
                    router.push({ name: refferer });
                    localStorage.removeItem('from');
                }
                if (userData.getAuthKey) {
                    prefetchSection('user');
                }
                const factoryGuidRoutes = ['factories', 'factoryReports', 'factoryTours', 'factoryTour'];
                const blogsRoutes = ['blogs', 'blogOf', 'certainBlog', 'adminElementInnerEdit'];

                if (blogsRoutes.includes(String(route.name)) || (route.name == 'adminElementInnerEdit' && route.params.id == '15')) {
                    prefetchSection('blogs')
                } else if (factoryGuidRoutes.includes(String(route.name))) {
                    prefetchSection('factoryGuid')
                }
            }
        }, { immediate: true, deep: true })

        return {
            isLogin,
            userId: computed(() => useUserData().getMyId),
            isDarkMode: computed(() => useStyleModeStore().getDarkMode),
            route
        }
    }
})
</script>
