<template>
<div class="row">
    <div class="col-12 col-md-10">
        <div class="personal__user__section row"
             v-if="user">
            <div class="col-12 col-md-6">
                <div class="personal__user__photo">
                    <img v-if="user && user.photo_file_url"
                         :src="user.photo_file_url"
                         alt="Игорь"
                         @click="modalIsOpen = true" />
                    <img src="https://portal.emk.ru/local/templates/intranet/img/no-user-photo.jpg"
                         alt="Фото пользователя не найдено"
                         v-else />
                </div>
                <div class="personal__user__about">
                </div>
                <div class="personal__user__mess">
                    <a :href='"https://portal.emk.ru/company/personal/user/" + user.id + "/"'
                       target="_blank"
                       class="personal__user__mess__link">Профиль в Bitrix24</a>
                    <button v-if="user.id !== myId && featureFlags.pointsSystem"
                            class="personal__user__mess__link"
                            @click="isPointsModalOpen = true">Отправить баллы</button>
                </div>
            </div>

            <div class="col-12 col-md-6">
                <div class="personal__user__top">
                    <div class="grid__content-1">
                        <h3 class="personal__user__top__title">Контактная информация</h3>
                    </div>
                </div>
                <div class="personal__user__property">
                    <div class="grid__content-1">
                        <div class="personal__user__property__items">
                            <div v-if="user.fio"
                                 class="personal__user__property__items__fio">
                                <h3>ФИО</h3>
                                <span>{{ user.fio }}</span>
                            </div>
                            <div v-if="user.indirect_data && user.indirect_data.work_position"
                                 class="personal__user__property__items__work-position">
                                <h3>Должность</h3>
                                <span>{{ user.indirect_data.work_position }}</span>
                            </div>
                            <div v-if="user.indirect_data && user.indirect_data.uf_usr_1696592324977 && user.indirect_data.uf_usr_1696592324977.length"
                                 class="personal__user__property__items__uf_usr_1696592324977">
                                <h3>Дирекция</h3>
                                <span v-for="item in user.indirect_data.uf_usr_1696592324977"
                                      :key="'dir' + item">
                                    {{ item }}
                                </span>
                            </div>
                            <div class="personal__user__property__items__uf_usr_1705744824758"
                                 v-if="user.indirect_data.uf_department || (user.indirect_data && user.indirect_data.uf_usr_1705744824758 && user.indirect_data.uf_usr_1705744824758.length)">
                                <h3>Отдел</h3>
                                <span v-for="(item, index) in user.indirect_data.uf_department"
                                      :key="'dep' + index">
                                    {{ item }}
                                </span>
                                <span v-for="(item, index) in user.indirect_data.uf_usr_1705744824758"
                                      :key="'dep' + index">
                                    {{ item }}
                                </span>
                            </div>
                            <div v-if="user.personal_birthday"
                                 class="personal__user__property__items__birthday">
                                <h3>День рождения</h3>
                                <span>{{ formatBirthday(user.personal_birthday) }}</span>
                            </div>
                            <div v-if="user.personal_city"
                                 class="personal__user__property__items__workplace">
                                <h3>Местоположение</h3>
                                <span>{{ user.personal_city }}</span>
                            </div>
                        </div>
                    </div>
                    <div class="grid__content-1">
                        <div class="personal__user__property__items">
                            <div v-if="user.email"
                                 class="personal__user__property__items__email">
                                <h3>Контактный e-mail</h3>
                                <span>{{ user.email }}</span>
                            </div>
                            <div v-if="user.indirect_data && user.indirect_data.uf_usr_1586854037086"
                                 class="personal__user__property__items__office">
                                <h3>Кабинет</h3>
                                <span>{{ user.indirect_data.uf_usr_1586854037086 }}</span>
                            </div>
                            <div v-if="user.uf_phone_inner"
                                 class="personal__user__property__items__inner-phone">
                                <h3>Внутренний телефон</h3>
                                <span>{{ user.uf_phone_inner }}</span>
                            </div>
                            <div v-if="user.indirect_data && user.indirect_data.work_phone"
                                 class="personal__user__property__items__work-phone">
                                <h3>Рабочий телефон</h3>
                                <span>{{ user.indirect_data.work_phone }}</span>
                            </div>
                            <!-- <h3>Профиль</h3>
                                <span>
                                    <a href="https://vcard.emk.ru/5bdbf37e-ad97-452a-ae80-cc666fa6f8e6"><img
                                             src="https://vcard.emk.ru/5bdbf37e-ad97-452a-ae80-cc666fa6f8e6/qr"
                                             style="width: 128px; height: 128px;"></a></span> -->
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
    <ZoomModal :image="[user.indirect_data.personal_photo ?? 'https://portal.emk.ru/local/templates/intranet/img/no-user-photo.jpg']"
               v-if="modalIsOpen == true"
               @close="modalIsOpen = false" />
    <SendPoints v-if="isPointsModalOpen"
                @sendPoints="sendPoints"
                @close="isPointsModalOpen = false" />
</div>
</template>

<script lang="ts">
import { defineComponent, ref, computed } from 'vue';
import Api from '@/utils/Api';
import ZoomModal from "@/components/tools/modal/ZoomModal.vue";
import { watch } from 'vue';
import { type IUser } from '@/interfaces/IEntities';
import { useUserData } from '@/stores/userData';
import SendPoints from './userPointsComponents/SendPointsModalSlot.vue';
import { handleApiError, handleApiResponse } from '@/utils/ApiResponseCheck';
import { useToastCompose } from '@/composables/useToastСompose';
import { useToast } from 'primevue/usetoast';
import type { IPointsForm } from '@/interfaces/IPutFetchData';
import { featureFlags } from '@/assets/static/featureFlags';

export default defineComponent({
    props: {
        id: {
            type: String
        },
    },
    components: {
        ZoomModal,
        SendPoints
    },
    setup(props) {
        const userData = useUserData();
        const user = ref();
        const modalIsOpen = ref(false);
        const isPointsModalOpen = ref(false);
        const toastInstance = useToast();
        const toast = useToastCompose(toastInstance);

        watch(props, (newVal) => {
            if (newVal) {
                Api.get(`users/find_by/${newVal.id}`)
                    .then((res: IUser) => {
                        user.value = res;
                        if (user.value && user.value.last_name && user.value.name && user.value.second_name) {
                            user.value.fio = user.value.last_name + " " + user.value.name + " " + user.value.second_name
                        }
                    })
            }
        }, { immediate: true, deep: true })

        function formatBirthday(dateString: string): string {
            if (!dateString) return '';

            const date = new Date(dateString);

            const russianMonths = [
                'января', 'февраля', 'марта', 'апреля', 'мая', 'июня',
                'июля', 'августа', 'сентября', 'октября', 'ноября', 'декабря'
            ];

            const day = date.getDate();
            const month = date.getMonth();

            return `${day} ${russianMonths[month]}`;
        }

        const senderId = computed(() => useUserData().getMyId);

        const sendPoints = (comment: string, activityId: number) => {
            const sendingData: IPointsForm = { "uuid_from": senderId.value, "uuid_to": Number(props.id), "activities_id": activityId, "description": comment };
            Api.put('peer/send_points', sendingData)
                .catch((error) => handleApiError(error, toast))
                .then((data) => {
                    handleApiResponse(data, toast, 'trySupportError', 'pointsSendSuccess');
                })
                .finally(() => isPointsModalOpen.value = false)
        }

        return {
            user,
            modalIsOpen,
            isPointsModalOpen,
            featureFlags,
            myId: computed(() => userData.getMyId),
            sendPoints,
            formatBirthday,
        }
    }
})
</script>