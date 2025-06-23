<template>
    <div class="row">
        <div class="col-12">
            <div class="tagDateNavBar__dropdown">
                <div class="dropdown-wrapper tagDateNavBar__dropdown-wrapper">
                    <button @click="showYears = !showYears"
                            class="btn btn-light dropdown-toggle tagDateNavBar__dropdown-toggle">
                        Год
                        публикации
                    </button>
                    <transition name="fade">
                        <ul class="dropdown__menu tagDateNavBar__dropdown__menu"
                            v-if="showYears && years">
                            <li class="dropdown__item-wrapper tagDateNavBar__dropdown__item-wrapper"
                                v-for="(year, index) in years"
                                :key="index"
                                @click="navToYear(year)">
                                <div class="dropdown__item tagDateNavBar__dropdown__item">{{ year }}</div>
                            </li>
                        </ul>
                    </transition>
                </div>
                <button v-if="modifiers !== 'noTag'"
                        @click="showTags = !showTags"
                        class="btn btn-light dropdown-toggle tagDateNavBar__dropdown-toggle">
                    Теги
                </button>
            </div>
            <transition v-if="modifiers !== 'noTag'"
                        name="fade">
                <div class="tagDateNavBar__tags"
                     v-if="showTags">
                    <div class="tagDateNavBar__tags__tag"
                         @click="navToTag(tag)"
                         v-for="(tag, index) in tags"
                         :key="index">#{{ tag }}</div>
                </div>
            </transition>
        </div>
    </div>
</template>
<script lang="ts">
import { defineComponent, ref } from 'vue';
import { tags } from '@/assets/static/newsTags';

export default defineComponent({
    props: {
        modifiers: String,
        years: Array<string>,
    },
    setup(props, { emit }) {
        const showTags = ref(false);
        const showYears = ref(false);
        const navToTag = (tag: string) => {
            emit('pickTag', tag);
            showTags.value = false;
        }
        const navToYear = (year: string) => {
            emit('pickYear', year);
            showYears.value = false;
        }

        return {
            tags,
            showTags,
            showYears,
            navToTag,
            navToYear
        }
    }
})
</script>