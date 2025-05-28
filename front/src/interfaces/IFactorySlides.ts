export type IFactorySlides = {
    id?: number;
    title: string;
    img: string;
    hrefTitle: string;
    reportages: boolean | string;
    reportsHref: string;
    tours: boolean | string;
    toursHref: string;
}

export type IFactoryReport = {
    id?: number;
    title: string;
    img: string;
    href: string;
    videoHref: string;
}

export type IFactoryTours = {
    title: string;
    img: string;
    tour: string;
    hrefTitle: string;
    hrefId: string;
}