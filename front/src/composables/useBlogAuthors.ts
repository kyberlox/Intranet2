import Api from "../utils/Api"
import { sectionTips } from "@/assets/static/sectionTips"
import type { IBlogAuthors, IBlog } from "@/interfaces/IEntities"
import { useblogDataStore } from "@/stores/blogData"
import avatarPlug from '@/assets/imgs/plugs/userplug.jpg'

export const getBlogAuthorsToStore = async () => {
    const blogsData = useblogDataStore();
    const shouldRecomputeAuthors = blogsData.getAllAuthors.length === 0;
    if (!shouldRecomputeAuthors) return;
    const uniqAuthors: IBlogAuthors[] = [];
        try {
            const res = await Api.get(`article/find_by/${sectionTips['Блоги']}`)
            res.map((e: IBlog) => {
                if (e.indirect_data) {
                    const isUser = 'users' in e.indirect_data && !(('company' in e.indirect_data) && e.indirect_data.company);
                    const newAuthor: IBlogAuthors = {
                        title: isUser ? e.indirect_data.users.TITLE : e.indirect_data.company,
                        authorId: isUser ?  e.indirect_data.users?.id : e.indirect_data.manufacture_id,
                        authorAvatar: isUser ? e.indirect_data.users.photo_file_url : e.preview_file_url ? e.preview_file_url : avatarPlug,
                        authorTitle: isUser ? String(e.indirect_data.users.TITLE) : String(e.indirect_data.company),
                        isCompany: !isUser,
                        companyId: isUser ? null : e.indirect_data.manufacture_id,
                        users: !isUser ? e.indirect_data.users : null
                        // link: e.indirect_data.users.link ?? null,
                        // !!! Сечас в preview_file_url приходят заводы, а в photo_file_url - фото людей, у земской приходит и preview, в нем QR !!!
                        // telegramQr: e.preview_file_url && e.indirect_data.photo_file_url ? e.preview_file_url : ''
                    }
                    if (!uniqAuthors.length || !uniqAuthors.some((e) =>( e.title == newAuthor.title || e.authorId == newAuthor.authorId))) {
                        uniqAuthors.push(newAuthor)
                    }
                    if(newAuthor.authorAvatar && uniqAuthors.some((e) => e.authorId == newAuthor.authorId)) {
                        uniqAuthors.find((e) => e.authorId == newAuthor.authorId)!.authorAvatar = newAuthor.authorAvatar
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
