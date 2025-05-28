<template>
    <div class="postcard">
        <h1 class="page__title">Сервис отправки поздравительных открыток</h1>

        <div class="postcard__container">
            <div class="postcard__form-wrapper">
                <select class="postcard__select">
                    <option value=""
                            disabled
                            selected>Выберите праздник</option>
                    <option>День рождения</option>
                    <option>Новый год</option>
                    <option>8 марта</option>
                    <option>23 февраля</option>
                </select>

                <form class="postcard__form">
                    <div class="postcard__form-group">
                        <label>От</label>
                        <input type="email"
                               placeholder="your@email.com" />
                    </div>

                    <div class="postcard__form-group">
                        <label>Кому</label>
                        <input type="email"
                               placeholder="recipient@email.com" />
                    </div>

                    <div class="postcard__form-group">
                        <label>Тема</label>
                        <input type="text"
                               placeholder="Поздравление" />
                    </div>

                    <div class="postcard__form-group postcard__swiper-wrapper">
                        <FullWidthSlider :images="slides" />
                    </div>

                    <div class="postcard__form-group">
                        <label>Текст письма</label>
                        <textarea v-model="greetingsText"
                                  :rows="textAreaRowsToContent(greetingsText)"
                                  placeholder="Введите текст поздравления..."></textarea>
                    </div>

                    <div class="postcard__form-group">
                        <label>Подпись</label>
                        <textarea v-model="signature"
                                  :rows="textAreaRowsToContent(signature)"
                                  class="postcard__signature">
                                  С уважением,
                                  --
                                  АО «НПО «ЭМК»
                                </textarea>
                        <!-- {{ FIO }} -->
                        <!-- {{ POST }} -->
                        <!-- Тел.: {{ PHONE }} -->
                        <!-- Email: {{ EMAIL }} -->
                    </div>

                    <div class="postcard__form-group">
                        <button type="submit"
                                class="submit-button">Отправить</button>
                    </div>
                </form>
            </div>
        </div>
    </div>
</template>

<script lang="ts">
import FullWidthSlider from "@/components/tools/swiper/FullWidthSlider.vue";
import { textAreaRowsToContent } from "@/utils/StringUtils.js";
import { ref } from "vue";
import { defineComponent } from "vue";
export default defineComponent({
    name: "PostCard",
    components: { FullWidthSlider },
    setup() {
        const signature = ref(`С уважением,
Газинский Игорь Владимирович
Программист
--
АО «НПО «ЭМК»
Тел.: +7 845 245-44-33 (5182)
Моб.: +7 902 045-61-66
Эл. почта: gazinskii.i.v@emk.ru`);
        const greetingsText = ref("");
        return {
            slides: ["https://portal.emk.ru/intranet/tools/mail/img/den-rossii/01.jpg", "https://portal.emk.ru/intranet/tools/mail/img/08-mar/01.jpg"],
            signature,
            greetingsText,
            textAreaRowsToContent
        };
    },
});
</script>