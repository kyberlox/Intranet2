<template>
    <div class="admin-panel">
        <div class="admin-panel__sidebar">
            <div v-if="!isVisibilityArea"
                 class="admin-panel__header">
                <h3 class="admin-panel__title">Панель редактора</h3>
            </div>
            <nav class="admin-panel__nav"
                 v-if="!isVisibilityArea">
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
            </nav>
            <nav class="admin-panel__nav"
                 v-else>
                <h6 class="admin-panel__nav-title mt20">Области</h6>
                <ul class="admin-panel__nav-list">
                    <li v-for="(area, index) in visibilityAreas"
                        :key="'section' + index"
                        class="admin-panel__nav-item"
                        @click="$emit('areaClicked', area.id)">
                        <div class="admin-panel__nav-link"
                             :class="{ 'admin-panel__nav-link--active': activeId == area.id }">
                            <div class="admin-panel__nav-icon">
                                <NavArrow />
                            </div>
                            <span class="admin-panel__nav-text">{{ area.vision_name }}</span>
                        </div>
                    </li>
                </ul>
                <button class="admin-panel__nav__button primary-button"
                        @click="$emit('addNewArea')">Добавить</button>
            </nav>
        </div>
        <div class="admin-panel__content ">
            <!-- <RouterView /> -->
        </div>
    </div>
</template>

<script lang="ts">
import { computed, defineComponent, onMounted, ref, type PropType } from 'vue';
import { useUserData } from '@/stores/userData';
import { AdminSections } from '@/assets/static/adminSections';
import Api from '@/utils/Api';
import NavArrow from '@/assets/icons/admin/NavArrow.svg?component'
import { useAdminData } from '@/stores/AdminData';
export default defineComponent({
    name: 'AdminSideBar',
    props: {
        isVisibilityArea: {
            type: Boolean,
            default: () => false,
        },
        visibilityAreas: {
            type: Array as PropType<{ id: number, vision_name: string }[]>
        },
        activeId: {
            type: Number
        }
    },
    emits: ['areaClicked', 'addNewArea'],
    components: {
        NavArrow
    },
    setup() {
        const myId = computed(() => useUserData().getMyId);
        const sections = computed(() => useAdminData().getSections);

        onMounted(() => {
            if (sections.value.length) return;
            Api.get(`editor/edit_sections`)
                .then((res) => {
                    useAdminData().setSections(res);
                })
        })

        return {
            myId,
            sections,
            AdminSections,
        }
    }
})
</script>
