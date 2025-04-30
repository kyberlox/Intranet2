<template>
    <div v-if="isLogin">
        <LayoutHeader />
        <main>
            <div class="container-fluid"
                 :class="{ 'container-fluid--nopadding': !isLogin }">
                <div class="row"
                     :class="{ 'row--nomargin': !isLogin }">
                    <div :class="{ 'col-12 col-md-12 col-lg-9 col-xl-9 col-xxl-10 main-content': isLogin }">
                        <RouterView />
                    </div>
                    <div v-if="isLogin"
                         class="col-12 col-md-12 col-lg-3 col-xl-3 col-xxl-2 d-print-none">
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
import { defineComponent, onMounted, computed, watch, ref } from "vue";
import { RouterView, useRoute } from "vue-router";
import LayoutHeader from "./components/layout/LayoutHeader.vue";
import Sidebar from "./components/layout/Sidebar.vue";
import AuthPage from "./views/user/AuthPage.vue";
import Api from "./utils/Api";
import { sectionTips } from "./assets/staticJsons/sectionTips";
import { useblogDataStore } from "./stores/blogData";
import { getBlogAuthorsToStore } from "./utils/getBlogAuthorsToStore";
export default defineComponent({
    name: "app-layout",
    components: {
        LayoutHeader,
        Sidebar,
        RouterView,
        AuthPage
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
        return {
            isLogin: true,
        }
    }
})
</script>

<style lang="scss">
@use "./assets/styles/mixins/mixins.scss" as *;

.main-content {
    margin: 0 auto;
    max-width: 1920px;
}

.container-fluid--nopadding {
    padding: 0;
}

.row--nomargin>* {
    margin: 0;
}
</style>
