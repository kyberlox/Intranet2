export interface WorkersOfTheYear {
    [year: number]: {
        id: number;
        name: string;
        position: string;
        department: string;
        photo: string;
        description?: string;
    }[];
}

