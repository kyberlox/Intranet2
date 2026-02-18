<template>
<LayoutPostsPreview :pageTitle="pageTitle"
                    :storeItemsName="storeItemsName"
                    :sectionId="Number(sectionId)"
                    :tagId="tagId"
                    :needTags="true"
                    :routeTo="'officialEvent'"
                    :needYears="true"
                    :galleryType="'complex'" />
</template>
<script lang="ts">
import { defineComponent } from 'vue';
import { sectionTips } from '@/assets/static/sectionTips';
import { type DataState } from '@/stores/viewsData';
import LayoutPostsPreview from '@/components/layout/LayoutPostsPreview.vue';

export default defineComponent({
    components: {
        LayoutPostsPreview
    },
    props: {
        tagId: {
            type: String
        },
    },
    setup() {
        return {
            pageTitle: 'Фотоотчеты',
            sectionId: sectionTips['офСобытия'],
            storeItemsName: 'officialEventsData' as keyof DataState
        };
    },
});
</script>