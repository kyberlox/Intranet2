interface IOfficialEvent {
    title: string,
    slides: string[]
}
interface IOfficialEventSlides {
    title: string,
    img: string,
    href: string
}

export const officialEventSlide: IOfficialEvent = {
    title: 'Индийская делегация на САЗ',
    slides: [
        'https://portal.emk.ru/upload/resize_cache/disk/fde/1024_1024_0/43rqquuauv4k1066o2qkjm9qgj9v3g5v.jpg',
        'https://portal.emk.ru/upload/resize_cache/disk/6c8/1024_1024_0/zq108owm0gtchalcst39f99wtsa0p3r7.jpg'
    ]
}

export const officialEventSlides: IOfficialEventSlides[] = [
    {
        title: 'Индийская делегация на САЗ',
        img: 'https://portal.emk.ru/upload/resize_cache/iblock/c0e/a54janbkziy7t6z93gw9ipz3lk83mcn3/296_168_2/DSC_4007-2.jpg',
        href: '1',
    },
]