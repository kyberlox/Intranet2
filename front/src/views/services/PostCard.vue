<template>
<div class="postcard">
    <h1 class="page__title">Сервис отправки поздравительных открыток</h1>
    <div class="postcard__container">
        <div class="postcard__form-wrapper">

            <div class="postcard__form-group">
                <label>Выберите праздник</label>
                <select class="postcard__select"
                        v-model="activeHoliday">
                    <option v-for="holiday in postCards"
                            :key="holiday.id"
                            :value="holiday.id">
                        {{ holiday.name }}
                    </option>
                </select>
            </div>

            <VForm @submit="''"
                   class="postcard__form">
                <div class="postcard__form-group">
                    <label>От</label>
                    <input type="email"
                           class="disabled"
                           disabled
                           :placeholder="msgSender" />
                </div>

                <div class="postcard__form-group">
                    <label for="msgRecieverTextField">Кому</label>
                    <ErrorMessage name="msgRecieverTextField"
                                  class="invalid-feedback" />
                    <Field as="input"
                           type="email"
                           name="msgRecieverTextField"
                           :rules="validateEmail"
                           rows="1"
                           placeholder="recipient@email.com"
                           v-model="msgReciever" />
                </div>

                <div class="postcard__form-group">
                    <label for="textField">Тема</label>
                    <Field as="textarea"
                           name="msgThemeTextField"
                           rows="1"
                           placeholder="Поздравление"
                           v-model="msgTheme" />
                </div>

                <div class="postcard__form-group postcard__swiper-wrapper">
                    <SwiperBlank :type="'postInner'"
                                 @indexChanged="changeMsgCardIndex"
                                 :needEmitIndex="true"
                                 :images="currentSlides" />
                </div>

                <div class="postcard__form-group">
                    <label for="textField">Текст письма</label>
                    <Field as="textarea"
                           name="msgTextField"
                           rows="8"
                           placeholder="Введите текст поздравления..."
                           v-model="msgText" />
                </div>

                <div class="postcard__form-group">
                    <label>Подпись</label>
                    <textarea v-model="signature"
                              :rows="textAreaRowsToContent(signature)"
                              class="postcard__signature"></textarea>
                </div>
            </VForm>

            <div class="postcard__form-group">
                <button @click="sendMsg"
                        class="submit-button postcard__form-group__submit-button">
                    <Loader v-if="isLoading"
                            class="neuroChat__send-button__loader" />
                    Отправить
                </button>
            </div>
        </div>
    </div>
</div>
</template>

<script lang="ts">
import { textAreaRowsToContent } from "@/utils/stringUtils.js";
import { ref, defineComponent, onMounted, watch, computed, nextTick } from "vue";
import SwiperBlank from "@/components/tools/swiper/SwiperBlank.vue";
import Api from "@/utils/Api";
import { sectionTips } from "@/assets/static/sectionTips";
import { type IPostCard } from "@/interfaces/IEntities";
import { useUserData } from "@/stores/userData";
import { createMail } from "@/utils/createMail";
import { Field, Form as VForm, ErrorMessage } from 'vee-validate';
import { handleApiError, handleApiResponse } from '@/utils/apiResponseCheck';
import { useToast } from 'primevue/usetoast';
import { useToastCompose } from '@/composables/useToastСompose';
import Loader from "@/components/layout/Loader.vue";

export default defineComponent({
    name: "PostCard",
    components: {
        SwiperBlank,
        Field,
        VForm,
        ErrorMessage,
        Loader
    },
    setup() {
        const greetingsText = ref("");
        const postCards = ref<IPostCard[]>([]);
        const currentSlides = ref();
        const activeHoliday = ref<number>();
        const userData = useUserData();
        const imageInMsg = ref<string>();
        const user = computed(() => userData.getUser);
        const signature = ref(computed(() => userData.getSignature));
        const msgSender = computed(() => userData.getUser.email)
        const msgTheme = ref<string>();
        const msgReciever = ref<string>();
        const msgText = ref<string>();
        const isLoading = ref(false);
        const toastInstance = useToast();
        const toast = useToastCompose(toastInstance);

        onMounted(() => {
            Api.get(`article/find_by/${sectionTips['открытки']}`)
                .then((data: IPostCard[]) => postCards.value = data)
        })

        const changeActiveHoliday = (id: number) => {
            activeHoliday.value = id;
        }

        watch((activeHoliday), (newVal) => {
            if (!newVal) { return }
            currentSlides.value = [];
            Api.get(`article/find_by_ID/${newVal}`)
                .then((data) => {
                    currentSlides.value = data.images;
                    changeMsgCardIndex(0);
                })
        })

        const changeMsgCardIndex = async (newIndex: number) => {
            await nextTick()
            console.log(currentSlides.value);

            imageInMsg.value = currentSlides.value[newIndex]?.file_url
        }

        const sendMsg = () => {
            isLoading.value = true;
            console.log(!msgSender.value || !msgReciever.value || !imageInMsg.value);

            if (!msgSender.value || !msgReciever.value || !imageInMsg.value) return;
            const mailText = msgText.value ? createMail(msgText.value, signature.value) : '';
            const mailTheme = msgTheme.value ? msgTheme.value : '';
            const body = {
                "sender": user.value.email,
                "reciever": msgReciever.value,
                "title": mailTheme,
                "text": mailText,
                "file_url": imageInMsg.value.replace('http://intranet.emk.org.ru/api/files/', '')
            }
            Api.post('/users/test_send_mail', body)
                .then((data) => handleApiResponse(data, toast, 'trySupportError', 'sendPostCardSuccess'))
                .catch((e) => handleApiError(e, toast))
                .finally(() => isLoading.value = false)
        }
        const validateEmail = (value: unknown): boolean | string => {
            if (typeof value !== 'string' || value.trim() === '') {
                return 'Email обязателен для заполнения';
            }

            const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
            if (!emailRegex.test(value)) {
                return 'Введите корректный email адрес';
            }

            return true;
        };

        return {
            currentSlides,
            signature,
            greetingsText,
            postCards,
            activeHoliday,
            msgSender,
            msgTheme,
            msgReciever,
            msgText,
            isLoading,
            sendMsg,
            changeMsgCardIndex,
            changeActiveHoliday,
            textAreaRowsToContent,
            validateEmail
        };
    },
});
</script>