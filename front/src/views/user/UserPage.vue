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
                        <a href="https://portal.emk.ru/company/personal/user/2366/"
                           class="personal__user__mess__link">Написать</a>
                    </div>
                </div>
                <div class="col-12 col-md-6">
                    <div class="personal__user__top">
                        <div class="grid__content-1">
                            <h3 class="personal__user__top__title">Контактная информация</h3>
                        </div>
                        <div class="grid__content-1">
                            <div class="personal__user__social__list">
                                <a href="gazinskii.i.v@emk.ru"
                                   target="_blank"><i
                                       class="personal__user__social__item personal__user__social__skype"></i></a>
                            </div>
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
                                    <span v-for="item in user.indirect_data.uf_usr_1696592324977">
                                        {{ item }}
                                    </span>
                                </div>
                                <div class="personal__user__property__items__uf_usr_1705744824758"
                                     v-if="user.indirect_data && user.indirect_data.uf_usr_1705744824758 && user.indirect_data.uf_usr_1705744824758.length">
                                    <h3>Отдел</h3>
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
                                     class="personal__user__property__items">
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
    </div>
</template>

<script lang="ts">
import { defineComponent, ref } from 'vue';
import Api from '@/utils/Api';
import ZoomModal from "@/components/tools/modal/ZoomModal.vue";
import { watch } from 'vue';

interface IUser {
    "id": number,
    "uuid": string,
    "active": boolean,
    "name": string,
    "last_name": string,
    "second_name": string,
    "email": string,
    "personal_mobile": string,
    "uf_phone_inner": string,
    "personal_city": string,
    "personal_gender": string,
    "personal_birthday": string,
    "indirect_data": {
        "id": number,
        "title": string,
        "work_www": string,
        "work_zip": string,
        "is_online": string,
        "time_zone": string,
        "user_type": string,
        "work_city": string,
        "last_login": string,
        "work_notes": string,
        "work_pager": string,
        "work_phone": string,
        "work_state": string,
        "timestamp_x": {},
        "work_street": string,
        "personal_fax": string,
        "personal_icq": string,
        "work_company": string,
        "work_country": string,
        "work_mailbox": string,
        "work_profile": string,
        "date_register": string,
        "uf_department": string[],
        "work_position": string,
        "personal_notes": string,
        "personal_pager": string,
        "personal_photo": string,
        "work_department": string,
        "personal_country": string,
        "time_zone_offset": string,
        "last_activity_date": {},
        "uf_employment_date": string,
        "personal_profession": string,
        "uf_usr_1586854037086": string,
        "uf_usr_1586861567149": string,
        "uf_usr_1594879216192": string,
        "uf_usr_1679387413613": string[],
        "uf_usr_1696592324977": string[],
        "uf_usr_1705744824758": string[],
        "uf_usr_1707225966581": string[] | boolean,
        "fio"?: string
    }
}

export default defineComponent({
    props: {
        id: {
            type: String
        },
    },
    components: {
        ZoomModal
    },
    setup(props) {
        const user = ref();
        // const myId = computed(() => useUserData().getMyId)
        const modalIsOpen = ref(false);
        watch(props, (newVal) => {
            if (newVal) {
                Api.get(`users/find_by/${newVal.id}`)
                    .then((res: IUser) => {
                        user.value = res;
                        if (user.value.last_name && user.value.name && user.value.second_name) {
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

        return {
            user,
            modalIsOpen,
            formatBirthday,
        }
    }
})
</script>