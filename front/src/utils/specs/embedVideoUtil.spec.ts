import { repairVideoUrl, getYoutubePreview } from '@/utils/embedVideoUtil';
import { test, expect } from 'vitest';

test('slashWithNoParam', () => {
    expect(repairVideoUrl('')).toBe('/')
})
//youtu.be/", "watch?v=", "/shorts/", "youtube.com/embed/ https://rutube.ru/video/
test('successUrlRepair', () => {
    expect(repairVideoUrl('https://rutube.ru/video/test')).toBe('https://rutube.ru/video/embed/test')
    expect(repairVideoUrl('https://youtube.com/watch?v=/test')).toBe('https://www.youtube.com/embed/test')
    expect(repairVideoUrl('https://youtube.com/shorts/test')).toBe('https://www.youtube.com/embed/test')
    expect(repairVideoUrl('https://youtube.com/embed/test')).toBe('https://www.youtube.com/embed/test')
})

test('successGetYtPreview', () => {
    expect(getYoutubePreview('https://www.youtube.com/watch?v=test')).toBe('https://img.youtube.com/vi/test/0.jpg')
    expect(getYoutubePreview('')).toBe(false)
})