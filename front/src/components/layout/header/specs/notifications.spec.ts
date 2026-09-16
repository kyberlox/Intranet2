import { afterEach, describe, expect, it } from 'vitest';
import { mount, type VueWrapper } from '@vue/test-utils';
import { createPinia } from 'pinia';
import { nextTick } from 'vue';
import LayoutHeaderNotifications from '../LayoutHeaderNotifications.vue';
import { useUserData } from '@/stores/userData';
import type { IUser } from '@/interfaces/entities/IUser';

let wrapper: VueWrapper;
afterEach(() => wrapper?.unmount());

function setup() {
    const pinia = createPinia();
    wrapper = mount(LayoutHeaderNotifications, { global: { plugins: [pinia] }, attachTo: document.body });
    return useUserData(pinia);
}

describe('header notifications', () => {
    it('updates after user loading and clears when the user logs out', async () => {
        const store = setup();
        await wrapper.get('button').trigger('click');
        expect(wrapper.text()).toContain('Уведомлений пока нет');
        store.setUserInfo({ indirect_data: { notifications: [
            { type: 'info', title: 'Новое событие', text: '<b>Сообщение</b>', payload: { id: 42 } },
        ] } } as unknown as IUser);
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
