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
        onMounted(() => {
            Api.get(`article/find_by_ID/${props.id}`)
                .then((data) => {
                    interviewFromOurPeople.value = data
                })
        })
        return {
            interviewFromOurPeople
        };
    },
});
</script>
