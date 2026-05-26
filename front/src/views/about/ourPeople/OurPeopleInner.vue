<template>
<Interview v-if="interviewFromOurPeople"
           :interviewInner="interviewFromOurPeople" />
</template>
<script lang="ts">
import Interview from "./components/Interview.vue";
import { defineComponent, onMounted, ref } from "vue";
import Api from "@/utils/Api";

export default defineComponent({
    components: {
        Interview,
    },
    props: {
        id: {
            type: String,
            required: true,
        },
    },
    setup(props) {
        const interviewFromOurPeople = ref();
        onMounted(async () => {
            try {
                const data = await Api.get(`article/find_by_ID/${props.id}`)
                interviewFromOurPeople.value = data
            } catch (error) {
                console.error(error)
            }
        })
        return {
            interviewFromOurPeople
        };
    },
});
</script>
