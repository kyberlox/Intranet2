<template>
<div class="admin-panel">
    <div class="admin-panel__sidebar">
        <div v-if="needDefaultNav"
             class="admin-panel__header">
            <h3 class="admin-panel__title">Панель редактора</h3>
        </div>

        <nav v-for="(item, index) in filterNavigationByFeatureFlags(fullNavigation)"
             :key="'nav' + index"
             class="admin-panel__nav">
            <h6 class="admin-panel__nav-title">
                {{ item.title }}
            </h6>
            <ul v-if="item.nav.length"
                class="admin-panel__nav-list"
                :key="sections.length">
                <li v-for="(section, index) in item.nav"
                    :key="'section' + index"
                    class="admin-panel__nav-item">
                    <RouterLink :to="defineRoute(item.id, section)"
                                class="admin-panel__nav-link"
                                active-class="admin-panel__nav-link--active">
                        <div class="admin-panel__nav-icon">
                            <NavArrow />
                        </div>
                        <span class="admin-panel__nav-text">
                            {{ section.name }}
                        </span>
                    </RouterLink>
                </li>
            </ul>
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
import { computed, defineComponent, ref, watch } from 'vue';
import { useUserData } from '@/stores/userData';
import { staticAdminSections } from '@/assets/static/adminSections';
import Api from '@/utils/Api';
import NavArrow from '@/assets/icons/admin/NavArrow.svg?component'
import { useAdminData } from '@/stores/adminData';
import { featureFlags } from '@/assets/static/featureFlags';

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
        },
        type: {
            type: String
        }
    },
    emits: ['areaClicked', 'addNewArea', 'deleteArea'],
    components: {
        NavArrow
    },
    setup(props) {
        const myId = computed(() => useUserData().getMyId);
        const sections = computed(() => useAdminData().getSections);
        const adminRoot = computed(() => useUserData().getUserRoots.PeerAdmin);

        const baseNavigation = ref<NavGroup[]>(
            staticAdminSections.map((g) => ({
                id: g.id,
                title: g.title,
                nav: [...g.nav] as AdminSection[],
            }))
        );

        // Проверка на наличие настройки прав по gpt в общем списке
        watch((adminRoot), () => {
            if (!adminRoot.value) {
                fullNavigation.value = baseNavigation.value.filter((e) => e.id !== 4)
            }
            else fullNavigation.value = baseNavigation.value
        })

        watch((sections), () => {
            if (!sections.value.length) {
                Api.get(`editor/get_sections_list`)
                    .then((res) => {
                        useAdminData().setSections(res);
                    })
            };
            if (props.needDefaultNav) {
                fullNavigation.value[0].nav.push(...sections.value)

            } else fullNavigation.value = fullNavigation.value.filter((e) => e.id == 0);
        }, { immediate: true, deep: true })

        const defineRoute = (typeId: number, section: { id: string | number, name: string }) => {
            if (typeId == 1) {
                return {
                    name: 'adminBlockInner', params: { id: String(section.id) }
                }
            } else
                return {
                    name: String(section.id)
                }
        }

        const filterNavigationByFeatureFlags = (fullNavigation: NavGroup[]) => {
            return fullNavigation.filter((e: NavGroup) => (featureFlags.visibleArea == (e.title == 'Администрирование')) && (featureFlags.pointsSystem == (e.title == 'Бальная система')))
        }

        return {
            myId,
            sections,
            fullNavigation,
            defineRoute,
            filterNavigationByFeatureFlags
        }
    }
})
</script>
