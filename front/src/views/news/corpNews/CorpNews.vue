<template>
<LayoutNewsPreview :id="id"
                   :tagId="tagId"
                   :needTags="false"
                   :pageTitle="pageTitle"
                   :storeItemsName="storeItemsName"
                   :sectionId="Number(sectionId)"
                   :type="'interview'"
                   :routeTo="'corpNewsArticle'" />
</template>
<script lang="ts">
import { sectionTips } from '@/assets/static/sectionTips';
import { defineComponent } from 'vue';
import LayoutNewsPreview from '@/components/layout/LayoutNewsPreview.vue';
import type { DataState } from '@/stores/viewsData';

export default defineComponent({
    components: {
        LayoutNewsPreview,
    },
    props: {
        id: {
            type: Number
        },
        tagId: {
            type: String
        }
    },
    setup() {

        return {
            pageTitle: 'Новости организационного развития',
            sectionId: sectionTips['НовостиОргРазвития'],
            storeItemsName: 'corpNewsData' as keyof DataState
        };
    },
});
</script>
