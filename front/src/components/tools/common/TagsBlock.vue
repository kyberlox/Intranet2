<template>
    <div>
        <div class="btn btn-light dropdown-toggle tagDateNavBar__dropdown-toggle"
             @click="tagsVisible = !tagsVisible">
            Теги
        </div>
        <Transition name="slide-down">
            <div v-if="tagsVisible"
                 class="tagDateNavBar__dropdown tags">
                <div v-for="tag in tags"
                     :key="tag.id"
                     class="tag__wrapper ">
                    <div class="tag section__item__link btn-air"
                         @click="$emit('pickTag', tag.id)">
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

interface Tag {
    id: number,
    tag_name: string
}

export default defineComponent({
    setup() {
        const tags: Ref<Tag[]> = ref([]);
        const tagsVisible = ref(false);

        onMounted(() => {
            Api.get('/tags/get_tags')
                .then((data) => tags.value = data)
        })

        return {
            tags,
            tagsVisible,
        }
    }
})
</script>