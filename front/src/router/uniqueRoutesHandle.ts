import type { IUnionEntities, IFactorySlides } from "@/interfaces/IEntities";
import { useUserData } from "@/stores/userData";

export const uniqueRoutesHandle = (
    route: string,
    slide: IUnionEntities,
    idForRoute?: number | null,
    reRoute?: string
) => {
    if (reRoute) {
        return { name: reRoute, params: { id: slide.id } }
    }
    else if (route === 'experienceType') {
        const typedSlide = slide as IFactorySlides
        return { name: route, params: { id: typedSlide.id, factoryId: typedSlide?.indirect_data?.factoryId } }
    }
    else if (route === 'experienceTypes') {
        const typedSlide = slide as IFactorySlides
        return { name: route, params: { factoryId: typedSlide?.indirect_data?.factoryId } }
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