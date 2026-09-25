<template>
    <section class="notification-broadcast">
        <RouterLink :to="{ name: 'admin' }">← Панель редактора</RouterLink>
        <h1 class="mt-3">Рассылка уведомлений</h1>
        <form v-if="canBroadcast" @submit.prevent="send">
            <fieldset :disabled="isSending">
                <legend>Получатели</legend>
                <label class="notification-broadcast__checkbox">
                    <input v-model="all" type="checkbox" name="all" /> Всем активным сотрудникам
                </label>
                <template v-if="!all">
                    <div v-for="group in recipientGroups" :key="group.kind" class="notification-broadcast__recipients">
                        <h2 class="fs-5">{{ group.title }}</h2>
                        <template v-if="!isSending">
                            <AdminEditUserSearch v-if="group.kind === 'users'" @handleUserPick="addUser" />
                            <AdminEditAreaSearch v-else multiple @handleDepartmentPick="addDepartment" />
                        </template>
                        <ul class="list-unstyled mt-2">
                            <li v-for="recipient in group.items" :key="recipient.id" class="notification-broadcast__recipient">
                                <span>{{ recipient.name }}</span>
                                <button type="button" class="btn btn-sm btn-outline-secondary"
                                    :aria-label="`Удалить: ${recipient.name}`"
                                    @click="removeRecipient(group.kind, recipient.id)">Удалить</button>
                            </li>
                        </ul>
                    </div>
                    <p class="text-muted">Можно выбрать сотрудников и подразделения одновременно.</p>
                </template>
                <p v-else>Уведомление будет отправлено всем активным сотрудникам.</p>
                <label>Заголовок
                    <input v-model="title" class="form-control" name="title" required />
                </label>
                <label>Текст уведомления
                    <textarea v-model="text" class="form-control" name="text" rows="5" required></textarea>
                </label>
                <details>
                    <summary>Дополнительные параметры</summary>
                    <label>Тип уведомления
                        <input v-model="type" class="form-control" name="type" required />
                    </label>
                    <label>Дополнительные данные (JSON-объект)
                        <textarea v-model="payload" class="form-control" name="payload" rows="4" spellcheck="false"></textarea>
                    </label>
                </details>
                <button class="primary-button mt-3" type="submit">
                    {{ isSending ? 'Отправка…' : 'Отправить уведомление' }}
                </button>
            </fieldset>
            <p v-if="error" class="mt-3 text-danger" role="alert">{{ error }}</p>
            <div v-if="result" class="mt-3" role="status">
                <p>Доставлено уведомлений: {{ result.delivered }}.</p>
                <p v-if="result.failed.length">Не удалось доставить сотрудникам с ID: {{ result.failed.join(', ') }}.</p>
            </div>
        </form>
        <p v-else>Рассылка уведомлений недоступна.</p>
    </section>
</template>

<script lang="ts">
import { computed, defineComponent, ref } from 'vue';
import { featureFlags } from '@/assets/static/featureFlags';
import { useUserData } from '@/stores/userData';
import Api from '@/utils/Api';
import type { INotificationBroadcast } from '@/interfaces/IPostFetch';
import type { IUserSearch } from '@/interfaces/IEntities';
import AdminEditUserSearch from '../components/inputFields/AdminEditUserSearch.vue';
import AdminEditAreaSearch from '../components/inputFields/AdminEditAreaSearch.vue';

type Recipient = { id: number; name: string };

export default defineComponent({
    components: { AdminEditUserSearch, AdminEditAreaSearch },
    setup() {
        const userData = useUserData();
        const canBroadcast = computed(() => featureFlags.notificationBroadcast && userData.getUserRoots.PeerAdmin);
        const all = ref(false);
        const users = ref<Recipient[]>([]);
        const departments = ref<Recipient[]>([]);
        const recipientGroups = computed(() => [
            { kind: 'users' as const, title: 'Сотрудники', items: users.value },
            { kind: 'departments' as const, title: 'Подразделения', items: departments.value },
        ]);
        const title = ref('');
        const text = ref('');
        const type = ref('custom');
        const payload = ref('{}');
        const isSending = ref(false);
        const error = ref('');
        const result = ref<{ delivered: number; failed: number[] } | null>(null);

        function addRecipient(list: Recipient[], id: number, name: string) {
            if (isSending.value || !Number.isSafeInteger(Number(id)) || Number(id) <= 0) return;
            if (!list.some(item => item.id === Number(id))) list.push({ id: Number(id), name });
        }

        function addUser(id: number, _field: string, user: IUserSearch) {
            addRecipient(users.value, id, user.name);
        }

        function addDepartment(id: number, name: string) {
            addRecipient(departments.value, id, name);
        }

        function removeRecipient(kind: 'users' | 'departments', id: number) {
            if (isSending.value) return;
            const list = kind === 'users' ? users : departments;
            list.value = list.value.filter(item => item.id !== id);
        }

        async function send() {
            if (!canBroadcast.value || isSending.value) return;
            error.value = '';
            result.value = null;
            let body: INotificationBroadcast;
            try {
                const userIds = all.value ? [] : users.value.map(item => item.id);
                const departmentIds = all.value ? [] : departments.value.map(item => item.id);
                if (!all.value && !userIds.length && !departmentIds.length) throw new Error('Укажите получателей уведомления.');
                if (!title.value.trim() || !text.value.trim() || !type.value.trim()) throw new Error('Заполните заголовок, текст и тип уведомления.');
                let parsedPayload: unknown;
                try { parsedPayload = JSON.parse(payload.value); }
                catch { throw new Error('Дополнительные данные должны быть корректным JSON-объектом.'); }
                if (!parsedPayload || typeof parsedPayload !== 'object' || Array.isArray(parsedPayload)) {
                    throw new Error('Дополнительные данные должны быть JSON-объектом.');
                }
                body = {
                    all: all.value,
                    ...(userIds.length ? { user_ids: userIds } : {}),
                    ...(departmentIds.length ? { department_ids: departmentIds } : {}),
                    type: type.value.trim(), title: title.value.trim(), text: text.value.trim(),
                    payload: parsedPayload as Record<string, unknown>,
                };
            } catch (e) {
                error.value = (e as Error).message;
                return;
            }
            isSending.value = true;
            try {
                const response = await Api.post('users/notifications/broadcast', body);
                if (response?.status !== true) {
                    error.value = response?.reason === 'no recipients'
                        ? 'Получатели не найдены. Проверьте выбранных сотрудников и подразделения.'
                        : 'Не удалось отправить уведомления. Проверьте результат перед повторной отправкой.';
                    return;
                }
                result.value = { delivered: response.delivered, failed: response.failed ?? [] };
            } catch {
                error.value = 'Не удалось отправить уведомления. Проверьте результат перед повторной отправкой.';
            } finally {
                isSending.value = false;
            }
        }

        return { canBroadcast, all, recipientGroups, addUser, addDepartment, removeRecipient,
            title, text, type, payload, isSending, error, result, send };
    },
});
</script>

<style scoped>
.notification-broadcast { max-width: 760px; margin: 0 auto; padding: 24px; }
fieldset { min-width: 0; }
label { display: block; margin: 16px 0; }
.notification-broadcast__checkbox { display: flex; align-items: center; gap: 8px; }
summary { cursor: pointer; }
.notification-broadcast__recipients { margin: 20px 0; }
.notification-broadcast__recipient { display: flex; align-items: center; justify-content: space-between; gap: 12px; margin: 8px 0; }
button:disabled { opacity: 0.6; cursor: wait; }
</style>
