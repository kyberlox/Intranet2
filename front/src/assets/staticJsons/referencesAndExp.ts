import type { IFactorySlides, IFactoryReport, IFactoryTours } from '@/interfaces/IFactorySlides';

export const expSlides: IFactorySlides[] = [
    {
        title: 'ЗАО «Саратовский арматурный завод»',
        img: 'https://portal.emk.ru/upload/iblock/aa0/%D0%97%D0%90%D0%9E%20%C2%AB%D0%A1%D0%B0%D1%80%D0%B0%D1%82%D0%BE%D0%B2%D1%81%D0%BA%D0%B8%D0%B9%20%D0%B0%D1%80%D0%BC%D0%B0%D1%82%D1%83%D1%80%D0%BD%D1%8B%D0%B9%20%D0%B7%D0%B0%D0%B2%D0%BE%D0%B4%C2%BB.png',
        hrefTitle: 'saz',
        reportages: true,
        reportsHref: 'factoriesReports',
        tours: true,
        toursHref: 'factoriesTours',
        id: 1,
        factoryId: 1,
    },
]

export const factoryReports: IFactoryReport[] = [
    {
        title: 'Обучающее видео по неразрушающим методам контроля. Рентген-камера.',
        img: 'https://portal.emk.ru/upload/resize_cache/iblock/cdf/xr0xqd3aeusy50v2fjdm9lqtxdn3tqo8/296_168_2/%D1%80%D0%B5%D0%BF%D0%BE%D1%80%D1%82%D0%B0%D0%B6.png',
        href: 'saz',
        videoHref: 'https://youtu.be/N3YU2u1qe9w?si=Spy8vdIvyZ2oLeWr'
    },
]

export const factoryTours: IFactoryTours[] = [{
    title: 'Цех затворов обратный',
    img: 'https://portal.emk.ru/upload/resize_cache/iblock/fb9/296_168_2/ht_preview_nodeimage_node3.jpg',
    tourId: '3d-01',
    hrefTitle: 'saz',
    hrefId: '1',
    id: 1,
},]

export const slides = [
    {
        id: 1,
        title: 'ЗАО «Саратовский арматурный завод»',
        img: 'https://portal.emk.ru/upload/iblock/aa0/%D0%97%D0%90%D0%9E%20%C2%AB%D0%A1%D0%B0%D1%80%D0%B0%D1%82%D0%BE%D0%B2%D1%81%D0%BA%D0%B8%D0%B9%20%D0%B0%D1%80%D0%BC%D0%B0%D1%82%D1%83%D1%80%D0%BD%D1%8B%D0%B9%20%D0%B7%D0%B0%D0%B2%D0%BE%D0%B4%C2%BB.png',
        href: 'saz',
        factoryId: 1,
        reportages: 1,
        tours: 1,
    },
]

export const expTypeSlides = [
    {
        id: 1,
        title: 'Нефтегаз',
        factoryId: 2,
        img: 'https://portal.emk.ru/upload/resize_cache/iblock/7fe/8cn5xjcv7hbr1127ovzedhjjk489wm8x/380_380_0/%D0%9D%D0%B5%D1%84%D1%82%D0%B5%D0%B3%D0%B0%D0%B7.png',
    }
];