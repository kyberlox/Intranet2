export interface IAllCources {
    id: number;
    name: string;
    img: string;
    structure: string[];
    additionalInfo: {
        title: string, text: string
    }[];
}