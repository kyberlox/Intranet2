<template>
    <div class="home__view__grid__card__group-buttons"
         :class="{ 'home__view__grid__card__group--blog': type == 'blog' }">
        <div v-if="type !== 'interview' && type !== 'blog'"
             class="home__view__grid__card__group-buttons__more-button">{{ type == "video" ? "Смотреть" : "Читать далее"
            }}</div>
        <div v-if="reactions"
             class="home__view__grid__card__group-buttons__reaction-buttons">
            <div v-if="reactions.views && (type == 'postPreview' || type == 'blog' || type == 'video' || type == 'interview')"
                 class="home__view__grid__card__group-buttons__reaction-buttons--views">
                <ViewsIcon />
                {{ reactions.views }}
            </div>
            <div v-if="reactions.likes"
                 class="home__view__grid__card__group-buttons__reaction-buttons--like home__view__grid__card__group-buttons__reaction-buttons--like_active">
                <LikeIcon />
                {{ reactions.likes.count }}
            </div>
        </div>
    </div>
</template>

<script lang="ts">
import ViewsIcon from "@/assets/icons/posts/ViewsIcon.svg?component";
import LikeIcon from "@/assets/icons/posts/LikeIcon.svg?component";
import { defineComponent } from "vue";
export default defineComponent({
    components: {
        LikeIcon,
        ViewsIcon,
    },
    props: {
        reactions: {
            type: Object,
            required: true,
        },
        type: {
            type: String,
            required: true,
        },
    },
});
</script>
