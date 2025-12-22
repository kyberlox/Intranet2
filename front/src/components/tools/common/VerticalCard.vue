<template>
<div :class="{ 'vertical-card--bg': page !== 'care' }"
     :style="{ backgroundImage: `url('${card.preview_file_url}')` }">
    <div v-if="page == 'safetyTechnics' || (modifiers && modifiers.includes('needLogo'))"
         class="vertical-card__item__banner">
        <span class="vertical-card__item__banner__inner">
            <span v-if="page == 'safetyTechnics'"
                  class="vertical-card__item__category">
                {{ card.header }}
            </span>
            <div class="vertical-card__item__logo">
                <img src="@/assets/imgs/emkLogo.webp"
                     alt="ЭМК"
                     title="ЭМК" />
            </div>
            <h3 class="vertical-card__item__title"
                :class="{ 'vertical-card__item__title--care': page == 'care' }">
                {{
                    page == 'safetyTechnics' ?
                        card.name :
                        card.indirect_data?.theme
                }}
            </h3>
            <RouterLink v-if="page == 'safetyTechnics' || page == 'care'"
                        :to="{ name: card.routeTo ?? routeTo, params: { id: card.id } }"
                        class="vertical-card__item__link">
                Читать
            </RouterLink>
        </span>
    </div>
    <div class="vertical-card__item__subtitle__wrapper">
        <div class="vertical-card__item__subtitle vertical-title">
            <span> {{ card.subtitle ?? card.name }}</span>
        </div>
        <div v-if="card.description"
             class="vertical-card__item__subtitle vertical-subtitle">
            <span> {{ card.description }}</span>
        </div>
        <div v-if="card.indirect_data?.organizer"
             class="vertical-card__item__subtitle vertical-subtitle">
            <span> {{ 'Организатор: ' + card.indirect_data?.organizer }}</span>
        </div>
    </div>
</div>
</template>

<script lang="ts">
import { defineComponent, type PropType } from "vue";

interface IVerticalCard {
    header?: string,
    preview_file_url?: string,
    name?: string,
    user_fio?: string,
    position?: string,
    department?: string,
    routeTo?: string,
    id?: number,
    subtitle?: string,
    description?: string,
    indirect_data?: {
        // для благотворительных
        organizer: string,
        phone_number: string,
        theme?: string,
    }
}

export default defineComponent({
    name: 'VerticalCard',
    props: {
        card: {
            type: Object as PropType<IVerticalCard>,
            required: true
        },
        page: {
            type: String as PropType<'safetyTechnics' | 'care'>
        },
        modifiers: {
            type: Array<string>
        },
        routeTo: String
    },
    setup() {
        return {

        }
    }
}
)
</script>
