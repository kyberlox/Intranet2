<template>
<p class="admin-element-inner__field-title fs-l">
    {{ tagsTitle }}
</p>
<div class="tags">
    <div v-for="tag in allTags"
         :key="typeof tag !== 'string' ? tag.id : tag"
         class="tag__wrapper ">
        <div class="tags__tag tags__tag--nohover tags__tag--inner section__item__link btn-air"
             :class="{
                'tags__tag--active': chosenTags.includes(typeof tag == 'string' ? String(tag) : String((tag as ITag).id))
            }"
             @click="chooseTag(typeof tag == 'string' ? tag : tag.id)">
            #{{ typeof tag == 'string' ? tag : tag.tag_name }}
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
            type: Array<ITag | string>
        },
        currentTags: {
            type: Array<number | string>
        },
        tagsTitle: {
            type: String,
            default: () => 'Выберите тэги'
        }
    },
    emits: ['tagsChanged'],
    setup(props, { emit }) {
        const chosenTags = ref<(string | number)[]>(props.currentTags || []);
        console.log(chosenTags.value);

        const chooseTag = (id: number | string) => {
            if (chosenTags.value.find((e) => e == String(id))) {
                chosenTags.value = chosenTags.value.filter((e) => String(e) !== String(id)).map(e => String(e))
            }
            else {
                chosenTags.value.push(String(id))
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