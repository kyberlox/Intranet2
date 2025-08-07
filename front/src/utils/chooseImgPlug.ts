import winterPlug from "@/assets/imgs/plugs/winter.jpg";
import autumnPlug from "@/assets/imgs/plugs/autumn.jpg";
import summerPlug from "@/assets/imgs/plugs/summer.jpg";
import springPlug from "@/assets/imgs/plugs/spring.jpg";

export const chooseImgPlug = () => {
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
    else return springPlug
}