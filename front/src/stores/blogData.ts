import { defineStore } from "pinia";
import type { IBlog, IBlogAuthors } from "@/interfaces/IEntities";

export const useblogDataStore = defineStore('blogData', {
    state: () => ({
        allAuthors: [] as IBlogAuthors[],
        allBlogs: [] as IBlog[],
    }),

    actions: {
        setAuthors(authors: IBlogAuthors[]) {
            this.allAuthors = authors;
        },
        setAllBlogs(blogs: IBlog[]) {
            this.allBlogs = blogs;
        }
    },

    getters: {
        getAllAuthors: (state) => state.allAuthors,
        getCurrentAuthor: (state) => (x: string) => state.allAuthors.find(e => e.authorId == Number(x)),
        getCurrentArticles: (state) => (x: string) => state.allBlogs.filter(e => e.indirect_data && (e.indirect_data['PROPERTY_453'] == x || e.indirect_data['PROPERTY_451'] == x)),
        getBlogById: (state) => (x: string) => state.allBlogs.find(e => String(e.id) == x),
    }
});