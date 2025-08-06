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
        getAllBlogs: (state) => state.allBlogs,
        getCurrentAuthor: (state) => (x: string) => state.allAuthors.find(e => e.authorId == Number(x)),
        getCurrentArticles: (state) => (x: number) => state.allBlogs.filter((e) => e.indirect_data && ((e.indirect_data.author_uuid == x) || e.indirect_data.company == x)),
        getBlogById: (state) => (x: string) => state.allBlogs.find(e => String(e.id) == x),
    }
});