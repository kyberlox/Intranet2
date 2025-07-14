import type { IUnionEntities, IFactorySlides, IFactoryData } from "@/interfaces/IEntities";

export const uniqueRoutesHandle = (
    route: string,
    slide: IUnionEntities,
    idForRoute?: number | null,
    reRoute?: string
) => {
    if (reRoute) {
        return { name: reRoute, params: { id: slide.id } }
    }
    else if (route === 'experienceTypes') {
        const typedSlide = slide as IFactoryData;
        return { name: route, params: { factoryId: typedSlide?.id } }
    }
    else if (route === 'experienceType') {
        const typedSlide = slide as IFactoryData;
        return { name: route, params: { factoryId: typedSlide.id, sectorId: typedSlide.sectorId } }
    }
    else if (route == 'factoryTour') {
        const typedSlide = slide as IFactorySlides
        return { name: route, params: { id: slide.id, tourId: typedSlide?.indirect_data?.tourId } }
    }
    else if (route === 'officialEvents') {
        const typedSlide = slide as IFactorySlides
        return { name: 'officialEvent', params: { id: typedSlide?.indirect_data?.href } }
    }
    else if (route == 'ideasPage' || route == 'auth' || route == 'admin') {
        return ({ name: route })
    }
    else if (idForRoute) {
        return ({ name: route, params: { id: idForRoute } })
    }
    else return { name: route, params: { id: slide.id } }
}