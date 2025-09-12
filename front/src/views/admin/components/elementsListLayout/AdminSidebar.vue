<template>
    <div class="admin-panel">
        <div class="admin-panel__sidebar"
             v-if="fullNavigation[0].nav.length">
            <div v-if="needDefaultNav"
                 class="admin-panel__header">
                <h3 class="admin-panel__title">Панель редактора</h3>
            </div>

            <nav v-for="(item, index) in fullNavigation"
                 :key="'nav' + index"
                 class="admin-panel__nav">
                <h6 class="admin-panel__nav-title">{{ item.title }}</h6>
                <ul v-if="item.nav.length"
                    class="admin-panel__nav-list">
                    <li v-for="(section, index) in item.nav"
                        :key="'section' + index"
                        class="admin-panel__nav-item">
                        <RouterLink :to="defineRoute(item.id, section)"
                                    class="admin-panel__nav-link"
                                    active-class="admin-panel__nav-link--active">
                            <div class="admin-panel__nav-icon">
                                <NavArrow />
                            </div>
                            <span class="admin-panel__nav-text">{{ section.name }}</span>
                        </RouterLink>
                    </li>
                </ul>
                <!-- <nav class="admin-panel__nav"
                 v-if="needDefaultNav">
                <h6 class="admin-panel__nav-title">Разделы</h6>
                <ul class="admin-panel__nav-list">
                    <li v-for="(section, index) in sections"
                        :key="'section' + index"
                        class="admin-panel__nav-item">
                        <RouterLink :to="{ name: 'adminBlockInner', params: { id: section.id } }"
                                    class="admin-panel__nav-link"
                                    active-class="admin-panel__nav-link--active">
                            <div class="admin-panel__nav-icon">
                                <NavArrow />
                            </div>
                            <span class="admin-panel__nav-text">{{ section.name }}</span>
                        </RouterLink>
                    </li>
                </ul>
               <h6 class="admin-panel__nav-title mt20">Администрирование</h6>
                <ul class="admin-panel__nav-list">
                    <li v-for="(adminSection, index) in AdminSections"
                        :key="'section' + index"
                        class="admin-panel__nav-item">
                        <RouterLink :to="{ name: adminSection.link }"
                                    class="admin-panel__nav-link"
                                    active-class="admin-panel__nav-link--active">
                            <div class="admin-panel__nav-icon">
                                <NavArrow />
                            </div>
                            <span class="admin-panel__nav-text">{{ adminSection.name }}</span>
                        </RouterLink>
                    </li>
                </ul>
                <h6 class="admin-panel__nav-title mt20">Бальная система</h6>
                <ul class="admin-panel__nav-list">
                    <li v-for="(adminSection, index) in PointsSection"
                        :key="'section' + index"
                        class="admin-panel__nav-item">
                        <RouterLink :to="{ name: adminSection.link }"
                                    class="admin-panel__nav-link"
                                    active-class="admin-panel__nav-link--active">
                            <div class="admin-panel__nav-icon">
                                <NavArrow />
                            </div>
                            <span class="admin-panel__nav-text">{{ adminSection.name }}</span>
                        </RouterLink>
                    </li>
                </ul> -->
            </nav>

            <slot>
            </slot>
        </div>
        <div class="admin-panel__content ">
            <!-- <RouterView /> -->
        </div>
    </div>
</template>

<script lang="ts">
import { computed, defineComponent, onMounted, ref } from 'vue';
import { useUserData } from '@/stores/userData';
import { abobus } from '@/assets/static/adminSections';
import Api from '@/utils/Api';
import NavArrow from '@/assets/icons/admin/NavArrow.svg?component'
import { useAdminData } from '@/stores/AdminData';

type AdminSection = {
    name: string;
    id: string | number;
    parent_id?: number;
    sectionHref?: string;
};

type NavGroup = {
    id: number;
    title: string;
    nav: AdminSection[];
};

export default defineComponent({
    name: 'AdminSideBar',
    props: {
        needDefaultNav: {
            type: Boolean,
            default: () => true,
        },
        activeId: {
            type: Number
        }
    },
    emits: ['areaClicked', 'addNewArea', 'deleteArea'],
    components: {
        NavArrow
    },
    setup() {
        const myId = computed(() => useUserData().getMyId);
        const sections = computed(() => useAdminData().getSections);

        const fullNavigation = ref<NavGroup[]>(
            abobus.map((g) => ({
                id: g.id,
                title: g.title,
                nav: [...g.nav] as AdminSection[],
            }))
        );
        onMounted(() => {
            if (sections.value.length) return;
            Api.get(`editor/edit_sections`)
                .then((res) => {
                    useAdminData().setSections(res);
                    fullNavigation.value[0].nav.push(...sections.value);
                })
        })

        const defineRoute = (typeId: number, section: { id: number, name: string }) => {
            if (typeId == 1) {
                return {
                    name: 'adminBlockInner', params: { id: section.id }
                }
            }
            else
                return {
                    name: section.id
                }
        }

        return {
            myId,
            sections,
            fullNavigation,
            defineRoute
        }
    }
})
</script>
