<template>
    <div class="page__title mt20">Новости организационного развития</div>
    <div class="row">
        <div class="news__list">
            <GridGallery :gallery="cardsForCorpNews"
                         :type="'postPreview'" />
        </div>
    </div>
</template>
<script lang="ts">
import GridGallery from "@/components/tools/gallery/GridGallery.vue";
import { mainPageCards } from "@/assets/staticJsons/mainPage";
import { defineComponent } from "vue";

export default defineComponent({
    components: {
        GridGallery
    },
    setup() {
        const cardsForCorpNews = [
            {
                id: 1,
                title: 'В Краснодарском крае введена в эксплуатацию ТЭС «Ударная»',
                description: 'В Краснодарском крае введена в эксплуатацию ТЭС «Ударная»',
                image: 'https://portal.emk.ru/upload/resize_cache/iblock/897/gry7fcbpqktpb9jorq1di2sxcftvi7ql/360_206_2/referer-a-friend.jpg',
                reactions: {
                    views: 123,
                    likes: {
                        count: 12,
                        mine: false,
                    }
                },
                href: 'home',
            },
            {
                id: 2,
                title: 'В Краснодарском крае введена в эксплуатацию ТЭС «Ударная»',
                description: 'В Краснодарском крае введена в эксплуатацию ТЭС «Ударная»',
                image: 'https://portal.emk.ru/upload/resize_cache/iblock/897/gry7fcbpqktpb9jorq1di2sxcftvi7ql/360_206_2/referer-a-friend.jpg',
                reactions: {
                    views: 123,
                    likes: {
                        count: 12,
                        mine: false,
                    }
                },
                href: 'home',
            },
            {
                id: 3,
                title: 'В Краснодарском крае введена в эксплуатацию ТЭС «Ударная»',
                description: 'В Краснодарском крае введена в эксплуатацию ТЭС «Ударная»',
                image: 'https://portal.emk.ru/upload/resize_cache/iblock/897/gry7fcbpqktpb9jorq1di2sxcftvi7ql/360_206_2/referer-a-friend.jpg',
                reactions: {
                    views: 123,
                    likes: {
                        count: 12,
                        mine: false,
                    }
                },
                href: 'home',
            },
            {
                id: 4,
                title: 'В Краснодарском крае введена в эксплуатацию ТЭС «Ударная»',
                description: 'В Краснодарском крае введена в эксплуатацию ТЭС «Ударная»',
                image: 'https://portal.emk.ru/upload/resize_cache/iblock/897/gry7fcbpqktpb9jorq1di2sxcftvi7ql/360_206_2/referer-a-friend.jpg',
                reactions: {
                    views: 123,
                    likes: {
                        count: 12,
                        mine: false,
                    }
                },
                href: 'home',
            },
            {
                id: 4,
                title: 'В Краснодарском крае введена в эксплуатацию ТЭС «Ударная»',
                description: 'В Краснодарском крае введена в эксплуатацию ТЭС «Ударная»',
                image: 'https://portal.emk.ru/upload/resize_cache/iblock/897/gry7fcbpqktpb9jorq1di2sxcftvi7ql/360_206_2/referer-a-friend.jpg',
                reactions: {
                    views: 123,
                    likes: {
                        count: 12,
                        mine: false,
                    }
                },
                href: 'home',
            },
        ]
        return {
            cardsForCorpNews
        };
    },
});
</script>