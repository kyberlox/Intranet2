<template>
<p class="admin-element-inner__field-title fs-l">Выберите тэги</p>
<div class="tags">
    <div v-for="tag in allTags"
         :key="tag.id"
         class="tag__wrapper ">
        <div class="tags__tag tags__tag--nohover tags__tag--inner section__item__link btn-air"
             :class="{ 'tags__tag--active': typeof tag.id == 'number' && chosenTags.includes(tag.id) }"
             @click="chooseTag(tag.id)">
            #{{ tag.tag_name }}
        </div>
    </div>
</div>
</template>

<script lang="ts">
import { defineComponent, ref } from "vue";
import type { ITag } from "@/interfaces/entities/ITag";

export default defineComponent({
    props: {
        allTags: {
            type: Array<ITag>
        },
        currentTags: {
            type: Array<number>
        }
    },
    emits: ['tagsChanged'],
    setup(props, { emit }) {
        const chosenTags = ref<number[]>(props.currentTags ? props.currentTags : []);
        const chooseTag = (id: number | string) => {
            if (chosenTags.value.find((e) => e == Number(id))) {
                chosenTags.value = chosenTags.value.filter((e) => e !== id)
            }
            else {
                chosenTags.value.push(Number(id))
            }
            emit('tagsChanged', chosenTags.value)
        }
        return {
            chosenTags,
            chooseTag
        }
    }
})
</script>