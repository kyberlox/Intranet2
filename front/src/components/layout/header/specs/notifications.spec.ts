import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';
import { flushPromises, mount, type VueWrapper } from '@vue/test-utils';
import { createPinia } from 'pinia';
import { nextTick } from 'vue';
import LayoutHeaderNotifications from '../LayoutHeaderNotifications.vue';
import { useUserData } from '@/stores/userData';
import type { IUser } from '@/interfaces/entities/IUser';
import Api from '@/utils/Api';

vi.mock('@/utils/Api', () => ({ default: { get: vi.fn(), delete: vi.fn() } }));
const notification = { id: 'notification-1', type: 'info', title: 'Новое событие', text: '<b>Сообщение</b>', payload: { id: 42 } };
beforeEach(() => {
    vi.resetAllMocks();
    vi.mocked(Api.get).mockResolvedValue([]);
});

let wrapper: VueWrapper;
afterEach(() => wrapper?.unmount());

function setup() {
    const pinia = createPinia();
    wrapper = mount(LayoutHeaderNotifications, { global: { plugins: [pinia] }, attachTo: document.body });
    return useUserData(pinia);
}

describe('header notifications', () => {
    it('fetches on mount, ignores stale profile notifications and clears on logout', async () => {
        vi.mocked(Api.get).mockResolvedValue([notification]);
        const store = setup();
        await flushPromises();
        expect(Api.get).toHaveBeenCalledWith('users/notifications', null, expect.any(AbortSignal));
        await wrapper.get('button').trigger('click');
        store.setUserInfo({ indirect_data: { notifications: [] } } as unknown as IUser);
        await nextTick();
        expect(wrapper.get('button').attributes('aria-label')).toBe('Уведомления: 1');
        expect(wrapper.get('li').text()).toContain('Новое событие');
        expect(wrapper.get('li').text()).toContain('<b>Сообщение</b>');
        expect(wrapper.find('b').exists()).toBe(false);
        store.logOut();
        await nextTick();
        expect(wrapper.find('li').exists()).toBe(false);
        expect(wrapper.text()).toContain('Уведомлений пока нет');
    });

    it('deletes one notification and then all notifications after server confirmation', async () => {
        vi.mocked(Api.get).mockResolvedValue([notification, { ...notification, id: 'second' }]);
        vi.mocked(Api.delete).mockResolvedValue({ data: { status: true } } as Awaited<ReturnType<typeof Api.delete>>);
        setup();
        await flushPromises();
        await wrapper.get('button').trigger('click');
        await wrapper.get('li button').trigger('click');
        await flushPromises();
        expect(Api.delete).toHaveBeenLastCalledWith('users/notifications/notification-1');
        expect(wrapper.findAll('li')).toHaveLength(1);
        await wrapper.get('section > button').trigger('click');
        await flushPromises();
        expect(Api.delete).toHaveBeenLastCalledWith('users/notifications');
        expect(wrapper.findAll('li')).toHaveLength(0);
        expect(wrapper.text()).toContain('Уведомлений пока нет');
    });

    it.each([false, 'network'])('keeps notifications when deletion fails: %s', async (failure) => {
        vi.mocked(Api.get).mockResolvedValue([notification]);
        if (failure === 'network') vi.mocked(Api.delete).mockRejectedValue(new Error('offline'));
        else vi.mocked(Api.delete).mockResolvedValue({ data: { status: false } } as Awaited<ReturnType<typeof Api.delete>>);
        setup();
        await flushPromises();
        await wrapper.get('button').trigger('click');
        await wrapper.get('li button').trigger('click');
        await flushPromises();
        expect(wrapper.findAll('li')).toHaveLength(1);
        expect(wrapper.get('[role="alert"]').text()).toContain('Не удалось удалить');
    });

    it('shows a load error when the API helper returns no data', async () => {
        vi.mocked(Api.get).mockResolvedValue(undefined);
        setup();
        await flushPromises();
        await wrapper.get('button').trigger('click');
        expect(wrapper.get('[role="alert"]').text()).toContain('Не удалось загрузить');
        expect(wrapper.text()).not.toContain('Уведомлений пока нет');
    });

    it('toggles and dismisses with Escape or an outside click', async () => {
        setup();
        const button = wrapper.get('button');
        await button.trigger('click');
        expect(wrapper.find('section').exists()).toBe(true);
        await button.trigger('keydown', { key: 'Escape' });
        expect(wrapper.find('section').exists()).toBe(false);
        expect(document.activeElement).toBe(button.element);
        await button.trigger('click');
        await new Promise(resolve => setTimeout(resolve, 0));
        document.body.dispatchEvent(new Event('pointerdown', { bubbles: true }));
        document.body.dispatchEvent(new MouseEvent('click', { bubbles: true }));
        await nextTick();
        expect(wrapper.find('section').exists()).toBe(false);
        expect(button.attributes('aria-expanded')).toBe('false');
    });
});
