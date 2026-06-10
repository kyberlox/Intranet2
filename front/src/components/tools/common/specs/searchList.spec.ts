import { describe, it, expect, vi } from 'vitest';
import { mount } from '@vue/test-utils';
import SearchList from '@/components/tools/common/SearchList.vue';
import type { IAreaDepartment } from '@/views/admin/components/inputFields/AdminEditAreaSearch.vue';
import type { IUserList } from '@/components/tools/common/SearchList.vue';

// Мок для иконки Cancel (svg-компонент)
vi.mock('@/assets/icons/common/Cancel.svg?component', () => ({
    default: {
        name: 'Cancel',
        template: '<svg />',
    },
}));

const mockUsers: IUserList[] = [
    { fio: 'Иванов Иван', id: 1, user_id: 1, name: 'Иванов Иван', photo_file_url: '/photo1.jpg', position: 'Инженер' },
    { fio: '', id: 2, user_id: 2, name: 'Петров Пётр', photo_file_url: '', position: 'Менеджер' },
];

const mockDepartments: IAreaDepartment[] = [
    { id: 10, name: 'Отдел разработки' },
    { id: 20, name: 'Отдел кадров' },
];

describe('SearchList.vue', () => {
    describe('Рендеринг', () => {
        it('не рендерит ul, когда searchList пустой или undefined', () => {
            const wrapper = mount(SearchList, { props: { searchList: undefined } });
            expect(wrapper.find('ul').exists()).toBe(false);

            const wrapper2 = mount(SearchList, { props: { searchList: [] } });
            expect(wrapper2.find('ul').exists()).toBe(false);
        });

        it('рендерит список пользователей (type="users")', () => {
            const wrapper = mount(SearchList, {
                props: { searchList: mockUsers, type: 'users' },
            });

            const items = wrapper.findAll('li');
            expect(items).toHaveLength(2);
            expect(items[0].text()).toContain('Иванов Иван');
            expect(items[1].text()).toContain('Петров Пётр');
        });

        it('рендерит список департаментов (type="departments")', () => {
            const wrapper = mount(SearchList, {
                props: { searchList: mockDepartments, type: 'departments' },
            });

            const items = wrapper.findAll('li');
            expect(items).toHaveLength(2);
            expect(items[0].text()).toContain('Отдел разработки');
            expect(items[1].text()).toContain('Отдел кадров');
        });

        it('показывает аватар, если есть image у пользователя', () => {
            const wrapper = mount(SearchList, {
                props: { searchList: mockUsers, type: 'users' },
            });

            const imgs = wrapper.findAll('img');
            expect(imgs).toHaveLength(1);
            expect(imgs[0].attributes('src')).toBe('/photo1.jpg');
            expect(imgs[0].attributes('alt')).toBe('Иванов Иван');
        });

        it('не показывает аватар, если image отсутствует', () => {
            const wrapper = mount(SearchList, {
                props: { searchList: [mockUsers[1]], type: 'users' },
            });

            expect(wrapper.find('img').exists()).toBe(false);
        });

        it('не показывает кнопку удаления, когда needDeleteButton=false', () => {
            const wrapper = mount(SearchList, {
                props: { searchList: mockUsers, needDeleteButton: false },
            });

            expect(wrapper.find('.visibility-editor__user__remove-btn').exists()).toBe(false);
        });

        it('показывает кнопку удаления, когда needDeleteButton=true', () => {
            const wrapper = mount(SearchList, {
                props: { searchList: mockUsers, needDeleteButton: true },
            });

            expect(wrapper.find('.visibility-editor__user__remove-btn').exists()).toBe(true);
        });
    });

    describe('События (emits)', () => {
        it('emits "pick" с данными пользователя при клике на элемент (type="users")', async () => {
            const wrapper = mount(SearchList, {
                props: { searchList: mockUsers, type: 'users' },
            });

            const items = wrapper.findAll('li');
            await items[0].trigger('click');

            const emitted = wrapper.emitted('pick');
            expect(emitted).toHaveLength(1);
            expect(emitted![0][0]).toEqual({
                name: 'Иванов Иван',
                user_position: 'Инженер',
                image: '/photo1.jpg',
                id: 1,
            });
        });

        it('emits "pick" с данными департамента при клике на элемент (type="departments")', async () => {
            const wrapper = mount(SearchList, {
                props: { searchList: mockDepartments, type: 'departments' },
            });

            const items = wrapper.findAll('li');
            await items[1].trigger('click');

            const emitted = wrapper.emitted('pick');
            expect(emitted).toHaveLength(1);
            expect(emitted![0][0]).toEqual({
                name: 'Отдел кадров',
                user_position: '',
                image: '',
                id: 20,
            });
        });

        it('emits "remove" с id элемента при клике на кнопку удаления', async () => {
            const wrapper = mount(SearchList, {
                props: { searchList: mockUsers, needDeleteButton: true },
            });

            const removeBtn = wrapper.find('.visibility-editor__user__remove-btn');
            await removeBtn.trigger('click');

            const emitted = wrapper.emitted('remove');
            expect(emitted).toHaveLength(1);
            expect(emitted![0][0]).toBe(1);
        });

        it('клик на кнопку удаления не вызывает pick', async () => {
            const wrapper = mount(SearchList, {
                props: { searchList: mockUsers, needDeleteButton: true },
            });

            const removeBtn = wrapper.find('.visibility-editor__user__remove-btn');
            await removeBtn.trigger('click');

            expect(wrapper.emitted('pick')).toBeUndefined();
        });
    });

    describe('formatElements (логика форматирования)', () => {
        it('форматирует пользователей: использует fio как name, photo_file_url как image, id как id', () => {
            const wrapper = mount(SearchList, {
                props: { searchList: mockUsers, type: 'users' },
            });

            const items = wrapper.findAll('li');
            expect(items[0].text()).toContain('Иванов Иван');
        });

        it('форматирует пользователей: при пустом fio использует name', () => {
            const wrapper = mount(SearchList, {
                props: { searchList: [mockUsers[1]], type: 'users' },
            });

            const items = wrapper.findAll('li');
            expect(items[0].text()).toContain('Петров Пётр');
        });

        it('форматирует департаменты: name, пустая должность и image', () => {
            const wrapper = mount(SearchList, {
                props: { searchList: mockDepartments, type: 'departments' },
            });

            const items = wrapper.findAll('li');
            expect(items[0].text()).toContain('Отдел разработки');
            expect(wrapper.find('img').exists()).toBe(false);
        });
    });
});