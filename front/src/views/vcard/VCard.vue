<template>
<div class="vcard__container">
    <div class="vcard__wrapper">
        <VCardSkeleton v-if="isLoading || !user" />
        <div v-else
             class="vcard">
            <div class="vcard__photo">
                <img class="vcard__photo-img"
                     :src="user.PERSONAL_PHOTO"
                     alt="Фото сотрудника" />
            </div>
            <div class="vcard__content">
                <div class="vcard__header">
                    <h4>{{ user.LAST_NAME + ' ' + user.NAME + ' ' + user.SECOND_NAME }}</h4>
                    <div v-if="user.WORK_POSITION"
                         class="vcard__work-position">
                        {{ user.WORK_POSITION }}
                    </div>
                </div>
                <div v-if="user"
                     class="vcard__employee__info"
                     :class="{ 'vcard__employee__info--big': user.Division && user.UF_DEPARTMENT && user.Direction && user.Combination && user.Combination.length }">
                    <div v-if="user.Direction"
                         class="vcard__employee__info__item">
                        <div>
                            Дирекция:
                        </div>
                        <div v-for="(dep, index) in user.Direction"
                             :key="dep + '' + index">
                            {{ dep }}
                        </div>
                    </div>
                    <div v-if="user.UF_DEPARTMENT"
                         class="vcard__employee__info__item">
                        <div>
                            Подразделение:
                        </div>
                        <div v-for="(dep, index) in user.UF_DEPARTMENT"
                             :key="dep + '' + index">
                            {{ dep }}
                        </div>
                    </div>
                    <div v-if="user.Combination && user.Combination.length"
                         class="vcard__employee__info__item">
                        <div>
                            Совместительство:
                        </div>
                        <div v-for="(dep, index) in user.Combination"
                             :key="dep + '' + index">
                            {{ dep }}
                        </div>
                    </div>
                    <div v-if="user.Division"
                         class="vcard__employee__info__item">
                        <div>
                            Подразделение (по иерархии):
                        </div>
                        <div v-for="(dep, index) in user.Division"
                             :key="dep + '' + index">
                            {{ dep }}
                        </div>
                    </div>
                </div>
                <div class="vcard__button-wrapper">
                    <div class="btn">
                        <div v-if="!isDownloading"
                             class="btn__text"
                             @click="downloadContact()">
                            Добавить в контакты
                        </div>
                        <Loader v-else />
                    </div>
                </div>
                <VCardCompany />
            </div>
        </div>
    </div>
</div>
</template>

<script lang="ts">
import { ref, watch, defineComponent, type Ref } from 'vue';
import Api from '@/utils/Api';
import download from 'downloadjs';
import VCardSkeleton from './VCardSkeleton.vue';
import { type IUser } from '@/interfaces/IEntities';
import VCardCompany from './VCardCompany.vue';
import { useRoute } from 'vue-router';
import Loader from '@/components/layout/Loader.vue';
import { handleApiError } from '@/utils/apiResponseCheck';
import { useToast } from 'primevue/usetoast';
import { useToastCompose } from '@/composables/useToastСompose';

export default defineComponent({
    components: {
        VCardSkeleton,
        VCardCompany,
        Loader
    },
    setup() {
        const isLoading: Ref<boolean> = ref(true);
        const route = useRoute();
        const user = ref();
        const uid = ref(route.params.id);
        const isDownloading = ref(false);
        const toastInstance = useToast();
        const toast = useToastCompose(toastInstance);

        watch((uid), () => {
            if (!uid.value) return;
            Api.get(`vcard/by_uuid/${uid.value}`)
                .then((res: IUser) => {
                    if (!res) {
                        toast.showWarning('noUserVCard');
                    } else
                        user.value = res;
                })
                .finally(() => {
                    isLoading.value = false;
                })
                .catch((e) => handleApiError(e, toast));
        }, { immediate: true, deep: true })

        const downloadContact = async () => {
            isDownloading.value = true;
            Api.post(`/vcard/get/${uid.value}`, null, { responseType: 'blob' })
                .then((data) => {
                    download(data.data, user.value.LAST_NAME + " " + user.value.NAME + " s" + user.value.SECOND_NAME + '.vcf')
                    isLoading.value = false
                })
                .finally(() => isDownloading.value = false)
                .catch((e) => handleApiError(e, toast));
        }

        return {
            user,
            isLoading,
            downloadContact,
            isDownloading
        }
    }
})
</script>
