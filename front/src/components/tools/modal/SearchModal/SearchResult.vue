<template>
    <div class="search-results"
         v-if="searchResult">
        <transition-group name="result-item"
                          tag="div">
            <div class="search-result-block"
                 v-for="(item, index) in searchResult"
                 :key="index">
                <div v-if="item?.content?.length"
                     class="search-result-block__section-title">
                    {{ item.section }}
                </div>
                <span>{{ item.msg }}</span>
                <RouterLink class="search-result-block-info"
                            v-for="(contentItem, index) in item.content"
                            :key="index"
                            :to="handleSearchRoute(contentItem)">
                    <div class="search-result-block-info__image-wrapper">
                        <img class="search-result-block-info__image"
                             v-if="contentItem.image"
                             :src="contentItem.image"
                             alt="изображение из поиска" />
                        <SearchRedirectIcon class="search-result-block-info__image"
                                            v-else />
                    </div>
                    <div class="search-result-block-info__text-block">
                        <div v-if="contentItem.name && searchTargetText"
                             class="search-result-block-info__title"
                             v-html="highlightCharacters(contentItem.name, searchTargetText)">
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
                </RouterLink>
            </div>
        </transition-group>
    </div>
</template>

<script lang="ts">
import SearchRedirectIcon from "@/assets/icons/layout/SearchRedirectIcon.svg?component";
import { defineComponent } from "vue";

export default defineComponent({
    name: 'SearchResult',
    props: {
        searchResult: {
            type: Object
        },
        searchTargetText: {
            type: String
        }
    },
    components: {
        SearchRedirectIcon
    },
    setup(props, { emit }) {
        const highlightCharacters = (text: string, searchTerm: string): string => {
            if (!searchTerm || !text) return text;

            const escapedSearchTerm = searchTerm.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');

            const regex = new RegExp(`(${escapedSearchTerm})`, 'gi');

            return text.replace(regex, '<strong class="search-highlight-sequential">$1</strong>');
        };

        const formatHighlight = (text: string) => {
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

        const handleSearchRoute = (item) => {
            emit('closeModal')
            return { name: item.href, params: { id: item.id } }
        }

        return {
            highlightCharacters,
            formatHighlight,
            handleSearchRoute
        }
    }
})
</script>