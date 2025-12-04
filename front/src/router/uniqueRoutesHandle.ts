interface ISlideForUniqueRoute {
    id?: number,
    sectorId?: string,
    factory_id?: string,
    tourId?: string,
    indirect_data?: {
        href?: string
    }
}

export const uniqueRoutesHandle = (
    route: string,
    slide: ISlideForUniqueRoute,
    idForRoute?: number | null,
    reRoute?: string
) => {
    if (reRoute) {
        return { name: reRoute, params: { id: slide.id } }
    }
    else if (route === 'experienceTypes') {
        return { name: route, params: { factoryId: slide?.id } }
    }
    else if (route === 'experienceType') {
        return { name: route, params: { factoryId: slide.id, sectorId: slide.sectorId } }
    }
    else if (route == 'factoryTour') {
        return { name: route, params: { factory_id: slide.factory_id, tourId: slide.tourId } }
    }
    else if (route === 'officialEvents') {
        return { name: 'officialEvent', params: { id: slide?.indirect_data?.href } }
    }
    else if (route == 'ideasPage' || route == 'auth' || route == 'admin') {
        return ({ name: route })
    }
    else if (idForRoute) {
        return ({ name: route, params: { id: idForRoute } })
    }
    else return { name: route, params: { id: slide.id } }
}