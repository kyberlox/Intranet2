export type IFactorySlides = {
    id?: number;
    title: string;
    img: string;
    hrefTitle: string;
    reportages: boolean | string;
    reportsHref: string;
    tours: boolean | string;
    toursHref: string;
    factoryId: number;
}

export type IFactoryReport = {
    id?: number;
    title: string;
    img: string;
    href: string;
    videoHref: string;
    factoryId: number;
}

export type IFactoryTours = {
    id: number;
    title: string;
    img: string;
    tourId: string;
    hrefTitle: string;
    hrefId: number;
}