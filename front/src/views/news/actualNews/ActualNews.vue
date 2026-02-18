<template>
<LayoutPostsPreview :tagId="tagId"
                    :needTags="true"
                    :pageTitle="pageTitle"
                    :storeItemsName="storeItemsName"
                    :sectionId="Number(sectionId)"
                    :type="'postPreview'"
                    :routeTo="'actualArticle'" />
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
            pageTitle: 'Актуальные новости',
            sectionId: sectionTips['АктуальныеНовости'],
            storeItemsName: 'actualNewsData' as keyof DataState
        };
    },
});
</script>
