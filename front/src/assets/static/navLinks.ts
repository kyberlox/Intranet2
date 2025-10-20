import PhoneIcon from "@/assets/icons/layout/sidebar/socLinks/PhoneIcon.svg";
import VkIcon from "@/assets/icons/layout/sidebar/socLinks/VkIcon.svg";
import TelegramIcon from "@/assets/icons/layout/sidebar/socLinks/TelegramIcon.svg";
import EmkLogo from "@/assets/icons/layout/sidebar/socLinks/EmkLogo.svg";
import DocsIcon from "@/assets/icons/layout/sidebar/socLinks/DocsIcon.svg";
import MotiwIcon from "@/assets/icons/layout/sidebar/workLinks/MotiwIcon.svg";
import BitrixIcon from "@/assets/icons/layout/sidebar/workLinks/BitrixIcon.svg";

import type { MainMenuPoints, WorkLink, SupportLink } from "@/interfaces/ILayout";

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
                    id: 0,
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
                href: "trainingcenter",
            },
            {
                id: 1.8,
                name: "Памятка новому сотруднику",
                href: "forNewWorker",
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
                id: 1.11,
                name: "Календарь событий",
                href: "calendar",
            },
            {
                id: 1.12,
                name: "Магазин мерча",
                href: "merchStore",
            },
            {
                id: 1.13,
                name: 'Новые сотрудники',
                href: 'newWorkers'
            }
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
                id: 2.51,
                name: "Разрешительная документация и сертификаты (диск U)",
                href: "udocs",
            },
            {
                id: 2.6,
                name: "Референсы и опыт поставок",
                href: "experience",
            },
            {
                id: 2.7,
                name: 'Информационное письмо о компании ЭМК',
                href: 'https://intranet.emk.ru/api/files/Информационное_письмо_НПО_ЭМК.docx',
            }
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
                href: "corpNews",
            },
            {
                id: 3.3,
                name: "Видеорепортажи",
                href: "videoReports",
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
                href: "corpLife",
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
            {
                id: 5.6,
                name: "Открытые вакансии",
                href: "vacancies",
            },
            {
                id: 5.7,
                name: "Конкурс",
                href: "contest",
            },
        ],
    },
];

export const points = [
    {
        id: 1,
        name: 'Моя страница',
        href: 'userPage',
    },
    {
        id: 2,
        name: 'Мои идеи',
        href: 'ideasPage',
    },
    {
        id: 3,
        name: 'Панель редактора',
        href: 'admin'
    },
]

export const workLinks: WorkLink[] = [
    {
        title: "Мотив",
        href: "http://motiw.imp.int/user/",
        description: "Задачи",
        linkTitle: "К задачам",
        icon: MotiwIcon,
    },
    {
        title: "Битрикс24",
        href: "https://portal.emk.ru/company/personal/user/k/tasks/",
        description: "Задачи",
        linkTitle: "К задачам",
        icon: BitrixIcon,
    },
];

export const supportLinks: SupportLink[] = [
    {
        title: "5182",
        href: "tel:#5182",
        description: "Тех. поддержка сайта",
        icon: PhoneIcon,
    },
    {
        title: "Мы в VK",
        href: "https://vk.com/npo_emk",
        description: "https://vk.com/npo_emk",
        icon: VkIcon,
    },
    {
        title: "Мы в Telegram",
        href: "https://t.me/emk_emk",
        description: "@emk_emk",
        icon: TelegramIcon,
    },
    {
        title: "Наш сайт",
        href: "http://www.emk.ru/",
        description: "http://www.emk.ru",
        icon: EmkLogo,
    },
    {
        title: "Редактор Интранет",
        href: "admin",
        description: "Перейти",
        icon: DocsIcon,
    },
];