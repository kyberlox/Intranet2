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

export interface IValidatePoints {
    action_id: number
    uuid_to: number
}

export interface IUsersLoad {
    art_id: string | undefined
    users_id: string[]
}
