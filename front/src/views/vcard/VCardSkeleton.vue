<template>
<div class="vcard vcard--loading">
    <div class="vcard__photo vcard__photo--skeleton skeleton-grid__gallery-image">
    </div>
    <div class="vcard__content">
        <div class="vcard__header">
            <div class="skeleton-flex__gallery-date skeleton-flex__gallery-date--long"></div>
        </div>
        <div class="vcard__employee__info">
            <div class="vcard__employee__info__item">
                <div>
                    <div class="skeleton-flex__gallery-date"></div>
                </div>
                <div>
                    <div class="skeleton-flex__gallery-date"></div>
                </div>
            </div>
            <div class="vcard__employee__info__item">
                <div>
                    <div class="skeleton-flex__gallery-date"></div>
                </div>
                <div>
                    <div class="skeleton-flex__gallery-date"></div>
                </div>
            </div>
            <div class="vcard__employee__info__item">
                <div>
                    <div class="skeleton-flex__gallery-date"></div>
                </div>
                <div>
                    <div class="skeleton-flex__gallery-date"></div>
                </div>
            </div>
        </div>
        <div class="vcard__button-wrapper">
            <div class="btn btn--loading">
                <Loader />
            </div>
        </div>
        <VCardCompany />
    </div>
</div>
</template>

<script lang="ts">
import { defineComponent } from "vue";
import VCardCompany from "./VCardCompany.vue";
import Loader from "@/components/layout/Loader.vue";

export default defineComponent({
    components: {
        VCardCompany,
        Loader
    },
    setup() {

        return {

        }
    }
})
</script>