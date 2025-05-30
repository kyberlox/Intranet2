export const uniqueRoutesHandle = (
    route: string,
    slide: { id: number, factoryId?: number, tourId?: string, href?: string },
    idForRoute?: number | null,
    reRoute?: string
) => {
    if (reRoute) {
        return { name: reRoute, params: { id: slide.id } }
    }
    else if (route === 'experienceType') {
        return { name: route, params: { id: slide.id, factoryId: slide.factoryId } }
    }
    else if (route === 'experienceTypes') {
        return { name: route, params: { factoryId: slide.factoryId } }
    }
    else if (route == 'factoryTour') {
        return { name: route, params: { id: slide.id, tourId: slide.tourId } }
    }
    else if (route === 'officialEvents') {
        return { name: 'officialEvent', params: { id: slide.href } }
    }
    else if (route == 'logout' || route == 'ideasPage' || route == 'auth' || route == 'admin') {
        return ({ name: route })
    }
    else if (idForRoute) {
        return ({ name: route, params: { id: idForRoute } })
    }
    else return { name: route, params: { id: slide.id } }
}