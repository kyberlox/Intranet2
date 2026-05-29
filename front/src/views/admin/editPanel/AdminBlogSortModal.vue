<template>
<SlotModal>
    <div v-if="!isLoading"
         class="blog__sort__wrapper">
        <div v-for="item in sortData?.sort((a, b) => a.user_fio.localeCompare(b.user_fio))"
             :key="item.user_id"
             class="blog__sort">
            <div class="blog__sort__user">
                <img :src="item.user_photo" />
                <div>{{ item.user_fio }}</div>
            </div>
            <div class="blog__sort__input">
                <input class="admin-element-inner__input fs-m"
                       :min="0"
                       v-model="item.sort" />
            </div>
        </div>
        <div class="blog__sort__button__wrapper">
            <button class="blog__sort__button primary-button"
                    @click="handleSortChanged">Сохранить</button>
        </div>
    </div>
    <div class="blog__sort__loader"
         v-else>
        <Loader />
    </div>
</SlotModal>
</template>
<script lang='ts'>
import Loader from '@/components/layout/Loader.vue';
import SlotModal from '@/components/tools/modal/SlotModal.vue';
import Api from '@/utils/Api';
import { defineComponent, onMounted, ref } from 'vue';
import { type ISortItems } from '@/interfaces/IEntities';

export default defineComponent({
    components: {
        SlotModal,
        Loader
    },
    props: {},
    setup(_, { emit }) {
        const sortData = ref<ISortItems[]>([]);
        const isLoading = ref(true);

        onMounted(async () => {
            sortData.value.length = 0;
            try {
                sortData.value = await Api.get('article/sort_and_blogs')
            } catch (error) {
                console.error(error)
            } finally {
                isLoading.value = false
            }
        })


        const findValIn = (uid: number) => {
            return sortData.value?.find(e => e.user_id == uid)?.sort
        }

        const handleSortChanged = async () => {
            try {
                Api.put('article/sort_to_blogs', sortData.value)
            } catch (error) {
                console.error(error)
            } finally {
                emit('close')
            }
        }

        return {
            sortData,
            isLoading,
            handleSortChanged,
            findValIn
        }
    }
});
</script>