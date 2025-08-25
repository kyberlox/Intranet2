import { watch, type Ref, ref } from "vue";
import Api from "@/utils/Api";
import type { INews } from "@/interfaces/IEntities";
import { sectionTips } from "@/assets/static/sectionTips";
import { extractYears } from "@/utils/extractYearsFromPosts";

export const useNewsFilterWatch = (currentTag: Ref<string>, currentYear: Ref<string>, allNews: Ref<INews[]>) => {

    const visibleNews = ref();
    const filterYears = ref();
    const emptyTag = ref();

    watch(([currentTag, currentYear]), () => {
        if (currentTag.value && currentYear.value || currentTag.value && !currentYear.value) {
            const newData = ref();
            Api.get(`article/get_articles_by_tag_id/${sectionTips['АктуальныеНовости']}/${currentTag.value}`)
                .then((data: INews[]) => newData.value = data.filter((e) => {
                    return e.date_creation?.includes(currentYear.value)
                }))
                .finally(() => {
                    if (!newData.value.length) return emptyTag.value = true;
                    visibleNews.value = newData.value;
                    filterYears.value = extractYears(visibleNews.value);
                    emptyTag.value = false;
                })
        }
        else if ((!currentTag.value && currentYear.value) || (!currentTag.value && !currentYear.value)) {
            filterYears.value = extractYears(visibleNews.value);
            visibleNews.value = allNews.value.filter((e) => {
                return e.date_creation?.includes(currentYear.value)
            })
            return visibleNews.value.length ? emptyTag.value = false : emptyTag.value = true;
        }
    })

    return {
        visibleNews,
        filterYears,
        emptyTag
    }
}