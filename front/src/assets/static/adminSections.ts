interface IAdminSections {
    name: string,
    link: string
}

export const AdminSections: IAdminSections[] = [
    { name: 'Области видимости', link: 'visibilityArea' },
    { name: 'Файловый менеджер', link: 'fileManager' }];