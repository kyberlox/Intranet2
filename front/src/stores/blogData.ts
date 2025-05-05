import { defineStore } from "pinia";

export const useblogDataStore = defineStore('blogData', {
    state: () => ({
        allBlogs: [],
        allAuthors: [],
    }),

    actions: {
        setAuthors(authors) {
            this.allAuthors = authors;
        },
        setAllBlogs(blogs) {
            console.log(blogs);
            this.allBlogs = blogs;
        }
    },

    getters: {
        getAllAuthors: (state) => state.allAuthors,
        getCurrentAuthor: (state) => (x: string) => state.allAuthors.find(e => e.authorId == x),
        getCurrentArticles: (state) => (x: string) => state.allBlogs.filter(e => e.indirect_data['PROPERTY_453'] == x || e.indirect_data['PROPERTY_451'] == x),
        getBlogById: (state) => (x: string) => state.allBlogs.find(e => e.id == x),
    }
});