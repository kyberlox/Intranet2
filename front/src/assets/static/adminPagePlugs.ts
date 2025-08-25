interface ISampleEvent {
    name?: string,
    title?: string,
    value?: string | string[] | number,
    type?: string,
    disabled?: boolean,
    options?: string[],
    attached?: string[],
}

export const sampleEvent: ISampleEvent[] = [
    {
        name: 'id',
        title: 'id',
        value: 1,
        type: 'text',
        disabled: true,
    },
    {
        name: 'name',
        title: 'Название',
        value: 'testName',
        type: 'text',
    },
    {
        name: 'preview_text',
        title: 'Текст превью',
        value: 'Текст превью',
        type: 'text',
    },
    {
        name: 'active',
        title: 'Активно',
        value: 'Нет',
        type: 'select',
        options: ['да', 'нет'],
    },
    {
        name: 'date_publiction',
        title: 'Дата публикации',
        value: '02-02-2002',
        type: 'date',
    },
    {
        name: 'date_creation',
        title: 'Дата создания',
        value: '02-02-2002',
        type: 'text',
        disabled: true,
    },
    {
        name: 'content_text',
        title: 'Текст записи',
        value: 'Полный текст записи',
        type: 'textWithRedact',
    },
    {
        name: 'images',
        title: 'Изображения',
        value: [
            'https://placehold.co/360x206',
            'https://placehold.co/360x206',
            'https://placehold.co/360x206',
            'https://placehold.co/360x206',
            'https://placehold.co/360x206',
        ],
        type: 'img',
    },
    {
        name: 'documents',
        title: 'Приложения',
        value: 'test.doc',
        type: 'doc',
        attached: [
            'https://placehold.co/760x1506',
            'https://placehold.co/360x206',
            'https://placehold.co/360x206',
            'https://placehold.co/360x206',
            'https://placehold.co/360x206',
        ],
    },
]