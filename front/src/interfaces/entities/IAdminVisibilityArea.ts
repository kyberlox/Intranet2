
export interface IVisionUser {
    id: number;
    name: string;
    last_name: string;
    second_name: string;
    post: string;
    image?: string;
    depart: string;
    depart_id: number;
}

export interface IDepartment {
    id: number;
    name: string;
    user_head_id: number;
    father_id: null;
    users: IUserSearch[];
    departments: IDepartment[];
}

export interface IUserSearch {
    department: string;
    depart: number;
    depart_id: number;
    name: string;
    id: number;
    user_position: string;
    dep_id: number;
    image?: string;
}

export interface IChoice {
    id: number;
    name: string;
    type: 'allDep' | 'onlyDep' | 'user'
}

export interface IFormattedUserGroup {
    depart: string;
    depart_id: number;
    users: IVisionUser[];
}