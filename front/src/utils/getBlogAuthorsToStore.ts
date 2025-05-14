import Api from "./Api"
import type { Ref } from "vue"
import { getProperty } from "./fieldChecker"
import { sectionTips } from "@/assets/staticJsons/sectionTips"
import type { IBlogAuthors, IBlog } from "@/interfaces/IEntities"
import type { useblogDataStore } from "@/stores/blogData"
const setAuthorId = (e: IBlog): string => {
    switch (true) {
        case getProperty(e, 'PROPERTY_451'):
            getProperty(e, 'PROPERTY_451')
            break;
        case getProperty(e, 'PROPERTY_453'):
            getProperty(e, 'PROPERTY_451')
            break;
        default:
            return '0'
    }
    return ''
}
export const getBlogAuthorsToStore = (allAuthors: Ref<IBlogAuthors[]>, blogData: ReturnType<typeof useblogDataStore>) => {
    Api.get(`article/find_by/${sectionTips['Блоги']}`)
        .then(res => {
            res.map((e: IBlog) => {
                const authorId = setAuthorId(e);
                if (e.indirect_data && e.indirect_data.TITLE && e.indirect_data.ID && authorId && (e.indirect_data.PROPERTY_451 || e.indirect_data.PROPERTY_453)) {
                    const newAuthor: IBlogAuthors = {
                        title: e.indirect_data.TITLE,
                        id: e.indirect_data.ID,
                        authorId: authorId
                    }
                    allAuthors.value.push(newAuthor);
                }
            })

            blogData.setAllBlogs(res);
            blogData.setAuthors(allAuthors.value);
        })
}