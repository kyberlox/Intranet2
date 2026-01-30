<template>
<div class="mt20">
    <div class="page__title">Капитал ЭМК</div>
    <div class="modal__text__content__points-info">
        <span>
            Уважаемые коллеги!
            <br />
            «Капитал ЭМК» - это ваш персональный бонусный клуб внутри компании: <br /> за труд, инициативу и достижения
            вы
            получаете баллы, которые можно обменять на товары из корпоративного каталога.


            <br />
            <strong>Важно</strong>: в программе учитывается стаж работы в компании - от него зависит начисление ряда
            баллов.
            <br />
            <strong>Пожалуйста, проверьте в своём личном кабинете дату трудоустройства.</strong>
            <br /> Если вы обнаружили неточность:
            <ul>
                <li>обратитесь к нам (тел. 5182/5185) - мы поможем внести корректную дату</li>
                <li>если вы помните только год трудоустройства, мы приурочим дату (день и месяц) ко Дню машиностроителя.
                </li>
            </ul>
            Перейти в каталог можно по кнопке, а ниже можно ознакомиться с перечнем активностей и стоимостью баллов за
            каждую из них.
        </span>
        <RouterLink :to="{ name: 'merchStore' }"
                    class="primary-button">Каталог ЭМК</RouterLink>
        <div class="block">
            <CapitalActivityTable :title="'Активности'"
                                  :allActivities="allActivities.filter((e) => e.id < 21)" />
            <!-- ">20" это юбилейные активности -->
            <CapitalActivityTable :title="'Баллы за время в компании'"
                                  :allActivities="allActivities.filter((e) => e.id > 20)" />
        </div>
    </div>
</div>
</template>

<script lang="ts">
import { defineComponent, onMounted, ref, computed } from 'vue';
import Api from '@/utils/Api';
import { sectionTips } from '@/assets/static/sectionTips';
import type { IMerch } from '@/interfaces/entities/IMerch';
import type { IBXFileType } from '@/interfaces/IEntities';
import { usePointsData } from '@/stores/pointsData';
import { featureFlags } from '@/assets/static/featureFlags';
import CapitalActivityTable from './CapitalActivityTable.vue';

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
        }
    }
})
</script>

<style>
.block {
    display: flex;
    flex-direction: row;
    align-items: baseline;
    gap: 15px;

}
</style>