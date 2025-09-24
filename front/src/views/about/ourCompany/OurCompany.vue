<template>
<div class="row">
    <div class="col-sm-6 d-flex align-items-stretch">
        <div class="m-sm-5 company__mission d-flex g-5 mt20">
            <h2 class="page__title">Миссия компании</h2>
            <p>
                <span class="fw-bold">Мы, НПО ЭМК</span>, крупнейший поставщик и производитель трубопроводной
                арматуры (ТПА) на рынке РФ, уникальное сочетание мощной производственной базы, широчайшего
                ассортимента продукции и инжинирингового
                потенциала.
            </p>
            <p>
                <span class="fw-bold">Наше предназначение</span> помогать российским и зарубежным Заказчикам в
                выполнении задач транспортировки различных сред при различных условиях эксплуатации, предлагая
                решения, связанные с использованием
                трубопроводной арматуры.
            </p>
            <p>
                <span class="fw-bold">Опираясь на</span> нашу деловую репутацию, финансовую устойчивость, широкую
                продуктовую линейку с уникальной номенклатурой, собственные производственные мощности,
                профессионализм сотрудников, способность
                быстро внедрять новые продукты, а также скорость и гибкость при принятии решений в управлении
                продажами и ценообразовании, мы: <span class="fw-bold">строим Компанию, с доминирующей долей
                    рынка</span> ТПА в РФ.
            </p>
            <p class="fw-bold">Опираясь на наши ценности, мы признаем важность командной работы, совершенствуем себя
                и свои команды, и развиваем организационную культуру Взаимного Уважения и Доверия.</p>
        </div>
    </div>
    <div class="col-sm-6 d-flex align-items-center">
        <iframe width="100%"
                height="400"
                src="https://www.youtube.com/embed/4XdwmMun-Mc"
                title="YouTube video player"
                allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share"
                allowfullscreen></iframe>
    </div>
</div>
<div class="row mt-5 justify-content-center">
    <div class="col-sm-10 achievments">
        <div class="mb-3 col-12 col-md p-2 text-center"
             v-for="(item, index) in achievments"
             :key="index">
            <span class="plus-num">{{ item.plusNum }}</span>
            <span class="plus-desc">{{ item.plusDesc }}</span>
        </div>
    </div>
</div>
<div class="row mt-5">
    <div class="col-sm-12 d-flex align-items-stretch">
        <div class="company-values">
            <h3 class="page__title">Ценности компании</h3>
            <ul>
                <li v-for="(item, index) in ourPleasures"
                    :key="'pleasure' + index">
                    {{ item }}
                </li>
            </ul>
        </div>
    </div>
</div>
</template>
<script lang="ts">
import { defineComponent } from 'vue';
export default defineComponent({
    setup() {

        const ourPleasures = [
            "Мы стремимся к тому, чтобы клиент в максимальной степени был удовлетворен работой с нами.",
            "Мы выполняем обязательства, которые на себя приняли. Сказал – сделал.",
            "Нам не нужна работа ради работы и процесс ради процесса. Мы нацелены на результат.",
            "Всякую проблему мы превращаем в задачу и решаем ее.",
            "Мы не допускаем необоснованного усложнения процедур и стараемся без ущерба для качества упрощать работу друг друга.",
            "Мы стремимся к тому, чтобы интересы сотрудников и компании в развитии друг друга совпадали.",
            "Мы учимся на ошибках и не повторяем их, всегда ищем ответ на вопрос «Что делать?», а не «Кто виноват?»",
            "Мы не воруем время друг у друга.",
            "Мы кратко и на понятном языке излагаем свои мысли и формируем документы Компании. Краткость – сестра таланта."
        ]

        const achievments = [
            {
                plusNum: "30+",
                plusDesc: "Лет мы предлагаем лучшие решения в области трубопроводной арматуры",
            },
            {
                plusNum: "2 000",
                plusDesc: "Высоко квалифицированных сотрудников",
            },
            {
                plusNum: "5 000",
                plusDesc: "Клиентов ежегодно",
            },
            {
                plusNum: "5",
                plusDesc: "Производственных площадок",
            },
            {
                plusNum: "2 000 000",
                plusDesc: "Продукции на складе",
            },
        ];
        return {
            achievments,
            ourPleasures
        };
    },
})
</script>
