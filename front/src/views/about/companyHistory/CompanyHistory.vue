<template>
<div class="row flex-nowrap book-pages__wrapper mt20">
    <div class="col-sm-3 book-pages">
        <SideBarNavigation :id="Number(currentPage)" />
    </div>
    <div class="col-sm-9 book-content"
         v-if="Object.keys(pages).length">
        <Transition name="fade"
                    mode="out-in">
            <div class="book-content__inner"
                 :key="currentPage">
                <component :is="pages[Number(currentPage)]"></component>
            </div>
        </Transition>
        <div class="book-content__navDiv">
            <a class="book-content__navDiv__arrowBackward"
               :class="{ hidden: Number(currentPage) == 0 }"
               @click="navigate(Number(currentPage) - 1)"> <i class="fa-solid fa-arrow-left"></i> Назад</a>
            <a class="book-content__navDiv__arrowForward"
               :class="{ hidden: Number(currentPage) == 20 }"
               @click="navigate(Number(currentPage) + 1)">Вперед <i class="fa-solid fa-arrow-right"></i></a>
        </div>
    </div>
</div>
</template>

<script lang="ts">
import SideBarNavigation from "./components/SideBarNavigation.vue";
import { defineAsyncComponent, defineComponent, ref, shallowRef, watch } from "vue";
import { useRouter } from "vue-router";

interface PagesRecord {
    [key: number]: unknown;
}

export default defineComponent({
    components: { SideBarNavigation },
    props: {
        id: {
            type: String,
            required: false,
            default: '0',
        },
    },

    setup(props) {
        const router = useRouter();

        const currentPage = ref(props.id ?? 0);
        const pages = shallowRef<PagesRecord>({});

        for (let index = 0; index < 21; index++) {
            pages.value[index] = defineAsyncComponent(() => import(`./components/chapters/Chapter-${index}.vue`));
        }

        const navigate = (page: number) => {
            router.push({ name: "book-emk-page", params: { id: page } });
            window.scrollTo(0, 0);
        };

        watch((props), (newVal) => {
            if (!newVal.id) return;
            currentPage.value = props.id;
        }, { deep: true, immediate: true })

        return {
            navigate,
            pages,
            currentPage,
        };
    },
});
</script>
