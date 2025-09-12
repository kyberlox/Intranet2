
interface IAdminSections {
    id: number,
    title: string,
    nav: { name: string, id: string | number, parent_id?: number, sectionHref?: string }[]
}

export const abobus: IAdminSections[] = [
    {
        id: 1, title: 'Разделы', nav: []
    },
    {
        id: 2,
        title: 'Администрирование', nav: [
            { name: 'Администрирование', id: 'pointsAdministrator' },
            { name: 'Модерирование баллов', id: 'pointsModeration' },
        ]
    },
    {
        id: 3,
        title: 'Бальная система', nav: [
            { name: 'Области видимости', id: 'visibilityArea' },
            // { name: 'Файловый менеджер', id: 'fileManager' },
        ]
    }
]