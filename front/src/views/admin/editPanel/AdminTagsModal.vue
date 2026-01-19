<template>
<SlotModal>
    <div class="tags-modal">
        <div class="tags-modal__header">
            <h2 class="tags-modal__title">
                Управление тегами
            </h2>
        </div>

        <div class="tags-modal__input-section">
            <AdminEditInput class="tags-modal__input"
                            :key="tags.length"
                            placeholder="Введите название тега..."
                            :item="{ value: newTagName }"
                            @pick="(newVal: string) => newTagName = newVal" />
            <div @click="addTag"
                 class="tags-modal__add-btn">
                <AddIcon class="tags-modal__add-icon" />
                <span>Добавить</span>
            </div>
        </div>

        <div class="tags-modal__tags-list"
             v-if="!isLoading">
            <div v-for="tag in tags.sort((a, b) => Number(a.tag_name?.[0] || 0) - Number(b.tag_name?.[0] || 0))"
                 :key="tag.id"
                 class="tags-modal__tag-item">
                <span class="tags-modal__tag-name">{{ tag.tag_name }}</span>
                <div @click="deleteTag(Number(tag.id))"
                     class="tags-modal__remove-btn">
                    <RemoveIcon class="tags-modal__remove-icon" />
                </div>
            </div>

            <div v-if="!tags || tags.length === 0"
                 class="tags-modal__empty-state">
                <p>Теги не добавлены</p>
            </div>
        </div>
        <div v-else
             class="contest__page__loader">
            <Loader />
        </div>
    </div>
</SlotModal>
</template>

<script lang="ts">
import SlotModal from '@/components/tools/modal/SlotModal.vue';
import { defineComponent, onMounted, ref } from 'vue';
import type { ITag } from '@/interfaces/entities/ITag';
import AdminEditInput from '../components/inputFields/AdminEditInput.vue';
import RemoveIcon from '@/assets/icons/admin/RemoveIcon.svg?component';
import AddIcon from '@/assets/icons/admin/PlusIcon.svg?component';
import Api from '@/utils/Api';
import Loader from '@/components/layout/Loader.vue';

export default defineComponent({
    components: {
        SlotModal,
        AdminEditInput,
        Loader,
        AddIcon,
        RemoveIcon
    },

    setup() {
        const tags = ref<ITag[]>([]);
        const isLoading = ref<boolean>(true);
        const newTagName = ref<string>();
        const tagsInit = () => {
            Api.get('tags/get_tags')
                .then((data) => tags.value = data)
                .finally(() => isLoading.value = false)
        }

        const addTag = () => {
            Api.put(`tags/add_tag/${newTagName.value}`)
                .then(() => { tagsInit(); newTagName.value = ''; })
                .finally(() => isLoading.value = false)
        }

        const deleteTag = (id: number) => {
            Api.delete(`tags/delete_tag/${id}`)
                .then(() => tagsInit())
                .finally(() => isLoading.value = false)
        }

        onMounted(() => {
            tagsInit();
        })

        return {
            tags,
            isLoading,
            newTagName,
            addTag,
            deleteTag
        }
    }
})
</script>