<template>
  <SlotModal @close="closeModal">
    <div
      class="modal__text__content modal__text__content--birthday-comments birthday__comments-modal"
    >
      <div class="birthday__comments-modal__header">
        <div class="birthday__comments-modal__title">
          Поздравления для {{ slide.user_fio }}
        </div>
        <div class="birthday__comments-modal__subtitle">
          {{ commentsCount ? `Всего: ${commentsCount}` : "" }}
        </div>
      </div>
      <div class="birthday__comments__list" v-if="commentsCount">
        <div
          class="birthday__comments__item"
          v-for="(congratulation, index) in slide.congratulations"
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
              v-if="canDeleteComment(congratulation)"
              aria-label="Удалить поздравление"
              title="Удалить поздравление"
              :disabled="deletingCommentIndex == index"
              @click="deleteComment(congratulation, index)"
            >
              <span aria-hidden="true">×</span>
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

<script lang="ts">
import { computed, defineComponent, ref, type PropType } from "vue";
import Api from "@/utils/Api";
import SlotModal from "@/components/tools/modal/SlotModal.vue";
import { useUserData } from "@/stores/userData";

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
  name: "BirthdaysModal",
  components: {
    SlotModal,
  },
  props: {
    slide: {
      type: Object as PropType<IBirthdaySlide>,
      required: true,
    },
  },
  emits: ["close", "refresh"],
  setup(props, { emit }) {
    const commentText = ref("");
    const commentError = ref("");
    const isSendingComment = ref(false);
    const deletingCommentIndex = ref<number | null>(null);

    const currentUserId = computed(() => useUserData().getMyId);
    const commentsCount = computed(() => props.slide.congratulations.length);
    const canSendComment = computed(
      () => Boolean(commentText.value.trim()) && !isSendingComment.value
    );

    const responseHasError = (response: unknown) => {
      const responseData = (response as { data?: unknown })?.data ?? response;
      const status = (responseData as { status?: string })?.status;
      return !responseData || status == "error" || status == "warning";
    };

    const canDeleteComment = (congratulation: ICongratulation) => {
      return (
        currentUserId.value == props.slide.id ||
        currentUserId.value == congratulation.user_id
      );
    };

    const closeModal = () => {
      emit("close");
    };

    const sendComment = async () => {
      const comment = commentText.value.trim();
      if (!comment) {
        commentError.value = "Введите текст поздравления";
        return;
      }

      isSendingComment.value = true;
      commentError.value = "";

      try {
        const response = await Api.post(
          "users/create_congratulation",
          {
            celebrant_id: props.slide.id,
            comment,
          } as never
        );

        if (responseHasError(response)) {
          commentError.value = "Не удалось отправить поздравление";
          return;
        }

        commentText.value = "";
        emit("refresh");
      } catch {
        commentError.value = "Не удалось отправить поздравление";
      } finally {
        isSendingComment.value = false;
      }
    };

    const deleteComment = async (
      congratulation: ICongratulation,
      commentIndex: number
    ) => {
      if (!canDeleteComment(congratulation)) return;

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

        if (responseHasError(response)) {
          commentError.value = "Не удалось удалить поздравление";
          return;
        }

        emit("refresh");
      } catch {
        commentError.value = "Не удалось удалить поздравление";
      } finally {
        deletingCommentIndex.value = null;
      }
    };

    return {
      commentText,
      commentError,
      isSendingComment,
      deletingCommentIndex,
      commentsCount,
      canSendComment,
      canDeleteComment,
      closeModal,
      sendComment,
      deleteComment,
    };
  },
});
</script>
