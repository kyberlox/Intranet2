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
        id: 2,
        name: "Сервисы",
        subPoints: [
            {
                id: 2.1,
                name: "Подбор оборудования (ТЭП)",
                href: "selectionTep",
            },
            {
                id: 2.2,
                name: "Подбор оборудования (Регулятор)",
                href: "selectionReg",
            },
            {
                id: 2.3,
                name: "Поздравительная открытка",
                href: "postcard",
            },
            {
                id: 2.4,
                name: "ChatGpt",
                href: "chatgpt",
            },
            {
                id: 2.5,
                name: "Разрешительная документация и сертификаты",
                href: "cert",
            },
            {
                id: 2.6,
                name: "Референсы и опыт поставок",
                href: "experience",
            },
        ],
    },
    {
        id: 3,
        name: "Новости",
        subPoints: [
            {
                id: 3.1,
                name: "Актуальные новости",
                href: "actualNews",
            },
            {
                id: 3.2,
                name: "Новости организационного развития",
                href: "corpnews",
            },
            {
                id: 3.3,
                name: "Видеорепортажи",
                href: "videoreport",
            },
            {
                id: 3.4,
                name: "Корпоративная газета ЭМК",
                href: "gazette",
            },
        ],
    },
    {
        id: 4,
        name: "Галерея",
        subPoints: [
            {
                id: 4.1,
                name: "Гид по предприятиям",
                href: "factories",
            },
            {
                id: 4.2,
                name: "Официальные события",
                href: "officialEvents",
            },
        ],
    },
    {
        id: 5,
        name: "Внутренние коммуникации",
        subPoints: [
            {
                id: 5.1,
                name: "Корпоративные события",
                href: "corpEvents",
            },
            {
                id: 5.2,
                name: "Корпоративная жизнь в фото",
                href: "corpEventsGallery",
            },
            {
                id: 5.3,
                name: "Афиша",
                href: "eventAnnounces",
            },
            {
                id: 5.4,
                name: "Предложения партнёров",
                href: "partners",
            },
            {
                id: 5.5,
                name: "Благотворительные проекты",
                href: "care",
            },
        ],
    },
];