export const uniqueRoutesHandle = (route, slide, idForRoute = null, reRoute = '') => {
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
    else if (idForRoute && idForRoute.value) {
        return ({ name: route, params: { id: idForRoute.value } })
    }
    else return { name: route, params: { id: slide.id } }
}