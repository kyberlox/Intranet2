<template>
    <div ref="container" class="header-notifications" @keydown.esc.stop="closeAndFocus">
        <button ref="trigger" type="button" class="header-notifications__trigger"
            :aria-label="`Уведомления: ${notifications.length}`" :aria-expanded="isOpen"
            :aria-controls="panelId" @click="isOpen = !isOpen">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor"
                stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
                <path d="M18 8a6 6 0 0 0-12 0c0 7-3 7-3 9h18c0-2-3-2-3-9" />
                <path d="M10 21h4" />
            </svg>
            <span v-if="notifications.length" class="header-notifications__count" aria-hidden="true">
                {{ notifications.length > 99 ? '99+' : notifications.length }}
            </span>
        </button>
        <section v-if="isOpen" :id="panelId" class="header-notifications__panel" aria-label="Уведомления">
            <h2 class="header-notifications__heading">Уведомления</h2>
            <button v-if="notifications.length" type="button" class="header-notifications__action"
                :disabled="isLoading || isDeleting" @click="deleteNotifications()">Удалить все</button>
            <p v-if="error" class="header-notifications__error" role="alert">{{ error }}</p>
            <p v-if="isLoading" class="header-notifications__empty" role="status">Загрузка уведомлений…</p>
            <ul v-if="notifications.length" class="header-notifications__list">
                <li v-for="notification in notifications" :key="notification.id" class="header-notifications__item">
                    <h3 class="header-notifications__title">{{ notification.title }}</h3>
                    <p class="header-notifications__text">{{ notification.text }}</p>
                    <button type="button" class="header-notifications__action"
                        :disabled="isLoading || isDeleting || !notification.id"
                        :aria-label="`Удалить уведомление: ${notification.title}`"
                        @click="deleteNotifications(notification.id)">Удалить</button>
                </li>
            </ul>
            <p v-else-if="!isLoading && !error" class="header-notifications__empty">Уведомлений пока нет</p>
        </section>
    </div>
</template>

<script lang="ts">
import { computed, defineComponent, onMounted, onBeforeUnmount, ref, useId } from 'vue';
import { onClickOutside } from '@vueuse/core';
import { useUserData } from '@/stores/userData';
import Api from '@/utils/Api';

export default defineComponent({
    setup() {
        const userData = useUserData();
        const notifications = computed(() => userData.getNotifications);
        const isOpen = ref(false);
        const container = ref<HTMLElement | null>(null);
        const trigger = ref<HTMLButtonElement | null>(null);
        const panelId = useId();
        const isLoading = ref(true);
        const isDeleting = ref(false);
        const error = ref('');
        const controller = new AbortController();
        const authKey = userData.getAuthKey;
        const isCurrentUser = () => !controller.signal.aborted && userData.getAuthKey === authKey;

        onMounted(async () => {
            try {
                const data = await Api.get('users/notifications', null, controller.signal);
                if (!isCurrentUser()) return;
                if (!Array.isArray(data)) throw new Error('Invalid notifications response');
                userData.setNotifications(data);
            } catch {
                if (isCurrentUser()) error.value = 'Не удалось загрузить уведомления.';
            } finally {
                isLoading.value = false;
            }
        });

        onBeforeUnmount(() => controller.abort());

        async function deleteNotifications(id?: string) {
            if (isLoading.value || isDeleting.value) return;
            isDeleting.value = true;
            error.value = '';
            try {
                const response = await Api.delete(id === undefined
                    ? 'users/notifications'
                    : `users/notifications/${encodeURIComponent(id)}`);
                if (!isCurrentUser()) return;
                if (response.data?.status !== true) throw new Error('Notification deletion failed');
                userData.setNotifications(id === undefined
                    ? []
                    : notifications.value.filter(notification => notification.id !== id));
            } catch {
                if (isCurrentUser()) error.value = 'Не удалось удалить уведомления. Попробуйте ещё раз.';
            } finally {
                isDeleting.value = false;
            }
        }

        onClickOutside(container, () => { isOpen.value = false; });

        function closeAndFocus() {
            isOpen.value = false;
            trigger.value?.focus();
        }

        return { notifications, isOpen, container, trigger, panelId, closeAndFocus,
            isLoading, isDeleting, error, deleteNotifications };
    },
});
</script>

<style scoped lang="scss">
.header-notifications {
    position: relative;
    flex-shrink: 0;

    &__trigger {
        position: relative;
        display: grid;
        place-items: center;
        width: 36px;
        height: 36px;
        padding: 0;
        border: 0;
        border-radius: 8px;
        background: transparent;
        color: var(--bs-body-color, #303030);
        cursor: pointer;

        &:hover, &[aria-expanded='true'] { color: var(--emk-brand-color); }
        &:focus-visible { outline: 2px solid var(--emk-brand-color); }
    }

    &__count {
        position: absolute;
        top: -3px;
        right: -5px;
        min-width: 18px;
        padding: 1px 4px;
        border-radius: 10px;
        background: var(--emk-brand-color);
        color: #fff;
        font-size: 10px;
        line-height: 16px;
    }

    &__panel {
        position: absolute;
        top: calc(100% + 12px);
        right: 0;
        width: 360px;
        max-width: calc(100vw - 24px);
        max-height: min(480px, 70dvh);
        overflow-y: auto;
        background: var(--bs-body-bg, #fff);
        color: var(--bs-body-color, #303030);
        border: 1px solid var(--bs-border-color, #ddd);
        border-radius: 12px;
        box-shadow: 0 8px 24px rgb(0 0 0 / 15%);
        z-index: 1000;
        overflow-wrap: anywhere;

        @media (max-width: 991px) {
            position: fixed;
            top: auto;
            right: 12px;
            margin-top: 12px;
        }
    }

    &__heading { margin: 0; padding: 16px; font-size: 18px; }
    &__action {
        margin: 8px 16px;
        padding: 4px 8px;
        border: 1px solid currentColor;
        border-radius: 6px;
        color: var(--emk-brand-color);
        background: transparent;
        font-size: 13px;
        cursor: pointer;
        &:disabled { opacity: 0.5; cursor: default; }
    }
    &__item &__action { margin: 12px 0 0; }
    &__error { padding: 0 16px; color: var(--bs-danger, #dc3545); font-size: 14px; }
    &__list { list-style: none; padding: 0; margin: 0; }
    &__item { padding: 16px; border-top: 1px solid var(--bs-border-color, #ddd); }
    &__title { margin: 0 0 6px; font-size: 15px; font-weight: 600; }
    &__text { margin: 0; font-size: 14px; white-space: pre-wrap; }
    &__empty { margin: 0; padding: 0 16px 16px; font-size: 14px; }
}
</style>
