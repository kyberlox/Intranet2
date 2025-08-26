<template>
    <div class="admin-element-inner__preview"
         :class="{ 'admin-element-inner__preview--full-width': previewFullWidth || isMobileScreen }">
        <Transition name="layout-change"
                    mode="out-in">
            <LayoutTop v-if="previewFullWidth && !isMobileScreen"
                       class="admin-element-inner__layout-toggle admin-element-inner__layout-toggle--zoom"
                       @click="$emit('changePreviewWidth')" />
            <LayoutLeft v-else-if="!isMobileScreen"
                        class="admin-element-inner__layout-toggle admin-element-inner__layout-toggle--zoom"
                        @click="$emit('changePreviewWidth')" />
        </Transition>

        <PostInner v-if="newFileData && activeType == 'news'"
                   class="admin-element-inner__preview-content mt30"
                   :previewElement="newData"
                   :type="'adminPreview'" />
        <Interview v-if="activeType == 'interview'"
                   class="admin-element-inner__preview-content"
                   :interviewInner="currentItem" />
        <CertainBlog v-if="activeType == 'blogs'"
                     class="admin-element-inner__preview-content"
                     :interviewInner="currentItem"
                     :id="String(15238)"
                     :authorId="String(157)" />
    </div>
</template>

<script lang="ts">
import { defineComponent, onMounted, type PropType } from 'vue';
import PostInner from '@/components/tools/common/PostInner.vue';
import Interview from '@/views/about/ourPeople/components/Interview.vue';
import CertainBlog from '@/views/about/blogs/CertainBlog.vue';
import type { IPostInner } from '@/components/tools/common/PostInner.vue';
import type { newFileData } from '@/interfaces/entities/IAdmin';
import LayoutLeft from "@/assets/icons/admin/LayoutLeft.svg?component";
import LayoutTop from "@/assets/icons/admin/LayoutTop.svg?component";

export default defineComponent({
    name: 'adminPostPreview',
    props: {
        previewFullWidth: {
            type: Boolean
        },
        isMobileScreen: {
            type: Boolean
        },
        newFileData: {
            type: Object as PropType<newFileData>
        },
        newData: {
            type: Object as PropType<IPostInner>
        },
        activeType: {
            type: String as PropType<'noPreview' | 'news' | 'interview' | 'blogs'>
        },
        currentItem: {
            type: Object as PropType<IPostInner>
        }
    },
    components: {
        PostInner,
        Interview,
        CertainBlog,
        LayoutLeft,
        LayoutTop
    },
    setup(props) {
        onMounted(() => console.log(props))
        return {

        }
    }
})
</script>