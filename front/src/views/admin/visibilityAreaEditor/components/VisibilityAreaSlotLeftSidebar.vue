<template>
    <nav class="admin-panel__nav">
        <h6 class="admin-panel__nav-title mt20">Области</h6>
        <ul class="admin-panel__nav-list">
            <li v-for="(area, index) in visibilityAreas"
                :key="'section' + index"
                class="admin-panel__nav-item"
                @click="$emit('areaClicked', area.id)">
                <div class="admin-panel__nav-link"
                     :class="{ 'admin-panel__nav-link--active': activeId == area.id }">
                    <div class="admin-panel__nav-icon">
                        <NavArrow />
                    </div>
                    <span class="admin-panel__nav-text">{{ area.vision_name }}</span>
                </div>
            </li>
        </ul>
        <div class="admin-panel__nav__button-group">
            <button class="admin-panel__nav__button primary-button"
                    @click="$emit('addNewArea')">Создать</button>
            <button v-if="activeId"
                    class="admin-panel__nav__button primary-button"
                    @click="$emit('deleteArea', activeId)">Удалить</button>
        </div>
    </nav>
</template>

<script lang="ts">
import { defineComponent, type PropType } from 'vue';
import NavArrow from "@/assets/icons/admin/NavArrow.svg?component"
export default defineComponent({
    props: {
        visibilityAreas: {
            type: Array as PropType<{ id: number, vision_name: string }[]>
        },
        activeId: {
            type: Number,
        }
    },
    components: {
        NavArrow
    },
    setup() {
        return {

        }
    }
})
</script>