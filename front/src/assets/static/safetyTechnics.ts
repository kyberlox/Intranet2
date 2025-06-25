import type { ISafetyTechnicsSlide } from "@/interfaces/IEntities";

export const safetyTechnics: ISafetyTechnicsSlide[] = {
    content: [
        {
            id: 1,
            name: "COVID-19",
            image: "https://portal.emk.ru/local/templates/intranet/img/safety/safety-1.jpg",
            header: "Берегите себя и своих близких",
            subtitle: "COVID-19 — острая респираторная инфекция, вызываемая коронавирусом SARS-CoV-2 (2019-nCoV)",
            description: "Как защитить своё здоровье от потенциальной угрозы",
            routeTo: "safetytechnicsCovid",
        },
        {
            id: 2,
            name: "Пожарная безопасность и эвакуация из офисного здания",
            image: "https://portal.emk.ru/local/templates/intranet/img/safety/safety-2.jpg",
            header: "При пожаре",
            subtitle: "Правила пожарной безопасности и эвакуации из офисного здания",
            description: "Схема эвакуации и что нужно делать при пожаре",
            routeTo: "safetytechnicsCovid",
        },
        {
            id: 3,
            name: "Посещение производственных площадок",
            image: "https://portal.emk.ru/local/templates/intranet/img/safety/safety-3.jpg",
            header: "Техника безопасности на производстве",
            subtitle: "Что нужно знать при посещении производственных площадок",
            description: "Правила для персонала и гостей",
            routeTo: "safetytechnicsCovid",
        }],
    sideInfo: `
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
                Вам никогда не столкнуться с чрезвычайными ситуациями!</strong>`
}

export const safetyTechnicsCovidInner: { id: number, title: string, image: string }[] =
{
    content: [
        {
            id: 1,
            title: 'Соблюдайте социальную дистанцию',
            image: '/src/assets/imgs/about/safetyTechnics/COVID1.jpg',
        },
        {
            id: 2,
            title: 'Ходите в масках и используйте антисептики',
            image: '/src/assets/imgs/about/safetyTechnics/COVID2.jpg',
        },
        {
            id: 3,
            title: 'Старайтесь не приглашать лишних людей в офис',
            image: '/src/assets/imgs/about/safetyTechnics/COVID3.jpg',
        }
    ],
    sideInfo: `<div class="news__detail__discr safety__section__discr">
                    <h2 class="news__detail__title mb-2">Техника безопасности</h2>
                    <p><strong>В течение режима повышенной готовности,</strong> связанного с пандемией COVID-19,
                        сотрудники
                        должны соблюдать следующие правила:</p>
                    <ul class="safety__section__info__list__style">
                        <li>Носить медицинские маски</li>
                        <li>Соблюдать социальную дистанцию 1,5 метра с окружающими людьми</li>
                        <li>Регулярно мыть руки</li>
                        <li>Обрабатывать поверхности антисептиками и санитайзерами</li>
                        <li>Посещение офиса посторонними людьми свести к минимуму</li>
                        <li>По возможности сократить собственные перемещения и командировки</li>
                        <li>Старайтесь сократить участие в мероприятиях с большим количеством людей</li>
                    </ul>
                    <p>При любом недомогании поставьте в известность Вашего руководителя и воздержитесь от посещения
                        офиса.
                        Также оставайтесь дома и обратитесь к врачу, если Вы контактировали с заразившимся COVID-19.</p>
                    <strong>Просим отнестись к этим мерам с пониманием. Будьте ответственны за себя и
                        окружающих.</strong>
                </div>`
}