import type { Ref } from "vue"

export const screenCheck = (width: Ref<number>) => {

    switch (true) {
        case width.value <= 768:
            return 'sm'
        case width.value <= 992:
            return 'md'
        case width.value <= 1200:
            return 'lg'
        case width.value <= 1400:
            return 'xl'
        case width.value > 1400:
            return 'xxl'
        default:
            return 'none';
    }
}
