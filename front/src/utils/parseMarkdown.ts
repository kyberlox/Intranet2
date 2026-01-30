import MarkdownIt from 'markdown-it';

const md = new MarkdownIt({
    html: true,
    linkify: true,
    typographer: false,
    breaks: true,
});

export const parseMarkdown = (markdown: string): string => {
    return md.render(markdown ?? '');
};
