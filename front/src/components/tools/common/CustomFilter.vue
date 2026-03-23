<template>
<div class="tagDateNavBar__dropdown">
    <div class="dropdown-wrapper tagDateNavBar__dropdown-wrapper">
        <ul class="dropdown__menu tagDateNavBar__dropdown__menu">
            <li class="dropdown__item-wrapper tagDateNavBar__dropdown__item-wrapper"
                v-for="(param, index) in (modifiers?.includes('nosort') ? newParams : newParams?.sort((a, b) => a.localeCompare(b)))"
                :key="index"
                @click="pickFilter(param)">
                <div class="dropdown__item tagDateNavBar__dropdown__item">
                    {{ param }}
                </div>
            </li>
            <li class="dropdown__item-wrapper tagDateNavBar__dropdown__item-wrapper"
                @click="pickFilter('')">
                <div class="dropdown__item tagDateNavBar__dropdown__item">
                    {{ clearButtonText }}
                </div>
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
        modifiers: Array<string>,
        params: Array<string>,
        buttonText: String,
        needButton: {
            type: Boolean,
            default: () => true
        },
        clearButtonText: {
            type: String,
            default: 'Очистить'
        }
    },
    emits: ['pickFilter'],
    setup(props, { emit }) {
        const showparams = ref();
        const newParams = props.params;

        const pickFilter = (param: string) => {
            emit('pickFilter', param);
            showparams.value = false;
        }

        return {
            tags,
            showparams,
            newParams,
            pickFilter
        }
    }
})
</script>