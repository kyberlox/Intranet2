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
            <AuthPage />
        </div>
    </div>
</PullToRefresh>
<Toast :position="'bottom-right'" />
<YandexMetrika :uid="userId" />
</template>

<script lang="ts">
import { defineComponent, computed, watch, onBeforeMount, ref } from "vue";
import { RouterView, useRoute, useRouter } from "vue-router";
import Toast from 'primevue/toast';
import LayoutHeader from "./components/layout/header/LayoutHeader.vue";
import Sidebar from "./components/layout/sidebars/RightSidebar.vue";
import Breadcrumbs from "./components/layout/Breadcrumbs.vue";
import AuthPage from "@/views/user/AuthPage.vue";
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
        const router = useRouter();
        const userData = useUserData();
        const isLogin = computed(() => userData.getIsLogin);
        const isLoading = ref(true);
        const isRefreshing = ref(false);
        const routerViewKey = ref(0);

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
        watch(([isLogin, route]), async () => {
            console.log(route.query)
            // Если приходит reroute(пр. контакты с выставок), то переадресую на reroute
            if (route && route.query && route.query.reroute && isLogin.value) {
                if (!route.query.reroute.includes('https://intranet.emk.ru')) return
                globalThis.location.href = String(route.query.reroute)
                return
            }

            if (userData.getIsLogin && userData.getMyId == 0) {
                userData.setLogin(false);
            }
            if (!isLogin.value) return
            await prefetchSection('score');
            await prefetchSection('calendar');
            await prefetchSection('user');

            const factoryGuidRoutes = ['factories', 'factoryReports', 'factoryTours', 'factoryTour'];
            const blogsRoutes = ['blogs', 'blogOf', 'certainBlog', 'adminElementInnerEdit'];
            if (blogsRoutes.includes(String(route.name)) || (route.name == 'adminElementInnerEdit' && route.params.id == '15')) {
                await prefetchSection('blogs')
            } else if (factoryGuidRoutes.includes(String(route.name))) {
                await prefetchSection('factoryGuid')
            }

            try {
                const res = await Api.getVendor('https://gpt.emk.ru/check_count')
                useUserData().setGenCount(res);
            }
            catch (error) { console.error(error) }

        }, { deep: true, immediate: true })

        onBeforeMount(async () => {
            const cookieKey = document?.cookie?.split(';')?.find((e) => e.includes('session_id'))?.replace(' session_id=', '');
            if (!cookieKey) return isLoading.value = false;

            try {
                const data = await Api.get(`users/find_by_session_id/${cookieKey}`)
                userData.initLogin(cookieKey, data);
                prefetchSection('user');
                userData.setLogin(true);
            }
            catch (error) {
                console.error(error)
            }
            finally {
                isLoading.value = false

            }
        })

        return {
            isLogin,
            userId: computed(() => useUserData().getMyId),
            isDarkMode: computed(() => useStyleModeStore().getDarkMode),
            route,
            isLoading,
            isRefreshing,
            routerViewKey,
            handleRefresh,
        }
    }
})
</script>
