import Api from "./Api"
import type { Ref } from "vue"
import { getProperty } from "./getPropertyFirstPos"
import { sectionTips } from "@/assets/staticJsons/sectionTips"
import type { IBlogAuthors, IBlog } from "@/interfaces/IEntities"
import type { useblogDataStore } from "@/stores/blogData"
import { propertyCheck } from "@/utils/propertyCheck";

const setAuthorId = (e: IBlog): string => {
    if (propertyCheck(e.indirect_data, 'PROPERTY_451')) {
        return getProperty(e, 'PROPERTY_451');
    }
    else if (propertyCheck(e.indirect_data, 'PROPERTY_1022')) {
        return getProperty(e, 'PROPERTY_1022')
    }
    else {
        return '0'
    }
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