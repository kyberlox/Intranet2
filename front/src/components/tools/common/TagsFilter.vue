<template>
    <div>
        <div class="btn btn-light dropdown-toggle tagDateNavBar__dropdown-toggle"
             @click="tagsVisible = !tagsVisible">
            {{ activeTag?.tag_name ?? 'Теги' }}
        </div>
        <Transition name="slide-down">
            <div v-if="tagsVisible"
                 class=" tags">
                <div v-for="tag in tags"
                     :key="tag.id"
                     class="tag__wrapper ">
                    <div class="tag section__item__link btn-air"
                         @click="setActiveTag(tag)">
                        #{{ tag.tag_name }}
                    </div>
                </div>
            </div>
        </Transition>
    </div>
</template>


<script lang="ts">
import Api from '@/utils/Api';
import { defineComponent, ref, onMounted, type Ref } from 'vue';

interface ITag {
    id: number,
    tag_name: string
}

export default defineComponent({
    setup(props, { emit }) {
        const tags: Ref<ITag[]> = ref([]);
        const tagsVisible = ref(false);
        const activeTag: Ref<ITag | undefined> = ref();


        onMounted(() => {
            Api.get('/tags/get_tags')
                .then((data) => tags.value = data)
        })

        const setActiveTag = (tag: ITag) => {
            activeTag.value = tag;
            emit('pickTag', tag.id)
        }

        return {
            tags,
            tagsVisible,
            activeTag,
            setActiveTag
        }
    }
})
</script>