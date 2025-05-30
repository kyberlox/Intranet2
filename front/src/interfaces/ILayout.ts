// sidebar
export interface WorkLink {
    title: string;
    href: string;
    description: string;
    linkTitle: string;
    icon: string;
}

export interface SupportLink {
    title: string;
    href: string;
    description: string;
    icon: string;
    linkTitle?: string;
}

export interface ISubPoint {
    id: number;
    name: string;
    href: string;
    params?: {
        id: number;
    };
}
// header
export interface IMenuPoint {
    id: number;
    name: string;
    subPoints: ISubPoint[];
    href?: string;
}

export type MainMenuPoints = IMenuPoint[];
