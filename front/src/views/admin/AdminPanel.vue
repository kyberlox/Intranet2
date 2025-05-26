<template>
    <div class="page__title mt20">Панель редактора</div>
    <div class="row">
        <h6>Выберите раздел</h6>
        <div class="admin-page__selector">
            <div class="admin-page__section__wrapper">
                <RouterLink v-for="(section, index) in sections"
                            :key="'section' + index"
                            :to="{ name: 'adminBlockInner', params: { id: section.id } }"
                            class="admin-page__section">
                    <span class="admin-page__section-link">
                        <div class="admin-page__section-icon">
                            <img src="https://portal.emk.ru/bitrix/images/lists/nopic_list_150.png"
                                 width="36"
                                 height="30"
                                 alt="" />
                        </div>
                        <span class="admin-page__section-title-wrapper">
                            <span class="admin-page__section-title">{{ section.name }}</span>
                        </span>
                    </span>
                </RouterLink>
            </div>
        </div>
    </div>
</template>

<script lang="ts">
import { computed, defineComponent, onMounted, ref } from 'vue';
import { useUserData } from '@/stores/userData';
import Api from '@/utils/Api';

export default defineComponent({
    setup() {
        const myId = computed(() => useUserData().getMyId)
        const sections = ref();
        onMounted(() => {
            Api.get('section/all')
                .then((res) => {
                    sections.value = res;
                })
        })

        return {
            myId,
            sections
        }
    }
})
</script>

<style lang="scss" scoped>
.admin-page__section {
    position: relative;
    background: #f2f6f7;
    border-radius: 5px;
    height: 80px;
    width: calc(20% - 13px);
    margin: 13px 13px 0 0;
    transition: 0.2ms;
    float: left;

    &:hover {
        transform: scale(1.02);
        background: #d3d6d6;
    }
}

@media(max-width: 1600px) {
    .admin-page__section {
        width: calc(25% - 13px)
    }
}

@media(max-width: 1280px) {
    .admin-page__section {
        width: calc(33% - 13px)
    }
}

.admin-page__section-link {
    padding: 9px 11px;
    display: flex;
    align-items: center;
    z-index: 1
}

.admin-page__section-title:hover .bx-lists-application-link {
    text-decoration: underline
}

.admin-page__section-icon {
    max-width: 55px;
    min-width: 55px;
    height: 55px;
    border-radius: 50%;
    background: #fff;
    display: block;
    overflow: hidden;
    position: relative
}

.admin-page__section-icon img {
    position: absolute;
    margin: auto;
    top: 0;
    right: 0;
    left: 0;
    bottom: 0
}

.admin-page__section-title-wrapper {
    flex: 1;
    padding-left: 10px;
    box-sizing: border-box;
    max-width: calc(100% - 55px)
}

.admin-page__section-title {
    overflow: hidden;
    display: block;
    font: var(--ui-font-weight-bold) 14px/18px var(--ui-font-family-primary, var(--ui-font-family-helvetica));
    white-space: nowrap;
    text-overflow: ellipsis;
    vertical-align: middle;
    color: #000
}

.admin-page__section-check {
    vertical-align: middle
}

.admin-page__section-check label {
    vertical-align: middle;
    font: 11px var(--ui-font-family-primary, var(--ui-font-family-helvetica));
    color: #000
}

.admin-page__section-check label:hover,
.admin-page__section-check input:checked+label {
    color: #000
}

.admin-page__section-check input {
    vertical-align: middle;
    margin: 0
}

.bx-lists-alert {
    background-color: #fffcde;
    color: #000;
    font-size: 15px;
    min-height: 45px;
    text-align: center;
    padding: 12px 40px 12px 60px;
    position: relative;
    width: 280px
}

.bx-lists-aligner {
    display: inline-block;
    height: 45px;
    margin-left: -1px;
    vertical-align: middle;
    width: 1px
}

.bx-lists-alert-text {
    display: inline-block;
    vertical-align: middle
}

.bx-lists-alert-footer {
    text-align: center
}

.bx-lists-alert-popup {
    background-color: #fffcde !important;
    border: 1px solid #f0f0f0 !important
}

.admin-page__section-title .bx-lists-application-link span:after {
    content: '';
    position: absolute;
    top: 0;
    right: 0;
    bottom: 0;
    height: 36px;
    width: 20px;
    background: -webkit-gradient(linear, left top, right top, from(rgba(255, 255, 255, 0)), to(#f2f6f7), color-stop(95%, #f2f6f7));
    background: -moz-linear-gradient(to right, rgba(255, 255, 255, 0), #f2f6f7 95%, #f2f6f7);
    background: -o-linear-gradient(to right, rgba(255, 255, 255, 0), #f2f6f7 95%, #f2f6f7);
    background: -ms-linear-gradient(to right, rgba(255, 255, 255, 0), #f2f6f7 95%, #f2f6f7);
    background: linear-gradient(to right, rgba(255, 255, 255, 0), #f2f6f7 95%, #f2f6f7)
}

.admin-page__section-title .bx-lists-application-link span {
    max-height: 36px;
    overflow: hidden;
    position: relative;
    display: block;
    white-space: nowrap;
    text-overflow: ellipsis
}
</style>