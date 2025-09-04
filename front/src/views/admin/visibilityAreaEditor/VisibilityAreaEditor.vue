<template>
    <div class="visibility-editor__title page__title mt20">Редактор областей видимости</div>
    <div class="visibility-editor__wrapper">
        <AdminSidebar :isVisibilityArea="true"
                      :visibilityAreas="allAreas"
                      :activeId="activeArea"
                      @addNewArea="console.log('addNewArea')"
                      @areaClicked="(i) => changeActiveArea(i)" />
        <div class="visibility-editor__area-users__wrapper">
            <div v-if="activeArea"
                 class="visibility-editor__area-users__edit-methods">
                <button @click="changeEditMode(!editGroupMode)"
                        class="visibility-editor__area-users__edit-methods__add">
                    {{ editGroupMode ? 'Вернуться' : 'Добавить' }}
                </button>
                <!-- <AdminEditInput class="visibility-editor__area-users__edit-methods__search"
                                :item="{ name: '', value: '' }"
                                :placeholder="'Фильтр по фио'" /> -->
            </div>
            <ul v-if="!editGroupMode"
                class="visibility-editor__area-users">
                <li v-for="user in activeAreaUsers"
                    :key="user.id"
                    class="visibility-editor__area-user">
                    <div class="visibility-editor__user-avatar">
                        <img v-if="user.photo"
                             :src="user.photo"
                             :alt="`${user.name} ${user.last_name}`"
                             class="visibility-editor__user-photo">
                    </div>
                    <div class="visibility-editor__user-fio">
                        {{ user.name + ' ' + user.last_name + ' ' + user.second_name }}
                    </div>
                </li>
            </ul>
            <VisibilityAreaEditorTree v-else
                                      @fixUserChoice="fixUserChoice"
                                      :choices="choices"
                                      :departments="allDepStructure" />
        </div>

        <div class="visibility-editor__right-sidebar">
            <table>
                <tbody>
                    <tr v-for="choice in choices"
                        :key="choice.type + choice.id">
                        <td>{{ choice.name }}</td>
                    </tr>
                </tbody>
            </table>
            <div class="visibility-editor__button-group">
                <button @click="saveChoices">Сохранить</button>
                <button @click="clearChoices">Сбросить</button>
            </div>
        </div>
    </div>
</template>

<script lang="ts">
import Api from '@/utils/Api';
import { defineComponent, onMounted, ref, watchEffect } from 'vue';
import AdminSidebar from '@/views/admin/components/elementsListLayout/AdminSidebar.vue';
import AdminEditInput from '../components/inputFields/AdminEditInput.vue';
import VisibilityAreaEditorTree from './components/VisibilityAreaEditorTree.vue';

interface IVisionUser {
    id: number;
    name: string;
    last_name: string;
    second_name: string;
    post: string;
    photo: null | string;
}

export interface IDepartment {
    id: number;
    name: string;
    user_head_id: number;
    father_id: null;
    users: IUserSearch[];
    departments: IDepartment[];
}

export interface IUserSearch {
    department: string;
    department_id: number;
    user_fio: string;
    user_id: number;
    user_position: string;
    photo: null | string;
}

