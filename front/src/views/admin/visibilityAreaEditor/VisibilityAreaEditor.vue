<template>
    <div class="visibility-editor__title page__title mt20">Редактор областей видимости</div>
    <div class="visibility-editor__wrapper">
        <AdminSidebar :isVisibilityArea="true"
                      :visibilityAreas="allAreas"
                      :activeId="activeArea"
                      @addNewArea="modalIsOpen = true"
                      @deleteArea="deleteArea"
                      @areaClicked="(i) => changeActiveArea(i)" />

        <SlotModal v-if="modalIsOpen"
                   @close="modalIsOpen = false">
            <VisibilityAreaSlotModal @cancelArea="modalIsOpen = false"
                                     @acceptArea="createNewArea" />
        </SlotModal>

        <div class="visibility-editor__area-users__wrapper">
            <VisibilityAreaControls v-if="activeArea"
                                    :editGroupMode="editGroupMode"
                                    class="visibility-editor__area-users__edit-methods"
                                    @changeEditMode="(value) => changeEditMode(value)"
                                    @depFilterChanged="(depValue) => handleFilterChanged(depValue, 'dep')"
                                    @fioFilterChanged="(fioValue) => handleFilterChanged(fioValue, 'fio')" />

            <VisibilityAreaUsersList v-if="!editGroupMode"
                                     :editGroupMode="editGroupMode"
                                     :userChoices="choices"
                                     :formattedUsers="formattedUsers"
                                     :filteredUsers="filteredUsers"
                                     :fioFilter="fioFilterValue"
                                     :depFilter="depFilterValue"
                                     @deleteDep="deleteDepFromVision"
                                     @pickUser="fixUserChoice" />

            <VisibilityAreaEditorTree v-else
                                      @fixUserChoice="fixUserChoiceFromDepTree"
                                      :filteredDepartments="filteredDepartments"
                                      :filteredUsers="filteredUsers"
                                      :choices="choices"
                                      :departments="allDepStructure" />
        </div>

        <VisibilityRightSidebar :choices="choices"
                                :editMode="editGroupMode"
                                @deleteMultipleUsers="deleteMultipleUsers"
                                @saveChoices="saveChoices"
                                @clearChoices="clearChoices"
                                @deleteFromChoice="deleteFromChoice" />
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
import SlotModal from '@/components/tools/modal/SlotModal.vue';
import VisibilityAreaSlotModal from './components/VisibilityAreaSlotModal.vue';
import type { IVisionUser, IChoice, IFormattedUserGroup, IDepartment, IUserSearch, IUser } from '@/interfaces/IEntities';

