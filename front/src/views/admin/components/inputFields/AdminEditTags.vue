<template>
<p class="admin-element-inner__field-title fs-l">
    {{ tagsTitle }}
</p>
<div class="primary-button"
     :class="{ 'primary-button--active': chosenTags?.includes('1') }"
     v-if="needAllButton"
     @click="chooseTag(1)">
    Общий доступ
</div>
<div class="tags"
     v-if="!chosenTags.includes('1')">
    <div v-for="tag in allTags?.filter(e => (typeof e !== 'string' && needAllButton) ? e.id !== '1' : true)"
         :key="typeof tag !== 'string' ? tag.id : tag"
         class="tag__wrapper ">
        <div class="tags__tag tags__tag--nohover tags__tag--inner section__item__link btn-air"
             :class="{
                'tags__tag--active': chosenTags.includes(typeof tag !== 'object' ? tag as string : String((tag as ITag).id))
            }"
             @click="chooseTag(typeof tag == 'string' ? tag : tag.id)">
            #{{ typeof tag == 'string' ? tag : tag.tag_name || tag.vision_name }}
        </div>
    </div>
</div>
</template>

<script lang="ts">
import { defineComponent, ref, watch } from "vue";
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
        },
        needAllButton: {
            type: Boolean,
            default: false
        }
    },
    emits: ['tagsChanged'],
    setup(props, { emit }) {
        const chosenTags = ref<(string | number)[]>([]);

        watch((props), () => {
            if (props.currentTags)
                chosenTags.value = props.currentTags;
            emit('tagsChanged', chosenTags.value)
        }, { immediate: true, deep: true })

        const chooseTag = (id: number | string) => {
            if (chosenTags.value.includes('1') && id == '1') {
                chosenTags.value = chosenTags.value.filter(e => e == '1')
            }
            else if (!chosenTags.value.includes('1') && id == '1') {
                chosenTags.value = chosenTags.value.filter(e => e !== '1')
            }
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