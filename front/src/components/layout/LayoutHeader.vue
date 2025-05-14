<template>
    <header class="header sticky-top d-print-none">
        <nav class="navbar navbar-light bg-light navbar-expand-lg">
            <div class="w-100">
                <div class="container-fluid">
                    <div class="row">
                        <div class="col-4 col-md-5 d-lg-none d-flex align-items-center justify-content-sm-start">
                            <button class="navbar-toggler"></button>
                        </div>
                        <div class="col-4 col-md-2 col-lg-2 d-flex align-items-center justify-content-center logo">
                            <router-link to="/"
                                         class="navbar-brand d-block mt-1 mb-1">
                                <div class="d-inline-block header__logo align-top"
                                     alt="ЭМК"
                                     loading="ЭМК"
                                     title="Энергомашкомплект"></div>
                            </router-link>
                        </div>

                        <div
                             class="order-3 order-lg-2 d-flex col-lg-8 align-items-center justify-content-center nav-menu">
                            <div class="navbar-collapse collapse"
                                 id="navbarScroll"
                                 style="">
                                <hr class="col-12 col-md-12 d-lg-none mt-4 mt-md-0" />
                                <ul class="navbar-nav m-auto">
                                    <li class="nav-item dropdown"
                                        :class="{ 'dropdown--opened': point.id == activeDrop }"
                                        v-for="point in mainMenuPoints"
                                        :key="'point' + point.id">
                                        <div class="nav-link nav-link--main-points dropdown-toggle"
                                             :to="{ name: point.href }"
                                             @click="openDropdown(point.id)">
                                            {{ point.name }}
                                        </div>
                                        <ul class="dropdown-menu">
                                            <li v-for="subpoint in point.subPoints"
                                                :key="'subpoint' + point.name + subpoint.id"
                                                class="dropdown__item"
                                                :class="{ 'dropdown__item--active': currentRoute == subpoint.href }"
                                                @click="handleDropDownClick(subpoint)">
                                                {{ subpoint.name }}
                                            </li>
                                        </ul>
                                    </li>
                                    <!-- <li onclick="$('#searchBar').slideToggle()" class="nav-item dropdown" id="searchCallButton">
                                        <div class="nav-link dropdown" id="navbarScrollingDropdown" role="button" data-bs-toggle="dropdown" aria-expanded="false" style="">
                                            <i class="fa-solid fa-magnifying-glass" style="font-size: 20px; color: var(--emk-brand-color)"></i>
                                        </div>
                                    </li> -->
                                </ul>
                            </div>
                        </div>

                        <div class="order-2 order-lg-3 col-4 col-md-5 col-lg-2 mt-3 mb-4 mt-md-0 mb-md-0 d-flex align-items-center justify-content-end"
                             @click="visibleSidebar = true">
                            <div class="header__user"
                                 title="Газинский Игорь Владимирович | ">
                                <button class="header__user__button"
                                        type="button">
                                    <img class="header__user__block__img"
                                         src="/src/assets/avatarGI.png" />
                                    <div class="header__user__block__title d-none d-lg-flex">
                                        <span class="header__user__block__name">Газинский Игорь Владимирович</span>
                                    </div>
                                </button>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </nav>
    </header>
    <SidebarLk @closeSidebar="visibleSidebar = false"
               :visibleSidebar="visibleSidebar" />
</template>

<script lang="ts">
import { ref, computed, watch, defineComponent } from "vue";
import { mainMenuPoints } from "@/assets/staticJsons/headerPoints";
import type { ISubPoint } from "@/interfaces/layout";
import { usePageDataStore } from "@/stores/pageData";
import { useRouter } from "vue-router";
import { useRoute } from "vue-router";
import SidebarLk from "./SidebarLk.vue";
export default defineComponent({
    components: {
        SidebarLk
    },
    setup() {
        const pageDataStore = usePageDataStore();
        const route = useRoute();
        const visibleSidebar = ref(false);

        watch(
            () => route.name,
            (newVal) => {
                if (newVal) {
                    activeDrop.value = null;
                    pageDataStore.setCurrentRoute(String(newVal));
                }
            }
        )

        const router = useRouter();
        const activeDrop = ref<null | number>(null);

        const openDropdown = (id: number) => {
            if (id == activeDrop.value) {
                return (activeDrop.value = null);
            }
            activeDrop.value = id;
        };

        const handleDropDownClick = (point: ISubPoint) => {
            activeDrop.value = null;
            if (point.params && point.params.id) {
                router.push({
                    name: point.href,
                    params: { id: point.params.id },
                });
            } else
                router.push({
                    name: point.href,
                });
        };

        return {
            handleDropDownClick,
            mainMenuPoints,
            openDropdown,
            activeDrop,
            currentRoute: computed(() => pageDataStore.getCurrentRoute),
            visibleSidebar
        };
    },
});
</script>