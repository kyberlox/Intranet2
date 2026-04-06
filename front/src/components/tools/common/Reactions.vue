<template>
<div class="homeview__grid__card__group-buttons"
     :class="[{ 'homeview__grid__card__group--blog': type == 'blog' }, { 'homeview__grid__card__group-buttons--between': type == 'interview' }]">
    <div v-if="date"
         class="news__detail__date">
        {{ dateConvert(date, 'toStringType') }}
    </div>
    <div v-if="newTypeReaction"
         class="homeview__grid__card__group-buttons__reaction-buttons"
         @mouseleave="usersLikesVisible = false">
        <div v-if="!modifiers.includes('noViews')"
             class="homeview__grid__card__group-buttons__reaction-buttons--views">
            <ViewsIcon />
            {{ newTypeReaction.views }}
        </div>
        <div v-if="newTypeReaction.likes && !modifiers.includes('noLikes')"
             @mouseenter="usersLikesVisible = true"
             @click.stop.prevent="setLike(id)"
             class="homeview__grid__card__group-buttons__reaction-buttons--like"
             :class="{ 'homeview__grid__card__group-buttons__reaction-buttons--like_active': newTypeReaction.likes.likedByMe }">
            <LikeIcon />
            {{ newTypeReaction.likes.count }}
        </div>
        <div v-if="newTypeReaction.likes.users.length && usersLikesVisible"
             class="homeview__grid__card__group-buttons__reaction__likes-list">
            <div @click.stop.prevent="$router.push({ name: 'userPage', params: { id: user.id } })"
                 class="homeview__grid__card__group-buttons__reaction__likes-list__item"
                 v-for="user in newTypeReaction.likes.users"
                 :key="user.id">
                <img class="homeview__grid__card__group-buttons__reaction__likes-list__item__photo"
                     :src=user.photo_file_url />
                <div class="homeview__grid__card__group-buttons__reaction__likes-list__item__name">{{ user.name }}</div>
            </div>
        </div>
    </div>
</div>
</template>

<script lang="ts">
import ViewsIcon from "@/assets/icons/posts/ViewsIcon.svg?component";
import LikeIcon from "@/assets/icons/posts/LikeIcon.svg?component";
import { defineComponent, ref, type Ref, type PropType, onMounted } from "vue";
import Api from "@/utils/Api";
import type { IReaction } from "@/interfaces/IEntities";
import { dateConvert } from "@/utils/dateConvert";

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
            type: String as PropType<'postPreview' | 'blog' | 'video' | 'interview' | 'ourPeople'>,
            required: true,
        },
        needReadMoreBtn: {
            type: Boolean,
            default: false
        },
        modifiers: {
            type: Array<string>,
            default: () => []
        },
        date: {
            type: String
        }
    },
    setup(props) {
        const newTypeReaction: Ref<IReaction> = ref(props.reactions);
        const usersLikesVisible = ref<boolean>(false);

        onMounted(() => {
            Api.get(`article/has_user_liked/${props.id}`)
                .then(data => { newTypeReaction.value = data });
        })

        const setLike = (id: number) => {
            Api.put(`article/add_or_remove_like/${id}`)
                .then((data: IReaction) => {
                    newTypeReaction.value = data;
                })
        }

        return {
            newTypeReaction,
            usersLikesVisible,
            dateConvert,
            setLike,
        }
    }
});
</script>
