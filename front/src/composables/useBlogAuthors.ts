import Api from "../utils/Api"
import { sectionTips } from "@/assets/static/sectionTips"
import type { IBlogAuthors, IBlog } from "@/interfaces/IEntities"
import { useblogDataStore } from "@/stores/blogData"

export const getBlogAuthorsToStore = async () => {
    const blogsData = useblogDataStore();
    const uniqAuthors: IBlogAuthors[] = [];
    if (!blogsData.getAllAuthors.length)
        try {
            const res = await Api.get(`article/find_by/${sectionTips['Блоги']}`)
            res.map((e: IBlog) => {
                if (e.indirect_data) {
                    const isUser = 'users' in e.indirect_data && !(('company' in e.indirect_data) && e.indirect_data.company);
                    // console.log(e)
                    console.log(isUser ? '' : e)
                    const newAuthor: IBlogAuthors = {
                        title: isUser ? e.indirect_data.users.TITLE : e.indirect_data.TITLE,
                        authorId: isUser ? e.indirect_data.users?.id : e.indirect_data.company,
                        authorAvatar: isUser ? e.indirect_data.users.photo_file_url : e.preview_file_url,
                        authorTitle: isUser ? e.indirect_data.users.TITLE : e.indirect_data.author,
                        isCompany: !isUser,
                        // link: e.indirect_data.users.link ?? null,
                        // !!! Сечас в preview_file_url приходят заводы, а в photo_file_url - фото людей, у земской приходит и preview, в нем QR !!!
                        // telegramQr: e.preview_file_url && e.indirect_data.photo_file_url ? e.preview_file_url : ''
                    }
                    if (!uniqAuthors.length || !uniqAuthors.find((e) => e.title == newAuthor.title)) {
                        uniqAuthors.push(newAuthor)
                    }
                }
            })
            blogsData.setAllBlogs(res);
            blogsData.setAuthors(uniqAuthors);
        }
        catch (error) {
            console.error(error)
        }
}