export default defineComponent({
    name: 'VisibilityAreaEditor',
    components: {
        AdminSidebar,
        AdminEditInput,
        VisibilityAreaEditorTree
    },
    setup() {
        const allChiefs = ref<IUserSearch[]>([]);
        const allAreas = ref<{ id: number, vision_name: string }[]>([]);
        const activeArea = ref<number>();
        const activeAreaUsers = ref<IVisionUser[]>();
        const editGroupMode = ref<boolean>(false);
        const allDepStructure = ref();
        const departmentMap = new Map();


        const changeEditMode = (val: boolean) => {
            editGroupMode.value = val;
        }

        const changeActiveArea = (id: number) => {
            activeArea.value = id;
            getVisionUser(id);
        }

        const getAllVisions = () => {
            Api.get(`fields_visions/get_all_visions`)
                .then((data) => { allAreas.value = data })
        }

        const getAllDirectors = () => {
            Api.get(`fields_visions/get_all_directors`)
                .then((data) => { allChiefs.value = data })
        }

        const getVisionUser = (visionId: number) => {
            activeAreaUsers.value = [];
            Api.get(`fields_visions/get_users_in_vision/${visionId}`)
                .then((data) => {
                    if ('msg' in data) return;
                    activeAreaUsers.value = data;
                    changeEditMode(false)
                })
        }

        const getDepStructureAll = () => {
            Api.get(`fields_visions/get_full_structure`)
                .then((data) => { createDepartmentTree(data); })

        }

        const getDepStructureById = (depId: number) => {
            Api.get(`fields_visions/get_dep_structure/${depId}`)
        }

        const getDepStructureByName = (word: string) => {
            Api.get(`fields_visions/get_dep_structure/${word}`)
        }

        const createNewArea = () => {
            Api.put('fields_visions/create_new_vision/abub')
        }

        const deleteArea = (id: number) => {
            Api.delete(`fields_visions/delete_vision/${id}`)
        }

        const addUserToArea = (visionId: number, userId: number) => {
            Api.put(`fields_visions/add_user_to_vision/${visionId}/${userId}`)
        }

        const addFullDepartmentToArea = (visionId: number, departmentId: number) => {
            Api.put(`fields_visions/add_users_list_to_vision/${visionId}/${departmentId}`)
        }


        const removeUserFromArea = (visionId: number, userId: number) => {
            Api.delete(`fields_visions/delete_vision/${visionId}/${userId}`)
        }

        const createDepartmentTree = (depStructure: IDepartment[]) => {
            if (!depStructure?.length) {
                allDepStructure.value = [];
                return [];
            }

            // Создаем карту всех департаментов
            depStructure.forEach(dept => {
                departmentMap.set(dept.id, { ...dept, departments: [] });
            });

            const rootDepartments: string[] = [];

            // Строим дерево
            depStructure.forEach(dept => {
                const currentDept = departmentMap.get(dept.id);

                if (!currentDept) return; // Защита от undefined

                if (dept.father_id === null || dept.father_id === undefined) {
                    // Это корневой департамент
                    rootDepartments.push(currentDept);
                } else {
                    // Это дочерний департамент, добавляем его к родителю
                    const parentDept = departmentMap.get(dept.father_id);
                    if (parentDept) {
                        parentDept.departments.push(currentDept);
                    } else {
                        // Если родитель не найден, считаем департамент корневым
                        console.warn(`Parent department with id ${dept.father_id} not found for department ${dept.id}`);
                        rootDepartments.push(currentDept);
                    }
                }
            });
            // Сохраняем построенное дерево, а не исходные данные
            allDepStructure.value = rootDepartments;
        }
        const choices = ref<{ id: number; name: string; type: 'allDep' | 'onlyDep' | 'user' }[]>([]);

        const fixUserChoice = (type: 'allDep' | 'onlyDep' | 'user', id: number, userId: number | null = null) => {
            const targetIndex = choices.value.findIndex((e) => e.id == (type == 'user' ? userId : id));

            if (targetIndex !== -1) {
                choices.value.splice(targetIndex, 1);
            }
            else
                if (type == 'user') {
                    const target = departmentMap.get(id).users.find((e: IUserSearch) => e.user_id == userId);

                    choices.value.push({ id: target.user_id, name: target.user_fio, type: 'user' })
                }
                else {
                    const target = departmentMap.get(id);
                    choices.value.push({ id: target.id, name: target.name + (type == "allDep" ? ' с подотделами' : ' без подотделов'), type: type })
                    console.log(choices.value);

                }
        }

        const saveChoices = () => {
            console.log(choices.value);
        }

        const clearChoices = () => {
            choices.value.length = 0;
        }

        onMounted(() => {
            getAllVisions();
            getDepStructureAll();
        })

        return {
            allAreas,
            activeArea,
            activeAreaUsers,
            editGroupMode,
            allDepStructure,
            choices,
            fixUserChoice,
            getVisionUser,
            createNewArea,
            changeActiveArea,
            changeEditMode,
            saveChoices,
            clearChoices
        }
    }
})
</script>

