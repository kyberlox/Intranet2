interface IAdminSections {
    name: string,
    link: string
}

export const AdminSections: IAdminSections[] = [
    { name: 'Области видимости', link: 'visibilityArea' },
    { name: 'Файловый менеджер', link: 'fileManager' },
    { name: 'Панель администратора', link: 'pointsAdministrator' },
]

export const PointsSection: IAdminSections[] = [
    { name: 'Администрирование', link: 'pointsAdministrator' },
    { name: 'Модерирование баллов', link: 'pointsModeration' },
]