<template>
    <transition name="modal"
                appear>
        <div v-if="visibleModal"
             class="modal__overlay modal__overlay--zoom"
             @click.stop.prevent="closeModal()">
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
                                               placeholder="Поиск..." />
                                    </div>
                                    <transition name="search-results"
                                                appear>
                                        <div class="search-results">
                                            <transition-group name="result-item"
                                                              tag="div">
                                                <div class="search-result-block"
                                                     v-for="(item, index) in plug"
                                                     :key="index">
                                                    <div class="search-result-block__section-title">{{ item.section }}
                                                    </div>
                                                    <div class="search-result-block-info"
                                                         v-for="(item, index) in item.content"
                                                         :key="index">
                                                        <div class="search-result-block-info__image-wrapper">
                                                            <img class="search-result-block-info__image"
                                                                 v-if="item.image"
                                                                 :src="item.image"
                                                                 alt="изображение из поиска" />
                                                            <SearchRedirectIcon class="search-result-block-info__image"
                                                                                v-else />
                                                        </div>
                                                        <div class="search-result-block-info__title">{{ item.name }}
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
import { defineComponent, ref, watch } from "vue";
import SearchIcon from "@/assets/icons/layout/SearchIcon.svg?component"
import SearchRedirectIcon from "@/assets/icons/layout/SearchRedirectIcon.svg?component"

export default defineComponent({
    props: {
        visibleModal: {
            type: Boolean,
            default: false
        }
    },
    components: {
        SearchIcon,
        SearchRedirectIcon
    },
    setup(props, { emit }) {
        const inputFocus = ref(false);
        watch((props), (newVal) => {
            if (newVal.visibleModal) {
                inputFocus.value = true;
            }
        })

        return {
            closeModal: () => emit('closeSearchModal'),
            plug: [
                {
                    section: 'Пользователи',
                    content: [
                        { name: "ТИТЛ", href: "/", section: "ТИТЛ СЕКЦИИ НАЙДЕННОГО", image: "https://portal.emk.ru/upload/resize_cache/disk/22f/357_204_2/vq9bw8bit78o5ga7xqxamigqc76xoy53.jpg" },
                        { name: "ТИТЛ", href: "/", section: "ТИТЛ СЕКЦИИ НАЙДЕННОГО", image: "https://portal.emk.ru/upload/resize_cache/disk/22f/357_204_2/vq9bw8bit78o5ga7xqxamigqc76xoy53.jpg" }
                    ]
                },
                {
                    section: 'Контент',
                    content: [
                        { name: "ТИТЛ", href: "/", section: "ТИТЛ СЕКЦИИ НАЙДЕННОГО", image: "https://portal.emk.ru/upload/resize_cache/disk/22f/357_204_2/vq9bw8bit78o5ga7xqxamigqc76xoy53.jpg" },
                        { name: "ТИТЛ", href: "/", section: "ТИТЛ СЕКЦИИ НАЙДЕННОГО" }
                    ]
                }
            ],
            inputFocus
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
    transform: translateX(-30px);
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
</style>
