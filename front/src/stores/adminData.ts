import { defineStore } from "pinia";

interface IAdminSections {
    id: number | string,
    name: string,
}

export const useAdminData = defineStore('adminData', {
    state: () => ({
        sections: [] as IAdminSections[],
    }),

    actions: {
        setSections(sections: IAdminSections[]) {
            this.sections = sections.sort((a, b) => a.name.localeCompare(b.name));
        }
    },

    getters: {
        getSections: (state) => state.sections,
    }
});
