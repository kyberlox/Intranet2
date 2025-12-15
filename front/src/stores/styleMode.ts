import { defineStore } from "pinia";

export const useStyleModeStore = defineStore('styleModeStore', {
    state: () => ({
        darkMode: false,
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