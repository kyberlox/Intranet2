
export interface IVisionUser {
    id: number;
    name: string;
    last_name: string;
    second_name: string;
    post: string;
    photo: null | string;
    depart: string;
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
    department_id: number;
    user_fio: string;
    user_id: number;
    user_position: string;
    photo: null | string;
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