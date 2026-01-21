<template>
<div class="mt20">
    <div v-if="pageTitle"
         class="page__title">
        {{ pageTitle }}
    </div>
    <PostInner :id="id == undefined ? undefined : String(id)"
               :type="type"
               :previewElement="pageTitle == 'Экскурсии' ? excursions : undefined"
               @pickTag="pickTag" />
</div>
</template>

<script lang="ts">
import { defineComponent } from "vue";
import PostInner from "@/components/tools/common/PostInner.vue";
import { excursions } from "@/assets/static/trainingCenterData";
import { useRouter } from "vue-router";

export default defineComponent({
    name: "PostPreview",
    props: {
        id: {
            type: String,
        },
        pageTitle: {
            type: String,
        },
        type: {
            type: String,
            default: 'default'
        }
    },
    components: {
        PostInner,
    },
    setup(props) {
        const router = useRouter();

        const pickTag = (id: string) => {
            if (props.pageTitle == 'Актуальные новости') {
                router.push({ name: 'actualNewsByTag', params: { tagId: id } })
            } else if (props.pageTitle == 'Видеорепортажи') {
                router.push({ name: 'videoReportsByTag', params: { tagId: id } })
            }
            else if (props.pageTitle == 'Корпоративные события') {
                router.push({ name: 'corpEventsByTag', params: { tagId: id } })
            }
        }
        return {
            excursions,
            pickTag
        }
    }
}
)
</script>