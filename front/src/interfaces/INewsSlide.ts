export interface INewsSlide {
    id?: number;
    name?: string;
    title?: string;
    href?: string;
    hrefId?: string;
    hrefTitle?: string;
    videoHref?: string;
    img?: string | string[];
    reportages?: string | boolean;
    reportsHref?: string;
    tours?: string | boolean;
    toursHref?: string;
}
