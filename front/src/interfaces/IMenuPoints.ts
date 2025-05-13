export interface ISubPoint {
    id: number;
    name: string;
    href: string;
    params?: {
        id: string;
    };
}

export interface IMenuPoint {
    id: number;
    name: string;
    subPoints: ISubPoint[];
    href?: string;
}

export type MainMenuPoints = IMenuPoint[];
