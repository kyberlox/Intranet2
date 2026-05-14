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
      <SlotModal v-if="commentsModalOpen" @close="commentsModalOpen = false">
        <div class="modal__text__content modal__text__content--birthday-comments birthday__comments-modal">
          <div class="birthday__comments-modal__header">
            <div class="birthday__comments-modal__title">
              Поздравления для {{ slide?.user_fio }}
            </div>
            <div class="birthday__comments-modal__subtitle">
              {{ commentsCount ? `Всего: ${commentsCount}` : "Пока нет поздравлений" }}
            </div>
          </div>
          <div class="birthday__comments__list" v-if="commentsCount">
            <div
              class="birthday__comments__item"
              v-for="(congratulation, index) in slide?.congratulations"
              :key="`${congratulation.user_id}-${index}`"
            >
              <RouterLink
                :to="{ name: 'userPage', params: { id: congratulation.user_id } }"
                class="birthday__comments__avatar"
                :style="{ backgroundImage: `url('${congratulation.user_photo}')` }"
              />
              <div class="birthday__comments__body">
                <RouterLink
                  :to="{ name: 'userPage', params: { id: congratulation.user_id } }"
                  class="birthday__comments__author"
                >
                  {{ congratulation.user_fio }}
                </RouterLink>
                <div class="birthday__comments__text">
                  {{ congratulation.user_comment }}
                </div>
                <button
                  class="birthday__comments__delete"
                  type="button"
                  :disabled="deletingCommentIndex == index"
                  @click="deleteComment(congratulation, index)"
                >
                  {{ deletingCommentIndex == index ? "Удаление..." : "Удалить" }}
                </button>
              </div>
            </div>
          </div>
          <div class="birthday__comments__empty" v-else>
            Поздравлений пока нет
          </div>
          <form class="birthday__comments__form" @submit.prevent="sendComment">
            <textarea
              class="birthday__comments__textarea"
              v-model="commentText"
              :disabled="isSendingComment"
              placeholder="Напишите поздравление..."
              rows="3"
            />
            <div class="birthday__comments__actions">
              <span class="birthday__comments__error" v-if="commentError">
                {{ commentError }}
              </span>
              <button
                class="primary-button birthday__comments__submit"
                type="submit"
                :disabled="!canSendComment"
              >
                {{ isSendingComment ? "Отправка..." : "Отправить" }}
              </button>
            </div>
          </form>
        </div>
      </SlotModal>
    </template>
  </div>
</template>

<script lang="ts">
import { computed, defineComponent, ref, type PropType } from "vue";
import Api from "@/utils/Api";
import SlotModal from "@/components/tools/modal/SlotModal.vue";
import { useUserData } from "@/stores/userData";
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
    BirthdayCake,
    CommentIcon,
    SlotModal,
  },
  emits: ["sendComment"],
  setup(props, { emit }) {
    const commentsModalOpen = ref(false);
    const commentText = ref("");
    const commentError = ref("");
    const isSendingComment = ref(false);
    const deletingCommentIndex = ref<number | null>(null);

    const currentUserId = computed(() => useUserData().getMyId);
    const commentsCount = computed(() => props.slide?.congratulations?.length || 0);
    const firstComment = computed(() => props.slide?.congratulations?.[0]);
    const canSendComment = computed(
      () => Boolean(commentText.value.trim()) && !isSendingComment.value
    );

    const canDeleteComment = (congratulation: ICongratulation) => {
      return (
        currentUserId.value == props.slide?.id ||
        currentUserId.value == congratulation.user_id
      );
    };

    const openCommentsModal = () => {
      commentsModalOpen.value = true;
    };

    const sendComment = async () => {
      const comment = commentText.value.trim();
      if (!props.slide?.id || !comment) {
        commentError.value = "Введите текст поздравления";
        return;
      }

      isSendingComment.value = true;
      commentError.value = "";
      //lorem

      try {
        const response = await Api.post(
          "users/create_congratulation",
          {
            celebrant_id: props.slide.id,
            comment,
          } as never
        );
        const status = (response as { status?: string })?.status;

        if (!response || status == "error" || status == "warn") {
          commentError.value = "Не удалось отправить поздравление";
          return;
        }

        commentText.value = "";
        emit("sendComment");
      } catch {
        commentError.value = "Не удалось отправить поздравление";
        return;
      } finally {
        isSendingComment.value = false;
      }
    };

    const deleteComment = async (
      congratulation: ICongratulation,
      commentIndex: number
    ) => {
      if (!props.slide?.id) return;

      deletingCommentIndex.value = commentIndex;
      commentError.value = "";

      try {
        const response = await Api.delete(
          "users/delete_congratulation",
          {
            celeba_id: props.slide.id,
            commentator_id: congratulation.user_id,
            user_comment: congratulation.user_comment,
          } as never
        );

        if (!response || status == "error" || status == "warn") {
          commentError.value = "Не удалось удалить поздравление";
          return;
        }

        emit("sendComment");
      } catch {
        commentError.value = "Не удалось удалить поздравление";
        return;
      } finally {
        deletingCommentIndex.value = null;
      }
    };

    return {
      commentsModalOpen,
      commentText,
      commentError,
      isSendingComment,
      deletingCommentIndex,
      commentsCount,
      firstComment,
      canSendComment,
      canDeleteComment,
      openCommentsModal,
      sendComment,
      deleteComment,
    };
  },
});
</script>
