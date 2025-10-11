import Api from "../utils/Api"
import { sectionTips } from "@/assets/static/sectionTips"
import type { IBlogAuthors, IBlog } from "@/interfaces/IEntities"
import { useblogDataStore } from "@/stores/blogData"

export const getBlogAuthorsToStore = () => {
    const blogsData = useblogDataStore();
    const uniqAuthors: IBlogAuthors[] = [];

    Api.get(`article/find_by/${sectionTips['Блоги']}`)
        .then(res => {
            res.map((e: IBlog) => {
                if (e.indirect_data?.TITLE) {
                    const newAuthor: IBlogAuthors = {
                        title: e.indirect_data.TITLE,
                        authorId: e.indirect_data.author_uuid ?? e.indirect_data.company,
                        authorAvatar: e.indirect_data.photo_file_url ?? e.preview_file_url,
                        authorTitle: e.indirect_data.author,
                        link: e.indirect_data.link ?? null,
                        // !!! Сечас в preview_file_url приходят заводы, а в photo_file_url - фото людей, у земской приходит и preview, в нем QR !!!
                        telegramQr: e.preview_file_url && e.indirect_data.photo_file_url ? e.preview_file_url : ''
                    }
                    if (!uniqAuthors.length || !uniqAuthors.find((e) => e.title == newAuthor.title)) {
                        uniqAuthors.push(newAuthor)
                    }
                }
            })
            blogsData.setAllBlogs(res);
            blogsData.setAuthors(uniqAuthors);
        })
}
