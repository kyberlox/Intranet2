<template>
    <transition name="modal"
                appear>
        <div v-if="visibleModal"
             class="modal__overlay modal__overlay--zoom">
            <div class="modal__overlay__close-button"
                 @click.stop.prevent="closeModal()"
                 type="button">
                <svg xmlns="http://www.w3.org/2000/svg"
                     width="30px"
                     height="30px"
                     viewBox="0 0 100 100"
                     version="1.1">

                    <path style="fill:currentColor;stroke:#222222;stroke-width:4;"
                          d="M 20,4 3,21 33,50 3,80 20,97 49,67 79,97 95,80 65,50 95,20 80,4 50,34 z" />
                </svg>
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
                                        <div class="search-results"
                                             v-if="plug">
                                            <transition-group name="result-item"
                                                              tag="div">
                                                <div class="search-result-block"
                                                     v-for="(item, index) in plug"
                                                     :key="index">
                                                    <div v-if="item.content.length"
                                                         class="search-result-block__section-title">{{ item.section }}
                                                    </div>
                                                    <div class="search-result-block-info"
                                                         v-for="(contentItem, index) in item.content"
                                                         :key="index">
                                                        <div class="search-result-block-info__image-wrapper">
                                                            <img class="search-result-block-info__image"
                                                                 v-if="contentItem.image"
                                                                 :src="contentItem.image"
                                                                 alt="изображение из поиска" />
                                                            <SearchRedirectIcon class="search-result-block-info__image"
                                                                                v-else />
                                                        </div>
                                                        <div v-if="contentItem.name"
                                                             class="search-result-block-info__title"
                                                             v-html="highlightCharacters(contentItem.name, searchTargetText)">
                                                        </div>
                                                    </div>
                                                </div>
                                            </transition-group>
                                        </div>
                                    </transition>
                                </div>
                                <div class="search-footer">
                                    <div class="search-footer-block">
                                        <label for="peopleSearch">По сотрудникам</label>
                                        <input type="checkbox"
                                               id="peopleSearch" />
                                    </div>
                                    <div class="search-footer-block">
                                        <label for="contentSearch">По контенту</label>
                                        <input type="checkbox"
                                               id="contentSearch" />
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
import { defineComponent, ref, watch, type Ref } from "vue";
import SearchIcon from "@/assets/icons/layout/SearchIcon.svg?component"
import SearchRedirectIcon from "@/assets/icons/layout/SearchRedirectIcon.svg?component"
import Api from "@/utils/Api";

interface searchResults {
    section: string,
    content: {
        name?: string,
        href?: string,
        section?: string,
        image?: string
    }[]
};

export default defineComponent({
    props: {
        visibleModal: {
            type: Boolean,
            default: false
        }
    },
    components: {
        SearchIcon,
        SearchRedirectIcon,
    },
    setup(props, { emit }) {
        const inputFocus = ref(false);
        const searchTargetText = ref();
        const needOnlyPeoples: Ref<boolean> = ref(false);
        const needOnlyContent: Ref<boolean> = ref(false);

        watch((props), (newVal) => {
            if (newVal.visibleModal) {
                inputFocus.value = true;
            }
        })

        const plug: Ref<searchResults[]> = ref([])

        watch((searchTargetText), (newVal) => {
            if (newVal) {
                Api.get(`/full_search/${newVal}`)
                    .then((data) => {
                        plug.value = data
                    })
            }
        })

        const highlightCharacters = (text: string, searchTerm: string): string => {
            if (!searchTerm || !text) return text;

            const searchLower = searchTerm.toLowerCase();
            const textLower = text.toLowerCase();
            let result = '';
            let searchIndex = 0;

            for (let i = 0; i < text.length; i++) {
                const currentChar = text[i];
                const currentCharLower = textLower[i];

                if (searchIndex < searchLower.length &&
                    currentCharLower === searchLower[searchIndex]) {
                    // Символ совпадает с текущей позицией в поисковом запросе
                    result += `<strong class="search-highlight-sequential">${currentChar}</strong>`;
                    searchIndex++;
                } else {
                    result += currentChar;
                }
            }

            return result;
        };


        return {
            closeModal: () => emit('closeSearchModal'),
            plug,
            inputFocus,
            searchTargetText,
            highlightCharacters
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
.search-results-enter-active,
.search-results-leave-active {
    transition: all 0.4s ease;
}

.search-results-enter-from,
.search-results-leave-to {
    opacity: 0;
    transform: translateY(20px);
}

// Анимация для отдельных элементов результатов
.result-item-enter-active,
.result-item-leave-active {
    transition: all 0.3s ease;
}

.result-item-enter-from,
.result-item-leave-to {
    opacity: 0;
    // transform: translateX(-30px);
}

.result-item-move {
    transition: transform 0.3s ease;
}

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
</style>
