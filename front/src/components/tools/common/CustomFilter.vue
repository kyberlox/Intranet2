<template>
<div class="tagDateNavBar__dropdown">
    <div class="dropdown-wrapper tagDateNavBar__dropdown-wrapper">
        <ul class="dropdown__menu tagDateNavBar__dropdown__menu">
            <li class="dropdown__item-wrapper tagDateNavBar__dropdown__item-wrapper"
                v-for="(param, index) in params"
                :key="index"
                @click="pickFilter(param)">
                <div class="dropdown__item tagDateNavBar__dropdown__item">
                    {{ param }}
                </div>
            </li>
            <li class="dropdown__item-wrapper tagDateNavBar__dropdown__item-wrapper"
                @click="pickFilter('')">
                <div class="dropdown__item tagDateNavBar__dropdown__item">Очистить</div>
            </li>
        </ul>

    </div>
</div>
</template>
<script lang="ts">
import { defineComponent, ref } from 'vue';
import { tags } from '@/assets/static/newsTags';

export default defineComponent({
    props: {
        modifiers: String,
        params: Array<string>,
        buttonText: String,
        needButton: {
            type: Boolean,
            default: () => true
        }
    },
    emits: ['pickFilter'],
    setup(props, { emit }) {
        const showparams = ref();

        const pickFilter = (param: string) => {
            emit('pickFilter', param);
            showparams.value = false;
        }

        return {
            tags,
            showparams,
            pickFilter
        }
    }
})
</script>