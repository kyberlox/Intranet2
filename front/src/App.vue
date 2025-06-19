<template>
    <div v-if="isLogin">
        <LayoutHeader />
        <main>
            <div class="container-fluid"
                 :class="{ 'container-fluid--nopadding': !isLogin }">
                <div class="row flex-layout"
                     :class="{ 'row--nomargin': !isLogin }">
                    <div class="main-content flex-grow">
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

import { useblogDataStore } from "./stores/blogData";
import { getBlogAuthorsToStore } from "./utils/getBlogAuthorsToStore";
import { useLoadingStore } from '@/stores/loadingStore'
import { useUserData } from "./stores/userData";
export default defineComponent({
    name: "app-layout",
    components: {
        LayoutHeader,
        Sidebar,
        RouterView,
        AuthPage,
    },
    setup() {
        const blogData = useblogDataStore();
        const blogAuthors = computed(() => blogData.getAllAuthors)
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

.flex-layout {
    display: flex;
    flex-wrap: nowrap;

    .main-content {
        flex: 1; // Занимает все доступное пространство
        min-width: 0; // Позволяет контенту сжиматься
    }

    .main-sidebar {
        flex: 0 0 auto; // Не растягивается и не сжимается, размер по контенту
        width: auto;
        min-width: fit-content;
    }
}

// Адаптивность для мобильных устройств
@media screen and (max-width: 991px) {
    .flex-layout {
        flex-direction: column;
    }
}
</style>
