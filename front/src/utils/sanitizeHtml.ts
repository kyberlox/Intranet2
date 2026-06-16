import sanitizeHtml from 'sanitize-html';

export const sanitizeValue = (html: string, noTags: boolean = false): string => {
    if (!html) return '';
    console.log(html);

    let cleanHtml = sanitizeHtml(html, {
        allowedTags: noTags ? ['ul'] : ['b', 'i', 'u', 'strong', 'em', 'a', 'p', 'br', 'li', 'ol', 'ul', 'img'],
        allowedAttributes: {
            'a': ['href', 'target', 'rel'],
            'img': ['src']
        },
        allowedStyles: {},
        transformTags: {
            'div': 'p',
            'span': () => ({ tagName: '', attribs: {} }),
        },
        disallowedTagsMode: 'discard'
    }).replaceAll('&nbsp;', ' ');

    cleanHtml = cleanHtml.replace(/<li>\s*<ul/g, '<ul');
    cleanHtml = cleanHtml.replace(/<li>\s*<ol/g, '<ol');
    cleanHtml = cleanHtml.replace(/<\/ol>\s*<\/li>/g, '</ol>');

    return cleanHtml;
};