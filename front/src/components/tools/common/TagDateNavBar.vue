<template>
    <div class="row">
        <div class="col-12">
            <div class="tagDateNavBar__dropdown">
                <div class="dropdown-wrapper tagDateNavBar__dropdown-wrapper">
                    <button @click="showparams = !showparams"
                            class="btn btn-light dropdown-toggle tagDateNavBar__dropdown-toggle">
                        {{ buttonText ?? 'Год публикации' }}
                    </button>
                    <transition name="fade">
                        <ul class="dropdown__menu tagDateNavBar__dropdown__menu"
                            v-if="showparams && params">
                            <li class="dropdown__item-wrapper tagDateNavBar__dropdown__item-wrapper"
                                v-for="(param, index) in params"
                                :key="index"
                                @click="pickFilter(param)">
                                <div class="dropdown__item tagDateNavBar__dropdown__item">{{ param }}</div>
                            </li>
                        </ul>
                    </transition>
                </div>
            </div>
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
        buttonText: String
    },
    emits: ['pickFilter'],
    setup(props, { emit }) {
        const showparams = ref();

        const pickFilter = (param) => {
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