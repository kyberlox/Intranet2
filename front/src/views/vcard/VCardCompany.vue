<template>
<div v-if="companyInfo"
     class="vcard__company__info">
    <h4 class="vcard__company__info__title">Информация о компании</h4>
    <div class="vcard__company__info-item"
         v-for="(item, index) in companyInfo"
         :key="'ci' + index">
        {{ item.name }}:
        <a v-if=item.href
           :href="item.href?.includes('www') ? `https://${item.href}` : item.href">{{ item.value }}
        </a>
        <div v-else>
            {{ item.value }}
        </div>
    </div>
</div>
</template>

<script lang="ts">
import { defineComponent } from 'vue';

export default defineComponent({
    setup() {
        const companyInfo = [
            {
                name: "Веб-сайт",
                value: "www.emk.ru",
                href: "www.emk.ru",
            },
            {
                name: "Продукция",
                value: "www.emk.ru/produktsiya.html",
                href: "www.emk.ru/produktsiya.html",
            },
            {
                name: "Почтовый адрес",
                value: "410017, г. Саратов, ул. Шелковичная, 37/45",
            },
            {
                name: "Телефон",
                value: "8 (495) 955-78-86",
                href: "tel:+79020456166",
            },
            {
                name: "E-mail",
                value: "emk@emk.ru",
                href: "mailto:+79020456166",
            },
        ]
        return {
            companyInfo
        }
    }
})
</script>