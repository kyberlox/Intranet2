import Api from "./Api"
import type { Ref } from "vue"
import { sectionTips } from "@/assets/static/sectionTips"
import type { IBlogAuthors, IBlog } from "@/interfaces/IEntities"
import type { useblogDataStore } from "@/stores/blogData"

export const getBlogAuthorsToStore = (allAuthors: Ref<IBlogAuthors[]>, blogData: ReturnType<typeof useblogDataStore>) => {
    const uniqAuthors = [];
    Api.get(`article/find_by/${sectionTips['Блоги']}`)
        .then(res => {
            res.map((e: IBlog) => {
                if (e.indirect_data?.TITLE) {
                    const newAuthor: IBlogAuthors = {
                        title: e.indirect_data.TITLE,
                        authorId: e.indirect_data.author_uuid ?? e.indirect_data.company,
                        authorAvatar: e.preview_file_url ?? e.indirect_data.photo_file_url,
                        link: e.indirect_data.link ?? null
                    }
                    console.log(newAuthor);
                    if (!uniqAuthors.length || !uniqAuthors.find((e) => e.title == newAuthor.title)) {
                        uniqAuthors.push(newAuthor)
                    }
                    allAuthors.value = uniqAuthors;
                }
            })

            blogData.setAllBlogs(res);
            blogData.setAuthors(allAuthors.value);
        })
}