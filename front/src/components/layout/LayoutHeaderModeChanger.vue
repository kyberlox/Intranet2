<template>
<div>
    <NightIcon v-if="!theme"
               class="navbar-nav__search-icon"
               @click="toggleDarkMode(true)" />
    <DayIcon v-else
             class="navbar-nav__search-icon"
             @click="toggleDarkMode(false)" />
</div>
</template>

<script lang="ts">
import { computed, onMounted, defineComponent } from 'vue';
import DayIcon from '@/assets/icons/layout/DayIcon.svg?component';
import NightIcon from '@/assets/icons/layout/NightIcon.svg?component';
import { useStyleModeStore } from '@/stores/styleMode';
export default defineComponent({
    components: {
        DayIcon,
        NightIcon
    },
    setup() {
        const styleMode = useStyleModeStore();

        onMounted(() => {
            const savedTheme = localStorage.getItem('darkMode');
            if (!savedTheme || savedTheme == 'false') {
                toggleDarkMode(false)
            }
            else {
                toggleDarkMode(true)
            }
        })

        const toggleDarkMode = (value: boolean) => {
            localStorage.setItem('darkMode', String(value));
            styleMode.setDarkMode(value);
        }
        
        return {
            toggleDarkMode,
            theme: computed(() => styleMode.getDarkMode)
        }
    }
})
</script>