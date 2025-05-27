<template>
    <div class="page__title mt20">Учебный центр</div>
    <div class="row d-flex">
        <div class="col-12 col-md-12 col-lg-6 col-xl-9 col-xxl-9 d-flex order-2 order-md-1">
            <div class="training__center__section mt20">
                <div class="training__center__section__items row">
                    <div class="col-12 col-md-6 col-lg-6 col-xl-4 col-xxl-4 d-flex"
                         v-for="(section, index) in sectionsJson"
                         :key="index">
                        <RouterLink class="training__center__section__item w-100"
                                    :title="section.name"
                                    :to="{ name: section.link }">
                            <div class="training__center__section__item__img">
                                <component :is="section.component"
                                           class="w-100" />
                            </div>
                            <h3 class="training__center__section__item__title">{{ section.name }}</h3>
                        </RouterLink>
                    </div>
                </div>
            </div>
        </div>

        <div class="col-12 col-md-12 col-lg-6 col-xl-3 col-xxl-3 order-1 order-md-2 d-flex">
            <div class="training__center__detail__content">
                <div class="training__center__detail__discr">
                    <h2 class="training__center__detail__title mb-2">Обучение и развитие</h2>
                    <h3 class="training__center__detail__title mb-2">Принципы обучения</h3>
                    <p>Высокий профессионализм – условие успеха «номер один» в работе на стремительно изменяющемся
                        рынке. Мы постоянно развиваем своих сотрудников, помогаем профессиональному и личностному росту.
                    </p>
                    <p>Ознакомьтесь с нашими Принципами обучения, и Вам станет понятнее наш подход в этому вопросу.</p>
                    <ul>
                        <li>Компания вкладывается в обучение тех сотрудников, кто самостоятельно развивается, находит
                            способы наращивания знаний и умений.</li>
                        <li>Для нас важно применение полученных знаний на практике. Мы ожидаем, что после обучения вы
                            внесете изменения в свою деятельность.</li>
                        <li>У нас принято делиться полученными знаниями. Такой взаимный обмен усиливает нашу команду.
                        </li>
                        <li>Компания оплачивает обучение сотрудников полностью или частично в зависимости от
                            актуальности и применимости результатов обучения в деятельности.</li>
                    </ul>

                    <h3 class="training__center__detail__title mb-2">Учебный центр</h3>
                    <p>
                        Используя огромный опыт работы на рынке трубопроводной арматуры, мы сформировали базу профильных
                        знаний, создали свою систему дистанционного обучения. Собранный нами материал будет полезен как
                        новичкам, так и старожилам рынка.
                    </p>
                    <p>Для получения доступа к электронным курсам Вам необходимо обратиться в Учебный центр (вн. тел.
                        1600) или к своему руководителю.</p>
                    <p>Мы регулярно проводим обучающие мероприятия для развития управленческих, коммуникативных навыков,
                        навыков личной эффективности. Это дает возможность закрепить необходимые знания, освоить новые
                        модели поведения.</p>
                    <p>Информацию о планируемых мероприятиях Вы найдете в разделе «Афиши».</p>
                    <p>Здесь же мы разместили полезные материалы и книги. Это поможет Вам сориентироваться в потоке
                        каждодневной информации и выбрать для себя качественное чтение.</p>
                    <p>Мы исходим из того, что нельзя научить, можно научиться. Если Вы решаете научиться, используйте
                        возможности Учебного центра!</p>
                </div>
            </div>
        </div>
    </div>
</template>
<script lang="ts">
import { sectionsJson } from "@/assets/staticJsons/trainingCenterData";
import { defineComponent } from "vue";
export default defineComponent({
    setup() {
        return {
            sectionsJson,
        };
    },
});
</script>
