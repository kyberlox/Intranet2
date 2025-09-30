<template>
<div class="mt20">
    <h2 class="page__title">Есть идея! (Мои идеи)</h2>
    <div class="row mb-5">
        <div class="col">
            <RouterLink :to="{ name: 'newIdeaPage' }"
                        class="btn btn-primary"
                        title="Отправить новую идею!">Предложить идею</RouterLink>
        </div>
    </div>
    <div class="row mb-5">
        <table class="table"
               v-if="ideas">
            <tbody>
                <tr>
                    <th>№</th>
                    <th>Дата</th>
                    <th>Название</th>
                    <th>Статус</th>
                </tr>
                <tr v-for="idea in ideas.sort((a, b) => Number(b.number) - Number(a.number))"
                    :key="idea.id"
                    class="idea__table"
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
import type { IIdeaData } from '@/interfaces/IEntities';

export default defineComponent({
    name: 'MyIdeas',
    components: {
        SlotModal,
        MyIdeaModalInner
    },
    setup() {
        const currentUser = computed(() => useUserData().getUser)

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
        })

        return {
            ideas,
            modalIsVisible,
            ideaInModal,
            callModal,
            currentUser
        };
    },
}); 
</script>