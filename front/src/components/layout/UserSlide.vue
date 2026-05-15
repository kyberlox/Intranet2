<template>
  <div class="birthday__slide-card">
    <RouterLink
      :to="{ name: 'userPage', params: { id: slide?.id } }"
      class="birthday__slide__grid"
    >
      <div
        class="birthday__slide__image"
        :style="{ backgroundImage: `url('${slide?.image}')` }"
      >
        <BirthdayCake class="birthday__slide__image__icon" v-if="needCakeIcon" />
      </div>
      <div class="birthday__slide__info">
        <div class="birthday__page__slide__title">
          {{ slide?.user_fio }}
        </div>
        <div class="birthday__page__slide__subtitle">
          {{ slide?.position }}
        </div>
        <div
          class="birthday__page__slide__subtitle"
          v-for="(dep, index) in slide?.department"
          :key="'dep' + index"
        >
          {{ dep }}
        </div>
        <div v-if="slide?.location" class="birthday__page__slide__location">
          {{ slide.location }}
        </div>
      </div>
    </RouterLink>
    <template v-if="needComments">
      <div class="birthday__comments-preview" v-if="firstComment">
        <div class="birthday__comments__item birthday__comments__item--preview">
          <RouterLink
            :to="{ name: 'userPage', params: { id: firstComment.user_id } }"
            class="birthday__comments__avatar"
            :style="{ backgroundImage: `url('${firstComment.user_photo}')` }"
          />
          <div class="birthday__comments__body">
            <RouterLink
              :to="{ name: 'userPage', params: { id: firstComment.user_id } }"
              class="birthday__comments__author"
            >
              {{ firstComment.user_fio }}
            </RouterLink>
            <div class="birthday__comments__text">
              {{ firstComment.user_comment }}
            </div>
          </div>
        </div>
      </div>
      <div class="birthday__comments-controls">
        <button
          class="birthday__comments-action"
          type="button"
          @click="openCommentsModal"
        >
          Поздравить
        </button>
        <button
          class="birthday__comments-count"
          type="button"
          title="Открыть поздравления"
          @click="openCommentsModal"
        >
          <CommentIcon class="birthday__comments-count__icon" />
          <span class="birthday__comments-count__value">
            {{ commentsCount }}
          </span>
        </button>
      </div>
      <BirthdaysModal
        v-if="commentsModalOpen && slide"
        :slide="slide"
        @close="commentsModalOpen = false"
        @refresh="refreshComments"
      />
    </template>
  </div>
</template>

<script lang="ts">
import { computed, defineComponent, ref, type PropType } from "vue";
import BirthdaysModal from "@/views/about/birthdays/BirthdaysModal.vue";
import BirthdayCake from "@/assets/icons/birthdayCake.svg?component";
import CommentIcon from "@/assets/icons/commentIcon.svg?component";

interface ICongratulation {
    user_id: number;
    user_fio: string;
    user_comment: string;
    user_photo: string;
}

interface IBirthdaySlide {
  department: string[];
  id: number;
  image: string;
  position: string;
  location: string;
  user_fio: string;
  congratulations: ICongratulation[];
}

export default defineComponent({
  name: "userSlide",
  props: {
    slide: {
      type: Object as PropType<IBirthdaySlide>,
    },
    needCakeIcon: {
      type: Boolean,
      default: () => false,
    },
    needComments: {
      type: Boolean,
      default: () => false,
    },
  },
  components: {
    BirthdaysModal,
    BirthdayCake,
    CommentIcon,
  },
  emits: ["sendComment"],
  setup(props, { emit }) {
    const commentsModalOpen = ref(false);

    const commentsCount = computed(() => props.slide?.congratulations?.length || 0);
    const firstComment = computed(() => props.slide?.congratulations?.[0]);

    const openCommentsModal = () => {
      commentsModalOpen.value = true;
    };

    const refreshComments = () => {
      emit("sendComment");
    };

    return {
      commentsModalOpen,
      commentsCount,
      firstComment,
      openCommentsModal,
      refreshComments,
    };
  },
});
</script>
