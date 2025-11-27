import { defineStore } from "pinia";

export const useStyleModeStore = defineStore('styleModeStore', {
    state: () => ({
        darkMode: true,
    }),

    actions: {
        setDarkMode(value: boolean){
            this.darkMode = value
        }
    },

    getters: {
        getDarkMode: (state) => state.darkMode,
    }
});