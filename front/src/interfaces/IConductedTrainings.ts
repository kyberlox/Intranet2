export interface ICounductedTraining {
    id: number;
    title: string;
    subtitle: string | null;
    score: number;
    reviewsCount: number | null;
    date: string;
    author: string;
    description?: string;
    link?: string;
}

export interface IConductedTrainings {
    [key: string]: ICounductedTraining[];
}