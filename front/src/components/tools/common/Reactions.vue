<template>
    <div class="homeview__grid__card__group-buttons"
         :class="{ 'homeview__grid__card__group--blog': type == 'blog' }">
        <div v-if="type !== 'interview' && type !== 'blog'"
             class="homeview__grid__card__group-buttons__more-button">{{ type == "video" ? "Смотреть" : "Читать далее"
            }}</div>
        <div v-if="newTypeReaction"
             class="homeview__grid__card__group-buttons__reaction-buttons">
            <div v-if="newTypeReaction.views && (type == 'postPreview' || type == 'blog' || type == 'video' || type == 'interview')"
                 class="homeview__grid__card__group-buttons__reaction-buttons--views">
                <ViewsIcon />
                {{ newTypeReaction.views }}
            </div>
            <div v-if="newTypeReaction.likes"
                 @click.stop.prevent="setLike(id)"
                 class="homeview__grid__card__group-buttons__reaction-buttons--like"
                 :class="{ 'homeview__grid__card__group-buttons__reaction-buttons--like_active': newTypeReaction.likes.likedByMe }">
                <LikeIcon />
                {{ newTypeReaction.likes.count }}
            </div>
        </div>
    </div>
</template>


<script lang="ts">
import ViewsIcon from "@/assets/icons/posts/ViewsIcon.svg?component";
import LikeIcon from "@/assets/icons/posts/LikeIcon.svg?component";
import { defineComponent, ref, type Ref, type PropType } from "vue";
import Api from "@/utils/Api";
import type { IReaction } from "@/interfaces/IEntities";

export default defineComponent({
    components: {
        LikeIcon,
        ViewsIcon,
    },
    props: {
        id: {
            type: Number,
            required: true,
        },
        reactions: {
            type: Object as PropType<IReaction>,
            required: true,
        },
        type: {
            type: String,
            required: true,
        },
    },
    setup(props) {
        const newTypeReaction: Ref<IReaction> = ref(props.reactions);

        const setLike = (id: number) => {
            Api.get(`plugtosetlike/${id}`)
                .then((data: IReaction) => {
                    console.log(data);
                    newTypeReaction.value = data
                })
        }

        return {
            setLike,
            newTypeReaction
        }
    }
});
</script>
