<template>
    <div class="page__title mt20">COVID-19</div>
    <div class="d-flex flex-column">
        <div class="section__image__list__section order-1 order-md-2">
            <div class="section__image__list__items row">
                <SafetyTechnicsSlide v-for="slide in safetyTechnicsSlides"
                                     :key="slide.id"
                                     :slide="slide"
                                     :place="'inner'" />

                <div class="col-12 col-xl-12 col-xxl-3">
                    <div class="news__detail__discr safety__section__discr"
                         v-html="sideInfoBlock"></div>
                </div>
            </div>
        </div>
    </div>
</template>
<script lang="ts">
import { defineComponent } from "vue";
import SafetyTechnicsSlide from "./components/SafetyTechnicsSlide.vue";
import { safetyTechnicsCovid } from "@/assets/static/safetyTechnics";
export default defineComponent({
    components: {
        SafetyTechnicsSlide,
    },
    setup() {
        const safetyTechnicsSlides = safetyTechnicsCovid;

        const sideInfoBlock: string = `
                    <h2 class="news__detail__title mb-2">Техника безопасности</h2>
                    <p><strong>В течение режима повышенной готовности,</strong> связанного с пандемией COVID-19,
                        сотрудники
                        должны соблюдать следующие правила:</p>
                    <ul class="safety__section__info__list__style">
                        <li>Носить медицинские маски</li>
                        <li>Соблюдать социальную дистанцию 1,5 метра с окружающими людьми</li>
                        <li>Регулярно мыть руки</li>
                        <li>Обрабатывать поверхности антисептиками и санитайзерами</li>
                        <li>Посещение офиса посторонними людьми свести к минимуму</li>
                        <li>По возможности сократить собственные перемещения и командировки</li>
                        <li>Старайтесь сократить участие в мероприятиях с большим количеством людей</li>
                    </ul>
                    <p>При любом недомогании поставьте в известность Вашего руководителя и воздержитесь от посещения
                        офиса.
                        Также оставайтесь дома и обратитесь к врачу, если Вы контактировали с заразившимся COVID-19.</p>
                    <strong>Просим отнестись к этим мерам с пониманием. Будьте ответственны за себя и
                        окружающих.</strong>
                `;
        return {
            safetyTechnicsSlides,
            sideInfoBlock,
        };
    },
});
</script>