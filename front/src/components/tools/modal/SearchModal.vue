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
                                             v-if="searchResult">
                                            <transition-group name="result-item"
                                                              tag="div">
                                                <div class="search-result-block"
                                                     v-for="(item, index) in searchResult"
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
                                                        <div class="search-result-block-info__text-block">
                                                            <div v-if="contentItem.name"
                                                                 class="search-result-block-info__title"
                                                                 v-html="contentItem.name">
                                                            </div>
                                                            <div v-if="contentItem.coincident">
                                                                <div v-if="contentItem.coincident?.preview_text"
                                                                     class="search-result-block-info__description"
                                                                     v-html="formatHighlight(contentItem.coincident?.preview_text[0])">
                                                                </div>
                                                                <div v-else-if="contentItem.coincident?.content_text"
                                                                     class="search-result-block-info__description"
                                                                     v-html="formatHighlight(contentItem.coincident?.content_text[0])">
                                                                </div>
                                                            </div>
                                                        </div>
                                                    </div>
                                                </div>
                                            </transition-group>
                                        </div>
                                    </transition>
                                </div>
                                <div class="search-footer">
                                    <div class="search-footer-block"
                                         v-for="radio in radioGroup"
                                         :key="'radio' + radio.id">
                                        <label :for="radio.name">{{ radio.title }}</label>
                                        <RadioButton :name="radio.name"
                                                     :checked="radio.value"
                                                     @change="setRadioActive(radio.id)" />
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
import { watchDebounced } from '@vueuse/core'

import SearchIcon from "@/assets/icons/layout/SearchIcon.svg?component"
import SearchRedirectIcon from "@/assets/icons/layout/SearchRedirectIcon.svg?component"
import Api from "@/utils/Api";
import { RadioButton, RadioButtonClasses } from "primevue";

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
        RadioButton
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

        const searchResult: Ref<searchResults[]> = ref([])

        watchDebounced((searchTargetText), (newVal) => {
            if (newVal) {
                const needSearchRoute = needOnlyPeoples.value ? 'full_search_users' : needOnlyContent.value ? 'full_search_art' : 'full_search';
                searchResult.value.length = 0;
                Api.get(`/${needSearchRoute}/${newVal}`)
                    .then((data) => {
                        searchResult.value = data
                    })
            }
        }, { debounce: 500, maxWait: 1500 })

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

        const formatHighlight = (text) => {
            if (!text) return;
            let newFormat = text;
            if (String(text).includes('<b>')) {
                newFormat = text.replaceAll('<b>', '').replaceAll('</b>', '');
            }
            if (newFormat.includes('<em>')) {
                newFormat = newFormat.replaceAll('<em>', '<b>').replaceAll('</em>', '</b>');
            }

            return newFormat;
        }

        const radioGroup = ref([{
            id: 1,
            title: 'По сотрудникам',
            name: 'peopleSearch',
            model: 'needOnlyPeoples',
            value: false
        },
        {
            id: 2,
            title: 'По контенту',
            name: 'contentSearch',
            model: 'needOnlyContent',
            value: false
        },
        {
            id: 3,
            title: 'Общий',
            name: 'fullSearch',
            model: '',
            value: true
        }])

        const setRadioActive = (id) => {
            radioGroup.value.map((e) => {
                e.value = false;
            })
            const target = radioGroup.value.find((e) => { return e.id == id });
            target.value = !target?.value
        }

        return {
            closeModal: () => emit('closeSearchModal'),
            searchResult,
            inputFocus,
            searchTargetText,
            highlightCharacters,
            formatHighlight,
            needOnlyPeoples,
            needOnlyContent,
            radioGroup,
            setRadioActive
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

// _______________________

// Стилизация радиокнопок PrimeVue
.search-footer-block {
    display: flex;
    flex-direction: row-reverse;
    gap: 8px;
    align-items: center;

    label {
        font-size: 14px;
        color: #374151;
        cursor: pointer;
        transition: color 0.2s ease;

        &:hover {
            color: var(--emk-brand-color);
        }
    }

    // Стилизация контейнера радиокнопки
    .p-radiobutton {
        .p-radiobutton-box {
            width: 18px;
            height: 18px;
            border: 2px solid #d1d5db;
            border-radius: 50%;
            background: white;
            transition: all 0.2s ease;
            position: relative;

            &:hover {
                border-color: var(--emk-brand-color);
                box-shadow: 0 0 0 3px rgba(var(--emk-brand-color-rgb), 0.1);
            }

            // Внутренний кружок (когда выбрано)
            .p-radiobutton-icon {
                width: 8px;
                height: 8px;
                border-radius: 50%;
                background: var(--emk-brand-color);
                transform: scale(0);
                transition: transform 0.15s ease;
            }
        }

        // Состояние когда радиокнопка выбрана
        &.p-radiobutton-checked {
            .p-radiobutton-box {
                border-color: var(--emk-brand-color);
                background: white;

                .p-radiobutton-icon {
                    transform: scale(1);
                }
            }
        }

        // Состояние фокуса
        &.p-focus {
            .p-radiobutton-box {
                box-shadow: 0 0 0 3px rgba(var(--emk-brand-color-rgb), 0.2);
            }
        }

        // Состояние при наведении
        &:not(.p-disabled):hover {
            .p-radiobutton-box {
                border-color: var(--emk-brand-color);
            }
        }

        // Отключенное состояние
        &.p-disabled {
            opacity: 0.6;
            cursor: not-allowed;

            .p-radiobutton-box {
                background: #f3f4f6;
                border-color: #d1d5db;
            }
        }
    }
}

// Альтернативный стиль с более современным дизайном
.search-footer-block--modern {
    .p-radiobutton {
        .p-radiobutton-box {
            width: 20px;
            height: 20px;
            border: 2px solid #e5e7eb;
            background: #f9fafb;
            box-shadow: 0 1px 2px rgba(0, 0, 0, 0.05);

            &:hover {
                background: white;
                border-color: var(--emk-brand-color);
                box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
            }

            .p-radiobutton-icon {
                width: 10px;
                height: 10px;
                background: linear-gradient(135deg, var(--emk-brand-color), #3b82f6);
            }
        }

        &.p-radiobutton-checked {
            .p-radiobutton-box {
                background: white;
                border-color: var(--emk-brand-color);
                box-shadow: 0 2px 4px rgba(var(--emk-brand-color-rgb), 0.2);
            }
        }
    }
}

// Дополнительные стили для анимации
@keyframes radioCheck {
    0% {
        transform: scale(0);
        opacity: 0;
    }

    50% {
        transform: scale(1.2);
        opacity: 0.8;
    }

    100% {
        transform: scale(1);
        opacity: 1;
    }
}

.p-radiobutton-checked .p-radiobutton-icon {
    animation: radioCheck 0.2s ease-out;
}
</style>
