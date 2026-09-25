import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';
import { flushPromises, mount, type VueWrapper } from '@vue/test-utils';
import { createPinia } from 'pinia';
import NotificationBroadcast from '../NotificationBroadcast.vue';
import { useUserData } from '@/stores/userData';
import { featureFlags } from '@/assets/static/featureFlags';
import Api from '@/utils/Api';
import AdminEditUserSearch from '../../components/inputFields/AdminEditUserSearch.vue';
import AdminEditAreaSearch from '../../components/inputFields/AdminEditAreaSearch.vue';

vi.mock('@/utils/Api', () => ({ default: { post: vi.fn() } }));
let wrapper: VueWrapper;
const originalFlag = featureFlags.notificationBroadcast;
beforeEach(() => { vi.resetAllMocks(); featureFlags.notificationBroadcast = true; });
afterEach(() => { wrapper?.unmount(); featureFlags.notificationBroadcast = originalFlag; });

function setup(admin = true) {
    const pinia = createPinia();
    useUserData(pinia).roots.PeerAdmin = admin;
    wrapper = mount(NotificationBroadcast, { global: { plugins: [pinia], stubs: { RouterLink: true, AdminEditUserSearch: true, AdminEditAreaSearch: true } } });
}

function pickUser(id: number) {
    wrapper.getComponent(AdminEditUserSearch).vm.$emit('handleUserPick', id, 'base', { id, name: `Сотрудник ${id}` });
}

function pickDepartment(id: number) {
    wrapper.getComponent(AdminEditAreaSearch).vm.$emit('handleDepartmentPick', id, `Отдел ${id}`);
}

async function fill() {
    await wrapper.get('[name="title"]').setValue('Заголовок');
    await wrapper.get('[name="text"]').setValue('Сообщение');
}

describe('notification broadcast', () => {
    it('sends combined recipients, deduplicates IDs and reports partial delivery', async () => {
        setup();
        await fill();
        pickUser(1); pickUser(2); pickUser(2);
        pickDepartment(96); pickDepartment(208); pickDepartment(96);
        await wrapper.get('[name="payload"]').setValue('{"event_id":42}');
        vi.mocked(Api.post).mockResolvedValue({ status: true, delivered: 3, failed: [2] });
        await wrapper.get('form').trigger('submit');
        await flushPromises();
        expect(Api.post).toHaveBeenCalledWith('users/notifications/broadcast', {
            user_ids: [1, 2], department_ids: [96, 208], all: false,
            type: 'custom', title: 'Заголовок', text: 'Сообщение', payload: { event_id: 42 },
        });
        expect(wrapper.get('[role="status"]').text()).toContain('Доставлено уведомлений: 3');
        expect(wrapper.get('[role="status"]').text()).toContain('ID: 2');
    });

    it('shows selected names, preserves selections when toggling all, and removes recipients', async () => {
        setup();
        await fill();
        pickUser(1);
        pickDepartment(96);
        await wrapper.get('[name="all"]').setValue(true);
        await wrapper.get('[name="all"]').setValue(false);
        expect(wrapper.text()).toContain('Сотрудник 1');
        expect(wrapper.text()).toContain('Отдел 96');
        await wrapper.get('[aria-label="Удалить: Сотрудник 1"]').trigger('click');
        expect(wrapper.text()).not.toContain('Сотрудник 1');
        vi.mocked(Api.post).mockResolvedValue({ status: true, delivered: 1, failed: [] });
        await wrapper.get('form').trigger('submit');
        await flushPromises();
        expect(Api.post).toHaveBeenCalledWith('users/notifications/broadcast', expect.objectContaining({ department_ids: [96] }));
        expect(vi.mocked(Api.post).mock.calls[0][1]).not.toHaveProperty('user_ids');
    });

    it('omits specific recipients when sending to all active users and prevents duplicate submissions', async () => {
        setup();
        await fill();
        pickUser(1);
        await wrapper.get('[name="all"]').setValue(true);
        let resolve!: (value: unknown) => void;
        vi.mocked(Api.post).mockImplementation(() => new Promise(done => { resolve = done; }));
        await wrapper.get('form').trigger('submit');
        await wrapper.get('form').trigger('submit');
        expect(Api.post).toHaveBeenCalledTimes(1);
        expect(Api.post).toHaveBeenCalledWith('users/notifications/broadcast', {
            all: true, type: 'custom', title: 'Заголовок', text: 'Сообщение', payload: {},
        });
        expect(wrapper.get('fieldset').attributes('disabled')).toBeDefined();
        resolve({ status: true, delivered: 20, failed: [] });
        await flushPromises();
        expect(wrapper.get('fieldset').attributes('disabled')).toBeUndefined();
    });

    it.each([
        [0, '{}'], [-1, '{}'], [1.2, '{}'], [1, '[]'], [1, 'null'], [1, '{'],
    ])('rejects invalid recipients or payload (%s, %s)', async (ids, payload) => {
        setup();
        await fill();
        pickUser(ids);
        await wrapper.get('[name="payload"]').setValue(payload);
        await wrapper.get('form').trigger('submit');
        expect(Api.post).not.toHaveBeenCalled();
        expect(wrapper.find('[role="alert"]').exists()).toBe(true);
    });

    it.each([undefined, { status: false, reason: 'no recipients' }])('shows unsuccessful responses without reporting delivery', async response => {
        setup();
        await fill();
        await wrapper.get('[name="all"]').setValue(true);
        vi.mocked(Api.post).mockResolvedValue(response);
        await wrapper.get('form').trigger('submit');
        await flushPromises();
        expect(wrapper.find('[role="alert"]').exists()).toBe(true);
        expect(wrapper.find('[role="status"]').exists()).toBe(false);
    });

    it('hides the form when the feature is disabled', () => {
        featureFlags.notificationBroadcast = false;
        setup();
        expect(wrapper.find('form').exists()).toBe(false);
    });

    it('hides the form from users without PeerAdmin', () => {
        setup(false);
        expect(wrapper.find('form').exists()).toBe(false);
    });
});
