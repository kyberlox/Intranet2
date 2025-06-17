<template>
    <div class="row">
        <div class="col-12 col-sm-12">
            <div class="blog__content mt20">
                <div class="row blog">
                    <h1 class="page__title">{{ interviewInner.name }}</h1>
                    <div class="col-sm-4">
                        <div :style="{ backgroundImage: `url('${interviewInner.image ?? 'https://placehold.co/490x642'}')` }"
                             class="interview__img"></div>
                        <div class="imageCaption">{{ interviewInner.name }}</div>
                        <div class="news-like">
                            <Reactions v-if="interviewInner.reactions"
                                       :reactions="interviewInner.reactions"
                                       :type="'interview'" />
                        </div>
                    </div>
                    <div class="col-sm-8"
                         v-html="interviewInner.content_text">
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>
<script lang="ts">
import Reactions from "@/components/Reactions.vue";
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
});
</script>
