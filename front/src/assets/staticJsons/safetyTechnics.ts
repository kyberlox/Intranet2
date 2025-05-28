import type { ISafetyTechnicsSlide } from "@/interfaces/ISafetyTechnicsSlide";

export const safetyTechnicsSlides: ISafetyTechnicsSlide[] = [
    {
        id: 1,
        title: "COVID-19",
        image: "https://portal.emk.ru/local/templates/intranet/img/safety/safety-1.jpg",
        header: "Берегите себя и своих близких",
        subtitle: "COVID-19 — острая респираторная инфекция, вызываемая коронавирусом SARS-CoV-2 (2019-nCoV)",
        description: "Как защитить своё здоровье от потенциальной угрозы",
        href: "safetytechnicsCovid",
    },
    {
        id: 2,
        title: "Пожарная безопасность и эвакуация из офисного здания",
        image: "https://portal.emk.ru/local/templates/intranet/img/safety/safety-2.jpg",
        header: "При пожаре",
        subtitle: "Правила пожарной безопасности и эвакуации из офисного здания",
        description: "Схема эвакуации и что нужно делать при пожаре",
        href: "safetytechnicsFire",
    },
    {
        id: 3,
        title: "Посещение производственных площадок",
        image: "https://portal.emk.ru/local/templates/intranet/img/safety/safety-3.jpg",
        header: "Техника безопасности на производстве",
        subtitle: "Что нужно знать при посещении производственных площадок",
        description: "Правила для персонала и гостей",
        href: "safetytechnicsFactory",
    },
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