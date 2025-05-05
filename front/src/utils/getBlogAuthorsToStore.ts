import type { Store } from "pinia"
import Api from "./Api"
import { sectionTips } from "@/assets/staticJsons/sectionTips"
export const getBlogAuthorsToStore = (allAuthors, blogData: Store) => {
    Api.get(API_URL + `article/find_by/${sectionTips['Блоги']}`)
        .then(res => {
            res.map((e) => {
                if (e.indirect_data.TITLE) {
                    const newAuthor = {
                        title: e.indirect_data.TITLE,
                        id: e.indirect_data.ID,
                        authorId: e.indirect_data.PROPERTY_451 ? e.indirect_data.PROPERTY_451[0] : e.indirect_data.PROPERTY_453[0],
                    }
                    allAuthors.value.push(newAuthor);
                }
            })
            blogData.setAllBlogs(res);
            blogData.setAuthors(allAuthors.value);
        })
}