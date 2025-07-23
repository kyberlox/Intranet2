<template>
    <div class="admin-panel">
        <div class="admin-panel__sidebar">
            <div class="admin-panel__header">
                <h3 class="admin-panel__title">Панель редактора</h3>
            </div>
            <nav class="admin-panel__nav">
                <h6 class="admin-panel__nav-title">Разделы</h6>
                <ul class="admin-panel__nav-list">
                    <li v-for="(section, index) in [{ id: 1, name: 'testetestete' }, { id: 1, name: 'testetestete' }, { id: 1, name: 'testetestete' }]"
                        :key="'section' + index"
                        class="admin-panel__nav-item">
                        <RouterLink :to="{ name: 'adminBlockInner', params: { id: section.id } }"
                                    class="admin-panel__nav-link"
                                    active-class="admin-panel__nav-link--active">
                            <div class="admin-panel__nav-icon">
                                <svg fill="#000000"
                                     width="20"
                                     height="20"
                                     viewBox="0 0 32 32"
                                     version="1.1"
                                     xmlns="http://www.w3.org/2000/svg">
                                    <path
                                          d="M30.713 16.090c0.009-0.041 0.014-0.087 0.014-0.135 0-0.004-0-0.008-0-0.011v0.001c-0.006-0.184-0.079-0.35-0.196-0.475l0 0-5-5c-0.136-0.137-0.325-0.222-0.533-0.222-0.415 0-0.751 0.336-0.751 0.751 0 0.208 0.085 0.396 0.221 0.532l3.721 3.72h-20.189c-0.414 0-0.75 0.336-0.75 0.75s0.336 0.75 0.75 0.75v0h20.188l-3.719 3.719c-0.136 0.136-0.22 0.324-0.22 0.531 0 0.415 0.336 0.751 0.751 0.751 0.207 0 0.395-0.084 0.531-0.22l5-5.001c0.025-0.026 0.017-0.064 0.038-0.093 0.040-0.052 0.098-0.088 0.124-0.151 0.013-0.050 0.020-0.108 0.020-0.167 0-0.011-0-0.021-0.001-0.032l0 0.002zM2 1.25c-0.414 0-0.75 0.336-0.75 0.75v0 28c0 0.414 0.336 0.75 0.75 0.75s0.75-0.336 0.75-0.75v0-28c-0-0.414-0.336-0.75-0.75-0.75v0z">
                                    </path>
                                </svg>
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
import { computed, defineComponent, onMounted, ref } from 'vue';
import { useUserData } from '@/stores/userData';
import Api from '@/utils/Api';

export default defineComponent({
    name: 'AdminSideBar',
    setup() {
        const myId = computed(() => useUserData().getMyId)
        const sections = ref();

        onMounted(() => {
            Api.get('section/all')
                .then((res) => {
                    sections.value = res;
                })
        })

        return {
            myId,
            sections
        }
    }
})
</script>

<style scoped>
.admin-panel {
    display: flex;
    min-height: 100vh;
}

.admin-panel__sidebar {
    width: 280px;
    background-color: #f8f9fa;
    border-right: 1px solid #e9ecef;
    border-top: 1px solid #e9ecef;
    padding: 0;
    position: fixed;
    height: 100vh;
    overflow-y: auto;
}

.admin-panel__header {
    padding: 20px;
    border-bottom: 1px solid #e9ecef;
    background-color: #fff;
}

.admin-panel__title {
    margin: 0;
    font-size: 18px;
    font-weight: 600;
    color: #333;
}

.admin-panel__nav {
    padding: 20px 0;
}

.admin-panel__nav-title {
    margin: 0 0 15px 0;
    padding: 0 20px;
    font-size: 14px;
    font-weight: 600;
    color: #6c757d;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}

.admin-panel__nav-list {
    list-style: none;
    margin: 0;
    padding: 0;
}

.admin-panel__nav-item {
    margin: 0;
}

.admin-panel__nav-link {
    display: flex;
    align-items: center;
    padding: 12px 20px;
    color: #495057;
    text-decoration: none;
    transition: all 0.2s ease;
    border-left: 3px solid transparent;
}

.admin-panel__nav-link:hover {
    background-color: #e9ecef;
    color: #007bff;
}

.admin-panel__nav-link--active {
    background-color: #e3f2fd;
    color: #007bff;
    border-left-color: #007bff;
    font-weight: 500;
}

.admin-panel__nav-icon {
    margin-right: 12px;
    width: 20px;
    height: 20px;
    display: flex;
    align-items: center;
    justify-content: center;
    color: inherit;
}

.admin-panel__nav-text {
    font-size: 14px;
    line-height: 1.4;
}

.admin-panel__content {
    flex: 1;
    margin-left: 280px;
    padding: 20px;
    background-color: #fff;
}

@media (max-width: 768px) {
    .admin-panel__sidebar {
        width: 100%;
        position: relative;
        height: auto;
    }

    .admin-panel__content {
        margin-left: 0;
    }
}
</style>
