<template>
    <div class="page__title mt20">Панель редактора</div>
    <div class="row">
        <h6>Выберите раздел</h6>
        <div class="admin-page__selector">
            <div class="admin-page__section__wrapper">
                <RouterLink v-for="(section, index) in sections"
                            :key="'section' + index"
                            :to="{ name: 'adminBlockInner', params: { id: section.id } }"
                            class="admin-page__section">
                    <span class="admin-page__section-link">
                        <div class="admin-page__section-icon">
                            <img src="https://portal.emk.ru/bitrix/images/lists/nopic_list_150.png"
                                 width="36"
                                 height="30"
                                 alt="" />
                        </div>
                        <span class="admin-page__section-title-wrapper">
                            <span class="admin-page__section-title">{{ section.name }}</span>
                        </span>
                    </span>
                </RouterLink>
            </div>
        </div>
    </div>
</template>

<script lang="ts">
import { computed, defineComponent, onMounted, ref } from 'vue';
import { useUserData } from '@/stores/userData';
import Api from '@/utils/Api';

export default defineComponent({
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