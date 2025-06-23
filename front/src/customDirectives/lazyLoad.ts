import type { Directive } from 'vue'

interface LazyLoadElement extends HTMLElement {
    _lazyObserver?: IntersectionObserver
}

export const vLazyLoad: Directive = {
    mounted(el: LazyLoadElement, binding) {
        const isBackgroundImage = el.tagName !== 'IMG'

        el.classList.add('skeleton-grid__gallery-image')

        const observer = new IntersectionObserver(
            (entries) => {
                entries.forEach((entry) => {
                    if (entry.isIntersecting) {
                        const element = entry.target as HTMLElement
                        const imageUrl = binding.value

                        if (imageUrl) {
                            if (isBackgroundImage) {
                                // Для фоновых изображений
                                const img = new Image()
                                img.onload = () => {
                                    // Убираем skeleton только после полной загрузки
                                    element.style.backgroundImage = `url(${imageUrl})`
                                    element.classList.remove('skeleton-grid__gallery-image')
                                    element.classList.add('lazy-loaded')
                                }
                                img.onerror = () => {
                                    element.style.backgroundImage = `url(https://placehold.co/360x206)`
                                    element.classList.remove('skeleton-grid__gallery-image')
                                    element.classList.add('lazy-error')
                                }
                                // Начинаем загрузку, но skeleton остается до onload
                                img.src = imageUrl
                            } else {
                                // Для img элементов
                                const imgElement = element as HTMLImageElement

                                // Создаем временное изображение для предзагрузки
                                const tempImg = new Image()
                                tempImg.onload = () => {
                                    // Устанавливаем src только после полной загрузки
                                    imgElement.src = imageUrl
                                    imgElement.classList.remove('skeleton-grid__gallery-image')
                                    imgElement.classList.add('lazy-loaded')
                                }
                                tempImg.onerror = () => {
                                    imgElement.src = 'https://placehold.co/360x206'
                                    imgElement.classList.remove('skeleton-grid__gallery-image')
                                    imgElement.classList.add('lazy-error')
                                }
                                // Начинаем предзагрузку
                                tempImg.src = imageUrl
                            }
                            observer.unobserve(element)
                        }
                    }
                })
            },
            {
                threshold: 0.1,
                rootMargin: '50px'
            }
        )

        el._lazyObserver = observer
        observer.observe(el)
    },

    unmounted(el: LazyLoadElement) {
        if (el._lazyObserver) {
            el._lazyObserver.disconnect()
        }
    }
}