export default defineComponent({
    name: 'VisibilityAreaEditor',
    components: {
        AdminSidebar,
        VisibilityAreaEditorTree,
        VisibilityRightSidebar,
        VisibilityAreaControls,
        VisibilityAreaUsersList,
        SlotModal,
        VisibilityAreaSlotModal
    },
    setup() {
        const allAreas = ref<{ id: number, vision_name: string }[]>([]);
        const activeArea = ref<number>();
        const activeAreaUsers = ref<IVisionUser[]>([]);
        const editGroupMode = ref<boolean>(false);
        const allDepStructure = ref();
        const modalIsOpen = ref(false);
        const choices = ref<IChoice[]>([]);
        const fioFilterValue = ref<string>();
        const depFilterValue = ref<string>();
        const filteredUsers = ref<IFormattedUserGroup[]>([]);
        const filteredDepartments = ref<IUserSearch[]>([]);

        const departmentMap = new Map();
        const formattedUsers = computed(() => {
            const formattedGroup: IFormattedUserGroup[] = [];
            activeAreaUsers.value.forEach((user) => {
                const target = formattedGroup.find((formatItem) => formatItem.depart == user.depart);
                if (!target) {
                    formattedGroup.push({ depart: user.depart, users: [user], depart_id: user.depart_id })
                }
                else target.users.push(user);
            })
            return formattedGroup
        });

        const changeEditMode = (val: boolean) => {
            editGroupMode.value = val;
            clearChoices();
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
                    changeEditMode(false);
                })
        }

        const getDepStructureAll = () => {
            Api.get(`fields_visions/get_full_structure`)
                .then((data) => {
                    createDepartmentTree(data);
                })
        }

        const addOneDepartmentToArea = (visionId: number, departmentId: number) => {
            Api.put((`fields_visions/add_dep_users_only/${visionId}/${departmentId}`))
                .finally(() => {
                    getVisionUser(visionId)
                })
        }

        const addFullDepartmentToArea = (visionId: number, departmentId: number) => {
            Api.put((`fields_visions/add_full_usdep_list_to_vision/${visionId}/${departmentId}`))
                .finally(() => {
                    getVisionUser(visionId)
                })
        }

        const addUsersToArea = (visionId: number, userIds: number[]) => {
            Api.put(`fields_visions/add_users_list_to_vision/${visionId}`, userIds)
                .finally(() => {
                    getVisionUser(visionId)
                })
        }

        const createNewArea = (newAreaName: string) => {
            Api.put(`fields_visions/create_new_vision/${newAreaName}`)
                .then(() => {
                    modalIsOpen.value = false;
                    getAllVisions();
                    changeEditMode(false);
                })
        }

        const deleteArea = (id: number) => {
            Api.delete(`fields_visions/delete_vision/${id}`)
                .then(() => {
                    getAllVisions();
                    changeEditMode(false);
                    activeArea.value = Number('');
                })
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

        const fixUserChoiceFromDepTree = (type: 'allDep' | 'onlyDep' | 'user', id: number, userId: number | null = null) => {
            const targetIndex = choices.value.findIndex((e) => e.id == (type == 'user' ? userId : id));

            if (targetIndex !== -1) {
                if (choices.value[targetIndex].type == type) {
                    choices.value.splice(targetIndex, 1);
                }
                else {
                    choices.value.splice(targetIndex, 1);
                    fixUserChoiceFromDepTree(type, id, userId);
                }
            }
            else
                if (type == 'user') {
                    const target = departmentMap.get(id).users.find((e: IUserSearch) => e.id == userId);
                    choices.value.push({ id: target.id, name: target.name, type: 'user' })
                }
                else {
                    const target = departmentMap.get(id);
                    const typeText = type == "allDep" ? ' с подотделами' : ' без подотделов';
                    choices.value.push({ id: target.id, name: target.name + typeText, type: type })
                }
        }

        const fixUserChoice = (user: IUser) => {
            const targetIndex = choices.value.findIndex((e) => e.id == user.id)
            if (targetIndex !== -1) {
                choices.value.splice(targetIndex, 1);
            }
            else {
                choices.value.push({
                    id: user.id,
                    name: user.name,
                    type: 'user'
                })
            }
        }

        const saveChoices = async () => {
            const newAreaUsers: number[] = []
            choices.value.map((e) => {
                switch (e.type) {
                    case 'allDep':
                        addFullDepartmentToArea(Number(activeArea.value), e.id);
                        break;
                    case 'onlyDep':
                        addOneDepartmentToArea(Number(activeArea.value), e.id);
                        break;
                    case 'user':
                        newAreaUsers.push(e.id)
                        break;
                    default:
                        break;
                }
            })
            if (newAreaUsers.length) {
                addUsersToArea(Number(activeArea.value), newAreaUsers);
            }
            clearChoices();
        }


        const clearChoices = () => {
            choices.value.length = 0;
        }

        const deleteFromChoice = (id: number) => {
            const targetId = choices.value.findIndex(e => e.id == id);
            choices.value.splice(targetId, 1);
        }

        const pickUser = (user: IChoice) => {
            choices.value.push(user)
        }

        const deleteMultipleUsers = () => {
            const userIds: number[] = [];
            choices.value.map((e) => {
                userIds.push(e.id)
            })

            Api.delete(`fields_visions/delete_users_from_vision/${activeArea.value}`, userIds)
                .finally(() => {
                    getVisionUser(activeArea.value!);
                })
        }

        const deleteDepFromVision = (id: number) => {
            Api.delete(`fields_visions/remove_depart_in_vision/${activeArea.value}/${id}`)
                .then(() => {
                    getVisionUser(activeArea.value!);
                })
        }

        const handleFilterChanged = (value: string, type: 'dep' | 'fio') => {
            switch (type) {
                case 'dep':
                    filteredUsers.value.length = 0;
                    depFilterValue.value = value;
                    if (!value) return filteredDepartments.value.length = 0;
                    getDepStructureByName(depFilterValue.value);
                    break;
                case 'fio':
                    filteredDepartments.value.length = 0;
                    fioFilterValue.value = value;
                    if (!value) return filteredUsers.value.length = 0;
                    getUserByName(fioFilterValue.value);
                    break;
                default:
                    break;
            }
        }

        onMounted(() => {
            getAllVisions();
            getDepStructureAll();
        })

        const getDepStructureByName = (word: string) => {
            Api.get(`fields_visions/get_dep_structure_by_name/${word}`)
                .then((data) => {
                    filteredUsers.value = [];
                    filteredDepartments.value = data;
                })
        }

        const getUserByName = (word: string) => {
            Api.get(`users/search/full_search_users/${word}/100`)
                .then((data) => {
                    filteredDepartments.value.length = 0;
                    filteredUsers.value = data[0].content;
                });
        }


        return {
            allAreas,
            activeArea,
            formattedUsers,
            editGroupMode,
            allDepStructure,
            choices,
            modalIsOpen,
            fioFilterValue,
            depFilterValue,
            filteredUsers,
            filteredDepartments,
            deleteDepFromVision,
            deleteMultipleUsers,
            handleFilterChanged,
            pickUser,
            deleteArea,
            deleteFromChoice,
            fixUserChoice,
            fixUserChoiceFromDepTree,
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

.user-choices-table__row {
    border-bottom: 1px solid rgba(128, 128, 128, 0.325);
    margin-top: 5px;
    padding: 5px;

    &>td {
        padding: 5px 0;
    }
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

.visibility-editor__area-users__department-header {
    display: flex;
    flex-direction: row;
    justify-content: space-between;

    &>svg {
        cursor: pointer;
        color: red;
        width: 30px;

        &:hover {
            color: rgba(255, 0, 0, 0.497);
        }
    }
}

.visibility-editor__area-users__department-title {
    font-size: 18px;
    transition: 0.2s;
    cursor: pointer;
    flex-grow: 1;
    user-select: none;

    &:hover {
        color: var(--emk-brand-color)
    }
}

.admin-panel__nav__button-group {
    display: flex;
    flex-direction: column;
    gap: 5px;
    margin-top: 15px;

    &>button {
        margin-top: 0;
        min-width: 139px;
    }
}

.visibility-editor__add-new-area__slot {
    padding: 15px 20px 0 15px !important;
}

.visibility-editor__add-new-area__slot__buttons {
    display: flex;
    flex-direction: row;
    gap: 5px;
    flex-wrap: wrap;
    justify-content: flex-end;
}

.visibility-editor__add-new-area__slot__button--accept {
    &:hover {
        background: green;
    }
}

.visibility-editor__add-new-area__slot__button--cancel {
    &:hover {
        background: red;
    }
}

.visibility-editor__add-new-area__slot__button {
    &>svg {
        width: 30px;

        &:hover {
            color: white;
        }
    }
}

.visibility-editor__add-new-area__slot__button--disabled {
    background: rgba(128, 128, 128, 0.41);

    &:hover {
        background: rgba(128, 128, 128, 0.41) !important;

        color: black !important;

        &>svg {
            color: black !important;
        }
    }
}

.visibility-editor__area-user--chosen {
    transform: translateY(-2px);
    box-shadow: 0 8px 25px rgba(0, 0, 0, 0.12);
    border-color: var(--emk-brand-color);
    background: #fafbfc;
}

.visibility-editor__area-users__department-header {
    display: flex;
    flex-direction: row;
}

.user-choices-table__row {
    cursor: pointer;

    &:hover {
        opacity: 0.7;

        &>svg {
            &:hover {
                color: rgba(255, 0, 0, 0.497);
            }
        }
    }

    &>svg {
        width: 20px;
        color: red;
        cursor: pointer;
    }
}

.visibility-editor__area-users__edit-methods {
    display: flex;
    flex-direction: column;
    align-items: center;
}

.visibility-editor__area-users__edit-methods__input-wrapper {
    display: flex;
    justify-content: space-between;
    gap: 10px;
}

.visibility-editor__area-users__edit-methods__search--disabled {
    &>input {
        background: #6666662d;
    }
}

.visibility-editor__area-users--userMode {
    gap: 5px;
    display: flex;
    flex-direction: column;
}
</style>