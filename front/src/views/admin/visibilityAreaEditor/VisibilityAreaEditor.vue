<template>
    <div class="visibility-editor__title page__title mt20">Редактор областей видимости</div>
    <div class="visibility-editor__wrapper">
        <AdminSidebar :isVisibilityArea="true"
                      :visibilityAreas="allAreas"
                      :activeId="activeArea"
                      @addNewArea="console.log('addNewArea')"
                      @areaClicked="(i) => changeActiveArea(i)" />

        <div class="visibility-editor__area-users__wrapper">
            <VisibilityAreaControls v-if="activeArea"
                                    class="visibility-editor__area-users__edit-methods"
                                    @changeEditMode="(value) => changeEditMode(value)" />

            <VisibilityAreaUsersList v-if="!editGroupMode"
                                     :editGroupMode="editGroupMode"
                                     :formattedUsers="formattedUsers" />

            <VisibilityAreaEditorTree v-else
                                      @fixUserChoice="fixUserChoice"
                                      :choices="choices"
                                      :departments="allDepStructure" />
        </div>

        <VisibilityRightSidebar :choices="choices"
                                @saveChoices="saveChoices"
                                @clearChoices="clearChoices" />
    </div>
</template>

<script lang="ts">
import Api from '@/utils/Api';
import { computed, defineComponent, onMounted, ref } from 'vue';
import AdminSidebar from '@/views/admin/components/elementsListLayout/AdminSidebar.vue';
import VisibilityAreaEditorTree from './components/VisibilityAreaEditorTree.vue';
import VisibilityRightSidebar from './components/VisibilityRightSidebar.vue';
import VisibilityAreaControls from './components/VisibilityAreaControls.vue';
import VisibilityAreaUsersList from './components/VisibilityAreaUsersList.vue';

export interface IVisionUser {
    id: number;
    name: string;
    last_name: string;
    second_name: string;
    post: string;
    photo: null | string;
    depart: string;
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

export interface IChoice {
    id: number;
    name: string;
    type: 'allDep' | 'onlyDep' | 'user'
}

export interface IFormattedUserGroup {
    depart: string;
    users: IVisionUser[];
}

export default defineComponent({
    name: 'VisibilityAreaEditor',
    components: {
        AdminSidebar,
        VisibilityAreaEditorTree,
        VisibilityRightSidebar,
        VisibilityAreaControls,
        VisibilityAreaUsersList
    },
    setup() {
        const allAreas = ref<{ id: number, vision_name: string }[]>([]);
        const activeArea = ref<number>();
        const activeAreaUsers = ref<IVisionUser[]>([]);
        const editGroupMode = ref<boolean>(false);
        const allDepStructure = ref();
        const choices = ref<IChoice[]>([]);

        const departmentMap = new Map();
        const formattedUsers = computed(() => {
            const formattedGroup: IFormattedUserGroup[] = [];
            activeAreaUsers.value.forEach((user) => {
                const target = formattedGroup.find((formatItem) => formatItem.depart == user.depart);
                if (!target) {
                    formattedGroup.push({ depart: user.depart, users: [user] })
                }
                else target.users.push(user);
            })
            return formattedGroup
        });

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

        const getVisionUser = (visionId: number) => {
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

        const addFullDepartmentToArea = (visionId: number, departmentId: number) => {
            const body = [4133, 2375, 2366];
            Api.put((`fields_visions/add_users_list_to_vision/${visionId}`), body);
        }
        // const getDepStructureById = (depId: number) => {
        //     Api.get(`fields_visions/get_dep_structure/${depId}`)
        // }

        // const getDepStructureByName = (word: string) => {
        //     Api.get(`fields_visions/get_dep_structure/${word}`)
        // }

        // const deleteArea = (id: number) => {
        //     Api.delete(`fields_visions/delete_vision/${id}`)
        // }

        // const addUserToArea = (visionId: number, userId: number) => {
        //     Api.put(`fields_visions/add_user_to_vision/${visionId}/${userId}`)
        // }

        // const removeUserFromArea = (visionId: number, userId: number) => {
        //     Api.delete(`fields_visions/delete_vision/${visionId}/${userId}`)
        // }
        const createNewArea = () => {
            Api.put('fields_visions/create_new_vision/abub')
        }

        const createDepartmentTree = (depStructure: IDepartment[]): void => {
            if (!depStructure?.length) {
                allDepStructure.value = [];
                return;
            }

            departmentMap.clear();
            depStructure.forEach(dept => {
                departmentMap.set(dept.id, { ...dept, departments: [] });
            });

            const rootDepartments: IDepartment[] = [];

            depStructure.forEach(dept => {
                const currentDept = departmentMap.get(dept.id);
                if (!currentDept) return;

                if (dept.father_id === null || dept.father_id === undefined) {
                    rootDepartments.push(currentDept);
                } else {
                    const parentDept = departmentMap.get(dept.father_id);
                    if (parentDept) {
                        parentDept.departments.push(currentDept);
                    } else {
                        rootDepartments.push(currentDept);
                    }
                }
            });

            allDepStructure.value = rootDepartments;
        };

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
                    const typeText = type == "allDep" ? ' с подотделами' : ' без подотделов';
                    choices.value.push({ id: target.id, name: target.name + typeText, type: type })
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
            addFullDepartmentToArea(2, 142);
        })

        return {
            allAreas,
            activeArea,
            formattedUsers,
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

.visibility-editor__area-users__department-title {
    font-size: 18px;
}
</style>