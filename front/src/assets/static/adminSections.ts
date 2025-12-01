
interface IAdminSections {
    id: number,
    title: string,
    nav: { name: string, id: string | number, parent_id?: number, sectionHref?: string }[]
}

export const staticAdminSections: IAdminSections[] = [
    {
        id: 1, title: 'Разделы', nav: []
    },
    {
        id: 2,
        title: 'Администрирование', nav: [
            { name: 'Области видимости', id: 'visibilityArea' },
        ]
    },
    {
        id: 3,
        title: 'Бальная система', nav: [
            { name: 'Администрирование', id: 'pointsAdministrator' },
            { name: 'Модерирование баллов', id: 'pointsModeration' },
            { name: 'История начислений баллов', id: 'curatorHistory' },
        ]
    },
    {
        id: 4,
        title: 'Настройка прав',
        nav: [{ name: 'Права на разделы', id: 'roots' },]
    }
]
