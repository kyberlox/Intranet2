<template>
    <nav>
        <h6 class="admin-panel__nav-title mt20">Области</h6>
        <!-- <ul class="admin-panel__nav-list">
            <li v-for="(area, index) in userPicks"
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
        </ul> -->
        <div class="mt20"
             @click="$emit('addNewArea')">Добавить</div>
    </nav>
</template>

<script lang="ts">
import { defineComponent, ref } from 'vue';

export default defineComponent({
    name: 'visibilityAreaRightSidebar',
    components: {

    },
    props: {

    },
    emits: ['areaClicked', 'addNewArea'],
    setup() {
        const userPicks = ref([]);

        return {
            userPicks
        }
    }
})
</script>