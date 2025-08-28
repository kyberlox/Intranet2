<template>
    <div class="admin-panel">
        <div class="admin-panel__sidebar">
            <div class="admin-panel__header">
                <h3 class="admin-panel__title">Панель редактора</h3>
            </div>
            <nav class="admin-panel__nav">
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
            </nav>
        </div>
        <div class="admin-panel__content">
            <RouterView />
        </div>
    </div>
</template>

<script lang="ts">
import { computed, defineComponent, onMounted } from 'vue';
import { useUserData } from '@/stores/userData';
import Api from '@/utils/Api';
import NavArrow from '@/assets/icons/admin/NavArrow.svg?component'
import { useAdminData } from '@/stores/AdminData';
export default defineComponent({
    name: 'AdminSideBar',
    components: {
        NavArrow
    },
    setup() {
        const myId = computed(() => useUserData().getMyId)
        const sections = computed(() => useAdminData().getSections)

        onMounted(() => {
            if (sections.value.length) return
            Api.get(`editor/edit_sections`)
                .then((res) => {
                    useAdminData().setSections(res)
                })
        })

        return {
            myId,
            sections
        }
    }
})
</script>
