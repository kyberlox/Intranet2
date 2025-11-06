<template>
<transition name="modal"
            appear>
    <div v-if="visibleModal"
         class="modal__overlay modal__overlay--zoom">
        <div class="modal__overlay__close-button"
             @click.stop.prevent="closeModal()"
             type="button">
            <CloseIcon />
        </div>
        <transition name="modal-content"
                    appear>
            <div class="modal__wrapper  modal__wrapper--zoom">
                <div class="modal__body  modal__body--zoom">
                    <div class="search-block__wrapper mt20">
                        <div class="search-block"
                             @click.stop.prevent>
                            <div class="search-wrapper">
                                <div class="search-input">
                                    <Loader v-if="isLoading"
                                            class="search-input__icon__loader" />
                                    <SearchIcon v-else
                                                class="search-input__icon" />
                                    <input :autofocus="true"
                                           placeholder="Поиск..."
                                           v-model="searchTargetText" />
                                </div>
                                <transition name="search-results"
                                            appear>
                                    <SearchResult :searchTargetText="searchTargetText"
                                                  :searchResult="searchResult"
                                                  @closeModal="closeModal()" />
                                </transition>
                            </div>
                            <div class="search-footer">
                                <div class="search-footer-block"
                                     v-for="(point, index) in searchTypes"
                                     :key="'radio' + index"
                                     @click="selectedSearchType = point.value">
                                    <span class="search-footer-block__title"
                                          :class="{ 'search-footer-block__title--active': selectedSearchType == point.value }">
                                        {{ point.title }}
                                    </span>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </transition>
    </div>
</transition>
</template>

<script lang="ts">
import { defineComponent, ref, type Ref, watch } from "vue";
import { watchDebounced } from '@vueuse/core';
import SearchIcon from "@/assets/icons/layout/SearchIcon.svg?component";
import Api from "@/utils/Api";
import CloseIcon from '@/assets/icons/layout/CloseIcon.svg?component';
import SearchResult from "./SearchResult.vue";
import Loader from "@/components/layout/Loader.vue";

interface searchResults {
    section?: string,
    msg?: string,
    content?: {
        name?: string,
        href?: string,
        id?: number,
        image?: string
        coincident?: {
            content_text?: string[],
            preview_text?: string[],
            name?: string[],
        }
    }[],
}

export default defineComponent({
    name: 'SearchModal',
    props: {
        visibleModal: {
            type: Boolean,
            default: false
        }
    },
    components: {
        CloseIcon,
        SearchIcon,
        SearchResult,
        Loader
    },
    setup(props, { emit }) {
        const searchTargetText = ref();
        const selectedSearchType = ref('full_search');
        const searchResult: Ref<searchResults[]> = ref([]);
        const isLoading = ref<boolean>(false);

        watchDebounced((searchTargetText), (newVal) => {
            if (!newVal) {
                searchResult.value.length = 0;
            } else
                getSearchResult();
        }, { debounce: 500, maxWait: 1500 });

        watch((selectedSearchType), (newVal) => {
            if (!newVal || !searchTargetText.value) return;
            getSearchResult();
        }, { deep: true });

        const getSearchResult = () => {
            isLoading.value = true;
            searchResult.value.length = 0;
            Api.get(`/${selectedSearchType.value}/${searchTargetText.value}`)
                .then((data) => {
                    searchResult.value = data
                })
                .finally(() => isLoading.value = false)
        }

        const searchTypes = [
            { value: 'users/search/full_search_users', title: 'По сотрудникам' },
            { value: 'article/search/full_search_art', title: 'По контенту' },
            { value: 'full_search', title: 'Общий' }
        ];

        return {
            searchResult,
            isLoading,
            searchTargetText,
            searchTypes,
            selectedSearchType,
            closeModal: () => emit('closeSearchModal'),
        }
    }
})
</script>