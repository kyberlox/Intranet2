import Api from "./Api"
import type { Ref } from "vue"
import { sectionTips } from "@/assets/staticJsons/sectionTips"
import type { IBlogAuthors, IBlog } from "@/interfaces/INewBlog"
import type { useblogDataStore } from "@/stores/blogData"
export const getBlogAuthorsToStore = (allAuthors: Ref<IBlogAuthors[]>, blogData: ReturnType<typeof useblogDataStore>) => {
    Api.get(`article/find_by/${sectionTips['Блоги']}`)
        .then(res => {
            res.map((e: IBlog) => {
                if (e.indirect_data && e.indirect_data.TITLE && e.indirect_data.ID && (e.indirect_data.PROPERTY_451 || e.indirect_data.PROPERTY_453)) {
                    const newAuthor: IBlogAuthors = {
                        title: e.indirect_data.TITLE,
                        id: e.indirect_data.ID,
                        authorId: e.indirect_data.PROPERTY_451 ? e.indirect_data.PROPERTY_451[0] : e.indirect_data.PROPERTY_453 ? e.indirect_data.PROPERTY_453[0] : '0',
                    }
                    allAuthors.value.push(newAuthor);
                }
            })

            blogData.setAllBlogs(res);
            blogData.setAuthors(allAuthors.value);
        })
}