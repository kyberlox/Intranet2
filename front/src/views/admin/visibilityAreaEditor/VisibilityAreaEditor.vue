<template>
<div class="visibility-editor__title page__title mt20">Редактор областей видимости</div>
<div class="visibility-editor__wrapper">
    <AdminSidebar :needDefaultNav="false">
        <VisibilityAreaSlotLeftSidebar :visibilityAreas="allAreas"
                                       :activeId="activeArea"
                                       @addNewArea="modalIsOpen = true"
                                       @deleteArea="deleteArea"
                                       @areaClicked="(i: number) => changeActiveArea(i)" />
    </AdminSidebar>

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

        <VisibilityAreaUsersList v-if="!editGroupMode && !isLoading"
                                 :editGroupMode="editGroupMode"
                                 :userChoices="choices"
                                 :formattedUsers="formattedUsers"
                                 :filteredUsers="filteredUsers"
                                 :fioFilter="fioFilterValue"
                                 :depFilter="depFilterValue"
                                 :activeArea="activeArea"
                                 @deleteDep="deleteDepFromVision"
                                 @pickUser="fixUserChoice" />

        <VisibilityAreaEditorTree v-else-if="editGroupMode && !isLoading"
                                  @fixUserChoice="fixUserChoiceFromDepTree"
                                  :filteredDepartments="filteredDepartments"
                                  :filteredUsers="filteredUsers"
                                  :choices="choices"
                                  :departments="allDepStructure" />
        <div v-else
             class="visibility-editor__area__loader__wrapper">
            <Loader />
        </div>
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
import Loader from '@/components/layout/Loader.vue';
import { useToast } from 'primevue/usetoast';
import { useToastCompose } from '@/composables/useToastСompose';
import { handleApiError } from '@/utils/ApiResponseCheck';
import VisibilityAreaSlotLeftSidebar from './components/VisibilityAreaSlotLeftSidebar.vue';

export default defineComponent({
    name: 'VisibilityAreaEditor',
    components: {
        AdminSidebar,
        VisibilityAreaEditorTree,
        VisibilityRightSidebar,
        VisibilityAreaControls,
        VisibilityAreaUsersList,
        SlotModal,
        VisibilityAreaSlotModal,
        VisibilityAreaSlotLeftSidebar,
        Loader
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
        const filteredUsers = ref<IUserSearch[]>([]);
        const filteredDepartments = ref<IDepartment[]>([]);
        const isLoading = ref(false);
        const toastInstance = useToast();
        const toast = useToastCompose(toastInstance);

        const departmentMap = new Map();
        const formattedUsers = computed(() => {
            const formattedGroup: IFormattedUserGroup[] = [];
            activeAreaUsers.value?.forEach((user) => {
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
                .catch(error => {
                    if (error.response?.status == 500) {
                        handleApiError(error, toast)
                    }
                })
                .then((data) => { allAreas.value = data })
        }

        const getVisionUser = (visionId: number) => {
            isLoading.value = true
            Api.get(`fields_visions/get_users_in_vision/${visionId}`)
                .then((data) => {
                    if ('msg' in data) return;
                    activeAreaUsers.value = data;
                    changeEditMode(false);
                })
                .catch(error => {
                    if (error.response?.status == 500) {
                        handleApiError(error, toast)
                    }
                })
                .finally(() => {
                    isLoading.value = false;
                })
        }

        const getDepStructureAll = () => {
            Api.get(`fields_visions/get_full_structure`)
                .catch(error => {
                    if (error.response?.status == 500) {
                        handleApiError(error, toast)
                    }
                })
                .then((data) => {
                    createDepartmentTree(data);
                })
        }

        const addOneDepartmentToArea = (visionId: number, departmentId: number) => {
            Api.put((`fields_visions/add_dep_users_only/${visionId}/${departmentId}`))
                .catch(error => {
                    if (error.response?.status == 500) {
                        handleApiError(error, toast)
                    }
                })
                .finally(() => {
                    getVisionUser(visionId)
                })
        }

        const addFullDepartmentToArea = (visionId: number, departmentId: number) => {
            isLoading.value = true;
            Api.put((`fields_visions/add_full_usdep_list_to_vision/${visionId}/${departmentId}`))
                .catch(error => {
                    if (error.response?.status == 500) {
                        handleApiError(error, toast)
                    }
                })
                .finally(() => {
                    getVisionUser(visionId);
                })
        }

        const addUsersToArea = (visionId: number, userIds: number[]) => {
            Api.put(`fields_visions/add_users_list_to_vision/${visionId}`, userIds)
                .catch(error => {
                    if (error.response?.status == 500) {
                        handleApiError(error, toast)
                    }
                })
                .finally(() => {
                    getVisionUser(visionId)
                })
        }

        const createNewArea = (newAreaName: string) => {
            Api.put(`fields_visions/create_new_vision/${newAreaName}`)
                .catch(error => {
                    if (error.response?.status == 500) {
                        handleApiError(error, toast)
                    }
                })
                .finally(() => {
                    modalIsOpen.value = false;
                    getAllVisions();
                    changeEditMode(false);
                })
        }

        const deleteArea = (id: number) => {
            changeEditMode(false);
            Api.delete(`fields_visions/delete_vision/${id}`)
                .catch(error => {
                    if (error.response?.status == 500) {
                        handleApiError(error, toast)
                    }
                })
                .finally(() => {
                    activeArea.value = Number('');
                    activeAreaUsers.value.length = 0;
                    getAllVisions();
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
                .catch(error => {
                    if (error.response?.status == 500) {
                        handleApiError(error, toast)
                    }
                })
                .finally(() => {
                    getVisionUser(activeArea.value!);
                })
        }

        const deleteDepFromVision = (id: number) => {
            isLoading.value = true;
            Api.delete(`fields_visions/remove_depart_in_vision/${activeArea.value}/${id}`)
                .catch(error => {
                    if (error.response?.status == 500) {
                        handleApiError(error, toast)
                    }
                })
                .finally(() => {
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
                .catch(error => {
                    if (error.response?.status == 500) {
                        handleApiError(error, toast)
                    }
                })
                .then((data) => {
                    filteredUsers.value = [];
                    filteredDepartments.value = data;
                })
        }

        const getUserByName = (word: string) => {
            Api.get(`users/search/full_search_users/${word}`)
                .catch(error => {
                    if (error.response?.status == 500) {
                        handleApiError(error, toast)
                    }
                })
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
            isLoading,
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