<style lang="scss">
p .visibility-editor__areas {
    display: flex;
    flex-direction: column;
    gap: 10px;
    padding: 0;
}

.visibility-editor__area {
    border: 1px solid var(--emk-brand-color);
    max-width: 30%;
    border-radius: 15px;
    display: flex;
    flex-direction: row;
    align-items: center;
    align-content: center;
    justify-content: center;
    cursor: pointer;
    padding: 5px;
    transition: all 0.2s;

    &:hover {
        background: var(--emk-brand-color);
        color: white;
    }
}

.visibility-editor__area-users__wrapper {
    flex: 1;
    padding-right: 10px;
    margin-left: 0;
}

.visibility-editor__wrapper {
    display: flex;
}

.visibility-editor__area-users {
    list-style: none;
    padding: 0;
    margin: 0;
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
    gap: 16px;
    max-height: 1000px;
    overflow-y: auto;
    padding: 8px 0;
}


.visibility-editor__area-user {
    background: #ffffff;
    border: 1px solid #e9ecef;
    color: black;
    border-radius: 12px;
    padding: 8px;
    display: flex;
    align-items: center;
    gap: 12px;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    cursor: pointer;
    position: relative;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.04);
    overflow: hidden;

    &--inDep:last-child {
        padding: 8px;
        margin-bottom: 15px;
    }
}

.visibility-editor__area-user:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 25px rgba(0, 0, 0, 0.12);
    border-color: var(--emk-brand-color);
    background: #fafbfc;
}

.visibility-editor__user-avatar {
    width: 56px;
    height: 56px;
    border-radius: 50%;
    overflow: hidden;
    flex-shrink: 0;
    position: relative;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
    transition: all 0.3s ease;
    display: flex;
    align-items: center;
}


.visibility-editor__user-photo {
    width: 100%;
    height: 100%;
    object-fit: cover;
    transition: all 0.3s ease;
}

.visibility-editor__area-user:hover .visibility-editor__user-photo {
    transform: scale(1.1);
}

.visibility-editor__user-fio {
    color: black;
}

.visibility-editor__area-users__edit-methods__search {
    // margin-top: 16px;
}

.visibility-editor__area-users__edit-methods {
    display: flex;
    flex-direction: row;
    align-items: baseline;
    justify-content: center;
    gap: 16px;
}

.visibility-editor__area-departments {
    display: flex;
    flex-direction: column;
    gap: 10px;
    padding: 0;
}

.visibility-editor__area-department {
    display: flex;
    flex-direction: row;
    gap: 5px;
    align-items: flex-start;
    justify-content: flex-start;
    cursor: pointer;
    transition: all 0.2s;
    border-left: 1px solid #6666666a;
    padding-left: 5px;


    &:hover:not(.visibility-editor__area-user) {
        // color: var(--emk-brand-color);
    }

    &:hover {
        &>svg {
            color: var(--emk-brand-color);

            &+.visibility-editor__area-department__info>span {
                color: var(--emk-brand-color);
            }
        }
    }

    &>svg {
        min-width: 20px;
        width: 20px;
        height: 20px;
        transition: all 0.2s ease;

        &:hover {
            color: var(--emk-brand-color);

            &+.visibility-editor__area-department__info>span {
                color: var(--emk-brand-color);
            }
        }
    }
}

.visibility-editor__area-department__info {
    user-select: none;
}

.visibility-editor__area-department__info__users {
    margin-top: 10px;
    display: flex;
    flex-direction: column;
    gap: 5px;
    user-select: none;
}

.visibility-editor__area-user-avatar {
    max-width: 20px;
    border-radius: 10px;
}

.visibility-editor__area-department--active {
    color: var(--emk-brand-color);
}

.visibility-editor__right-sidebar {
    border-left: 1px solid #e9ecef;
    border-top: 1px solid #e9ecef;
    background-color: #f8f9fa;
    min-height: 100vh;
    max-width: 160px;
    min-width: 160px;
    padding: 10px;
    // position: fixed;
}

.visibility-editor__button-group {
    display: flex;
    flex-direction: column;
    gap: 5px;
}
</style>