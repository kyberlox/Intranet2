import type { MainMenuPoints } from "@/interfaces/IMenuPoints";

export const mainMenuPoints: MainMenuPoints = [
    {
        id: 1,
        name: "О нас",
        subPoints: [
            {
                id: 1.1,
                name: "Наша компания",
                href: "personal",
            },
            {
                id: 1.2,
                name: "История компании",
                href: "book-emk",
                params: {
                    id: "0",
                },
            },
            {
                id: 1.3,
                name: "Наши люди",
                href: "our-people",
            },
            {
                id: 1.4,
                name: "Доска почета",
                href: "year-results",
            },
            {
                id: 1.5,
                name: "Блоги",
                href: "blogs",
            },
            {
                id: 1.6,
                name: "Видеоинтервью",
                href: "videoInterviews",
            },
            {
                id: 1.7,
                name: "Учебный центр",
                href: "training",
            },
            {
                id: 1.8,
                name: "Памятка новому сотруднику",
                href: "fornewworker",
            },
            {
                id: 1.9,
                name: "Дни Рождения",
                href: "birthdays",
            },
            {
                id: 1.10,
                name: "Техника безопасности",
                href: "safetytechnics",
            },
            {
                id: 1.10,
                name: "Открытые вакансии",
                href: "vacancies",
            },
            {
                id: 1.11,
                name: "Календарь событий",
                href: "calendar",
            },
        ],
    },
    {
        id: 12,
        name: "Сервисы",
        subPoints: [
            {
                id: 13,
                name: "Подбор оборудования",
                href: "selection",
            },
            {
                id: 14,
                name: "Поздравительная открытка",
                href: "postcard",
            },
            {
                id: 15,
                name: "ChatGpt",
                href: "chatgpt",
            },
            {
                id: 16,
                name: "Разрешительная документация и сертификаты",
                href: "cert",
            },
            {
                id: 17,
                name: "Референсы и опыт поставок",
                href: "experience",
            },
        ],
    },
    {
        id: 18,
        name: "Новости",
        subPoints: [
            {
                id: 19,
                name: "Актуальные новости",
                href: "actualNews",
            },
            {
                id: 20,
                name: "Новости организационного развития",
                href: "corpNews",
            },
            {
                id: 21,
                name: "Корпоративная газета ЭМК",
                href: "gazette",
            },
        ],
    },
    {
        id: 22,
        name: "Галерея",
        subPoints: [
            {
                id: 23,
                name: "Гид по предприятиям",
                href: "factories",
            },
            {
                id: 24,
                name: "Официальные события",
                href: "officialEvents",
            },
        ],
    },
    {
        id: 25,
        name: "Внутренние коммуникации",
        subPoints: [
            {
                id: 26,
                name: "Корпоративные события",
                href: "corporateEvents",
            },
            {
                id: 27,
                name: "Корпоративная жизнь в фото",
                href: "corporateEventsGallery",
            },
            {
                id: 28,
                name: "Афиша",
                href: "eventAnnounces",
            },
            {
                id: 29,
                name: "Предложения партнёров",
                href: "partners",
            },
            {
                id: 30,
                name: "Благотворительные проекты",
                href: "care",
            },
        ],
    },
];