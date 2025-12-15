<template>
<header class="header sticky-top d-print-none">
    <nav class="navbar navbar-light navbar-expand-lg">
        <div class="w-100">
            <div class="container-fluid">
                <div class="row">
                    <div class="col-4 col-md-5 d-lg-none d-flex align-items-center justify-content-sm-start">
                        <button class="navbar-toggler"
                                type="button"
                                @click="toggleMobileMenu">
                            <span class="navbar-toggler-icon"></span>
                        </button>
                    </div>
                    <div class="col-4 col-md-2 col-lg-2 d-flex align-items-center justify-content-center logo">
                        <RouterLink to="/"
                                    class="navbar-brand d-block mt-1 mb-1">
                            <div class="d-inline-block header__logo align-top"
                                 alt="ЭМК"
                                 loading="ЭМК"
                                 title="Энергомашкомплект"></div>
                        </RouterLink>
                    </div>

                    <div class="order-3 order-lg-2 d-flex col-lg-8 align-items-center justify-content-center nav-menu">
                        <div class="navbar-collapse collapse"
                             :class="{ 'show': isMobileMenuOpen && isMobileScreen }">
                            <ul class="navbar-nav m-auto">
                                <li class="nav-item dropdown"
                                    @mouseleave="handleDropdown('close', point.id)"
                                    :class="[{ 'dropdown--opened': point.id == activeDrop || isMobileScreen },
                                    { 'dropdown--mobile': isMobileScreen }]"
                                    v-for="point in mainMenuPoints"
                                    :key="'point' + point.id">
                                    <div class="nav-link nav-link--main-points dropdown-toggle"
                                         :to="{ name: point.href }"
                                         @mouseenter="handleDropdown('open', point.id)">
                                        {{ point.name }}
                                    </div>
                                    <ul class="dropdown-menu"
                                        @mouseleave="handleDropdown('close', point.id)">
                                        <div v-for="subpoint in point.subPoints"
                                             :key="'subpoint' + point.name + subpoint.id">
                                            <li v-if="subpoint.name == 'Информационное письмо'"
                                                class="dropdown__item">
                                                <a :href=subpoint.href
                                                   download>{{ subpoint.name }}</a>
                                            </li>
                                            <li v-else
                                                class="dropdown__item"
                                                :class="{ 'dropdown__item--active': currentRoute == subpoint.href }"
                                                @click="handleDropDownItemClick(subpoint)">
                                                {{ subpoint.name }}
                                            </li>
                                        </div>
                                    </ul>
                                </li>
                                <div>
                                    <SearchIcon class="navbar-nav__search-icon"
                                                @click="visibleSearchModal = true" />
                                </div>
                                <SearchModal :visibleModal=visibleSearchModal
                                             @closeSearchModal="visibleSearchModal = false" />
                                <LayoutHeaderModeChanger />
                            </ul>
                        </div>
                    </div>

                    <div
                         class="order-2 order-lg-3 col-4 col-md-5 col-lg-2 mt-3 mb-4 mt-md-0 mb-md-0 d-flex align-items-center justify-content-end header__right-top">

                        <div class="header__user"
                             v-if="userFio && userAvatar"
                             @click="visibleSidebar = true">
                            <div v-if="featureFlags.pointsSystem"
                                 class="header__points-balance__wrapper">
                                <div class="header__points-balance"
                                     title="Ваши баллы"
                                     @click.stop.prevent="pointsModalIsOpen = true">
                                    {{ userScore }}
                                </div>
                            </div>
                            <div class="header__user__block">
                                <img class="header__user__block__img"
                                     :src="userAvatar"
                                     alt="Ваша фотография" />
                                <div class="header__user__block__title d-none d-lg-flex">
                                    <span class="header__user__block__name">
                                        {{ userFio }}
                                    </span>
                                </div>
                            </div>
                        </div>
                        <div @click="visibleSidebar = true"
                             v-else>
                            ...
                        </div>
                        <SlotModal v-if="pointsModalIsOpen == true && featureFlags.pointsSystem"
                                   @close="pointsModalIsOpen = false">
                            <LayoutHeaderPointsModal />
                        </SlotModal>
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
import { mainMenuPoints } from "@/assets/static/navLinks";
import type { ISubPoint } from "@/interfaces/ILayout";
import { usePageDataStore } from "@/stores/pageData";
import { useRoute, useRouter } from "vue-router";
import SidebarLk from "./TopRightSidebar.vue";
import SearchIcon from "@/assets/icons/layout/SearchIcon.svg?component";
import SearchModal from "@/components/tools/modal/SearchModal/SearchModal.vue";
import { useUserData } from "@/stores/userData";
import { useWindowSize } from '@vueuse/core'
import { screenCheck } from "@/utils/screenCheck";
import { useUserScore } from "@/stores/userScoreData";
import SlotModal from "../tools/modal/SlotModal.vue";
import LayoutHeaderPointsModal from "./LayoutHeaderPointsModal.vue";

import { featureFlags } from "@/assets/static/featureFlags";
import LayoutHeaderModeChanger from "./LayoutHeaderModeChanger.vue";

export default defineComponent({
    components: {
        SidebarLk,
        SearchIcon,
        SearchModal,
        SlotModal,
        LayoutHeaderPointsModal,
        LayoutHeaderModeChanger
    },
    setup() {
        const userData = useUserData();
        const pageDataStore = usePageDataStore();
        const route = useRoute();
        const visibleSidebar = ref(false);
        const isMobileMenuOpen = ref(false);
        const visibleSearchModal = ref(false);
        const router = useRouter();
        const activeDrop = ref<null | number>(null);
        const { width } = useWindowSize();
        const pointsModalIsOpen = ref(false);

        watch(
            () => route.name,
            (newVal) => {
                if (newVal) {
                    activeDrop.value = null;
                    pageDataStore.setCurrentRoute(String(newVal));
                }
            }
        )

        const handleDropdown = (type: 'open' | 'close', id: number) => {
            return type == 'open' ? activeDrop.value = id : activeDrop.value = null
        };

        const handleDropDownItemClick = (point: ISubPoint) => {
            activeDrop.value = null;

            router.push({
                name: point.href,
            })
                .then(() => isMobileMenuOpen.value = false);
        };

        return {
            mainMenuPoints,
            activeDrop,
            visibleSidebar,
            visibleSearchModal,
            isMobileMenuOpen,
            pointsModalIsOpen,
            userScore: computed(() => useUserScore().getCurrentScore),
            userAvatar: computed(() => userData.getPhoto),
            userFio: computed(() => userData.getFio),
            currentRoute: computed(() => pageDataStore.getCurrentRoute),
            isMobileScreen: computed(() => ['sm', 'md'].includes(screenCheck(width))),
            featureFlags,
            handleDropdown,
            handleDropDownItemClick,
            toggleMobileMenu: () => isMobileMenuOpen.value = !isMobileMenuOpen.value,
        };
    },
});
</script>