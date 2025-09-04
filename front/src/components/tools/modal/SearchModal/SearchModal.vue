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
                <div class="modal__wrapper modal__wrapper--zoom">
                    <div class="modal__body modal__body--zoom">
                        <div class="search-block__wrapper mt20">
                            <div class="search-block"
                                 @click.stop.prevent>
                                <div class="search-wrapper">
                                    <div class="search-input">
                                        <SearchIcon class="navbar-nav__search-icon navbar-nav__search-icon--inModal" />
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
                                              :class="{ 'search-footer-block__title--active': selectedSearchType == point.value }">{{
                                                point.title }}</span>
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
import { watchDebounced } from '@vueuse/core'
import SearchIcon from "@/assets/icons/layout/SearchIcon.svg?component"
import Api from "@/utils/Api";
import CloseIcon from '@/assets/icons/layout/CloseIcon.svg?component'
import SearchResult from "./SearchResult.vue";

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
    },
    setup(props, { emit }) {
        const searchTargetText = ref();
        const selectedSearchType = ref('full_search');
        const searchResult: Ref<searchResults[]> = ref([])

        watchDebounced((searchTargetText), (newVal) => {
            if (!newVal) return;
            getSearchResult();
        }, { debounce: 500, maxWait: 1500 });

        watch((selectedSearchType), (newVal) => {
            if (!newVal || !searchTargetText.value) return;
            getSearchResult();
        }, { deep: true });

        const getSearchResult = () => {
            searchResult.value.length = 0;
            Api.get(`/${selectedSearchType.value}/${searchTargetText.value}`)
                .then((data) => {
                    searchResult.value = data
                })
        }

        const searchTypes = [
            { value: 'users/search/full_search_users', title: 'По сотрудникам' },
            { value: 'article/search/full_search_art', title: 'По контенту' },
            { value: 'full_search', title: 'Общий' }
        ];

        return {
            closeModal: () => emit('closeSearchModal'),
            searchResult,
            searchTargetText,
            searchTypes,
            selectedSearchType
        }
    }
})
</script>

<style lang="scss">
// Анимация для контента модального окна
.modal-content-enter-active,
.modal-content-leave-active {
    transition: all 0.1s cubic-bezier(0.25, 0.8, 0.25, 1);
}

.modal-content-enter-from,
.modal-content-leave-to {
    opacity: 0;
    transform: scale(0.8) translateY(-50px);
}

// Анимация для результатов поиска
// Анимация для отдельных элементов результатов

// Анимация для отдельных элементов результатов
.result-item-enter-active,
.result-item-leave-active {
    transition: all 0.4s cubic-bezier(0.25, 0.8, 0.25, 1);
}

.result-item-enter-from {
    opacity: 0;
    transform: translateY(20px) translateX(-15px);
}

.result-item-leave-to {
    opacity: 0;
    transform: translateY(-20px) translateX(15px);
}

.result-item-move {
    transition: transform 0.3s ease;
}


// .result-item-move {
//     transition: transform 0.3s ease;
// }

.search-block__wrapper {
    min-height: 500px;
    display: flex;
    justify-content: center;
    align-items: center;
}

.search-wrapper {
    padding: 20px;
    width: 100%;
    max-height: 700px;
    overflow-y: scroll;
    max-width: 550px;

}

.modal__wrapper__close-btn {
    position: absolute;
    top: 50px;
    right: 50px;

    &>svg {
        color: red;
        width: 30px;
    }

}

.search-block {
    background: #f5f5f5;
    align-items: center;
    margin: 60px;
    display: flex;
    flex-direction: column;
    border-radius: 10px;
    min-width: 550px;
    transition: box-shadow 0.2s ease;

    &:hover {
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.1);
    }
}

.search-input {
    display: flex;
    flex-direction: row;
    width: 100%;
    padding: 10px;
    border-radius: 5px;
    border: 1px solid var(--emk-brand-color);
    background: white;
    transition: border-color 0.2s ease, box-shadow 0.2s ease;

    &:focus-within {
        border-color: var(--emk-brand-color);
        box-shadow: 0 0 0 3px rgba(var(--emk-brand-color-rgb), 0.1);
    }

    &>input {
        border: none;
        outline: none;
        padding: 5px;
        width: 100%;
        transition: all 0.2s ease;
    }
}

.search-footer {
    align-items: center;
    border-radius: 0 0 8px 8px;
    box-shadow: 0 -1px 0 0 #e0e3e8, 0 -3px 6px 0 rgba(69, 98, 155, .12);
    display: flex;
    flex-shrink: 0;
    height: 44px;
    padding: 0 12px;
    position: relative;
    -webkit-user-select: none;
    user-select: none;
    width: 100%;
    z-index: 300;
    justify-content: flex-start;
    gap: 20px;

    &-block {
        display: flex;
        flex-direction: row;
        gap: 5px;
        align-items: center;
    }
}

.navbar-nav__search-icon--inModal {
    cursor: default !important;
    transition: color 0.2s ease;

    &:hover {
        color: #666 !important;
    }
}

.search-result-block {
    margin-top: 10px;
    font-size: 14px;
}

.search-result-block-info {
    margin-top: 5px;
    display: flex;
    flex-direction: row;
    gap: 20px;
    font-size: 16px;
    background: white;
    padding: 10px;
    border-radius: 5px;
    cursor: pointer;
    box-shadow: 0 1px 3px 0 #d4d9e1;
    align-items: center;
    justify-content: flex-start;
    transition: all 0.2s cubic-bezier(0.25, 0.8, 0.25, 1);

    &:hover {
        color: var(--emk-brand-color);
        box-shadow: 0 4px 12px 0 rgba(var(--emk-brand-color-rgb), 0.2);
        transform: translateY(-2px);
    }
}

.search-result-block-info__image {
    max-width: 120px;
    border-radius: 5px;
    min-width: 50px;
    color: #666;
    transition: transform 0.2s ease;
}

.search-result-block-info:hover .search-result-block-info__image {
    transform: scale(1.05);
}

.search-highlight-char {
    text-decoration: underline;
}

.search-result-block-info__text-block {
    display: flex;
    flex-direction: column;
}

.search-result-block-info__title {
    font-size: 16px;
}

.search-result-block-info__description {
    font-size: 14px;
    margin-top: 5px;

    &>p {
        margin: 0;
        padding: 0;
    }

}

.search-result-block-info__image-wrapper {
    min-width: 120px;
}


.search-footer-block__title {
    cursor: pointer;
    transition: 0.1s all ease-in-out;
    border-bottom: 1px solid white;

    &:hover {
        border-bottom: 1px solid var(--emk-brand-color);
        color: black;
    }

    &--active {
        color: black;
        border-bottom: 1px solid var(--emk-brand-color);
    }
}

.search-highlight-sequential {
    color: #535151fc;
}
</style>