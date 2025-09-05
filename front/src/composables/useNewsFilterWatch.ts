import { type Ref, ref } from "vue";
import Api from "@/utils/Api";
import type { INews } from "@/interfaces/IEntities";
import { sectionTips } from "@/assets/static/sectionTips";
import { extractYears } from "@/utils/extractYearsFromPosts";

export const useNewsFilterWatch = async (currentTag: Ref<string>, currentYear: Ref<string>, allNews: Ref<INews[]>, visibleNews: Ref<INews[]>) => {

    const newVisibleNews: Ref<INews[]> = ref([]);
    const newFilterYears: Ref<string[]> = ref([]);
    const newEmptyTag: Ref<boolean> = ref(false);

    if ((currentTag.value && currentYear.value) || (currentTag.value && !currentYear.value)) {
        const newData: Ref<INews[]> = ref([]);
        await Api.get(`article/get_articles_by_tag_id/${sectionTips['АктуальныеНовости']}/${currentTag.value}`)
            .then((data: INews[]) => {
                newData.value = data.filter((e) => {
                    return e.date_creation?.includes(currentYear.value)
                })
            })
            .finally(() => {
                if (!newData.value.length) {
                    newEmptyTag.value = true;
                } else {
                    newVisibleNews.value = newData.value;
                    newFilterYears.value = extractYears(newData.value);
                    newEmptyTag.value = false;
                }
            })
    }
    else if ((!currentTag.value && currentYear.value) || (!currentTag.value && !currentYear.value)) {
        newVisibleNews.value = allNews.value.filter((e) => {
            return e.date_creation?.includes(currentYear.value)
        });
        newFilterYears.value = extractYears(allNews.value);
        newEmptyTag.value = newVisibleNews.value.length === 0;
    }


    return {
        newVisibleNews,
        newFilterYears,
        newEmptyTag
    }
}