<template>
    <div class="row">
        <div class="col-12 col-sm-12">
            <div class="blog__content mt20">
                <h1 class="page__title">{{ interviewInner.name }}</h1>
                <div class="row blog">
                    <div class="col-sm-4">
                        <div v-if="interviewInner.preview_file_url"
                             :style="{ backgroundImage: `url('${interviewInner.preview_file_url}')` }"
                             class="interview__img"></div>
                        <div class="imageCaption">{{ interviewInner.name }}</div>
                        <div class="news-like">
                            <Reactions v-if="interviewInner.reactions"
                                       :reactions="interviewInner.reactions"
                                       :id="interviewInner.id"
                                       :type="'interview'" />
                        </div>
                    </div>
                    <div class="col-sm-8"
                         v-html="parseMarkdown(interviewInner.content_text).replaceAll('{.answer}', '<hr>').replaceAll('{.question}', '')">
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>
<script lang="ts">
import Reactions from "@/components/tools/common/Reactions.vue";
import { parseMarkdown } from "@/utils/parseMarkdown";
import { defineComponent } from "vue";
export default defineComponent({
    components: {
        Reactions,
    },
    props: {
        interviewInner: {
            type: Object,
            required: true,
        },
    },
    setup() {
        return {
            parseMarkdown
        }
    }
});
</script>
