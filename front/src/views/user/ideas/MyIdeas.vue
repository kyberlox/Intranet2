<template>
<div class="mt20">
    <h2 class="page__title">Есть идея! (Мои идеи)</h2>
    <div class="row mb-5">
        <div class="col">
            <div>
                <RouterLink :to="{ name: 'newIdeaPage' }"
                            class="primary-button"
                            title="Отправить новую идею!">Предложить идею</RouterLink>
            </div>
        </div>
    </div>
    <div class="row mb-5 idea__table__wrapper">
        <div class="contest__page__loader"
             v-if="!isLoading">
            <Loader />
        </div>
        <table class="table idea__table"
               v-else-if="ideas">
            <tbody>
                <tr>
                    <th>№</th>
                    <th>Дата</th>
                    <th>Название</th>
                    <th>Статус</th>
                </tr>
                <tr v-for="idea in ideas.sort((a, b) => Number(b.number) - Number(a.number))"
                    :key="idea.id"
                    class="idea__table__tr"
                    @click="callModal(idea)">
                    <td>{{ idea.number }}</td>
                    <td>{{ idea.date_create.split(' ')[0] }}</td>
                    <td> {{ idea.name }} </td>
                    <td>{{ idea.status }}</td>
                </tr>
            </tbody>
        </table>

    </div>
    <SlotModal v-if="modalIsVisible"
               class="idea__modal"
               @close="modalIsVisible = false">
        <MyIdeaModalInner :currentUser="currentUser"
                          :textContent="ideaInModal" />
    </SlotModal>
</div>
</template>
<script lang="ts">
import { defineComponent, onMounted, ref, computed, type Ref } from 'vue';
import Api from '@/utils/Api';
import { sectionTips } from '@/assets/static/sectionTips';
import { useUserData } from '@/stores/userData';
import SlotModal from '@/components/tools/modal/SlotModal.vue';
import MyIdeaModalInner from './MyIdeaModalInner.vue';
import Loader from '@/components/layout/Loader.vue';
import type { IIdeaData } from '@/interfaces/IEntities';

export default defineComponent({
    name: 'MyIdeas',
    components: {
        SlotModal,
        MyIdeaModalInner,
        Loader
    },
    setup() {
        const currentUser = computed(() => useUserData().getUser)
        const isLoading = ref(true);
        const ideas: Ref<IIdeaData[]> = ref([]);
        const ideaInModal = ref();
        const modalIsVisible = ref(false);

        const callModal = (idea: IIdeaData) => {
            ideaInModal.value = idea;
            modalIsVisible.value = true;
        }

        onMounted(() => {
            Api.get(`article/find_by/${sectionTips['ЕстьИдея']}`)
                .then((data) => {
                    ideas.value = data;
                })
                .finally(() => isLoading.value = false)
        })

        return {
            ideas,
            isLoading,
            modalIsVisible,
            ideaInModal,
            callModal,
            currentUser
        };
    },
}); 
</script>