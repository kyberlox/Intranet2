export const chooseImgPlug = () => {
    const currentMonth = new Date().getMonth() + 1;
    if (currentMonth in [12, 1, 2]) {
        return '@/assets/imgs/plugs/winter.jpg'
    }
    else if (currentMonth in [3, 4, 5]) {
        return '@/assets/imgs/plugs/autumn.jpg'
    }
    else if (currentMonth in [6, 7, 8]) {
        return '@/assets/imgs/plugs/summer.jpg'
    }
    else return '@/assets/imgs/plugs/spring.jpg'
}