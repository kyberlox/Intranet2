<template>
<VCard v-if="route.name == 'vcard'" />
<InService v-else-if="route.name == 'inservice'" />
<PullToRefresh v-else
               :refreshing="isRefreshing"
               :on-refresh="handleRefresh">
    <div :class="{ 'dark-mode': isDarkMode }">
        <SnowFlakes v-if="[12, 1, 2].includes(new Date().getMonth() + 1)" />
        <div v-if="isLogin">
            <LayoutHeader />
            <main>
                <div class="container-fluid">
                    <div class="row main-layout">
                        <div class="main-content flex-grow">
                            <Breadcrumbs />
                            <RouterView :key="routerViewKey" />
                        </div>
                        <div class="main-sidebar flex-shrink d-print-none">
                            <Sidebar />
                        </div>
                    </div>
                </div>
                <PageScrollArrow />
            </main>
        </div>
        <div v-else-if="!isLoading">
            <AuthPage :reroute="reroute" />
        </div>
    </div>
</PullToRefresh>
<Toast :position="'bottom-right'" />
<YandexMetrika v-if="userId"
               :uid="userId" />
</template>

<script lang="ts">
import { defineComponent, computed, watch, onBeforeMount, ref } from "vue";
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
import Api from "./utils/Api";
import InService from "./views/errors/InService.vue";
import PullToRefresh from "./components/tools/pullToRefresh/PullToRefresh.vue";

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
        VCard,
        InService,
        PullToRefresh,
    },

    setup() {
        const route = useRoute();
        const userData = useUserData();
        const isLogin = computed(() => userData.getIsLogin);
        const isLoading = ref(true);
        const isRefreshing = ref(false);
        const routerViewKey = ref(0);
        const reroute = ref();

        const handleRefresh = () => {
            return new Promise<void>((resolve) => {
                isRefreshing.value = true;

                routerViewKey.value++;

                setTimeout(() => {
                    isRefreshing.value = false;
                    resolve();
                }, 500);
            });
        };

        // предзагрузка данных в стор
        watch([route, isLogin], () => {
            if (userData.getIsLogin && userData.getMyId == 0) {
                userData.setLogin(false);
            }
            else
                if (isLogin.value) {
                    prefetchSection('score');
                    prefetchSection('calendar');

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

        onBeforeMount(() => {
            const cookieKey = document?.cookie?.split(';')?.find((e) => e.includes('session_id'))?.replace(' session_id=', '');
            if (!cookieKey) return isLoading.value = false;

            Api.get(`users/find_by_session_id/${cookieKey}`)
                .then((data) => {
                    userData.initLogin(cookieKey, data);
                    prefetchSection('user');
                })
                .finally(() => { userData.setLogin(true); isLoading.value = false })

            console.log(useRoute());

            if (useRoute().query.reroute) {
                reroute.value = String(useRoute().query.reroute).replace('/?reroute=', '')
            }
        })

        return {
            isLogin,
            userId: computed(() => useUserData().getMyId),
            isDarkMode: computed(() => useStyleModeStore().getDarkMode),
            route,
            isLoading,
            isRefreshing,
            handleRefresh,
            routerViewKey,
            reroute
        }
    }
})
</script>
