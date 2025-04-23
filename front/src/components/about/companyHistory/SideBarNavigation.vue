<template>
    <div class="sidebar">
        <div class="sidebar__burger"
             @click="rollSidebar">
            <div class="sidebar__burger__switch-icon"
                 id="burgerMenuOpen">
                <ListSidebar />
            </div>
        </div>
        <ul class="level-1">
            <div class="bookNav__wrapper"
                 v-for="(point, index) in bookNavigation"
                 :key="'bookNav' + index">
                <li class="bookNav__li"
                    :class="{ 'bookNav__li--active': point.href?.params?.id && point.href.params.id == id }"
                    @click="handlePointClick(point?.id)">
                    <RouterLink v-if="point.href"
                                :to="point.href">{{ point.name }}</RouterLink>
                    <span v-else>{{ point.name }}
                        <ListArrowDown />
                    </span>
                </li>
                <ul class="level-2"
                    :class="{ 'level-2--hidden': point.id && !openThisPageBlocks.includes(point.id) }"
                    v-if="point.subpages.length">
                    <li class="bookNav__li"
                        v-for="(subpoint, index) in point.subpages"
                        :key="'bookNavSub' + index"
                        :class="{ 'bookNav__li--active': subpoint.href && subpoint.href.params.id == id }">
                        <RouterLink v-if="subpoint.href"
                                    :to="subpoint.href">{{ subpoint.name }}</RouterLink>
                        <span v-else>{{ subpoint.name }}</span>
                    </li>
                </ul>
            </div>
        </ul>
    </div>
</template>

<script lang="ts">
import { defineComponent, ref, watch } from "vue";
import { RouterLink } from "vue-router";
import ListSidebar from "@/assets/icons/book-emk/ListSidebar.svg?component";
import ListArrowDown from "@/assets/icons/book-emk/arrow-down.svg?component";
import { bookNavigation } from "@/assets/staticJsons/bookNavigation";
import type { SubpageItem, IBook } from "@/interfaces/IBook";

export default defineComponent({
    name: "SideBarNavigation",
    components: {
        RouterLink,
        ListSidebar,
        ListArrowDown,
    },
    props: {
        id: {
            type: Number,
            required: true,
        },
    },
    emits: ["rollSidebar"],
    setup(props, { emit }) {
        const openThisPageBlocks = ref<(number | string)[]>([]);

        watch(
            () => props.id,
            (newId) => {
                if (newId) {
                    openThisPageBlocks.value = [];

                    bookNavigation.forEach((item: IBook) => {
                        if (item.subpages) {
                            item.subpages.forEach((subpage: SubpageItem) => {
                                if (item.id && subpage.href && subpage.href.params.id === props.id) {
                                    openThisPageBlocks.value.push(item.id);
                                }
                            });
                        }
                    });
                }
            },
            { immediate: true }
        );

        const handlePointClick = (id: number | string | undefined) => {
            if (!id) return;
            if (openThisPageBlocks.value.includes(id)) {
                openThisPageBlocks.value = openThisPageBlocks.value.filter((item) => item !== id);
            } else {
                openThisPageBlocks.value.push(id);
            }
        };

        return {
            openThisPageBlocks,
            handlePointClick,
            bookNavigation,
            rollSidebar: () => emit("rollSidebar"),
        };
    },
});
</script>
