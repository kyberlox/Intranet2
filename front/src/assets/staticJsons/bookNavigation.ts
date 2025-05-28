
import type { IBook } from '@/interfaces/IBook';

export const bookNavigation: IBook[] = [
    {
        name: "Вступление",
        href: {
            name: "book-emk-page",
            params: {
                id: 0,
            },
        },
        subpages: [],
    },
    {
        name: "Часть 1. 1991–1997 гг.",
        id: "p1",
        subpages: [
            {
                name: "Глава 1. Простор",
                href: {
                    name: "book-emk-page",
                    params: {
                        id: 1,
                    },
                },
            },
            {
                name: "Глава 2. Разрыв",
                href: {
                    name: "book-emk-page",
                    params: {
                        id: 2,
                    },
                },
            },
            {
                name: "Глава 3. Команда",
                href: {
                    name: "book-emk-page",
                    params: {
                        id: 3,
                    },
                },
            },
            {
                name: "Глава 4. Эпоха бартера",
                href: {
                    name: "book-emk-page",
                    params: {
                        id: 4,
                    },
                },
            },
            {
                name: "Глава 5. Система управления",
                href: {
                    name: "book-emk-page",
                    params: {
                        id: 5,
                    },
                },
            },
        ],
    },
    {
        name: "Часть 2. 1996–2004 гг.",
        id: "p2",
        subpages: [
            {
                name: "Глава 6. Обретение ИФАЗа",
                href: {
                    name: "book-emk-page",
                    params: {
                        id: 6,
                    },
                },
            },
            {
                name: "Глава 7. Украинская арматура",
                href: {
                    name: "book-emk-page",
                    params: {
                        id: 7,
                    },
                },
            },
            {
                name: "Глава 8. Атомная тема",
                href: {
                    name: "book-emk-page",
                    params: {
                        id: 8,
                    },
                },
            },
            {
                name: "Глава 9. Рождение САЗа",
                href: {
                    name: "book-emk-page",
                    params: {
                        id: 9,
                    },
                },
            },
            {
                name: "Глава 10. Тульский проект",
                href: {
                    name: "book-emk-page",
                    params: {
                        id: 10,
                    },
                },
            },
            {
                name: "Глава 11. Расцвет нулевых",
                href: {
                    name: "book-emk-page",
                    params: {
                        id: 11,
                    },
                },
            },
        ],
    },
    {
        name: "Часть 3. 2003–2010 гг.",
        id: "p3",
        subpages: [
            {
                name: "Глава 12. Ассоциация и журнал",
                href: {
                    name: "book-emk-page",
                    params: {
                        id: 12,
                    },
                },
            },
            {
                name: "Глава 13. Два холдинга с разной судьбой",
                href: {
                    name: "book-emk-page",
                    params: {
                        id: 13,
                    },
                },
            },
            {
                name: "Глава 14. Хроника распада партнёрства",
                href: {
                    name: "book-emk-page",
                    params: {
                        id: 14,
                    },
                },
            },
            {
                name: "Глава 15. Становление собственного производства",
                href: {
                    name: "book-emk-page",
                    params: {
                        id: 15,
                    },
                },
            },
        ],
    },
    {
        name: "Часть 4. 2009–2016 гг.",
        id: "p4",
        subpages: [
            {
                name: "Глава 16. Как закалялся САЗ",
                href: {
                    name: "book-emk-page",
                    params: {
                        id: 16,
                    },
                },
            },
            {
                name: "Глава 17. Трудный путь в атомную отрасль",
                href: {
                    name: "book-emk-page",
                    params: {
                        id: 17,
                    },
                },
            },
            {
                name: "Глава 18. Регулятор",
                href: {
                    name: "book-emk-page",
                    params: {
                        id: 18,
                    },
                },
            },
            {
                name: "Глава 19. Люди и проекты",
                href: {
                    name: "book-emk-page",
                    params: {
                        id: 19,
                    },
                },
            },
        ],
    },
    {
        name: "ВЗГЛЯД В БУДУЩЕЕ",
        href: {
            name: "book-emk-page",
            params: {
                id: 20,
            },
        },
        subpages: [],
    },
];
