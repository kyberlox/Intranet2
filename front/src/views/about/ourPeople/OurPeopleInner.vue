<template>
    <Interview v-if="interviewFromOurPeople"
               :interviewInner="interviewFromOurPeople" />
</template>
<script lang="ts">
import Interview from "@/components/about/ourPeople/Interview.vue";
import { interviewFromOurPeople } from "@/assets/staticJsons/ourPeopleSampleInterview";
import { defineComponent } from "vue";
import type { IInterviewFromOurPeople } from "@/interfaces/IInterviewFromOurPeople";

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
        return {
            interviewFromOurPeople: interviewFromOurPeople.find((item: IInterviewFromOurPeople) => props.id == item.id),
        };
    },
});
</script>
