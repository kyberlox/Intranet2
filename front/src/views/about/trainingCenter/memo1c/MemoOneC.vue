<template>
<h1 class="one-c-memo-title page__title">Инструкция по работе с 1С </h1>
<div class="one-c-memo-container__title">{{ currentNav }}</div>
<div class="one-c-memo-container">

    <div class="one-c-memo-layout">
        <nav class="one-c-memo-sidebar">
            <div class="one-c-memo-nav-item"
                 :class="{ 'one-c-memo-nav-item--active': currentNav === nav }"
                 v-for="(nav, index) in navigation"
                 :key="'nav' + index"
                 @click="showContent(nav)">
                {{ capitalize(nav.toLocaleLowerCase()) }}
            </div>
        </nav>

        <main class="one-c-memo-content">
            <div class="one-c-memo-card"
                 v-for="(item, index) in currentContent"
                 :key="item.id">
                <h5 class="one-c-memo-card__title">{{ currentNav?.toLowerCase() == 'приложение' ?
                    capitalize(item.name.toLowerCase()) : index + 1
                    + '.' }}</h5>

                <div v-if="item.img"
                     class="one-c-memo-card__img__wrapper">
                    <img v-lazy-load="item.img"
                         :alt="item.name"
                         class="one-c-memo-card__img" />
                </div>

                <div class="one-c-memo-card__text"
                     v-html="item.text"></div>
            </div>
        </main>
    </div>
</div>
</template>

<script lang="ts">
import { defineComponent, onMounted, ref } from "vue";
import Api from "@/utils/Api";
import { capitalize } from "vue";

interface IMemo {
    id: number;
    img: string;
    name: string;
    text: string;
}

export default defineComponent({
    setup() {
        const navigation = ref<string[]>([]);
        const memoData = ref();
        const currentContent = ref<IMemo[]>([]);
        const currentNav = ref<string>();

        onMounted(() => {
            Api.get('1c-help/menu_plus')
                .then((data) => {
                    memoData.value = data;
                    navigation.value = Object.keys(data);
                    showContent(navigation.value[0]);
                });
        });

        const showContent = (nav: string) => {
            window.scrollTo({
                top: 0,
                behavior: 'smooth',
            });
            currentNav.value = nav;
            currentContent.value = memoData.value[nav];
        };

        return {
            navigation,
            currentNav,
            currentContent,
            capitalize,
            showContent,
        };
    }
});
</script>