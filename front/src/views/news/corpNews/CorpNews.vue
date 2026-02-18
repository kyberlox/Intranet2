<template>
<LayoutPostsPreview :tagId="tagId"
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
import LayoutPostsPreview from '@/components/layout/LayoutPostsPreview.vue';
import type { DataState } from '@/stores/viewsData';

export default defineComponent({
    components: {
        LayoutPostsPreview,
    },
    props: {
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
