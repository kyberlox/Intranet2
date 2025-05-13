import type { IBlogArticle } from "@/interfaces/IBlog"

export const blogArticles: IBlogArticle = {
    title: 'Друзина Ирина Алексеевна',
    description: 'Директор по маркетингу </br> АО «НПО «ЭМК»',
    image: 'https://portal.emk.ru/upload/resize_cache/main/3a9/la6p0xocac50n4ai2i4bmu2pdeeeyyqf/360_360_2/%D0%94%D1%80%D1%83%D0%B7%D0%B8%D0%BD%D0%B0.jpg.png',
    href: 'druzina',
    articles: [
        {
            id: 1,
            title: 'Цифровизация в маркетинге',
            date: '14 марта 2024',
            reactions: {
                views: 27,
                likes: {
                    count: 2,
                    mine: false,
                }
            }
        },
        {
            id: 2,
            title: 'Цифровизация за дверью?',
            date: '16 января 2024',
            description: `Существует теория технологических укладов, согласно которой человечество развивается не по спирали, а по синусоиде, и каждый новый цикл определяется масштабным технологическим прорывом и новыми глобальными лидерами. Причем определяет этот технологический прорыв вид энергии, вернее его источник. А какая новая технология определяет нашу реальность? Это IT-технология.`,
            reactions: {
                views: 33,
                likes: {
                    count: 2,
                    mine: false,
                }
            }
        }
    ]
}
