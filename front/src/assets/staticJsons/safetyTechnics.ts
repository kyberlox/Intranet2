import type { ISafetyTechnicsSlide } from "@/interfaces/IEntities";

export const safetyTechnicsSlides: ISafetyTechnicsSlide[] = [
    {
        id: 1,
        name: "COVID-19",
        // image: "https://portal.emk.ru/local/templates/intranet/img/safety/safety-1.jpg",
        // header: "Берегите себя и своих близких",
        // subtitle: "COVID-19 — острая респираторная инфекция, вызываемая коронавирусом SARS-CoV-2 (2019-nCoV)",
        // description: "Как защитить своё здоровье от потенциальной угрозы",
        // href: "safetytechnicsCovid",
        indirect_data: {
            "ID": "5259",
            "IBLOCK_ID": "56",
            "NAME": "Фонд «Забытые живые» ",
            "CREATED_BY": "970",
            "BP_PUBLISHED": "Y",
            "PROPERTY_342": [
                "134718"
            ],
            "PROPERTY_343": [
                "125207"
            ],
            "PROPERTY_344": [
                "Пожилые люди"
            ],
            "PROPERTY_435": [
                "Кириллова Ирина"
            ],
            "PROPERTY_347": [
                "8 (927) 223-58-01"
            ],
            "PROPERTY_348": [
                {
                    "TYPE": "HTML",
                    "TEXT": "<p>\r\n</p>\r\n<div>\r\n\t Фонд «Забытые живые» - фонд помощи старикам, пожилым и часто одиноким людям. Уже на протяжении 2-х лет совместно со всеми сотрудниками ЭМК мы закупаем новогодние подарки для подопечных фонда, в виде продуктовых корзин к Новому году. Мы будем рады любой помощи!\r\n</div>\r\n<p>\r\n</p>\r\n <br>"
                }
            ],
            "PROPERTY_349": [
                "40"
            ]
        },
    },
    {
        id: 2,
        name: "Пожарная безопасность и эвакуация из офисного здания",
        // image: "https://portal.emk.ru/local/templates/intranet/img/safety/safety-2.jpg",
        // header: "При пожаре",
        // subtitle: "Правила пожарной безопасности и эвакуации из офисного здания",
        // description: "Схема эвакуации и что нужно делать при пожаре",
        // href: "safetytechnicsFire",
        indirect_data: {
            "ID": "5259",
            "IBLOCK_ID": "56",
            "NAME": "Фонд «Забытые живые» ",
            "CREATED_BY": "970",
            "BP_PUBLISHED": "Y",
            "PROPERTY_342": [
                "134718"
            ],
            "PROPERTY_343": [
                "125207"
            ],
            "PROPERTY_344": [
                "Пожилые люди"
            ],
            "PROPERTY_435": [
                "Кириллова Ирина"
            ],
            "PROPERTY_347": [
                "8 (927) 223-58-01"
            ],
            "PROPERTY_348": [
                {
                    "TYPE": "HTML",
                    "TEXT": "<p>\r\n</p>\r\n<div>\r\n\t Фонд «Забытые живые» - фонд помощи старикам, пожилым и часто одиноким людям. Уже на протяжении 2-х лет совместно со всеми сотрудниками ЭМК мы закупаем новогодние подарки для подопечных фонда, в виде продуктовых корзин к Новому году. Мы будем рады любой помощи!\r\n</div>\r\n<p>\r\n</p>\r\n <br>"
                }
            ],
            "PROPERTY_349": [
                "40"
            ]
        },
    },
    {
        id: 3,
        name: "Посещение производственных площадок",
        // image: "https://portal.emk.ru/local/templates/intranet/img/safety/safety-3.jpg",
        // header: "Техника безопасности на производстве",
        // subtitle: "Что нужно знать при посещении производственных площадок",
        // description: "Правила для персонала и гостей",
        // href: "safetytechnicsFactory",
        indirect_data: {
            "ID": "5259",
            "IBLOCK_ID": "56",
            "NAME": "Фонд «Забытые живые» ",
            "CREATED_BY": "970",
            "BP_PUBLISHED": "Y",
            "PROPERTY_342": [
                "134718"
            ],
            "PROPERTY_343": [
                "125207"
            ],
            "PROPERTY_344": [
                "Пожилые люди"
            ],
            "PROPERTY_435": [
                "Кириллова Ирина"
            ],
            "PROPERTY_347": [
                "8 (927) 223-58-01"
            ],
            "PROPERTY_348": [
                {
                    "TYPE": "HTML",
                    "TEXT": "<p>\r\n</p>\r\n<div>\r\n\t Фонд «Забытые живые» - фонд помощи старикам, пожилым и часто одиноким людям. Уже на протяжении 2-х лет совместно со всеми сотрудниками ЭМК мы закупаем новогодние подарки для подопечных фонда, в виде продуктовых корзин к Новому году. Мы будем рады любой помощи!\r\n</div>\r\n<p>\r\n</p>\r\n <br>"
                }
            ],
            "PROPERTY_349": [
                "40"
            ]
        },
    }
];

export const sideInfoBlock: string = `
            <h4>Техника безопасности</h4>
            <strong>Уважаемые Коллеги!</strong>
            <p>Согласно правилам техники безопасности, мы хотели бы обратить Ваше внимание на следующие
                параграфы:</p>
            <ul class="">
                <li><a href="COVID-19/">COVID-19</a></li>
                <li><a href="fire-safety/">Пожарная безопасность</a> и <a href="evacuation/">эвакуация</a> из офисного здания
                </li>
                <li>Посещение производственных площадок для
                    персонала и гостей
                </li>
            </ul>
            <strong>Соблюдайте эти простые правила</strong>
            <p>Техника безопасности — это система правил и норм, которая призвана сделать все возможное, чтобы не
                допустить неблагоприятного воздействия опасных факторов на человека.</p>
            <strong>Соблюдая эти правила и инструкции, Вы сможете избежать опасности для себя и окружающих. Желаем
                Вам никогда не столкнуться с чрезвычайными ситуациями!</strong>

        `;


export const safetyTechnicsCovid: { id: number, title: string, image: string }[] = [{
    id: 1,
    title: 'Соблюдайте социальную дистанцию',
    image: 'https://portal.emk.ru/local/templates/intranet/img/safety/COVID-19/COVID-19-1.jpg'
}]