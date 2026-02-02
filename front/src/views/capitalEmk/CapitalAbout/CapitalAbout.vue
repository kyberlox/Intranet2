<template>
<div class="mt20">
    <div class="page__title">Капитал ЭМК</div>
    <div v-if="myId"
         class="modal__text__content__points-info">
        <span>
            Уважаемые коллеги!
            <br />
            «Капитал ЭМК» - это ваш персональный бонусный клуб внутри компании: <br /> за труд, инициативу и достижения
            Вы
            получаете баллы, которые можно обменять на товары из
            <RouterLink :to="{ name: 'merchStore' }">
                <strong class="link">корпоративного
                    магазина мерча.</strong>
            </RouterLink>
            <br />
            <strong>Важно</strong>: в программе учитывается стаж работы в компании - от него зависит начисление ряда
            баллов.
            <br />
            <RouterLink :to="{ name: 'userPage', params: { id: myId } }">
                Пожалуйста, проверьте в своём <strong class="link"> личном кабинете</strong> дату трудоустройства.
            </RouterLink>
            <br /> Если Вы обнаружили неточность:
            <ul>
                <li>обратитесь к нам (тел. 5182/5185 или на почту it.dpm@emk.ru) - мы поможем внести корректную дату
                </li>
                <li>
                    если Вы помните только год трудоустройства, мы приурочим дату (день и месяц) ко Дню машиностроителя,
                    для этого также сообщите нам (тел. 5182/5185).
                </li>
            </ul>
            Как потратить баллы
        </span>
        <RouterLink :to="{ name: 'merchStore' }"
                    class="primary-button">
            Магазин мерча
        </RouterLink>
        <div class="block">
            Ниже можно ознакомиться с перечнем событий и достижений и
            стоимостью
            баллов за
            каждую из них.
            <CapitalActivityTable :title="'За что начисляют баллы'"
                                  :allActivities="allActivities.filter((e) => !e.name.includes('Годовщина') && !e.name.includes('Юбилейная')).sort((a, b) => a.coast - b.coast)" />
            <CapitalActivityTable :title="'Баллы за стаж работы в компании'"
                                  :allActivities="allActivities.filter((e) => e.name.includes('Годовщина') || e.name.includes('Юбилейная')).sort((a, b) => a.coast - b.coast)" />
        </div>
    </div>
</div>
</template>

<script lang="ts">
import { defineComponent, ref, computed } from 'vue';
import type { IMerch } from '@/interfaces/entities/IMerch';
import { usePointsData } from '@/stores/pointsData';
import { featureFlags } from '@/assets/static/featureFlags';
import CapitalActivityTable from './CapitalActivityTable.vue';
import { useUserData } from '@/stores/userData';

export default defineComponent({
    components: {
        CapitalActivityTable
    },
    setup() {
        const allActivities = computed(() => usePointsData().getActivities);
        const pointsAboutOpen = ref(false);
        const merchItems = ref<IMerch[]>([]);
        const isLoading = ref<boolean>(false);

        return {
            merchItems,
            isLoading,
            allActivities,
            pointsAboutOpen,
            featureFlags,
            myId: computed(() => useUserData().getMyId),
        }
    }
})
</script>

<style>
.block {
    display: flex;
    flex-direction: column;
    align-items: baseline;
    gap: 15px;

}
</style>