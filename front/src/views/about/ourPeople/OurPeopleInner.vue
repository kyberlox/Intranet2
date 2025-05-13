<template>
    <Interview v-if="interviewFromOurPeople"
               :interviewInner="interviewFromOurPeople" />
</template>
<script lang="ts">
import Interview from "@/components/about/ourPeople/Interview.vue";
import { interviewFromOurPeople } from "@/assets/staticJsons/ourPeopleSampleInterview";
import { defineComponent, onMounted, ref } from "vue";
import type { IInterviewFromOurPeople } from "@/interfaces/IInterviewFromOurPeople";
import Api from "@/utils/Api";

export default defineComponent({
    components: {
        Interview,
    },
    props: {
        id: {
            type: Number,
            required: true,
        },
    },
    setup(props) {
        const currentPost = ref();
        onMounted(() => {
            Api.get(`article/find_by_ID/${props.id}`)
                .then((data) => {
                    currentPost.value = data
                })
        })
        return {
            // interviewFromOurPeople: interviewFromOurPeople.find((item: IInterviewFromOurPeople) => props.id == item.id),
            interviewFromOurPeople: currentPost
        };
    },
});
</script>
