export const repairVideoUrl = (url: string): string | false => {
    if (!url) return '/';
    console.log(url);

    let cleanUrl = url;

    const youtubePatterns = ["youtu.be/", "watch?v=", "/shorts/", "youtube.com/embed/"];

    const rutubePattern = "https://rutube.ru/video/";

    if (url.includes(rutubePattern)) {
        cleanUrl = url.replace(rutubePattern, "https://rutube.ru/video/embed/");
        return cleanUrl;
    }
    else
        youtubePatterns.forEach((item) => {
            const keyIndex = url.indexOf(item);

            if (keyIndex == -1) return;

            const videoId = url.substring(keyIndex + item.length).split("&")[0];
            console.log(url);

            console.log(videoId);

            cleanUrl = `https://www.youtube.com/embed/${videoId}`;
            return cleanUrl;
        })
    console.log(cleanUrl)
    return cleanUrl
}

export const getYoutubePreview = (url: string): string | false => {
    if (!url) return false;

    let previewUrl: string | false = false;

    const patterns = ["youtu.be/", "watch?v="];

    patterns.forEach((item) => {
        const keyIndex = url.indexOf(item);

        if (keyIndex !== -1) {
            const videoId = url.substring(keyIndex + item.length).split("&")[0];
            previewUrl = `https://img.youtube.com/vi/${videoId.trim()}/0.jpg`;
        }
    })
    return previewUrl;
}