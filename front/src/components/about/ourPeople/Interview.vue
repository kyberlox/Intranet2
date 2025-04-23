<template>
    <div class="row">
        <div class="col-12 col-sm-12">
            <div class="blog__content mt20">
                <div class="row blog">
                    <div class="col-sm-4">
                        <div :style="{ backgroundImage: `url('${interviewInner.fullImage}')` }"
                             class="interview__img"></div>
                        <div class="imageCaption">{{ interviewInner.title }}</div>
                        <div class="news-like">
                            <Reactions :reactions="interviewInner.reactions"
                                       :type="'interview'" />
                        </div>
                    </div>
                    <div class="col-sm-8"
                         v-html="interviewInner.innerText"></div>
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
            type: Object || String,
            required: true,
        },
    },
});
</script>
