import type { OurPeoplePost } from "@/interfaces/IOurPeoplePost";


export const posts: OurPeoplePost[] = [
    {
        id: 1,
        image: "https://portal.emk.ru/upload/iblock/bb6/opwvwb4yznmcf3x6s0hi58xzoi3ml7q1/1_small.jpg",
        title: "«Мы – настоящая команда»: программисты Саша и Игорь о работе в ЭМК",
        reactions: {
            views: 12,
            likes: { count: 13, likedByMe: 1 },
        },
        href: "our-people-interview",
    },
]