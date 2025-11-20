export interface IAuth {
    login: string
    password: string
}

export interface IPostIdea {
    NAME?: string
    DETAIL_TEXT?: string
    CREATED_BY?: string
    base_name?: string
    base?: string
}

export interface IPostEventToExcell{
    id: number;
    entryId: string;
    status: string;
}

export interface IValidatePoints {
    action_id: number
    uuid_to: number
}

export interface IUsersLoad {
    art_id: string | null
    users_id: string[]
}

