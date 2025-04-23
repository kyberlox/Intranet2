<template>
    <div class="page__title mt20">Благотворительные проекты</div>
    <div class="d-flex flex-column">
        <div class="section__image__list__section order-1 order-md-2">
            <div class="section__image__list__items row">
                <SafetyTechnicsSlide v-for="slide in safetyTechnicsSlides"
                                     :key="slide.id"
                                     :slide="slide" />
            </div>
        </div>
    </div>
</template>
<script lang="ts">
import SafetyTechnicsSlide from "@/components/about/safetyTechnics/SafetyTechnicsSlide.vue";
import { defineComponent } from "vue";
import { safetyTechnicsSlides } from "@/assets/staticJsons/careSlides";

export default defineComponent({
    components: {
        SafetyTechnicsSlide,
    },
    setup() {
        const sideInfoBlock = `
                    <h4>Техника безопасности</h4>
                    <strong>Уважаемые Коллеги!</strong>
                    <p>Согласно правилам техники безопасности, мы хотели бы обратить Ваше внимание на следующие
                        параграфы:</p>
                    <ul class="">
                        <li><a href="COVID-19/">COVID-19</a></li>
                        <li><a href="fire-safety/">Пожарная безопасность</a> и <a href="evacuation/">эвакуация</a> из офисного здания
                        </li>
                        <li>Посещение производственных площадок для
                            персонала и гостей
                        </li>
                    </ul>
                    <strong>Соблюдайте эти простые правила</strong>
                    <p>Техника безопасности — это система правил и норм, которая призвана сделать все возможное, чтобы не
                        допустить неблагоприятного воздействия опасных факторов на человека.</p>
                    <strong>Соблюдая эти правила и инструкции, Вы сможете избежать опасности для себя и окружающих. Желаем
                        Вам никогда не столкнуться с чрезвычайными ситуациями!</strong>

                `;
        return {
            safetyTechnicsSlides,
            sideInfoBlock,
        };
    },
});
</script>
