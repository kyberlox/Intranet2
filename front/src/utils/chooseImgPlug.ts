import winterPlug from "@/assets/imgs/plugs/winter.jpg";
import autumnPlug from "@/assets/imgs/plugs/autumn.jpg";
import summerPlug from "@/assets/imgs/plugs/summer.jpg";
import springPlug from "@/assets/imgs/plugs/spring.jpg";

import ideaPlug from "@/assets/imgs/plugs/bannerIdea.jpg";
import orgPlug from "@/assets/imgs/plugs/bannerOrg.jpg";
import { type IHomeViewSoloBlock } from "@/views/homeView/components/MainPageSoloBlock.vue";

export const chooseImgPlug = (card: IHomeViewSoloBlock | null = null): string => {
    // заглушка для баннера есть идея
    if (card && card.id == 4 && !card.images[0]?.image) {
        return ideaPlug
    }
    // заглушка для баннера орг развития
    else if (card && card.id == 32 && !card?.images[0]?.image) {
        return orgPlug
    }
    // заглушка для ост баннеров
    else {
        const currentMonth = new Date().getMonth() + 1;
        if (currentMonth in [12, 1, 2]) {
            return winterPlug
        }
        else if (currentMonth in [3, 4, 5]) {
            return autumnPlug
        }
        else if (currentMonth in [6, 7, 8]) {
            return summerPlug
        }
        else
            return springPlug
    }
}