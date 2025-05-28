<template>
    <h2 class="page__title mt20">
        Новые сотрудники
    </h2>

    <div class="row mb-5 mt20">
        <div class="staff__item-wrapper col-sm-2"
             v-for="item in newWorkers"
             :key="item.id">
            <RouterLink :to="{ name: item.href, params: { id: item.id } }"
                        class="staff__item">
                <img class="img-fluid staff__item-img"
                     src="/src/assets/imgs/about/yearResults/gazinskii.png" />
                <div class="staff__item-name">
                    {{ item.name }}
                </div>
            </RouterLink>
            <div class="staff__item-position">{{ item.position }}</div>
            <div class="staff__item-organisation">{{ item.department }}</div>
        </div>
    </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue';
import { RouterLink } from 'vue-router';

export default defineComponent({
    name: "newWorkers",
    components: {
        RouterLink
    },
    setup() {
        const newWorkers = [{
            id: 1,
            name: 'Иванов Иван Иванович',
            position: 'Директор',
            department: 'Отдел продаж',
            href: 'userPage',
        }]
        return {
            newWorkers,
        }
    }
})
</script>